from unittest.mock import MagicMock

from declarai.orchestrator.task_orchestrator import LLMTaskOrchestrator


def test_task_orchestrator():
    operator = MagicMock()
    instantiated_operator = MagicMock()
    operator.return_value = instantiated_operator

    instantiated_operator.compile.return_value = "compiled_result"
    instantiated_operator.predict.return_value = "predicted_result"

    def test_task() -> str:
        pass

    task_orchestrator = LLMTaskOrchestrator(test_task, operator)
    assert task_orchestrator.compile() == "compiled_result"

    # TODO: Implement test when plan is implemented
    # task_orchestrator.plan()

    res = task_orchestrator()
    assert res == "predicted_result"
