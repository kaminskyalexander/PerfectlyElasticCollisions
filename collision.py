from setup import *

class CollisionResult:

    def __init__(self):
        self.is_colliding = False
        self.hit_normal = None
        self.hit_depth = None

class CollisionDetection:

    @staticmethod
    def circle_circle(circle1, circle2):
        result = CollisionResult()
        # pythagorian theorem
        distance = math.hypot(circle1.position.x - circle2.position.x,
                              circle1.position.y - circle2.position.y)
        result.hit_depth = (circle1.radius + circle2.radius) - distance
        result.is_colliding = result.hit_depth > 0
        # Hit normal is the vector pointing from one circle's center to the other circle's center.
        result.hit_normal = (circle1.position - circle2.position)
        
        if result.hit_normal.length() != 0:
            result.hit_normal.normalize_ip()
        return result

    @staticmethod
    def circle_worldbounds(circle, worldbounds):
        result = CollisionResult()
        result.hit_normal = pygame.Vector2(0, 0)

        hit_depth_s = worldbounds.min_extent.y - (circle.position.y - circle.radius)
        hit_depth_n = circle.position.y + circle.radius - worldbounds.max_extent.y
        hit_depth_w = worldbounds.min_extent.x - (circle.position.x - circle.radius)
        hit_depth_e = circle.position.x + circle.radius - worldbounds.max_extent.x
    
        num_collisions = 0

        if hit_depth_s > 0: # S collision
            result.is_colliding = True
            result.hit_normal.y += 1
            num_collisions += 1
        if hit_depth_n > 0: # N collision
            result.is_colliding = True
            result.hit_normal.y -= 1
            num_collisions += 1
        if hit_depth_w > 0: # W collision
            result.is_colliding = True
            result.hit_normal.x += 1
            num_collisions += 1
        if hit_depth_e > 0: # E collision
            result.is_colliding = True
            result.hit_normal.x -= 1
            num_collisions += 1
        
        max_hit_depth = max(hit_depth_s, hit_depth_n, hit_depth_w, hit_depth_e)
        if num_collisions == 1:
            result.hit_depth = max_hit_depth
        elif num_collisions == 2:
            result.hit_depth = math.sqrt(2) * max_hit_depth

        if result.hit_normal.length() != 0:
            result.hit_normal.normalize_ip()
        return result

class Collider:

    def __init__(self, position):
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

    def step(self, delta_time):
        self.position += self.velocity * delta_time
        self.velocity += self.acceleration * delta_time
        # To prevent acceleration from accumulating (it should be added every frame)
        self.acceleration = pygame.Vector2(0, 0)

class CircleCollider(Collider):

    def __init__(self, position, radius):
        super().__init__(position)
        self.radius = radius

    def collides_with(self, other):
        if isinstance(other, CircleCollider):
            return CollisionDetection.circle_circle(self, other)
        elif isinstance(other, WorldBoundsCollider):
            return CollisionDetection.circle_worldbounds(self, other)
        else:
            raise NotImplementedError("Unknown collider type")

class WorldBoundsCollider:

    def __init__(self, min_extent, max_extent):
        self.min_extent = min_extent # NW corner
        self.max_extent = max_extent # SE corner