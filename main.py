import pygame as pg
import sys
from game_objects import BallObj, PaddleObj
import neat
import os

# config window
pg.init()
clock = pg.time.Clock()

size = (800, 600)

bg_color = pg.Color('grey12')

screen = pg.display.set_mode(size)
pg.display.set_caption('Pong')


def train_genome(genomes, config):
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # paddle object that uses that network to play
    nets = []
    ge = []
    paddles = []
    balls = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        balls.append(BallObj.Ball(size, size[0] / 2, size[1] / 2))
        paddles.append(PaddleObj.Paddle(size, size[0] / 2, size[1]))
        ge.append(genome)

    while True and len(paddles) > 0:
        screen.fill(bg_color)

        # Handle input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        for i, paddle in enumerate(paddles):

            if balls[i].body.bottom == paddle.body.top and (
                    balls[i].body.right >= paddle.body.left and balls[i].body.left <= paddle.body.right):
                ge[i].fitness += 1
            if balls[i].body.top >= paddle.body.bottom:
                ge[i].fitness -= 1

            output = nets[i].activate((paddle.body.x, balls[i].body.x, balls[i].body.y, balls[i].speed_x))

            if output[0] > 0.5:
                paddle.movement(1)
            if output[1] > 0.5:
                paddle.movement(-1)
            if output[2] > 0.5:
                paddle.movement(0)

            paddle.update()
            balls[i].update(paddle)
            paddle.draw(screen)
            balls[i].draw(screen)

            if not paddle.alive:
                paddles.remove(paddle)
                balls.remove(balls[i])
                nets.remove(nets[i])
                ge.remove(ge[i])

        # Update the window
        pg.display.flip()
        clock.tick(60)
        # print(clock.get_fps())


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 10 generations.
    winner = p.run(train_genome, 10)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # set path to neat
    local_dir = os.path.dirname(__file__)
    config_path = local_dir + '/neat_config'
    run(config_path)
