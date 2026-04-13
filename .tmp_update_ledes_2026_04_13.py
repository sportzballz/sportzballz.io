from pathlib import Path
import re

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

repl = {
    '2026-04-13.html': [
        "Camden Yards still plays long in left-center (about 333 to left and 410 to the alley), but tonight’s 79° air and breeze to right make opposite-field carry real for Arizona’s left-handed contact. With both lineups posted and no late star absences, this reads like a full-strength game where Arizona’s cleaner defensive innings and steadier middle relief are worth the underdog tag.",
        "Truist is balanced on paper (roughly 335-400-325), yet clear 81° weather usually rewards hard contact to the gaps by the middle innings. Atlanta gets the nod because the order is intact, the bullpen enters fresher, and Miami’s available bats still look top-heavy if Pérez doesn’t give length. At this price, the favorite still has a practical path to separation late.",
        "At PNC (about 325 down the line with deep power alleys), this is less about one swing and more about who strings clean innings together. Warm air and 16 mph out to left will test command, but Pittsburgh’s staff profile is better built for traffic management, and Washington’s recent availability churn leaves less margin once the game reaches third-time-through decisions.",
        "Target Field suppresses cheap homers in cooler nights, and with wind in from center the long ball is less automatic despite 69° conditions. Boston still grades ahead because Crochet’s swing-and-miss floor pairs with a healthier run-prevention shape behind him, while Minnesota’s lineup continuity has been less stable. The edge is narrow, but it lands on the side with fewer late-inning failure points.",
        "Seattle at home remains a run-prevention wager: T-Mobile’s dimensions (around 331-401-326) and controlled roof conditions reduce random carry and reward command. With both cards announced and no fresh marquee scratches, the deciding factor is bullpen execution. Seattle’s relief shape is cleaner right now, and that matters more than raw brand power in this park.",
        "Dodger Stadium (about 330-395-330) can turn lively when wind nudges toward right, and tonight’s cooler 59° air keeps that effect selective rather than constant. Los Angeles still owns the stronger route because the Mets enter with more lineup turnover and fewer reliable bridge innings. In a game likely decided in the sixth through eighth, the Dodgers’ depth is the sharper knife.",
        "Sutter Health Park plays fair early and jumpy later, so run prevention has to survive changing conditions, not just first-pitch expectations. Texas gets the lean because the lineup arrives stable and the veteran starter profile is less likely to gift free baserunners. Sacramento’s roomy center (around 403) also rewards gap defense, another quiet point in Texas’ favor.",
        "Citizens Bank is compact to both corners (roughly 329 and 330), and with warm air plus wind to right the pressure on contact pitchers rises immediately. Philadelphia’s lineup continuity and late-inning run creation fit that environment better than Chicago’s current availability mix. This isn’t about a blowout script; it’s about which side is likelier to win the two biggest innings.",
        "Busch can look spacious at first glance (near 336-400-335), but 83° weather and wind to left change the arithmetic for doubles and deep flies. St. Louis is the plus-money side because the matchup is closer than market framing suggests, and the Cardinals’ healthier core bats give them enough punch if this turns into a trading-runs game by the middle frames.",
        "Yankee Stadium’s short right (about 314) always tempts the obvious angle, but tonight’s wind to left shifts value toward complete offensive sequences instead of one-spot power. The Angels are live at +157 because their current lineup mix is less top-heavy than New York’s recent availability profile, and their starter can keep the game in the range where underdog leverage matters."
    ],
    '2026-04-13-plus-money.html': [
        "At Camden Yards, the long left-center gap usually protects pitchers, but warm air and a gentle push to right flatten that edge tonight. Arizona’s lineup is intact, the defensive shape is clean, and Baltimore’s current availability picture still leans volatile in the lower third. For a plus-price ticket, this is the better blend of talent and game-state resilience.",
        "Busch is roomy enough to punish empty fly balls, yet tonight’s heat and wind to left support extra-base traffic when contact is squared. St. Louis is worth the plus number because the lineups are both posted near full strength, and the Cardinals’ healthier core plus home bullpen usage pattern gives them a credible late-game path, not just an upset narrative.",
        "The short porches in the Bronx can hide roster fragility for a night, but they can also magnify it if innings get extended. With 75° weather and wind helping to left, run swings should come in clusters. That favors an underdog with live bats and usable depth, so the Angels remain the right plus-money stab despite the market badge on the other side."
    ],
    '2026-04-13-run-line.html': [
        "Run-line angle: Arizona’s profile fits a multi-run win if contact quality shows early. Camden’s dimensions and rightward breeze support gap damage, and with both lineups confirmed, bullpen depth becomes the tiebreaker. Arizona carries the steadier bridge arms for protecting and extending a lead.",
        "Run-line case for Atlanta hinges on inning control, not fireworks. Truist’s neutral layout and warm, clear conditions put pressure on strike-throwing depth, and Atlanta’s available relief corps is better positioned to convert a one-run edge into a two-run finish.",
        "Pittsburgh run line is viable because PNC rewards teams that defend the alleys and avoid extra pitches. Wind out to left can accelerate mistakes, but the Pirates’ current staff mix is more likely to limit free traffic and create separation by the late innings.",
        "Boston run-line support is thinner but real: Target’s inward breeze trims cheap carry, so cleaner sequencing matters more than brute power. The Red Sox have the more dependable strikeout path and enough lineup continuity to pressure Minnesota’s middle relief.",
        "Seattle run line remains a precision play in a roof-managed park. T-Mobile reduces weather noise, and the Mariners’ defensive range plus bullpen command profile offers the better chance to turn a close game into a two-run result.",
        "Dodgers run line tracks because this matchup points to late leverage. In cool air with only selective carry, depth beats volatility, and Los Angeles has more trustworthy outs from the sixth inning forward.",
        "Texas on the run line is a park-context call as much as a talent call. Sutter Health’s deep center and roomy gaps reward clubs that run clean routes and limit extra bases; Texas currently checks those boxes better.",
        "Phillies run line is built on environment and lineup shape. Citizens Bank plus warm wind out to right can amplify one crooked inning, and Philadelphia’s available middle-order power gives them the better chance to create that inning.",
        "Cardinals run line is the aggressive interpretation of a close moneyline game. Busch usually suppresses chaos, but tonight’s heat and outflow wind increase run volatility, and St. Louis has enough healthy thump to win by margin if momentum flips early.",
        "Angels run line is contrarian but coherent in this weather. Yankee Stadium with wind to left can produce fast swings, and the underdog side has enough active bats to turn a tied game into a multi-run gap once bullpens rotate."
    ],
    '2026-04-13-run-totals.html': [
        "OVER 9.0 fits Philadelphia because Citizens Bank’s short corners and 80° air with wind out to right support carry on ordinary contact. With both lineups posted and no major late offensive scratches, this total should be attacked before bullpens can fully settle.",
        "At PNC, OVER 8.67 is justified by weather more than brand names: warm conditions and 16 mph out to left can turn warning-track balls into damage. Once starters hit traffic, the run environment can accelerate quickly.",
        "Busch typically asks hitters to earn every run, but 83° weather and wind to left shrink that margin tonight. OVER 8.42 is playable because both offenses bring enough available bats to capitalize on one messy inning.",
        "Yankee Stadium plus 75° air and wind to left supports OVER 8.5 even without a pure slugfest projection. The park’s dimensions reward line-drive pull power, and both teams can stack baserunners in bunches.",
        "Camden’s expanded left-center keeps totals honest, yet OVER 8.5 still works with warm weather and a breeze helping balls to right. The game shape points to sustained pressure rather than isolated solo shots.",
        "OVER 8.5 in Atlanta survives the wind-in note because temperature and lineup quality still support run creation over nine innings. Truist plays neutral enough that repeated hard contact eventually shows on the board.",
        "Dodger Stadium can run quieter at 59°, but wind out to right and two deep lineups keep OVER 7.5 in range. This number is modest enough that a standard late-game bullpen exchange can push it across.",
        "OVER 8.5 in Sacramento is a context play: Sutter Health’s outfield geometry encourages extra-base traffic when command slips. With both offenses carrying active middle-order bats, a midgame scoring burst is plausible.",
        "Target Field with wind in from center argues caution, but OVER 8.0 remains viable because both starters face lineups that can manufacture runs without relying on pure carry. This total can clear through sequencing and bullpen exposure.",
        "For Mariners-Astros, OVER 7.55 is low enough to clear even in a pitcher-friendly, roof-managed setting. T-Mobile limits chaos, but two disciplined offenses plus multiple bullpen turns create enough paths to eight runs."
    ]
}

for fn, leads in repl.items():
    p = base / fn
    txt = p.read_text()
    matches = list(re.finditer(r'<p class="lede">.*?</p>', txt, flags=re.S))
    n = min(len(matches), len(leads))
    out = []
    last = 0
    for m, new in zip(matches[:n], leads[:n]):
        out.append(txt[last:m.start()])
        out.append(f'<p class="lede">{new}</p>')
        last = m.end()
    out.append(txt[last:])
    p.write_text(''.join(out))
    print(f'updated {fn} replaced {n} of {len(matches)} existing ledes')
