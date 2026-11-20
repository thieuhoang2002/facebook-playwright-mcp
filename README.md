# facebook-playwright-mcp

A Model Context Protocol (MCP) server for personal Facebook automation using Playwright.

## Features

- **check_login_status**: Verify whether your Facebook session is active.
- **read_newsfeed**: Retrieve recent posts from your personal newsfeed.
- **post_personal_status**: Publish new status updates directly to your timeline.
- **search_facebook**: Search for posts, people, groups, or pages.
- **read_page_or_group**: Extract readable content from any specific Facebook link.

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

## Security & Privacy

- All credentials, session data, and cookies remain exclusively on your local machine.
- The `browser_profile/` directory is strictly ignored in `.gitignore` to prevent accidental credential leaks.
