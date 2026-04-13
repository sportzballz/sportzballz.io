import re, random
from pathlib import Path

ROOT = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
FILES = [
    ROOT/'2026-04-08.html',
    ROOT/'2026-04-08-plus-money.html',
    ROOT/'2026-04-08-run-line.html',
    ROOT/'2026-04-08-run-totals.html',
]

ANALYST_PANEL = [
 {'id': 'mack-ledger', 'name': 'Mack Ledger', 'title': 'Market Maker', 'style': 'market'},
 {'id': 'nora-splitter', 'name': 'Nora Splitter', 'title': 'Matchup Film Room', 'style': 'matchup'},
 {'id': 'dex-numbers', 'name': 'Dex Numbers', 'title': 'Quant', 'style': 'quant'},
 {'id': 'rico-heatcheck', 'name': 'Rico Heatcheck', 'title': 'Momentum & Vibes', 'style': 'energy'},
 {'id': 'grant-halberd', 'name': 'Grant Halberd', 'title': 'Beat Writer', 'style': 'journal'},
 {'id': 'ivy-chen', 'name': 'Ivy Chen', 'title': 'Data Scientist', 'style': 'quant'},
 {'id': 'toby-quinn', 'name': 'Toby Quinn', 'title': 'Contrarian', 'style': 'contrarian'},
 {'id': 'lena-park', 'name': 'Lena Park', 'title': 'Weather/Umpire Specialist', 'style': 'context'},
 {'id': 'vince-valentino', 'name': 'Vince Valentino', 'title': 'Showman', 'style': 'energy'},
 {'id': 'maya-rios', 'name': 'Maya Rios', 'title': 'Process Coach', 'style': 'discipline'},
 {'id': 'owen-pike', 'name': 'Owen Pike', 'title': 'Model Whisperer', 'style': 'model'},
 {'id': 'jules-archer', 'name': 'Jules Archer', 'title': 'Underdog Hunter', 'style': 'underdog'},
 {'id': 'roman-slate', 'name': 'Roman Slate', 'title': 'Line Movement Hawk', 'style': 'market'},
 {'id': 'keira-bloom', 'name': 'Keira Bloom', 'title': 'Injury/Lineup Impact', 'style': 'availability'},
 {'id': 'eli-mercer', 'name': 'Eli Mercer', 'title': 'Totals Architect', 'style': 'totals'},
 {'id': 'sanjay-vale', 'name': 'Sanjay Vale', 'title': 'CLV Auditor', 'style': 'discipline'},
]

PAT = re.compile(r'<p class="lede">(.*?)</p>', re.S)

BANNED = [
 'avg','groundOuts','airOuts','runs','doubles','triples','homeRuns','rbi','whip','strikeoutWalkRatio',
 'strikeoutsPer9Inn','walksPer9Inn','hitsPer9Inn','runsScoredPer9','homeRunsPer9','era','strikePercentage'
]

last_id = None


def pick_analyst():
    global last_id
    choices = [a for a in ANALYST_PANEL if a['id'] != last_id] or ANALYST_PANEL
    a = random.choice(choices)
    last_id = a['id']
    return a


def clean_source(text):
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'^[^—]{2,140}—\s*', '', t)
    return t


def extract(src):
    pick = re.search(r'([A-Za-z .\-\'’]+ over [A-Za-z .\-\'’]+ at [+-]?\d+)', src)
    conf = re.search(r'confidence\s+([0-9]+\.[0-9]+)', src, re.I)
    dp = re.search(r'\(([0-9.]+/[0-9.]+|[0-9]+/[0-9]+)\)', src)
    line = re.search(r'(line(?:\s|-)movement[^\.]*\.|market[^\.]*\.)', src, re.I)
    lineup = re.search(r'(lineups?[^\.]*\.)', src, re.I)
    weather = re.search(r'(weather[^\.]*\.|roof[^\.]*\.|umpire[^\.]*\.)', src, re.I)
    def clean_frag(x, fallback):
        if not x:
            return fallback
        t = x.strip().strip('() ')
        t = re.sub(r'^(line(?:\s|-)movement\s*[:\-]?\s*)', '', t, flags=re.I)
        t = re.sub(r'^(market\s*movement\s*[:\-]?\s*)', '', t, flags=re.I)
        t = re.sub(r'^(weather\s*[:\-]?\s*)', '', t, flags=re.I)
        t = re.sub(r'^(roof\s*[:\-]?\s*)', 'Roof: ', t, flags=re.I)
        t = re.sub(r'^(lineups?\s*[:\-]?\s*)', '', t, flags=re.I)
        t = re.sub(r'\s+', ' ', t).strip()
        if not t.endswith('.'):
            t += '.'
        return t

    return {
      'pick': pick.group(1) if pick else src.split('.')[0],
      'conf': conf.group(1) if conf else None,
      'dp': dp.group(1) if dp else None,
      'line': clean_frag(line.group(1) if line else None, 'Market movement is modest into first pitch.'),
      'lineup': clean_frag(lineup.group(1) if lineup else None, 'Lineup status remains an important pregame checkpoint.'),
      'weather': clean_frag(weather.group(1) if weather else None, 'Weather and umpire context look neutral right now.'),
    }


