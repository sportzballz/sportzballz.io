import re, html
from pathlib import Path

root=Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
files=['2026-04-08.html','2026-04-08-plus-money.html','2026-04-08-run-line.html','2026-04-08-run-totals.html']

voices=[
    ('Avery Cross','Market Pulse Analyst'),
    ('Nora Finch','Matchup Strategist'),
    ('Theo Vance','Value Board Editor'),
    ('Lena Mercer','Clubhouse Context Lead'),
    ('Cal Rowan','Risk Management Desk'),
    ('Ivy Clarke','Weather and Venue Analyst'),
    ('Miles Hart','Line Movement Correspondent'),
    ('Sage Bennett','Game Script Analyst'),
    ('Rory Hale','Probability Desk Editor'),
    ('Quinn Harper','Situational Edge Analyst'),
]

side_openers=[
    "{team_a} over {team_b} at {odds} is the current lean.",
    "Board read still points to {team_a} over {team_b} at {odds}.",
    "Ticket angle remains {team_a} over {team_b} on {odds}.",
    "Primary side stays {team_a} over {team_b} with a posted {odds}.",
]
side_edge_lines=[
    "The model frame favors this side on stronger overall game shape and matchup pressure.",
    "Projection support leans to this dugout on broader form and situational fit.",
    "This side keeps the edge through cleaner profile balance and opponent pressure points.",
    "The lean comes from a steadier all-around profile with fewer red flags on paper.",
]

runline_openers=[
    "Run-line card opens with {lean} as the preferred side.",
    "For run line exposure, the page lean is {lean}.",
    "The listed run-line side remains {lean}.",
    "Run-line posture favors {lean} right now.",
]

total_openers=[
    "Totals lean is {lean} for {matchup}.",
    "Current total position stays {lean} in {matchup}.",
    "For this matchup, the totals board points to {lean}.",
    "Posted totals angle remains {lean} on {matchup}.",
]

voice_i=0

def next_voice():
    global voice_i
    v=voices[voice_i % len(voices)]
    voice_i += 1
    return v, (voice_i-1)

def clean(s):
    return re.sub(r'\s+',' ',html.unescape(re.sub('<.*?>','',s))).strip()

def parse_meta(article):
    pairs=re.findall(r'<div><span>(.*?)</span><strong>(.*?)</strong></div>',article,re.S)
    out={}
    for k,v in pairs:
        out[clean(k).rstrip(':')]=clean(v)
    return out

def parse_details(article):
    items=re.findall(r'<li><strong>(.*?):</strong>\s*(.*?)</li>',article,re.S)
    out={}
    for k,v in items:
        out[clean(k)]=clean(v)
    return out

def parse_matchup(h2):
    h=clean(h2)
    if ' over ' in h:
        a,b=h.split(' over ',1)
        return a.strip(), b.strip()
    if ' vs ' in h:
        a,b=h.split(' vs ',1)
        b=b.split(' — ')[0].strip()
        return a.strip(), b.strip()
    return h,None

def build_lede(page,article,idx):
    (name,title),vidx=next_voice()
    h2m=re.search(r'<h2>(.*?)</h2>',article,re.S)
    h2=clean(h2m.group(1)) if h2m else 'Matchup'
    meta=parse_meta(article)
    details=parse_details(article)

    if page.endswith('run-totals.html'):
        lean=meta.get('Lean','totals lean pending')
        conf=meta.get('Confidence')
        price=meta.get('Price')
        venue=meta.get('Venue')
        weather=details.get('Weather')
        move=details.get('Total Movement')

        opener=total_openers[(idx+vidx)%len(total_openers)].format(lean=lean, matchup=h2.split(' — ')[0])
        parts=[f"{name} ({title}) — {opener}"]
        if conf: parts.append(f"Confidence is {conf}.")
        if price: parts.append(f"Price reference sits at {price}.")
        if venue: parts.append(f"Venue: {venue}.")
        if weather: parts.append(f"Weather context: {weather}.")
        if move: parts.append(f"Total movement note: {move}")
        return '<p class="lede">'+' '.join(parts)+'</p>'

    team_a,team_b=parse_matchup(h2)

    if page.endswith('run-line.html'):
        lean=meta.get('Run Line','Model lean side unavailable').replace('Model lean side: ','')
        conf=meta.get('Confidence')
        pitching=meta.get('Pitching')
        venue=meta.get('Venue')

        opener=runline_openers[(idx+vidx)%len(runline_openers)].format(lean=lean)
        parts=[f"{name} ({title}) — {opener}"]
        if conf: parts.append(f"Model confidence is {conf}.")
        if team_a and team_b: parts.append(f"Matchup is {team_a} vs {team_b}.")
        if pitching: parts.append(f"Starting pitching listed: {pitching}.")
        if venue: parts.append(f"Venue: {venue}.")
        parts.append(side_edge_lines[(idx*2+vidx)%len(side_edge_lines)])
        return '<p class="lede">'+' '.join(parts)+'</p>'

    # Daily + plus-money
    odds=meta.get('Odds')
    conf=meta.get('Confidence')
    pitching=meta.get('Pitching')
    venue=meta.get('Venue')
    weather=details.get('Weather')
    ump=details.get('Umpire Crew')
    move=details.get('Line Movement')
    lineup=details.get('Starting Lineups')
    lineup_impact=details.get('Lineup Change Impact')

    if team_a and team_b and odds:
        opener=side_openers[(idx+vidx)%len(side_openers)].format(team_a=team_a,team_b=team_b,odds=odds)
    elif team_a and team_b:
        opener=f"{team_a} over {team_b} remains the listed side."
    else:
        opener=f"{h2} remains on the card."

    parts=[f"{name} ({title}) — {opener}"]
    if conf: parts.append(f"Model confidence is {conf}.")
    if pitching: parts.append(f"Pitching matchup: {pitching}.")
    if venue: parts.append(f"Venue: {venue}.")
    parts.append(side_edge_lines[(idx+vidx)%len(side_edge_lines)])

    ctx=[]
    if weather: ctx.append(f"weather ({weather})")
    if ump: ctx.append(f"umpire crew ({ump})")
    if move: ctx.append(f"market move ({move})")
    if ctx: parts.append('Context check: ' + ', '.join(ctx) + '.')

    if lineup: parts.append(f"Lineup status: {lineup}")
    if lineup_impact and lineup_impact.lower()!='n/a': parts.append(f"Lineup change impact: {lineup_impact}")

    return '<p class="lede">'+' '.join(parts)+'</p>'

