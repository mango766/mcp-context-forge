# -*- coding: utf-8 -*-
"""Location: ./mcpgateway/plugins/framework/__init__.py
Copyright 2025
SPDX-License-Identifier: Apache-2.0
Authors: Fred Araujo

Services Package.
Exposes core ContextForge plugin components:
- Context
- Manager
- Payloads
- Models
- ExternalPluginServer
"""

# Standard
from typing import Optional

# First-Party
from mcpgateway.plugins.framework.base import Plugin
from mcpgateway.plugins.framework.errors import PluginError, PluginViolationError
from mcpgateway.plugins.framework.external.mcp.server import ExternalPluginServer
from mcpgateway.plugins.framework.hooks.registry import HookRegistry, get_hook_registry
from mcpgateway.plugins.framework.loader.config import ConfigLoader
from mcpgateway.plugins.framework.loader.plugin import PluginLoader
from mcpgateway.plugins.framework.manager import PluginManager, DBPluginManager
from mcpgateway.plugins.framework.observability import ObservabilityProvider
from mcpgateway.plugins.framework.hooks.http import (
    HttpAuthCheckPermissionPayload,
    HttpAuthCheckPermissionResult,
    HttpAuthCheckPermissionResultPayload,
    HttpAuthResolveUserPayload,
    HttpAuthResolveUserResult,
    HttpHeaderPayload,
    HttpHookType,
    HttpPostRequestPayload,
    HttpPostRequestResult,
    HttpPreRequestPayload,
    HttpPreRequestResult,
)
from mcpgateway.plugins.framework.hooks.agents import AgentHookType, AgentPostInvokePayload, AgentPostInvokeResult, AgentPreInvokePayload, AgentPreInvokeResult
from mcpgateway.plugins.framework.hooks.resources import ResourceHookType, ResourcePostFetchPayload, ResourcePostFetchResult, ResourcePreFetchPayload, ResourcePreFetchResult
from mcpgateway.plugins.framework.hooks.prompts import (
    PromptHookType,
    PromptPosthookPayload,
    PromptPosthookResult,
    PromptPrehookPayload,
    PromptPrehookResult,
)
from mcpgateway.plugins.framework.hooks.tools import ToolHookType, ToolPostInvokePayload, ToolPostInvokeResult, ToolPreInvokeResult, ToolPreInvokePayload
from mcpgateway.plugins.framework.models import (
    GlobalContext,
    MCPServerConfig,
    PluginCondition,
    PluginConfig,
    PluginContext,
    PluginContextTable,
    PluginErrorModel,
    PluginMode,
    PluginPayload,
    PluginResult,
    PluginViolation,
)
from mcpgateway.plugins.framework.utils import get_attr

# Plugin manager singleton — set once by main.py before service imports
_plugin_manager: Optional[DBPluginManager] = None


def set_plugin_manager(manager: Optional[DBPluginManager]) -> None:
    """Set the plugin manager singleton.

    Args:
        manager: DBPluginManager instance to set as the singleton, or None to clear it.

    Examples:
        >>> from mcpgateway.plugins.framework import set_plugin_manager
        >>> set_plugin_manager(None)
    """
    global _plugin_manager  # pylint: disable=global-statement
    _plugin_manager = manager


def get_plugin_manager(observability: Optional[ObservabilityProvider] = None) -> Optional[DBPluginManager]:
    """Get the plugin manager singleton.

    This is the public API for accessing the plugin manager from anywhere in the application.
    The singleton is set by main.py via set_plugin_manager() before service modules are imported.

    Args:
        observability: Unused; retained for backwards compatibility.

    Returns:
        DBPluginManager instance if plugins are enabled and initialized, None otherwise.

    Examples:
        >>> from mcpgateway.plugins.framework import get_plugin_manager
        >>> pm = get_plugin_manager()
        >>> pm is None or isinstance(pm, DBPluginManager)
        True
    """
    return _plugin_manager


__all__ = [
    "AgentHookType",
    "AgentPostInvokePayload",
    "AgentPostInvokeResult",
    "AgentPreInvokePayload",
    "AgentPreInvokeResult",
    "ConfigLoader",
    "ExternalPluginServer",
    "get_attr",
    "get_hook_registry",
    "get_plugin_manager",
    "set_plugin_manager",
    "GlobalContext",
    "HookRegistry",
    "HttpAuthCheckPermissionPayload",
    "HttpAuthCheckPermissionResult",
    "HttpAuthCheckPermissionResultPayload",
    "HttpAuthResolveUserPayload",
    "HttpAuthResolveUserResult",
    "HttpHeaderPayload",
    "HttpHookType",
    "HttpPostRequestPayload",
    "HttpPostRequestResult",
    "HttpPreRequestPayload",
    "HttpPreRequestResult",
    "MCPServerConfig",
    "ObservabilityProvider",
    "Plugin",
    "PluginCondition",
    "PluginConfig",
    "PluginContext",
    "PluginContextTable",
    "PluginError",
    "PluginErrorModel",
    "PluginLoader",
    "PluginManager",
    "DBPluginManager",
    "PluginMode",
    "PluginPayload",
    "PluginResult",
    "PluginViolation",
    "PluginViolationError",
    "PromptHookType",
    "PromptPosthookPayload",
    "PromptPosthookResult",
    "PromptPrehookPayload",
    "PromptPrehookResult",
    "ResourceHookType",
    "ResourcePostFetchPayload",
    "ResourcePostFetchResult",
    "ResourcePreFetchPayload",
    "ResourcePreFetchResult",
    "ToolHookType",
    "ToolPostInvokePayload",
    "ToolPostInvokeResult",
    "ToolPreInvokeResult",
    "ToolPreInvokePayload",
]
