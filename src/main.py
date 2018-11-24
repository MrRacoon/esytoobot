import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Human, Bot, Computer
from unit_manager import ProtossBot

run_game(
    maps.get("(2)DreamcatcherLE"), [
        # Human(Race.Protoss),
        Bot(Race.Protoss, ProtossBot()),
        Computer(Race.Zerg, Difficulty.Easy),
     ],
    realtime=False,
)
