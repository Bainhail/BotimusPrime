from rlutilities.simulation import Car, Input
from rlutilities.linear_algebra import dot, normalize, sgn, vec3
from maneuvers.jumps.jump import Jump


class AirDodge:

    def __init__(self, car, duration=0.0, target=None):

        self.car: Car = car
        self.target: vec3 = target
        self.controls = Input()

        self.jump = Jump(duration)

        if duration <= 0:
            self.jump.finished = True

        self.counter = 0
        self.state_timer = 0.0
        self.total_timer = 0.0

        self.finished = False

    def step(self, dt):

        recovery_time = 0.0 if (self.target is None) else 0.4

        if not self.jump.finished:

            self.jump.step(dt)
            self.controls = self.jump.controls

        else:

            if self.counter == 0:

                # double jump
                if self.target is None:
                    self.controls.roll = 0
                    self.controls.pitch = 0
                    self.controls.yaw = 0

                # air dodge
                else:
                    target_local = dot(self.target - self.car.position, self.car.orientation)
                    target_local[2] = 0

                    direction = normalize(target_local)

                    self.controls.roll = 0
                    self.controls.pitch = -direction[0]
                    self.controls.yaw = sgn(self.car.orientation[2, 2]) * direction[1]

            elif self.counter == 2:

                self.controls.jump = 1

            elif self.counter >= 4:

                self.controls.roll = 0
                self.controls.pitch = 0
                self.controls.yaw = 0
                self.controls.jump = 0

            self.counter += 1
            self.state_timer += dt

        self.finished = (self.jump.finished and
                         self.state_timer > recovery_time and
                         self.counter >= 6)