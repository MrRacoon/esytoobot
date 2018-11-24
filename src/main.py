import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from unit_manager import ProtossBot

run_game(
    maps.get("(2)DreamcatcherLE"), [
        Bot(Race.Protoss, ProtossBot()),
        # Human(Race.Terran),
        Computer(Race.Zerg, Difficulty.Easy)
     ],
    realtime=False,
)
