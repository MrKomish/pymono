import random

from pymono.lib.observable import Observable
from pymono.models.Cell import Cell

from pymono.lib.popup import PopupBuilder


class CompanyCell(Cell):
    def __init__(self, name, price, income_factor, big_income_factor):
        super().__init__(name)

        self.price = price
        self.income_factor = income_factor
        self.big_income_factor = big_income_factor  # means the income factor used if you own 2 companies.
        self.owner = Observable()

    def purchase(self, player_observable: Observable):
        player_observable.get().money -= self.price
        player_observable.changed()

        self.owner = player_observable

    def get_factor(self, cells):
        company_cells = [cell for cell in cells if isinstance(cell, CompanyCell)]
        player_company_cells = [cell for cell in company_cells if cell.owner.get() == self.owner.get()]

        if player_company_cells == 1:
            return self.income_factor
        else:
            return self.big_income_factor

    def payment_amount(self, cells):
        return random.randrange(1, 7) * self.get_factor(cells)

    def pay(self, payment_amount, current_player_observer):

        self.owner.get().money += payment_amount
        self.owner.changed()

        current_player_observer.get().money -= payment_amount
        current_player_observer.changed()

    def on_step(self, board_ctrl, on_end):

        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        current_player_observer = board_ctrl.players_ctrl.current_player

        if self.owner.get() is None:

            def on_purchase_click(purchase_popup):
                self.purchase(current_player_observer)
                purchase_popup.close()
                on_end()

            purchase_popup = PopupBuilder() \
                .set_title("Purchase offer") \
                .set_message("Would you like to purchase the " + self.name + "?") \
                .add_button("Buy For $%d" % self.price, on_click=on_purchase_click) \
                .add_button("Reject Offer", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            purchase_popup.show(board_ctrl)

        elif self.owner.get() != current_player_observer.get():
            payment_amount = self.payment_amount(board_ctrl.board.cells)
            self.pay(payment_amount, current_player_observer)

            charge_popup = PopupBuilder() \
                .set_title("It's " + current_player_observer.get().color.title() + " Player " + self.name) \
                .set_message("You just payed $" + str(payment_amount) + " to the " + self.owner.get().color.title() + " player") \
                .add_button("OK", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            charge_popup.show(board_ctrl)
