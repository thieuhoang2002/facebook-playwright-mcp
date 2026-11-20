# facebook-playwright-mcp

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io/)
[![Playwright](https://img.shields.io/badge/browser-Playwright-orange.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server for personal Facebook automation using Playwright.

## Features

- **check_login_status**: Verify whether your Facebook session is active.
- **read_newsfeed**: Retrieve recent posts from your personal newsfeed.
- **post_personal_status**: Publish new status updates directly to your timeline.
- **search_facebook**: Search for posts, people, groups, or pages.
- **read_page_or_group**: Extract readable content from any specific Facebook link.

## Architecture

```
AI Client (Antigravity / Claude)
              │
              ▼  (JSON-RPC / stdio)
   Facebook MCP Server (FastMCP)
              │
              ▼  (Local Playwright Session)
   Chromium with Persistent Profile
              │
              ▼  (User Actions)
         Facebook.com
```

## Installation

```bash
git clone https://github.com/thieuhoang2002/facebook-playwright-mcp.git
cd facebook-playwright-mcp
pip install -e .
playwright install chromium
```

## Quick Start (One-Time Authentication)

Run the interactive login command:

```bash
facebook-mcp-login
```

1. A visible Chrome window will open to `facebook.com`.
2. Log into your account (complete 2FA if enabled).
3. Once your feed is visible, switch back to your terminal and press **ENTER**.
4. Your browser profile will be saved locally to `~/.facebook_mcp/browser_profile/`.

## MCP Client Configuration

### Claude Desktop / Antigravity (`mcp_config.json`)

```json
{
  "mcpServers": {
    "facebook": {
      "command": "facebook-mcp"
    }
  }
}
```

### Cursor (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "facebook": {
      "command": "facebook-mcp"
    }
  }
}
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup and contribution workflow.

## Security & Privacy

See [SECURITY.md](SECURITY.md) for security notes and credential protection details.
