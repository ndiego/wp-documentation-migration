// Generates deterministic placeholder JPEGs (original work, no licensing concerns) via headless Chromium canvas.
import { chromium } from '@playwright/test';
import fs from 'node:fs';
const specs = [
  ['mountain-lake.jpg', ['#1e3a5f','#5b8fb9','#e8d8b0'], 'Mountain Lake'],
  ['autumn-forest.jpg', ['#5a2d0c','#c4661f','#f2c14e'], 'Autumn Forest'],
  ['city-at-dusk.jpg', ['#1a1033','#6b2d5c','#f08a5d'], 'City at Dusk'],
];
const b = await chromium.launch(); const p = await b.newPage();
for (const [name, cols, label] of specs) {
  const data = await p.evaluate(([cols,label]) => {
    const c = document.createElement('canvas'); c.width=1600; c.height=1067; const x=c.getContext('2d');
    const g=x.createLinearGradient(0,0,0,c.height); cols.forEach((col,i)=>g.addColorStop(i/(cols.length-1),col)); x.fillStyle=g; x.fillRect(0,0,c.width,c.height);
    x.fillStyle='rgba(0,0,0,.35)'; x.beginPath(); x.moveTo(0,800); x.lineTo(400,450); x.lineTo(700,700); x.lineTo(1100,350); x.lineTo(1600,780); x.lineTo(1600,1067); x.lineTo(0,1067); x.fill();
    x.fillStyle='rgba(255,255,255,.9)'; x.font='bold 72px sans-serif'; x.fillText(label,80,140);
    return c.toDataURL('image/jpeg',0.85);
  }, [cols,label]);
  fs.writeFileSync('assets/'+name, Buffer.from(data.split(',')[1],'base64'));
}
await b.close(); console.log('ok');
