import importlib.util
from types import ModuleType

from infra.pulumi.pulumi_service import PULUMI_PROJECT_DIR

_POLICY_FILE = PULUMI_PROJECT_DIR / "modules" / "policy.py"
_cached: ModuleType | None = None


def load_policy() -> ModuleType:
    """Carrega infra/pulumi/modules/policy.py (fonte única das regras), sem importar o pacote pulumi."""
    global _cached
    if _cached is None:
        spec = importlib.util.spec_from_file_location("cloudwise_policy", _POLICY_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _cached = module
    return _cached
