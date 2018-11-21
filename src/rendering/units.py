from sc2.constants import PROBE, NEXUS, HATCHERY, DRONE, SCV, COMMANDCENTER
from sc2 import Race
from rendering.map import size_mod
import cv2

# protoss_units = [
#     PROBE,
#     NEXUS
# ]
#
# zerg_units = [
#     DRONE,
#     HATCHERY
# ]
#
# terran_units = [
#     SCV,
#     COMMANDCENTER
# ]

white = (200, 200, 200)

def draw_units(self, game_data):
    for unit in self.state.units:
        draw_unit(unit, game_data)

def draw_unit (unit, game_data) :
    # Coloring
    mod = 7919 # some prime
    default = 23

    position = (int(unit.position[0]), int(unit.position[1]))
    size = unit.radius * size_mod
    radius = unit.radar_range * size_mod

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
        radius = 1

    # Sight
    cv2.circle(
        game_data,
        position,
        int(radius),
        white,
        1
    )
    # Body
    cv2.circle(
        game_data,
        position,
        int(size),
        color,
        -1
    )
