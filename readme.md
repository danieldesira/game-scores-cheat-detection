# Game Scores Cheat Detection

Proof-of-concept console app in Python which 
compares the scores in a Redis store against a rule 
sheet in a file. Used for Mission Sea Turtle Nest 
but can be adapted to support other games too.

## Rule sheet structure

Please check out the following JSON document 
as a reference:
```json
{
  "level1": {
    "characterMax": 180,
    "pass": 10
  },
  "level2": {
    "characterMax": 224,
    "pass": 10
  },
  "level3": {
    "characterMax": 2100,
    "pass": 50
  },
  "level4": {
    "characterMax": 1900,
    "pass": 75
  },
  "level5": {
    "characterMax": 1500,
    "pass": 100
  },
  "level6": {
    "characterMax": 420,
    "pass": 100
  },
  "level7": {
    "characterMax": 480,
    "pass": 100
  },
  "level8": {
    "characterMax": 800,
    "pass": 100
  },
  "durationReward": {
    "durationLimit": 300,
    "reward": 300
  }
}
```

``level*``: Contains point totals possible 
in the given level.

``characterMax``: Total accumalative points 
for all possible positive interactions with 
other characters. For example, eating food, 
mating or killing/avoiding opponents.

``pass``: Reward points for completing the 
given level.

``durationReward``: Contains information 
related to time-based reward systems.

``durationLimit``: Maximum time in seconds 
for the reward to be granted.

``reward``: Points awarded following a win 
in under the given ``durationLimit``.
