#!/usr/bin/env node
// JackieG Reel Editor · MCP App (local, stdio). Opens Jackie's editor panel inside the Claude desktop app.
// Zero dependencies: plain Node (Claude Desktop ships Node), so students install nothing extra.
// Phase 1 (test): the panel lists your brands and reels, runs the system check, and shows a reel in Finder.
// The heavy work stays in skills/jackieg-reel-editor/scripts (same scripts the skill uses).
// Protocol: MCP over stdio (newline-delimited JSON-RPC) + the MCP Apps extension (ui:// resource, _meta.ui.resourceUri).
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { homedir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const SKILL = resolve(HERE, '..', 'skills', 'jackieg-reel-editor');
const REELS_ROOT = resolve((process.env.REELS_ROOT || '~/reels-jackieg').replace(/^~(?=$|\/)/, homedir()));
const UI_URI = 'ui://jackieg/editor';
const UI_HTML = readFileSync(join(HERE, 'ui.html'), 'utf8');
const VERSION = JSON.parse(readFileSync(join(HERE, '..', '.claude-plugin', 'plugin.json'), 'utf8')).version;
const APP_CDN = 'https://unpkg.com';

function savedLang() {
  try { return readFileSync(join(homedir(), '.config', 'jackieg-reel-editor', 'lang'), 'utf8').trim() === 'en' ? 'en' : 'es'; }
  catch { return 'es'; }
}

// Same rule as scripts/brands.py: ~/reels-jackieg itself and any folder in ~/reels-jackieg or ~/reels-jackieg/brands with a brand.json.
function brands() {
  const cands = [REELS_ROOT];
  for (const base of [REELS_ROOT, join(REELS_ROOT, 'brands')]) {
    try { for (const d of readdirSync(base, { withFileTypes: true })) if (d.isDirectory()) cands.push(join(base, d.name)); } catch { /* none */ }
  }
  const seen = new Set(), out = [];
  for (const d of cands) {
    const f = join(d, 'brand.json');
    if (!existsSync(f) || seen.has(d)) continue;
    seen.add(d);
    let name = d.split('/').pop();
    try { name = JSON.parse(readFileSync(f, 'utf8')).name || name; } catch { /* keep folder name */ }
    out.push({ name, folder: d, reels: reels(d) });
  }
  return out;
}

function reels(brandDir) {
  const list = [];
  let entries = [];
  try { entries = readdirSync(brandDir, { withFileTypes: true }); } catch { return list; }
  for (const e of entries) {
    if (!e.isDirectory() || !/^\d{4}-\d{2}-\d{2}-/.test(e.name)) continue;
    const dir = join(brandDir, e.name);
    let files = [];
    try { files = readdirSync(dir); } catch { continue; }
    if (!files.some((f) => f.startsWith('raw.'))) continue;
    const status = files.includes('final.mp4') ? (files.includes('post.md') ? 'listo' : 'video') : files.includes('edl.json') ? 'cortado' : 'nuevo';
    list.push({ name: e.name.slice(11), date: e.name.slice(0, 10), folder: dir, status, mtime: statSync(dir).mtimeMs });
  }
  return list.sort((a, b) => b.mtime - a.mtime).slice(0, 30);
}

function run(cmd, args, timeoutMs = 120000) {
  return new Promise((res) => execFile(cmd, args, { timeout: timeoutMs, maxBuffer: 1 << 20, env: process.env }, (err, stdout, stderr) =>
    res({ code: err ? (typeof err.code === 'number' ? err.code : 1) : 0, out: String(stdout || '') + String(stderr || '') })));
}

function inside(p, roots) { const r = resolve(p); return roots.some((root) => r === root || r.startsWith(root + '/')); }

// ---- tools ---------------------------------------------------------------------------------------------------
const TOOLS = [
  {
    name: 'jackieg_editor',
    title: 'Abrir el editor JackieG',
    description: 'Open the JackieG Reel Editor panel: the person\'s brands and recent reels (status of each), with buttons to run the system check and show a reel in Finder. Use when they ask to open their reel editor, see their reels, or "abre mi editor".',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
    _meta: { ui: { resourceUri: UI_URI }, 'ui/resourceUri': UI_URI },
    async call() {
      const b = brands(), lang = savedLang();
      const n = b.reduce((s, x) => s + x.reels.length, 0);
      return {
        content: [{ type: 'text', text: `JackieG Reel Editor ${VERSION}: ${b.length} brand(s), ${n} reel(s) in ${REELS_ROOT}.` }],
        structuredContent: { version: VERSION, lang, reelsRoot: REELS_ROOT, brands: b },
      };
    },
  },
  {
    name: 'jackieg_check',
    title: 'Revisar el editor',
    description: 'Run the JackieG Reel Editor system check (doctor.sh): ✅/⚠️/❌ lines with JG-* codes and the fix for each. Read-only.',
    inputSchema: { type: 'object', properties: { lang: { type: 'string', enum: ['es', 'en'] } }, additionalProperties: false },
    async call({ lang } = {}) {
      const r = await run('bash', [join(SKILL, 'scripts', 'doctor.sh'), lang || savedLang()]);
      const status = r.code === 0 ? 'ready' : r.code === 2 ? 'limits' : 'missing';
      return { content: [{ type: 'text', text: r.out }], structuredContent: { status, text: r.out } };
    },
  },
  {
    name: 'jackieg_show_in_finder',
    title: 'Mostrar en Finder',
    description: 'Reveal a reel folder (inside ~/reels-jackieg) in Finder.',
    inputSchema: { type: 'object', properties: { folder: { type: 'string' } }, required: ['folder'], additionalProperties: false },
    async call({ folder }) {
      if (!folder || !inside(folder, [REELS_ROOT])) return { isError: true, content: [{ type: 'text', text: 'Only folders inside ~/reels-jackieg can be shown.' }] };
      const r = process.platform === 'darwin' ? await run('open', ['-R', resolve(folder)]) : { code: 1, out: 'Finder is only on a Mac.' };
      return { content: [{ type: 'text', text: r.code === 0 ? 'Shown in Finder.' : r.out }], structuredContent: { ok: r.code === 0 } };
    },
  },
];

// ---- MCP over stdio ------------------------------------------------------------------------------------------
const send = (msg) => process.stdout.write(JSON.stringify(msg) + '\n');
const reply = (id, result) => send({ jsonrpc: '2.0', id, result });
const fail = (id, code, message) => send({ jsonrpc: '2.0', id, error: { code, message } });

async function handle(m) {
  const { id, method, params = {} } = m;
  if (id === undefined) return; // notifications (initialized, cancelled…)
  switch (method) {
    case 'initialize':
      return reply(id, {
        protocolVersion: params.protocolVersion || '2025-06-18',
        capabilities: { tools: { listChanged: false }, resources: { listChanged: false } },
        serverInfo: { name: 'jackieg-reel-editor', title: 'JackieG Reel Editor', version: VERSION },
        instructions: 'JackieG Reel Editor (powered by perlili.dev). Use jackieg_editor to open the editor panel. Editing itself follows the jackieg-reel-editor skill.',
      });
    case 'ping': return reply(id, {});
    case 'tools/list':
      return reply(id, { tools: TOOLS.map(({ call, ...t }) => t) });
    case 'tools/call': {
      const t = TOOLS.find((x) => x.name === params.name);
      if (!t) return fail(id, -32602, `Unknown tool: ${params.name}`);
      try { return reply(id, await t.call(params.arguments || {})); }
      catch (e) { return reply(id, { isError: true, content: [{ type: 'text', text: String(e?.message || e) }] }); }
    }
    case 'resources/list':
      return reply(id, { resources: [{ uri: UI_URI, name: 'JackieG editor panel', mimeType: 'text/html;profile=mcp-app' }] });
    case 'resources/read':
      if (params.uri !== UI_URI) return fail(id, -32602, `Unknown resource: ${params.uri}`);
      return reply(id, { contents: [{ uri: UI_URI, mimeType: 'text/html;profile=mcp-app', text: UI_HTML,
        _meta: { ui: { csp: { resourceDomains: [APP_CDN] }, prefersBorder: false } } }] });
    default:
      return fail(id, -32601, `Method not found: ${method}`);
  }
}

let buf = '', pending = 0, ended = false;
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  buf += chunk;
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!line) continue;
    let m; try { m = JSON.parse(line); } catch { fail(null, -32700, 'Parse error'); continue; }
    pending++; handle(m).finally(() => { pending--; if (ended && !pending) process.exit(0); });
  }
});
process.stdin.on('end', () => { ended = true; if (!pending) process.exit(0); });
