from draw import Plane
from ga import GA
import argparse
import pygame

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=300, help='Number of equal incumbents before stopping.')
    parser.add_argument('--mu', type=int, default=100, help='Population size.')
    parser.add_argument('--pc', type=float, default=0.2, help='Crossover rate.')
    parser.add_argument('--pm', type=float, default=0.02, help='Permutation rate.')
    args = parser.parse_args()
    if 0 >= args.pc >= 1 or 0 >= args.pm:
        raise argparse.ArgumentTypeError('Crossover/permutation rate should be between 0 and 1.')

    plane = Plane()
    plane.draw_pixels()
    ga = GA(plane.cities, plane.city_count, plane.draw_route, args.mu, args.pc, args.pm)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if ga.equal_count < args.n:
            ga.optimize()
        elif ga.equal_count == args.n:
            ga.incumbent()
            ga.equal_count += 1
