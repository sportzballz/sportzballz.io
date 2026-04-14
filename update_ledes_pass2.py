from pathlib import Path
import re, html

base = Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

side_map = {
"Arizona Diamondbacks over Baltimore Orioles":"Camden Yards is a storyteller’s park now—333 to left, 410 to center, 318 to right—and on an 80° night with breeze to right, long at-bats tend to end in loud doubles instead of harmless flies. Both clubs carry active injury sheets, but Arizona’s card looks cleaner in the leverage innings, especially once the game turns from starters to middle relief. That is why the underdog has real footing here: fewer fragile outs between the sixth and eighth.",
"Atlanta Braves over Miami Marlins":"Truist plays fair at 335-400-325, so this comes down to roster integrity and inning control more than logo strength. In clear 78° weather, with both teams still managing regular injury-report traffic, Atlanta’s deeper late-game options make the favorite price feel earned rather than inflated. If this is close through five, the Braves have the sturdier path to the final six outs.",
"Pittsburgh Pirates over Washington Nationals":"At PNC (325 to left, 410 to center, 320 to right), the deep alleys punish sloppy route-running, and tonight’s 79° air with 14 mph out to left raises the tax on every command miss. Injury news on both sides points to active roster management, but Pittsburgh is better built to absorb that churn without leaking runs late. The lean is simple: better run prevention in the part of the game that usually decides it.",
"Boston Red Sox over Minnesota Twins":"Target Field’s 339-411-328 frame and a cool overcast breeze out to left make this less of a home-run contest and more of a sequencing contest. Both teams have names on the availability board, yet Boston’s current pitching ladder looks less brittle when traffic starts in the middle innings. In a one-run game environment, that stability is worth backing.",
"Seattle Mariners over Houston Astros":"Under a roof at T-Mobile, weather gets removed and baseball gets honest: 331-401-326, clean sightlines, and no free atmospheric carry. With both injury reports still active, the separator is which bullpen asks fewer emergency outs; tonight that edge tilts Seattle. This is a craftsmanship pick, not a headline pick.",
"Texas Rangers over Athletics":"Sutter Health Park’s shape—roughly 330 to left, 403 to center, 325 to right—rewards clubs that defend the gaps and avoid free baserunners. In clear 65° conditions with a light crosswind, both teams’ injury updates matter mostly in depth roles, and Texas owns the cleaner starter-to-bullpen chain. Over nine innings, that usually wins this exact kind of game.",
"Philadelphia Phillies over Chicago Cubs":"Citizens Bank Park is compact where it matters (329 and 330 down the lines), and tonight’s 78° air with 16 mph out to right can turn ordinary contact into inning-spinning traffic. Both lineups have availability notes, but Philadelphia’s healthy middle-order core gives them more ways to cash those extra baserunners. The home side’s edge is in sustained pressure, not one lucky swing.",
"St. Louis Cardinals over Cleveland Guardians":"Busch is roomy on paper at 336-400-335, yet 80° warmth and wind pushing to left make it play smaller by the fourth inning. Injury management is present for both clubs, and that raises the value of a team that can manufacture offense without a perfect lineup card. At plus money, St. Louis has a believable late path, not just an upset prayer.",
"Los Angeles Dodgers over New York Mets":"Dodger Stadium in 59° night air usually suppresses loft, but an 11 mph push to right keeps doubles-and-damage alive if hitters stay patient. Both sides carry injury-report noise, and Los Angeles is simply deeper at the spots that matter after the starter exits. In a close game, the Dodgers own more reliable outs and more credible ninth-inning offense.",
"New York Yankees over Los Angeles Angels":"Yankee Stadium’s porch math (318 to left, 399 to center, 314 to right) plus wind toward center creates volatility that helps underdogs hang around and strike late. With each team still listing active injury news, lineup balance and bullpen discipline matter more than star power. At this number, the Angels are a live dog with an actual script to win.",
}

