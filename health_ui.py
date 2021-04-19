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

        self.character_names = []
        self.names_generated = False

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
        self.generate_names()

    def generate_names(self):
        self.names_generated = True

        self.character_names = []
        friendly_team = self.battle_obj.friendly_team

        count = 0
        try:
            for column in friendly_team:
                for character in column:
                    if character is not None:
                        count += 1

                        name = object.Text(self.handler, f"Health UI Text {count}", font="Arial", text=character.name.upper(), width=(0.579 * self.ui_base.get_width()), height=(0.32 * self.ui_base.get_height()))
                        self.character_names.append(name)
        except TypeError:
            self.names_generated = False

    def draw(self):
        if not self.names_generated:
            self.generate_names()

        friendly_team = self.battle_obj.friendly_team
        x_pos = self.x_pos
        y_pos = self.y_pos

        index_x, index_y = self.battle_obj.get_friendly_grid_selection()
        if index_x is not None and index_y is not None:
            character = friendly_team[index_x][index_y]

            if character:
                ui_width = self.ui_base.get_width()
                ui_height = self.ui_base.get_height()

                self.ui_full.resize(width=self.gauge_width * character.get_p_health())

                self.ui_base.local_x = x_pos
                self.ui_base.local_y = y_pos
                self.ui_empty.local_x = x_pos + ui_width * 0.35
                self.ui_empty.local_y = y_pos + ui_height * 0.45
                self.ui_full.local_x = x_pos + ui_width * 0.35
                self.ui_full.local_y = y_pos + ui_height * 0.45

                nametag = self.get_nametag(character.name)
                nametag.local_x = x_pos + ui_width * 0.35
                nametag.local_y = y_pos

                icon = character.icon
                icon.local_x = x_pos + ui_width * 0.05
                icon.local_y = y_pos + ui_height * 0.3

                self.ui_full.render()

                self.ui_base.draw()
                self.ui_empty.draw()
                self.ui_full.draw()
                nametag.draw()
                icon.draw()

    def get_nametag(self, name):
        for nametag in self.character_names:
            if nametag.text == name.upper():
                return nametag
        return None
