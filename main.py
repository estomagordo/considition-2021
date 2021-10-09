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
	maps = argv[2:-2]
	weld = argv[-2] == 'weld'
	shake = argv[-1] == 'shake'
	bestfor = defaultdict(int)

	for iteration in range(times):
		volume_weight = rand.gauss(0.96, 0.29)
		weight_class_weight = rand.gauss(23437.0, 4621.0)
		order_class_weight = rand.gauss(23969.0, 5612.0)
		volume_weight = 0.920933831169626
		weight_class_weight = 20950.389095089384
		order_class_weight = 20295.98922990018
		print(f'iteration: {iteration+1}/{times} after {round(time()-t, 3)} seconds, with volume weight: {volume_weight}, weight class weight: {weight_class_weight}, order class weight: {order_class_weight}')
		print(bestfor)

		for map_name in maps:
			response = api.new_game(api_key, map_name)
			solver = BruteSolver(response, volume_weight, weight_class_weight, order_class_weight, shake, weld)
			for solution in solver.Solve():
				submit_game_response = api.submit_game(api_key, map_name, solution)
				bestfor[map_name] = max(bestfor[map_name], submit_game_response['score'])
				print(map_name, submit_game_response)

if __name__ == "__main__":
    main()
