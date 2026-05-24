from typing import Optional, Tuple, Callable, Any
import functools
from .utils import EngineConfig, ModelRegistry
from .action_gate import ActionGate

class ThreeSFilter:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = EngineConfig.load(config_path)
        self.registry = ModelRegistry(self.config)
        self.gate = ActionGate(self.registry)

    def evaluate(self, text: str, expected_intent: Optional[str] = None) -> Tuple[str, dict]:
        """
        Evaluate an agent output.
        Returns: (decision, report)
        """
        return self.gate.evaluate(text, expected_intent)

    def monitor(self, expected_intent: Optional[str] = None):
        """
        Decorator to monitor a function that returns agent output.
        If decision is BLOCK, it raises a PermissionError.
        """
        def decorator(func: Callable[..., str]):
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> str:
                output = func(*args, **kwargs)
                decision, report = self.evaluate(output, expected_intent)
                if decision == "BLOCK":
                    raise PermissionError(f"3S_Filter BLOCKED action: {report}")
                return output
            return wrapper
        return decorator

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
