from pathlib import Path

import pytest

from nanobot.agent.memory import MemoryStore, create_memory_backend
from nanobot.config.schema import AgentMemoryConfig


def test_create_memory_backend_defaults_to_builtin(tmp_path: Path) -> None:
    backend = create_memory_backend(tmp_path)

    assert isinstance(backend, MemoryStore)


def test_create_memory_backend_accepts_builtin_aliases(tmp_path: Path) -> None:
    for adapter in ("builtin", "memorystore", "memory_store"):
        backend = create_memory_backend(tmp_path, adapter=adapter)
        assert isinstance(backend, MemoryStore)


def test_create_memory_backend_accepts_adapter_from_config(tmp_path: Path) -> None:
    config = AgentMemoryConfig(adapter="memory_store")

    backend = create_memory_backend(tmp_path, config=config)

    assert isinstance(backend, MemoryStore)


def test_create_memory_backend_raises_for_unknown_adapter(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unknown memory adapter"):
        create_memory_backend(tmp_path, adapter="custom")
