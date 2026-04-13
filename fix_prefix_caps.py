import re, pathlib
base=pathlib.Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
files=['2026-04-07.html','2026-04-07-plus-money.html','2026-04-07-run-line.html','2026-04-07-run-totals.html']
for f in files:
    p=base/f
    s=p.read_text()
    s=re.sub(r'(Bottom line:|Here\'s the card:|My read:|Short version:|No mystery here:)\s+([a-z])',lambda m:m.group(1)+' '+m.group(2).upper(),s)
    s=s.replace('Jr. Are available','Jr. are available')
    p.write_text(s)
    print(f)
