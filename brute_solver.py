class BruteSolver:
    placed_packages = []

    def __init__(self, game_info):
        self.vehicle_length = game_info['vehicle']['length']
        self.vehicle_width = game_info['vehicle']['width']
        self.vehicle_height = game_info['vehicle']['height']
        self.packages = game_info['dimensions']
        
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
        for i, package in enumerate(self.packages()):
            if not self.place_package(package):
                print('TRAGEDY on parcel', i)

        return self.placed_packages

    def place_package(self, package):
        for x in range(self.vehicle_length - package['length']):
            for y in range(self.vehicle_width - package['width']):
                for z in range(self.vehicle_height - package['height']):
                    
                    valid = True

                    for dx in range(package['length']):
                        if not valid:
                            break
                        for dy in range(package['width']):
                            if not valid:
                                break
                            for dz in range(package['height']):
                                if self.space[x+dx][y+dy][z+dz]:
                                    valid = False
                                    break

                    if valid:
                        self.placed_packages.append({'id': package['id'], 'x1': x, 'x2': x, 'x3': x, 'x4': x,
                                    'x5': x + package['length'], 'x6': x + package['length'], 'x7': x + package['length'], 'x8': x + package['length'],
                                    'y1': y, 'y2': y, 'y3': y, 'y4': y,
                                    'y5': y + package['width'], 'y6': y + package['width'], 'y7': y + package['width'], 'y8': y + package['width'],
                                    'z1': z, 'z2': z, 'z3': z, 'z4': z,
                                    'z5': z + package['height'], 'z6': z + package['height'], 'z7': z + package['height'], 'z8': z + package['height'], 'weightClass': package['weightClass'], 'orderClass': package['orderClass']})

                        return True
        return False