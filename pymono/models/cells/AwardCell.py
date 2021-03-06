from pymono.models.Cell import Cell

from pymono.lib.popup import PopupBuilder


class AwardCell(Cell):
    def __init__(self, name, amount):
        super().__init__(name)

        self.amount = amount

    def on_step(self, board_ctrl, on_end):

        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        player_observable = board_ctrl.players_ctrl.current_player
        player_observable.get().money += self.amount
        player_observable.changed()

        popup = PopupBuilder() \
            .set_title("Congratulations!") \
            .set_message("You just won $" + str(self.amount)) \
            .add_button("Thanks", on_click=on_close_click) \
            .set_size(500, 220) \
            .build()

        popup.show(board_ctrl)
