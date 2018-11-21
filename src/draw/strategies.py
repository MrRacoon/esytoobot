from sc2.constants import PROBE
import cv2


async def workerRush(self):
    for worker in self.workers:
        await self.do(worker.attack(self.enemy_start_locations[0]))
