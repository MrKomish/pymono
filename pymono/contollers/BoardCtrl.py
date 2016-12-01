import pymono.data.board
from pymono.contollers.CellDetailsCtrl import CellDetailsCtrl
from pymono.contollers.DiceCtrl import DiceCtrl
from pymono.contollers.PlayersCtrl import PlayersCtrl
from pyglet import clock

from pymono.lib.popup import PopupBuilder
from pymono.views.BoardView import BoardView


class BoardCtrl:

    def __init__(self):
        self.board = pymono.data.board.board
        self.turn_number = 0

        self.cell_details_ctrl = CellDetailsCtrl(self)
        self.dice_ctrl = DiceCtrl(self)
        self.players_ctrl = PlayersCtrl(self)

        self.view = BoardView(self, self.cell_details_ctrl.view, self.dice_ctrl.view, self.players_ctrl.view)

        self._first_throw_result = None

    def mouse_move(self, x, y):
        self.cell_details_ctrl.current_cell.set(self.view.board_layout.get_cell_at_position(self.board, x, y))

    def start(self):
        self.turn()

    def turn(self):
        self.turn_number += 1

        self.dice_ctrl.reset_dice()

        if self.players_ctrl.can_player_move():
            self.dice_ctrl.wait_for_throw(self.on_first_throw)
        else:
            self.players_ctrl.decrease_freeze_turns(on_end=self.pre_turn_end)

    def on_first_throw(self, result):
        self.dice_ctrl.stop_waiting_for_throw(self.on_first_throw)

        self._first_throw_result = result

        clock.schedule_once(lambda _: self.dice_ctrl.reset_dice(), delay=0.3)

        self.dice_ctrl.wait_for_throw(self.on_second_throw)

    def on_second_throw(self, result):
        self.dice_ctrl.stop_waiting_for_throw(self.on_second_throw)

        self.players_ctrl.move_player(self._first_throw_result + result, self.on_player_moved)

    def on_player_moved(self):
        player = self.players_ctrl.current_player.get()
        cell = self.board.cells[player.cell_index]
        cell.on_step(self, on_end=self.pre_turn_end)

    def pre_turn_end(self):
        player = self.players_ctrl.current_player

        self.players_ctrl.next_turn()

        if player.get().money < 0:
            self.players_ctrl.player_lost(player, on_end=self.turn_end)
        else:
            self.turn_end()

    def turn_end(self):
        if len(self.players_ctrl.players) == 1:
            popup = PopupBuilder() \
                .set_title(self.players_ctrl.players[0].get().color.title() + " Player Won!") \
                .set_message("Congratulations! You have won this Monopoly game!") \
                .add_button("Good Game!", on_click=lambda popup: exit()) \
                .set_size(550, 220) \
                .build()

            popup.show(self)
        else:
            self.turn()
