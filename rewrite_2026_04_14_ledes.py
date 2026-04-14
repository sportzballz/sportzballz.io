import re
from pathlib import Path

base=Path('/Users/asmith/.openclaw/workspace/sportzballz.io')

repls={
'2026-04-14.html':[
"Pittsburgh is the steadier club in a park built for adults: 325 down the left line, a deep 399 to center, and that long left-center pocket that turns eager fly balls into outs. With warm air (79°) and a hard crosswind, contact quality and defensive range matter more than moonshot hunting, and that favors the home side’s cleaner run prevention. Bryan Reynolds is listed active, both lineups are posted, and the edge rests on innings control rather than surprise absences.",
"Atlanta gets this spot because Truist (roughly 335-400-325) rewards balanced damage, and the Braves can score to all fields instead of living on one swing plane. Dry, warm conditions and a mild crosswind keep the run environment fair, while the Marlins still arrive with more pressure on their middle innings. Austin Riley and Chris Sale are both listed active, so the favorite keeps the more reliable nine-inning path.",
"Comerica’s huge center field (420) and deep alleys punish cheap power, which nudges this game toward sequencing and gap defense. Detroit profiles better for that style, especially if this turns into doubles baseball instead of homer baseball. Framber Valdez and Bobby Witt Jr. are both active, but the Tigers still carry the cleaner run-prevention shape in this park.",
"Camden is still quirky after the left-field changes: tougher for routine lefty lift, friendlier for disciplined right-center work, and Arizona fits that geometry well. In 88-degree heat with a light breeze to center, this underdog has enough thump and speed to create extra-base pressure without needing three homers. Corbin Carroll and Colton Cowser are active, and the plus number remains justified.",
"Busch (336-400-335) is spacious enough that outfield reads and contact suppression usually decide close games, and St. Louis grades better in that texture. The hot night and breeze out to center raise scoring risk, but the Cardinals still carry the sturdier route through the late innings. Iván Herrera and Bo Naylor are active; this still prices as a legitimate home-dog setup.",
"At Rate Field, the dimensions are neutral on paper (330-400-335), so this is really a starter-and-bullpen control game. Tampa Bay’s pitching profile is built for that, and the White Sox still carry more volatility in run prevention when traffic starts stacking. Andrew Benintendi is listed active, but with lineups pending the Rays remain the steadier construction.",
"Petco’s big gaps and marine air usually reward command over chaos, and this matchup leans that way despite San Diego’s star power. The forecast says mid-60s with wind in from center, which trims long-ball luck and makes execution in leverage innings the true separator. Seattle’s lineup is posted while San Diego’s is pending; even with Fernando Tatis Jr. active, that uncertainty helps the road side.",
"Yankee Stadium is always a geometry conversation: 314 to right, a towering look to left-center, and no mercy for pitchers who miss arm side. With warm air and breeze carrying to center, this can get loud fast, but New York’s offense is better equipped to turn that setting into crooked numbers. Aaron Judge is active and both lineups are in, so the price reflects a real matchup edge.",
"Dodger Stadium plays fairer than its reputation when the night is cool, but the home club still owns more ways to win this specific game script. The dimensions (330-400-330) don’t hand free offense to either side; they reward complete at-bats and cleaner staff work. With both lineups confirmed and major pieces active, Los Angeles remains the side with fewer weak innings to protect.",
"Under the Milwaukee roof, weather noise drops out and roster quality gets louder. The Brewers’ profile fits that: enough athletic pressure to create extra 90 feet, plus a pitching path that can survive if the starter only gives five. Brice Turang and Daulton Varsho are both active, but with lineups still pending this still tilts to Milwaukee’s steadier build.",
"Target Field is roomy to center and right-center, so this game should hinge on who strings quality plate appearances rather than who steals one short-porch homer. Minnesota’s underdog case comes from exactly that: patient offense and enough mound depth to keep Boston from avalanche innings. Byron Buxton and Ceddanne Rafaela are active, and the plus price stays playable.",
"Great American is compact (328 to left, 325 to right) and can flip a game in ten minutes, so backing anyone here requires a team that can answer runs, not just prevent them. San Francisco brings a more complete run-creation profile into those conditions, even before the humid 80-degree air adds carry. Elly De La Cruz is active, but with lineups pending the slight road price is still defensible.",
"Sutter Health Park has tighter minor-league style sightlines and quicker run swings than many bettors price in, but Texas is the deeper roster over nine innings. The evening weather is mild with a gentle push to center, enough to reward hard contact but not enough to erase pitching command. Corey Seager is active and both lineups are posted, so the Rangers’ side is still the sturdier hold.",
"Citizens Bank (329-401-330) is built for volatility, yet Philadelphia enters with the better balance between damage and damage control. Warm conditions and a crosswind to right keep offense live, but the Phillies are better positioned to win the middle-third innings where these games often break open. Bryce Harper and Dansby Swanson are active, and this still reads as structure over noise."
],
'2026-04-14-plus-money.html':[
"Arizona’s plus-money value is rooted in fit: Camden’s current shape rewards line-drive precision and athletic outfield play, and the Diamondbacks can do both. In hot, dry weather with a breeze to center, they still have enough speed-and-gap pressure to manufacture runs without waiting on the three-run ball. Corbin Carroll and Colton Cowser are active, and the dog is live for all nine.",
"St. Louis as a dog works because Busch stretches offense into a full-field exam, and the Cardinals are better built for that exam tonight. The heat and wind out to center raise total-run risk, but they also reward clubs that control contact quality and avoid free passes late. With Iván Herrera and Bo Naylor both active, this plus price is worth taking.",
"Minnesota plus money is a park-and-style play: Target Field’s spacious right-center limits cheap pull damage and favors teams that run counts and drive gaps. The Twins’ lineup shape matches that environment, and Boston’s path asks for more pitch-level precision than this matchup usually grants. Byron Buxton and Ceddanne Rafaela are active, and the underdog case remains sturdy."
],
'2026-04-14-run-totals.html':[
"OVER 9.5 fits PNC tonight because warm air and a lively crosswind can turn routine flies into playable chaos, especially in the big left-center gaps. Both offenses can pressure the extra-base lanes, and with Bryan Reynolds active this game has enough lineup punch to stress both bullpens.",
"OVER 8.5 is justified at Truist: 335-400-325 with good carry temperatures tends to reward hard contact from both boxes. Austin Riley is active, and this projects more like sustained traffic than a clean duel.",
"UNDER 7.59 leans on park geometry and starting talent: Comerica’s deep center and wide alleys suppress easy homers, forcing long rallies to beat a low total. If the starters command early, this becomes a doubles-and-strand game that often lands below number.",
"OVER 8.5 in St. Louis is a weather-and-contact call: near-90 heat plus wind to center can erase some of Busch’s usual run suppression. With Iván Herrera and Bo Naylor active, this sets up for at least a couple of multi-run frames.",
"UNDER 7.5 at Rate Field is playable because the total is already tight and the pitching matchup can keep damage segmented rather than snowballing. Crosswind conditions and heavier air help keep pull-side loft from turning into automatic seats.",
"UNDER 7.0 at Petco is a classic marine-layer profile: cooler temps, wind in from center, and a park that punishes mishit power. Even with Fernando Tatis Jr. active, this environment usually demands three clean contacts in one inning to clear a number this low.",
"OVER 8.59 in the Bronx is mostly geometry and weather: the short right-field porch and warm air expand the home-run window for both lineups. With Aaron Judge active, one misplaced fastball can move this total a full run toward the over.",
"OVER 7.5 at Dodger Stadium asks for steady offense, not a slugfest, and both clubs can supply that against this game script. Neutral dimensions with a light breeze out are enough to turn quality contact into eight-plus total runs by late innings.",
"OVER 8.0 in Minneapolis is a sequencing bet: both offenses can string at-bats, and Target’s gaps reward line-drive baseball when defenders are forced to cover distance. With Byron Buxton active and both lineups posted, eight is a reachable threshold.",
"OVER 9.45 at Great American is straightforward park math: compact corners, summer-like warmth, and enough wind to keep carry alive. With Elly De La Cruz active, this venue can turn ordinary fly-ball nights into bullpen stress tests quickly.",
"OVER 9.5 in Philadelphia rides conditions and dimensions together: 329/401/330 with warm air keeps the ball in flight and the pressure on middle relief. Bryce Harper active raises the damage floor in a park where one shaky inning snowballs fast.",
"UNDER 8.82 in Baltimore is a run-shape play: Camden’s altered left field cuts off some routine pull power, and both clubs can work efficiently through the first six innings. Even in heat, this number leaves room for offense without demanding a full shootout.",
"UNDER 7.0 in Milwaukee benefits from roof-controlled stability and two staffs capable of limiting free baserunners. With weather removed from the equation, run creation has to be earned pitch by pitch, which favors a lower total.",
"UNDER 8.59 in Sacramento leans on night conditions and projected inning distribution: mild temps plus manageable wind make it harder for fringe contact to leave. Unless one starter loses the zone entirely, this total asks for more sustained damage than the setup suggests."
]
}

for fn, arr in repls.items():
    p=base/fn
    s=p.read_text()
    matches=list(re.finditer(r'<p class="lede">.*?</p>', s, flags=re.S))
    if len(matches)!=len(arr):
        raise RuntimeError(f'{fn}: expected {len(arr)} ledes, found {len(matches)}')
    out=[]
    last=0
    for m,new in zip(matches,arr):
        out.append(s[last:m.start()])
        out.append(f'<p class="lede">{new}</p>')
        last=m.end()
    out.append(s[last:])
    p.write_text(''.join(out))
    print('updated', fn)
