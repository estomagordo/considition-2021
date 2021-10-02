from itertools import permutations

class BruteSolver:
    placed_packages = []

    def __init__(self, game_info):
        self.vehicle_length = game_info['vehicle']['length']
        self.vehicle_width = game_info['vehicle']['width']
        self.vehicle_height = game_info['vehicle']['height']
        self.packages = sorted(game_info['dimensions'], key=lambda package: [-package['height'] * package['width'], -package['weightClass'], -package['orderClass']])
        
        self.create_space()

    def create_space(self):
        self.space = []

        for x in range(self.vehicle_length):
            plane = []
            for y in range(self.vehicle_width):
                column = [False for z in range(self.vehicle_height)]
                plane.append(column)
            self.space.append(plane)

    def Solve(self):
        for i, package in enumerate(self.packages):
            if not self.place_package(package):
                print('TRAGEDY on parcel', i)
            print('Placed package', i+1, 'out of', len(self.packages))

        return self.placed_packages

    def place_package(self, package):
        dimensions = sorted([package['length'], package['width'], package['height']])

        for p in permutations(dimensions):
            for x in range(self.vehicle_length - p[0]):
                for y in range(self.vehicle_width - p[1]):
                    for z in range(self.vehicle_height - p[2]):
                        
                        valid = True

                        for dx in range(p[0]):
                            if not valid:
                                break
                            for dy in range(p[1]):
                                if not valid:
                                    break
                                for dz in range(p[2]):
                                    if self.space[x+dx][y+dy][z+dz]:
                                        valid = False
                                        break

                        if valid:
                            for dx in range(p[0]):
                                for dy in range(p[1]):
                                    for dz in range(p[2]):
                                        self.space[x+dx][y+dy][z+dz] = True

                            self.placed_packages.append({'id': package['id'], 'x1': x, 'x2': x, 'x3': x, 'x4': x,
                                        'x5': x + p[0], 'x6': x + p[0], 'x7': x + p[0], 'x8': x + p[0],
                                        'y1': y, 'y2': y, 'y3': y, 'y4': y,
                                        'y5': y + p[1], 'y6': y + p[1], 'y7': y + p[1], 'y8': y + p[1],
                                        'z1': z, 'z2': z, 'z3': z, 'z4': z,
                                        'z5': z + p[2], 'z6': z + p[2], 'z7': z + p[2], 'z8': z + p[2], 'weightClass': package['weightClass'], 'orderClass': package['orderClass']})

                            return True
        return False