import importlib.util
from functools import cache
from types import ModuleType

from infra.pulumi.pulumi_service import PULUMI_PROJECT_DIR

_POLICY_FILE = PULUMI_PROJECT_DIR / "modules" / "policy.py"


@cache
def load_policy() -> ModuleType:
    """Loads infra/pulumi/modules/policy.py (single source of the rules)
    without importing pulumi."""
    spec = importlib.util.spec_from_file_location("cloudwise_policy", _POLICY_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
