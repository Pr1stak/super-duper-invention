from pygame import *

font.init()
WINDOW_SIZE = (768, 512)
FPS = 60
TILE_SIZE = 64
window = display.set_mode(WINDOW_SIZE)
text = font.SysFont('Times New Roman', 30)
clock = time.Clock()
running = True
finished = False

board = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
]


class Checker(sprite.Sprite):

    def __init__(self, x, y, color, img, king=False):
        super().__init__()
        self.color = color
        self.isKing = king
        self.image = image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):  # changing piece's image

        if piece_selected == self:
            self.image = image.load('images/select_' + piece_selected.color[0] + '.png')  # select_w/b.png

        if self.isKing:
            self.image = image.load('images/'+self.color + '_king.png')

        if piece_selected == self and self.isKing:
            self.image = image.load('images/select_' + piece_selected.color[0] + '_king' + '.png')  # select_w/b_king.png

        if piece_selected != self and not self.isKing:
            self.image = (image.load('images/'+self.color + '.png'))


class Board:
    def select_checker(coords):
        global piece_selected
        if coords[0] >= len(board[0]):  # clicking outside the board
            return

        if queue == 0:
            if board[coords[1]][coords[0]] and board[coords[1]][coords[0]].color == 'white':
                piece_selected = board[coords[1]][coords[0]]
                return
        else:
            if board[coords[1]][coords[0]] and board[coords[1]][coords[0]].color == 'black':
                piece_selected = board[coords[1]][coords[0]]
                return

        if piece_selected != 0:
            Board.move_checker(piece_selected, coords)

    def move_checker(checker, coords):  # moving pieces around and killing enemy pieces
        global queue, piece_selected

        delta_x = coords[0] * TILE_SIZE - checker.rect.x
        delta_y = coords[1] * TILE_SIZE - checker.rect.y

        if abs(delta_x) == abs(delta_y) == 1 * TILE_SIZE:  # moving 1 tile forward
            if board[coords[1]][coords[0]]:
                piece_selected = 0
                return
            board[checker.rect.y // TILE_SIZE + delta_y // TILE_SIZE][checker.rect.x // TILE_SIZE + delta_x // TILE_SIZE] = checker
            board[checker.rect.y // TILE_SIZE][checker.rect.x // TILE_SIZE] = 0
            checker.rect.x += delta_x
            checker.rect.y += delta_y
            queue = not queue
            piece_selected = 0

        elif abs(delta_x) == abs(delta_y) == 2 * TILE_SIZE:  # moving 2 tiles forward

            # if clicked on an already busy tile
            if board[coords[1]][coords[0]]:
                piece_selected = 0
                return
            # if the tile between the old and new positions is not taken by anything
            if not board[coords[1] - delta_y // (2 * TILE_SIZE)][coords[0] - delta_x // (2 * TILE_SIZE)]:
                piece_selected = 0
                return
            # and if it is, check whether the color of that piece matches the color of moving piece
            if board[coords[1] - delta_y // (2 * TILE_SIZE)][
                coords[0] - delta_x // (2 * TILE_SIZE)].color == checker.color:
                piece_selected = 0
                return

            # moving pieces on board
            board[checker.rect.y // TILE_SIZE + delta_y // TILE_SIZE][
                checker.rect.x // TILE_SIZE + delta_x // TILE_SIZE] = checker
            board[checker.rect.y // TILE_SIZE][checker.rect.x // TILE_SIZE] = 0
            checker.rect.x += delta_x
            checker.rect.y += delta_y
            # removing the enemy piece
            board[coords[1] - delta_y // (2 * TILE_SIZE)][coords[0] - delta_x // (2 * TILE_SIZE)].kill()
            board[coords[1] - delta_y // (2 * TILE_SIZE)][coords[0] - delta_x // (2 * TILE_SIZE)] = 0
            queue = not queue
            piece_selected = 0

        else:
            piece_selected = 0
            return

        if checker.color == 'white' and checker.rect.y == 0:
            checker.isKing = True
        if checker.color == 'black' and checker.rect.y == WINDOW_SIZE[1] - TILE_SIZE:
            checker.isKing = True

    def queue_text(queue):
        if len(pieces_white) == 0 or len(pieces_black) == 0:
            return "Game over"
        if queue == 0:
            return "White's turn"
        else:
            return "Black's turn"


pieces_black = sprite.Group()
pieces_white = sprite.Group()
piece_selected = 0
queue = 0

for row in range(len(board)):
    for column in range(len(board[row])):
        if board[row][column] == 1:
            b_piece = Checker(column * TILE_SIZE, row * TILE_SIZE, 'black', 'images/black.png')
            board[row][column] = b_piece
            pieces_black.add(b_piece)

        elif board[row][column] == 2:
            w_piece = Checker(column * TILE_SIZE, row * TILE_SIZE, 'white', 'images/white.png')
            board[row][column] = w_piece
            pieces_white.add(w_piece)

while running:
    if not finished:
        if pieces_black == 0:
            finished = True
        if pieces_white == 0:
            finished = True

        window.fill((0, 0, 0))
        window.blit(image.load('images/board.png'), (0, 0))
        pieces_white.draw(window)
        pieces_black.draw(window)

        pieces_white.update()
        pieces_black.update()

        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                Board.select_checker([x // TILE_SIZE, y // TILE_SIZE])

        window.blit(text.render(Board.queue_text(queue), False, (255, 255, 255)), (544, 64))
        window.blit(text.render(('White pieces: ' + str(len(pieces_white))), False, (255, 255, 255)), (544, 128))
        window.blit(text.render(('Black pieces: ' + str(len(pieces_black))), False, (255, 255, 255)), (544, 192))

        clock.tick(FPS)
        display.update()