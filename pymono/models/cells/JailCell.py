import random

from pymono.models.Cell import Cell
from pyglet import clock

from pymono.lib.popup import PopupBuilder


class LeaveTrier:
    def __init__(self, board_ctrl, on_end):
        self.board_ctrl = board_ctrl
        self.on_end = on_end
        self.current_player_observer = board_ctrl.players_ctrl.current_player

        self.first_result = None

    def start(self):
        self.show_popup()

    def show_popup(self):
        purchase_popup = PopupBuilder() \
            .set_title("You Have A Chance To Leave The Jail!") \
            .set_message("All you need to do is to get double") \
            .add_button("Try", on_click=self.on_chance_popup_close_click) \
            .set_size(500, 270) \
            .build()

        purchase_popup.show(self.board_ctrl)

    def on_chance_popup_close_click(self, purchase_popup):
        purchase_popup.close()
        self.board_ctrl.dice_ctrl.reset_dice()
        self.board_ctrl.dice_ctrl.wait_for_throw(self.on_first_throw)

    def on_first_throw(self, first_result):
        self.board_ctrl.dice_ctrl.stop_waiting_for_throw(self.on_first_throw)
        self.first_result = first_result

        clock.schedule_once(lambda _: self.board_ctrl.dice_ctrl.reset_dice(), delay=0.3)
        self.board_ctrl.dice_ctrl.wait_for_throw(self.on_second_throw)

    def on_second_throw(self, second_result):
        self.board_ctrl.dice_ctrl.stop_waiting_for_throw(self.on_second_throw)

        if second_result == self.first_result:
            self.current_player_observer.get().is_in_jail = False
            self.current_player_observer.get().freeze_turns_left = 0
            self.current_player_observer.changed()

            self.show_success_popup()

        else:
            self.show_fail_popup()

    def show_success_popup(self):
        purchase_popup = PopupBuilder() \
            .set_title("You Done It!") \
            .set_message("You got out of jail") \
            .add_button("Yey!", on_click=self.on_popup_close_click) \
            .set_size(500, 220) \
            .build()

        purchase_popup.show(self.board_ctrl)

    def show_fail_popup(self):
        purchase_popup = PopupBuilder() \
            .set_title("You Failed!") \
            .set_message("Maybe in the next turn") \
            .add_button("Ok", on_click=self.on_popup_close_click) \
            .set_size(500, 220) \
            .build()

        purchase_popup.show(self.board_ctrl)

    def on_popup_close_click(self, popup):
        popup.close()
        self.on_end()


class JailCell(Cell):
    def __init__(self):
        super().__init__("Jail")

    def on_step(self, board_ctrl, on_end):
        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        current_player_observer = board_ctrl.players_ctrl.current_player

        if random.randrange(1, 7) == random.randrange(1, 7) == random.randrange(1, 7):

            purchase_popup = PopupBuilder() \
                .set_title("LUCKY! You Won't go to The Prison!") \
                .set_message("Because of a triple we thrown for you!") \
                .add_button("Yey!", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            purchase_popup.show(board_ctrl)

        else:

            current_player_observer.get().freeze_turns_left += 3
            current_player_observer.get().is_in_jail = True
            current_player_observer.changed()

            purchase_popup = PopupBuilder() \
                .set_title("You Are In The Jail!") \
                .set_message("You will stay here for the next 3 turns!") \
                .add_button("Ok", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            purchase_popup.show(board_ctrl)

    def try_to_leave(self, board_ctrl, on_end):

        leave_trier = LeaveTrier(board_ctrl, on_end)
        leave_trier.start()