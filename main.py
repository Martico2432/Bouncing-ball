import pygame
import math
import random
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colliding Balls with Gravity")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Gravity constant
GRAVITY = 0.1

# Ball class
class Ball:
    def __init__(self, x, y, size, speed, angle):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = math.radians(angle)
        self.vx = speed * math.cos(self.angle)
        self.vy = speed * math.sin(self.angle)

    def move(self):
        # Apply gravity
        self.vy += GRAVITY

        prev_x, prev_y = self.x, self.y  # Store previous position

        self.x += self.vx
        self.y += self.vy

        # Check for collision with the circle boundary
        distance_from_center = math.hypot(self.x - WIDTH // 2, self.y - HEIGHT // 2)
        if distance_from_center + self.size > boundary_radius:
            # Calculate the distance to move back from the boundary
            overlap = distance_from_center + self.size - boundary_radius
            # Move the ball back by the overlap distance
            self.x -= overlap * (self.x - WIDTH // 2) / distance_from_center
            self.y -= overlap * (self.y - HEIGHT // 2) / distance_from_center

            # Calculate the normal vector at the point of collision
            nx = (self.x - WIDTH // 2) / distance_from_center
            ny = (self.y - HEIGHT // 2) / distance_from_center

            # Reflect the velocity vector
            dot_product = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot_product * nx
            self.vy -= 2 * dot_product * ny

            # Maintain speed by normalizing the velocity vector
            speed = math.hypot(self.vx, self.vy)
            if speed != 0:
                self.vx = (self.vx / speed) * self.speed
                self.vy = (self.vy / speed) * self.speed

            self.when_bounce()


    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

    def when_bounce(self):
        print(f"Bounced! New speed: {self.speed}, size: {self.size}")

    def check_collision(self, other):
        if not other:
            return
        distance = math.hypot(self.x - other.x, self.y - other.y)
        if distance < self.size + other.size:
            # Calculate the normal vector at the point of collision
            nx = (self.x - other.x) / distance
            ny = (self.y - other.y) / distance

            # Reflect the velocities
            dot_product_self = self.vx * nx + self.vy * ny
            dot_product_other = other.vx * nx + other.vy * ny

            self.vx -= 2 * dot_product_self * nx
            self.vy -= 2 * dot_product_self * ny
            other.vx -= 2 * dot_product_other * nx
            other.vy -= 2 * dot_product_other * ny

            self.when_bounce()
            other.when_bounce()

def spawn_ball(x, y, size, speed, angle):
    return Ball(x, y, size, speed, angle)

# Define circle boundary
boundary_radius = 250

# Create balls
ball1 = spawn_ball(WIDTH // 2, HEIGHT // 2, 20, 20, random.randint(0, 179))
# ball2 = spawn_ball(WIDTH // 2 - 50, HEIGHT // 2 - 50, 20, 3, 135)  # Modify or set to None if you don't want a second ball

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Draw boundary circle
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), boundary_radius, 1)

    # Move and draw balls
    ball1.move()
    ball1.draw(screen)
    try:
        if ball2:  # Ensure ball2 exists before processing
          ball2.move()
          ball2.draw(screen)
          ball1.check_collision(ball2)
          ball2.check_collision(ball1)  # Double-check collision to ensure both react
    except:
        pass

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
