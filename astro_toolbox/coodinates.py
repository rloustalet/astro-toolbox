import numpy as np
class Equatorial():
    def __init__(self, alpha, delta):
        self.alpha = alpha
        self.delta = delta
    def __repr__(self):
        return (f'\N{GREEK SMALL LETTER ALPHA} = {self.alpha}, \N{GREEK SMALL LETTER DELTA} = {self.delta}')
    def get_hourangle(self, gamma):
        return gamma - self.alpha
    def to_horizontal(self):
        HA = self.get_hourangle()
        h = np.arcsin()