plus_map = {
"Arizona Diamondbacks over Baltimore Orioles":"This is the kind of Camden dog you can defend: deep left-center, warm air, and a right-field breeze that rewards Arizona’s line-drive shape. Both injury reports are active, but the Diamondbacks look less vulnerable in the middle-relief bridge where plus-money tickets usually die. If the game is tied late, this price is too generous.",
"St. Louis Cardinals over Cleveland Guardians":"A Busch underdog usually needs weather help, and tonight it gets it: 80° with wind to left in a park built 336-400-335. Both teams are navigating player availability, and St. Louis has enough healthy run creators to convert one crooked inning when Cleveland goes to secondary arms. That makes this plus number practical, not romantic.",
"New York Yankees over Los Angeles Angels":"In the Bronx, underdogs cash when games stay messy, and the setup points that way—short porches, 77° air, and wind pushing toward center. Each side carries injury-list movement, but the Angels still bring enough active offense to punish bullpen mistakes in bunches. For plus money, the path is there.",
}

runline_map = {
"Arizona Diamondbacks vs Baltimore Orioles — Run Line Lean":"Run-line read: Camden’s 333-410-318 layout and out-to-right breeze create extra-base pressure, which is how one-run leads become two-run leads. With both teams managing injury availability, Arizona has the cleaner relief staircase to protect and extend. That makes the margin outcome plausible, not forced.",
"Atlanta Braves vs Miami Marlins — Run Line Lean":"Atlanta by margin is an innings-control play. Truist’s neutral dimensions in clear weather reward clubs that keep pitch counts down, and the Braves’ healthier late-game options give them the better chance to add insurance in the seventh or eighth.",
"Pittsburgh Pirates vs Washington Nationals — Run Line Lean":"PNC run lines are won in the alleys, and 14 mph out to left means every defensive step matters tonight. Both injury reports are busy, but Pittsburgh’s current run-prevention structure is less likely to crack in a high-traffic middle third. The two-run band is very live.",
"Boston Red Sox vs Minnesota Twins — Run Line Lean":"Target Field with a cool breeze is usually a sequencing game, not a launch game. Boston’s strikeout floor and steadier bullpen usage against an injury-managed opponent create a realistic path from a narrow lead to a cover late.",
"Seattle Mariners vs Houston Astros — Run Line Lean":"At T-Mobile, margins come from execution because the roof strips out weather luck. Seattle’s defensive spine and bullpen command profile are better positioned to turn a tie game into a two-run finish once matchups begin.",
"Texas Rangers vs Athletics — Run Line Lean":"Sutter Health’s deep center and broad gaps punish misplays, which favors the side with cleaner outfield routes and fewer free passes. Texas currently checks both boxes, even with normal injury-report churn on each roster. That is enough for a legitimate run-line case.",
"Philadelphia Phillies vs Chicago Cubs — Run Line Lean":"Phillies run line fits the park-weather combo: short corners at Citizens Bank and strong wind to right can produce one avalanche inning. With both clubs carrying active availability notes, Philadelphia still holds the deeper healthy power pocket to create separation.",
"St. Louis Cardinals vs Cleveland Guardians — Run Line Lean":"This is the aggressive read in a close matchup, but the environment supports it. Busch plays bigger most nights; tonight, heat and wind to left increase swing volatility, and the Cardinals have enough active bats to turn first momentum into a multi-run finish.",
"Los Angeles Dodgers vs New York Mets — Run Line Lean":"Dodgers by two is a depth argument in cool conditions. When the ball does not fly easily, teams need repeated quality plate appearances and dependable relief turns; Los Angeles has more of both while both sides juggle injury availability.",
"New York Yankees vs Los Angeles Angels — Run Line Lean":"Contrarian run-line, but coherent: Yankee Stadium can flip fast in windy conditions, especially once bullpens churn. The Angels’ active lineup still has enough length to turn a one-run edge into a two-run result in the late innings.",
}

