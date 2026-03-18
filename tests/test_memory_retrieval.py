from pathlib import Path

from nanobot.agent.context import ContextBuilder
from nanobot.agent.memory import MemoryStore
from nanobot.config.schema import AgentMemoryConfig


class _FakeMem0:
    def __init__(self, results):
        self.results = results
        self.search_calls = 0
        self.last_search_kwargs: dict | None = None

    def add(self, *_args, **_kwargs) -> None:
        return None

    def search(self, query: str, user_id: str, limit: int):
        self.search_calls += 1
        self.last_search_kwargs = {"query": query, "user_id": user_id, "limit": limit}
        return self.results


def _make_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True)
    return workspace


def test_core_memory_injection_is_bounded(tmp_path: Path) -> None:
    workspace = _make_workspace(tmp_path)
    store = MemoryStore(workspace, config=AgentMemoryConfig(max_core_chars=24))
    store.write_long_term("A" * 80)

    builder = ContextBuilder(workspace, memory_store=store)
    prompt = builder.build_system_prompt(memory_query="hello")

    assert "A" * 80 not in prompt
    assert "## Long-term Memory" in prompt
    assert "[... truncated ...]" in prompt


def test_mem0_relevant_memory_is_bounded_by_count_and_chars(tmp_path: Path) -> None:
    workspace = _make_workspace(tmp_path)
    config = AgentMemoryConfig(enabled=True, max_mem0_results=2, max_mem0_chars=32)
    store = MemoryStore(workspace, config=config)
    fake_mem0 = _FakeMem0(
        results={
            "results": [
                {"memory": "first relevant memory line"},
                {"memory": "second relevant memory line"},
                {"memory": "third should be dropped by max_mem0_results"},
            ]
        }
    )
    store._mem0_client = fake_mem0
    store._mem0_init_attempted = True

    context = store.get_memory_context(query="travel plans", include_relevant=True)

    assert "## Relevant Memory" in context
    assert "third should be dropped" not in context
    assert context.count("- ") <= 2
    assert fake_mem0.last_search_kwargs == {
        "query": "travel plans",
        "user_id": store._mem0_user_id,
        "limit": 2,
    }


def test_token_probe_does_not_query_mem0(tmp_path: Path) -> None:
    workspace = _make_workspace(tmp_path)
    store = MemoryStore(workspace, config=AgentMemoryConfig(enabled=True))
    fake_mem0 = _FakeMem0(results=[{"memory": "should not be fetched"}])
    store._mem0_client = fake_mem0
    store._mem0_init_attempted = True

    builder = ContextBuilder(workspace, memory_store=store)
    probe_messages = builder.build_messages(history=[], current_message="[token-probe]")

    assert fake_mem0.search_calls == 0
    assert "## Relevant Memory" not in probe_messages[0]["content"]
