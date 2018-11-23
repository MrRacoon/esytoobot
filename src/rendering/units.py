from sc2.constants import ASSIMILATOR, VESPENEGEYSER
from sc2 import Race
import cv2


white = (200, 200, 200)


def draw_units(self, game_data):
    for unit in self.state.units:
        draw_unit_2(self, unit, game_data)


def draw_unit_2(self, unit, game_data):
    position = (int(unit.position[0] * self.SIZE_MOD), int(unit.position[1] * self.SIZE_MOD))
    size = unit.radius * self.SIZE_MOD
    # build_radius = -1 if not unit.build_progress == 1 else unit.build_progress * size
    # sight = unit.sight_range * size_mod

    mod = 7919  # some prime
    default = 30
    amount = ((unit.type_id.value * mod) % 255)
    if unit.race == Race.Zerg:
        color = (default, default, amount)
    elif unit.race == Race.Terran:
        color = (default, amount, default)
    elif unit.race == Race.Protoss:
        color = (amount, default, default)
    else:
        color = (amount, amount, amount)
    #
    # Resources
    #

    if unit.is_mineral_field:
        cv2.circle(
            game_data,
            position,
            int(size),
            (200, 50, 100),
            1
        )
    elif unit.type_id == VESPENEGEYSER:
        assim = self.units(ASSIMILATOR).closer_than(1.0, unit)
        if not assim.exists or (hasattr(assim, "build_progress") and assim.build_progress < 1):
            cv2.circle(
                game_data,
                position,
                int(size),
                (50, 200, 100),
                1
            )

    #
    # Units
    #

    else:
        # print(unit)
        cv2.circle(
            game_data,
            position,
            int(size * unit.build_progress),
            color,
            1 if unit.build_progress < 1 else -1
        )
