from cocos.layer import ColorLayer, director
from cocos.text import Label

from pymono.config import rgba_colors


# Popup library build on cocos2d that I wrote


class PopupButton:
    def __init__(self, text, on_click):
        self.text = text
        self.on_click = on_click


class PopupView(ColorLayer):
    def __init__(self, popup_ctrl):
        super().__init__(*rgba_colors["popup_background"])

        self.popup_ctrl = popup_ctrl
        self.buttons_container = []

    def build(self, width, height):
        self.width, self.height = width, height
        self.x, self.y = (director.window.width - width) // 2, (director.window.height - height) // 2

        title_label = Label(self.popup_ctrl.title,
                            font_name='Calibri',
                            color=rgba_colors["black"],
                            font_size=23,
                            anchor_x='center', anchor_y='center')

        title_label.x = width // 2
        title_label.y = height - 50

        self.add(title_label)

        message_label = Label(self.popup_ctrl.message,
                              font_name='Calibri',
                              color=rgba_colors["black"],
                              font_size=16,
                              anchor_x='center', anchor_y='center')

        message_label.x = width // 2
        message_label.y = height - 100

        self.add(message_label)

        for i, button in enumerate(self.popup_ctrl.buttons):
            padding = 20
            button_container = ColorLayer(*rgba_colors["popup_button_background"],
                                          width=(width - padding) // len(self.popup_ctrl.buttons) - padding,
                                          height=40)

            button_container.position = padding * (i + 1) + button_container.width * i, 30

            self.add(button_container)
            self.buttons_container.append(button_container)

            button_text = Label(button.text,
                                font_name='Calibri',
                                color=rgba_colors["white"],
                                font_size=18,
                                anchor_x='center', anchor_y='center')

            button_text.position = button_container.x + button_container.width / 2, button_container.y + button_container.height / 2 + 3

            self.add(button_text)

        director.window.push_handlers(self.popup_ctrl)


class PopupCtrl:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.buttons = []

        self.shadow = ColorLayer(0, 0, 0, 100)
        self.view = PopupView(self)

        self.parent_ctrl = None

    def show(self, parent_ctrl):
        self.parent_ctrl = parent_ctrl

        parent_ctrl.view.add(self.shadow)
        parent_ctrl.view.add(self.view)

    def close(self):
        if self.parent_ctrl is None:
            raise Exception("PopupCtrl's .show() method was never called!")

        director.window.remove_handlers(self)
        self.parent_ctrl.view.remove(self.shadow)
        self.parent_ctrl.view.remove(self.view)

    def on_mouse_press(self, x, y, button, modifiers):
        for i, button_container in enumerate(self.view.buttons_container):
            start_x, start_y = button_container.x + self.view.x, button_container.y + self.view.y
            end_x, end_y = start_x + button_container.width, start_y + button_container.height

            if start_x <= x <= end_x and start_y <= y <= end_y:
                self.buttons[i].on_click(self)


class PopupBuilder:
    def __init__(self):
        self.popup_ctrl = PopupCtrl()

        self.width = None
        self.height = None

    def set_title(self, title):
        self.popup_ctrl.title = title
        return self

    def set_message(self, message):
        self.popup_ctrl.message = message
        return self

    def set_size(self, width, height):
        self.width = width
        self.height = height
        return self

    def add_button(self, text, on_click):
        self.popup_ctrl.buttons.append(PopupButton(text, on_click))
        return self

    def build(self):
        if self.width is None:
            raise Exception('PopupBuilder width was never set!')

        if self.height is None:
            raise Exception('PopupBuilder height was never set!')

        self.popup_ctrl.view.build(self.width, self.height)

        return self.popup_ctrl
