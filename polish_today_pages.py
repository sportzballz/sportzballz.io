import re
import random
import html
from pathlib import Path

TODAY = "2026-04-08"
FILES = [
    f"{TODAY}.html",
    f"{TODAY}-plus-money.html",
    f"{TODAY}-run-line.html",
    f"{TODAY}-run-totals.html",
]

PANEL = [
    {"id":"mack-ledger","name":"Mack Ledger","title":"Market Maker"},
    {"id":"nora-splitter","name":"Nora Splitter","title":"Matchup Film Room"},
    {"id":"dex-numbers","name":"Dex Numbers","title":"Quant"},
    {"id":"rico-heatcheck","name":"Rico Heatcheck","title":"Momentum & Vibes"},
    {"id":"grant-halberd","name":"Grant Halberd","title":"Beat Writer"},
    {"id":"ivy-chen","name":"Ivy Chen","title":"Data Scientist"},
    {"id":"toby-quinn","name":"Toby Quinn","title":"Contrarian"},
    {"id":"lena-park","name":"Lena Park","title":"Weather/Umpire Specialist"},
    {"id":"vince-valentino","name":"Vince Valentino","title":"Showman"},
    {"id":"maya-rios","name":"Maya Rios","title":"Process Coach"},
    {"id":"owen-pike","name":"Owen Pike","title":"Model Whisperer"},
    {"id":"jules-archer","name":"Jules Archer","title":"Underdog Hunter"},
    {"id":"roman-slate","name":"Roman Slate","title":"Line Movement Hawk"},
    {"id":"keira-bloom","name":"Keira Bloom","title":"Injury/Lineup Impact"},
    {"id":"eli-mercer","name":"Eli Mercer","title":"Totals Architect"},
    {"id":"sanjay-vale","name":"Sanjay Vale","title":"CLV Auditor"},
]

OPENERS = {
    "mack-ledger": "Price first: this entry is only worth a ticket if the board still respects the edge at the current number.",
    "nora-splitter": "From a matchup room view, the script favors cleaner leverage innings and fewer bailout moments.",
    "dex-numbers": "The probability shape supports this side as a positive-expectation decision, not a narrative swing.",
    "rico-heatcheck": "There is legitimate energy behind this play, but confidence works best when it stays disciplined.",
    "grant-halberd": "The headline case is straightforward and supported by the measurable pregame profile.",
    "ivy-chen": "Validation checks hold, and the signal agreement is strong enough to keep this as a qualified entry.",
    "toby-quinn": "This is a classic pricing pocket where public sentiment can drift faster than true game probability.",
    "lena-park": "Context is central here, because venue conditions and crew uncertainty can reshape the edge quickly.",
    "vince-valentino": "Big-stage number, but the show only matters if the process still says this ticket is justified.",
    "maya-rios": "Process check first: stake quality has to follow edge quality, not emotion.",
    "owen-pike": "Plain-language model read: the edge clears the go line under current assumptions.",
    "jules-archer": "Selective aggression is the right approach, especially when the board offers asymmetric upside.",
    "roman-slate": "Market behavior is the gatekeeper; the team read only matters if the number still carries value.",
    "keira-bloom": "Availability context is a real factor, and this edge should be treated as lineup-sensitive.",
    "eli-mercer": "Run environment framing supports the call, with scoring shape and suppression risk both accounted for.",
    "sanjay-vale": "CLV discipline says this is actionable now, provided the closing process stays intact.",
}

