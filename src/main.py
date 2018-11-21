import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from draw.buildings import draw_buildings
from draw.units import draw_units
from draw.strategies import workerRush
import cv2
import numpy as np


class EsyTooBot(sc2.BotAI):
    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 50

    async def on_step(self, iteration):
        await self.intel()
        if iteration == 0:
            await workerRush(self)

    async def intel(self):
        # https://github.com/Dentosal/python-sc2/blob/master/sc2/game_info.py#L162
        # print(self.game_info.map_size)

        # flip around. It's y, x when you're dealing with an array.
        game_data = np.zeros(
            (self.game_info.map_size[1], self.game_info.map_size[0], 3),
            np.uint8
        )
        # draw_buildings(self, game_data)
        draw_units(self, game_data)

        # flip horizontally to make our final fix in visual representation:
        flipped = cv2.flip(game_data, 0)
        resized = cv2.resize(flipped, dsize=None, fx=4, fy=4)

        cv2.imshow('Overview', resized)
        cv2.waitKey(1)


run_game(
    maps.get("(2)DreamcatcherLE"),
    [Bot(Race.Protoss, EsyTooBot()),
     Computer(Race.Protoss, Difficulty.Medium)
     ],
    realtime=False,
)
