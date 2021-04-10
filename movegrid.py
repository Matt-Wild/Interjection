from pe2 import object


class Movegrid:

    def __init__(self, handler, tile_size, x, y):
        self.handler = handler
        self.movegrid = []

        x_pos = x
        for i in range(3):
            column = []
            y_pos = y

            for j in range(3):
                tile = object.Image(handler, f"Movegrid {i} {j}", image_path="movementGrid/grid_tile.png", x=x_pos, y=y_pos)
                tile.rescale(width=tile_size, height=tile_size)
                column.append(tile)

                y_pos += tile_size

            self.movegrid.append(column)
            x_pos += tile_size

    def update(self):
        for column in self.movegrid:
            for tile in column:
                tile.update()

    def draw(self):
        for column in self.movegrid:
            for tile in column:
                tile.draw()
