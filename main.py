from setup import *
from simulation import Simulation

is_running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perfectly Elastic Collisions")

simulation = Simulation()

clock = pygame.time.Clock()

while is_running:

    delta_time_ms = clock.get_time()

    screen.fill((255, 255, 255))

    # Window close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # Speed up simulation when user presses left shift key
    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
        delta_time_ms *= 8

    simulation.step(delta_time_ms / 1000) # convert delta_time_ms to seconds
    simulation.draw(screen)

    pygame.display.update()
    clock.tick()

pygame.quit()