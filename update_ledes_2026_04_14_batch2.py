import re
from pathlib import Path

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')
re_lede = re.compile(r'<p class="lede">.*?</p>', re.S)


def replace_ledes(path: Path, new_ledes: list[str]):
    text = path.read_text()
    matches = list(re_lede.finditer(text))
    if len(matches) != len(new_ledes):
        raise SystemExit(f'{path.name}: expected {len(matches)} ledes, got {len(new_ledes)} replacements')
    out = []
    last = 0
    for m, new in zip(matches, new_ledes):
        out.append(text[last:m.start()])
        out.append(f'<p class="lede">{new}</p>')
        last = m.end()
    out.append(text[last:])
    path.write_text(''.join(out))
    print(f'updated {path.name} ({len(new_ledes)} ledes)')


daily = [
"Pittsburgh is the cleaner side in the first long breath of spring at PNC: a 325-foot notch to left, a deep 410 to center, and a left-field wind around 13 mph that can turn hard contact into crooked numbers. Keller’s profile fits that big middle alley better than Mikolas on this card, and with both lineups posted and no major absences flagged among everyday pieces, the favorite has fewer ways to beat itself late.",
"Houston gets the nod because this game is insulated from weather and chaos; with the roof closed at Daikin Park, the run environment is stable and easier to handicap. The park still plays quirky—short down the lines, deep to center—so contact quality matters more than gusts, and the Astros are better built for that shape tonight even with Colorado bringing most regular bats.",
"At Yankee Stadium, where right field is 314 and left is reachable at 318, the 10 mph push toward left keeps this from being a quiet night. Even so, the Yankees remain the sturdier moneyline side: their run production floor at home is higher, and with both lineups announced and core stars active on both cards, this projects as a game where New York’s depth separates in the middle innings.",
"Atlanta in this spot reads like a veteran handicap: trust the stronger roster in familiar weather and let the game come to you. Truist’s 400-foot center keeps cheap homers in check, and with warm air but breeze in from right, this looks more like sustained pressure than random slug. Both clubs list regular contributors as active, and the Braves’ continuity gives them the cleaner path over nine innings.",
"Comerica can look spacious at 420 to center, but with 13 mph out toward left, balls carry better than the dimensions suggest. In a near-pick’em profile, Detroit earns preference because their contact mix is less feast-or-famine here, and the posted lineups plus largely active injury reports reduce surprise risk before first pitch.",
"Arizona as plus money is the kind of ticket built on context, not noise. Camden now asks for real lift to clear left-center after the wall changes, but 87-degree heat and breeze out to center re-open scoring lanes for disciplined hitters. With both lineups in and no obvious star scratches, the underdog has a real, repeatable road to control early innings and steal leverage late.",
"St. Louis at home as a slight dog is playable because Busch still rewards complete baseball more than one-dimensional power. Yes, the air is hot and the wind is moving out left, but that park’s 400 to center and roomy alleys punish sloppy sequencing. If the Cardinals keep traffic moving and avoid free outs, this number gives enough room for a tight one-run finish.",
"Seattle over San Diego is a contrarian favorite in a pitcher-friendly yard that still supports it: Petco’s deep gaps and marine air at mid-60s, with wind in from right, trim cheap offense. With San Diego’s lineup not posted at publish while Seattle’s is set, the preparation edge leans Mariners, especially in a game likely decided by bullpen command windows.",
"Tampa Bay is the side despite a modest projection edge because the environment in Chicago suppresses volatility tonight. Wind in from right at Rate Field cuts the easy pull-side damage, and that helps the club more likely to string at-bats than wait for one swing. Both lineups are posted and major names are active, so the handicap comes down to cleaner inning-to-inning execution.",
"The Dodgers are still the practical side, but this number has to be treated with discipline after the listing volatility. Dodger Stadium plays fair at 330 down each line and 400 to center, and tonight’s light breeze out right nudges fly balls without turning it into a launch contest. With both lineups announced and front-line talent active, Los Angeles carries the steadier run-prevention profile into late innings.",
"Milwaukee is a controlled-environment play: with roof conditions at American Family Field, you get repeatable flight and fewer weather surprises. The park’s deep alleys can mute one-and-done offense, and the Brewers’ structure is better suited for that grind game, especially if both clubs finalize lineups close to first pitch with no major health shocks.",
"Minnesota as a home underdog is a pure value read shaped by park geometry and weather. Target’s 411 to center and broad right-center gaps reward line drives and baserunning pressure, and a gentle breeze out to right can help opposite-field carry. With both lineups posted and key contributors listed active, the Twins have enough paths to win that this plus price remains worth the risk.",
"Texas projects as the better side in Sacramento’s temporary setting, where dimensions play more like a lively neutral than a true suppressor. Mild air and breeze out to center can accelerate scoring swings, so roster balance matters; the Rangers’ top half gives a steadier on-base spine, and with both clubs posting expected regulars, they deserve the nod in a coin-flip environment.",
"Philadelphia at Citizens Bank is still a favorite worth backing when conditions tilt hitter-friendly: 329 and 330 down the lines, warm mid-80s, and wind out to center. That combination magnifies lineup quality and late pinch-hit options, and with both cards showing core bats active, the Phillies’ deeper pressure profile is the safer side.",
"San Francisco in Cincinnati is less about headline talent and more about surviving ballpark math. Great American is tiny down the lines and dangerous when contact elevates, but tonight’s wind in from left helps soften the cheap-homer risk. With both lineups posted yet each showing some turnover lately, the Giants’ steadier run-prevention shape makes them the preferable small favorite.",
]

