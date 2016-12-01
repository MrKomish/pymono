rgba_colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 4, 0, 255),
    "yellow": (255, 216, 0, 255),
    "green": (0, 127, 70, 255),
    "blue": (0, 0, 255, 255),

    "popup_background": (243, 243, 243, 255),
    "popup_button_background": (173, 173, 173, 255)
}

is_production = True

if is_production:
    cells_jumping_start_delay = 0.25
    cells_jumping_speed = 0.05

else:
    cells_jumping_start_delay = 0.0001
    cells_jumping_speed = 0.0001
