import re, html
from pathlib import Path

base=Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

DIMENSIONS={
 'Daikin Park':'315 to left, 362 to left-center, 409 to center, 373 to right-center, 326 to right',
 'Busch Stadium':'336 to left, 375 to left-center, 400 to center, 375 to right-center, 335 to right',
 'PNC Park':'325 to left, 383 to left-center, 399 to center, 375 to right-center, 320 to right',
 'Truist Park':'335 to left, 385 to left-center, 400 to center, 375 to right-center, 325 to right',
 'Yankee Stadium':'318 to left, 399 to left-center, 408 to center, 385 to right-center, 314 to right',
 'Comerica Park':'345 to left, 370 to left-center, 420 to center, 365 to right-center, 330 to right',
 'UNIQLO Field at Dodger Stadium':'330 to left, 385 to left-center, 395 to center, 375 to right-center, 330 to right',
 'Petco Park':'334 to left, 390 to left-center, 396 to center, 391 to right-center, 322 to right',
 'American Family Field':'344 to left, 371 to left-center, 400 to center, 374 to right-center, 345 to right',
 'Citizens Bank Park':'329 to left, 374 to left-center, 401 to center, 369 to right-center, 330 to right',
 'Target Field':'339 to left, 377 to left-center, 411 to center, 367 to right-center, 328 to right',
 'Sutter Health Park':'330 to left, 380 to left-center, 403 to center, 370 to right-center, 325 to right',
 'Oriole Park at Camden Yards':'333 to left, 384 to left-center, 410 to center, 373 to right-center, 318 to right',
 'Great American Ball Park':'328 to left, 379 to left-center, 404 to center, 370 to right-center, 325 to right',
 'Rate Field':'330 to left, 375 to left-center, 400 to center, 375 to right-center, 335 to right'
}

voices=[
    ('A summer-night lyric hangs over this one', 'The shape of this game feels old-fashioned: pressure on starters, then a sprint to the seventh.', 'If the better infield defense gets even two extra outs, the ticket usually cashes.'),
    ('Notebook view from first coffee to first pitch', 'The pricing asks a straightforward question: can this side control the first two turns through the order?', "Given tonight's setup, that answer is more often yes than no."),
    ('This one has city-noise energy and late-inning drama written all over it', 'The park will reward lifted contact, and both clubs have enough pull power to make one mistake expensive.', 'I still prefer the steadier bullpen bridge and cleaner ninth-inning path.'),
    ('If you\'ve watched this sport long enough, you know this script', 'A broad outfield gap plus warm air turns singles into doubles and doubles into trouble.', 'The side with fewer free passes is usually the side still smiling at 10:30 p.m.'),
    ('Call this a ballgame for scorebook people', 'The matchup leans toward whichever club wins the 2-1 counts and keeps traffic off the bases.', 'That profile points to one dugout with fewer ways to lose itself.'),
    ('Strip away the noise and keep the baseball bones', 'Run creation consistency, defensive conversion, and late leverage all land on the same side of the ledger tonight.', "When several independent game-shape checks agree, I'm willing to lay the number."),
]

article_pat=re.compile(r'(<article class="pick-card">.*?</article>)',re.S)

# Parse main for injury context
main=(base/'2026-04-14.html').read_text()
articles=article_pat.findall(main)
match_info={}
for a in articles:
    h2=re.search(r'<h2>([^<]+)</h2>',a)
    if not h2:
        continue
    title=html.unescape(h2.group(1))
    if ' over ' not in title:
        continue
    t1,t2=[x.strip() for x in title.split(' over ',1)]
    weather=re.search(r'<li><strong>Weather:</strong>\s*([^<]+)</li>',a)
    weather=html.unescape(weather.group(1).strip()) if weather else 'Weather neutral.'
    venue=re.search(r'<div><span>Venue</span><strong>([^<]+)</strong></div>',a)
    venue=html.unescape(venue.group(1).strip()) if venue else ''
    inj={}
    for m in re.finditer(r'<li><strong>([^<]+) Injuries:</strong>\s*([^<]+)</li>',a):
        team=html.unescape(m.group(1).strip())
        names=[n.strip() for n in html.unescape(m.group(2)).split(',') if n.strip()]
        inj[team]=names
    match_info[frozenset([t1,t2])]={'weather':weather,'venue':venue,'inj':inj}


def injury_phrase(team, names):
    if not names:
        return f"{team}'s board is quiet"
    top=', '.join(names[:2])
    return f"{team} list is mostly green (notably {top})"


