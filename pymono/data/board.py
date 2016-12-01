from pymono.models.Board import Board
from pymono.models.Cell import Cell

from pymono.models.cells.AwardCell import AwardCell
from pymono.models.cells.CompanyCell import CompanyCell
from pymono.models.cells.FreeParkingCell import FreeParkingCell
from pymono.models.cells.JailCell import JailCell
from pymono.models.cells.PenaltyCell import PenaltyCell
from pymono.models.cells.StreetCell import StreetCell, StreetPrices
from pymono.models.cells.TaxCell import TaxCell
from pymono.models.cells.TrainCell import TrainCell
from pymono.models.cells.GoToJailCell import GoToJailCell

train_income_table = [25, 50, 100, 200]

bottom_right_cell = Cell("Start")  # Start Cell

bottom_cells = [
    StreetCell("Sderot HaTmarim", "Eylat", StreetPrices(60, 50, 50), [4, 20, 60, 180, 320, 450]),
    AwardCell("Chest", amount=20),  # Chest
    StreetCell("Eilot Street", "Eylat", StreetPrices(60, 50, 50), [6, 10, 30, 90, 160, 250]),
    TaxCell("Tax", percents=10),
    TrainCell("Parvarim Train", 200, train_income_table),
    StreetCell("Ha-Yarden Street", "Tveria", StreetPrices(100, 50, 50), [6, 30, 90, 270, 400, 550]),
    PenaltyCell("Penalty", amount=20),
    StreetCell("HaAtsma'ut Street", "Tveria", StreetPrices(100, 50, 50), [6, 30, 90, 270, 400, 550]),
    StreetCell("HaGalil Street", "Tveria", StreetPrices(120, 50, 50), [8, 40, 100, 300, 450, 600])
]

bottom_left_cell = JailCell()

top_cells = [
    StreetCell("Abba Hillel Street", "Ramat Gan", StreetPrices(220, 150, 150), [18, 90, 250, 700, 875, 1050]),
    PenaltyCell("Penalty", amount=20),
    StreetCell("Jabotinsky Street", "Ramat Gan", StreetPrices(220, 150, 150), [18, 90, 250, 700, 875, 1050]),
    StreetCell("Bialik Street", "Ramat Gan", StreetPrices(240, 150, 150), [20, 100, 300, 750, 925, 1100]),
    TrainCell("Rosh-Hanakra", 200, train_income_table),
    StreetCell("Jaffa Street", "Jerusalem", StreetPrices(240, 150, 150), [22, 110, 330, 800, 975, 1150]),
    StreetCell("Ben-Yehuda Street", "Jerusalem", StreetPrices(260, 150, 150), [22, 110, 330, 800, 975, 1150]),
    CompanyCell("Water Company", price=150, income_factor=4, big_income_factor=10),
    StreetCell("King George Street", "Jerusalem", StreetPrices(280, 150, 150), [24, 120, 360, 850, 1025, 1200])
]

top_left_cell = FreeParkingCell()

left_cells = [
    StreetCell("Sderot Shazar", "Beersheba", StreetPrices(140, 100, 100), [10, 50, 150, 450, 625, 750]),
    CompanyCell("Electrics Company", price=150, income_factor=4, big_income_factor=10),
    StreetCell("Sderot Ha-Nesi'im", "Beersheba", StreetPrices(140, 100, 100), [10, 50, 150, 450, 625, 750]),
    StreetCell("Dereh Heylat", "Beersheba", StreetPrices(160, 100, 100), [12, 60, 180, 500, 700, 900]),
    TrainCell("Masa Trains Ltd.", 200, train_income_table),
    StreetCell("Sderot Binyamin", "Natanya", StreetPrices(180, 100, 100), [14, 70, 200, 550, 750, 950]),
    AwardCell("Chest", amount=20),
    StreetCell("Sderot Weizman", "Netanya", StreetPrices(180, 100, 100), [14, 70, 200, 550, 750, 950]),
    StreetCell("Herzl Street", "Netanya", StreetPrices(200, 100, 100), [16, 80, 220, 600, 800, 1000])
]

top_right_cell = GoToJailCell()

right_cells = [
    StreetCell("Sderot HaAtsma'ut", "Hayfa", StreetPrices(300, 200, 200), [26, 130, 390, 900, 1100, 1275]),
    StreetCell("He-Khaluts Street", "Hayfa", StreetPrices(300, 200, 200), [26, 130, 390, 900, 1100, 1275]),
    AwardCell("Chest", amount=20),
    StreetCell("Moriya Street", "Hayfa", StreetPrices(320, 200, 200), [28, 150, 450, 1000, 1200, 1400]),
    TrainCell("North Train", 200, train_income_table),
    PenaltyCell("Penalty", amount=20),
    StreetCell("Allenby Street", "Tel-Aviv", StreetPrices(350, 200, 200), [35, 175, 500, 1100, 1300, 1500]),
    TaxCell("Tax", percents=10),
    StreetCell("Dizengoff Street", "Tel-Aviv", StreetPrices(400, 200, 200), [50, 200, 600, 1400, 1700, 2000])
]

board = Board(
    bottom_right_cell, bottom_cells,
    bottom_left_cell, left_cells,
    top_left_cell, top_cells,
    top_right_cell, right_cells
)
