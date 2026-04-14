import re, html
from pathlib import Path

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

updates = {
    '2026-04-14.html': [
        "Pittsburgh is the side because this game is built for two-way pressure: contact to the big alleys at PNC (325 to left, 399 to center, 320 down the Clemente wall) and enough lift from a warm 78° breeze pushing toward left. Mitch Keller’s heavy fastball profile plays when the infield can shorten innings, and with Bryan Reynolds and the core bats available, the Pirates should turn extra baserunners into crooked numbers before Washington’s middle relief settles.",
        "Atlanta gets the nod in a park that rewards firm contact to the gaps (335-400-325) and in air dry enough to let tonight’s carry show up. With Austin Riley confirmed and Reynaldo López healthy, the Braves can pressure Max Meyer early, then hand clean innings to a fresher late bridge; Miami has speed but still profiles as too dependent on sequencing in this run environment.",
        "Detroit is the steadier play at Comerica, where the deep power alleys (370 and 365) and broad center field (420) punish one-dimensional lineups. The wind is blowing in from left at more than 12 mph, which trims Kansas City’s easiest long-ball path, and with Framber Valdez active and the Tigers’ regulars available, this sets up as a run-prevention game that leans home side.",
        "Arizona at plus money is live because Camden’s reworked left-center geometry still asks hitters to earn every lifted ball, even on an 88° night. Merrill Kelly’s strike-throwing pace fits that shape, Corbin Carroll and Gabriel Moreno are both available, and the Diamondbacks can manufacture offense in layers rather than waiting on one swing against Trevor Rogers.",
        "St. Louis is the better side in heat and wind that should make Busch play smaller than usual, especially to left. The Cardinals have continuity in tonight’s lineup card, Iván Herrera remains available in the heart of the order, and with Michael McGreevy attacking the zone, they’re positioned to win the middle innings where Cleveland has been forced to overextend matchup arms.",
        "Tampa Bay is still playable because this weather knocks down the cheap opposite-field carry at Rate Field (330-400-335), and that pairs with Shane McClanahan’s ability to miss barrels when hitters have to stay through the ball. If the White Sox cannot get free loft into the wind from left, the Rays’ more complete contact profile should decide this by the seventh.",
        "Seattle is the right look at Petco, where the marine layer, big alleys (390 and 391), and wind drifting in from right all tilt toward strike-throwers. Bryan Woo can live on the edges without paying for one miss, and even with Fernando Tatis Jr. active, San Diego’s lineup depth is thinner if this becomes a low-traffic game after the first turn.",
        "The Yankees deserve favorite status in Bronx weather that can turn routine fly balls into loud contact, especially with 314 feet to right and warm air carrying to center. Aaron Judge and Cody Bellinger both being available matters in this setup, and if Ryan Weathers leaves balls up to that side of the yard, New York can separate quickly.",
        "Los Angeles is the call because Dodger Stadium at night still rewards premium command more than chaos, and Yoshinobu Yamamoto has the cleaner path to strike one and soft contact. With the Dodgers’ core healthy enough to stack pressure and the Mets asking a young arm to navigate that lineup in a 330-375-400 bowl, the game script favors the home club over nine innings.",
        "Milwaukee is the lean in a roof-controlled spot where game state matters more than wind and where their athletic lineup tends to steal one extra ninety feet per inning. Jacob Misiorowski’s power mix gives the Brewers the strikeout escape hatch, and with Toronto carrying several day-to-day bats on the report, this is a spot where home execution can outlast name-brand pitching.",
        "Minnesota as a dog makes sense in Target Field conditions that are playable but not explosive, with just a light push toward right and plenty of room in center. Byron Buxton being active gives the Twins both range and first-to-third pressure, and if Mick Abel keeps Boston from living on pull-side doubles, the value sits with the home side late.",
        "San Francisco is the pick in a Cincinnati weather pocket that screams offense but still rewards the team that can control traffic first. Great American’s short porches (328 and 325) plus 14.6 mph wind to left can flip innings fast, yet Robbie Ray’s strikeout shape and the Giants’ deeper run-prevention options make them better built for the inevitable high-leverage spots.",
        "Texas gets the nod despite odd pricing noise because this Sacramento park can play jumpy at dusk, and the side with cleaner infield defense usually survives it. Corey Seager and Evan Carter both being available keeps the Rangers’ run creation diversified, and MacKenzie Gore’s ability to front-run counts gives them the safer path through the first six.",
        "Philadelphia is the side in Citizens Bank conditions that favor authoritative pull contact, with warmth and wind helping balls toward the right-field seats (330 line). With Bryce Harper and Alec Bohm active and Aaron Nola lined up to absorb innings, the Phillies carry the more reliable blend of early scoring and late-out stability against a Cubs group that still leans streaky away from home."
    ],
    '2026-04-14-plus-money.html': [
        "Arizona is the plus-money look because this matchup is less about one big swing and more about stringing pressure in a hot Camden night. The Diamondbacks have their top table-setters available, Merrill Kelly can keep the game on schedule, and the Orioles’ remodeled deep left-center still asks hitters to hit it flush instead of simply high.",
        "St. Louis fits the dog profile: warm, windy Busch weather that boosts gap contact, a lineup with most regulars intact, and a starter willing to throw strike one. If Cleveland doesn’t win the count early, the Cardinals’ extra-base lanes to left-center and their steadier defensive conversion become the separator.",
        "Minnesota at this number is worthwhile in a game likely decided by execution, not fireworks. Target Field’s big middle (411 to center) keeps random homers in check, Byron Buxton’s availability raises both run prevention and basepath pressure, and Boston’s edge narrows if Sonny Gray has to pitch from traffic instead of ahead."
    ],
    '2026-04-14-run-totals.html': [
        "Over 9.5 is justified because PNC’s asymmetric gaps create doubles traffic when the weather is warm and the ball is carrying to left. Both clubs have enough healthy middle-order bats to cash in with runners in motion, and neither starter profile suggests a parade of quick three-pitch outs once the order turns over.",
        "Over 8.5 works at Busch tonight: 87° heat, 14 mph out to left, and two lineups mostly intact. The park normally suppresses cheap damage, but these conditions plus available pull power on both rosters make sustained scoring innings more likely than a clean 3-2 style game.",
        "Over 8.75 lines up with Great American’s dimensions and the weather tax on fly-ball command. At 85° with wind to left, routine mistakes get punished fast, and both clubs have enough active speed-and-gap pieces to keep pressure on even when the home run isn’t there.",
        "Over 9.0 at Yankee Stadium is a geometry play as much as a form play: short right field, warm air, and two staffs that can run into trouble when first-pitch strikes disappear. With major bats active on both sides, this total can clear on sequencing and one bullpen wobble.",
        "Over 8.83 is reasonable in Atlanta because Truist carries well to left on warm nights and both teams have available right-handed thunder in the middle third. Even if the starters settle early, this environment often creates two big innings once the game hits secondary relievers.",
        "Over 8.75 in Baltimore gets support from heat, outward wind, and two offenses that can score without waiting for a three-run homer. Camden’s deep left-center still gives pitchers hope, but tonight’s conditions and healthy top-of-order pieces point to sustained run creation.",
        "Over 8.25 in Philadelphia is a classic weather-and-park combo: warm evening, breeze to right, and a venue that rewards lifted pull contact. With headline sluggers available and both pens likely asked for multiple leverage outs, nine-plus runs is the fair side of variance.",
        "Under 7.0 at Petco is the stronger read because the marine air and wind in from right make full-flight carry hard to sustain. Both teams have active star bats, but this yard plus two quality starters usually forces station-to-station offense, and that is difficult to stack into a big total.",
        "Over 8.0 at Dodger Stadium is playable because neither lineup has to rely exclusively on the long ball; both can score through hard singles and doubles in front of power. With healthy core bats available and a total that leaves little room for a 5-4 type finish, the over has more outs.",
        "Over 7.88 in Minneapolis leans on game flow: enough breeze to right to reward clean lift, plus two offenses with active top-half bats that create base traffic before the late innings. This number is low enough that one crooked frame from either side can tilt the whole ticket.",
        "Under 7.88 in Detroit fits Comerica’s large outfield and a notable wind pushing in from left. With two starters capable of controlling hard contact and plenty of warning-track real estate (420 to center), this projects as scattered scoring rather than sustained rallies.",
        "Under 8.33 on the South Side is supported by wind in from left and humidity that can deaden carry once the sun drops. Even with healthy hitters available, this setup asks for multi-hit rallies instead of solo-jump offense, and that favors the under over nine innings.",
        "Over 9.5 in Sacramento is a volatility play: Sutter Health’s outfield shape and evening carry can turn routine flies into extra bases, and both teams have active bats that run well once they reach. If command loosens even briefly in the middle innings, this climbs in a hurry.",
        "Under 7.0 in Milwaukee makes sense in a roof-controlled game where pitchers can repeat release points without wind interference. With two quality starters and fewer random weather boosts, run creation has to be earned pitch by pitch, which is exactly the environment that protects low totals."
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
