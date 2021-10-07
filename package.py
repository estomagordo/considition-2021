# For now: Only allow welding two packages together.

class Package:
    def __init__(self, raw_package):
        self.offsets = [[raw_package['id'], 0, 0, 0, raw_package['length'], raw_package['height'], raw_package['width'], raw_package['weightClass'], raw_package['orderClass']]]
        self.rotation = 0
        self.weight_class = raw_package['weightClass']
        self.order_class = raw_package['orderClass']

    def dimensions(self):
        return self.offsets[-1][4:]

    def rotate(self):
        self.rotation = (self.rotation + 1) % 6

    def length(self):
        if self.rotation < 2:
            return self.dimensions()[0]
        if self.rotation < 4:
            return self.dimensions()[1]
        return self.dimensions()[2]

    def height(self):
        if self.rotation in (2, 3):
            return self.dimensions()[0]
        if self.rotation in (0, 5):
            return self.dimensions()[1]
        return self.dimensions()[2]

    def width(self):
        if self.rotation > 3:
            return self.dimensions()[0]
        if self.rotation in (1, 3):
            return self.dimensions()[1]
        return self.dimensions()[2]

    def volume(self):
        return self.length() * self.height() * self.width()
    
    def try_merge(self, other):
        if len(self.offsets) > 1:
            return False

        if len(other.offsets) > 1:
            return False

        other_weight_class = other.offsets[0][-2]
        other_order_class = other.offsets[0][-1]

        for rotations in range(6):
            if self.length() == other.length():
                if self.height() == other.height():
                    self.offsets.append([other.offsets[0][0], 0, 0, self.width(), self.length(), self.height(), self.width()+other.width(), other_weight_class, other_order_class])
                    return True
                if self.width() == other.width():
                    self.offsets.append([other.offsets[0][0], 0, self.height(), 0, self.length(), self.height()+other.height(), self.width(), other_weight_class, other_order_class])
                    return True
            if self.height() == other.height() and self.width() == other.width():
                self.offsets.append([other.offsets[0][0], self.length(), 0, 0, self.length()+other.length(), self.height(), self.width(), other_weight_class, other_order_class])
                return True

            other.rotate()

        return False

    def __str__(self):
        return f'Ids: {[offset[0] for offset in self.offsets]}, length: {self.length()}, height: {self.height()}, width: {self.width()}'