from setup import *
from collision import WorldBoundsCollider
from ball import Ball

class Simulation:

    def __init__(self):
        #self.balls = [Ball(random.randint(0, 64), random.randint(0, 64), 0.4) for _ in range(5)]
        self.balls = [Ball(25, 32, 2), Ball(50, 32, 200)]

        self.balls.extend([Ball(random.randint(0, 64), random.randint(0, 64), random.randint(2, 20)) for _ in range(20)])

        self.balls[1].collider.velocity = pygame.Vector2(-10, 0)

        self.gravity = -9.8
        self.bounds = WorldBoundsCollider(pygame.Vector2(0, 0), pygame.Vector2(pixels_to_m(WIDTH), pixels_to_m(HEIGHT)))
    
    def step(self, delta_time):
        for b in self.balls:
            F_g = b.mass * self.gravity
            b.apply_force(pygame.Vector2(0, F_g))
            b.step(delta_time)
        for i, ball1 in enumerate(self.balls):
            # Start at the element after ball1 to ensure we go over each pair of balls exactly once
            for j, ball2 in enumerate(self.balls[i+1:]):
                hit_result = ball1.collider.collides_with(ball2.collider)
                if hit_result.is_colliding:
                    
                    # Push the two balls out of collision; if this is not done, it is possible
                    # that the balls will still be colliding the next physics step, causing 
                    # unwanted changes in velocity.
                    # One of the balls may have to move. We want this to be the lighter ball since 
                    # the lighter ball should not push the heavier one.
                    if ball1.mass < ball2.mass: # TODO consider doing this differently
                        ball1.collider.position += hit_result.hit_normal * hit_result.hit_depth
                    else:
                        ball2.collider.position -= hit_result.hit_normal * hit_result.hit_depth

                    m1 = ball1.mass
                    m2 = ball2.mass

                    # Get components of velocities along the hit normal
                    vi1 = ball1.collider.velocity.dot(hit_result.hit_normal)
                    vi2 = ball2.collider.velocity.dot(hit_result.hit_normal)

                    # Use the linear collision velocity formula
                    vf1 = ((m1 - m2)/(m1 + m2) * vi1) + ((2 * m2)/(m1 + m2) * vi2)
                    vf2 = ((2 * m1)/(m1 + m2) * vi1) + ((m2 - m1)/(m1 + m2) * vi2)
                    
                    # Apply the changes to the component of the velocities along the hit normal only
                    ball1.collider.velocity -= hit_result.hit_normal * vi1
                    ball1.collider.velocity += hit_result.hit_normal * vf1
                    ball2.collider.velocity -= hit_result.hit_normal * vi2
                    ball2.collider.velocity += hit_result.hit_normal * vf2

                    #print(f"{m1=} {m2=} {vi1=} {vi2=} {vf1=} {vf2=}")

        # Collision with window edges
        for ball in self.balls:
            hit_result = ball.collider.collides_with(self.bounds)
            if hit_result.is_colliding:
                ball.collider.position += hit_result.hit_normal * hit_result.hit_depth
                # Reflect velocity along the hit normal.
                ball.collider.velocity.reflect_ip(hit_result.hit_normal)


    def draw(self, surface):
        for b in self.balls:
            b.draw(surface)