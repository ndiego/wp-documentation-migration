import { chromium } from '@playwright/test';
const b = await chromium.launch(); const c = await b.newContext({ baseURL: 'http://127.0.0.1:9400' }); const p = await c.newPage();
await p.goto('/wp-admin/post-new.php');
await p.waitForFunction(() => window.wp?.data?.select('core/editor')?.getCurrentPostId?.());
console.log(await p.evaluate(async () => ({
  all: window.wp.data.select('core/preferences').get('core/edit-post','fullscreenMode'),
  meta: await window.wp.apiFetch({ path: '/wp/v2/users/me?context=edit&_fields=meta' }),
  ver: document.body.className.match(/branch-[\d-]+/)?.[0],
  theme: window.wp.data.select('core').getCurrentTheme()?.stylesheet,
})));
await b.close();
