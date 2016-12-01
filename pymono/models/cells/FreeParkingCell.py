from pymono.models.Cell import Cell

from pymono.lib.popup import PopupBuilder


class FreeParkingCell(Cell):
    def __init__(self):
        super().__init__("Free Parking")

    def on_step(self, board_ctrl, on_end):
        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        current_player_observer = board_ctrl.players_ctrl.current_player

        current_player_observer.get().freeze_turns_left += 1
        current_player_observer.changed()

        purchase_popup = PopupBuilder() \
            .set_title("You Found Free Parking Spot") \
            .set_message("You will stay here for the next turn!") \
            .add_button("Ok", on_click=on_close_click) \
            .set_size(500, 220) \
            .build()

        purchase_popup.show(board_ctrl)
