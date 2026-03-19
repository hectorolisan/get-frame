import sys

from functools import wraps
from rich.console import Console
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')
console = Console()

def print_styled(
    message: str,
    error_type: str | None = None,
    color: str = "white"
) -> None:
    """Imprime un mensaje con estilo usando rich."""
    console.print(f"[{color}]{f'❌ ({error_type}) ' if error_type else ''}{message}[/{color}]")

def handle_errors(error_message: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorador para manejar excepciones y mostrar errores con estilo."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_type = type(e).__name__
                print_styled(
                    message=f"{error_message}: {str(e)}\n",
                    error_type=error_type,
                    color="red"
                )
                sys.exit(1)
                raise
        return wrapper
    return decorator
