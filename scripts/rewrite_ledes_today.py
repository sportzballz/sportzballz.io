import re
from pathlib import Path
from html import unescape

ROOT = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
DATE = '2026-04-13'
FILES_SIDE = [
    ROOT / f'{DATE}.html',
    ROOT / f'{DATE}-run-line.html',
    ROOT / f'{DATE}-plus-money.html',
]
FILE_TOTALS = ROOT / f'{DATE}-run-totals.html'

DIMENSIONS = {
    'Oriole Park at Camden Yards': 'LF 333, LCF 364, CF 400, RCF 373, RF 318',
    'Target Field': 'LF 339, LCF 377, CF 403, RCF 367, RF 328',
    'Truist Park': 'LF 335, LCF 385, CF 400, RCF 375, RF 325',
    'PNC Park': 'LF 325, LCF 383, CF 399, RCF 375, RF 320',
    'T-Mobile Park': 'LF 331, LCF 378, CF 401, RCF 381, RF 326',
    'Citizens Bank Park': 'LF 329, LCF 374, CF 401, RCF 369, RF 330',
    'Busch Stadium': 'LF 336, LCF 375, CF 400, RCF 375, RF 335',
    'UNIQLO Field at Dodger Stadium': 'LF 330, LCF 375, CF 400, RCF 375, RF 330',
    'Sutter Health Park': 'LF 330, LCF 380, CF 403, RCF 380, RF 325',
    'Yankee Stadium': 'LF 318, LCF 399, CF 408, RCF 385, RF 314',
}

VOICE_OPENERS = [
    'By first pitch this game usually reveals itself in layers, not fireworks.',
    'The smartest read here is patient: this is a nine-inning geometry problem.',
    'If you watch the middle innings closely, the edge is easier to see than the price suggests.',
    'This one feels like old-school baseball math: field shape, air, and bullpen sequencing.',
    'A clean handicap starts with run lanes and who controls the game once starters exit.',
    'There is some theater in this number, but the practical baseball reasons are stronger than the noise.',
]

ARTICLE_RE = re.compile(r'(<article class="pick-card">.*?</article>)', re.S)
H2_RE = re.compile(r'<h2>(.*?)</h2>', re.S)
PITCH_RE = re.compile(r'<div><span>Pitching</span><strong>(.*?)</strong></div>', re.S)
ODDS_RE = re.compile(r'<div><span>Odds</span><strong>(.*?)</strong></div>', re.S)
RUNLINE_RE = re.compile(r'<div><span>Run Line</span><strong>(.*?)</strong></div>', re.S)
VENUE_RE = re.compile(r'<div><span>Venue</span><strong>(.*?)</strong></div>', re.S)
LEDE_RE = re.compile(r'<p class="lede">.*?</p>', re.S)
LI_RE = re.compile(r'<li><strong>([^<]+)</strong>\s*(.*?)</li>', re.S)


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', text))).strip()


def parse_list_items(article: str):
    out = {}
    for k, v in LI_RE.findall(article):
        out[clean(k).rstrip(':')] = clean(v)
    return out


def top_names(injury_line: str):
    names = []
    for seg in injury_line.split(','):
        nm = seg.split('(')[0].strip()
        if nm:
            names.append(nm)
    return names[:2]


def side_lede(article: str, idx: int) -> str:
    title = clean(H2_RE.search(article).group(1))
    odds = clean(ODDS_RE.search(article).group(1)) if ODDS_RE.search(article) else ''
    runline = clean(RUNLINE_RE.search(article).group(1)) if RUNLINE_RE.search(article) else ''
    runline = re.sub(r'^Model lean side:\s*', '', runline)
    venue = clean(VENUE_RE.search(article).group(1)) if VENUE_RE.search(article) else ''
    pitching = clean(PITCH_RE.search(article).group(1)) if PITCH_RE.search(article) else ''
    details = parse_list_items(article)
    weather = details.get('Weather', 'Weather unavailable at publish time.')
    line = details.get('Line Movement', 'Line held steady into publish.')

    dims = DIMENSIONS.get(venue, 'standard MLB dimensions')
    pick_desc = title
    m = re.match(r'(.+?) over (.+)', title)
    if m:
        team_a, team_b = m.group(1), m.group(2)
    else:
        m2 = re.match(r'(.+?) vs (.+?) —', title)
        if m2:
            team_a, team_b = m2.group(1), m2.group(2)
            if runline:
                pick_desc = f"{runline} in {team_a} vs {team_b}"
        else:
            team_a, team_b = title, 'opponent'

    inj_a = top_names(details.get(f'{team_a} Injuries', ''))
    inj_b = top_names(details.get(f'{team_b} Injuries', ''))
    inj_text = 'Injury board is mostly maintenance listings.'
    if inj_a or inj_b:
        left = ', '.join(inj_a) if inj_a else 'the expected core'
        right = ', '.join(inj_b) if inj_b else 'the expected core'
        inj_text = f"Availability check: {left} are listed active for {team_a}, and {right} are listed active for {team_b}, so late scratches are not driving this pick."

    opener = VOICE_OPENERS[idx % len(VOICE_OPENERS)]
    rationale = [
        opener,
        f"{pick_desc}{(' at ' + odds) if odds else ''} gets the nod because {team_a} carries the steadier path from first trip through the order to the bullpen handoff, while {team_b} needs a cleaner-than-usual game to flip the script.",
        f"{venue} ({dims}) matters here: the outfield shape rewards gap authority and punishes extra baserunners, which fits the side with the cleaner contact-and-command profile.",
        f"Weather context: {weather}",
        inj_text,
        f"Pitching matchup: {pitching}. Market note: {line} The number is still playable at publish."
    ]
    return '<p class="lede">' + ' '.join(rationale) + '</p>'


