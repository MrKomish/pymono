from cocos.director import director
from cocos.text import Label
from pymono.models.Player import Player

from pymono.config import rgba_colors
from pymono.lib.cocos2d import *


class PlayersView(cocos.layer.Layer):
    def __init__(self, players_ctrl):
        super().__init__()

        self.players_ctrl = players_ctrl

        self.players_details_labels = [None, None, None, None]

        self.x = director.window.width - 150
        self.y = director.window.height - 60

    def set_player_details(self, player: Player, player_index):

        if self.players_details_labels[player_index] in self.get_children():
            self.remove(self.players_details_labels[player_index])

        if player is None:
            return

        font_size = 30 if self.players_ctrl.current_player.get().color == player.color else 26

        player_details = Label(player.color.title() + " - $%d" % player.money,
                               font_name='Calibri',
                               color=rgba_colors[player.color],
                               font_size=font_size,
                               anchor_x='center', anchor_y='center')

        player_details.position = 0, - player_index * 50

        self.players_details_labels[player_index] = player_details

        self.add(player_details)

    def build(self):
        for i, player in enumerate(self.players_ctrl.players):
            player.watch(lambda player, i=i: self.set_player_details(player, i))
