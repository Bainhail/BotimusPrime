from maneuvers.kit import *

from maneuvers.strikes.strike import Strike
from maneuvers.jumps.aim_dodge import AimDodge

class DodgeStrike(Strike):

    def __init__(self, car, ball, target):
        super().__init__(car, ball, target)
        self.dodge = AimDodge(car)
        self.dodging = False

    def is_intercept_desirable(self):
        # return self.intercept.position[2] < 320
        return self.intercept.position[2] < 280

    def get_offset_target(self):
        return ground(self.intercept.position) - self.get_hit_direction() * 100

    @staticmethod
    def get_time_to_z(z, press=0.2) -> float:
        # this function has been stolen from Wildfire
        # https://github.com/robbai/Wildfire/blob/6fa33fe53c8ab44d576b1b63049d5276df332172/src/main/java/wildfire/wildfire/physics/JumpPhysics.java#L20-L38
        # thanks Robbie

        velocity = 300
        acceleration = 1400 - 650

        displacement = velocity * press + 0.5 * acceleration * press**2

        velocity += acceleration * press
        acceleration = -650

        square = 2 * acceleration * (z - displacement) + velocity ** 2
        return press + (math.sqrt(square) - velocity) / acceleration

    def get_jump_time(self) -> float:
        target_height = clamp(self.intercept.position[2] - Ball.radius, 0, 220)

        time = self.get_time_to_z(target_height)
        return clamp(time, 0.05, 0.9)

    def configure_mechanics(self):
        super().configure_mechanics()

        self.dodge.car = self.car
        additional_jump = self.get_jump_time()
        self.dodge.duration = additional_jump
        self.arrive.additional_shift = additional_jump * norm(self.car.velocity)


    def step(self, dt):
        if self.dodging:
            self.dodge.direction = vec2(ground_direction(self.car, self.intercept))
            self.dodge.step(dt)
            self.controls = self.dodge.controls
        else:
            super().step(dt)
            if self.arrive.time - self.car.time < self.dodge.duration + 0.2:
                self.dodging = True
                self.dodge.direction = vec2(self.get_hit_direction())
        self.finished = self.finished or self.dodge.finished
