class Package:
    def __init__(self, raw_package):
        self.id = raw_package['id']
        self.offsets = [0, 0, 0]
        self.dimensions = [raw_package['length'], raw_package['height'], raw_package['width']]
        self.packages = [self]
        self.rotation = 0
        self.weight_class = raw_package['weightClass']
        self.order_class = raw_package['orderClass']

    def weighted_weight_class(self):
        return self.weight_class

    def weighted_order_class(self):
        return sum(p.order_class for p in self.packages)/len(self.packages)

    def rotate(self):
        for package in self.packages:
            package.rotation = (package.rotation + 1) % 6

    def x1(self):
        if self.rotation in (0, 1):
            return self.offsets[0]
        if self.rotation in (2, 4):
            return self.offsets[1]
        return self.offsets[2]

    def x2(self):
        if self.rotation in (0, 1):
            return self.offsets[0] + self.dimensions[0]
        if self.rotation in (2, 4):
            return self.offsets[1] + self.dimensions[1]
        return self.offsets[2] + self.dimensions[2]

    def y1(self):
        if self.rotation in (4, 5):
            return self.offsets[0]
        if self.rotation in (1, 3):
            return self.offsets[1]
        return self.offsets[2]

    def y2(self):
        if self.rotation in (4, 5):
            return self.offsets[0] + self.dimensions[0]
        if self.rotation in (1, 3):
            return self.offsets[1] + self.dimensions[1]
        return self.offsets[2] + self.dimensions[2]

    def z1(self):
        if self.rotation in (2, 3):
            return self.offsets[0]
        if self.rotation in (0, 5):
            return self.offsets[1]
        return self.offsets[2]

    def z2(self):
        if self.rotation in (2, 3):
            return self.offsets[0] + self.dimensions[0]
        if self.rotation in (0, 5):
            return self.offsets[1] + self.dimensions[1]
        return self.offsets[2] + self.dimensions[2]

    def length(self):
        return max(package.x2() for package in self.packages)

    def height(self):
        return max(package.z2() for package in self.packages)

    def width(self):
        return max(package.y2() for package in self.packages)

    def volume(self):
        return self.length() * self.height() * self.width()

    def rex(self):
        if self.rotation in (0, 1):
            return 0
        if self.rotation in (2, 4):
            return 1
        return 2

    def rez(self):
        if self.rotation in (2, 3):
            return 0
        if self.rotation in (0, 5):
            return 1
        return 2

    def rey(self):
        if self.rotation in (4, 5):
            return 0
        if self.rotation in (1, 3):
            return 1
        return 2
    
    def try_merge(self, other):
        if self.weight_class != other.weight_class:
            return False

        if self.order_class != other.order_class:
            return False

        for rotations in range(6):
            if self.length() == other.length():
                if self.height() == other.height():
                    other.rotation = self.rotation
                    a = [i for i in range(3) if other.dimensions[i] == self.length()][0]
                    b = [i for i in range(3) if other.dimensions[i] == self.height() and i != a][0]
                    c = [i for i in range(3) if i not in (a, b)][0]
                    other.offsets = [other.offsets[a], other.offsets[b], other.offsets[c]+self.width()]
                    other.dimensions = [other.dimensions[a], other.dimensions[b], other.dimensions[c]]
                    self.packages.append(other)
                    return True
                if self.width() == other.width():
                    other.rotation = self.rotation
                    a = [i for i in range(3) if other.dimensions[i] == self.length()][0]
                    c = [i for i in range(3) if other.dimensions[i] == self.width() and i != a][0]
                    b = [i for i in range(3) if i not in (a, c)][0]
                    other.offsets = [other.offsets[a], other.offsets[b]+self.height(), other.offsets[c]]
                    other.dimensions = [other.dimensions[a], other.dimensions[b], other.dimensions[c]]
                    self.packages.append(other)
                    return True
            if self.height() == other.height() and self.width() == other.width():
                other.rotation = self.rotation
                b = [i for i in range(3) if other.dimensions[i] == self.height()][0]
                c = [i for i in range(3) if other.dimensions[i] == self.width() and i != b][0]
                a = [i for i in range(3) if i not in (b, c)][0]
                other.offsets = [other.offsets[a]+self.length(), other.offsets[b], other.offsets[c]]
                other.dimensions = [other.dimensions[a], other.dimensions[b], other.dimensions[c]]
                self.packages.append(other)
                return True

            other.rotate()

        return False

    def __str__(self):
        return f'Ids: {[package.id for package in self.packages]}, length: {self.length()}, height: {self.height()}, width: {self.width()}'

    def __repr__(self):
        return self.__str__()