import pygame
import chess
import sys
import os

# Stałe
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption("Szachy")
FONT = pygame.font.SysFont("arial", 24)

# Wczytaj obrazy figur
pieces_img = {}
def load_images():
    pieces = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    for piece in pieces:
        image = pygame.image.load(f"assets/{piece}.png")
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        pieces_img[piece] = image

def draw_board(win, board, selected_square):
    colors = [WHITE, BROWN]
    for row in range(8):
        for col in range(8):
            square_color = colors[(row + col) % 2]
            rect = pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, square_color, rect)
            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                img = pieces_img[piece.symbol()]
                win.blit(img, rect.topleft)
            if selected_square == square:
                pygame.draw.rect(win, HIGHLIGHT, rect, 4)

def draw_text(win, text, y, color=(0, 0, 0)):
    label = FONT.render(text, True, color)
    win.blit(label, (10, y))

def save_result(result):
    with open("scores.txt", "a") as f:
        f.write(result + "\n")

def show_scoreboard(win):
    draw_text(win, "Tablica wyników:", HEIGHT + 5)
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines[-5:]):
                draw_text(win, f"{i+1}. {line.strip()}", HEIGHT + 30 + i*25)

def get_square_under_mouse(pos):
    x, y = pos
    if y >= HEIGHT:
        return None
    col = x // SQUARE_SIZE
    row = 7 - (y // SQUARE_SIZE)
    return chess.square(col, row)

def main():
    load_images()
    board = chess.Board()
    clock = pygame.time.Clock()
    selected_square = None
    run = True
    game_over = False
    result = ""

    while run:
        clock.tick(30)
        WIN.fill((255, 255, 255))
        draw_board(WIN, board, selected_square)
        show_scoreboard(WIN)

        if not game_over:
            turn = "Biały" if board.turn else "Czarny"
            draw_text(WIN, f"Tura: {turn}", HEIGHT - 30)
        else:
            draw_text(WIN, f"Koniec gry: {result}", HEIGHT - 30)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                square = get_square_under_mouse(pygame.mouse.get_pos())
                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == board.turn:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None

                        if board.is_checkmate():
                            result = "Biały wygrał!" if board.turn == chess.BLACK else "Czarny wygrał!"
                            save_result(result)
                            game_over = True
                        elif board.is_stalemate():
                            result = "Remis (pat)"
                            save_result(result)
                            game_over = True
                        elif board.is_insufficient_material():
                            result = "Remis (brak materiału)"
                            save_result(result)
                            game_over = True
                    else:
                        selected_square = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()
                    game_over = False
                    selected_square = None

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()