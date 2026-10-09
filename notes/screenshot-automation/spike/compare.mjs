// node compare.mjs dirA dirB  -> byte + pixel comparison of same-named PNGs
import fs from 'node:fs'; import crypto from 'node:crypto';
import { PNG } from 'pngjs'; import pixelmatch from 'pixelmatch';
const [a, b] = process.argv.slice(2); fs.mkdirSync(`${b}/diff`, { recursive: true });
const h = f => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex').slice(0, 12);
const rows = [];
for (const f of fs.readdirSync(a).filter(f => f.endsWith('.png'))) {
  const A = PNG.sync.read(fs.readFileSync(`${a}/${f}`)), B = PNG.sync.read(fs.readFileSync(`${b}/${f}`));
  const sameSize = A.width === B.width && A.height === B.height;
  let diff = null;
  if (sameSize) { const D = new PNG({ width: A.width, height: A.height }); diff = pixelmatch(A.data, B.data, D.data, A.width, A.height, { threshold: 0 }); if (diff) fs.writeFileSync(`${b}/diff/${f}`, PNG.sync.write(D)); }
  rows.push({ file: f, size: `${A.width}x${A.height}`, byteIdentical: h(`${a}/${f}`) === h(`${b}/${f}`), sameSize, diffPixels: diff });
}
console.table(rows); fs.writeFileSync(`${b}/compare.json`, JSON.stringify(rows, null, 2));
