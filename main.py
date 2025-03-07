import pygame
import random
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AGENT_COLORS = [pygame.Color("blue"), pygame.Color("green"), pygame.Color("red"), pygame.Color("yellow"), pygame.Color("purple")]

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chrome Ninja Game AI')

# Clock object to control the frame rate
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Ninja settings
ninja_size = (35, 60)
ninja_jump_speed = 15
ninja_gravity = 1

# Obstacle settings
obstacle_width = 20
obstacle_height = 40
base_obstacle_speed = 7

# Game settings
FPS = 30

# Load background and ground images
background_img = pygame.image.load('Assets\\bg2.jpg')

# Load ninja sprites for animation
ninja_run_imgs = [pygame.image.load('Assets\\sprite\\r1.png'), pygame.image.load('Assets\\sprite\\r2.png'), pygame.image.load('Assets\\sprite\\r3.png'), pygame.image.load('Assets\\sprite\\r4.png'), pygame.image.load('Assets\\sprite\\r5.png')]
ninja_jump_img = pygame.image.load('Assets\\sprite\\j3.png')

# Load obstacle images
obstacle_imgs = [pygame.image.load('Assets\\obs3.png')]

# Sound effects
jump_sound = pygame.mixer.Sound('Assets\\jump.wav')
#bg_sound = pygame.mixer.Sound('Assets\\jump.mp3')


bground_x = 0

def draw_background():
    global bground_x
    bground_x -= obstacle_speed  # Move the ground along with the obstacles

    # Reset ground position to create a looping effect
    if bground_x <= -background_img.get_width():
        bground_x = 0

    # Draw two ground images to cover the entire screen and create the illusion of movement
    screen.blit(background_img, (bground_x, SCREEN_HEIGHT - background_img.get_height()))
    screen.blit(background_img, (bground_x + background_img.get_width(), SCREEN_HEIGHT - background_img.get_height()))

class NinjaAI:
    def __init__(self, weights=None, color=None):
        self.ninja_pos = [50, (SCREEN_HEIGHT - ninja_size[1])-50]
        self.ninja_jump = False
        self.ninja_fall_speed = 0
        self.score = 0
        self.alive = True
        self.run_index = 0
        self.run_frame_time = 0.1  # Time in seconds for each frame of running
        self.run_frame_counter = 0  # Counter to track the frame time
        self.weights = weights if weights is not None else np.random.rand(3, 1)
        self.color = color if color is not None else random.choice(AGENT_COLORS)

    def decide(self, inputs):
        result = np.dot(inputs, self.weights)
        return result > 0.5

    def update(self, obstacles):
        if self.alive:
            inputs = self.get_inputs(obstacles)
            if self.decide(inputs) and not self.ninja_jump:
                jump_sound.play()
                self.ninja_jump = True
                self.ninja_fall_speed = -ninja_jump_speed

            if self.ninja_jump:
                self.ninja_pos[1] += self.ninja_fall_speed
                self.ninja_fall_speed += ninja_gravity
                if self.ninja_pos[1] >= (SCREEN_HEIGHT - ninja_size[1]-50):
                    self.ninja_pos[1] = (SCREEN_HEIGHT - ninja_size[1]-50)
                    self.ninja_jump = False

            self.score += 1 / FPS

    def get_inputs(self, obstacles):
        next_obstacle = obstacles[0] if obstacles else [SCREEN_WIDTH, SCREEN_HEIGHT]
        distance = next_obstacle[0] - self.ninja_pos[0]
        height = next_obstacle[1]
        speed = obstacle_speed
        return np.array([distance, height, speed])

    def check_collision(self, obstacles):
        for obstacle_pos in obstacles:
            if (self.ninja_pos[0] < obstacle_pos[0] + obstacle_width and
                self.ninja_pos[0] + ninja_size[0] > obstacle_pos[0] and
                self.ninja_pos[1] < obstacle_pos[1] + obstacle_height and
                self.ninja_pos[1] + ninja_size[1] > obstacle_pos[1]):
                self.alive = False
                return

    def draw(self):
        if self.ninja_jump:
            screen.blit(ninja_jump_img, (self.ninja_pos[0], self.ninja_pos[1]))
        else:
            self.run_frame_counter += 1 / FPS  # Increment frame counter
            if self.run_frame_counter >= self.run_frame_time:
                self.run_index = (self.run_index + 1) % len(ninja_run_imgs)
                self.run_frame_counter = 0  # Reset counter
            screen.blit(ninja_run_imgs[self.run_index], (self.ninja_pos[0], self.ninja_pos[1]))

