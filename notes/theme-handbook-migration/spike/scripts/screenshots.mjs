// Side-by-side screenshots: production (left) vs local import (right), post content column only.
// Usage: node screenshots.mjs <out-dir> [path ...]      (paths below /themes/, default set below)
// Playwright comes from ~/Developer/wordpress-org/local-tools/playwright (override with PW=...).
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';

const { chromium } = await import(
	process.env.PW ?? `${ homedir() }/Developer/wordpress-org/local-tools/playwright/node_modules/playwright/index.mjs`
);

const OUT = process.argv[ 2 ];
const PATHS = process.argv.slice( 3 ).length ? process.argv.slice( 3 ) : [
	'',
	'getting-started/quick-start-guide',
	'global-settings-and-styles/settings/spacing',
	'patterns/registering-patterns',
	'patterns/patterns-and-block-locking',
	'classic-themes/customize-api/customizer-objects',
	'classic-themes/functionality/media/audio',
	'classic-themes/functionality/custom-logo',
	'classic-themes/basics/including-css-javascript',
	'theme-security/theme-security-issues',
];
const MAX_H = 2600;
mkdirSync( OUT, { recursive: true } );

const browser = await chromium.launch();
const ctx = await browser.newContext( {
	viewport: { width: 1280, height: 900 },
	userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',
} );
const page = await ctx.newPage();

async function shot( url, file ) {
	await page.goto( url, { waitUntil: 'networkidle', timeout: 60000 } );
	// Scroll through so lazy images load (Markdown images have no width/height, nothing reserved).
	await page.evaluate( async () => {
		for ( let y = 0; y < document.body.scrollHeight; y += 600 ) {
			window.scrollTo( 0, y );
			await new Promise( ( r ) => setTimeout( r, 80 ) );
		}
		window.scrollTo( 0, 0 );
	} );
	await page.waitForTimeout( 1000 );
	await page.addStyleTag( { content: '.wp-block-wporg-local-navigation-bar, .global-header { position: static !important; }' } );
	const main = page.locator( 'main' ).first();
	const box = await main.boundingBox();
	await page.screenshot( {
		path: file,
		fullPage: true,
		clip: { x: box.x, y: box.y, width: box.width, height: Math.min( box.height, MAX_H ) },
	} );
	return box.height;
}

for ( const p of PATHS ) {
	const slug = p ? p.replace( /\//g, '__' ) : 'index';
	const prodFile = `${ OUT }/${ slug }.prod.png`;
	const localFile = `${ OUT }/${ slug }.local.png`;
	const hp = await shot( `https://developer.wordpress.org/themes/${ p }${ p ? '/' : '' }`, prodFile );
	const hl = await shot( `http://localhost:8888/themes/${ p }${ p ? '/' : '' }`, localFile );
	// Compose side by side in the browser itself (no image library needed).
	const b64 = ( f ) => `data:image/png;base64,${ readFileSync( f ).toString( 'base64' ) }`;
	const html = `<html><body style="margin:0;display:flex;gap:8px;background:#c00">
		<div style="flex:1;background:#fff"><div style="font:16px sans-serif;padding:6px;background:#eee">production (${ Math.round( hp ) }px)</div><img src="${ b64( prodFile ) }" style="width:100%"></div>
		<div style="flex:1;background:#fff"><div style="font:16px sans-serif;padding:6px;background:#eee">local import (${ Math.round( hl ) }px)</div><img src="${ b64( localFile ) }" style="width:100%"></div>
	</body></html>`;
	const tmp = `${ OUT }/${ slug }.compose.html`;
	writeFileSync( tmp, html );
	await page.setViewportSize( { width: 1600, height: 900 } );
	await page.goto( `file://${ tmp }` );
	await page.screenshot( { path: `${ OUT }/${ slug }.side-by-side.png`, fullPage: true } );
	await page.setViewportSize( { width: 1280, height: 900 } );
	console.log( `${ slug }: prod main ${ Math.round( hp ) }px, local main ${ Math.round( hl ) }px` );
}
await browser.close();
