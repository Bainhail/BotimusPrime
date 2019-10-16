from maneuvers.kit import *

from maneuvers.driving.drive import Drive
from maneuvers.driving.travel import Travel

from utils.travel_plan import TravelPlan
from math import pi, asin, atan2, sin, cos


class Arrive(Maneuver):
    '''
    Arrive at a target position at a certain time (game seconds).
    You can also specify `target_direction`, and it will try to arrive
    at an angle. However this does work well only if the car is already
    roughly facing the specified direction, and only if it's far enough.
    '''
    def __init__(self, car: Car):
        super().__init__(car)

        self.target_direction: vec3 = None
        self.target: vec3 = None
        self.time: float = 0
        self.speed_control: bool = False
        self.additional_shift = 0
        self.arena_clamp = 0

        self.lerp_t = 0.58

        self.drive = Drive(car)
        self.travel = Travel(car)

    def get_shifted_target(self) -> vec3:
        if self.target_direction is None:
            return vec3(self.target)

        car_vel = norm(self.car.velocity)
        target_direction = normalize(self.target_direction)
        shift = clamp(distance(self.car, self.target) * self.lerp_t, 0, car_vel * 1.5)
        car_to_target = ground_direction(self.car, self.target)

        if dot(target_direction, car_to_target) < 0:
            perpendicular_direction = cross(car_to_target)
            if dot(target_direction, perpendicular_direction) < 0:
                perpendicular_direction *= -1
            target_direction = perpendicular_direction

        if shift - self.additional_shift < turn_radius(clamp(car_vel, 1400, 2300) * 1.1):
            shift = 0
        else:
            shift += self.additional_shift

        shifted_target = self.target - target_direction * shift
        return Arena.clamp(shifted_target, self.arena_clamp)

    def get_total_distance(self) -> float:
        translated_target = self.get_shifted_target()
        return ground_distance(self.car, translated_target) + ground_distance(translated_target, self.target)

    def estimate_time(self) -> float:
        dist = self.get_total_distance()
        return self.travel.time_for_distance(dist)

    def step(self, dt):
        car = self.car
        translated_target = self.get_shifted_target()    

        if self.speed_control:
            translated_time = self.time - distance(translated_target, self.target) / max(1, clamp(norm(self.car.velocity), 500, 2300))            
            dist_to_target = distance(car.position, translated_target)
            target_speed = clamp(dist_to_target / max(0.001, translated_time - car.time), 0, 2300)

            if target_speed < 500:
                target_speed = 0

            self.drive.target_pos = translated_target
            self.drive.target_speed = target_speed
            self.drive.step(dt)
            self.controls = self.drive.controls
        else:
            self.travel.target = translated_target
            self.travel.step(dt)
            self.controls = self.travel.controls

        self.finished = self.car.time >= self.time

    def render(self, draw: DrawingTool):
        if self.speed_control:
            self.drive.render(draw)
        else:
            self.travel.render(draw)

        if self.target_direction is not None:
            draw.color(draw.lime)
            draw.triangle(self.target - self.target_direction * 250, self.target_direction)
            draw.color(draw.white)
            draw.line(self.target, self.get_shifted_target())

        