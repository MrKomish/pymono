class Player:
    def __init__(self, color):
        self.color = color
        self.cell_index = 0
        self.money = 1500
        self.is_current = False

        self.freeze_turns_left = 0
        self.is_in_jail = False
