from sc2.constants import NEXUS, HATCHERY, COMMANDCENTER
import cv2


def draw_buildings(self, game_data):
    for nexus in self.units(NEXUS):
        nex_pos = nexus.position
        cv2.circle(
            game_data,
            (int(nex_pos[0]), int(nex_pos[1])),
            10,
            (0, 255, 0),  # BGR
            -1
        )
    for hatchery in self.units(HATCHERY):
        nex_pos = hatchery.position
        cv2.circle(
            game_data,
            (int(nex_pos[0]), int(nex_pos[1])),
            10,
            (0, 0, 255),  # BGR
            -1
        )

    for cc in self.units(COMMANDCENTER):
        nex_pos = cc.position
        cv2.circle(
            game_data,
            (int(nex_pos[0]), int(nex_pos[1])),
            10,
            (255, 0, 0),  # BGR
            -1
        )
