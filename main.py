import api

from brute_solver import BruteSolver
from greedy_solver_copy import GreedySolver
from random import Random
from sys import argv

api_key = ""

with open('secret') as f:
	api_key = f.readline().rstrip()


def main():
	rand = Random()
	times = int(argv[1])

	for iteration in range(times):
		area_weight = rand.gauss(1.0, 0.2)
		weight_class_weight = rand.gauss(500.0, 125.0)
		order_class_weight = rand.gauss(150.0, 35.0)
		print(f'iteration: {iteration+1} out of {times} with area weight: {area_weight}, weight class weight: {weight_class_weight}, order class weight: {order_class_weight}')
		for map_name in ('training1', 'training2'):
			response = api.new_game(api_key, map_name)
			solver = BruteSolver(response, area_weight, weight_class_weight, order_class_weight)
			solution = solver.Solve()
			submit_game_response = api.submit_game(api_key, map_name, solution)
			print(map_name, submit_game_response)

if __name__ == "__main__":
    main()
