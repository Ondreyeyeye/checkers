import pygame as pg


def closest_number(list, number):
    min = 100
    min_value = 0
    for i in range(len(list)):
        if abs(list[i] - number) < min:
            min = abs(list[i] - number)
            min_value = list[i]
    return min_value


def closest_number2(list, x, y):
    min_dif = 1000
    # min_value = [[0], [0]]
    min_value = 0
    for i in range(len(list)):
        if abs(list[i][2] - x) + abs(list[i][3] - y) < min_dif:
            min_dif = abs(list[i][2] - x) + abs(list[i][3] - y)
            # min_value[0] = list[i][2]
            # min_value[1] = list[i][3]
            min_value = i
    return min_value


class App:
    def __init__(self):
        self.running = False
        self.drawing = False
        self.size = width, length = 600, 500
        self.size_field = 400
        self.step_field = 20

        self.centers = []
        for i in range(8):
            self.centers.append(self.step_field + self.size_field // 8 // 2 + self.size_field // 8 * i)

        self.color_cells = []
        for i in range(8):
            self.color_cells.append([0] * 8)
        for i in range(8):
            for j in range(8):
                if i % 2 == 0:
                    if j % 2 != 0:
                        self.color_cells[i][j] = "BLACK"
                else:
                    if j % 2 == 0:
                        self.color_cells[i][j] = "BLACK"

        self.field_description = []
        for i in range(64):
            self.field_description.append([[], [], [], []]) # [0] - can move here [1] - not ready yet [2] - x [3] - y

        self.coordinates = []  # [0] - alive(0 - no, 1 - yes) [1] - color(0 - black, 1 = white), [2] - x, [3] - y, [4] - king
        for i in range(24):
            self.coordinates.append([[], [], [], [], []])

        self.diagonals = [0, 0, 0, 0]

        self.index = 0
        self.old_x = 0
        self.old_y = 0

        self.screen = pg.display.set_mode(self.size)
        self.screen.fill("PURPLE")
        self.surf_white = pg.Surface((self.size_field, self.size_field), pg.SRCALPHA, 32)
        self.surf_black = pg.Surface((self.size_field, self.size_field), pg.SRCALPHA, 32)

    def run(self):
        self.running = True
        pg.init()
        self.checkers()
        while self.running:
            self.field()
            self.input()
            self.moving()
            pg.display.flip()
            # print(*self.coordinates)
            # print(*self.centers)

    def input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                self.drawing = True
                x = event.pos[0]
                y = event.pos[1]
                self.index = closest_number2(self.coordinates, x, y)
                self.old_x = self.coordinates[self.index][2]
                self.old_y = self.coordinates[self.index][3]

            if event.type == pg.MOUSEMOTION:
                pass
            if event.type == pg.MOUSEBUTTONUP:
                self.drawing = False
                x = event.pos[0]
                y = event.pos[1]
                new_x = 0
                new_y = 0
                test = 1
                for i in range(len(self.centers)):
                    new_x = closest_number(self.centers, x)
                    new_y = closest_number(self.centers, y)

                for i in range(24):
                    if new_x == self.coordinates[i][2] and new_y == self.coordinates[i][3] and self.coordinates[i][0] != 0:
                        test = 0

                if self.color_cells[(new_x - 20 - 25) // 50][(new_y - 20 - 25) // 50] != "BLACK":
                    test = 0

                if self.coordinates[self.index][4] != 0:
                    if self.coordinates[self.index][1] == "WHITE":
                        if new_y >= self.old_y:
                            test = 0
                    else:
                        if new_y <= self.old_y:
                            test = 0
                    self.diagonals = [0, 0, 0, 0]
                    self.check_near(self.old_x, self.old_y)

                    # if self.check_near(self.old_x, self.old_y) == "right_up":
                    if self.diagonals[0] == 1:
                        x = self.coordinates[self.index][2]
                        y = self.coordinates[self.index][3]
                        if new_x != self.old_x + 50 * 2 or new_y != self.old_y - 50 * 2:
                            test = 0
                        else:
                            if test != 0:
                                self.coordinates[self.empty_cell(self.old_x + 50, self.old_y - 50, 2)][0] = 0

                    # if self.check_near(self.old_x, self.old_y) == "left_up":
                    if self.diagonals[1] == 1:
                        x = self.coordinates[self.index][2]
                        y = self.coordinates[self.index][3]
                        if new_x != self.old_x - 50 * 2 or new_y != self.old_y - 50 * 2:
                            test = 0
                        else:
                            if test != 0:
                                self.coordinates[self.empty_cell(self.old_x - 50, self.old_y - 50, 2)][0] = 0

                    # if self.check_near(self.old_x, self.old_y) == "right_down":
                    if self.diagonals[2] == 1:
                        x = self.coordinates[self.index][2]
                        y = self.coordinates[self.index][3]
                        if new_x != self.old_x + 50 * 2 or new_y != self.old_y + 50 * 2:
                            test = 0
                        else:
                            if test != 0:
                                self.coordinates[self.empty_cell(self.old_x + 50, self.old_y + 50, 2)][0] = 0

                    # if self.check_near(self.old_x, self.old_y) == "left_down":
                    if self.diagonals[3] == 1:
                        x = self.coordinates[self.index][2]
                        y = self.coordinates[self.index][3]
                        if new_x != self.old_x - 50 * 2 or new_y != self.old_y + 50 * 2:
                            test = 0
                        else:
                            if test != 0:
                                self.coordinates[self.empty_cell(self.old_x - 50, self.old_y + 50, 2)][0] = 0



                print(*self.diagonals)

                if test == 1:
                    self.coordinates[self.index][2] = new_x
                    self.coordinates[self.index][3] = new_y
                else:
                    self.coordinates[self.index][2] = self.old_x
                    self.coordinates[self.index][3] = self.old_y

            if self.drawing:
                x = event.pos[0]
                y = event.pos[1]
                on_screen = True
                if x > 395 or x < 45 or y > 395 or y < 45:
                    on_screen = False
                # pg.draw.circle(self.screen, self.coordinates[self.index][1], (x, y), self.size_field // 32 * 1.5)
                if on_screen:
                    self.coordinates[self.index][2] = x
                    self.coordinates[self.index][3] = y

    def field(self):
        field = pg.Rect(self.step_field, self.step_field, self.size_field, self.size_field)
        pg.draw.rect(self.screen, (78, 64, 31), field)
        parity = 0
        size = self.size_field // 8
        for y in range(0 + self.step_field, self.size_field + self.step_field, size):
            parity += 1
            start = self.step_field
            if parity % 2 == 0:
                start += size
            for x in range(start, self.size_field + self.step_field, size * 2):
                cell = pg.Rect(x, y, size, size)
                pg.draw.rect(self.screen, (185, 152, 76), cell)

        count = 8
        for i in self.centers:
            font = pg.font.Font(None, 36)
            text = font.render(str(count), False, (255, 255, 255))
            self.screen.blit(text, (5, i))
            count -= 1
        count = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for i in self.centers:
            font = pg.font.Font(None, 36)
            text = font.render(letters[count], False, (255, 255, 255))
            self.screen.blit(text, (i, 425))
            count += 1

    def checkers(self):
        counter = 0
        parity = 0
        for y in range(7, 4, -1):
            parity += 1
            start = 0
            if parity % 2 == 0:
                start += 1
            for x in range(start, len(self.centers), 2):
                # pg.draw.circle(self.surf_white, "WHITE", (self.centers[x] - self.step_field, self.centers[y] - self.step_field), self.size_field // 32)
                self.coordinates[counter][0] = 1
                self.coordinates[counter][1] = "WHITE"
                self.coordinates[counter][2] = self.centers[x]
                self.coordinates[counter][3] = self.centers[y]
                counter += 1
        # self.screen.blit(self.surf_white, (self.step_field, self.step_field))

        parity = 0
        for y in range(0, 3):
            parity += 1
            start = 0
            if parity % 2 != 0:
                start += 1
            for x in range(start, len(self.centers), 2):
                # pg.draw.circle(self.surf_black, "BLACK", (self.centers[x] - self.step_field, self.centers[y] - self.step_field), self.size_field // 32)
                self.coordinates[counter][0] = 1
                self.coordinates[counter][1] = "BLACK"
                self.coordinates[counter][2] = self.centers[x]
                self.coordinates[counter][3] = self.centers[y]
                counter += 1

        # self.screen.blit(self.surf_black, (self.step_field, self.step_field))

    def moving(self):
        for i in range(0, 24):
            if self.coordinates[i][0] == 1:
                pg.draw.circle(self.screen, self.coordinates[i][1], (self.coordinates[i][2], self.coordinates[i][3]), self.size_field // 32 * 1.5)

    def check_near(self, x, y):
        for i in range(len(self.coordinates)):
            if self.coordinates[i][0] == 0:
                continue
            if x + 50 == self.coordinates[i][2] and y - 50 == self.coordinates[i][3] and self.coordinates[i][1] != self.coordinates[self.index][1]:
                if self.empty_cell(x + 50 * 2, y - 50 * 2, 1):
                    self.diagonals[0] = 1
                    # return "right_up"

            if x - 50 == self.coordinates[i][2] and y - 50 == self.coordinates[i][3] and self.coordinates[i][1] != self.coordinates[self.index][1]:
                if self.empty_cell(x - 50 * 2, y - 50 * 2, 1):
                    self.diagonals[1] = 1
                    # return "left_up"
            if x + 50 == self.coordinates[i][2] and y + 50 == self.coordinates[i][3] and self.coordinates[i][1] != self.coordinates[self.index][1]:
                if self.empty_cell(x + 50 * 2, y + 50 * 2, 1):
                    self.diagonals[2] = 1
                    # return "right_down"
            if x - 50 == self.coordinates[i][2] and y + 50 == self.coordinates[i][3] and self.coordinates[i][1] != self.coordinates[self.index][1]:
                if self.empty_cell(x - 50 * 2, y + 50 * 2, 1):
                    self.diagonals[3] = 1
                    # return "left_down"

    def empty_cell(self, x, y, if_one_return_True_if_two_return_index):
        for i in range(len(self.coordinates)):
            if if_one_return_True_if_two_return_index == 1:
                if x == self.coordinates[i][2] and y == self.coordinates[i][3] or x > 420 or x < 20 or y > 420 or y < 20:
                    return False
                else:
                    return True
            else:
                if x == self.coordinates[i][2] and y == self.coordinates[i][3] or x > 420 or x < 20 or y > 420 or y < 20:
                    return i


if __name__ == "__main__":
    app = App()
    app.run()



