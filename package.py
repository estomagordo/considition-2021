class Package:
    def __init__(self, raw_package):
        self.offsets = {raw_package['id']: (0, 0, 0)}
        self.rotation = 0
        self.dim0 = raw_package['length']
        self.dim1 = raw_package['height']
        self.dim2 = raw_package['width']

    def rotate(self):
        self.rotation = (self.rotation + 1) % 6

    def length(self):
        if self.rotation < 2:
            return self.dim0
        if self.rotation < 4:
            return self.dim1
        return self.dim2

    def height(self):
        if self.rotation in (2, 3):
            return self.dim0
        if self.rotation in (0, 5):
            return self.dim1
        return self.dim2

    def width(self):
        if self.rotation > 3:
            return self.dim0
        if self.rotation in (1, 3):
            return self.dim1
        return self.dim2

    def dimensions(self):
        return [self.length, self.height, self.width]
    
    def try_merge(self, other):
        for rotations in range(6):
            lenmatch = other['length'] == self.length()
            heimatch = other['height'] == self.height()
            widmatch = other['width'] == self.width()

            if lenmatch:
                if heimatch:
                    