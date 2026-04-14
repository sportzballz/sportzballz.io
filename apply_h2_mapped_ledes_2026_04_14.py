import re
from pathlib import Path

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

main_ledes = {
"Pittsburgh Pirates over Washington Nationals": "Pittsburgh is the side because this park turns into a carry lane when the breeze runs out to left, and tonight’s 79° air with a 13.7 mph push should reward hard contact to the pull gaps. At PNC (320 down the left line, 410 to dead center), Keller’s sinker profile plays to the deep alleys better than Mikolas if traffic builds. The Nationals’ group is healthy on paper, but Pittsburgh’s core has looked steadier inning to inning, and the home bullpen path is cleaner if this game gets to the seventh tied.",
"Atlanta Braves over Miami Marlins": "The Braves get the nod because this matchup is built for their right-handed thunder in warm, dry Atlanta air. Truist’s 335-400-325 geometry can look small when the ball jumps to left, and tonight’s 81.7° with wind drifting that way gives Atlanta’s middle order extra margin. Miami can stay in it if Meyer gets chases early, but the deeper relief options and late-inning run production still sit with the home side.",
"Detroit Tigers over Kansas City Royals": "This one reads as a narrow Detroit edge mostly because Comerica’s giant center field (420) punishes mis-hit fly-ball offenses and favors complete pitching sequences. With 81.8° conditions and wind out to left, there will be carry, but extra-base damage still requires precision in this yard. Valdez’s ground-ball mix is a better antidote to volatility than a pure strikeout hunt, and the Tigers usually string cleaner at-bats when the game settles into middle innings.",
"Arizona Diamondbacks over Baltimore Orioles": "Arizona as a plus-money side makes sense in Baltimore tonight, where 88° heat and breeze to center can turn line drives into trouble quickly. Camden’s reworked left field still asks hitters to earn it, but right-center remains playable for speed and gap pressure, and that suits this Diamondbacks group. Kelly’s pace and strike-throwing give Arizona a credible path to six workable innings before handing it to a rested enough bridge.",
"St. Louis Cardinals over Cleveland Guardians": "In St. Louis, the weather is the co-star: 89.5° with a hard 15 mph wind out to left in a park that is 336 down the line and 400 to center. That setup can flip one mistake into a crooked number, and the Cardinals are the lineup more likely to cash in those mistake pitches at home. With both clubs reasonably intact, the difference is shape: St. Louis projects fewer empty innings and a steadier ninth-inning route.",
"Tampa Bay Rays over Chicago White Sox": "Back Tampa Bay here because Rate Field’s 330-400-335 frame plus wind in from left creates a game that rewards command and sequencing over pure loft. McClanahan’s profile fits that script better, especially if early contact stays on the ground. Chicago has live young arms, but without confirmed lineups the safer read is the club that tends to manufacture one extra run before the bullpen handshake innings.",
"Seattle Mariners over San Diego Padres": "Seattle is the play in a Petco game that should feel heavy and controlled: 65° air, wind in from right, and deep right-center geometry that suppresses cheap damage. Woo’s ability to get ahead matters in this park, where 334 to left and nearly 400 in the gaps force hitters to square everything. If the Padres’ not-yet-final lineup leaves even one middle-order bat less than full strength, the Mariners’ prevention-first shape gains value late.",
"New York Yankees over Los Angeles Angels": "Yankee Stadium can turn loud quickly in this weather window—84.7° with wind toward center—and the short right-field porch (314) always hovers over late-game strategy. New York’s advantage is less about flash and more about pressure: they can score in bunches or one run at a time. With both lineups posted and core bats active, the better route still belongs to the home club if this becomes a bullpen chess match.",
"Los Angeles Dodgers over New York Mets": "At Dodger Stadium, cooler 62° air usually keeps this game from spiraling, but the Dodgers still own the cleaner run-creation blueprint over nine innings. The park is fair but not generous (330-395-330), so quality contact depth matters more than one superstar swing. Yamamoto’s strike efficiency in this setting is the separator, especially against a Mets group that may need a little more lineup protection to sustain rallies.",
"Milwaukee Brewers over Toronto Blue Jays": "In a roof-flex environment at American Family Field, the game leans toward whichever club controls tempo and free bases, and that tends to be Milwaukee at home. The dimensions (344 to left, 400 to center, 345 to right) don’t hand out many cheap homers unless misses are loud. Misiorowski versus Gausman is volatile on paper, but the Brewers’ blend of speed and contact quality gives them a steadier path through innings 6-9.",
"Minnesota Twins over Boston Red Sox": "This is a true underdog case, not a coin flip dressed up: Minnesota in cool evening air at Target Field with enough breeze to center to reward disciplined launch windows. The park’s deep center (411) and angled right-center cut down sloppy power swings, which favors clubs that can build innings with doubles and pressure. With both lineups confirmed and key names active, the Twins are better positioned to win the middle frames and hold the lane late.",
"San Francisco Giants over Cincinnati Reds": "Great American can become a pinball table when it’s warm, and tonight’s 80° with wind out to left puts that risk in play from first pitch. Even so, San Francisco has the better recipe for surviving this park’s short corners (328 left, 325 right): limit free passes, avoid middle-middle fastballs, and force Cincinnati to hit three singles instead of one blast. If Ray keeps the ball off barrel depth early, the Giants can take control by the sixth.",
"Texas Rangers over Athletics": "Sutter Health Park is still revealing its MLB personality, but the basic shape—tighter lines, bigger power alleys—rewards teams that can turn singles into pressure innings. In 64.8° air with a light breeze to center, this doesn’t project as a slugfest by default. Texas gets the edge because its lineup construction is deeper one through seven, and that matters when the first big chance comes with two outs.",
"Philadelphia Phillies over Chicago Cubs": "Philadelphia is the side because Citizens Bank in 86° warmth with wind toward right can punish any lapse in fastball location. Even with a deep center marker at 409, the 329/330 corners let hot lineups create instant leverage. Nola’s experience working this environment plus a healthier middle of the Phillies order gives the home club the more reliable run-prevention and run-cashing profile by late innings."
}