def evolve(population):
    population.sort(key=lambda x: x.score, reverse=True)
    next_generation = population[:len(population)//2]
    while len(next_generation) < len(population):
        parent1, parent2 = random.sample(next_generation, 2)
        child_weights = crossover(parent1.weights, parent2.weights)
        child_weights = mutate(child_weights)
        next_generation.append(NinjaAI(child_weights, random.choice(AGENT_COLORS)))
    return next_generation

def crossover(weights1, weights2):
    new_weights = weights1.copy()
    for i in range(len(new_weights)):
        if random.random() < 0.5:
            new_weights[i] = weights2[i]
    return new_weights

def mutate(weights):
    for i in range(len(weights)):
        if random.random() < 0.1:
            weights[i] += np.random.randn()
    return weights

def timer(scr, num_agents_left,gen):
    timer_text = font.render(f"Timer: {int(scr)} seconds", True, WHITE)
    agents_text = font.render(f"Agents Left: {num_agents_left}", True, WHITE)
    gen_text = font.render(f"Generation: {gen}", True, WHITE)
    screen.blit(agents_text, (10, 10))
    screen.blit(timer_text, (10, 50))
    screen.blit(gen_text, (10, 90))

def spawn_obstacle():
    obstacle_type = random.choice(obstacle_imgs)
    return [SCREEN_WIDTH, (SCREEN_HEIGHT-50) - obstacle_type.get_height(), obstacle_type]

def game_over():
    game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# Game loop
def main():
    global obstacle_speed
    scr = 0
    num_agents = 50
    generations = 100
    population = [NinjaAI(color=random.choice(AGENT_COLORS)) for _ in range(num_agents)]
    
    for gen in range(generations):
        obstacles = []
        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
        start_ticks = pygame.time.get_ticks()
        speed_increase_interval = 5000  # 5 seconds in milliseconds
        last_speed_increase_time = start_ticks
        obstacle_speed = base_obstacle_speed

        while any(agent.alive for agent in population):
            current_ticks = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT + 1:
                    obstacles.append(spawn_obstacle())
                    pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000, 2000))

            num_agents_left = sum(agent.alive for agent in population)
            
            for agent in population:
                agent.update(obstacles)
                agent.check_collision(obstacles)

            obstacles = [[x - obstacle_speed, y, img] for x, y, img in obstacles if x > -obstacle_width]

            # Increase obstacle speed every 5 seconds
            if current_ticks - last_speed_increase_time >= speed_increase_interval:
                obstacle_speed += 1
                last_speed_increase_time = current_ticks

            # Drawing
            screen.fill(WHITE)
            draw_background()

            #draw_ground()

            for agent in population:
                if agent.alive:
                    agent.draw()

            for obstacle_pos in obstacles:
                screen.blit(obstacle_pos[2], (obstacle_pos[0], obstacle_pos[1]))

            timer(scr, num_agents_left,gen)
            pygame.display.flip()

            clock.tick(FPS)
            scr += 1 / FPS

        print(f"Generation {gen + 1} - Max Score: {max(agent.score for agent in population):.2f}")
        population = evolve(population)
        obstacle_speed = base_obstacle_speed  # Reset speed for new generation
        scr = 0

    pygame.quit()

if __name__ == "__main__":
    main()


