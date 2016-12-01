import random

from pymono.lib.utils import start, end
from pyglet.event import EventDispatcher

from pymono.lib.observable import Observable
from pymono.views.DiceView import DiceView


class DiceCtrl(EventDispatcher):

    def __init__(self, board_ctrl):
        super().__init__()
        self.board_ctrl = board_ctrl

        self.view = DiceView(self)

        self.dice_result = Observable()

    def throw_dice(self):
        self.dice_result.set(random.randrange(1, 7))
        self.dispatch_event('dice_thrown', self.dice_result.get())

    def wait_for_throw(self, callback):
        self.push_handlers(dice_thrown=callback)

    def stop_waiting_for_throw(self, callback):
        self.remove_handlers(dice_thrown=callback)

    def reset_dice(self):
        self.dice_result.set(None)

    def on_dice_click(self):
        if self.dice_result.get() is None:
            self.throw_dice()

    def on_mouse_press(self, x, y, button, modifiers):
        view, dice = self.view, self.view.dice
        start_x, start_y = start(dice, view)
        end_x, end_y = end(dice, view)

        if start_x <= x <= end_x and start_y <= y <= end_y:
            self.on_dice_click()

DiceCtrl.register_event_type('dice_thrown')
