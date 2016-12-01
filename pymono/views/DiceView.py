from cocos.director import director
from cocos.sprite import Sprite

from pymono.lib.cocos2d import *


class DiceView(cocos.layer.Layer):
    def __init__(self, dice_ctrl):
        super().__init__()
        self.dice_ctrl = dice_ctrl

        self.dice = None
        self.throw_dice_label = None

        self.x = director.window.width - 150
        self.y = director.window.height - 290

    def build(self):
        self.dice_ctrl.dice_result.watch(self.set_dice)
        director.window.push_handlers(self.dice_ctrl)

    def set_dice(self, value):

        if self.throw_dice_label in self.get_children():
            self.remove(self.throw_dice_label)

        self.dice = Sprite(image="res/dice" + str(value) + ".png",
                           position=(0, -110))

        self.add(self.dice)

        self._set_dice_text(value is not None)

    def _set_dice_text(self, dice_thrown):

        if self.throw_dice_label in self.get_children():
            self.remove(self.throw_dice_label)

        text = 'You Got' if dice_thrown else 'Throw The Dice'

        self.throw_dice_label = cocos.text.Label(text,
                                                 font_name='Calibri',
                                                 color=(0, 0, 0, 255),
                                                 font_size=26,
                                                 anchor_x='center', anchor_y='center')

        self.throw_dice_label.position = 0, 0

        self.add(self.throw_dice_label)
