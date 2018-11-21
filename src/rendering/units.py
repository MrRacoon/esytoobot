from sc2.constants import PROBE, NEXUS, HATCHERY, DRONE, SCV, COMMANDCENTER
from sc2 import Race
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

def draw_units(self, game_data):
    for unit in self.state.units:
        draw_unit(unit, game_data)

def draw_unit (unit, game_data) :
    # Coloring
    mod = 7919 # some prime
    default = 50
    amount = ((unit.type_id.value * mod) % 255)
    if unit.race == Race.Protoss:
        color = (default, default, amount)
    elif unit.race == Race.Terran:
        color = (default, amount, default)
    elif unit.race == Race.Zerg:
        color = (amount, default, default)
    else:
        color = (amount, amount, amount)

    cv2.circle(
        game_data,
        (int(unit.position[0]), int(unit.position[1])),
        1,
        color,
        -1
    )