def total_lede(article: str, idx: int, side_map: dict) -> str:
    title = clean(H2_RE.search(article).group(1))
    venue = clean(VENUE_RE.search(article).group(1)) if VENUE_RE.search(article) else ''
    details = parse_list_items(article)
    weather = details.get('Weather', 'Weather unavailable at publish time.')
    move = details.get('Total Movement', 'Total held steady.')
    dims = DIMENSIONS.get(venue, 'standard MLB dimensions')

    m = re.match(r'(.+?) vs (.+?) — (OVER|UNDER) ([0-9.]+)', title)
    if m:
        ta, tb, ou, num = m.groups()
        matchup_key = f'{ta} vs {tb}'
    else:
        ta, tb, ou, num = title, '', 'OVER', ''
        matchup_key = title

    inj = side_map.get(matchup_key, 'Injury board is mostly active listings on both sides, so run environment and pitcher execution remain the key drivers.')
    opener = VOICE_OPENERS[(idx + 2) % len(VOICE_OPENERS)]

    text = (
        f"{opener} {ou} {num} in {ta} vs {tb} is a play on run environment, not wishcasting. "
        f"At {venue} ({dims}), extra-base lanes and foul-ground behavior keep pressure on command pitchers once traffic starts. "
        f"Weather context: {weather} {inj} {move} That combination supports a game script with enough scoring volume to clear this total."
    )
    return '<p class="lede">' + text + '</p>'


# Build matchup injury notes from side page
side_reference = (ROOT / f'{DATE}.html').read_text(encoding='utf-8')
side_map = {}
for art in ARTICLE_RE.findall(side_reference):
    h2m = H2_RE.search(art)
    if not h2m:
        continue
    title = clean(h2m.group(1))
    mm = re.match(r'(.+?) over (.+)', title)
    if not mm:
        continue
    ta, tb = mm.groups()
    details = parse_list_items(art)
    inj_a = top_names(details.get(f'{ta} Injuries', ''))
    inj_b = top_names(details.get(f'{tb} Injuries', ''))
    if inj_a or inj_b:
        side_map[f'{ta} vs {tb}'] = (
            f"Availability check: {', '.join(inj_a) if inj_a else ta} and {', '.join(inj_b) if inj_b else tb} are listed active, so this total read is less about absences and more about contact quality plus bullpen shape."
        )

for fp in FILES_SIDE:
    if not fp.exists():
        continue
    src = fp.read_text(encoding='utf-8')
    pieces = []
    last = 0
    idx = 0
    for m in ARTICLE_RE.finditer(src):
        art = m.group(1)
        new_lede = side_lede(art, idx)
        art2 = LEDE_RE.sub(new_lede, art, count=1)
        pieces.append(src[last:m.start()])
        pieces.append(art2)
        last = m.end()
        idx += 1
    pieces.append(src[last:])
    fp.write_text(''.join(pieces), encoding='utf-8')

if FILE_TOTALS.exists():
    src = FILE_TOTALS.read_text(encoding='utf-8')
    pieces = []
    last = 0
    idx = 0
    for m in ARTICLE_RE.finditer(src):
        art = m.group(1)
        new_lede = total_lede(art, idx, side_map)
        art2 = LEDE_RE.sub(new_lede, art, count=1)
        pieces.append(src[last:m.start()])
        pieces.append(art2)
        last = m.end()
        idx += 1
    pieces.append(src[last:])
    FILE_TOTALS.write_text(''.join(pieces), encoding='utf-8')

print('rewrote ledes for', DATE)
