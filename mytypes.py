from overlay_lib import Vector2D

class Coord(Vector2D):
    x: int
    y: int
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other: int) -> Vector2D:
        self.x += other
        self.y += other
        return Vector2D(self.x, self.y)

    def __sub__(self, other: int):
        return self.__add__(-other)

    def __repr__(self) -> str:
         return f"Coord(x={self.x}, y={self.y})"

# this should be illegal. like the FBI arrests you for it illegal
coord = Coord(1,2)
vector = coord - 2
print(coord)
print(vector)
