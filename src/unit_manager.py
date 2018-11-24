import sc2
from sc2.units import Units
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, PHOTONCANNON, \
    FORGE, CYBERNETICSCORE, STARGATE, VOIDRAY, GATEWAY, ZEALOT, STALKER
from rendering import render
from enum import Enum

class State(Enum):
    Collecting = 1,
    STAGING = 2
    Attacking = 3,


class ProtossBot(sc2.BotAI):
    def __init__(self):
        self._unit_map = {
            ZEALOT: 3,
            STALKER: 2,
            VOIDRAY: 1,
        }

        self.units = []
        self.production_threshold = 2

        self.SIZE_MOD = 4
        self.ITERATIONS_PER_MINUTE = 165

        self.MIN_SUPPLY_GAP = 6 # Min number of supply to trigger Pylon

        self.NUM_BASE = 3 # number of concurrent bases
        self.WORKERS_PER_BASE = 22 # number of concurrent bases
        self.BASE_STEP = 8
        self.BASE_RADIUS = 15
        self.PYLONS_PER_NEXUS = 3
        self.MAX_WORKERS = (self.NUM_BASE * self.WORKERS_PER_BASE)
        
        self.POP_TO_RETREAT_THRESHOLD = 0.2
        self.POP_TO_STAGE_THRESHOLD = 0.5
        self.POP_TO_ATTACK_THRESHOLD = 1.0

        self.group_state = State.Collecting
        self.zone_radius = 5
        self.worker_update_interval = 100

        self._saturated = False
        
   ########################################################################### 
   # The Machine

    async def on_step(self, iteration):
        # Rendering the 2d game view
        await render(self)

        # Worker Management
        if iteration % self.worker_update_interval == 0:
            await self.distribute_workers()

        # Structural assurance
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilator()

        # Unit Command
        await self.provide_units()
        await self.order_units()

        # Expansion
        await self.expand_new_base()

   ########################################################################### 
   # Economics

    def is_saturated(self, unit):
        unit_count = self.units(unit).amount
        unit_threshold = self._unit_map.get(unit, 0)
        return unit_count >= unit_threshold
    
    def population_progress(self):
        total = 0
        sum = 0
        for unit, desired_amount in self._unit_map.items():
            sum += self.units(unit).amount
            total += desired_amount
        return sum / total

   ########################################################################### 
   # Growth and Globalization

    async def build_unit(self, unit):
        if not self.already_pending(unit):
            if unit == ZEALOT:
                if not self.units(GATEWAY).exists:
                    await self.build_structure(GATEWAY)
                else:
                    await self.train_unit(unit, GATEWAY)
            if unit == STALKER:
                if not self.units(GATEWAY).exists:
                    await self.build_structure(GATEWAY)
                elif not self.units(CYBERNETICSCORE).exists:
                    await self.build_structure(CYBERNETICSCORE)
                else:
                    await self.train_unit(unit, GATEWAY)
            if unit == VOIDRAY:
                if not self.units(STARGATE).exists:
                    await self.build_structure(STARGATE)
                else:
                    await self.train_unit(unit, STARGATE)

    async def build_near_pylon(self, unit, pylon, queue=1):
        if self.can_afford(unit):
            if self.units(unit).not_ready.amount < queue:
                print("+", unit)
                await self.build(unit, near=pylon)

    async def build_structure(self, struct):
        if self.already_pending(struct):
            return
        pylons = self.units(PYLON).ready
        if pylons.exists:
            pylon = pylons.random
            ss = self.units(struct)
            if ss.amount < self.production_threshold:
                if struct == GATEWAY:
                    await self.build_near_pylon(struct, pylon, 1)
                if struct == CYBERNETICSCORE:
                    if not self.units(GATEWAY).ready.exists:
                        await self.build_structure(GATEWAY)
                    else:
                        await self.build_near_pylon(struct, pylon, 1)
                if struct == STARGATE:
                    if not self.units(CYBERNETICSCORE).ready.exists:
                        await self.build_structure(CYBERNETICSCORE)
                    else:
                        await self.build_near_pylon(struct, pylon, 1)
                        

    async def train_unit(self, unit, struct):
        ss = self.units(struct).ready.noqueue
        if ss.exists:
            if self.can_afford(unit):
                print("+", unit)
                await self.do(ss.random.train(unit))

   ########################################################################### 
   # Dept of Infrastructure

    async def build_pylons(self):
        nexi = self.units(NEXUS)
        if self.supply_left < self.MIN_SUPPLY_GAP:
            if not self.already_pending(PYLON):
                await self.build(PYLON, near=nexi.random, placement_step=self.BASE_STEP)
        else:
            for nexus in nexi:
                pylons_at_nexus = self.units(PYLON).closer_than(self.BASE_RADIUS, nexus.position)
                if pylons_at_nexus.amount < self.PYLONS_PER_NEXUS:
                    if not self.already_pending(PYLON):
                        await self.build(PYLON, near=nexus, placement_step=self.BASE_STEP)

    async def build_workers(self):
        # nexus = command center
        if self.MAX_WORKERS > self.workers.amount:
            for nexus in self.units(NEXUS).ready.noqueue:
                if self.can_afford(PROBE) and self.units(PROBE).amount < self.MAX_WORKERS:
                    print("+", PROBE)
                    await self.do(nexus.train(PROBE))

    async def build_assimilator(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(20.0, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR) or self.already_pending(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    print("+", ASSIMILATOR)
                    await self.do(worker.build(ASSIMILATOR, vaspene))


    async def expand_new_base(self):
        if self.NUM_BASE > self.units(NEXUS).amount:
            if self.can_afford(NEXUS):
                if not self.already_pending(NEXUS):
                    extra_workers = self.workers.amount - (self.units(NEXUS).amount * self.WORKERS_PER_BASE)
                    if extra_workers > 0 or self.MAX_WORKERS == self.workers.amount:
                            await self.expand_now()
    
    ##########################################################################
    # Politics

    async def provide_units(self):
        for unit in self._unit_map:
            if not self.is_saturated(unit):
                await self.build_unit(unit)

    async def order_units(self):
        if self.group_state == State.Attacking:
            await self.attack_enemy_main()
            if self.population_progress() < self.POP_TO_RETREAT_THRESHOLD:
                print('@collecting')
                self.group_state = State.Collecting

        elif self.group_state == State.Collecting:
            await self.rally_home()
            if self.population_progress() > self.POP_TO_STAGE_THRESHOLD:
                print('@staging')
                self.group_state = State.STAGING

        elif self.group_state == State.STAGING:
            await self.control_middle()
            if self.population_progress() >= self.POP_TO_ATTACK_THRESHOLD:
                print('@attacking')
                self.group_state = State.Attacking


    # Spot intel
    async def all_witin_zone(self, position):
        for unit_type in self._unit_map:
            if self.units(unit_type).further_than(self.zone_radius, position).idle.exists:
                return False
        return True
    
    async def all_witin_base(self):
        return self.all_witin_zone(self.main_base_ramp.top_center)

    async def all_within_middle(self):
        return self.all_witin_zone(self._game_info.map_center)

    
    # Spot migration
    async def rally_home(self):
        await self.zone_at(self.main_base_ramp.top_center)

    async def control_zone(self, position):
        await self.attack_at(position)

    async def control_middle(self):
        await self.control_zone(self._game_info.map_center)

    async def attack_enemy_main(self):
        await self.control_zone(self.enemy_start_locations[0])

    ##########################################################################
    # Laws and Justice

    async def pinpoint_at(self, position):
        "Move all idle units in the group exactly to the given position"
        for unit_type in self._unit_map:
            for unit in self.units(unit_type).idle:
                print(">-", unit)
                await self.do(unit.move(position))
    
    async def zone_at(self, position, group=None):
        "Move all idle units outside of the given zone, to rally to the zone"
        for unit_type in self._unit_map:
            strays = self.units(unit_type).further_than(self.zone_radius, position).idle
            for unit in strays:
                print(">o", unit)
                await self.do(unit.move(position))
    
    async def attack_at(self, position, group=None):
        "Send all idle units in the group to attack at a given place"
        if group is None:
            for unit_type in self._unit_map:
                strays = self.units(unit_type).further_than(self.zone_radius, position).idle
                for unit in strays:
                    print(">x", unit)
                    await self.do(unit.attack(position))
        else:
            for unit in group:
                print(">x", unit)
                await self.do(unit.attack(position))
