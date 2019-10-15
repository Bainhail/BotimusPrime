from training.botimus_training import BotimusStrikerExcercise, Car, Ball, SpecificManeuverStrikerExcercise
from rlutilities.linear_algebra import look_at, vec3, axis_to_rotation
from utils.vector_math import ground_direction


class ChipShot(SpecificManeuverStrikerExcercise):

    maneuver_name = "Offense"
    timeout = 10

    def set_car_ball_state(self, car: Car, ball: Ball):
        ball.position[0] = self.rng.n11() * 500
        ball.position[1] = -2000
        ball.position[2] = 200

        ball.velocity[0] = self.rng.n11() * 1500
        ball.velocity[1] = self.rng.n11() * 500
        ball.velocity[2] = 0

        car.position[0] = self.rng.n11() * 500
        car.position[1] = -5000
        car.position[2] = 20
        tdir = ground_direction(car, ball)
        car.orientation = axis_to_rotation(vec3(0,0,self.rng.uniform(0.0, 3.14)))
        car.velocity = tdir * 0
        car.boost = 100

class RampShot(SpecificManeuverStrikerExcercise):

    maneuver_name = "Offense"
    timeout = 10

    def set_car_ball_state(self, car: Car, ball: Ball):
        ball.position[0] = 2000
        ball.position[1] = -2000
        ball.position[2] = 200

        ball.velocity[0] = self.rng.uniform(1000, 2000)
        ball.velocity[1] = self.rng.n11() * 500
        ball.velocity[2] = 0

        car.position[0] = 3000
        car.position[1] = -4000
        car.position[2] = 20
        tdir = ground_direction(car, ball)
        car.orientation = look_at(tdir, vec3(0,0,1))
        car.velocity = tdir * 0
        car.boost = 100

class BouncyShot(SpecificManeuverStrikerExcercise):

    maneuver_name = "Offense"
    timeout = 10

    def set_car_ball_state(self, car: Car, ball: Ball):
        ball.position[0] = self.rng.n11() * 500
        ball.position[1] = 2000
        ball.position[2] = 1000

        ball.velocity[0] = self.rng.n11() * 1000
        ball.velocity[1] = self.rng.n11() * 500
        ball.velocity[2] = 0

        car.position[0] = self.rng.n11() * 500
        car.position[1] = -2000
        car.position[2] = 20
        tdir = ground_direction(car, ball)
        car.orientation = look_at(tdir, vec3(0,0,1))
        car.velocity = tdir * 0
        car.boost = 100

class WaitForBallToRollInfrontOfGoal(SpecificManeuverStrikerExcercise):

    maneuver_name = "Offense"
    timeout = 5

    def set_car_ball_state(self, car: Car, ball: Ball):
        ball.position[0] = 3200
        ball.position[1] = 5000 - self.rng.uniform(150, 2000)
        ball.position[2] = 200

        ball.velocity[0] = -800
        ball.velocity[1] = 0
        ball.velocity[2] = 200

        car.position[0] = self.rng.uniform(0, 3000)
        car.position[1] = 0
        car.position[2] = 20
        tdir = ground_direction(car, ball)
        car.orientation = look_at(tdir, vec3(0,0,1))
        car.velocity = tdir * 1000
        car.boost = 100

class WaitForBallToBounceInfrontOfGoal(SpecificManeuverStrikerExcercise):

    maneuver_name = "Offense"
    timeout = 5

    def set_car_ball_state(self, car: Car, ball: Ball):
        ball.position[0] = 3200
        ball.position[1] = 5000 - self.rng.uniform(150, 2000)
        ball.position[2] = 1000

        ball.velocity[0] = -800
        ball.velocity[1] = 0
        ball.velocity[2] = 200

        car.position[0] = self.rng.uniform(0, 3000)
        car.position[1] = 0
        car.position[2] = 20
        tdir = ground_direction(car, ball)
        car.orientation = look_at(tdir, vec3(0,0,1))
        car.velocity = tdir * 1000
        car.boost = 100