from pymono.lib.observable import Observable
from pymono.models.Player import Player
from pyglet import clock

from pymono.config import cells_jumping_start_delay, cells_jumping_speed
from pymono.lib.popup import PopupBuilder
from pymono.views.PlayersView import PlayersView


class PlayersCtrl:
    @property
    def current_player(self):
        return [player for player in self.players if player.get().is_current][0]

    @property
    def current_player_index(self):
        return self.players.index(self.current_player)

    @current_player_index.setter
    def current_player_index(self, index):
        old_current_player = self.current_player
        new_current_player_index = divmod(index, len(self.players))[1]
        new_current_player = self.players[new_current_player_index]

        old_current_player.get().is_current, new_current_player.get().is_current = False, True

        new_current_player.changed()
        old_current_player.changed()

    def set_players(self, players: [Player]):
        self.players = [Observable(player) for player in players]
        self.players[0].get().is_current = True
        self.players[0].changed()

        """ debug code:
        for cell in self.board_ctrl.board.cells:
            try:
                cell.owner = self.players[0]
            except:
                pass
        """

    def __init__(self, board_ctrl):
        self.board_ctrl = board_ctrl

        self.players = []

        self.view = PlayersView(self)

    def decrease_freeze_turns(self, on_end):
        if self.current_player.get().freeze_turns_left > 0:

            self.current_player.get().freeze_turns_left -= 1

            if self.current_player.get().freeze_turns_left == 0:
                self.current_player.get().is_in_jail = False

            self.current_player.changed()

        if self.current_player.get().is_in_jail:
            jail_cell = self.board_ctrl.board.cells[self.current_player.get().cell_index]
            jail_cell.try_to_leave(self.board_ctrl, on_end)
        else:
            on_end()

    def next_turn(self):
        self.current_player_index += 1

    def can_player_move(self):
        return self.current_player.get().freeze_turns_left == 0

    def move_player(self, cell_number, callback):
        clock.schedule_once(lambda _: self._move_player(cell_number, callback), delay=cells_jumping_start_delay)

    def _move_player(self, left, callback):

        if left > 0:

            player = self.current_player.get()
            player.cell_index = divmod(player.cell_index + 1, len(self.board_ctrl.board.cells))[1]

            if player.cell_index == 0:
                self.current_player.get().money += 200

            self.current_player.changed()

            clock.schedule_once(lambda _: self.move_player(left - 1, callback), delay=cells_jumping_speed)

        else:
            clock.schedule_once(lambda _: callback(), delay=1)

    def player_lost(self, player, on_end):
        def on_close_click(popup):
            popup.close()
            on_end()

        popup = PopupBuilder() \
            .set_title(player.get().color.title() + " Player Lost!") \
            .set_message("You lost the game, Good luck in your next game!") \
            .add_button("Thanks", on_click=on_close_click) \
            .set_size(500, 220) \
            .build()

        player.set(None)
        self.players.remove(player)

        popup.show(self.board_ctrl)

