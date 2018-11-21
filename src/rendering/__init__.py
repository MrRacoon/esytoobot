from rendering.units import draw_units
import cv2
import numpy as np

# This function will draw the game in realtime, in a pixelated game via
# opencv.
#
async def render(self):
    # https://github.com/Dentosal/python-sc2/blob/master/sc2/game_info.py#L162
    # print(self.game_info.map_size)

    # flip around. It's y, x when you're dealing with an array.
    game_data = np.zeros(
        (self.game_info.map_size[1], self.game_info.map_size[0], 3),
        np.uint8
    )

    draw_units(self, game_data)

    # flip horizontally to make our final fix in visual representation:
    flipped = cv2.flip(game_data, 0)
    resized = cv2.resize(flipped, dsize=None, fx=4, fy=4)

    cv2.imshow('Overview', resized)
    cv2.waitKey(1)
