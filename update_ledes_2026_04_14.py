import re
from pathlib import Path

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

main_ledes = [
"On a warm river night at PNC, where the 21-foot wall in right can turn routine flies into anxiety, Pittsburgh gets the cleaner path. Keller’s sinker profile fits a park that rewards ground-ball command, and the Nationals arrive with a lineup that has shuffled lately while Pittsburgh’s main run producers remain available. With 79° air and a 13 mph breeze helping the ball toward left, the Pirates still grade as the steadier side because their run prevention travels better inning to inning.",
"This one has Bronx geometry written all over it: the short right-field porch can punish even decent misses, and 81° with wind drifting to left keeps both foul poles in play. New York’s lineup has churned, but the top-end thunder is still active, and the Angels’ pitching side has been asked to cover too many high-stress outs recently. The Yankees are the side because their damage paths are broader in this ballpark, not because of one narrow edge.",
"At Truist, the gaps are fair but not forgiving, and tonight’s heat keeps contact lively even with a light breeze nudging in from right. Atlanta’s core remains intact enough to pressure Max Meyer early, while Miami still leans on thinner margin innings once the starter exits. The Braves deserve the nod because their lineup continuity and late-game run prevention are better aligned for this park shape.",
"Comerica usually asks hitters to earn extra bases, but 73° with wind out to left shrinks that burden for pull power and fastballs left up. Detroit gets the lean because its lineup card is closer to full rhythm, while Kansas City’s recent shuffles create more swing-and-miss pockets against left-handed sequencing. In a park with huge alleys, the club that controls contact quality deeper into the game is the Tigers.",
"Camden’s deeper left-field wall still matters, but the warm, dry air and breeze toward center tonight soften some of that deterrent. Arizona profiles as a live dog because its contact-first table setters can force Trevor Rogers into long counts, and Baltimore’s run prevention has had to patch around recurring availability concerns. The Diamondbacks are playable at plus money because their path to six-plus competitive innings is believable in this environment.",
"Busch can look spacious until the wind starts carrying to left, and at 87° that carry arrives early. St. Louis has enough healthy middle-order bats to turn Joey Cantillo’s mistakes into crooked numbers, while Cleveland’s offense has been more start-stop by the week. As a slight plus side, the Cardinals make sense because their bullpen bridge is better positioned for a high-contact night.",
"Rate Field with wind blowing in from right usually trims cheap homers, which suits Tampa Bay’s style of stringing pressure instead of waiting for one blast. McClanahan gives the Rays a cleaner first-turn pitching expectation, and Chicago’s lineup uncertainty before first pitch adds volatility they can’t really afford. Tampa is the call because their run-creation routes are more repeatable even if the weather suppresses carry.",
"Petco’s marine-layer tendencies plus wind in from right point toward a low-variance scoring environment, and that often favors the club with the steadier starter-command profile. Seattle gets that tag tonight with Woo’s strike-throwing foundation, while San Diego entered publish time without a fully settled lineup card. The Mariners are preferred because in this park, extra baserunners usually matter more than occasional loud contact.",
"Dodger Stadium at night can still yield carry to right when the breeze cooperates, but this handicap is more about structure than spectacle. Yamamoto gives Los Angeles the stronger probability of quiet early frames, and the Mets’ run prevention has leaned heavily on high-leverage outs lately. The Dodgers remain the side because their floor is higher across all nine innings, even if the listed price is noisy.",
"Under a roof in Milwaukee, weather disappears and execution is exposed. The Brewers get the edge because their lineup depth can force Gausman into full-pitch-mix usage by the fourth, while Toronto’s offense has leaned on fewer stable run producers game to game. In a neutralized environment, the team with the cleaner bullpen handoff plan is Milwaukee.",
"Target Field can suppress sloppy fly-ball offense, but tonight’s mild out-blowing breeze to right gives both clubs a little extra distance. Minnesota is the value side because its healthy top-end speed and contact mix can pressure Boston’s defense over nine innings, while the Red Sox pitching plan looks more vulnerable after the starter. At plus money, the Twins offer the better full-game path rather than the better headline name.",
"Great American rewards conviction swings, yet wind in from left can punish teams that rely too heavily on lift-only contact. San Francisco’s profile is more balanced here: enough pull power, but also enough gap doubles to survive weather drag, and Robbie Ray’s form supports cleaner early traffic control. The Giants are the better side because they can win multiple game scripts in this park.",
"At Sutter Health Park, the ball can jump in neutral temps when hitters square it, so sequencing and bullpen timing become everything. Texas gets the preference because its core bats are available and its run prevention shape has been less erratic than the Athletics in middle innings. Even with quirky pricing, the Rangers are the side that better matches the park’s volatility.",
"Citizens Bank is built for momentum: short corners, loud crowd, and 85° air with wind toward center can flip a game in two batters. Philadelphia’s healthy heart-of-order plus Nola’s workload reliability give them the stronger baseline, while Chicago still carries more uncertainty after the first pitching turn. The Phillies are preferred because their pathway to both early and late scoring is more complete in this setting.",
]

