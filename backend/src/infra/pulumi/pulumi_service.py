import asyncio
from typing import Any

from infra.config import get_settings


class PulumiService:
    def __init__(self) -> None:
        self._settings = get_settings()

    async def up(self, stack_name: str, config: dict[str, Any]) -> None:
        await asyncio.to_thread(self._run_up, stack_name, config)

    def _run_up(self, stack_name: str, config: dict[str, Any]) -> None:
        import pulumi.automation as auto

        work_dir = "infra/pulumi"
        stack = auto.create_or_select_stack(
            stack_name=stack_name,
            project_name="cloud-wise",
            work_dir=work_dir,
        )

        stack.set_config("resource_name", auto.ConfigValue(value=config["resource_name"]))
        stack.set_config("environment", auto.ConfigValue(value=config["environment"]))
        stack.set_config("location", auto.ConfigValue(value=config.get("location", "eastus")))

        stack.up(on_output=lambda msg: None)
