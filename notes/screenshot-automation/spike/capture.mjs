// Docs screenshot spike: node capture.mjs <outDir> [--video]
import { chromium } from '@playwright/test';
import { Editor } from '@wordpress/e2e-test-utils-playwright';
import fs from 'node:fs';
import path from 'node:path';

const BASE = process.env.WP_BASE || 'http://127.0.0.1:9400';
const out = process.argv[2] || 'out/run1';
const wantVideo = process.argv.includes('--video');
fs.mkdirSync(out, { recursive: true });
const timings = []; const notes = [];
const T = async (label, fn) => { const t = performance.now(); const r = await fn(); timings.push({ label, ms: Math.round(performance.now() - t) }); return r; };
const tTotal = performance.now();

const browser = await T('launch chromium', () => chromium.launch());
const context = await browser.newContext({
  baseURL: BASE,
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 2,
  reducedMotion: 'reduce',
  colorScheme: 'light',
  locale: 'en-US',
  timezoneId: 'UTC',
  ...(wantVideo ? { recordVideo: { dir: path.join(out, 'video'), size: { width: 1440, height: 900 } } } : {}),
});
const page = await context.newPage();
page.on('pageerror', e => notes.push('pageerror: ' + e.message));

// --- (a) Auth: Playground's blueprint `login` step makes the server auto-login ANY client on first request
await T('open post-new.php (auth)', async () => {
  await page.goto('/wp-admin/post-new.php');
  if (await page.locator('#loginform').count()) {
    notes.push('auth: auto-login did not apply; posted wp-login.php form');
    await page.fill('#user_login', 'admin'); await page.fill('#user_pass', 'password');
    await Promise.all([page.waitForNavigation(), page.click('#wp-submit')]);
    await page.goto('/wp-admin/post-new.php');
  } else notes.push('auth: logged in via Playground auto-login cookie (no form post needed)');
  const cookies = (await context.cookies()).map(c => c.name);
  notes.push('cookies: ' + cookies.join(', '));
});

const editor = new Editor({ page });
await T('editor ready', async () => {
  await page.waitForFunction(() => window.wp?.data?.select('core/editor')?.getCurrentPostId?.());
  await editor.canvas.locator('body').waitFor();
  await editor.canvas.locator('.wp-block-post-title, [aria-label="Add title"]').first().waitFor();
});

// Diagnostics: modals / notices / theme
const diag = await page.evaluate(() => ({
  isFullscreenClass: document.body.classList.contains('is-fullscreen-mode'),
  wp: document.querySelector('#wp-version')?.textContent,
  modals: [...document.querySelectorAll('.components-modal__frame')].map(m => m.getAttribute('aria-label') || m.className),
  notices: [...document.querySelectorAll('.components-notice, .notice, .components-snackbar')].map(n => n.textContent.trim().slice(0, 120)),
  adminBar: !!document.querySelector('#wpadminbar') && getComputedStyle(document.querySelector('#wpadminbar')).display !== 'none',
  prefsWelcome: window.wp.data.select('core/preferences').get('core/edit-post', 'welcomeGuide'),
  prefsCoreWelcome: window.wp.data.select('core/preferences').get('core', 'welcomeGuide'),
  fullscreen: window.wp.data.select('core/preferences').get('core/edit-post', 'fullscreenMode'),
  theme: document.querySelector('link[id$="-style-css"]')?.id,
  bodyClass: document.body.className,
}));
const canvasFonts = await editor.canvas.locator('body').evaluate(() => getComputedStyle(document.body).fontFamily);
diag.canvasFont = canvasFonts;
diag.stylesheet = await page.evaluate(() => window.wp.data.select('core').getCurrentTheme?.()?.stylesheet);
// Close any modal that slipped through (record it)
if (diag.modals.length) { notes.push('modal present on load: ' + diag.modals.join('|')); await page.keyboard.press('Escape'); }

const settle = async () => {
  await page.mouse.move(1439, 899); // park in status bar corner; (0,0) hovers the admin-bar W menu
  await page.evaluate(() => document.fonts.ready);
  await editor.canvas.locator('body').evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(300); // let popovers position
};
const shot = (name, fn) => T('shot ' + name, fn);
const SO = { animations: 'disabled', caret: 'hide', scale: 'device' };

// --- (c) Insert Image block
await T('insert image block', async () => {
  await editor.insertBlock({ name: 'core/paragraph', attributes: { content: 'A well-planned day hike is the perfect introduction to the trails near you.' } });
  await editor.insertBlock({ name: 'core/image' });
  await editor.canvas.locator('[data-type="core/image"]').waitFor();
});
await settle();
await shot('01-editor-image-placeholder', () => page.screenshot({ path: `${out}/01-editor-image-placeholder.png`, ...SO }));

