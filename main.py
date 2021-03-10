import pygame

from pe2 import utils
from pe2 import handler
from pe2 import runner
from pe2 import object
from pe2 import complex
from pe2 import sound

import player_data

hover_sound = sound.new("main_menu_select.wav")
confirm_sound = sound.new("main_menu_confirm.wav")
hover_sound.set_volume(0.2)
confirm_sound.set_volume(0.2)


class StateManager:

    def __init__(self):
        self.main_menu = MainMenu()
        self.battle = Battle()

        self.states = [self.main_menu, self.battle]

        # Game states:
        # 0 - Main Menu
        # 1 - Battle
        self.state = 0

        self.main_menu.start_process()

    def process(self):

        process = self.states[self.state].run()
        if process != self.state:
            self.state = process
            self.states[self.state].start_process()


class Battle:

    def __init__(self):
        self.grid = object.Image(handler, "Battle Grid", image_path="test_grid.png")
        self.grid.rescale_pwidth(0.98)
        self.grid.set_px(0.5)
        self.grid.set_py(0.5)

        self.friendly_tiles = []
        self.hostile_tiles = []
        self.create_tiles()

        self.friendly_team = None

        button_y = self.grid.get_bottom_y() + 10

        self.battle_passive = object.Image(handler, "Battle Button Passive", image_path="battleButtons/battle_button_[unhovered-selected1-denied1].png", y=button_y)
        self.battle_hovered = object.Animation(handler, "Battle Button Hovered", frame_paths=("battleButtons/battle_button_[hovered1].png", "battleButtons/battle_button_[hovered2].png", "battleButtons/battle_button_[hovered3].png", "battleButtons/battle_button_[hovered4].png", "battleButtons/battle_button_[hovered5].png"), y=button_y)
        self.battle_selected = object.Animation(handler, "Battle Button Selected", frame_paths=("battleButtons/battle_button_[unhovered-selected1-denied1].png", "battleButtons/battle_button_[selected2].png", "battleButtons/battle_button_[selected3].png"), y=button_y, repeat=False)
        self.battle_button = complex.Button("Battle Button", self.battle_passive, self.battle_hovered, self.battle_selected)
        self.battle_passive.rescale_pwidth(0.2)
        self.battle_hovered.rescale_pwidth(0.2)
        self.battle_selected.rescale_pwidth(0.2)
        self.battle_passive.set_px(0.17)
        self.battle_hovered.set_px(0.17)
        self.battle_selected.set_px(0.17)

        self.move_passive = object.Image(handler, "Move Button Passive", image_path="battleButtons/move_button_[unhovered-selected1-denied1].png", y=button_y)
        self.move_hovered = object.Animation(handler, "Move Button Hovered", frame_paths=("battleButtons/move_button_[hovered1].png", "battleButtons/move_button_[hovered2].png", "battleButtons/move_button_[hovered3].png", "battleButtons/move_button_[hovered4].png", "battleButtons/move_button_[hovered5].png"), y=button_y)
        self.move_selected = object.Animation(handler, "Move Button Selected", frame_paths=("battleButtons/move_button_[unhovered-selected1-denied1].png", "battleButtons/move_button_[selected2].png", "battleButtons/move_button_[selected3].png"), y=button_y, repeat=False)
        self.move_button = complex.Button("Move Button", self.move_passive, self.move_hovered, self.move_selected)
        self.move_passive.rescale_pwidth(0.2)
        self.move_hovered.rescale_pwidth(0.2)
        self.move_selected.rescale_pwidth(0.2)
        self.move_passive.set_px(0.5)
        self.move_hovered.set_px(0.5)
        self.move_selected.set_px(0.5)

        self.menu_passive = object.Image(handler, "Menu Button Passive", image_path="battleButtons/menu_button_[unhovered-selected1-denied1].png", y=button_y)
        self.menu_hovered = object.Animation(handler, "Menu Button Hovered", frame_paths=("battleButtons/menu_button_[hovered1].png", "battleButtons/menu_button_[hovered2].png", "battleButtons/menu_button_[hovered3].png", "battleButtons/menu_button_[hovered4].png", "battleButtons/menu_button_[hovered5].png"), y=button_y)
        self.menu_selected = object.Animation(handler, "Menu Button Selected", frame_paths=("battleButtons/menu_button_[unhovered-selected1-denied1].png", "battleButtons/menu_button_[selected2].png", "battleButtons/menu_button_[selected3].png"), y=button_y, repeat=False)
        self.menu_button = complex.Button("Menu Button", self.menu_passive, self.menu_hovered, self.menu_selected)
        self.menu_passive.rescale_pwidth(0.2)
        self.menu_hovered.rescale_pwidth(0.2)
        self.menu_selected.rescale_pwidth(0.2)
        self.menu_passive.set_px(0.83)
        self.menu_hovered.set_px(0.83)
        self.menu_selected.set_px(0.83)

        move_bottom = self.move_passive.get_bottom_y()
        movegrid_height = handler.window.get_size()[1] - move_bottom - 10

        self.movegrid_blank = object.Image(handler, "Move Grid Blank", image_path="movementGrid/movement_grid_tab_[default_empty].png", y=move_bottom)
        self.movegrid_blank.rescale(height=movegrid_height)
        self.movegrid_blank.set_px(0.5)

    def start_process(self):
        runner.clear_update_queue()
        runner.clear_draw_queue()

        self.friendly_team = PD.team_layout

        self.reset_buttons()

        runner.append_to_update_queue((self.grid, self.battle_button, self.move_button, self.menu_button))
        runner.append_to_draw_queue((self.grid, self.battle_button, self.move_button, self.menu_button))

        self.pass_tiles_to_runner()
        self.configure_friendly_team()

    def run(self):
        window.fill((0, 0, 0))

        if self.battle_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.battle_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.move_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.move_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.menu_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.menu_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.battle_button.trigger_disabled:
            self.battle_selected.set_frame(0)
            self.battle_selected.paused = False

        if self.move_button.trigger_disabled:
            self.move_selected.set_frame(0)
            self.move_selected.paused = False
            self.disable_movegrid()

        if self.menu_button.trigger_disabled:
            self.menu_selected.set_frame(0)
            self.menu_selected.paused = False

        if self.battle_button.trigger_enabled:
            confirm_sound.play()
        if self.move_button.trigger_enabled:
            confirm_sound.play()
            self.enable_movegrid()
        if self.menu_button.trigger_enabled:
            confirm_sound.play()
            return 0

        return 1

    def configure_friendly_team(self):
        self.rescale_friendly_team()

        self.reposition_friendly_team()

        self.runner_refresh_friendly_team()

    def reposition_friendly_team(self):
        for column in range(3):
            x = self.friendly_tiles[column][0].passive_state.get_x() + self.friendly_tiles[column][0].passive_state.get_width() // 3
            for row in range(3):
                character = self.friendly_team[column][row]
                if character is not None:
                    y = self.friendly_tiles[column][row].passive_state.get_y() + self.friendly_tiles[column][row].passive_state.get_height() // 2 - character.passive_state.get_height()
                    character.set_local_pos(x, y)

    def rescale_friendly_team(self):
        for column in self.friendly_team:
            for character in column:
                if character is not None:
                    character.rescale(width=self.friendly_tiles[0][0].passive_state.get_width() // 3)

    def runner_remove_friendly_team(self):
        for column in self.friendly_team:
            for character in column:
                if character is not None:
                    runner.remove_from_update_queue(character)
                    runner.remove_from_draw_queue(character)

    def runner_add_friendly_team(self):
        for i in range(3):
            for j in range(3):
                if self.friendly_team[j][i] is not None:
                    runner.append_to_update_queue(self.friendly_team[j][i])
                    runner.append_to_draw_queue(self.friendly_team[j][i])

    def runner_refresh_friendly_team(self):
        self.runner_remove_friendly_team()
        self.runner_add_friendly_team()

    def create_tiles(self):
        self.friendly_tiles = []
        self.hostile_tiles = []

        tile_width = self.grid.get_width() / 6
        tile_height = self.grid.get_height() / 3
        tile_x = self.grid.get_x()
        tile_y = self.grid.get_y()
        for x in range(3):
            row = []
            for y in range(3):
                name = "Friendly Tile " + str(x) + " " + str(y)

                passive = object.Object(handler, name + " Passive", width=tile_width, height=tile_height, x=tile_x + (x * tile_width), y=tile_y + (y * tile_height))
                hovered = object.Rect(handler, name + " Hovered", width=tile_width, height=tile_height, x=tile_x + (x * tile_width), y=tile_y + (y * tile_height), colour=(255, 255, 255), alpha=100)
                active = object.Rect(handler, name + " Active", width=tile_width, height=tile_height, x=tile_x + (x * tile_width), y=tile_y + (y * tile_height), colour=(0, 255, 255), alpha=100)

                button = complex.Button(name, passive, hovered, active)
                row.append(button)
            self.friendly_tiles.append(row)

        tile_x = self.grid.get_x() + self.grid.get_width() / 2
        tile_y = self.grid.get_y()
        for x in range(3):
            row = []
            for y in range(3):
                name = "Hostile Tile " + str(x) + " " + str(y)

                passive = object.Object(handler, name + " Passive", width=tile_width, height=tile_height, x=tile_x + (x * tile_width), y=tile_y + (y * tile_height))
                hovered = object.Rect(handler, name + " Hovered", width=tile_width, height=tile_height, x=tile_x + (x * tile_width), y=tile_y + (y * tile_height), colour=(255, 100, 100), alpha=100)
                active = object.Rect(handler, name + " Active", width=tile_width, height=tile_height, x=tile_x + (x * tile_width), y=tile_y + (y * tile_height), colour=(255, 50, 50), alpha=100)

                button = complex.Button(name, passive, hovered, active)
                row.append(button)
            self.hostile_tiles.append(row)

    def pass_tiles_to_runner(self):
        for row in self.friendly_tiles:
            for tile in row:
                runner.append_to_update_queue(tile)
                runner.append_to_draw_queue(tile)

        for row in self.hostile_tiles:
            for tile in row:
                runner.append_to_update_queue(tile)
                runner.append_to_draw_queue(tile)

    def reset_buttons(self):
        self.battle_button.enabled = False
        self.move_button.enabled = False
        self.menu_button.enabled = False

    def enable_movegrid(self):
        runner.append_to_update_queue(self.movegrid_blank)
        runner.append_to_draw_queue(self.movegrid_blank)

    def disable_movegrid(self):
        runner.remove_from_update_queue(self.movegrid_blank)
        runner.remove_from_draw_queue(self.movegrid_blank)


class MainMenu:

    def __init__(self):
        self.title = object.Animation(handler, "Title", frame_delay=8, frame_paths=("title/title_1.png", "title/title_1_2.png", "title/title_1_3.png", "title/title_1_4.png", "title/title_1_5.png", "title/title_1_6.png", "title/title_1_7.png", "title/title_1_8.png", "title/title_1_9.png", "title/title_1_10.png", "title/title_1_11.png", "title/title_1_10.png", "title/title_1_9.png", "title/title_1_8.png", "title/title_1_7.png", "title/title_1_6.png", "title/title_1_5.png", "title/title_1_4.png", "title/title_1_3.png", "title/title_1_2.png"))
        self.title.rescale_pwidth(0.6)
        self.title.set_px(0.5)

        self.title_pulse = object.Animation(handler, "Title Pulse", frame_delay=8, frame_paths=("title/title_1.png", "title/title_1_2.png", "title/title_1_3.png", "title/title_1_4.png", "title/title_1_5.png", "title/title_1_6.png", "title/title_1_7.png", "title/title_1_8.png", "title/title_1_9.png", "title/title_1_10.png", "title/title_1_11.png", "title/title_1_10.png", "title/title_1_9.png", "title/title_1_8.png", "title/title_1_7.png", "title/title_1_6.png", "title/title_1_5.png", "title/title_1_4.png", "title/title_1_3.png", "title/title_1_2.png"))
        self.title_pulse.rescale_pwidth(0.62)
        self.title_pulse.set_px(0.5)

        self.title_pulse_down_1 = object.Animation(handler, "Title Pulse Down 1", frame_delay=8, frame_paths=("title/title_1.png", "title/title_1_2.png", "title/title_1_3.png", "title/title_1_4.png", "title/title_1_5.png", "title/title_1_6.png", "title/title_1_7.png", "title/title_1_8.png", "title/title_1_9.png", "title/title_1_10.png", "title/title_1_11.png", "title/title_1_10.png", "title/title_1_9.png", "title/title_1_8.png", "title/title_1_7.png", "title/title_1_6.png", "title/title_1_5.png", "title/title_1_4.png", "title/title_1_3.png", "title/title_1_2.png"))
        self.title_pulse_down_1.rescale_pwidth(0.615)
        self.title_pulse_down_1.set_px(0.5)

        self.title_pulse_down_2 = object.Animation(handler, "Title Pulse Down 2", frame_delay=8, frame_paths=("title/title_1.png", "title/title_1_2.png", "title/title_1_3.png", "title/title_1_4.png", "title/title_1_5.png", "title/title_1_6.png", "title/title_1_7.png", "title/title_1_8.png", "title/title_1_9.png", "title/title_1_10.png", "title/title_1_11.png", "title/title_1_10.png", "title/title_1_9.png", "title/title_1_8.png", "title/title_1_7.png", "title/title_1_6.png", "title/title_1_5.png", "title/title_1_4.png", "title/title_1_3.png", "title/title_1_2.png"))
        self.title_pulse_down_2.rescale_pwidth(0.61)
        self.title_pulse_down_2.set_px(0.5)

        self.title_pulse_down_3 = object.Animation(handler, "Title Pulse Down 3", frame_delay=8, frame_paths=("title/title_1.png", "title/title_1_2.png", "title/title_1_3.png", "title/title_1_4.png", "title/title_1_5.png", "title/title_1_6.png", "title/title_1_7.png", "title/title_1_8.png", "title/title_1_9.png", "title/title_1_10.png", "title/title_1_11.png", "title/title_1_10.png", "title/title_1_9.png", "title/title_1_8.png", "title/title_1_7.png", "title/title_1_6.png", "title/title_1_5.png", "title/title_1_4.png", "title/title_1_3.png", "title/title_1_2.png"))
        self.title_pulse_down_3.rescale_pwidth(0.605)
        self.title_pulse_down_3.set_px(0.5)

        self.exit_passive = object.Image(handler, "Exit Button Passive", image_path="exit_option_unselected.png", alpha=150)
        self.exit_hovered = object.Animation(handler, "Exit Button Hovered", frame_paths=("exit_option_selection_1.png", "exit_option_selection_2.png", "exit_option_selection_3.png", "exit_option_selection_2.png"))
        self.exit_active = object.Image(handler, "Exit Button Active", image_path="exit_option_unselected.png")
        self.exit_button = complex.Button("Exit Button", self.exit_passive, self.exit_hovered, self.exit_active)
        self.exit_passive.rescale_pheight(0.08)
        self.exit_hovered.rescale_pheight(0.08)
        self.exit_active.rescale_pheight(0.08)
        self.exit_passive.set_px(0.5)
        self.exit_hovered.set_px(0.5)
        self.exit_active.set_px(0.5)
        self.exit_passive.set_py(0.9)
        self.exit_hovered.set_py(0.9)
        self.exit_active.set_py(0.9)

        self.settings_passive = object.Image(handler, "Settings Button Passive", image_path="settings_option_unselected.png", alpha=150)
        self.settings_hovered = object.Animation(handler, "Settings Button Hovered", frame_paths=("settings_option_selection_1.png", "settings_option_selection_2.png", "settings_option_selection_3.png", "settings_option_selection_2.png"))
        self.settings_active = object.Image(handler, "Settings Button Active", image_path="settings_option_unselected.png")
        self.settings_button = complex.Button("Settings Button", self.settings_passive, self.settings_hovered, self.settings_active)
        self.settings_passive.rescale_pheight(0.08)
        self.settings_hovered.rescale_pheight(0.08)
        self.settings_active.rescale_pheight(0.08)
        self.settings_passive.set_px(0.5)
        self.settings_hovered.set_px(0.5)
        self.settings_active.set_px(0.5)
        self.settings_passive.set_py(0.8)
        self.settings_hovered.set_py(0.8)
        self.settings_active.set_py(0.8)

        self.campaign_passive = object.Image(handler, "Campaign Button Passive", image_path="campaign_option_unselected.png", alpha=150)
        self.campaign_hovered = object.Animation(handler, "Campaign Button Hovered", frame_paths=("campaign_option_selection_1.png", "campaign_option_selection_2.png", "campaign_option_selection_3.png", "campaign_option_selection_2.png"))
        self.campaign_active = object.Image(handler, "Campaign Button Active", image_path="campaign_option_unselected.png")
        self.campaign_button = complex.Button("Campaign Button", self.campaign_passive, self.campaign_hovered, self.campaign_active)
        self.campaign_passive.rescale_pheight(0.08)
        self.campaign_hovered.rescale_pheight(0.08)
        self.campaign_active.rescale_pheight(0.08)
        self.campaign_passive.set_px(0.5)
        self.campaign_hovered.set_px(0.5)
        self.campaign_active.set_px(0.5)
        self.campaign_passive.set_py(0.45)
        self.campaign_hovered.set_py(0.45)
        self.campaign_active.set_py(0.45)

        self.coop_passive = object.Image(handler, "Coop Button Passive", image_path="coop_option_unselected.png", alpha=150)
        self.coop_hovered = object.Animation(handler, "Coop Button Hovered", frame_paths=("coop_option_selection_1.png", "coop_option_selection_2.png", "coop_option_selection_3.png", "coop_option_selection_2.png"))
        self.coop_active = object.Image(handler, "Coop Button Active", image_path="coop_option_unselected.png")
        self.coop_button = complex.Button("Coop Button", self.coop_passive, self.coop_hovered, self.coop_active)
        self.coop_passive.rescale_pwidth(0.2)
        self.coop_hovered.rescale_pwidth(0.2)
        self.coop_active.rescale_pwidth(0.2)
        self.coop_passive.set_px(0.4)
        self.coop_hovered.set_px(0.4)
        self.coop_active.set_px(0.4)
        self.coop_passive.set_py(0.55)
        self.coop_hovered.set_py(0.55)
        self.coop_active.set_py(0.55)

        self.versus_passive = object.Image(handler, "Versus Button Passive", image_path="versus_option_unselected.png", alpha=150)
        self.versus_hovered = object.Animation(handler, "Versus Button Hovered", frame_paths=("versus_option_selection_1.png", "versus_option_selection_2.png", "versus_option_selection_3.png", "versus_option_selection_2.png"))
        self.versus_active = object.Image(handler, "Versus Button Active", image_path="versus_option_unselected.png")
        self.versus_button = complex.Button("Versus Button", self.versus_passive, self.versus_hovered, self.versus_active)
        self.versus_passive.rescale_pwidth(0.2)
        self.versus_hovered.rescale_pwidth(0.2)
        self.versus_active.rescale_pwidth(0.2)
        self.versus_passive.set_px(0.6)
        self.versus_hovered.set_px(0.6)
        self.versus_active.set_px(0.6)
        self.versus_passive.set_py(0.55)
        self.versus_hovered.set_py(0.55)
        self.versus_active.set_py(0.55)

        self.custom_passive = object.Image(handler, "Custom Button Passive", image_path="custom_option_unselected.png", alpha=150)
        self.custom_hovered = object.Animation(handler, "Custom Button Hovered", frame_paths=("custom_option_selection_1.png", "custom_option_selection_2.png", "custom_option_selection_3.png", "custom_option_selection_2.png"))
        self.custom_active = object.Image(handler, "Custom Button Active", image_path="custom_option_unselected.png")
        self.custom_button = complex.Button("Custom Button", self.custom_passive, self.custom_hovered, self.custom_active)
        self.custom_passive.rescale_pheight(0.08)
        self.custom_hovered.rescale_pheight(0.08)
        self.custom_active.rescale_pheight(0.08)
        self.custom_passive.set_px(0.5)
        self.custom_hovered.set_px(0.5)
        self.custom_active.set_px(0.5)
        self.custom_passive.set_py(0.65)
        self.custom_hovered.set_py(0.65)
        self.custom_active.set_py(0.65)

        self.background_music_channel = pygame.mixer.Channel(1)
        self.background_music = sound.new("Oriental Panorama - En1gmA.mp3")
        self.background_music.set_volume(0.1)

        self.background_music_timer = utils.Timer()

        self.title_pulse_timer = 0
        self.title_pulsing = False

        self.pulse_times = [90, 910, 2160, 2570, 2980, 3400, 4220, 5470, 5880, 6290, 6710, 7530, 8780, 9190, 9600,
                            10020, 10840, 12090, 12500, 12910, 13330, 14150, 15400, 15810, 16220, 16640, 17460, 18710,
                            19120, 19530, 19950, 20770, 22020, 22430, 22840, 23260, 24080, 25330, 25740, 26150, 26570,
                            27390, 28640, 29050, 29460, 29880, 30700, 31950, 32360, 32770, 33190, 34010, 35260, 35670,
                            36080, 36500, 39810, 40630, 41880, 42290, 42700, 43120, 43940,
                            45190, 45600, 46010, 46430, 47250, 48500, 48910, 49320, 49740, 50560, 51810, 52220, 52630,
                            53050, 53870, 55120, 55530, 55940, 56360, 57180, 58430, 58840, 59250, 59670, 60490, 61740,
                            62150, 62560, 62980, 63800, 65460, 65870, 66290, 67110, 68360, 68770, 69180, 69600,
                            70420, 71670, 72080, 72490, 72910, 73730, 74650, 75390, 75800, 76220, 77040, 78290, 78700,
                            79110, 79530, 80350, 81600, 82010, 82420, 82840, 83660, 84910, 85320, 85730, 86150, 86970,
                            88220, 88630, 89040, 89460, 90280, 91530, 91940, 92350, 92770, 93590, 94840, 95250, 95660,
                            96080, 96900, 98150, 98560, 98970, 99390, 100210, 101460, 101870, 102280, 102700, 103520,
                            104770, 105180, 105590, 106010, 106830, 108080, 108490, 108900, 109320, 110140, 111390,
                            111800, 112210, 112630, 113450, 114700, 115110, 115520, 115940, 116760, 118440,
                            119250, 120070, 121320, 121730, 121960, 122560, 123400, 125040, 125260,
                            125870, 126690, 128350, 129180, 130000, 131250, 131660, 131880, 132490,
                            134560, 135190, 135800, 138500, 139110, 142420,
                            198690, 199510, 200760, 201170, 201580, 202000, 202820, 204070, 204480, 204890, 205310,
                            206130, 207380, 207790, 208200, 208620, 209440, 210690, 211100, 211510, 211930, 212750,
                            214000, 214410, 214820, 215240, 216060, 217310, 217720, 218130, 218550, 219370, 220620,
                            221030, 221440, 221860, 222680, 223930, 224340, 224750, 225170, 225990, 227240, 227650,
                            228060, 228480, 229300, 230550, 230960, 231370, 231790, 232610, 233860, 234270, 234680,
                            235100, 235920, 237170, 237580, 237990, 238410, 239230, 240480, 240890, 241300, 241720,
                            242540, 243790, 244200, 244610, 245030, 245850, 247100, 247510, 247920, 248340, 251650,
                            252470, 253340, 253740, 254130, 254540, 254960, 255780, 257030,
                            257440, 257850, 258270, 259090, 260340, 260750, 261160, 261580, 262400, 263240, 264060,
                            264470, 264890, 265710, 266560, 267370, 267780, 268200, 269020, 269870, 270270, 270680,
                            271090,
                            271510, 272330, 273580, 273990, 274400, 274820, 275640, 276490, 277300, 277710, 278130,
                            278950, 279800, 280610, 281020, 281440, 282260, 283120, 283510, 283920, 284330, 284750,
                            285570,
                            286820, 287460, 288060, 288880, 289720, 290130, 290540, 290950, 291370, 292190, 292610,
                            293040,
                            293850, 294260, 294680, 295500, 296340, 296750, 297160, 297570, 297990, 298810, 300060,
                            300700,
                            301200, 302120, 302970, 303780, 304190, 304610]
        self.pulse_index = 0

        self.window_lightness = 0

    def start_process(self):
        runner.clear_update_queue()
        runner.clear_draw_queue()

        self.reset_buttons()

        self.background_music_channel.stop()
        self.window_lightness = 0

        runner.append_to_update_queue((self.title, self.title_pulse, self.title_pulse_down_1, self.title_pulse_down_2, self.title_pulse_down_3, self.exit_button, self.settings_button, self.campaign_button, self.coop_button, self.versus_button, self.custom_button))
        runner.append_to_draw_queue((self.title, self.exit_button, self.settings_button, self.campaign_button, self.coop_button, self.versus_button, self.custom_button))

    def run(self):
        window.fill((self.window_lightness, self.window_lightness, self.window_lightness * 2))

        if self.exit_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.exit_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.settings_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.settings_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.campaign_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.campaign_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.coop_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.coop_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.versus_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.versus_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        if self.custom_button.trigger_hovered:
            hover_sound.play()
            handler.mouse.set_custom_mouse(mouse_hovered_object)
        elif self.custom_button.trigger_unhovered:
            handler.mouse.set_custom_mouse(mouse_object)

        # Dealing with background music
        if not self.background_music_channel.get_busy():
            self.background_music_channel.play(self.background_music)
            self.background_music_timer.start()
            self.pulse_index = 0

        # Title pulse behaviour
        if not self.title_pulsing:
            current_timer = self.background_music_timer.get_ms()
            if len(self.pulse_times) > self.pulse_index:
                if current_timer > self.pulse_times[self.pulse_index]:
                    #print(self.pulse_times[self.pulse_index])
                    self.title_pulse_timer = 14
                    self.pulse_index += 1
                    self.window_lightness += 5

        # Decreasing window lightness
        if self.window_lightness > 0:
            self.window_lightness -= 0.1

        # Switching between titles
        if not self.title_pulsing and self.title_pulse_timer == 14:
            self.title_pulsing = True
            runner.remove_from_draw_queue(self.title)
            runner.append_to_draw_queue(self.title_pulse)
        elif self.title_pulsing and self.title_pulse_timer == 9:
            runner.remove_from_draw_queue(self.title_pulse)
            runner.append_to_draw_queue(self.title_pulse_down_1)
            self.title_pulse_timer -= 1
        elif self.title_pulsing and self.title_pulse_timer == 6:
            runner.remove_from_draw_queue(self.title_pulse_down_1)
            runner.append_to_draw_queue(self.title_pulse_down_2)
            self.title_pulse_timer -= 1
        elif self.title_pulsing and self.title_pulse_timer == 3:
            runner.remove_from_draw_queue(self.title_pulse_down_2)
            runner.append_to_draw_queue(self.title_pulse_down_3)
            self.title_pulse_timer -= 1
        elif self.title_pulsing and self.title_pulse_timer == 0:
            self.title_pulsing = False
            runner.remove_from_draw_queue(self.title_pulse_down_3)
            runner.append_to_draw_queue(self.title)
        elif self.title_pulsing:
            self.title_pulse_timer -= 1

        # Dealing with button behaviour
        if self.exit_button.enabled:
            confirm_sound.play()
            runner.close()

        if self.settings_button.trigger_enabled:
            confirm_sound.play()

        if self.campaign_button.trigger_enabled:
            confirm_sound.play()

        if self.coop_button.trigger_enabled:
            confirm_sound.play()

        if self.versus_button.trigger_enabled:
            confirm_sound.play()

        if self.custom_button.trigger_enabled:
            confirm_sound.play()
            return 1

        return 0

    def reset_buttons(self):
        self.exit_button.enabled = False
        self.settings_button.enabled = False
        self.campaign_button.enabled = False
        self.coop_button.enabled = False
        self.versus_button.enabled = False
        self.custom_button.enabled = False


window = pygame.display.set_mode(utils.get_screen_resolution())
handler = handler.Handler(window)
runner = runner.Runner(handler, 120, True)

utils.set_window_caption("Interjection")
utils.set_window_icon("window_icon.png")

mouse_object = object.Image(handler, "Custom Mouse", image_path="cursor/unselected0.png")
mouse_hovered_object = object.Image(handler, "Custom Mouse Hovered", image_path="cursor/selected0.png")
handler.mouse.set_custom_mouse(mouse_object)

SM = StateManager()
PD = player_data.PlayerData(handler)
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()
PD.add_random_character()


def game_behaviour():
    SM.process()


runner.set_behaviour_func(game_behaviour)

running = True
while running:
    running = runner.run()
