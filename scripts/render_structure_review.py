"""Render data/structure-review.md from data/structure.yaml.

Usage: .venv/bin/python -I scripts/render_structure_review.py <project-root>
Counts are computed from the YAML; the `classic` flag is shown on the section that sets it."""
import html, json, sys, yaml
root = sys.argv[1]
data = yaml.safe_load(open(root + '/data/structure.yaml'))
T = {x['slug']: html.unescape(x['title']['rendered']) for x in json.load(open(root + '/raw/articles.json'))}
def count(s): return len(s.get('articles') or []) + (1 if 'index' in s else 0) + sum(count(c) for c in s.get('children') or [])
out = []; stats = {'sections': 0, 'index': 0, 'depth': 0, 'classic_sections': 0, 'classic_articles': 0}
placed = []
def walk(secs, d, path, classic):
    for s in secs:
        p = path + '/' + s['slug']; lg = classic or s.get('classic') is True
        stats['sections'] += 1; stats['depth'] = max(stats['depth'], d + 1)
        if 'index' in s: stats['index'] += 1; placed.append(s['index'])
        if lg: stats['classic_sections'] += 1; stats['classic_articles'] += len(s.get('articles') or []) + (1 if 'index' in s else 0)
        title = T[s['index']] if 'index' in s else s['title']
        note = f" — index: `{s['index']}`" if 'index' in s else ''
        flag = ' — `classic: true`' if s.get('classic') is True else ''
        n = count(s)
        out.append(f"{'  '*d}- **{title}** (`{p.strip('/')}/`, {n} article{'s' if n != 1 else ''}){note}{flag}")
        for a in s.get('articles') or []:
            placed.append(a); out.append(f"{'  '*(d+1)}- {T[a]} (`{a}`)")
        walk(s.get('children') or [], d + 1, p, lg)
walk(data['sections'], 0, '', False)
missing = set(T) - set(placed); dup = len(placed) - len(set(placed)); unknown = set(placed) - set(T)
lines = open(root + '/data/structure.yaml').read().split('\n')
dec = []; on = False
for l in lines:
    if l.startswith('# Decisions'): on = True; continue
    if on:
        if not l.startswith('#'): break
        t = l[1:].rstrip()
        if set(t.strip()) <= {'-'}: continue
        if t.startswith('  - '): dec.append('- ' + t[4:])
        elif t.startswith('    '): dec[-1] += ' ' + t.strip()
        elif t.strip(): dec.append('\n### ' + t.strip() + '\n')
total = sum(count(s) for s in data['sections'])
hdr = f"""# Proposed documentation tree: review

Rendered from `data/structure.yaml` (the source of truth; regenerate this file rather than editing it by hand).
{total} articles, {stats['sections']} sections ({stats['index']} of them use an article as their index page), at most {stats['depth']} folder levels under `docs/`.
Check: {len(set(placed) & set(T))}/{len(T)} articles placed, {len(missing)} missing, {dup} duplicates, {len(unknown)} unknown slugs.

**Block-first.** The main tree describes what a fresh WordPress install gives you today: the block editor, a block
theme and the Site Editor. Everything that only applies to the Classic Editor plugin, to classic themes (widgets,
Customizer, Menus screen) or to classic-era media shortcodes is in **Classic WordPress**, the last top-level
section, marked `classic: true` ({stats['classic_articles']} articles in {stats['classic_sections']} sections; the flag is inherited by every
section below it and appears as `classic: true` in the generated frontmatter and manifest).

The old "Technical guides" top-level section is dissolved into Using WordPress ("Installation & hosting",
"Maintenance & security"), with two of its articles moved to more specific homes (see decisions).

## Tree

Counts include all descendants. Sections with an `index` take their title and intro from that article.
`classic: true` is shown on the section that sets it; everything below it inherits it.

"""
open(root + '/data/structure-review.md', 'w').write(hdr + '\n'.join(out) + '\n\n## Decisions\n' + '\n'.join(dec) + '\n')
print(stats, total, len(missing), dup, len(unknown))
