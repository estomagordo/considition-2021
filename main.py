from greedy_solver_copy import GreedySolver
import api
import json

api_key = ""

with open('secret') as f:
	api_key = f.readline().rstrip()

# The different map names can be found on considition.com/rules
# TODO: You map choice here. Unless changed, the map "training1" will be selected.
map_name = "training1"


def main():
	print("Starting game...")
	response = api.new_game(api_key, map_name)
	greedy = GreedySolver(game_info=response)
	solution = greedy.Solve()
	submit_game_response = api.submit_game(api_key, map_name, solution)
	print(submit_game_response)
if __name__ == "__main__":
    main()
