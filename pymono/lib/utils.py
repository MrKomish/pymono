def start(obj, view=None):
    if view is None:
        return obj.x - obj.width / 2, obj.y - obj.height / 2
    else:
        x, y = start(obj)
        return x + view.x, y + view.y


def end(obj, view=None):
    if view is None:
        return obj.x + obj.width / 2, obj.y + obj.height / 2
    else:
        x, y = end(obj)
        return x + view.x, y + view.y
