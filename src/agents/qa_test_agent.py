from __future__ import annotations

import argparse
import json
import multiprocessing
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field, ValidationError

from src.app.settings import get_settings
from src.llm.factory import get_chat_model
from src.observability.tracing import (
    append_trace,
    estimate_cost_credits,
    usage_from_message,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRACE_FILE = "evidence/session-01/qa-test-agent-trace.jsonl"


class QATestRequest(BaseModel):
    task_id: str = Field(min_length=3)
    pytest_target: str = Field(default="tests/starter/test_api.py", min_length=1)
    timeout_seconds: int = Field(default=60, ge=1, le=300)


class QAFinding(BaseModel):
    severity: Literal["low", "medium", "high"]
    description: str


class QATestResult(BaseModel):
    status: Literal["passed", "failed", "needs_review", "error"]
    summary: str
    pytest_exit_code: int | None = None
    findings: list[QAFinding] = Field(default_factory=list)
    human_approval_required: bool = True


class QAState(TypedDict, total=False):
    request: QATestRequest
    pytest_output: str
    pytest_exit_code: int | None
    result: dict[str, Any]
    error: str


def _message_text(message: Any) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts)
    return str(content)


def _safe_pytest_target(relative_target: str) -> Path:
    requested = (REPO_ROOT / relative_target).resolve()
    tests_root = (REPO_ROOT / "tests").resolve()
    try:
        requested.relative_to(tests_root)
    except ValueError as exc:
        raise ValueError("pytest target must stay below tests/") from exc
    if not requested.exists():
        raise FileNotFoundError(relative_target)
    return requested


def run_pytest_tool(relative_target: str, timeout_seconds: int) -> tuple[int, str]:
    target = _safe_pytest_target(relative_target)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", str(target), "-q"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    output = "\n".join(
        part.strip()
        for part in (completed.stdout, completed.stderr)
        if part and part.strip()
    )
    return completed.returncode, output[-6000:]


def _parse_result(text: str, pytest_exit_code: int | None) -> QATestResult:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].lstrip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        cleaned = cleaned[start : end + 1]
    try:
        return QATestResult.model_validate(json.loads(cleaned))
    except (json.JSONDecodeError, ValidationError):
        if pytest_exit_code == 0:
            return QATestResult(
                status="passed",
                summary="pytest completed successfully; LLM output was not valid JSON.",
                pytest_exit_code=pytest_exit_code,
                findings=[
                    QAFinding(
                        severity="low",
                        description="Human review should check the unparseable LLM summary.",
                    )
                ],
            )
        return QATestResult(
            status="needs_review",
            summary=text[:1000] or "pytest result requires human review.",
            pytest_exit_code=pytest_exit_code,
        )


def _invoke_configured_llm_worker(
    system_text: str,
    human_text: str,
    queue: multiprocessing.Queue,
) -> None:
    try:
        response = get_chat_model().invoke(
            [SystemMessage(content=system_text), HumanMessage(content=human_text)]
        )
        queue.put(
            {
                "text": _message_text(response),
                "usage": usage_from_message(response),
            }
        )
    except Exception as exc:
        queue.put({"error": f"{type(exc).__name__}: {exc}"})


def _invoke_configured_llm_bounded(
    system_text: str,
    human_text: str,
    timeout_seconds: int,
) -> tuple[str | None, tuple[int | None, int | None], str | None]:
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    process = ctx.Process(
        target=_invoke_configured_llm_worker,
        args=(system_text, human_text, queue),
    )
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join(5)
        return None, (None, None), "LLM call timed out"
    if queue.empty():
        return None, (None, None), "LLM call produced no response"
    payload = queue.get()
    if payload.get("error"):
        return None, (None, None), payload["error"]
    return payload["text"], tuple(payload["usage"]), None


