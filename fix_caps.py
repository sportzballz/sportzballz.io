import re, pathlib
base=pathlib.Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
files=['2026-04-07.html','2026-04-07-plus-money.html','2026-04-07-run-line.html','2026-04-07-run-totals.html']
pat=re.compile(r'<p class="lede">(.*?)</p>',re.S)

def cap_sentences(t:str)->str:
    # capitalize first alphabetic character
    chars=list(t)
    for i,c in enumerate(chars):
        if c.isalpha():
            chars[i]=c.upper(); break
    t=''.join(chars)
    # capitalize sentence starts after .!? and space
    t=re.sub(r'([\.!?]\s+)([a-z])', lambda m: m.group(1)+m.group(2).upper(), t)
    return t

for f in files:
    p=base/f
    s=p.read_text()
    def repl(m):
        return f'<p class="lede">{cap_sentences(m.group(1))}</p>'
    p.write_text(pat.sub(repl,s))
    print(f)