const toolbar = page.locator('.block-editor-block-contextual-toolbar, .block-editor-block-toolbar').first();
await toolbar.waitFor();
await shot('02-block-toolbar', () => toolbar.screenshot({ path: `${out}/02-block-toolbar.png`, ...SO }));

// Settings sidebar (Block tab)
await T('open settings sidebar', async () => {
  await page.evaluate(() => window.wp.data.dispatch('core/edit-post').openGeneralSidebar('edit-post/block'));
});
const sidebar = page.locator('.interface-complementary-area').first();
await sidebar.waitFor(); await settle();
await shot('03-block-settings-sidebar', () => sidebar.screenshot({ path: `${out}/03-block-settings-sidebar.png`, ...SO }));

// Inserter with "image" search
await T('open inserter + type', async () => {
  await page.getByRole('button', { name: /block inserter/i }).first().click();
  const search = page.getByRole('searchbox', { name: /search/i }).first();
  await search.fill('image');
  await page.locator('.block-editor-block-types-list__item').first().waitFor();
});
await settle();
await shot('04-inserter-search-image', () => page.screenshot({ path: `${out}/04-inserter-search-image.png`, ...SO }));
const inserterPanel = page.locator('.editor-inserter-sidebar, .block-editor-inserter__main-area').first();
await shot('04b-inserter-panel', () => inserterPanel.screenshot({ path: `${out}/04b-inserter-panel.png`, ...SO }));
await page.getByRole('button', { name: /block inserter|close/i }).first().click().catch(() => page.keyboard.press('Escape'));

// --- (d) Annotation: give the image a real media item so the toolbar has "Replace", then outline it
const media = await page.evaluate(async () => (await window.wp.apiFetch({ path: '/wp/v2/media?search=mountain-lake&_fields=id,source_url' }))[0]);
await page.evaluate(({ id, source_url }) => {
  const { select, dispatch } = window.wp.data;
  const img = select('core/block-editor').getBlocks().find(b => b.name === 'core/image');
  dispatch('core/block-editor').updateBlockAttributes(img.clientId, { id, url: source_url, alt: 'Mountain lake at sunrise', sizeSlug: 'large' });
  dispatch('core/block-editor').selectBlock(img.clientId);
}, media);
await editor.canvas.locator('[data-type="core/image"] img').evaluate(i => i.complete || new Promise(r => (i.onload = r)));
await settle();
await shot('05-editor-with-image', () => page.screenshot({ path: `${out}/05-editor-with-image.png`, ...SO }));

const replace = page.locator('.block-editor-block-toolbar').getByRole('button', { name: 'Replace' }).first();
await replace.waitFor();
await page.addStyleTag({ content: `.docs-highlight{outline:2px solid #d63638 !important;outline-offset:3px !important;border-radius:2px;box-shadow:0 0 0 6px rgba(214,54,56,.12) !important;position:relative;z-index:2}` });
await replace.evaluate(el => el.classList.add('docs-highlight'));
await settle();
const tb = await page.locator('.block-editor-block-toolbar').first().boundingBox();
const PAD = 32;
await shot('06-annotated-replace', () => page.screenshot({ path: `${out}/06-annotated-replace.png`, ...SO,
  clip: { x: Math.max(0, tb.x - PAD), y: Math.max(0, tb.y - PAD), width: tb.width + PAD * 2, height: tb.height + PAD * 2 + 120 } }));
await replace.evaluate(el => el.classList.remove('docs-highlight'));

// Mask demo: mask the post title + the image itself (e.g. hide volatile content), magenta default -> neutral
await editor.canvas.locator('.wp-block-post-title, [aria-label="Add title"]').first().click();
await page.keyboard.type('Planning Your First Hiking Trip');
await page.mouse.move(1439, 899);
await shot('07-mask-and-caret-hidden', () => page.screenshot({ path: `${out}/07-mask-and-caret-hidden.png`, ...SO,
  mask: [editor.canvas.locator('[data-type="core/image"] img')], maskColor: '#dcdcde' }));
await shot('07b-caret-visible-for-contrast', () => page.screenshot({ path: `${out}/07b-caret-visible.png`, animations: 'disabled', caret: 'initial' }));

await context.close();
await browser.close();
timings.push({ label: 'TOTAL', ms: Math.round(performance.now() - tTotal) });
const report = { out, diag, notes, timings };
fs.writeFileSync(`${out}/report.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
