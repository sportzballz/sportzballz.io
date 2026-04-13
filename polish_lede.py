import re, pathlib
base=pathlib.Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
files=['2026-04-07.html','2026-04-07-plus-money.html','2026-04-07-run-line.html','2026-04-07-run-totals.html']

subs=[
    (r"\bIn today's matchup\b", "Today"),
    (r"\bIn the matchup between\b", "In"),
    (r"\bIn the matchup at\b", "At"),
    (r"\bIn the upcoming clash between\b", "In"),
    (r"\bOverall,\s*", ""),
    (r"\bMeanwhile,\s*", ""),
    (r"\bConversely,\s*", ""),
    (r"\bAdditionally,\s*", ""),
    (r"\bOn the flip side,\s*", ""),
    (r"\bpresent a compelling case\b", "are a live underdog case"),
    (r"\bpresent a solid betting opportunity\b", "are the right side"),
    (r"\bbetting on\b", "backing"),
    (r"\bmaking it essential to monitor conditions as game time approaches\b", "still worth tracking into first pitch"),
    (r"\bexpect fireworks\b", "expect runs"),
    (r"\bhinting at\b", "pointing to"),
    (r"\bshowing a tick of confidence\b", "showing a small confidence bump"),
    (r"\bindicating increased confidence in their chances\b", "showing increased market confidence"),
    (r"\bindicating market movement away from\b", "showing market movement away from"),
    (r"\bpoised to\b", "set to"),
    (r"\bset to battle\b", "set to face"),
    (r"\bflaunt(?:ing)?\b", "show"),
    (r"\bboast(?:ing)?\b", "show"),
    (r"\bwith the prediction model favoring\b", "with the model favoring"),
    (r"\bthe data clearly leans toward\b", "the data leans toward"),
    (r"\bThe model indicates a confidence level of\b", "Model confidence is"),
    (r"\breflecting a market shift from\b", "after moving from"),
    (r"\breflecting some market support for\b", "showing some market support for"),
    (r"\bWeather conditions\b", "Weather"),
    (r"\bWith the game played in a dome, weather is a non-factor\b", "In the dome, weather is a non-factor"),
    (r"\bthe team to bet on for today's game\b", "the side today"),
]

prefixes=[
    "Bottom line:","Here's the card:","My read:","Short version:","No mystery here:"
]

def polish(text,idx):
    t=' '.join(text.split())
    for a,b in subs:
        t=re.sub(a,b,t,flags=re.IGNORECASE)
    t=t.replace('savvy choice','smart play').replace('compelling underdog pick','live underdog pick')
    t=t.replace('ready to roll','available').replace('locked and loaded','ready')
    if not re.match(r'^(Bottom line:|Here\'s the card:|My read:|Short version:|No mystery here:)',t):
        t=f"{prefixes[idx%len(prefixes)]} {t[0].lower()+t[1:] if t and t[0].isupper() else t}"
    return t

pat=re.compile(r'<p class="lede">(.*?)</p>',re.S)
for f in files:
    p=base/f
    s=p.read_text()
    def repl(m):
        new=polish(m.group(1),repl.counter)
        repl.counter +=1
        return f'<p class="lede">{new}</p>'
    repl.counter=0
    ns=pat.sub(repl,s)
    p.write_text(ns)
    print(f, 'ledes', repl.counter)