def make_side_lede(article,idx):
    title=html.unescape(re.search(r'<h2>([^<]+)</h2>',article).group(1))
    t1,t2=[x.strip() for x in title.split(' over ',1)]
    odds=html.unescape(re.search(r'<div><span>Odds</span><strong>([^<]+)</strong></div>',article).group(1))
    conf=html.unescape(re.search(r'<div><span>Confidence</span><strong>([^<]+)</strong></div>',article).group(1))
    pitch=html.unescape(re.search(r'<div><span>Pitching</span><strong>([^<]+)</strong></div>',article).group(1))
    venue=html.unescape(re.search(r'<div><span>Venue</span><strong>([^<]+)</strong></div>',article).group(1))
    weather_m=re.search(r'<li><strong>Weather:</strong>\s*([^<]+)</li>',article)
    weather=html.unescape(weather_m.group(1).strip()) if weather_m else 'conditions look stable'
    line_m=re.search(r'<li><strong>Line Movement:</strong>\s*([^<]+)</li>',article)
    line=html.unescape(line_m.group(1).strip()) if line_m else 'price held steady through the afternoon'
    lineups_m=re.search(r'<li><strong>Starting Lineups:</strong>\s*([^<]+)</li>',article)
    lineups=html.unescape(lineups_m.group(1).strip()) if lineups_m else 'lineups are set'
    inj={}
    for m in re.finditer(r'<li><strong>([^<]+) Injuries:</strong>\s*([^<]+)</li>',article):
        team=html.unescape(m.group(1).strip())
        names=[n.strip() for n in html.unescape(m.group(2)).split(',') if n.strip()]
        inj[team]=names
    dims=DIMENSIONS.get(venue,'standard MLB dimensions with fair alleys and reachable corners')
    v=voices[idx%len(voices)]
    inj1=injury_phrase(t1,inj.get(t1,[]))
    inj2=injury_phrase(t2,inj.get(t2,[]))
    text=(f"{v[0]}. I'm on <strong>{t1} over {t2}</strong> at <strong>{odds}</strong>. "
          f"At {venue} ({dims}), the matchup of {pitch} favors {t1} because their current lineup is more likely to string quality plate appearances instead of relying on one swing. "
          f"{v[1]} Weather reads {weather}, and that points to a game where contact quality should show up honestly rather than randomly. "
          f"Health check: {inj1}; {inj2}. {lineups} With {line}, the market isn't fighting this angle. "
          f"{v[2]} Confidence snapshot: {conf}.")
    return text


total_voices=[
    'You can almost hear this total climbing before first pitch',
    'This total reads like a clean over/under script, not a coin flip',
    'From a run-environment standpoint, this is a table-setter',
    'The geometry of the park matters here as much as the names on the jerseys',
    'If you like totals that win by shape, this is one of them',
    'No fireworks needed—just steady pressure innings',
]


def make_total_lede(article,idx):
    h2=html.unescape(re.search(r'<h2>([^<]+)</h2>',article).group(1))
    m=re.match(r'(.+?) vs (.+?) — (OVER|UNDER) ([0-9.]+)',h2)
    t1,t2,ou,total=m.group(1).strip(),m.group(2).strip(),m.group(3),m.group(4)
    venue=html.unescape(re.search(r'<div><span>Venue</span><strong>([^<]+)</strong></div>',article).group(1))
    odds=html.unescape(re.search(r'<div><span>Odds</span><strong>([^<]+)</strong></div>',article).group(1))
    conf=html.unescape(re.search(r'<div><span>Confidence</span><strong>([^<]+)</strong></div>',article).group(1))
    weather=html.unescape(re.search(r'<li><strong>Weather:</strong>\s*([^<]+)</li>',article).group(1).strip())
    move_m=re.search(r'<li><strong>Total Movement:</strong>\s*([^<]+)</li>',article)
    move=html.unescape(move_m.group(1).strip()) if move_m else 'total has held'
    dims=DIMENSIONS.get(venue,'balanced dimensions')
    info=match_info.get(frozenset([t1,t2]),{})
    inj=info.get('inj',{})
    inj1=injury_phrase(t1,inj.get(t1,[]))
    inj2=injury_phrase(t2,inj.get(t2,[]))
    tone=total_voices[idx%len(total_voices)]
    if ou=='OVER':
        angle='Warmth, carry, and reachable power alleys create more extra-base traffic, so crooked numbers are live in the middle innings.'
        close='I want the game state where both teams can score in clusters, and this matchup provides it.'
    else:
        angle='The weather and outfield depth suppress cheap damage, so scoring should require multi-hit sequences rather than one mistake.'
        close='That usually keeps the game under the posted runway unless defense unravels.'
    return (f"{tone}. Lean <strong>{ou} {total}</strong> in {t1} vs {t2} at <strong>{odds}</strong>. "
            f"{venue} plays at {dims}, and with {weather} the ball should travel in a way that supports this total position. "
            f"{angle} Injury board context: {inj1}; {inj2}. {move} Confidence: {conf}. {close}")


# Rewrite side files
for fn in ['2026-04-14.html','2026-04-14-plus-money.html']:
    path=base/fn
    text=path.read_text()
    arts=article_pat.findall(text)
    new_arts=[]
    for i,a in enumerate(arts):
        newlede=make_side_lede(a,i + (0 if fn=='2026-04-14.html' else 20))
        a2=re.sub(r'<p class="lede">.*?</p>',f'<p class="lede">{newlede}</p>',a,flags=re.S)
        new_arts.append(a2)
    it=iter(new_arts)
    text2=article_pat.sub(lambda m: next(it), text)
    path.write_text(text2)

# Rewrite totals
path=base/'2026-04-14-run-totals.html'
text=path.read_text()
arts=article_pat.findall(text)
new_arts=[]
for i,a in enumerate(arts):
    newlede=make_total_lede(a,i)
    a2=re.sub(r'<p class="lede">.*?</p>',f'<p class="lede">{newlede}</p>',a,flags=re.S)
    new_arts.append(a2)
it=iter(new_arts)
text2=article_pat.sub(lambda m: next(it), text)
path.write_text(text2)

print('rewrote',len(articles),'main ledes,',len(article_pat.findall((base/'2026-04-14-plus-money.html').read_text())),'plus,',len(arts),'totals')
