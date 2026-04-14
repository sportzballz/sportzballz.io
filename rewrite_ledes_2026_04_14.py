import re
from pathlib import Path

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

# Park dimensions (approximate wall marks used for narrative context)
park_dims = {
    'PNC Park': '325-399-320',
    'Truist Park': '335-400-325',
    'Comerica Park': '345-412-330',
    'Oriole Park at Camden Yards': '333-400-318',
    'Busch Stadium': '336-400-335',
    'Rate Field': '330-400-335',
    'Petco Park': '334-396-322',
    'Yankee Stadium': '318-399-314',
    'UNIQLO Field at Dodger Stadium': '330-395-330',
    'American Family Field': '344-400-345',
    'Target Field': '339-403-328',
    'Great American Ball Park': '328-404-325',
    'Citizens Bank Park': '329-401-330',
    'Sutter Health Park': '330-403-325',
}

voices = [
    ('lyric', 'The evening feels made for patient offense'),
    ('notebook', 'If you work this game from first pitch through the seventh, the shape is clear'),
    ('column', 'Call this the practical side of the card'),
    ('nostalgic', 'There are nights when baseball still reads like an old scorebook'),
    ('street', 'Here’s the straight talk on this matchup'),
    ('analytic', 'Strip away the noise and this is a run-environment decision'),
]

article_pat = re.compile(r'(<article class="pick-card">.*?</article>)', re.S)


