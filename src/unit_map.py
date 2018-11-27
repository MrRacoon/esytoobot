import sc2
from sc2.units import Units
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, PHOTONCANNON, \
    FORGE, CYBERNETICSCORE, STARGATE, VOIDRAY, GATEWAY, ZEALOT, STALKER
from rendering import render
from enum import Enum


class UnitType(Enum):
    UNIT: 1
    STRUCTURE: 2

class Contruct(object):
    def __init__():
        self.BASE_STEP = 8
        self.BASE_RADIUS = 15
        
        self.protoss_unit_map = {
            # Unit
            ZEALOT: {
                type: UnitType.Unit,
                built_by: GATEWAY,
            },
            STALKER: {
                type: UnitType.Unit,
                built_by: GATEWAY,
            },
            VOIDRAY: {
                type: UnitType.Unit,
                built_by: STARGATE,
            },
            ORACLE: {
                type: UnitType.Unit,
                built_by: STARGATE,
            },

            # Structures
            NEXUS: {
                type: UnitType.Structure,
                depends: [ ],
                built_by: PROBE,
            },
            ASSIMILATOR: {
                type: UnitType.Structure,
                depends: [ ],
                built_by: PROBE,
            },
            PYLON: {
                type: UnitType.Structure,
                depends: [ ],
                built_by: PROBE,
            },
            GATEWAY: {
                type: UnitType.Structure,
                depends: [ ],
                built_by: PROBE,
            },
            FORGE: {
                type: UnitType.Structure,
                depends: [ ],
                built_by: PROBE,
            },
            SHIELDBATTERY: {
                type: UnitType.Structure,
                depends: [ GATEWAY ],
                built_by: PROBE,
            },
            CYBERNETICSCORE: {
                type: UnitType.Structure,
                depends: [ GATEWAY ],
                built_by: PROBE,
            },
            STARGATE: {
                type: UnitType.Structure,
                depends: [ CYBERNETICSCORE ],
                built_by: PROBE,
            },
            PHOTONCANNON: {
                type: Type.Structure
                depends: [ FORGE ],
                built_by: PROBE,
            },
        }

    def build(self, unit):
        info = self.protoss_unit_map.get(unit, None)
        if info is not Node:
            self._build(unit, info)
            
    def _build(self, unit, unit_info):
        deps_satisfied = True

        for dep in unit_info.depends:
            if not self.units(dep).exists:
                deps_satisfied = False
                self.build(dep)

        # Check dependencies
        if deps_satisfied:
            if unit_info.type == Type.Structure:
                if not self.already_pending(unit)
                    if unit == PYLON:
                        self.build_pylon()
                    else:
                        pylons = self.units(PYLON).ready
                        workers = self.workers
                        if workers.exists and pylons.exists:
                            pending_actions.append(worker.random.build(unit, near=pylon.random, placement_step=3))
            if unit_info.type == Type.Unit:
                buildings = self.units(unit_info.built_by)
                if buildings.exists
                    building = buildings.ready.noqueue
                    pending_actions.append(worker.build(unit, near=pylon, placement_step=3))


    async def build_pylon(self, worker=None):
        if worker is None and self.workers.exists:
            worker = self.workers.random
        nexi = self.units(NEXUS)
        target_nexus = None
        lowest_count = 0
        for nexus in nexi:
            pylons_at_nexus = self.units(PYLON).closer_than(self.BASE_RADIUS, nexus.position)
            if pylons_at_nexus.amount <= lowest_count
                target_nexus = nexus
                lowest_count = pylons_at_nexus.amount
                await self.pending_actions(worker.build(PYLON, near=nexus, placement_step=self.BASE_STEP))
