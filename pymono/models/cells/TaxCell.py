from pymono.models.Cell import Cell

from pymono.lib.popup import PopupBuilder


class TaxCell(Cell):
    def __init__(self, name, percents):
        super().__init__(name)
        
        self.percents = percents

    def on_step(self, board_ctrl, on_end):

        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        player_observable = board_ctrl.players_ctrl.current_player
        payment_amount = player_observable.get().money * self.percents / 100
        player_observable.get().money -= payment_amount
        player_observable.changed()

        popup = PopupBuilder() \
            .set_title("Tax!") \
            .set_message("You have to pay 10% of your money ($" + str(payment_amount) + ")") \
            .add_button("Ok", on_click=on_close_click) \
            .set_size(500, 220) \
            .build()

        popup.show(board_ctrl)