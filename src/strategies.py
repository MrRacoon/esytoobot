from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR


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
    if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
        await self.expand_now()
