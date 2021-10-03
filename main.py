import api

from brute_solver import BruteSolver
from collections import defaultdict
from greedy_solver_copy import GreedySolver
from random import Random, shuffle
from sys import argv
from time import time

api_key = ""

with open('secret') as f:
	api_key = f.readline().rstrip()


def main():
	t = time()
	rand = Random()
	times = int(argv[1])
	maps = argv[2:]
	bestfor = defaultdict(int)

	for iteration in range(times):
		area_weight = rand.gauss(0.91, 0.04)
		weight_class_weight = rand.gauss(438.0, 25.0)
		order_class_weight = rand.gauss(567.0, 15.0)
		print(f'iteration: {iteration+1}/{times} after {round(time()-t, 3)} seconds, with area weight: {area_weight}, weight class weight: {weight_class_weight}, order class weight: {order_class_weight}')
		print(bestfor)

		for map_name in maps:
			response = api.new_game(api_key, map_name)
			solver = BruteSolver(response, area_weight, weight_class_weight, order_class_weight)
			solution = solver.Solve()
			submit_game_response = api.submit_game(api_key, map_name, solution)
			bestfor[map_name] = max(bestfor[map_name], submit_game_response['score'])
			print(map_name, submit_game_response)

if __name__ == "__main__":
    main()