plus_ledes = {
"Arizona Diamondbacks over Baltimore Orioles": "Underdog ticket, but not a blind one: Arizona’s speed-and-gap game is well suited to a hot Camden night with the ball carrying to center. In this park, the renovated left-field wall grabs headlines, yet the real damage lane is still fast pressure into right-center. With the Diamondbacks’ key bats active and Kelly capable of stealing strike one consistently, this price is playable on structure, not hope.",
"St. Louis Cardinals over Cleveland Guardians": "Plus money on St. Louis is justified when Busch is this warm and the wind is howling toward left. Those conditions can erase margin for contact pitchers, and the Cardinals’ middle order is better built to capitalize quickly. Cleveland can absolutely grind, but the home side’s inning-to-inning leverage—especially if this reaches setup men with traffic—makes the underdog number worth taking.",
"Minnesota Twins over Boston Red Sox": "This is a practical home-dog angle: Target Field’s deep center and cool night profile usually reward cleaner sequencing over pure slug. Minnesota’s active core gives them enough on-base table-setting to create two-run innings without needing three homers. At this number, the case is simple—if the Twins are even through five, their path to an upset is very real."
}

run_ledes = {
"Pittsburgh Pirates vs Washington Nationals — OVER 9.5": "Over 9.5 is the call because this weather window is built for carry at PNC: 79° with a firm wind to left, exactly where mistakes can leave quickly in a park that opens to 410 in center but plays lively down the line. Both clubs can string at-bats when first-pitch strikes disappear, so one crooked inning per side is very live.",
"Atlanta Braves vs Miami Marlins — OVER 8.5": "Over 8.5 fits the setting at Truist, where warm 81.7° air and a left-field breeze can add distance to already hard contact. With 335/325 lines and a fast infield, this can become a doubles-and-bullpen stress game even before the late innings.",
"Detroit Tigers vs Kansas City Royals — UNDER 7.59": "Under 7.59 has logic because Comerica’s 420-foot center and broad alleys suppress easy homers even on warm nights. Yes, the wind is out to left, but this park still asks for sustained quality contact rather than one lucky swing, which supports a lower-scoring path.",
"St. Louis Cardinals vs Cleveland Guardians — OVER 8.5": "Over 8.5 is a weather-and-park blend play: Busch at nearly 90° with strong wind to left can turn routine fly balls into warning-track drama and warning-track outs into seats. Once either starter exits, this total can accelerate quickly.",
"Tampa Bay Rays vs Chicago White Sox — UNDER 7.5": "Under 7.5 works because wind in from left at Rate Field trims marginal carry and pushes this matchup toward sequencing baseball. In a 330-400-335 park, that often means long innings without the one swing that breaks it open.",
"Seattle Mariners vs San Diego Padres — UNDER 7.0": "Under 7.0 matches Petco’s profile tonight: cool marine air, wind in from right, and deep alleys that punish half-hit fly balls. This is the classic one-run-at-a-time environment where both starters can survive traffic.",
"New York Yankees vs Los Angeles Angels — OVER 8.59": "Over 8.59 is supported by conditions in the Bronx—warm air, breeze toward center, and a short right-field porch that changes bullpen matchups from the fifth inning on. Big innings are always one mislocated fastball away here.",
"Los Angeles Dodgers vs New York Mets — OVER 7.5": "Over 7.5 is modest but fair at Dodger Stadium when two deep lineups face off and even neutral weather can’t fully mute gap power. The park is balanced, yet late-inning relief volatility can push this past a low total.",
"Minnesota Twins vs Boston Red Sox — OVER 8.0": "Over 8.0 is playable because both lineups can manufacture runs in Target Field without needing perfect homer weather. Even in cooler air, doubles lanes to the gaps stay open and can snowball once bullpens rotate.",
"San Francisco Giants vs Cincinnati Reds — OVER 9.45": "Over 9.45 is a Great American special: short corners, warm air, and wind to left in a park that rarely forgives elevated contact. This total can look high until one fifth-inning rally turns into a three-batter avalanche.",
"Philadelphia Phillies vs Chicago Cubs — OVER 9.5": "Over 9.5 is justified at Citizens Bank with hot conditions and wind aiding right field. The 329/330 lines keep both dugouts one mistake from instant damage, and neither side needs many baserunners to cash this number.",
"Arizona Diamondbacks vs Baltimore Orioles — UNDER 8.82": "Under 8.82 is the sharper angle despite the heat because Camden’s modern shape can still turn hard contact into long outs, especially when offenses chase pull-side lift too early. If the starters steal first-pitch strikes, this game can stay under the explosive threshold.",
"Milwaukee Brewers vs Toronto Blue Jays — UNDER 7.0": "Under 7.0 makes sense in a roof-managed park where environment is stable and both starters can work without wind distortion. In American Family Field, run spikes usually require command collapse, not just weather luck.",
"Texas Rangers vs Athletics — UNDER 8.59": "Under 8.59 is a structural play at Sutter Health Park: moderate temperatures, deeper alleys, and a game script that leans toward singles clusters over constant extra-base damage. Unless defensive lapses pile up, nine-plus runs is a tough ask."
}

article_pat = re.compile(r'(<article class="pick-card">.*?</article>)', re.S)


def update_file(path: Path, lede_map: dict[str, str]):
    text = path.read_text()
    out = text
    replaced = 0
    for art in article_pat.findall(text):
        h2m = re.search(r'<h2>(.*?)</h2>', art, re.S)
        pm = re.search(r'<p class="lede">.*?</p>', art, re.S)
        if not h2m or not pm:
            continue
        key = re.sub(r'\s+', ' ', h2m.group(1)).strip()
        if key not in lede_map:
            raise KeyError(f'Missing lede for {key} in {path.name}')
        newp = f'<p class="lede">{lede_map[key]}</p>'
        newart = art[:pm.start()] + newp + art[pm.end():]
        out = out.replace(art, newart, 1)
        replaced += 1

    if replaced != len(lede_map):
        raise RuntimeError(f'{path.name}: replaced {replaced}, expected {len(lede_map)}')

    path.write_text(out)
    print(f'updated {path.name}')


update_file(base / '2026-04-14.html', main_ledes)
update_file(base / '2026-04-14-plus-money.html', plus_ledes)
update_file(base / '2026-04-14-run-totals.html', run_ledes)
print('updated')
