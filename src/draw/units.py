from sc2.constants import PROBE
import cv2


def draw_units(self, game_data):
    for probe in self.units(PROBE):
        nex_pos = probe.position
        cv2.circle(
            game_data,
            (int(nex_pos[0]), int(nex_pos[1])),
            1,
            (0, 0, 255),
            -1
        )  # BGR
