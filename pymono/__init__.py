# To run this game:
# pip install cocos2d

from cocos.director import director
from pymono.contollers.BoardCtrl import BoardCtrl
from pymono.lib.cocos2d import *
from pymono.models.Player import Player

from pymono.lib.popup import PopupBuilder


class Game:
    def __init__(self):
        self.window = director.init(width=1300, height=1000, caption="Monopoly", fullscreen=False)

        self.board_ctrl = BoardCtrl()

        self.scene = cocos.scene.Scene(self.board_ctrl.view)

    def start(self):
        self.show_welcome_popup()
        director.run(self.scene)

    def show_welcome_popup(self):
        welcome_popup_builder = PopupBuilder() \
            .set_title("Welcome To Monopoly!") \
            .set_message("Select amount of players:") \
            .set_size(500, 220)

        for i in range(2, 5):
            def on_click(welcome_popup, i=i):
                welcome_popup.close()
                self.on_players_count_selected(i)

            welcome_popup_builder.add_button(str(i), on_click)

        welcome_popup = welcome_popup_builder.build()
        welcome_popup.show(self.board_ctrl)

    def on_players_count_selected(self, count):
        players = [Player("red"), Player("blue"), Player("green"), Player("yellow")][:count]

        self.board_ctrl.players_ctrl.set_players(players)
        self.board_ctrl.view.build()
        self.board_ctrl.start()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
