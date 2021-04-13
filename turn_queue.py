from pe2 import object


class TurnQueue:

    def __init__(self, handler, turn_queue):
        self.handler = handler
        self.turn_queue = turn_queue

        self.next_turn_image = object.Image(handler, "Next Turn Image", image_path="turnQueue/turn_tab_1.png")
        self.turn_queue_image = object.Image(handler, "Turn Queue Image", image_path="turnQueue/turn_tab_2.png")
        self.next_turn_image.rescale_pwidth(0.071)
        self.turn_queue_image.rescale_pwidth(0.032)

        self.next_turn_image.set_px(0.34)

    def draw(self):
        x_pos = self.next_turn_image.local_x

        x_increase = self.turn_queue_image.get_width() + 20
        icon_dif = self.turn_queue_image.get_width() // 40
        icon_large_dif = self.next_turn_image.get_width() // 40

        icon_large = self.turn_queue[0].icon_large
        icon_large.local_x = x_pos + icon_large_dif
        icon_large.local_y = 0

        self.next_turn_image.draw()

        icon_large.draw()

        x_pos += self.next_turn_image.get_width() + 30

        for i in range(5):
            icon = self.turn_queue[i + 1].icon
            icon.local_x = x_pos + icon_dif
            icon.local_y = 0

            self.turn_queue_image.local_x = x_pos
            self.turn_queue_image.draw()

            icon.draw()

            x_pos += x_increase