def build_graph(llm: Any | None = None):

    def run_tests(state: QAState) -> QAState:
        request = state["request"]
        try:
            exit_code, output = run_pytest_tool(
                request.pytest_target,
                request.timeout_seconds,
            )
            return {"pytest_exit_code": exit_code, "pytest_output": output}
        except subprocess.TimeoutExpired:
            return {"error": "pytest timed out before producing a result"}
        except Exception as exc:
            return {"error": f"{type(exc).__name__}: {exc}"}

    def route_after_tests(state: QAState):
        return END if state.get("error") else "summarize"

    def summarize(state: QAState) -> QAState:
        request = state["request"]
        system_text = (
            "You are the QA & Test Engineer agent for a student software "
            "company. Return ONLY valid JSON with keys status, summary, "
            "pytest_exit_code, findings, human_approval_required. status "
            "must be passed, failed, needs_review, or error. findings is "
            "a list of objects with severity low|medium|high and description."
        )
        human_text = (
            "/no_think\n"
            f"Task: {request.task_id}\n"
            f"pytest target: {request.pytest_target}\n"
            f"pytest exit code: {state['pytest_exit_code']}\n\n"
            f"pytest output:\n{state['pytest_output']}"
        )
        if llm is None:
            text, usage, llm_error = _invoke_configured_llm_bounded(
                system_text,
                human_text,
                min(request.timeout_seconds, 45),
            )
            if llm_error:
                result = QATestResult(
                    status="needs_review",
                    summary=(
                        "pytest finished, but the configured LLM could not "
                        f"summarize the run: {llm_error}"
                    ),
                    pytest_exit_code=state["pytest_exit_code"],
                    findings=[
                        QAFinding(
                            severity="medium",
                            description="Human QA review required because LLM summarization failed.",
                        )
                    ],
                )
                result_dict = result.model_dump()
                result_dict["_usage"] = usage
                return {"result": result_dict}
            result = _parse_result(text or "", state["pytest_exit_code"])
            result_dict = result.model_dump()
            result_dict["_usage"] = usage
            return {"result": result_dict}

        response = llm.invoke(
            [SystemMessage(content=system_text), HumanMessage(content=human_text)]
        )
        result = _parse_result(_message_text(response), state["pytest_exit_code"])
        result_dict = result.model_dump()
        result_dict["_usage"] = usage_from_message(response)
        return {"result": result_dict}

    builder = StateGraph(QAState)
    builder.add_node("run_tests", run_tests)
    builder.add_node("summarize", summarize)
    builder.add_edge(START, "run_tests")
    builder.add_conditional_edges("run_tests", route_after_tests, ["summarize", END])
    builder.add_edge("summarize", END)
    return builder.compile()


def run_qa_agent(
    request: QATestRequest,
    *,
    llm: Any | None = None,
    trace_file: str | None = DEFAULT_TRACE_FILE,
) -> QATestResult:
    run_id = str(uuid.uuid4())
    settings = get_settings()
    started = time.perf_counter()
    graph = build_graph(llm)
    state = graph.invoke({"request": request})
    duration = time.perf_counter() - started

    if state.get("error"):
        result = QATestResult(
            status="error",
            summary=state["error"],
            pytest_exit_code=state.get("pytest_exit_code"),
        )
        append_trace(
            {
                "run_id": run_id,
                "task_id": request.task_id,
                "agent": "qa-test-agent",
                "model": settings.llm_model,
                "status": result.status,
                "tools": ["run_pytest_tool"],
                "duration_seconds": round(duration, 4),
                "error": state["error"],
            },
            trace_file,
        )
        return result

    raw = dict(state["result"])
    input_tokens, output_tokens = raw.pop("_usage", (None, None))
    result = QATestResult.model_validate(raw)
    append_trace(
        {
            "run_id": run_id,
            "task_id": request.task_id,
            "agent": "qa-test-agent",
            "model": settings.llm_model,
            "status": result.status,
            "tools": ["run_pytest_tool"],
            "duration_seconds": round(duration, 4),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_credits": estimate_cost_credits(
                duration_seconds=duration,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            ),
        },
        trace_file,
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", default="SESSION-01-QA")
    parser.add_argument("--pytest-target", default="tests/starter/test_api.py")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()

    result = run_qa_agent(
        QATestRequest(
            task_id=args.task_id,
            pytest_target=args.pytest_target,
            timeout_seconds=args.timeout_seconds,
        )
    )
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