total_map = {
"Philadelphia Phillies vs Chicago Cubs — OVER 9.0":"OVER 9.0 is justified by environment first: Citizens Bank’s 329-401-330 shape, 78° warmth, and hard wind to right all raise carry and RBI traffic. Both teams still carry active injury-report management, which tends to thin late defensive substitutions. Nine is reachable on ordinary game flow.",
"Pittsburgh Pirates vs Washington Nationals — OVER 8.67":"PNC usually suppresses cheap homers, but 79° with 14 mph out to left changes the risk profile on every elevated pitch. With both clubs navigating player availability, middle-inning run prevention looks less secure than the number suggests. The over has multiple clean paths.",
"St. Louis Cardinals vs Cleveland Guardians — OVER 8.43":"Busch totals rise when wind goes left and temperatures stay warm, and that is exactly tonight’s setup at 80° and 15 mph outflow. Each lineup has injury-list noise, so bullpen and bench defense can fray late. That supports an over built on accumulation, not fireworks.",
"New York Yankees vs Los Angeles Angels — OVER 8.5":"Yankee Stadium totals do not need perfect weather, but tonight they get help: short porches and a lively 77° night with wind toward center. Both clubs are still managing injuries, and extended innings against secondary relievers are the over’s best friend. This number is playable.",
"Boston Red Sox vs Minnesota Twins — OVER 8.0":"Target Field can look quiet, yet 8.0 is a modest bar when both offenses can manufacture through doubles and walks. Even with cooler air, wind out to left keeps extra-base opportunities on the table, and active injury reports on both sides can stress late run prevention.",
"Arizona Diamondbacks vs Baltimore Orioles — OVER 8.5":"Camden’s deep alley keeps things honest, but warm air plus breeze to right still supports sustained scoring chains. Add two teams carrying active availability concerns, and the later innings become less predictable on the run-prevention side. OVER 8.5 is a volume play, not a one-inning gamble.",
"Atlanta Braves vs Miami Marlins — OVER 8.42":"At Truist, 78° clear conditions and balanced dimensions make this a pressure-over: hard contact over time rather than instant slugfest. Both clubs come in with injury-report management in play, which can expose bullpen depth by the sixth. This total can clear through steady traffic.",
"Los Angeles Dodgers vs New York Mets — OVER 7.5":"The number is low enough to like even in cooler Dodger air. Wind to right offsets part of the 59° dampening effect, and both teams still carry injury-news wrinkles that can thin relief quality later. Eight runs is a realistic median outcome.",
"Texas Rangers vs Athletics — OVER 8.5":"Sutter Health can turn ordinary contact into doubles traffic because of the 403-foot center lane and generous gaps. With both rosters actively managing availability, late-inning command depth is a question for each side. That keeps OVER 8.5 in play well past the starters.",
"Seattle Mariners vs Houston Astros — OVER 7.55":"Roof game, low total, disciplined offenses—that combination still leans over at 7.55. Even without wind effects, repeated bullpen transitions and active injury management on both rosters create enough small scoring windows to get to eight.",
}


def replace_by_h2(path: Path, mapping: dict[str, str]):
    text = path.read_text()

    def repl(m):
        block = m.group(0)
        h2m = re.search(r'<h2>(.*?)</h2>', block, re.S)
        if not h2m:
            return block
        h2 = html.unescape(re.sub('<.*?>', '', h2m.group(1))).strip()
        if h2 not in mapping:
            raise KeyError(f'{path.name}: missing mapping for {h2}')
        return re.sub(
            r'<p class="lede">.*?</p>',
            f'<p class="lede">{mapping[h2]}</p>',
            block,
            count=1,
            flags=re.S,
        )

    new_text = re.sub(r'<article class="pick-card">.*?</article>', repl, text, flags=re.S)
    path.write_text(new_text)


replace_by_h2(base / '2026-04-13.html', side_map)
replace_by_h2(base / '2026-04-13-plus-money.html', plus_map)
replace_by_h2(base / '2026-04-13-run-line.html', runline_map)
replace_by_h2(base / '2026-04-13-run-totals.html', total_map)
print('pass2 complete')
