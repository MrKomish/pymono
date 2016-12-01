from cocos.director import director
from cocos.text import Label
from pymono.lib.cocos2d import *
from pymono.lib.observable import Observable
from pymono.models.cells.StreetCell import StreetCell, StreetPrices

from pymono.config import rgba_colors
from pymono.models.Cell import Cell


class CellDetailsView(cocos.layer.Layer):
    def __init__(self, cell_details_ctrl):
        super(CellDetailsView, self).__init__()

        self.cell_details_ctrl = cell_details_ctrl

        self.cell_name_label = None
        self.owner_label = None
        self.current_income_label = None

        self.street_prices_labels = [None, None, None]
        self.street_prices_labels_order = ["land_price", "house_price", "hotel_price"]

        self.x = director.window.width - 150
        self.y = 50

    def build(self):
        self.cell_details_ctrl.current_cell.watch(self.set_cell)

    def remove_all_cell_details(self):
        if self.cell_name_label in self.get_children():
            self.remove(self.cell_name_label)

        self.cell_name_label = None

        for street_price_label in self.street_prices_labels:
            if street_price_label in self.get_children():
                self.remove(street_price_label)

        self.street_prices_labels = [None, None, None]

        if self.owner_label in self.get_children():
            self.remove(self.owner_label)

        self.owner_label = None

        if self.current_income_label in self.get_children():
            self.remove(self.current_income_label)

        self.current_income_label = None

    def set_cell(self, cell: Cell):

        self.remove_all_cell_details()

        if cell is None:
            return

        self.create_cell_name_label(cell.name)

        if isinstance(cell, StreetCell):
            self.create_street_cell_prices_labels(cell.prices)
            self.create_cell_owner_label(cell.owner)
            self.create_cell_street_current_income(cell.owner.get() is not None, cell.current_income)

    def create_cell_name_label(self, text):

        self.cell_name_label = Label(text,
                                     font_name='Calibri',
                                     color=(0, 0, 0, 255),
                                     font_size=24,
                                     anchor_x='center', anchor_y='center')

        self.cell_name_label.position = 0, 210

        self.add(self.cell_name_label)

    def create_street_cell_prices_labels(self, prices: StreetPrices):
        for price_type, price in prices:
            view_index = self.street_prices_labels_order.index(price_type)

            price_label = Label("- " + price_type.replace("_", " ").title() + ": $%d" % price,
                                font_name='Calibri',
                                color=(0, 0, 0, 255),
                                font_size=18,
                                anchor_x='center', anchor_y='center')

            price_label.position = 0, 150 - view_index * 30

            self.street_prices_labels[view_index] = price_label
            self.add(price_label)

    def create_cell_owner_label(self, owner_observable: Observable):
        owner = owner_observable.get()

        color = rgba_colors[owner.color if owner is not None else "black"]
        owner_text = owner.color.title() if owner is not None else "No One"

        self.owner_label = Label("Owner: " + owner_text,
                                 font_name='Calibri',
                                 color=color,
                                 font_size=20,
                                 anchor_x='center', anchor_y='center')

        self.owner_label.position = 0, 30

        self.add(self.owner_label)

    def create_cell_street_current_income(self, has_owner, current_income):

        self.current_income_label = Label(("" if has_owner else "Potential ") + "Income: $%d" % current_income,
                                          font_name='Calibri',
                                          color=rgba_colors["black"],
                                          font_size=20,
                                          anchor_x='center', anchor_y='center')

        self.current_income_label.position = 0, 0

        self.add(self.current_income_label)
