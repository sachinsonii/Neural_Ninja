import pygame
import random
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AGENT_COLORS = [pygame.Color("blue"), pygame.Color("green"), pygame.Color("red"), pygame.Color("yellow"), pygame.Color("purple")]

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chrome Dino Game AI')

# Clock object to control the frame rate
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

# Dino settings
dino_size = (60, 60)
dino_jump_speed = 15
dino_gravity = 1

# Obstacle settings
obstacle_width = 20
obstacle_height = 40
obstacle_color = BLACK
base_obstacle_speed = 7

# Game settings
FPS = 30

class DinoAI:
    def __init__(self, weights=None, color=None):
        self.dino_pos = [50, SCREEN_HEIGHT - dino_size[1]]
        self.dino_jump = False
        self.dino_fall_speed = 0
        self.score = 0
        self.alive = True
        self.weights = weights if weights is not None else np.random.rand(3, 1)
        self.color = color if color is not None else random.choice(AGENT_COLORS)

    def decide(self, inputs):
        result = np.dot(inputs, self.weights)
        return result > 0.5

    def update(self, obstacles):
        if self.alive:
            inputs = self.get_inputs(obstacles)
            if self.decide(inputs) and not self.dino_jump:
                self.dino_jump = True
                self.dino_fall_speed = -dino_jump_speed

            if self.dino_jump:
                self.dino_pos[1] += self.dino_fall_speed
                self.dino_fall_speed += dino_gravity
                if self.dino_pos[1] >= SCREEN_HEIGHT - dino_size[1]:
                    self.dino_pos[1] = SCREEN_HEIGHT - dino_size[1]
                    self.dino_jump = False

            self.score += 1 / FPS

    def get_inputs(self, obstacles):
        next_obstacle = obstacles[0] if obstacles else [SCREEN_WIDTH, SCREEN_HEIGHT]
        distance = next_obstacle[0] - self.dino_pos[0]
        height = next_obstacle[1]
        speed = obstacle_speed
        return np.array([distance, height, speed])

    def check_collision(self, obstacles):
        for obstacle_pos in obstacles:
            if (self.dino_pos[0] < obstacle_pos[0] + obstacle_width and
                self.dino_pos[0] + dino_size[0] > obstacle_pos[0] and
                self.dino_pos[1] < obstacle_pos[1] + obstacle_height and
                self.dino_pos[1] + dino_size[1] > obstacle_pos[1]):
                self.alive = False
                return

def evolve(population):
    # Select the top half of the population based on score
    population.sort(key=lambda x: x.score, reverse=True)
    next_generation = population[:len(population)//2]

    # Generate new agents through crossover and mutation
    while len(next_generation) < len(population):
        parent1, parent2 = random.sample(next_generation, 2)
        child_weights = crossover(parent1.weights, parent2.weights)
        child_weights = mutate(child_weights)
        next_generation.append(DinoAI(child_weights, random.choice(AGENT_COLORS)))

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

def timer(scr,num_agents_left):
     # Render timer text
        timer_text = font.render(f"Timer: {int(scr)} seconds", True, BLACK)
        agents_text = font.render(f"Agents Left: {num_agents_left}", True, BLACK)
        screen.blit(agents_text, (10, 10))
        screen.blit(timer_text, (10, 50))

# Game loop
def main():
    global obstacle_speed
    scr=0
    num_agents = 50
    generations = 100
    population = [DinoAI(color=random.choice(AGENT_COLORS)) for _ in range(num_agents)]

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
                    obstacle_pos = [SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_height]
                    obstacles.append(obstacle_pos)
                    pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000, 2000))

            num_agents_left = sum(agent.alive for agent in population)
            
            for agent in population:
                agent.update(obstacles)
                agent.check_collision(obstacles)

            obstacles = [[x - obstacle_speed, y] for x, y in obstacles if x > -obstacle_width]

            # Increase obstacle speed every 5 seconds
            if current_ticks - last_speed_increase_time >= speed_increase_interval:
                obstacle_speed += 1
                last_speed_increase_time = current_ticks

            # Drawing
            screen.fill(WHITE)

            for agent in population:
                if agent.alive:
                    pygame.draw.rect(screen, agent.color, (agent.dino_pos[0], agent.dino_pos[1], dino_size[0], dino_size[1]))
            for obstacle_pos in obstacles:
                pygame.draw.rect(screen, obstacle_color, (obstacle_pos[0], obstacle_pos[1], obstacle_width, obstacle_height))
            timer(scr,num_agents_left)
            pygame.display.flip()

            clock.tick(FPS)
            scr += 1/FPS
        print(f"Generation {gen + 1} - Max Score: {max(agent.score for agent in population):.2f}")
        population = evolve(population)
        obstacle_speed = base_obstacle_speed  # Reset speed for new generation
        scr=0
    pygame.quit()

if __name__ == "__main__":
    main()