from pathlib import Path
import re

files = {
"/Users/asmith/.openclaw/workspace/sportzballz.io/2026-04-14.html": [
"Houston is the cleaner side in a closed-roof game where chaos is mostly self-inflicted. Daikin Park plays fair at 315-362-409-373-326, and with no wind to rescue mishit fly balls, the better strike-throwing club usually cashes the late innings. Colorado still carries uncertainty around Ezequiel Tovar and Brenton Doyle availability, and that matters against a Houston staff built to shorten games once it gets six competent frames.",
"Take St. Louis as the plus-money club because this weather asks pitchers to survive, not just execute. Busch sits roomy at 336-375-400-375-335, but 87° heat with a breeze to left can turn routine contact into extra pressure innings. Cleveland’s lineup continuity has been uneven, and with Bo Naylor and Brayan Rocchio still listed on the watch board, this feels like a night where the Cardinals’ contact depth plays up.",
"Pittsburgh fits the shape of this game: defend the strike zone, force Washington to earn every ninety feet, and let the park do the rest. PNC is asymmetric at 325-383-410-399-320, with that deep left-center gap punishing impatient hitters. Washington still carries active concerns around CJ Abrams and Brady House, so the safer read is the home side behind the more stable leverage plan.",
"Atlanta is the practical pick because this matchup should be decided by who controls traffic, not who lands the loudest swing. Truist’s 335-385-400-375-325 frame can reward pull power, but the light breeze in from right trims cheap homers just enough to favor deeper lineups. Miami’s board still flags Connor Norby and Andrew Nardi as active concerns, and that thin margin shows up late against Atlanta’s bullpen layering.",
"The Yankees are expensive, but the geometry supports them. Yankee Stadium is 318-399-408-385-314, and the short right-field porch keeps pressure on every left-handed mistake even when winds run crossfield. With Aaron Judge and Austin Wells active while the Angels monitor Jo Adell and Jordan Romano availability, New York carries the steadier path from first pitch to final three outs.",
"Detroit is the side because Comerica rewards complete baseball, and this is a complete-baseball matchup. At 345-370-420-365-330, the park stretches doubles into triples and punishes sloppy relay work, which favors disciplined clubs. Kansas City still has Bobby Witt Jr. and Cole Ragans on the active concern list, so the Tigers’ cleaner run-prevention profile is worth the shorter price.",
"Back Tampa Bay even with modest confidence, because the game state points their way. Rate Field checks in at 330-375-400-375-335, and a hard breeze in from right should flatten marginal fly-ball damage. Chicago’s active injury sheet still includes Andrew Benintendi and Colson Montgomery, and that leaves the Rays with the better chance to stack quality plate appearances instead of chasing one big inning.",
"Seattle is the call in a game that should stay narrow and tactical. Petco’s 334-390-396-382-322 profile and cool 65° air usually suppress carry, so command and defensive execution matter more than raw slug. San Diego still lists Fernando Tatis Jr. and Adrian Morejon as active concerns, and against Bryan Woo that lineup fragility is enough to lean Mariners.",
"Milwaukee is the lean because this matchup is about rhythm as much as talent. American Family Field at 344-371-400-374-345 plays neutral under the roof, which shifts the edge toward the club that strings at-bats together. Toronto still has Daulton Varsho and Andrés Giménez on the active sheet, and the Brewers’ fresher lineup flow gives them the cleaner route in a coin-flip game.",
"The Dodgers deserve the favorite tag because this matchup asks for depth, not heroics. Dodger Stadium runs 330-375-400-375-330, and the gentle push to right can reward disciplined opposite-field contact over all-or-nothing swings. With the Mets still monitoring Brett Baty and David Peterson status, Los Angeles owns the sturdier path once the bullpens begin trading matchup punches.",
"Philadelphia is the side because Citizens Bank turns good contact into quick damage when the night gets warm. At 329-374-401-369-330 with 15 mph out to center, run expectancy rises every time a starter misses arm side. Chicago’s active concern list still includes Dansby Swanson and Ben Brown, so the Phillies’ deeper run-creation floor is the better bet in a game likely decided by middle innings traffic.",
"Minnesota at plus money is playable because this game may hinge on sequencing, not ceiling. Target Field is 339-377-411-403-328, a park that rewards clubs willing to take extra bases and pressure cutoffs. Boston still tracks Connor Wong and Brayan Bello as active concerns, and with mild crosswind conditions the Twins’ cleaner run-manufacturing profile is enough to justify the dog price.",
"Texas is the pick, but not because of headline odds; because the run environment favors the steadier club. Sutter Health Park’s 330-403-407-403-325 center-field depth demands full innings of execution from both staffs. The Athletics still list Denzel Clarke and Hogan Harris as active concerns, and that roster uncertainty tilts late leverage toward Texas.",
"Baltimore remains the right side in a warm Camden setup where contact quality compounds quickly. The park sits 333-364-410-373-318, and 86° air with a slight push to center rewards lineups that can attack in waves. Arizona’s active concern notes on Alek Thomas and Corbin Carroll make their margin thinner than usual, giving the Orioles the more reliable late-game script.",
"San Francisco is a thin but reasonable lean in a park built for offense and stress. Great American is 328-379-404-370-325, yet the wind in from left can neutralize some pull-side loft and shift value to pitching command. Cincinnati still carries active concerns around Elly De La Cruz and Andrew Abbott availability, so the Giants’ veteran sequencing gives them the slightly safer finish in a tight game."
],
"/Users/asmith/.openclaw/workspace/sportzballz.io/2026-04-14-plus-money.html": [
"This is the kind of underdog ticket worth buying: St. Louis gets heat, breeze, and a workable park profile at Busch (336-375-400-375-335). In 87° weather with wind to left, plus-money sides survive by avoiding free passes and extending at-bats, and that is where the Cardinals can steal control. Cleveland still has Bo Naylor and Brayan Rocchio on the active board, which trims their depth in exactly the spots this game should turn.",
"Minnesota as a dog makes sense when you picture how Target Field plays at 339-377-411-403-328. Big alleys, cooler air, and a modest crosswind often reward doubles-and-defense baseball more than brute force. Boston’s active concern list still includes Connor Wong and Brayan Bello, so the Twins have a realistic path to grind this one into their preferred tempo."
],
"/Users/asmith/.openclaw/workspace/sportzballz.io/2026-04-14-run-totals.html": [
"Lean over in Philadelphia because Citizens Bank (329-374-401-369-330) plus 85° and wind out to center is a classic carry setup. Even well-located fastballs can turn loud in this air, and both offenses bring enough healthy core bats to keep pressure on middle relievers.",
"Over is justified at Busch tonight: 87° with wind to left can shrink a spacious 336-375-400-375-335 field in a hurry. With Cleveland still monitoring catcher depth and St. Louis carrying several active bullpen tags, there are too many plausible scoring paths to stay under 8.5.",
"Comerica’s big frame (345-370-420-365-330) usually scares over bettors, but warm air and wind to left make gap power play bigger than usual. Both lineups still feature key active bats, and late-inning command risk is enough to push this total toward nine.",
"Over at Truist is a pace call more than a weather call. The park dimensions (335-385-400-375-325) favor power alleys, and Atlanta-Miami projects to create repeated traffic with both clubs carrying active injury concerns in bullpen pieces. That is the profile that breaks totals open after the fifth.",
"Yankee Stadium over remains live because 318 down the right-field line never stops mattering. In warm 82° conditions, crosswind doesn’t kill carry so much as redistribute it, and both sides have enough top-end thump to force bullpen exposure by the middle frames.",
"Dodger Stadium over is playable even in cooler air because 330-375-400-375-330 still rewards disciplined line-drive offense when wind drifts to right. With active status questions around pieces of the Mets’ run prevention group, eight runs is a reachable bar.",
"Over in Houston comes from game texture: roof closed at Daikin means no weather drag and a stable hitting backdrop. On a 315-362-409-373-326 field, both lineups can build crooked innings if early command slips, and Colorado’s active concern list adds volatility to that outcome.",
"Under at Petco is the cleaner angle: 334-390-396-382-322 with 65° air and breeze in from left suppresses easy carry. If both starters hold first-pitch strike rhythm, this game should spend long stretches in one-run innings rather than big clusters.",
"Twins-Red Sox over works because Target’s deep alleys generate extra-base chaos when defenders get stretched. At 67° with neutral wind, this is less about weather and more about both clubs carrying enough active middle-order bats to threaten two big innings apiece.",
"Pirates-Nationals over leans on bullpen shape and park asymmetry, not wind. PNC’s 325-383-410-399-320 profile can still produce scoring when command wobbles, and Washington’s active concerns around key position players create defensive stress that feeds extra runs.",
"Camden over is reasonable in 86° air with a little help to center. The 333-364-410-373-318 layout suppresses some cheap pull homers, but sustained contact still creates doubles traffic, and both teams carry enough active lineup uncertainty to invite late mistakes.",
"Great American over stays attractive because the dimensions (328-379-404-370-325) do most of the heavy lifting even with wind in from left. One or two barrels per side can still flip the script fast in this park, especially once middle relief enters.",
"Brewers-Blue Jays over is a roof-game efficiency play. American Family’s controlled environment at 344-371-400-374-345 removes weather variance, and both rosters still show active tags among key arms, increasing the odds of one bullpen inning getting away.",
"Rangers-Athletics over tracks with Sutter Health’s deep gaps and long innings profile. At 330-403-407-403-325, extra-base hits pile up when command is ordinary, and both teams have enough active injury churn to make run prevention fragile after the starters exit.",
"Rays-White Sox over is uncomfortable but justified: warm 82° air and a park at 330-375-400-375-335 can still produce despite wind in from right. If either starter falls behind counts, this number can clear on doubles volume and bullpen traffic alone."
]
}

pattern = re.compile(r'<p class="lede">.*?</p>', re.S)

for path, ledes in files.items():
    p = Path(path)
    text = p.read_text()
    matches = list(pattern.finditer(text))
    if len(matches) != len(ledes):
        raise SystemExit(f"{path}: expected {len(ledes)} ledes but found {len(matches)}")
    out = []
    last = 0
    for m, new_lede in zip(matches, ledes):
        out.append(text[last:m.start()])
        out.append(f'<p class="lede">{new_lede}</p>')
        last = m.end()
    out.append(text[last:])
    p.write_text(''.join(out))
    print(f"updated {path}")
