import json
from types import SimpleNamespace

from typer.testing import CliRunner

from nanobot.cli.commands import app
from nanobot.config.loader import load_config, save_config
from nanobot.config.schema import Config


def test_load_config_keeps_max_tokens_and_ignores_legacy_memory_window(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "agents": {
                    "defaults": {
                        "maxTokens": 1234,
                        "memoryWindow": 42,
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.agents.defaults.max_tokens == 1234
    assert config.agents.defaults.context_window_tokens == 65_536
    assert not hasattr(config.agents.defaults, "memory_window")


def test_save_config_writes_context_window_tokens_but_not_memory_window(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "agents": {
                    "defaults": {
                        "maxTokens": 2222,
                        "memoryWindow": 30,
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)
    save_config(config, config_path)
    saved = json.loads(config_path.read_text(encoding="utf-8"))
    defaults = saved["agents"]["defaults"]

    assert defaults["maxTokens"] == 2222
    assert defaults["contextWindowTokens"] == 65_536
    assert "memoryWindow" not in defaults


def test_onboard_does_not_crash_with_legacy_memory_window(tmp_path, monkeypatch) -> None:
    config_path = tmp_path / "config.json"
    workspace = tmp_path / "workspace"
    config_path.write_text(
        json.dumps(
            {
                "agents": {
                    "defaults": {
                        "maxTokens": 3333,
                        "memoryWindow": 50,
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("nanobot.config.loader.get_config_path", lambda: config_path)
    monkeypatch.setattr(
        "nanobot.cli.commands.get_workspace_path", lambda _workspace=None: workspace
    )

    runner = CliRunner()
    result = runner.invoke(app, ["onboard"], input="n\n")

    assert result.exit_code == 0


def test_onboard_refresh_backfills_missing_channel_fields(tmp_path, monkeypatch) -> None:
    config_path = tmp_path / "config.json"

    workspace = tmp_path / "workspace"
    config_path.write_text(
        json.dumps(
            {
                "channels": {
                    "qq": {
                        "enabled": False,
                        "appId": "",
                        "secret": "",
                        "allowFrom": [],
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("nanobot.config.loader.get_config_path", lambda: config_path)
    monkeypatch.setattr(
        "nanobot.cli.commands.get_workspace_path", lambda _workspace=None: workspace
    )
    monkeypatch.setattr(
        "nanobot.channels.registry.discover_all",
        lambda: {
            "qq": SimpleNamespace(
                default_config=lambda: {
                    "enabled": False,
                    "appId": "",
                    "secret": "",
                    "allowFrom": [],
                    "msgFormat": "plain",
                }
            )
        },
    )

    runner = CliRunner()

    result = runner.invoke(app, ["onboard"], input="n\n")

    assert result.exit_code == 0
    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert saved["channels"]["qq"]["msgFormat"] == "plain"


def test_save_config_persists_memory_settings_in_camel_case(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config = Config()
    config.agents.defaults.memory.enabled = True
    config.agents.defaults.memory.max_core_chars = 123
    config.agents.defaults.memory.max_mem0_results = 7
    config.agents.defaults.memory.max_mem0_chars = 456
    config.agents.defaults.memory.max_mem0_index_chars = 89
    config.agents.defaults.memory.mem0_config = {"vectorStore": {"provider": "memory"}}

    save_config(config, config_path)

    saved = json.loads(config_path.read_text(encoding="utf-8"))
    memory = saved["agents"]["defaults"]["memory"]
    assert memory == {
        "enabled": True,
        "maxCoreChars": 123,
        "maxMem0Results": 7,
        "maxMem0Chars": 456,
        "maxMem0IndexChars": 89,
        "mem0Config": {"vectorStore": {"provider": "memory"}},
    }


def test_load_config_reads_memory_settings_from_camel_case(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "agents": {
                    "defaults": {
                        "memory": {
                            "enabled": True,
                            "maxCoreChars": 321,
                            "maxMem0Results": 6,
                            "maxMem0Chars": 654,
                            "maxMem0IndexChars": 98,
                            "mem0Config": {"llm": {"provider": "openai"}},
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)

    memory = config.agents.defaults.memory
    assert memory.enabled is True
    assert memory.max_core_chars == 321
    assert memory.max_mem0_results == 6
    assert memory.max_mem0_chars == 654
    assert memory.max_mem0_index_chars == 98
    assert memory.mem0_config == {"llm": {"provider": "openai"}}


def test_save_config_omits_default_memory_adapter(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config = Config()

    save_config(config, config_path)

    saved = json.loads(config_path.read_text(encoding="utf-8"))
    memory = saved["agents"]["defaults"]["memory"]
    assert "adapter" not in memory
    assert "memoryAdapter" not in memory


def test_save_config_persists_non_default_memory_adapter(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config = Config()
    config.agents.defaults.memory.adapter = "memory_store"

    save_config(config, config_path)

    saved = json.loads(config_path.read_text(encoding="utf-8"))
    memory = saved["agents"]["defaults"]["memory"]
    assert memory["adapter"] == "memory_store"


def test_load_config_reads_optional_memory_adapter(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "agents": {
                    "defaults": {
                        "memory": {
                            "adapter": "memory_store",
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.agents.defaults.memory.adapter == "memory_store"
