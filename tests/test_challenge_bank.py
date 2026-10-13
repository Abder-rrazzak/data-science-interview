"""Run all challenge reference tests independently (including numeric tolerances)."""
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
CHALLENGES = sorted((ROOT / "python" / "coding_challenges").glob("[0-9]*_*"))

@pytest.mark.parametrize("folder", CHALLENGES, ids=lambda p: p.name)
def test_reference_solution(folder):
    spec = importlib.util.spec_from_file_location(f"challenge_{folder.name}", folder / "solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import ast
    text = (folder / "test_solution.py").read_text(encoding="utf-8")
    test = ast.parse(text)
    assertion = next(node for node in ast.walk(test) if isinstance(node, ast.Assert))
    expr = ast.Expression(assertion.test)
    assert eval(compile(expr, str(folder / "test_solution.py"), "eval"), {"solve": module.solve})
