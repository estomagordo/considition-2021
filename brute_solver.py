from itertools import permutations
from package import Package

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

    def packager(self, raw_packages):
        packages = list(map(Package, raw_packages))

        if self.weld:
            original_count = len(packages)

            while True:
                to_remove = -1

                for i in range(len(packages)-1):
                    if to_remove != -1:
                        break
                    for j in range(i+1, len(packages)):
                        if packages[i].try_merge(packages[j]):
                            to_remove = j
                            # print('Successfully welded!', i, j, packages[i], packages[j])
                            break

                if to_remove == -1:
                    break

                packages = packages[:to_remove] + packages[to_remove+1:]

            print(f'Welded down from {original_count} to {len(packages)} packages.')

        return packages
    
    def prioritizer(self, package):
        return self.volume_weight * -package.volume() - self.weight_class_weight * (package.weighted_weight_class() +1) - self.order_class_weight * (package.weighted_order_class()+1)

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

    def can_place(self, x, y, z, package):
        xlim = package.length()
        zlim = package.height()
        ylim = package.width()

        for dx in range(xlim):
            for dz in range(zlim):
                for dy in range(ylim):
                    if self.space[x+dx][y+dy][z+dz]:
                        return False

        return True

    def any_floats(self, x, y, z, package):
        for i, p in enumerate(package.packages):
            zlo = p.z1()

            if z+zlo == 0:
                continue

            if i > 0 and any(pack.z1() < zlo for pack in package.packages[:i]):
                continue

            floats = True

            xlo = p.x1()
            xhi = p.x2()
            ylo = p.y1()
            yhi = p.y2()

            for dx in range(x+xlo, x+xhi):
                if not floats:
                    break
                for dy in range(y+ylo, y+yhi):
                    if self.space[dx][dy][z+zlo-1]:
                        floats = False
                        break

            if floats:
                return True

        return False

    def pre_rotate(self, package):
        targetlength = min(package.length(), package.height(), package.width())
        
        while package.length() != targetlength:
            package.rotate()

    def place_package(self, package):
        self.pre_rotate(package)

        for rotation in range(6):
            for x in range(self.vehicle_length+1 - package.length()):
                for z in range(self.vehicle_height+1 - package.height()):                    
                    for y in range(self.vehicle_width+1 - package.width()):
                        if not self.can_place(x, y, z, package):
                            continue
                        
                        if self.any_floats(x, y, z, package):
                            continue
                        
                        for dx in range(package.length()):
                            for dz in range(package.height()):
                                for dy in range(package.width()):
                                    self.space[x+dx][y+dy][z+dz] = True

                        for p in package.packages:
                            x1 = p.x1()
                            x2 = p.x2()
                            y1 = p.y1()
                            y2 = p.y2()
                            z1 = p.z1()
                            z2 = p.z2()
                            weight_class = p.weight_class
                            order_class = p.order_class
                            self.placed_packages.append({'id': p.id, 'x1': x+x1, 'x2': x+x1, 'x3': x+x1, 'x4': x+x1,
                                        'x5': x+x2, 'x6': x+x2, 'x7': x+x2, 'x8': x+x2,
                                        'y1': y+y1, 'y2': y+y1, 'y3': y+y1, 'y4': y+y1,
                                        'y5': y+y2, 'y6': y+y2, 'y7': y+y2, 'y8': y+y2,
                                        'z1': z+z1, 'z2': z+z1, 'z3': z+z1, 'z4': z+z1,
                                        'z5': z+z2, 'z6': z+z2, 'z7': z+z2, 'z8': z+z2, 'weightClass': weight_class, 'orderClass': order_class})

                        return True
            package.rotate()
        return False