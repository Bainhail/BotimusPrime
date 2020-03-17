from typing import Optional

from maneuvers.driving.drive import Drive
from maneuvers.driving.travel import Travel
from maneuvers.kit import Maneuver
from rlutilities.linear_algebra import vec3, norm, normalize
from rlutilities.simulation import Car
from utils.drawing import DrawingTool
from utils.math import clamp, nonzero
from utils.misc import turn_radius
from utils.vector_math import ground_distance


class Arrive(Maneuver):
    """
    Arrive at a target position at a certain time (game seconds).
    You can also specify `target_direction`, and it will try to arrive
    at an angle. However this does work well only if the car is already
    roughly facing the specified direction, and only if it's far enough.
    """

    def __init__(self, car: Car):
        super().__init__(car)
        self.drive = Drive(car)
        self.travel = Travel(car)

        self.target_direction: Optional[None] = None
        self.target: vec3 = None
        self.arrival_time: float = 0

        self.lerp_t = 0.6
        self.allow_dodges_and_wavedashes: bool = True
        self.additional_shift = 0

    def step(self, dt):
        target = self.target
        car = self.car

        if self.target_direction is not None:
            car_speed = norm(car.velocity)
            target_direction = normalize(self.target_direction)

            # in order to arrive in a direction, we need to shift the target in the opposite direction
            # the magnitude of the shift is based on how far are we from the target
            shift = clamp(ground_distance(car.position, target) * self.lerp_t, 0, car_speed * 1.5)

            # if we're too close to the target, aim for the actual target so we don't miss it
            if shift - self.additional_shift < turn_radius(clamp(car_speed, 1400, 2000) * 1.1):
                shift = 0
            else:
                shift += self.additional_shift

            shifted_target = target - target_direction * shift

            time_shift = ground_distance(shifted_target, target) * 0.7 / clamp(car_speed, 500, 2300)
            shifted_arrival_time = self.arrival_time - time_shift

        else:
            shifted_target = target
            shifted_arrival_time = self.arrival_time

        self.drive.target_pos = shifted_target

        dist_to_target = ground_distance(car.position, shifted_target)
        time_left = nonzero(shifted_arrival_time - car.time)
        target_speed = clamp(dist_to_target / time_left, 0, 2300)
        self.drive.target_speed = target_speed

        if (
            self.allow_dodges_and_wavedashes and norm(car.velocity) < target_speed - 600
            or not self.travel.driving  # a dodge/wavedash is in progress
        ):
            self.travel.target = shifted_target
            self.travel.step(dt)
            self.controls = self.travel.controls
        else:
            self.drive.step(dt)
            self.controls = self.drive.controls

        self.finished = self.car.time >= self.arrival_time

    def render(self, draw: DrawingTool):
        self.drive.render(draw)

        if self.target_direction is not None:
            draw.color(draw.lime)
            draw.triangle(self.target - self.target_direction * 250, self.target_direction)
