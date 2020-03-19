from maneuvers.strikes.dodge_shot import DodgeShot
from utils.intercept import Intercept
from utils.math import abs_clamp


class CloseShot(DodgeShot):

    def configure(self, intercept: Intercept):
        self.target[0] = abs_clamp(self.intercept.ground_pos[0], 400)
        super().configure(intercept)
