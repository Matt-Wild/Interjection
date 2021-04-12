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

        self.next_turn_image.draw()

        x_pos += self.next_turn_image.get_width() + 30

        for i in range(5):
            self.turn_queue_image.local_x = x_pos
            self.turn_queue_image.draw()

            x_pos += x_increase
