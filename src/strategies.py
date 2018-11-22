from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, PHOTONCANNON, FORGE


# select and tell all workers to go rush the enepy base
async def worker_rush(self):
    for worker in self.workers:
        await self.do(worker.attack(self.enemy_start_locations[0]))


# Build more workers when the minerals are available
async def build_workers(self):
    # nexus = command center
    for nexus in self.units(NEXUS).ready.noqueue:
        if self.can_afford(PROBE):
            await self.do(nexus.train(PROBE))


async def build_pylons(self):
    if self.supply_left < 5 and not self.already_pending(PYLON):
        nexuses = self.units(NEXUS).ready
        if nexuses.exists:
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexuses.first)


async def build_assimilator(self):
    for nexus in self.units(NEXUS).ready:
        vaspenes = self.state.vespene_geyser.closer_than(20.0, nexus)
        for vaspene in vaspenes:
            if not self.can_afford(ASSIMILATOR):
                break
            worker = self.select_build_worker(vaspene.position)
            if worker is None:
                break
            if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                await self.do(worker.build(ASSIMILATOR, vaspene))


async def expand(self):
    if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS) and not self.already_pending(NEXUS):
        await self.expand_now()


async def turtle_up(self):
    pylons = self.units(PYLON).ready
    if pylons.exists:
        pylon = pylons.random
        if not self.units(FORGE).ready.exists:
            if self.can_afford(FORGE) and not self.already_pending(FORGE):
                await self.build(FORGE, near=pylon)
        else:
            can_afford_cannon = self.can_afford(PHOTONCANNON) 
            less_cannons_than_pylons = self.units(PHOTONCANNON).amount < self.units(PYLON).amount
            not_already_building_one = not self.already_pending(PHOTONCANNON)
            if can_afford_cannon and less_cannons_than_pylons and not_already_building_one:
                await self.build(PHOTONCANNON, near=pylon)