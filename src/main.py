import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from strategies import build_workers, build_pylons, build_assimilator, expand, turtle_up, build_offense
from rendering import render


# The bot is described here.
#
# If we'll want to run bots against eachother, it's important to have this be
# exported.
#
class EsyTooBot(sc2.BotAI):
    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 70
        self.MIN_SUPPLY = 6 # Min number of supply to trigger Pylon
        self.BASE_STEP = 8
        self.BASE_RADIUS = 15
        self.NUM_BASE = 6 # number of concurrent bases
        self.PYLONS_PER_NEXUS = 2 # Min Number of pylons per base
        self.GATEWAY_PER_BASE = 2 # number of gateway required, for number of bases acquired
        self.STARGATE_PER_BASE = 1 # number of gateway required, for number of bases acquired

    # This is the function that gets run everytime starcraft asks us what we
    # want to do next. The on_step function runs from top to bottom, so the most
    # important functiions go at the top.
    #
    # Initially, let's make sure we have a decent macro before we can afford to
    # spend time worrying about the micro. Therefore, we'll prioritize mineral
    # collection, and since we're protoss for now (and likely for as long as we
    # want to keep winning), we'll need to find time to collect gas for mid to
    # late game.
    #
    async def on_step(self, iteration):
        # Rendering the game
        # await render(self)

        # Macro Force
        if iteration % 50 == 0:
            await self.distribute_workers()

        await build_workers(self)
        await build_pylons(self)
        await build_assimilator(self)
        # await turtle_up(self)
        await build_offense(self, iteration)
        await expand(self)


# Running this python file start a single game. This function is responsible for
# creating the game at a high level.
#
# The first argument describes what map we're going to play on (and that map
# better be available in your 'Starcraft 2' folder).
#
# The second argument describes the players. Our bot, and a computer.
#
# The third argument is for whether we want the game to run in realtime. It's
# fun to whatch with this set to True, but when it's time to run a TON of these
# games at once, we'll want to speed them up by making this False.
#
run_game(
    maps.get("(2)DreamcatcherLE"), [
        Bot(Race.Protoss, EsyTooBot()),
        # Human(Race.Terran),
        Computer(Race.Zerg, Difficulty.Medium)
     ],
    realtime=True,
)
