from sc2.constants import ASSIMILATOR, VESPENEGEYSER
from sc2 import Race
from rendering.map import size_mod
import cv2


white = (200, 200, 200)


def draw_units(self, game_data):
    for unit in self.state.units:
        draw_unit_2(self, unit, game_data)


def draw_unit(unit, game_data):
    # Coloring

    position = (int(unit.position[0] * size_mod), int(unit.position[1] * size_mod))
    size = unit.radius
    sight = unit.sight_range

    mod = 7919  # some prime
    default = 23
    amount = ((unit.type_id.value * mod) % 255)
    if unit.race == Race.Zerg:
        color = (default, default, amount)
    elif unit.race == Race.Terran:
        color = (default, amount, default)
    elif unit.race == Race.Protoss:
        color = (amount, default, default)
    else:
        color = (amount, amount, amount)
        size = 1
        sight = 0


    # Sight
    # cv2.circle(
    #     game_data,
    #     position,
    #     int(sight),
    #     white,
    #     1
    # )

    if not hasattr(unit, "build_progress") or unit.build_progress == 1:
        # Body
        cv2.circle(
            game_data,
            position,
            int(size * size_mod),
            color,
            -1
        )
    else:
        cv2.circle(
            game_data,
            position,
            int(size * unit.build_progress * size_mod),
            color,
            1
        )

def draw_unit_2(self, unit, game_data):
    position = (int(unit.position[0] * size_mod), int(unit.position[1] * size_mod))
    size = unit.radius * size_mod
    build_radius = -1 if not unit.build_progress == 1 else unit.build_progress * size
    sight = unit.sight_range * size_mod

    mod = 7919  # some prime
    default = 0
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
