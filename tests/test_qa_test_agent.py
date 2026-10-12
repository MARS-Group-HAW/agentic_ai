import json

from langchain_core.messages import AIMessage

from src.agents.qa_test_agent import QATestRequest, run_qa_agent, run_pytest_tool


class FakeLLM:
    def invoke(self, messages):
        return AIMessage(
            content=json.dumps(
                {
                    "status": "passed",
                    "summary": "QA agent verified the selected pytest target.",
                    "pytest_exit_code": 0,
                    "findings": [],
                    "human_approval_required": True,
                }
            )
        )


def test_pytest_tool_rejects_paths_outside_tests() -> None:
    try:
        run_pytest_tool("src/app/main.py", 10)
    except ValueError:
        pass
    else:
        raise AssertionError("pytest target outside tests/ should be rejected")


def test_qa_agent_returns_structured_result_and_trace(tmp_path) -> None:
    trace_file = tmp_path / "qa-trace.jsonl"
    result = run_qa_agent(
        QATestRequest(
            task_id="TEST-QA-001",
            pytest_target="tests/starter/test_api.py",
            timeout_seconds=30,
        ),
        llm=FakeLLM(),
        trace_file=str(trace_file),
    )

    assert result.status == "passed"
    assert result.pytest_exit_code == 0
    assert result.human_approval_required is True

    trace = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace["task_id"] == "TEST-QA-001"
    assert trace["agent"] == "qa-test-agent"
    assert "run_pytest_tool" in trace["tools"]
