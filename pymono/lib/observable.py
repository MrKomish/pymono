from pyglet.event import EventDispatcher


class Observable(EventDispatcher):
    def __init__(self, value=None):
        self.__value = value

    def get(self):
        return self.__value

    def set(self, value):
        old_value = self.__value
        self.__value = value

        if value != old_value:
            self.dispatch_event('value_changed', value)

    def changed(self):
        self.dispatch_event('value_changed', self.__value)

    def watch(self, on_value):
        on_value(self.__value)
        self.push_handlers(value_changed=on_value)


Observable.register_event_type('value_changed')
