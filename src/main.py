import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Human, Bot, Computer
from unit_manager import ProtossBot
from terran_unit_manager import MassReaperBot

run_game(
    maps.get("(2)DreamcatcherLE"), [
        # Human(Race.Protoss),
        Bot(Race.Protoss, ProtossBot()),
        Bot(Race.Terran, MassReaperBot())
     ],
    realtime=False,
)
