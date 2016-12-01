from cocos.director import director
from cocos.sprite import Sprite
from pymono.lib.cocos2d import *
from pymono.lib.utils import start

from pymono.models.BoardLayout import BoardLayoutBuilder


class BoardView(cocos.layer.ColorLayer):

    def __init__(self, board_ctrl, cell_details_view, dice_view, players_view):

        super(BoardView, self).__init__(255, 255, 255, 255)
        self.board_ctrl = board_ctrl

        self.cell_details_view = cell_details_view
        self.dice_view = dice_view
        self.players_view = players_view

        self.board_background = Sprite('res/Monopoly-1000px.png',
                                       position=(director.window.width / 2 - 150, director.window.height / 2))

        self.board_layout = BoardLayoutBuilder(self.board_background.width, self.board_background.height) \
            .config_corner_cells(corner_size=132) \
            .config_bottom_cells(height=132, width=82) \
            .config_left_cells(height=82, width=132) \
            .config_top_cells(height=132, width=82) \
            .config_right_cells(height=82, width=132) \
            .build()

        self.players_sprites = [None, None, None, None]

    def redraw_player(self, player, i):

        if self.players_sprites[i] in self.get_children():
            self.remove(self.players_sprites[i])

        if player is None:
            return

        cell_x, cell_y, cell_width, cell_height = self.board_layout.cells[player.cell_index]

        cell_x += start(self.board_background)[0]

        x = cell_x + (cell_width - 38) // 2 + divmod(i, 2)[0] * 38
        y = cell_y + (cell_height - 38) // 2 + divmod(i, 2)[1] * 38

        player_sprite = Sprite("res/dots/" + player.color + ".png",
                               position=(x, y))

        self.players_sprites[i] = player_sprite

        self.add(player_sprite)

    def build(self):

        self.cell_details_view.build()
        self.add(self.cell_details_view)

        self.dice_view.build()
        self.add(self.dice_view)

        self.players_view.build()
        self.add(self.players_view)

        self.add(self.board_background)

        director.window.push_handlers(on_mouse_motion=lambda x, y, dx, dy: self.board_ctrl.mouse_move(x, y))

        for i, player_observer in enumerate(self.board_ctrl.players_ctrl.players):
            player_observer.watch(lambda player, player_observer=player_observer, i=i: self.redraw_player(player_observer.get(), i))