plus_money_ledes = [
"Baltimore’s outfield redesign still suppresses some left-field damage, but this matchup leans to Arizona because the Diamondbacks can score in layers—first-to-third pressure, line drives, then occasional lift. In hot, dry Camden air with wind to center, Merrill Kelly’s ability to limit free passes keeps the underdog script alive deep into the game. Plus money is justified when the dog can create offense without needing three-run homers.",
"At Busch tonight, the weather gives carry and the Cardinals have enough active middle-order pieces to capitalize if Cantillo misses arm side. St. Louis also enters with a more coherent bullpen ladder for innings six through eight, which matters in a near coin-flip price range. Taking the plus side is defensible because the home club owns the cleaner late-inning map.",
"Minnesota at plus money is a roster-shape wager as much as a pitching wager: the Twins can pressure with speed and contact while keeping their core bats in the lineup. Target Field’s deep alleys still reward gap hitting, and the light wind to right nudges borderline flies into play. If this game gets to tied-or-one-run territory late, the underdog path remains very real.",
]

totals_ledes = [
"Yankee Stadium plus 81-degree air is rarely subtle: one pulled mistake can erase two clean innings. With wind drifting out and both lineups carrying active power bats, the over 9.0 has room even if the starters are decent. The park’s short right-field geometry is the quiet extra push.",
"In St. Louis, 87-degree warmth and a firm breeze to left improve carry enough to turn warning-track contact into scoring swings. Both clubs can string quality at-bats after the first trip through the order, so over 8.5 is a fair lean. This total is more about sustained traffic than one bullpen implosion.",
"PNC usually plays fair, but 79 with wind out to left raises the home-run ceiling for right-handed pull contact. Both staffs also have innings where command can leak, which is all an over 9.5 needs in this weather. Expect scoring windows in the middle frames.",
"Citizens Bank remains one of the quicker places for rallies to become crooked numbers, and tonight’s warm breeze to center helps that profile. Over 8.25 fits because both offenses bring healthy middle-order bats and both bullpens can be taxed by long innings. The ballpark does not forgive mistakes up in the zone.",
"Camden’s dimensions are less extreme than a few years ago, but 87-plus heat and wind to center still favor hard contact. Over 8.75 works when both lineups can pressure from the top and neither side is built to coast once pitch counts rise. This projects as a game with repeat scoring chances, not one big inning.",
"Even with a slight breeze in from right, Atlanta’s warm conditions keep exit velocity relevant over nine innings. Over 8.83 is playable because the Braves can drive totals by themselves and Miami has enough contact bats to contribute. Late bullpen matchups are unlikely to fully choke off scoring.",
"Comerica’s deep alleys usually suppress slug, yet wind out to left creates a narrower path to the over than the park reputation suggests. Over 7.88 is reasonable with two lineups that can produce doubles traffic and force pitchers into stretch mode. You don’t need a shootout to clear this number.",
"Petco plus marine air and wind in from right normally point under, and that aligns with the 7.67 lean. Seattle and San Diego both profile for stretches of clean pitching when ahead in counts, and extra-base carry should be limited. Unless defense unravels, this game sets up as a grind.",
"Dodger Stadium night games can still run over when both teams bring patient top halves and enough right-center power. Over 8.0 is viable with a modest breeze out to right and two offenses capable of forcing deep counts early. This number leaves little room for even an average scoring tempo.",
"Target Field isn’t tiny, but a light push to right and two disciplined offenses make over 7.88 attractive. Both clubs can score without relying solely on homers, which matters in April conditions. A couple of multi-run innings likely gets this home.",
"Rate Field with 14 mph in from right lowers pure carry, which supports the under 8.33 stance. Tampa and Chicago can still create chances, but this weather rewards strike-throwers and outfield depth more than loft. The total asks for sustained offense that conditions are likely to mute.",
"Great American is always one bad pitch away from noise, but wind in from left offsets some of its usual homer volatility. The over 8.75 still has merit because both teams can manufacture traffic and this park turns singles into pressure quickly. Think steady accumulation rather than derby ball.",
"Sutter Health Park can play lively when contact is squared, and both lineups bring enough active bats to threaten quick three-run pockets. Over 9.5 is aggressive but defensible with neutral weather and uncertain middle-relief stability on both sides. This is a sequencing total as much as a power total.",
"With the roof environment in Milwaukee, run context comes down to pitcher execution and lineup depth. Under 7.0 fits because both starters can work efficiently early and neither offense projects as fully explosive tonight. In a controlled setting, seven is low but still reachable to the under with clean defense.",
]


