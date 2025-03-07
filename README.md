# Neural Ninja

Neural Ninja is a side-scrolling AI-based game built with Pygame, where AI-controlled ninja agents learn to jump over obstacles using a neural network and evolutionary algorithms.

## Features
- AI-controlled ninjas learn to jump over obstacles.
- Uses a simple neural network for decision-making.
- Implements genetic algorithms for evolving better-performing ninjas.
- Animated ninja sprites with smooth movements.
- Dynamic obstacle spawning and increasing difficulty over time.
- Background scrolling effect for immersive gameplay.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/sachinsonii/Neural_Ninja.git
   cd Neural_Ninja
   ```
2. Install dependencies:
   ```sh
   pip install pygame numpy
   ```
3. Run the game:
   ```sh
   python main.py
   ```

## Controls
- The game is fully automated. AI ninjas learn and improve through evolution.
- Press **R** to restart when the game is over.
- Press **ESC** to quit.

## How It Works
- Each ninja agent is controlled by a neural network with randomly initialized weights.
- The network takes inputs such as distance to the next obstacle, obstacle height, and speed.
- A decision is made based on the network's output to determine if the ninja should jump.
- After each generation, ninjas with the best scores survive, reproduce, and pass their traits to the next generation with mutations.

## Evolutionary Algorithm
- **Selection:** The top-performing ninjas are selected based on their survival time.
- **Crossover:** Offspring inherit weights from two parents.
- **Mutation:** A small random mutation is applied to some weights to introduce variety.
- **Next Generation:** The new population replaces the old one, repeating the cycle.

## Assets
- Sprites and background images are stored in the `Assets/` folder.
- Sound effects (jump sounds) are loaded from the `Assets/` folder.

## Future Enhancements
- Implement more complex neural networks with deeper layers.
- Add more environmental challenges like moving obstacles.
- Improve visuals with smoother animations and particle effects.
- Implement a leaderboard to track the highest-performing ninjas.

## License
This project is licensed under the MIT License.

