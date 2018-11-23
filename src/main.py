import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from unit_manager import GroupManager

run_game(
    maps.get("(2)DreamcatcherLE"), [
        Bot(Race.Protoss, GroupManager()),
        # Human(Race.Terran),
        Computer(Race.Zerg, Difficulty.Easy)
     ],
    realtime=False,
)