def body(style, d):
    conf_part = f"The model sits at {d['conf']} with {d['dp']} behind it." if d['conf'] and d['dp'] else "The model still grades this as a playable side."
    base = {
      'market': f"{d['pick']}. {conf_part} Pricing context matters here: {d['line']} The underlying profile points to cleaner run creation, steadier run prevention, and fewer self-inflicted innings. Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} Bottom line: this is still the right side at current price.",
      'matchup': f"{d['pick']}. {conf_part} From a pure game-script angle, one side carries the more stable start-to-finish profile while the opponent needs too many breaks to flip the script. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} If this board stays near current numbers, the lean is justified.",
      'quant': f"{d['pick']}. {conf_part} The probability edge is not coming from one flashy stat; it comes from a broader balance of contact quality, run prevention stability, and lower variance paths late. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} The expected-value case remains intact.",
      'energy': f"Here’s the card: {d['pick']}. {conf_part} The better side looks sharper in all the spots that usually decide this game—traffic conversion, cleaner innings, and fewer momentum-killing mistakes. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} This is a confident, fan-readable side.",
      'journal': f"{d['pick']}. {conf_part} The read is straightforward: one club enters with the steadier two-way shape, while the other is chasing upside with a thinner margin for error. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} At this number, the recommendation still holds.",
      'contrarian': f"{d['pick']}. {conf_part} This spot works because the market isn’t fully pricing the stability gap between these clubs. The preferred side has the cleaner path over nine innings, while the other relies on volatility to steal it. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} That’s enough to stay on this number.",
      'context': f"{d['pick']}. {conf_part} The side holds up on matchup quality, but context is what keeps it playable: Weather and umpire context: {d['weather']} Lineup status: {d['lineup']} {d['line']} With those conditions, the edge remains practical rather than theoretical.",
      'discipline': f"{d['pick']}. {conf_part} Treat this as a disciplined edge, not a hero bet. The preferred side owns the steadier profile across offense-to-prevention balance and should generate fewer high-stress innings. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} Keep process first and the side still makes sense.",
      'model': f"{d['pick']}. {conf_part} The model’s direction aligns with how this game likely unfolds: one team has the more repeatable run profile and better path to hold leverage late. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} It’s not flashy, but it is a solid edge.",
      'underdog': f"{d['pick']}. {conf_part} The value case here comes from resilience and path quality, not noise. The selected side has enough two-way stability to justify backing this number, especially if the market keeps the price in range. {d['line']} Lineup status: {d['lineup']} Weather and umpire context: {d['weather']} This remains a selective but playable ticket.",
      'availability': f"{d['pick']}. {conf_part} Availability and continuity matter in this matchup, and the preferred side looks less fragile heading into first pitch. Lineup status: {d['lineup']} {d['line']} Weather and umpire context: {d['weather']} With fewer roster question marks, the edge is cleaner than it might look on first glance.",
      'totals': f"{d['pick']}. {conf_part} The run environment points to a stable script: cleaner prevention on one side and a more reliable scoring floor across the game. Weather and umpire context: {d['weather']} {d['line']} Lineup status: {d['lineup']} That blend keeps the recommendation intact.",
    }
    return base.get(style, base['journal'])


def sanitize(text):
    t = re.sub(r'\s+', ' ', text).strip()
    for b in BANNED:
        t = re.sub(rf'\b{re.escape(b)}\b', 'team-strength signal', t, flags=re.I)
    t = re.sub(r'\b(prediction model|confidence rating|data points)\b', 'model view', t, flags=re.I)
    return t


for fp in FILES:
    if not fp.exists():
        continue
    src = fp.read_text(encoding='utf-8')
    out = []
    last = 0
    count = 0
    for m in PAT.finditer(src):
        raw = clean_source(m.group(1))
        d = extract(raw)
        a = pick_analyst()
        paragraph = body(a['style'], d)
        paragraph = sanitize(paragraph)
        paragraph = f"{a['name']} ({a['title']}) — {paragraph}"
        out.append(src[last:m.start()])
        out.append(f'<p class="lede">{paragraph}</p>')
        last = m.end()
        count += 1
    out.append(src[last:])
    if count:
        fp.write_text(''.join(out), encoding='utf-8')
    print(fp.name, count)
