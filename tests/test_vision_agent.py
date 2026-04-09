"""Тесты vision_agent.py — адаптеры и фабрика (Sprint 1)."""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from vision_agent import (
    AVAILABLE_PROVIDERS,
    AnthropicAdapter,
    OpenAICompatibleAdapter,
    VisionProvider,
    get_provider,
)


# --- Интерфейс ---

def test_vision_provider_is_abstract():
    with pytest.raises(TypeError):
        VisionProvider()  # type: ignore


# --- AnthropicAdapter ---

def test_anthropic_adapter_missing_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            AnthropicAdapter(api_key="")


def test_anthropic_adapter_analyze(monkeypatch):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="style: minimal")]
    )
    with patch("vision_agent.AnthropicAdapter.__init__", lambda self, **kw: None):
        adapter = AnthropicAdapter.__new__(AnthropicAdapter)
        adapter.client = mock_client
        adapter.model = "claude-haiku-4-5-20251001"

    result = adapter.analyze("base64data", "image/png", "Analyze style")
    assert result == "style: minimal"


# --- OpenAICompatibleAdapter ---

def test_openai_adapter_missing_key():
    env = {k: v for k, v in os.environ.items() if "API_KEY" not in k}
    with patch.dict(os.environ, env, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            OpenAICompatibleAdapter(provider="openai", api_key="")


def test_openai_adapter_analyze(monkeypatch):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="style: bold"))]
    )
    with patch("openai.OpenAI", return_value=mock_client):
        adapter = OpenAICompatibleAdapter(provider="openai", api_key="sk-test")

    result = adapter.analyze("base64data", "image/jpeg", "Analyze style")
    assert result == "style: bold"


# --- get_provider фабрика ---

def test_get_provider_anthropic(monkeypatch):
    monkeypatch.setenv("VISION_PROVIDER", "anthropic")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    with patch("anthropic.Anthropic"):
        provider = get_provider()
    assert isinstance(provider, AnthropicAdapter)


def test_get_provider_openai(monkeypatch):
    monkeypatch.setenv("VISION_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    with patch("openai.OpenAI"):
        provider = get_provider()
    assert isinstance(provider, OpenAICompatibleAdapter)


def test_get_provider_unknown():
    with pytest.raises(ValueError, match="Неизвестный провайдер"):
        get_provider(provider="unknown_llm")


def test_get_provider_error_lists_available():
    with pytest.raises(ValueError) as exc:
        get_provider(provider="mystery")
    for name in AVAILABLE_PROVIDERS:
        assert name in str(exc.value)
