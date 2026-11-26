# JackieG Reel Editor · app inside Claude (MCP App) — test phase

Opens Jackie's editor panel inside the Claude desktop app: your brands and reels, the system check, "Show in Finder".
Plain Node, no dependencies (`server.mjs` + `ui.html`). The editing itself still runs through the `jackieg-reel-editor`
skill and its scripts; later phases move the review page here too.

## Try it on your Mac (developer test)

1. Have this repo on your Mac, e.g. `~/Documents/jackieg-reel-editor`, and Node.js (`node -v`, 18 or newer).
2. In the Claude desktop app: **Settings → Developer → Edit Config**. That opens `claude_desktop_config.json`. Add
   (keep anything already there, and use your own path):
   ```json
   {
     "mcpServers": {
       "jackieg-reel-editor": {
         "command": "node",
         "args": ["/Users/YOUR-USER/Documents/jackieg-reel-editor/mcp-app/server.mjs"]
       }
     }
   }
   ```
3. Quit Claude completely (Cmd+Q) and open it again.
4. In a new chat, say **"abre mi editor JackieG"**. Approve the tool when Claude asks. The pink panel should appear.
5. Check: does it open in the chat, beside the chat, or full screen? Does "Revisar mi editor" work? Does "Ver en Finder" open the folder?

If the tool runs but no panel shows, see https://claude.com/docs/connectors/building/mcp-apps/troubleshooting
(the panel loads the MCP Apps client from unpkg.com, so it needs internet).

## Next phases
1. One-click install: package as `.mcpb` (Claude Desktop extension) with Jackie's icon, no config file editing.
2. Move the review page here: tap words to cut, captions, music, cover — edited in the panel, by the person or by Claude.
3. Tools for each step (transcribe, cut, render, music, post copy) so the panel can show progress.