def build_tldr(file_name,text):
    card_count=len(re.findall(r'<article class="pick-card">',text))
    updated_m=re.search(r'Updated\s*([^<]+)</div>',text)
    updated=updated_m.group(1).strip() if updated_m else None
    heads=[clean(h) for h in re.findall(r'<h2>(.*?)</h2>',text,re.S)]

    bullets=[]
    if file_name=='2026-04-08.html':
        bullets.append(f"{card_count} game-side picks are posted for 2026-04-08.")
        m=re.search(r'<h2>(.*?)</h2>.*?<div><span>Odds</span><strong>([^<]+)</strong></div>.*?<div><span>Confidence</span><strong>([^<]+)</strong>',text,re.S)
        if m:
            bullets.append(f"Top listed matchup is {clean(m.group(1))} at {clean(m.group(2))} with {clean(m.group(3))}.")
        d=re.search(r'<span>Decided</span><strong>([^<]+)</strong>',text)
        r=re.search(r'<span>Record</span><strong>([^<]+)</strong>',text)
        if d and r: bullets.append(f"Tracker currently shows {clean(d.group(1))} decided picks and a {clean(r.group(1))} record.")
        bullets.append("Brewers–Red Sox had both starting lineups announced at publish time.")
    elif file_name=='2026-04-08-plus-money.html':
        bullets.append(f"{card_count} plus-money picks are posted for 2026-04-08.")
        odds=[int(x) for x in re.findall(r'<div><span>Odds</span><strong>\+?(\d+)</strong></div>',text)]
        if odds: bullets.append(f"Posted underdog prices range from +{min(odds)} to +{max(odds)}.")
        m=re.search(r'<h2>(.*?)</h2>.*?<div><span>Odds</span><strong>([^<]+)</strong></div>.*?<div><span>Confidence</span><strong>([^<]+)</strong>',text,re.S)
        if m: bullets.append(f"Highest-listed confidence slot starts with {clean(m.group(1))} at {clean(m.group(2))} ({clean(m.group(3))}).")
        bullets.append("Card record is still pending with no decided outcomes yet.")
    elif file_name=='2026-04-08-run-line.html':
        bullets.append(f"{card_count} run-line leans are posted for 2026-04-08.")
        confs=[float(x) for x in re.findall(r'<div><span>Confidence</span><strong>([0-9.]+)',text)]
        if confs: bullets.append(f"Highest listed run-line confidence on the page is {max(confs):.3f}.")
        if heads: bullets.append(f"The board opens with {heads[0].replace(' — Run Line Lean','')}.")
        bullets.append("All listed run-line outcomes are still marked PENDING.")
    elif file_name=='2026-04-08-run-totals.html':
        bullets.append(f"{card_count} run-total leans are posted for 2026-04-08.")
        over=sum('— OVER ' in h for h in heads)
        under=sum('— UNDER ' in h for h in heads)
        bullets.append(f"Current split is {over} OVER leans and {under} UNDER leans.")
        confs=[float(x) for x in re.findall(r'<div><span>Confidence</span><strong>([0-9.]+)</strong></div>',text)]
        if confs: bullets.append(f"Top listed totals confidence is {max(confs):.3f}.")
        bullets.append("Totals movement notes currently show unchanged numbers for each listed game.")
    if updated: bullets.append(f"Page header update stamp: {updated}.")

    bullets=bullets[:5]
    tldr='\n    <section class="pick-card tldr-card">\n      <h2>TL;DR</h2>\n      <ul>\n'
    for b in bullets:
        tldr+=f'        <li>{b}</li>\n'
    tldr+='      </ul>\n    </section>\n\n'
    return tldr

for fn in files:
    p=root/fn
    text=p.read_text()

    # rewrite each article lede independently
    articles=re.findall(r'<article class="pick-card">.*?</article>',text,re.S)
    new_articles=[]
    for i,art in enumerate(articles):
        new_lede=build_lede(fn,art,i)
        if re.search(r'<p class="lede">.*?</p>',art,re.S):
            art=re.sub(r'<p class="lede">.*?</p>',new_lede,art,count=1,flags=re.S)
        else:
            art=art.replace('</div>\n', '</div>\n        '+new_lede+'\n',1)
        new_articles.append(art)

    # rebuild with rewritten articles in order
    def repl(_):
        return new_articles.pop(0)
    text_new=re.sub(r'<article class="pick-card">.*?</article>',repl,text,flags=re.S)

    # refresh TLDR section
    text_new=re.sub(r'\n\s*<section class="pick-card tldr-card">.*?</section>\n','\n',text_new,flags=re.S)
    tldr=build_tldr(fn,text_new)
    text_new=text_new.replace('  <article class="pick-card">',tldr+'  <article class="pick-card">',1)

    p.write_text(text_new)

print('updated', ', '.join(files))