CLOSERS = {
    "mack-ledger": "Keep it pending until final checks clear; if price quality deteriorates, pass without hesitation.",
    "nora-splitter": "Hold pending status through final cards, then confirm once the game script is fully visible.",
    "dex-numbers": "Treat this as pending until lock so late inputs do not invalidate the expected value case.",
    "rico-heatcheck": "It stays pending for now, and it is still a no-play if late information weakens the setup.",
    "grant-halberd": "For now, pending remains appropriate while final lineup and board checks complete.",
    "ivy-chen": "Pending status remains in place until late validation confirms the edge is still intact.",
    "toby-quinn": "Leave it pending and be ready to pass if the market corrects the mispricing window.",
    "lena-park": "Keep it pending until final context checks lock weather, crew notes, and pricing behavior.",
    "vince-valentino": "Pending for now: either late confirmation gives a green light, or this becomes a clean pass.",
    "maya-rios": "Keep it pending, protect bankroll rules, and only fire if the close still matches plan.",
    "owen-pike": "Pending status is correct until final confirmations keep the edge above threshold.",
    "jules-archer": "Pending for now; take the shot only if the closing number still rewards selectivity.",
    "roman-slate": "Maintain pending status and recheck near close, because edge and price are inseparable.",
    "keira-bloom": "Keep pending status until confirmed availability removes late uncertainty.",
    "eli-mercer": "Leave it pending until final context confirms the projected scoring environment.",
    "sanjay-vale": "Pending stands until close, and execution is valid only if entry still projects CLV.",
}

FORBIDDEN = [
    "avg","groundOuts","runs","doubles","homeRuns","rbi","whip","strikeoutWalkRatio",
    "strikeoutsPer9Inn","walksPer9Inn","hitsPer9Inn","runsScoredPer9","homeRunsPer9","era","strikePercentage"
]

random.seed()
usage = {p["name"]: 0 for p in PANEL}


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def parse_meta(article: str) -> dict:
    meta = {}
    for m in re.finditer(r"<div><span>([^<]+)</span><strong>(.*?)</strong></div>", article, flags=re.S):
        meta[strip_tags(m.group(1))] = html.unescape(strip_tags(m.group(2)))
    return meta


def sentence(src: str, pattern: str) -> str:
    m = re.search(pattern, src, flags=re.I)
    return m.group(1).strip() if m else ""


def add_tldr(content: str, bullets: list[str]) -> str:
    content = re.sub(r"\n\s*<section class=\"pick-card tldr\">.*?</section>\n", "\n", content, flags=re.S)
    first_article = re.search(r"\n\s*<article class=\"pick-card\">", content)
    if not first_article:
        return content
    tldr = [
        "\n    <section class=\"pick-card tldr\">",
        "      <div class=\"pick-head\">",
        "        <div class=\"pick-num\">TL;DR</div>",
        "        <h2>Quick Read</h2>",
        "      </div>",
        "      <ul>",
    ]
    for b in bullets:
        tldr.append(f"        <li>{b}</li>")
    tldr.extend(["      </ul>", "    </section>", ""])
    idx = first_article.start()
    return content[:idx] + "\n".join(tldr) + content[idx:]


def choose(prev_id):
    choices = [p for p in PANEL if p["id"] != prev_id]
    pick = random.choice(choices)
    usage[pick["name"]] += 1
    return pick


