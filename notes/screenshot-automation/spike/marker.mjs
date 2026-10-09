// node marker.mjs create|check  -> creates/looks for a "STATE MARKER" post to test persistence across restarts
import { chromium } from '@playwright/test';
const b = await chromium.launch(); const p = await (await b.newContext({ baseURL: 'http://127.0.0.1:9400' })).newPage();
await p.goto('/wp-admin/post-new.php'); await p.waitForFunction(() => window.wp?.apiFetch);
const r = await p.evaluate(async (mode) => mode === 'create'
  ? (await wp.apiFetch({ path: '/wp/v2/posts', method: 'POST', data: { title: 'STATE MARKER', status: 'publish' } })).id
  : (await wp.apiFetch({ path: '/wp/v2/posts?search=STATE%20MARKER&_fields=id' })).length, process.argv[2]);
console.log(process.argv[2], r); await b.close();
