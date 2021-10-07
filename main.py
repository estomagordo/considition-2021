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
		volume_weight = rand.gauss(0.90, 0.29)
		weight_class_weight = rand.gauss(13437.0, 2821.0)
		order_class_weight = rand.gauss(9969.0, 2112.0)
		volume_weight = 0.8166920792716333
		weight_class_weight = 15736.434985654178
		order_class_weight = 10522.958876387987
		print(f'iteration: {iteration+1}/{times} after {round(time()-t, 3)} seconds, with volume weight: {volume_weight}, weight class weight: {weight_class_weight}, order class weight: {order_class_weight}')
		print(bestfor)

		for map_name in maps:
			response = api.new_game(api_key, map_name)
			solver = BruteSolver(response, volume_weight, weight_class_weight, order_class_weight, shake, weld)
			for solution in solver.Solve():
				print(solution)
				submit_game_response = api.submit_game(api_key, map_name, solution)
				bestfor[map_name] = max(bestfor[map_name], submit_game_response['score'])
				print(map_name, submit_game_response)

if __name__ == "__main__":
    main()