def replace_ledes(path: Path, new_ledes: list[str]):
    txt = path.read_text()
    matches = list(re.finditer(r'<p class="lede">.*?</p>', txt, flags=re.S))
    if len(matches) != len(new_ledes):
        raise SystemExit(f'{path.name}: expected {len(new_ledes)} ledes but found {len(matches)}')
    out, last = [], 0
    for m, new in zip(matches, new_ledes):
        out.append(txt[last:m.start()])
        out.append(f'<p class="lede">{new}</p>')
        last = m.end()
    out.append(txt[last:])
    path.write_text(''.join(out))
    print(f'updated {path.name}')

# 2026-04-14.html currently has 15 ledes, including one extra Houston game at slot 2.
# Preserve that one unchanged and replace the rest by position.
main_path = base / '2026-04-14.html'
main_txt = main_path.read_text()
main_matches = list(re.finditer(r'<p class="lede">.*?</p>', main_txt, flags=re.S))
if len(main_matches) != 15:
    raise SystemExit(f'2026-04-14.html: expected 15 ledes but found {len(main_matches)}')

# Slot map by current file order (1-indexed):
# 1 PIT, 2 HOU(keep), 3 NYY, 4 ATL, 5 DET, 6 ARI, 7 STL, 8 SEA, 9 TB,
# 10 LAD, 11 MIL, 12 MIN, 13 TEX, 14 PHI, 15 SF
slot_to_main_index = {
    1: 0,
    3: 1,
    4: 2,
    5: 3,
    6: 4,
    7: 5,
    9: 6,
    8: 7,
    10: 8,
    11: 9,
    12: 10,
    15: 11,
    13: 12,
    14: 13,
}

updated_main = []
for idx, m in enumerate(main_matches, start=1):
    if idx in slot_to_main_index:
        updated_main.append(main_ledes[slot_to_main_index[idx]])
    else:
        updated_main.append(m.group(0)[len('<p class="lede">'):-len('</p>')])

replace_ledes(main_path, updated_main)
replace_ledes(base / '2026-04-14-plus-money.html', plus_money_ledes)
replace_ledes(base / '2026-04-14-run-totals.html', totals_ledes)