plus = [
"If you want an underdog that can actually finish the job, Arizona is the one: Camden’s post-renovation left-center still demands real authority, but 87-degree heat and breeze to center increase carry for line-drive offenses. Merrill Kelly’s ability to stay ahead in counts gives the Diamondbacks a cleaner script than this price implies, and both lineups arriving intact removes most of the pregame uncertainty.",
"St. Louis at plus money fits the classic home-dog profile: enough power to punish mistakes, enough park depth at Busch to protect a lead if they pitch to plan. The hot air and wind out left raise scoring variance, but that helps a modest dog with multiple run-creation paths. With regulars available on both sides, this is a value bet on game state, not luck.",
"Minnesota at +119 is a measured swing, not a blind one. Target Field’s expansive center and right-center reward teams that can pressure with doubles and first-to-third aggression, and the mild breeze toward right gives extra carry without turning into chaos. With both lineups announced and no major injury absences popping up pregame, the Twins own enough matchup equity to justify the plus price.",
]

run_totals = [
"OVER 9.36 fits Yankee Stadium geometry and weather: short lines (318 left, 314 right), warm 81-degree air, and breeze out to left all support extra-base carry. With both lineups posted and star-level bats available, this total is justified by environment plus depth on both sides.",
"OVER 8.5 in St. Louis is grounded in conditions, not hype. Busch is normally fair-to-spacious, but 87-degree heat and 14 mph out to left increase flight on pulled contact, and both clubs arrive with regular bats active enough to cash mistakes.",
"OVER 9.55 at PNC asks for sustained offense, but the setup is there: warm upper-70s, wind out to left, and two staffs that can leak traffic if command slips. The deep 410 center limits freebies, yet the corners and weather still create enough scoring lanes.",
"OVER 8.25 in Philadelphia is a park-and-weather play first. Citizens Bank’s short porches, 85-degree warmth, and wind to center all enhance carry, and both projected lineups are intact enough to keep pressure on from the first inning through bullpen time.",
"OVER 8.75 at Camden is supported by heat and airflow: upper-80s with breeze to center can neutralize some of the post-wall dampening in left-center. With both teams bringing active core hitters, this number leaves room for a 5-4 type game without requiring an outlier explosion.",
"OVER 8.88 in Atlanta still works even with wind in from right because the temperature is high and both offenses can build runs without needing three homers. Truist’s 400-foot center keeps it honest, but lineup depth and warm air keep this above median scoring expectations.",
"OVER 7.88 in Detroit is a modest target for a big park. Comerica’s 420 center usually suppresses total runs, yet 13 mph out to left plus competent top-of-order bats on both sides can get this into the 8-9 run band with ordinary sequencing.",
"OVER 8.55 in Houston benefits from roof control: no weather volatility, just stable hitting conditions in a park with inviting lines and a deep center gap. With regular bats expected to be available, this total leans to cumulative pressure rather than one big inning.",
"UNDER 7.67 at Petco is the rare total where park and weather point the same way: marine air in the mid-60s, wind in from right, and deep power alleys. Even with healthy bats, this profile favors run prevention and pushes the game toward a 4-3 ceiling range.",
"OVER 8.0 in Los Angeles is reasonable because Dodger Stadium plays neutral-to-offense when air is mild and wind nudges toward right. With both lineups posted and front-end hitters active, this number can clear on balanced scoring without either starter imploding.",
"OVER 7.88 in Minnesota is a market-friendly threshold in a park with a large center but playable corners and a slight push to right. Both clubs’ regular hitters being available raises the floor enough that eight runs is a fair expectation.",
"OVER 8.75 in Cincinnati respects the park first: Great American’s short lines and homer-prone profile always keep overs live. Even with breeze in from left, warm air and complete lineups give enough extra-base potential to justify an over at this number.",
"OVER 9.5 in the Rangers-Athletics game is aggressive but defensible in a temporary venue that plays lively down the lines and fair to center. Mild wind out to center and mostly intact batting orders create multiple paths to double-digit scoring.",
"OVER 8.33 at Rate Field requires patience, but it’s playable with warm 79-degree conditions and both lineups largely healthy. Wind in from right trims one lane of power, yet enough opposite-field and gap contact remains to get this over by late innings.",
"UNDER 7.0 in Milwaukee is a thin number, but roof-controlled conditions plus deeper gaps at American Family Field can suppress the cheap run. With both starters in and no weather inflation, this profiles as a lower-event game where seven may be enough to stay under.",
]

replace_ledes(base / '2026-04-14.html', daily)
replace_ledes(base / '2026-04-14-plus-money.html', plus)
replace_ledes(base / '2026-04-14-run-totals.html', run_totals)
