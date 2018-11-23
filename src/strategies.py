from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, PHOTONCANNON, \
    FORGE, CYBERNETICSCORE, STARGATE, VOIDRAY, GATEWAY, ZEALOT


async def worker_rush(self):
    for worker in self.workers:
        await self.do(worker.attack(self.enemy_start_locations[0]))


async def build_workers(self):
    # nexus = command center
    for nexus in self.units(NEXUS).ready.noqueue:
        if self.can_afford(PROBE) and self.units(PROBE).amount < self.MAX_WORKERS:
            print("Training", PROBE)
            await self.do(nexus.train(PROBE))


async def build_pylons(self):
    nexi = self.units(NEXUS)
    if self.supply_left < self.MIN_SUPPLY:
        if not self.already_pending(PYLON):
            await self.build(PYLON, near=nexi.random, placement_step=self.BASE_STEP)
    else:
        for nexus in nexi:
            pylons_at_nexus = self.units(PYLON).closer_than(self.BASE_RADIUS, nexus.position)
            if pylons_at_nexus.amount < self.PYLONS_PER_NEXUS:
                if not self.already_pending(PYLON):
                    await self.build(PYLON, near=nexus, placement_step=self.BASE_STEP)


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
                print("Building", ASSIMILATOR)
                await self.do(worker.build(ASSIMILATOR, vaspene))


async def expand(self):
    if self.NUM_BASE > self.units(NEXUS).amount and self.can_afford(NEXUS) and not self.already_pending(NEXUS):
        await self.expand_now()


async def turtle_up(self):
    pylons = self.units(PYLON).ready
    if pylons.exists:
        pylon = pylons.random
        if not self.units(FORGE).ready.exists:
            await build_near_pylon(self, FORGE, pylon, 1)
        else:
            if self.units(PHOTONCANNON).amount < self.units(PYLON).amount:
                if not self.already_pending(PHOTONCANNON):
                    await build_photon_cannon(self, pylon)


async def build_offense(self, iteration):
    pylons = self.units(PYLON).ready

    # Build Void Rays
    if self.units(STARGATE).ready.exists:
        for sg in self.units(STARGATE).ready.noqueue:
            await train_at_stargate(self, VOIDRAY, sg)

    if self.units(GATEWAY).ready.exists:
        for gw in self.units(GATEWAY).ready.noqueue:
            if self.units(ZEALOT).amount < 7 and self.can_afford(ZEALOT):
                await train_at_gateway(self, ZEALOT, gw)

    # Assemble, and Attack Move
    if self.units(VOIDRAY).idle.amount > 2 and iteration % 100 == 0:
        for vr in self.units(VOIDRAY).idle:
            await self.do(vr.attack(self.enemy_start_locations[0]))

    if self.units(ZEALOT).idle.amount > 7 and iteration % 100 == 0:
        for z in self.units(ZEALOT).idle:
            await self.do(z.attack(self.enemy_start_locations[0]))

    # Macro
    if pylons.exists:
        pylon = pylons.random

        if self.units(GATEWAY).amount < self.NUM_BASE * self.GATEWAY_PER_BASE:
            await build_near_pylon(self, GATEWAY, pylon, 2)

        elif not self.units(CYBERNETICSCORE).ready.exists:
            await build_near_pylon(self, CYBERNETICSCORE, pylon, 1)

        elif self.units(STARGATE).amount < self.STARGATE_PER_BASE:
            await build_near_pylon(self, STARGATE, pylon, 1)


###############################################################################
# Utilities
#
# To help reduce the sheer volume of code


async def build_near_pylon(self, unit, pylon, queue=1):
    if self.can_afford(unit):
        if self.units(unit).not_ready.amount < queue:
            print("-", unit)
            await self.build(unit, near=pylon)
            print("+", unit)


async def train_at_gateway(self, unit,  gw):
    if self.can_afford(unit):
        print("-", unit)
        await self.do(gw.train(unit))
        print("+", unit)


async def train_at_stargate(self, unit,  sg):
    if self.can_afford(unit):
        print("-", unit)
        await self.do(sg.train(unit))
        print("+", unit)

async def build_photon_cannon(self, near, step=1):
    if self.can_afford(PHOTONCANNON):
        print("-", PHOTONCANNON)
        await self.build(PHOTONCANNON, near, placement_step=step)
        print("+", PHOTONCANNON)
