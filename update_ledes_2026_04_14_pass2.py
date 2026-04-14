import re, html
from pathlib import Path

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

updates = {
    '2026-04-14.html': [
        "By twilight on the river, PNC tends to reward the club that can hit the ball where the park is widest, not loudest. With 325 to left, 399 to center, warm air at 78°, and wind nudging balls toward left, Pittsburgh’s full-strength core around Bryan Reynolds has more ways to score than Washington’s all-or-nothing pockets, and Mitch Keller’s sinker shape is well matched to that script.",
        "This feels like an Atlanta game: hot, dry air, a park built for hard contact in the alleys, and a lineup card that still includes Austin Riley in a prime damage slot. Reynaldo López can grab the first six outs quickly, and once the game reaches middle relief, the Braves’ depth of quality plate appearances should outlast Miami’s thinner scoring routes.",
        "Comerica is a long-yard test (420 to center, deep gaps), and tonight’s wind in from left only adds friction for quick-strike power. That favors Detroit’s cleaner prevention profile with Framber Valdez active and enough healthy regulars behind him, while Kansas City likely needs more perfectly timed extra-base hits than this park usually gives.",
        "Arizona as the dog has real shape: Camden’s deep left-center still turns marginal fly balls into outs, and Merrill Kelly’s strike management can keep the game in that lane. With Corbin Carroll and Gabriel Moreno both available, the Diamondbacks can pressure with pace, baserunning, and contact quality instead of waiting for one three-run swing.",
        "Tonight Busch plays warmer and smaller than its reputation, especially with wind carrying to left, but that doesn’t automatically mean chaos; it means execution. St. Louis brings a stable lineup, Iván Herrera remains in the run-production spine, and Michael McGreevy’s attack approach gives the Cardinals the better chance to own innings five through seven.",
        "The Rays are the side because this weather takes away cheap loft and asks hitters to square the baseball repeatedly. At Rate Field (330-400-335) with wind driving in from left, Shane McClanahan’s miss-barrel profile matters more, and Tampa Bay’s healthier contact chain should create the steadier run flow.",
        "Petco at night is a discipline park: big alleys, marine air, and wind leaning in from right. That setup flatters Bryan Woo’s command rhythm, and even with Fernando Tatis Jr. available, San Diego still carries more volatility through the lower third than Seattle in what projects as a low-traffic game.",
        "In the Bronx, geometry is destiny. With 314 to right and warm air pushing to center, one elevated miss can turn into a two-run scene in a heartbeat. With Aaron Judge and Cody Bellinger both active, New York has the heavier punishment profile, and that makes the Yankees the rightful favorite.",
        "Dodger Stadium after dark usually belongs to the club that owns strike one and keeps traffic orderly. Yoshinobu Yamamoto is better built for that job tonight, and with the Dodgers’ core largely intact, Los Angeles has the more reliable route through nine against a Mets staff still patching key innings together.",
        "Milwaukee is the practical lean in a roof-controlled game where weather can’t rescue mistakes and every ninety feet must be earned. Jacob Misiorowski gives the Brewers a true strikeout escape valve, and with Toronto carrying several health-question bats into first pitch, home execution is more bankable than brand-name variance.",
        "Minnesota at plus money is a craftsman’s pick, not a fireworks ticket. Target Field’s big middle suppresses random damage, Byron Buxton’s availability upgrades both range and pressure, and the Twins can win this by stringing disciplined at-bats while forcing Boston to manufacture against a set defense.",
        "Great American is the kind of place where a routine fly can become tomorrow’s headline when it’s 85° and the wind is running out to left. In that noise, San Francisco still profiles sturdier because Robbie Ray can miss bats when traffic builds, and the Giants carry more dependable late-inning run prevention pieces.",
        "Ignore the noisy number and watch the shape: Sacramento’s Sutter Health setup can play lively at dusk, and games swing toward the cleaner defensive club when that happens. With Corey Seager and Evan Carter both available and MacKenzie Gore equipped to lead counts, Texas owns the safer middle-innings runway.",
        "Philadelphia gets the edge in a Citizens Bank weather pattern that favors lifted pull contact toward right. With Bryce Harper and Alec Bohm active, plus Aaron Nola lined up for volume, the Phillies have the better blend of early scoring probability and late stability against a Cubs group that still rides streaks more than structure."
    ],
    '2026-04-14-plus-money.html': [
        "If you want a true plus-money case, this is it: Arizona can win without a parade of home runs. Camden’s deep left-center geometry still punishes lazy carry, Merrill Kelly keeps innings tidy, and with Carroll and Moreno available, the Diamondbacks can build pressure pitch by pitch until one inning breaks open.",
        "St. Louis is a live dog in tonight’s Busch weather because warm air and wind to left reward well-struck contact, not guesswork. The Cardinals’ regulars are mostly in place, their lineup continuity is better than usual, and that gives them a credible edge once Cleveland has to expose middle relief matchups.",
        "Minnesota offers the right kind of underdog value: low-noise park dimensions, active top-end athleticism with Buxton, and a game likely decided by first-to-third execution instead of homer variance. At this number, the Twins only need a clean sequencing edge to cash."
    ],
    '2026-04-14-run-totals.html': [
        "Over 9.5 is the right side of chaos at PNC tonight: warm air, breeze to left, and gap-heavy dimensions that turn solid contact into doubles trains. With both lineups carrying healthy middle-order threats, run creation should arrive in clusters, not drips.",
        "Over 8.5 at Busch is a weather upgrade from the baseline park expectation. At 87° with 14 mph carrying to left and both offenses mostly intact, balls that die on normal nights should find warning track and beyond, pushing this game toward a higher scoring band.",
        "Over 8.75 fits Great American’s personality perfectly. The park is already homer-friendly, and with 85° heat plus wind out to left, command misses become expensive; both clubs have enough active speed and gap contact to keep innings alive between homers.",
        "Over 9.0 in the Bronx is a structural play: short right field, warm carry, and two staffs that can unravel when first-pitch strike rate dips. With star bats active on both sides, one bullpen wobble can turn this from 4-3 to 6-4 fast.",
        "Over 8.83 in Atlanta is justified by environment and roster shape. Truist carries to left on warm nights, and both lineups still feature healthy right-handed run producers who can punish middle-inning mistakes.",
        "Over 8.75 in Baltimore is supported by heat, outbound wind, and offenses that can score in more than one style. Even with Camden’s deeper left-center, tonight’s carry plus available top-order talent points to sustained traffic.",
        "Over 8.25 in Philadelphia is the classic Citizens Bank cocktail: warm night, helping breeze to right, and power bats available to exploit the short dimensions. Nine runs is not a stretch in this setup; it is the median path if either bullpen blinks.",
        "Under 7.0 at Petco remains the cleaner read because this air mass and wind-in profile suppress full carry, especially to right-center. With two quality starters and fewer free-weather runs, offense has to be built one base at a time.",
        "Over 8.0 in Los Angeles works because both offenses can create run pressure without waiting for a single long ball. Healthy core bats on both sides plus a modest total leaves room for an over even in a game that starts quietly.",
        "Over 7.88 in Minneapolis is a number play with weather support: enough breeze to right, enough healthy top-half hitters, and enough bullpen exposure risk to produce one crooked inning that changes the board.",
        "Under 7.88 in Detroit matches the park map and the wind map: huge center field, deep alleys, and air moving in from left. With starters capable of limiting loud contact, this profiles closer to scattered scoring than sustained rallies.",
        "Under 8.33 on the South Side has real footing because wind in from left and evening humidity shave carry off marginal fly balls. In that environment, teams need multi-hit construction to score, and that usually keeps totals in check.",
        "Over 9.5 in Sacramento is a volatility over: Sutter Health can produce awkward outfield reads in twilight, and both active lineups run well enough to turn singles into immediate pressure. One command lapse with traffic can add three runs in a blink.",
        "Under 7.0 in Milwaukee is a control-room game under a roof: no wind gifts, consistent mound conditions, and two quality starters built to repeat mechanics. When weather is removed from the equation, low totals become easier to defend."
    ],
}

for fn, ledes in updates.items():
    p = base / fn
    txt = p.read_text()
    pattern = re.compile(r'<p class="lede">.*?</p>', re.S)
    matches = list(pattern.finditer(txt))
    if len(matches) != len(ledes):
        raise RuntimeError(f'{fn}: expected {len(ledes)} ledes, found {len(matches)}')

    out = []
    last = 0
    for m, new in zip(matches, ledes):
        out.append(txt[last:m.start()])
        out.append('<p class="lede">' + html.escape(new, quote=False) + '</p>')
        last = m.end()
    out.append(txt[last:])
    p.write_text(''.join(out))
    print('updated', fn)
