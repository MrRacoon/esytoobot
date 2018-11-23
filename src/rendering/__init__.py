from rendering.units import draw_units
from cv2 import INTER_CUBIC
import cv2
import numpy as np


# This function will draw the game in realtime, in a pixelated game via
# opencv.
#
async def render(self):
    # https://github.com/Dentosal/python-sc2/blob/master/sc2/game_info.py#L162

    game_data = np.zeros(
        (self.game_info.map_size[1] * self.SIZE_MOD, self.game_info.map_size[0] * self.SIZE_MOD, 3),
        np.uint8
    )

    draw_units(self, game_data)

    # flip horizontally to make our final fix in visual representation:
    flipped = cv2.flip(game_data, 0)
    resized = cv2.resize(
        flipped,
        dsize=(1000, 760),
        fx=self.SIZE_MOD,
        fy=self.SIZE_MOD,
        interpolation=INTER_CUBIC
    )

    cv2.imshow('Overview', flipped)
    cv2.waitKey(1)