for f in FILES:
    path = Path(f)
    data = path.read_text()
    last = 0
    prev = None
    out = []

    for m in re.finditer(r"<p class=\"lede\">.*?</p>", data, flags=re.S):
        out.append(data[last:m.start()])
        old_lede_html = m.group(0)
        old_lede = html.unescape(strip_tags(old_lede_html))

        astart = data.rfind('<article class="pick-card">', 0, m.start())
        aend = data.find('</article>', m.end())
        article = data[astart:aend] if astart != -1 and aend != -1 else data[max(0, m.start()-1200):m.end()+200]

        h2 = html.unescape(strip_tags(re.search(r"<h2>(.*?)</h2>", article, flags=re.S).group(1)))
        pick_name = h2.replace(" — Run Line Lean", "")

        meta = parse_meta(article)
        price = meta.get("Odds") or meta.get("Price") or "listed price"
        conf_line = meta.get("Confidence", "")
        conf = sentence(conf_line, r"([0-9]+\.[0-9]+)")
        dp_match = sentence(conf_line, r"\(([^\)]+/[^\)]+)\)")
        dp_txt = f" with data points {dp_match}" if dp_match else ""

        movement = sentence(old_lede, r"((?:Moneyline|Total) unchanged[^.]*\.)")
        if not movement:
            movement = sentence(article, r"<li><strong>Total Movement:</strong>\s*([^<]+)</li>")
            if movement and not movement.endswith('.'):
                movement += '.'

        weather = sentence(article, r"<li><strong>Weather:</strong>\s*([^<]+)</li>")
        umpire = sentence(old_lede, r"(Umpire crew unavailable at run time\.)")
        lineup = sentence(old_lede, r"(Starting lineups were not announced[^.]*\.)")
        if not lineup and "Both starting lineups were announced" in old_lede:
            lineup = "Both starting lineups were announced at publish time."

        persona = choose(prev)
        prev = persona["id"]

        opener = OPENERS[persona["id"]]
        core = f"For {pick_name}, the board shows {price}"
        if conf:
            core += f", with model confidence at {conf}{dp_txt}"
        core += "."

        strength = (
            "The support profile points to steadier command, cleaner run prevention windows, and better conversion paths "
            "without pretending variance is gone."
        )
        if "OVER" in h2 or "UNDER" in h2:
            strength = (
                "The projection points to a credible scoring trajectory at the posted total, balancing pace, bullpen stress, "
                "and quality contact expectations."
            )

        context_bits = []
        if weather:
            context_bits.append(f"weather: {weather}")
        if umpire:
            context_bits.append(f"crew note: {umpire}")
        if movement:
            context_bits.append(f"market: {movement}")
        if lineup:
            context_bits.append(f"lineups: {lineup}")
        context = "External context check — " + "; ".join(context_bits) + "." if context_bits else "External context remains neutral at publish time."

        lede = f"{persona['name']} ({persona['title']}) — {opener} {core} {strength} {context} {CLOSERS[persona['id']]}"
        lede = re.sub(r"\s+", " ", lede).strip()

        if len(lede.split()) < 95:
            lede += " Position size should stay proportional to edge quality, with a willingness to pass if late information materially changes expected value."
        words = lede.split()
        if len(words) > 160:
            lede = " ".join(words[:160]).rstrip(".,;:") + "."

        for tok in FORBIDDEN:
            lede = re.sub(rf"\b{re.escape(tok)}\b", "signal", lede, flags=re.I)

        out.append(f'<p class="lede">{html.escape(lede, quote=False)}</p>')
        last = m.end()

    out.append(data[last:])
    new_content = "".join(out)

    if f.endswith("-run-totals.html"):
        bullets = [
            "15 totals leans are posted for 2026-04-08, including 14 OVER calls and 1 UNDER call.",
            "Displayed confidence values on this card run from 0.175 to 0.447.",
            "Most totals movement notes show numbers holding steady at publish update time.",
            "Several games still list missing weather or crew details from the MLB feed."
        ]
    elif f.endswith("-plus-money.html"):
        bullets = [
            "Three plus-money sides are on today’s card: Brewers +113, Angels +115, and White Sox +136.",
            "Shown confidence values for those entries are 0.419, 0.253, and 0.034.",
            "All three spots were published with lineup announcements still pending.",
            "These are selective underdog entries, not a volume spray approach."
        ]
    elif f.endswith("-run-line.html"):
        bullets = [
            "15 run-line leans are published for 2026-04-08.",
            "Top confidence entries on this page are Phillies (0.663) and Dodgers (0.545).",
            "Most listed moneyline movement notes show unchanged pricing at publish update.",
            "Many matchups still require late lineup confirmation before lock."
        ]
    else:
        bullets = [
            "15 moneyline picks are published for 2026-04-08 with confidence values from 0.034 to 0.663.",
            "Highest-confidence listed sides are Phillies -133 and Dodgers -166.",
            "Most market notes indicate unchanged moneyline pricing at publish update.",
            "Lineup status is still pending in most matchups on this card."
        ]

    new_content = add_tldr(new_content, bullets)
    path.write_text(new_content)

print("Analyst usage")
for name, count in sorted(usage.items(), key=lambda kv: (-kv[1], kv[0])):
    if count:
        print(f"{name}: {count}")
