"""Validate the Editing & design decisions (dec.py) and render the area proposal.

Writes data/content-proposal/editing-and-design.md (head.md + per-section tables + tail.md) and .json.
Run from anywhere: python3 -I data/content-proposal/generators/editing-and-design/gen.py
"""
import json, re, runpy, pathlib
from collections import Counter
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
facts = {r['slug']: r for r in json.load(open(ROOT / 'data' / 'article-facts.json'))}
scope = {s for s, r in facts.items() if r['proposed_path'].startswith('editing-and-design/')}

# tree order + subsection from structure-review.md
lines = (ROOT / 'data' / 'structure-review.md').read_text().split('\n')
start = next(i for i, l in enumerate(lines) if l.startswith('- **Editing & design**'))
end = next(i for i, l in enumerate(lines) if l.startswith('- **Classic WordPress**'))
order = []; stack = {}
def secname(st):
    sec = ' > '.join(st[k] for k in sorted(st))
    return 'Themes > Default themes' if sec.startswith('Themes > Default themes') else sec
for l in lines[start + 1:end]:
    ind = (len(l) - len(l.lstrip())) // 2
    m = re.match(r'\s*- \*\*(.+?)\*\*(.*)', l)
    if m:
        stack = {k: v for k, v in stack.items() if k < ind}; stack[ind] = m.group(1)
        idx = re.search(r'index: `([^`]+)`', m.group(2))
        if idx: order.append((idx.group(1), secname(stack)))
        continue
    m = re.match(r'\s*- .*\(`([^`]+)`\)\s*$', l)
    if m: order.append((m.group(1), secname({k: v for k, v in stack.items() if k < ind})))
assert {s for s, _ in order} == scope, (scope ^ {s for s, _ in order})

dec = runpy.run_path(str(HERE / 'dec.py'))
D, NEW = dec['D'], dec['NEW']
missing = scope - set(D); extra = set(D) - scope
assert not missing and not extra, (missing, extra)

def label(a, t):
    if a in ('KEEP', 'REWRITE', 'NEW'): return a
    if a == 'DELETE': return f'DELETE (redirect → {t})'
    return f'{a} → {t}'
out = []; tables = {}; secorder = []
for s, sec in order:
    a, t, res, why = D[s]
    assert len(why.split()) <= 20, (s, len(why.split()))
    if sec not in tables: tables[sec] = []; secorder.append(sec)
    tables[sec].append(f"| `{s}` | {facts[s]['title'].replace('|', '/')} | {label(a, t)} | {res} | {why} |")
    out.append(dict(slug=s, title=facts[s]['title'], section=sec, action=a,
                    target=t if a in ('MERGE', 'SPLIT', 'DELETE', 'MOVE') else None, why=why))
for n in NEW:
    assert len(n['why'].split()) <= 20
    tables[n['section']].append(f"| `{n['slug']}` | {n['title']} | NEW | {n['result']} | {n['why']} |")
    out.append(dict(slug=n['slug'], title=n['title'], section=n['section'], action='NEW', why=n['why']))
# every MERGE/DELETE target must be a page that survives
surv = {o['title'].lower() for o in out if o['action'] in ('KEEP', 'REWRITE', 'NEW')}
for o in out:
    if o['action'] in ('MERGE', 'DELETE') and o['target'] not in (None,) and o['target'].lower() not in surv:
        # targets are short names ("Embeds", "Set your site title, logo and icon"); accept a match on a kept page's title or result
        ok = any(o['target'].lower() in (D.get(x['slug'], [None, None, ''])[2] or '').lower() or o['target'].lower() in x['title'].lower() for x in out if x['action'] in ('KEEP', 'REWRITE', 'NEW'))
        assert ok, ('target not a surviving page', o['slug'], o['target'])

def pages(rows):
    c = Counter(r['action'] for r in rows)
    split = sum(len(D[r['slug']][1].split(';')) for r in rows if r['action'] == 'SPLIT')
    return c['KEEP'] + c['REWRITE'] + c['NEW'] + split
existing = [o for o in out if o['action'] != 'NEW']
AREAS = [('Block editor (top level)', lambda s: s == 'Block editor'),
         ('Working with blocks (incl. Block settings)', lambda s: s.startswith('Block editor > Working with blocks')),
         ('Patterns', lambda s: s.startswith('Block editor > Patterns')),
         ('Blocks reference', lambda s: s.startswith('Block editor > Blocks list')),
         ('Site Editor', lambda s: s.startswith('Site Editor')),
         ('Themes', lambda s: s.startswith('Themes'))]
for name, f in AREAS:
    rs = [o for o in out if f(o['section'])]
    print(f'{name}: {len([r for r in rs if r["action"] != "NEW"])} -> {pages(rs)}')
for sec in secorder:
    if sec.startswith('Block editor > Blocks list'):
        rs = [o for o in out if o['section'] == sec]
        print(f'  {sec}: {len([r for r in rs if r["action"] != "NEW"])} -> {pages(rs)}')
now, after = len(existing), pages(out)
c = Counter(o['action'] for o in out)
print(dict(c), f'pages {now} -> {after}')

head = (HERE / 'head.md').read_text(); tail = (HERE / 'tail.md').read_text()
m = re.search(r'\*\*(\d+) pages now → (\d+) pages proposed\*\*', head)
assert m and (int(m.group(1)), int(m.group(2))) == (now, after), ('head.md Summary out of date', m and m.groups(), now, after)
for a, n in c.items():
    assert re.search(rf'^\| {a} \| {n} \|', head, re.M), ('head.md count out of date', a, n)

(ROOT / 'data' / 'content-proposal' / 'editing-and-design.json').write_text(json.dumps(out, indent=2, ensure_ascii=False))
md = []
for sec in secorder:
    md.append(f'### {sec}\n\n| Slug | Title | Action | Result / target | Why (≤ 20 words) |\n|---|---|---|---|---|')
    md += tables[sec]; md.append('')
(ROOT / 'data' / 'content-proposal' / 'editing-and-design.md').write_text(head + '\n'.join(md) + tail)
print('wrote data/content-proposal/editing-and-design.{md,json}')
