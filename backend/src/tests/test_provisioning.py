import pytest
from httpx import AsyncClient

from infra.config import Settings

PAYLOAD = {"template_id": "rg-storage", "resource_name": "fake-run", "environment": "dev", "location": "eastus"}
CTRL = "infra.http.controllers.runops_controller"


class SuccessRunner:
    calls: list = []

    async def up(self, stack_name, config):
        SuccessRunner.calls.append((stack_name, config))
        return {"resource_group_name": "rg-fake-run-dev", "storage_account_name": "safakerundev1234"}


class FailingRunner:
    async def up(self, stack_name, config):
        raise RuntimeError("quota exceeded in eastus")


async def _create_and_get(client, login, user):
    headers = login(user, "runops.provisioner")
    created = await client.post("/api/v1/runops/provision", json=PAYLOAD, headers=headers)
    assert created.status_code == 202
    return (await client.get(f"/api/v1/runops/status/{created.json()['id']}", headers=headers)).json()


async def test_background_run_marks_success(client: AsyncClient, login, monkeypatch):
    monkeypatch.setattr(f"{CTRL}.PulumiService", SuccessRunner)
    body = await _create_and_get(client, login, "runner-ok")
    assert body["status"] == "success"
    stack, config = SuccessRunner.calls[-1]
    assert stack == f"provision-{body['id']}" and config["owner"] == "runner-ok"
    assert body["outputs"] == {
        "resource_group_name": "rg-fake-run-dev",
        "storage_account_name": "safakerundev1234",
    }


async def test_runner_failure_is_recorded_with_message(client: AsyncClient, login, monkeypatch):
    monkeypatch.setattr(f"{CTRL}.PulumiService", FailingRunner)
    body = await _create_and_get(client, login, "runner-fail")
    assert body["status"] == "failed"
    assert "quota exceeded" in body["error_message"]


async def test_unexpected_crash_never_leaves_request_running(client: AsyncClient, login, monkeypatch):
    async def boom(self, provision_id):
        raise RuntimeError("db connection lost")

    monkeypatch.setattr(f"{CTRL}.ExecuteProvisionUseCase.execute", boom)
    body = await _create_and_get(client, login, "runner-crash")
    assert body["status"] == "failed"
    assert "db connection lost" in body["error_message"]


def test_settings_require_secrets_outside_development(monkeypatch):
    for var in ("SECRET_KEY", "PULUMI_CONFIG_PASSPHRASE"):
        monkeypatch.delenv(var, raising=False)
    with pytest.raises(ValueError):
        Settings(app_env="production", _env_file=None)
    ok = Settings(app_env="production", secret_key="s3cret", pulumi_config_passphrase="p4ss", _env_file=None)
    assert ok.secret_key == "s3cret"
    dev = Settings(app_env="development", _env_file=None)
    assert dev.secret_key and dev.pulumi_config_passphrase


def test_storage_account_name_is_valid_and_unique_per_request():
    from infra.pulumi.policy_loader import load_policy

    policy = load_policy()
    a = policy.storage_account_name("my-long-resource-nm", "prod", "1234abcd-0000")
    b = policy.storage_account_name("my-long-resource-nm", "prod", "9999ffff-0000")
    assert a != b
    assert 3 <= len(a) <= 24 and a.isalnum() and a == a.lower()


class VerboseFailingRunner:
    async def up(self, stack_name, config):
        raise RuntimeError(
            "update failed\n" + "diagnostics: lots of noise\n" * 40
            + "error: Code=\"InvalidResourceName\" Message=\"name already taken\"\n"
            + "error: Code=\"InvalidResourceName\" Message=\"name already taken\"\n"
        )


async def test_long_pulumi_error_is_summarized(client: AsyncClient, login, monkeypatch):
    monkeypatch.setattr(f"{CTRL}.PulumiService", VerboseFailingRunner)
    body = await _create_and_get(client, login, "runner-verbose")
    assert body["status"] == "failed"
    assert body["error_message"] == 'error: Code="InvalidResourceName" Message="name already taken"'
    assert body["outputs"] == {}


def test_summarize_error_truncates_and_has_fallback():
    from domain.runops.application.errors.summarize_error import MAX_LENGTH, summarize_error

    assert len(summarize_error("error: " + "x" * 2000)) == MAX_LENGTH
    assert summarize_error("a\nb\nc\nd\ne") == "c | d | e"
    assert summarize_error("") == "Unknown provisioning failure"