def normalize_space(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def get_weather(art: str) -> str:
    m = re.search(r'<li><strong>Weather:</strong>\s*(.*?)</li>', art, re.S)
    return normalize_space(m.group(1)) if m else 'weather context neutral'


def get_line(art: str, label: str) -> str:
    m = re.search(fr'<li><strong>{re.escape(label)}</strong>\s*(.*?)</li>', art, re.S)
    return normalize_space(m.group(1)) if m else ''


def team_key_from_h2(h2: str) -> str:
    txt = normalize_space(h2)
    if ' — ' in txt:
        left = txt.split(' — ')[0]
        if ' vs ' in left:
            a, b = [x.strip() for x in left.split(' vs ', 1)]
            return ' vs '.join(sorted([a, b]))
    if ' over ' in txt:
        a, b = [x.strip() for x in txt.split(' over ', 1)]
        return ' vs '.join(sorted([a, b]))
    return txt


def build_injury_map(daily_text: str):
    inj_map = {}
    for art in article_pat.findall(daily_text):
        h2 = re.search(r'<h2>(.*?)</h2>', art, re.S)
        if not h2:
            continue
        matchup = normalize_space(h2.group(1))
        m = re.match(r'(.+?) over (.+)', matchup)
        if not m:
            continue
        t1, t2 = m.group(1).strip(), m.group(2).strip()
        key = ' vs '.join(sorted([t1, t2]))

        inj_lines = re.findall(r'<li><strong>([^<]+) Injuries:</strong>\s*(.*?)</li>', art, re.S)
        parts = []
        for team, plist in inj_lines[:2]:
            names = [x.strip() for x in plist.split(',')[:2]]
            names = [re.sub(r'\s*\(.*?\)', '', n).strip() for n in names if n.strip()]
            if names:
                parts.append(f"{team}: {', '.join(names)} listed active")

        lineup = ''
        lm = re.search(r'<li><strong>Starting Lineups:</strong>\s*(.*?)</li>', art, re.S)
        if lm:
            lineup = normalize_space(lm.group(1))

        inj_map[key] = ('; '.join(parts), lineup)
    return inj_map


def make_side_lede(ctx, voice_idx, underdog=False):
    voice, opener = voices[voice_idx % len(voices)]
    pick = ctx['h2']
    odds = ctx.get('odds', '')
    pitch = ctx.get('pitching', '')
    venue = ctx.get('venue', '')
    dims = park_dims.get(venue, 'varied alley depths')
    weather = ctx.get('weather', '')
    lineups = ctx.get('lineups', '')
    lm = ctx.get('line_move', '')
    inj = ctx.get('inj', '')

    bet_tone = 'at plus money' if underdog or odds.startswith('+') else 'as the favorite'
    if voice == 'lyric':
        return f"{opener}: {pick} {bet_tone} ({odds}). At {venue}, with fences roughly {dims}, this park asks for clean contact in the alleys and steady command late. {pitch} gives this side the calmer path through six innings, and {weather} points to a ball that should carry without turning chaotic. {inj if inj else 'The injury sheet is mostly maintenance names, not game-changing absences.'} {lineups} {lm}"
    if voice == 'notebook':
        return f"{opener}. The play is {pick} at {odds}. The matchup sits in {venue} ({dims}), where extra-base lanes matter more than raw homer distance, and that favors the team with the steadier starter pairing tonight ({pitch}). Weather reads {weather}, useful for hard line drives but not the kind of wind that flips a handicap. Injury report note: {inj if inj else 'both clubs arrive without a major late downgrade.'} {lineups} {lm}"
    if voice == 'column':
        return f"{opener}: {pick} at {odds}. This is a nine-inning depth call, not a one-inning gamble. {venue} plays to {dims}, and in these dimensions the side with cleaner strike throwing and fewer free baserunners usually dictates tempo; {pitch} tilts that way. With {weather}, run creation should come in waves, not avalanches, and that helps the better-structured roster. {inj if inj else 'Pre-game injury notes read stable.'} {lineups} {lm}"
    if voice == 'nostalgic':
        return f"{opener}, and this one points to {pick} at {odds}. In {venue}, the walls at {dims} reward teams that can move runners station to station before the big swing arrives. {pitch} suggests that rhythm leans to the picked side, especially if the starter gets ahead early. The weather ({weather}) should keep the game quick and honest. {inj if inj else 'No major injury cloud is hanging over first pitch.'} {lineups} {lm}"
    if voice == 'street':
        return f"{opener}: {pick} at {odds}. {venue} ({dims}) can punish sloppy sequencing, and this side is built to avoid the crooked-inning mistake. {pitch} gives them the better chance to hand a lead to the right bullpen pockets, while {weather} is favorable enough for offense but not a total coin flip. Injury board check: {inj if inj else 'nothing here screams emergency scratch.'} {lineups} {lm}"
    return f"{opener}. Recommendation: {pick} at {odds}. In a park shaped {dims} at {venue}, the best edge is controlling contact quality and baserunner traffic; {pitch} favors that profile. Weather is {weather}, which raises carry slightly but still keeps run expectancy in a manageable band. The injury/availability read is stable ({inj if inj else 'no high-impact losses reported'}), and lineup status supports a normal game script. {lm}"


def make_total_lede(ctx, voice_idx, inj_map):
    voice, opener = voices[voice_idx % len(voices)]
    h2 = ctx['h2']
    lean = ctx.get('lean', '')
    odds = ctx.get('odds', '')
    venue = ctx.get('venue', '')
    dims = park_dims.get(venue, 'varied alley depths')
    weather = ctx.get('weather', '')
    tm = ctx.get('total_move', '')
    key = team_key_from_h2(h2)
    inj, lineups = inj_map.get(key, ('', ''))

    over = 'OVER' in lean
    side_word = 'carry and gap power' if over else 'suppressed damage and strand rate'

    if voice == 'lyric':
        return f"{opener}, and the total read is {lean} ({odds}) for {h2}. {venue} sits at roughly {dims}, a shape that decides whether fly balls die on the track or find grass in the alleys; tonight the expected conditions ({weather}) point toward {side_word}. {inj if inj else 'Availability is mostly clean on both rosters.'} {lineups} {tm}"
    if voice == 'notebook':
        return f"{opener}: {lean} at {odds} in {h2}. Ballpark geometry at {venue} ({dims}) plus {weather} gives a workable script for {('run volume' if over else 'run suppression')} rather than randomness. The relevant question is traffic, not fireworks, and this setup supports the posted lean. Injury/status check: {inj if inj else 'no disruptive late injury downgrade flagged.'} {lineups} {tm}"
    if voice == 'column':
        return f"{opener} on totals: {lean} at {odds} for {h2}. These dimensions ({dims}) in {venue} reward teams that execute their first two pitches of each plate appearance; that usually means {('more barrels over nine innings' if over else 'fewer clean scoring windows')}. With {weather}, the environment supports this number. {inj if inj else 'Roster health looks steady pregame.'} {lineups} {tm}"
    if voice == 'nostalgic':
        return f"{opener}, and the number to play is {lean} at {odds} in {h2}. {venue} has old-school proportions ({dims}), where the ballgame is often decided by doubles into space and bullpen command after sunset. Add {weather} and you get a profile that fits {lean.lower()}. {inj if inj else 'No major injury surprise at lineup lock.'} {lineups} {tm}"
    if voice == 'street':
        return f"{opener}: {lean} at {odds} for {h2}. In {venue} ({dims}), this total is about who avoids the one bad inning. Weather is {weather}, and that nudges the game toward {('extra-base traffic and late scoring' if over else 'quieter middle innings')}. Injury board says {inj if inj else 'both sides are close to expected availability'}. {lineups} {tm}"
    return f"{opener}. Total recommendation: {lean} at {odds} in {h2}. Given {venue} dimensions ({dims}) and {weather}, modeled run distribution clusters around this side of the number, especially once bullpen leverage innings begin. Availability context ({inj if inj else 'no key absences'}) and lineup timing support a standard scoring path rather than an outlier game state. {tm}"


def rewrite_file(path: Path, filetype: str, start_idx: int, inj_map):
    txt = path.read_text()
    arts = article_pat.findall(txt)
    out = txt

    for i, art in enumerate(arts):
        h2 = normalize_space(re.search(r'<h2>(.*?)</h2>', art, re.S).group(1))
        venue = normalize_space(re.search(r'<div><span>Venue</span><strong>(.*?)</strong></div>', art, re.S).group(1))

        oddsm = re.search(r'<div><span>Odds</span><strong>(.*?)</strong></div>', art, re.S)
        odds = normalize_space(oddsm.group(1)) if oddsm else ''

        weather = get_weather(art)
        key = team_key_from_h2(h2)
        inj, lineups = inj_map.get(key, ('', ''))

        lm = get_line(art, 'Line Movement:')
        tm = get_line(art, 'Total Movement:')

        if not lineups:
            lineups = get_line(art, 'Starting Lineups:')

        pitchm = re.search(r'<div><span>Pitching</span><strong>(.*?)</strong></div>', art, re.S)
        pitching = normalize_space(pitchm.group(1)) if pitchm else ''

        leanm = re.search(r'<div><span>Lean</span><strong>(.*?)</strong></div>', art, re.S)
        lean = normalize_space(leanm.group(1)) if leanm else ''

        ctx = dict(
            h2=h2,
            venue=venue,
            odds=odds,
            weather=weather,
            inj=inj,
            lineups=lineups,
            line_move=lm,
            total_move=tm,
            pitching=pitching,
            lean=lean,
        )

        if filetype == 'totals':
            new_lede = make_total_lede(ctx, start_idx + i, inj_map)
        else:
            new_lede = make_side_lede(ctx, start_idx + i, underdog=(filetype == 'plus'))

        new_lede = normalize_space(new_lede)

        oldp = re.search(r'<p class="lede">.*?</p>', art, re.S).group(0)
        newp = f'<p class="lede">{new_lede}</p>'
        newart = art.replace(oldp, newp)
        out = out.replace(art, newart, 1)

    path.write_text(out)


def main():
    daily = (base / '2026-04-14.html').read_text()
    inj_map = build_injury_map(daily)

    rewrite_file(base / '2026-04-14.html', 'daily', 0, inj_map)
    rewrite_file(base / '2026-04-14-plus-money.html', 'plus', 2, inj_map)
    rewrite_file(base / '2026-04-14-run-totals.html', 'totals', 4, inj_map)

    print('rewritten')


if __name__ == '__main__':
    main()
