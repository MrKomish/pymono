from pymono.lib.observable import Observable
from pymono.models.Cell import Cell

from pymono.lib.popup import PopupBuilder


class TrainCell(Cell):
    def __init__(self, name, price, income_table):
        super().__init__(name)

        self.price = price

        self.income_table = income_table
        """ Array with 4 elements:
        (0) if you got 1 train stations.
        (1) if you got 2 train stations.
        (2) if you got 3 train stations.
        (3) if you got 4 train stations.
        """

        self.owner = Observable()

    def purchase(self, player_observable: Observable):
        player_observable.get().money -= self.price
        player_observable.changed()

        self.owner = player_observable

    def payment_amount(self, cells):
        train_cells = [cell for cell in cells if isinstance(cell, TrainCell)]
        player_train_cells = [cell for cell in train_cells if cell.owner.get() == self.owner.get()]

        return self.income_table[len(player_train_cells)]

    def pay(self, payment_amount, current_player_observer):

        self.owner.get().money += payment_amount
        self.owner.changed()

        current_player_observer.get().money -= payment_amount
        current_player_observer.changed()

    def on_step(self, board_ctrl, on_end):

        current_player_observer = board_ctrl.players_ctrl.current_player

        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        if self.owner.get() is None:

            def on_purchase_click(purchase_popup):
                self.purchase(current_player_observer)
                purchase_popup.close()
                on_end()

            purchase_popup = PopupBuilder() \
                .set_title("Purchase offer") \
                .set_message("Would you like to purchase " + self.name + "?") \
                .add_button("Buy For $%d" % self.price, on_click=on_purchase_click) \
                .add_button("Reject Offer", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            purchase_popup.show(board_ctrl)

        elif self.owner.get() != current_player_observer.get():
            payment_amount = self.payment_amount(board_ctrl.board.cells)
            self.pay(payment_amount, current_player_observer)

            popup = PopupBuilder() \
                .set_title("It's " + current_player_observer.get().color.title() + " Player Train!") \
                .set_message("You have to pay $%d" % payment_amount) \
                .add_button("Ok", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            popup.show(board_ctrl)

        else:
            on_end()