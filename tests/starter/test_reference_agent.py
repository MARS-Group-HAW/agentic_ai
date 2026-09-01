import json

from langchain_core.messages import AIMessage

from examples.file_review_agent import (
    read_repository_text_file,
    run_review,
)


class FakeLLM:
    def invoke(self, messages):
        return AIMessage(
            content=json.dumps(
                {
                    "status": "approved",
                    "summary": "Starter fake review completed.",
                    "findings": [],
                }
            )
        )


def test_safe_file_tool_reads_repository_file() -> None:
    content = read_repository_text_file("src/app/main.py")
    assert "FastAPI" in content


def test_safe_file_tool_rejects_escape() -> None:
    try:
        read_repository_text_file("../../etc/passwd")
    except ValueError:
        pass
    else:
        raise AssertionError("repository escape should have been rejected")


def test_reference_graph_returns_structured_output(tmp_path) -> None:
    trace_file = tmp_path / "trace.jsonl"
    result = run_review(
        "src/app/main.py",
        task_id="TEST-001",
        llm=FakeLLM(),
        trace_file=str(trace_file),
    )
    assert result.status == "approved"
    assert trace_file.exists()
    trace = json.loads(trace_file.read_text(encoding="utf-8").splitlines()[0])
    assert trace["task_id"] == "TEST-001"
    assert "read_repository_text_file" in trace["tools"]
