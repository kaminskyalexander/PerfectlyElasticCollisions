from setup import *
from collision import CircleCollider

class Ball:

    def __init__(self, x, y, mass = 0.1):

        # mass is in kg
        self.mass = mass
        self.radius = mass * .01 + 1
        self.collider = CircleCollider(pygame.Vector2(x, y), self.radius)

    def step(self, delta_time):
        self.collider.step(delta_time)

    def apply_force(self, force):
        # Newton's second law duh XD
        self.collider.acceleration += force / self.mass 

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), get_pixel_position(self.collider.position), 
                           m_to_pixels(self.radius))