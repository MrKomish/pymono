from pymono.lib.observable import Observable
from pymono.models.Cell import Cell

from pymono.lib.popup import PopupBuilder


class StreetPrices:
    def __init__(self, land_price, house_price, hotel_additional_price):
        self.land_price = land_price
        self.house_price = house_price
        self.hotel_price = house_price * 4 + hotel_additional_price

    def __iter__(self):
        """
        :returns: list of (price_type, price)'s
        """
        yield "land_price", self.land_price
        yield "house_price", self.house_price
        yield "hotel_price", self.house_price


class StreetCell(Cell):
    @property
    def current_income(self):
        return self.income_table[self.current_income_index]

    @property
    def next_price(self):
        if self.owner.get() is None:
            return self.prices.land_price

        elif self.current_income_index < 4:
            return self.prices.house_price

        else:
            return self.prices.hotel_price

    def __init__(self, name, city, prices: StreetPrices, income_table):
        super().__init__(name)

        self.city = city
        self.prices = prices

        """
        List with 6 elements:
        (0) Income from street without houses or hotel.
        (1) Income from street with house.
        (2) Income from street with 2 houses.
        (3) Income from street with 3 houses.
        (4) Income from street with 4 houses.
        (5) Income from street with hotel.
        """
        self.income_table = income_table
        self.current_income_index = 0

        self.owner = Observable()

    def purchase(self, player_observable: Observable):
        player_observable.get().money -= self.prices.land_price
        player_observable.changed()

        self.owner = player_observable

    def upgrade(self):
        self.owner.get().money -= self.next_price
        self.owner.changed()

        self.current_income_index += 1

    def pay(self, current_player_observer):
        current_player_observer.get().money -= self.current_income
        current_player_observer.changed()

        self.owner.get().money += self.current_income
        self.owner.changed()

    def on_step(self, board_ctrl, on_end):

        current_player_observer = board_ctrl.players_ctrl.current_player

        def on_close_click(purchase_popup):
            purchase_popup.close()
            on_end()

        if self.owner.get() is None:

            if self.prices.land_price > current_player_observer.get().money:
                on_end()

            def on_purchase_click(purchase_popup):
                self.purchase(current_player_observer)
                purchase_popup.close()
                on_end()

            purchase_popup = PopupBuilder() \
                .set_title("Purchase offer") \
                .set_message("Would you like to purchase " + self.name + "?") \
                .add_button("Buy For $%d" % self.prices.land_price, on_click=on_purchase_click) \
                .add_button("Reject Offer", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            purchase_popup.show(board_ctrl)

        elif self.owner.get() != current_player_observer.get():

            self.pay(current_player_observer)

            charge_popup = PopupBuilder() \
                .set_title("It's " + current_player_observer.get().color.title() + " Player Street") \
                .set_message("You just payed $" + str(self.current_income) + " to the " + self.owner.get().color.title() + " player") \
                .add_button("OK", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            charge_popup.show(board_ctrl)

        # 100% - current player is the owner
        elif all(not isinstance(cell, StreetCell) or cell.city != self.city or cell.owner.get() == self.owner.get()
                 for cell in board_ctrl.board.cells) and self.current_income_index < 5:

            if self.next_price > current_player_observer.get().money:
                on_end()

            if self.current_income_index == 0:
                upgrade_type = "a House"

            elif self.current_income_index < 4:
                upgrade_type = "another House"

            else:
                upgrade_type = "a Hotel"

            def on_upgrade_click(upgrade_popup):
                self.upgrade()
                upgrade_popup.close()
                on_end()

            upgrade_popup = PopupBuilder() \
                .set_title("Upgrade opportunity") \
                .set_message("Would you like to build " + upgrade_type + " here for $%d?" % self.next_price) \
                .add_button("Upgrade", on_click=on_upgrade_click) \
                .add_button("Reject opportunity", on_click=on_close_click) \
                .set_size(500, 220) \
                .build()

            upgrade_popup.show(board_ctrl)


