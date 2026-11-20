import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any

from infra.config import get_settings

# pulumi_service.py -> pulumi -> infra -> src -> backend -> <raiz do repositorio>
logger = logging.getLogger(__name__)

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
            # Credenciais lidas pelo provider azure-native
            "ARM_CLIENT_ID": s.azure_client_id,
            "ARM_CLIENT_SECRET": s.azure_client_secret,
            "ARM_TENANT_ID": s.azure_tenant_id,
            "ARM_SUBSCRIPTION_ID": s.azure_subscription_id,
            # Backend local (estado em arquivo) e senha dos segredos
            "PULUMI_BACKEND_URL": f"file://{self._state_dir()}",
            "PULUMI_CONFIG_PASSPHRASE": s.pulumi_config_passphrase,
            # Garante que o programa Pulumi use o Python do venv do backend
            "PULUMI_PYTHON_CMD": sys.executable,
            "PATH": os.environ.get("PATH", ""),
        }

    def _run_up(self, stack_name: str, config: dict[str, Any]) -> dict[str, Any]:
        import pulumi.automation as auto

        missing = [
            k for k in ("ARM_CLIENT_ID", "ARM_CLIENT_SECRET", "ARM_TENANT_ID", "ARM_SUBSCRIPTION_ID")
            if not self._env_vars()[k]
        ]
        if missing:
            raise RuntimeError(f"Credenciais Azure ausentes no .env: {', '.join(missing)}")

        stack = auto.create_or_select_stack(
            stack_name=stack_name,
            project_name="cloud-wise",
            work_dir=str(PULUMI_PROJECT_DIR),
            opts=auto.LocalWorkspaceOptions(env_vars=self._env_vars()),
        )

        stack.set_config("resource_name", auto.ConfigValue(value=config["resource_name"]))
        stack.set_config("environment", auto.ConfigValue(value=config["environment"]))
        stack.set_config("location", auto.ConfigValue(value=config.get("location", "eastus")))
        stack.set_config("template", auto.ConfigValue(value=config.get("template", "rg-storage")))
        stack.set_config("owner", auto.ConfigValue(value=config.get("owner", "unknown")))
        stack.set_config("request_id", auto.ConfigValue(value=config.get("request_id", "0000")))

        result = stack.up(on_output=lambda msg: logger.info("pulumi[%s] %s", stack_name, msg.rstrip()))
        return {name: output.value for name, output in result.outputs.items()}
