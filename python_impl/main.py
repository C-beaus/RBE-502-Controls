import pygame
import math
from dynamics import RobotDynamics, r, l

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ROBOT_WIDTH = 2  # Thickness of the robot's body in the side profile
MULTI = 40
ROBOT_HEIGHT = l * MULTI
WHEEL_RADIUS = r * MULTI
GRAVITY = 9.81
TIME_STEP = 0.02
IMPULSE_MAGNITUDE = 5

# PID constants
Kp = 100
Kd = 20
Ki = 1

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2-Wheel Self-Balancing Robot Visualization')

# Robot class
class Robot:
    def __init__(self, x, y):
        self.position = x
        self.angle = 0

        self.x_offset = x
        self.y_offset = y
        self.x = x
        self.y = y 

        self.dynamics = RobotDynamics()
    
    def update(self, dt):
        x_dyn, angle_dyn = self.dynamics.next_step(dt)
        self.x = self.x + MULTI * x_dyn
        self.angle = angle_dyn
    
    def apply_impulse(self, impulse):
        self.angular_velocity += impulse
    
    def draw(self, screen):
        wheel_center = (int(self.x), int(self.y + WHEEL_RADIUS))
        pygame.draw.circle(screen, BLACK, wheel_center , WHEEL_RADIUS)

        # Calculate the rotation matrix
        sin_angle = math.sin(self.angle+math.pi/2)
        cos_angle = math.cos(self.angle)
        print(self.angle)

        link_end = ( self.x_offset+ ROBOT_WIDTH*cos_angle,  self.y_offset-ROBOT_HEIGHT*sin_angle)
        
        pygame.draw.line(screen, BLUE, wheel_center, link_end, ROBOT_WIDTH)


        # # Calculate the body coordinates
        # body_top = (self.x + (ROBOT_HEIGHT / 2) * sin_angle, self.y - (ROBOT_HEIGHT / 2) * cos_angle)
        # body_bottom = (self.x - (ROBOT_HEIGHT / 2) * sin_angle, self.y + (ROBOT_HEIGHT / 2) * cos_angle)
        
        # # Draw the body
        # pygame.draw.line(screen, BLUE, body_top, body_bottom, ROBOT_WIDTH)
        
        # # Calculate the wheel position
        # wheel_center = (self.x, self.y + (ROBOT_HEIGHT / 2) * cos_angle)
        
        # Draw the wheel

# Main loop
def main():
    clock = pygame.time.Clock()
    robot = Robot(WIDTH // 2, HEIGHT // 2)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    robot.apply_impulse(-IMPULSE_MAGNITUDE)
                elif event.key == pygame.K_RIGHT:
                    robot.apply_impulse(IMPULSE_MAGNITUDE)
        
        # Update robot state
        robot.update(TIME_STEP)
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Draw the robot
        robot.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(int(1 / TIME_STEP))

    pygame.quit()

if __name__ == "__main__":
    main()
