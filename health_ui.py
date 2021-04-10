from pe2 import object


class UI:

    def __init__(self, handler, battle_obj, x_pos, y_pos):
        self.handler = handler
        self.battle_obj = battle_obj

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.ui_base = object.Image(self.handler, "Health UI Base", image_path="healthUI/health_ui.png")
        self.ui_empty = object.Image(self.handler, "Health UI Empty", image_path="healthUI/health_empty.png")
        self.ui_full = object.Image(self.handler, "Health UI Full", image_path="healthUI/health_full.png")

        self.gauge_width = self.ui_full.get_width()

    def rescale(self, width=None, height=None):
        gauge_width = None
        gauge_height = None

        if width:
            gauge_width = round(width * 0.614)
        if height:
            gauge_height = round(height * 0.446)

        self.ui_base.rescale(width, height)
        self.ui_empty.rescale(gauge_width, gauge_height)
        self.ui_full.rescale(gauge_width, gauge_height)

        self.gauge_width = self.ui_full.get_width()

    def draw(self):
        friendly_team = self.battle_obj.friendly_team
        x_pos = self.x_pos
        y_pos = self.y_pos

        count = 0
        for column in friendly_team:
            for character in column:
                if character is not None:
                    count += 1

                    ui_width = self.ui_base.get_width()
                    ui_height = self.ui_base.get_height()

                    self.ui_full.resize(width=self.gauge_width * character.get_p_health())

                    self.ui_base.local_x = x_pos
                    self.ui_base.local_y = y_pos
                    self.ui_empty.local_x = x_pos + ui_width * 0.35
                    self.ui_empty.local_y = y_pos + ui_height * 0.45
                    self.ui_full.local_x = x_pos + ui_width * 0.35
                    self.ui_full.local_y = y_pos + ui_height * 0.45

                    self.ui_full.render()

                    self.ui_base.draw()
                    self.ui_empty.draw()
                    self.ui_full.draw()

                    y_pos += ui_height + 5

                    if count % 3 == 0:
                        y_pos = self.y_pos
                        x_pos += ui_width + 5
