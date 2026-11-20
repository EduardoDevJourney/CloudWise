import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any

from infra.config import get_settings

logger = logging.getLogger(__name__)

# this file -> pulumi -> infra -> src -> backend -> repo root
REPO_ROOT = Path(__file__).resolve().parents[4]
PULUMI_PROJECT_DIR = REPO_ROOT / "infra" / "pulumi"


class PulumiService:
    def __init__(self) -> None:
        self._settings = get_settings()

    async def up(self, stack_name: str, config: dict[str, Any]) -> dict[str, Any]:
        return await asyncio.to_thread(self._run_up, stack_name, config)

    def _state_dir(self) -> Path:
        state_dir = Path(self._settings.pulumi_state_dir)
        if not state_dir.is_absolute():
            state_dir = REPO_ROOT / state_dir
        state_dir.mkdir(parents=True, exist_ok=True)
        return state_dir

    def _env_vars(self) -> dict[str, str]:
        s = self._settings
        return {
            "ARM_CLIENT_ID": s.azure_client_id,
            "ARM_CLIENT_SECRET": s.azure_client_secret,
            "ARM_TENANT_ID": s.azure_tenant_id,
            "ARM_SUBSCRIPTION_ID": s.azure_subscription_id,
            "PULUMI_BACKEND_URL": f"file://{self._state_dir()}",
            "PULUMI_CONFIG_PASSPHRASE": s.pulumi_config_passphrase,
            # the Pulumi program has to run on the backend's venv interpreter
            "PULUMI_PYTHON_CMD": sys.executable,
            "PATH": os.environ.get("PATH", ""),
        }

    def _run_up(self, stack_name: str, config: dict[str, Any]) -> dict[str, Any]:
        import pulumi.automation as auto

        env = self._env_vars()
        missing = [
            k
            for k in ("ARM_CLIENT_ID", "ARM_CLIENT_SECRET", "ARM_TENANT_ID", "ARM_SUBSCRIPTION_ID")
            if not env[k]
        ]
        if missing:
            raise RuntimeError(f"Missing Azure credentials in .env: {', '.join(missing)}")

        stack = auto.create_or_select_stack(
            stack_name=stack_name,
            project_name="cloud-wise",
            work_dir=str(PULUMI_PROJECT_DIR),
            opts=auto.LocalWorkspaceOptions(env_vars=env),
        )

        stack_config = {
            "resource_name": config["resource_name"],
            "environment": config["environment"],
            "location": config.get("location", "eastus"),
            "template": config.get("template", "rg-storage"),
            "owner": config.get("owner", "unknown"),
            "request_id": config.get("request_id", "0000"),
        }
        for key, value in stack_config.items():
            stack.set_config(key, auto.ConfigValue(value=value))

        result = stack.up(
            on_output=lambda msg: logger.info("pulumi[%s] %s", stack_name, msg.rstrip())
        )
        return {name: output.value for name, output in result.outputs.items()}
