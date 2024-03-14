import Physics

table = Physics.Table()

pos = Physics.Coordinate(Physics.TABLE_WIDTH/2, Physics.TABLE_LENGTH/2)

ball = Physics.StillBall(0, pos)

table += ball

with open("table.svg", "w") as file:
    file.write(table.svg())