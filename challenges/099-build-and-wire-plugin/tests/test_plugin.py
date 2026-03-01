import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from plugin_base import Plugin
from plugins.uppercase import UppercasePlugin
from registry import PluginRegistry
from config import load_config, setup_registry


def test_plugin_base_is_abstract():
    """Cannot instantiate Plugin directly."""
    with pytest.raises(TypeError):
        Plugin()


def test_uppercase_plugin_name():
    """UppercasePlugin().name() returns 'uppercase'."""
    plugin = UppercasePlugin()
    assert plugin.name() == "uppercase"


def test_uppercase_transform():
    """UppercasePlugin().transform('hello') returns 'HELLO'."""
    plugin = UppercasePlugin()
    assert plugin.transform("hello") == "HELLO"


def test_registry_register_and_get():
    """Register UppercasePlugin, then get it by name."""
    registry = PluginRegistry()
    registry.register(UppercasePlugin)
    plugin = registry.get("uppercase")
    assert isinstance(plugin, UppercasePlugin)
    assert plugin.transform("test") == "TEST"


def test_registry_list_plugins():
    """list_plugins returns ['uppercase'] after registration."""
    registry = PluginRegistry()
    registry.register(UppercasePlugin)
    assert registry.list_plugins() == ["uppercase"]


def test_registry_unknown_plugin():
    """get('nonexistent') raises KeyError."""
    registry = PluginRegistry()
    with pytest.raises(KeyError):
        registry.get("nonexistent")


def test_pipeline_single():
    """Pipeline with ['uppercase'] transforms text."""
    registry = PluginRegistry()
    registry.register(UppercasePlugin)
    pipeline = registry.create_pipeline(["uppercase"])
    assert pipeline("hello world") == "HELLO WORLD"


def test_pipeline_multiple():
    """Pipeline applies multiple plugins in order."""

    class ReversePlugin(Plugin):
        def name(self):
            return "reverse"

        def transform(self, text):
            return text[::-1]

    registry = PluginRegistry()
    registry.register(UppercasePlugin)
    registry.register(ReversePlugin)
    pipeline = registry.create_pipeline(["uppercase", "reverse"])
    assert pipeline("hello") == "OLLEH"


def test_load_config():
    """load_config returns proper structure."""
    config_dict = {
        "plugins": [
            {"class": "plugins.uppercase.UppercasePlugin", "settings": {"enabled": True}}
        ]
    }
    config = load_config(config_dict)
    assert "plugins" in config
    assert len(config["plugins"]) == 1
    assert config["plugins"][0]["class"] == "plugins.uppercase.UppercasePlugin"


def test_setup_registry_from_config():
    """Full flow: config -> registry -> transform works."""
    config_dict = {
        "plugins": [
            {"class": "plugins.uppercase.UppercasePlugin", "settings": {"enabled": True}}
        ]
    }
    config = load_config(config_dict)
    registry = setup_registry(config)
    plugin = registry.get("uppercase")
    assert plugin.transform("integration test") == "INTEGRATION TEST"
