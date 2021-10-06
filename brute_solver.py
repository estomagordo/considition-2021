from itertools import permutations
from math import e

class BruteSolver:
    def __init__(self, game_info, volume_weight, weight_class_weight, order_class_weight, shake, weld):
        self.vehicle_length = game_info['vehicle']['length']
        self.vehicle_width = game_info['vehicle']['width']
        self.vehicle_height = game_info['vehicle']['height']
        self.volume_weight = volume_weight
        self.weight_class_weight = weight_class_weight
        self.order_class_weight = order_class_weight
        self.shake = shake
        self.weld = weld
        self.reset()        

        self.packages = self.packager(game_info['dimensions'])
        self.packages.sort(key=lambda package: self.prioritizer(package))

    def reset(self):
        self.placed_packages = []
        self.create_space()

    def package(self, raw_package):
        

    def packager(self, raw_packages):

    
    def prioritizer(self, package):
        return self.volume_weight * -package['height'] * package['width'] * package['length'] - self.weight_class_weight * (package['weightClass']+1) - self.order_class_weight * (package['orderClass']+1)

    def create_space(self):
        self.space = []

        for x in range(self.vehicle_length):
            plane = []
            for y in range(self.vehicle_width):
                column = [False for z in range(self.vehicle_height)]
                plane.append(column)
            self.space.append(plane)

    def Solve(self):
        if self.shake:
            for x in range(1, len(self.packages)):
                package_list = list(self.packages)
                package_list[x-1], package_list[x] = package_list[x], package_list[x-1]
                for i, package in enumerate(package_list):
                    if not self.place_package(package):
                        print('TRAGEDY on parcel', i)
                    # print('Placed package', i+1, 'out of', len(self.packages))

                yield self.placed_packages
                self.reset()
        else:
            for i, package in enumerate(self.packages):
                if not self.place_package(package):
                    print('TRAGEDY on parcel', i)
                # print('Placed package', i+1, 'out of', len(self.packages))

            yield self.placed_packages

    def place_package(self, package):
        dimensions = sorted([package['length'], package['height'], package['width']])

        for p in permutations(dimensions):
            for x in range(self.vehicle_length+1 - p[0]):
                for z in range(self.vehicle_height+1 - p[2]):
                    for y in range(self.vehicle_width+1 - p[1]):
                        
                        valid = True

                        for dx in range(p[0]):
                            if not valid:
                                break
                            for dz in range(p[2]):
                                if not valid:
                                    break
                                for dy in range(p[1]):
                                    if self.space[x+dx][y+dy][z+dz]:
                                        valid = False
                                        break

                        if valid:
                            for dx in range(p[0]):
                                for dz in range(p[2]):
                                    for dy in range(p[1]):
                                        self.space[x+dx][y+dy][z+dz] = True

                            self.placed_packages.append({'id': package['id'], 'x1': x, 'x2': x, 'x3': x, 'x4': x,
                                        'x5': x + p[0], 'x6': x + p[0], 'x7': x + p[0], 'x8': x + p[0],
                                        'y1': y, 'y2': y, 'y3': y, 'y4': y,
                                        'y5': y + p[1], 'y6': y + p[1], 'y7': y + p[1], 'y8': y + p[1],
                                        'z1': z, 'z2': z, 'z3': z, 'z4': z,
                                        'z5': z + p[2], 'z6': z + p[2], 'z7': z + p[2], 'z8': z + p[2], 'weightClass': package['weightClass'], 'orderClass': package['orderClass']})

                            return True
        return False