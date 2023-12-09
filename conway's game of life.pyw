import pygame as pg
import random
pg.init()

clockspeed = 20

boardsize = [170, 150]
tilesize = int((pg.display.Info().current_h/boardsize[1])*0.8)

dead_color = (0, 0, 0)
alive_color = (255, 255, 255)
grid_color = (50, 50, 50)
boarder_color = (255,0,0)
draw_grid = True


class Cell:
    def __init__(self, x, y, alive=False):
        self.x = x
        self.y = y
        self.alive = alive

    def get_neighbors(self, board):
        count = 0
        for xj in range(-1, 2):
            for yj in range(-1, 2):
                neighbor_x = (self.x + xj) % board.w  # Wrap around horizontally
                neighbor_y = (self.y + yj) % board.h  # Wrap around vertically

                if board.cells[neighbor_x][neighbor_y].alive and not (xj == 0 and yj == 0):
                    count += 1

        return count


class Board:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[Cell(x, y) for y in range(h)] for x in range(w)]

##    def print_self(self):
##        cache = ""
##        for row in self.cells:
##            for cell in row:
##                if cell.alive:
##                    cache += "O "
##                else:
##                    cache += "  "
##            cache += "\n"
##        print(cache)

    def switch_cell(self,x,y):
        self.cells[x][y].alive = not self.cells[x][y].alive

    def kill_cell(self,x,y):
        self.cells[x][y].alive = False

    def rise_cell(self,x,y):
        self.cells[x][y].alive = True
        

    def next_generation(self):
        new_cells = [[Cell(x, y) for y in range(self.h)] for x in range(self.w)]

        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                n = cell.get_neighbors(self)
                if cell.alive and (n < 2 or n > 3):
                    new_cells[x][y].alive = False
                elif cell.alive and (n == 2 or n == 3):
                    new_cells[x][y].alive = True
                elif not cell.alive and n == 3:
                    new_cells[x][y].alive = True

        self.cells = new_cells

    def draw_self(self, display, board,paused):
        display.fill(dead_color)

        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                if cell.alive:
                    pg.draw.rect(display, alive_color, (x * tilesize, y * tilesize, tilesize, tilesize))
                else:
                    pg.draw.rect(display, dead_color, (x * tilesize, y * tilesize, tilesize, tilesize))
        if draw_grid:
            for x in range(board.w):
                x_position = x * tilesize
                pg.draw.line(display, grid_color, (x_position, 0), (x_position, board.h * tilesize))

            for y in range(board.h):
                y_position = y * tilesize
                pg.draw.line(display, grid_color, (0, y_position), (board.w * tilesize, y_position))


        if paused:
            pg.draw.rect(display,boarder_color,(0,0,displaysize[0],displaysize[1]),int(tilesize/2))


def get_mouse_cell():
    mousepos = pg.mouse.get_pos()
    return mousepos[0] // tilesize, mousepos[1] // tilesize


def main():
    global board, dead, displaysize, paused, clockspeed,draw_grid

    clock = pg.time.Clock()
    displaysize = (boardsize[0] * tilesize, boardsize[1] * tilesize)
    display = pg.display.set_mode(displaysize)
    board = Board(boardsize[0], boardsize[1])
    paused = True

    dead = False
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True
                continue

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = True
                    continue

                if event.key == pg.K_SPACE:
                    paused = not paused

                if event.key == pg.K_KP_PLUS:
                    clockspeed *= 2

                if event.key == pg.K_KP_MINUS:
                    clockspeed /= 2

                if event.key == pg.K_g:
                    draw_grid = not draw_grid

                if event.key == pg.K_r:
                    board = Board(boardsize[0], boardsize[1])
                    

#            if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed(3)[0]:
                x, y = get_mouse_cell()
                board.rise_cell(x,y)

            if pg.mouse.get_pressed(3)[2]:
                x, y = get_mouse_cell()
                board.kill_cell(x,y)
                    

        board.draw_self(display, board,paused)
        pg.display.flip()

        if not paused:
            board.next_generation()
            clock.tick(clockspeed)
    pg.quit()


main()
quit()
