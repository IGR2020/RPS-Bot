import pygame as pg
from pygame.image import load
pg.font.init()
from time import time

def blit_text(win, text, pos, colour=(0, 0, 0), size=30, font="arialblack", blit=True, center=False):
    text = str(text)
    x, y = pos
    font_style = pg.font.SysFont(font, size)
    text_surface = font_style.render(text, True, colour)
    if center:
        x -= text_surface.get_width()//2
        y -= text_surface.get_height()//2
    if blit:
        win.blit(text_surface, (x, y))
    return text_surface


class Button(pg.Rect):
    def __init__(self, pos, image, scale=1, *args):
        x, y = pos
        width, height = image.get_width() * scale, image.get_height() * scale
        super().__init__(x, y, width, height)
        self.image = pg.transform.scale(image, (width, height))
        if len(args) == 1:
            self.info = args[0]
        else:
            self.info = args

    def clicked(self):
        pos = pg.mouse.get_pos()
        if self.collidepoint(pos):
            return True
        return False

    def display(self, win, background=None):
        """
        background can be any RGB value
        """
        if background is not None:
            pg.draw.rect(win, background, self)
        win.blit(self.image, self)

window = pg.display.set_mode()
window_width, window_height = window.get_size()
image_width = 250
rock_image = load("Rock.png")
rock_button = Button((0, window_height/2-image_width/2), rock_image)
paper_image = load("Paper.png")
paper_button = Button((window_width/2-image_width/2, window_height/2-image_width/2), paper_image)
scissor_image = load("Scissor.png")
scissor_button = Button((window_width-image_width, window_height/2-image_width/2), scissor_image)

run = True
fps = 60
clock = pg.time.Clock()

has_clicked = False
clicked_item = None

winning_move = {"Paper": "Scissor", "Scissor": "Rock", "Rock": "Paper"}

# returns true if play1 wins and None if tie
def get_win(play1, play2):
    if play1 == "Rock" and play2 == "Scissor": return True
    if play1 == "Scissor" and play2 == "Paper": return True
    if play1 == "Paper" and play2 == "Rock": return True
    if play1 == play2: return None
    return False

class Bot:
    def __init__(self) -> None:
        self.all_moves = []
        self.choice = "Rock"
        self.depth = 200
        self.search_size = 2

    def update_choice(self):
        scissor_val = 0
        paper_val = 0
        rock_val = 0
        if len(self.all_moves) < 1:
            return
        for i, move in enumerate(self.all_moves):
            if move == self.all_moves[-1]:
                try:
                    next_move = self.all_moves[i+1]
                except IndexError:
                    continue
                if next_move == "Paper":
                    scissor_val += 1
                elif next_move == "Rock":
                    paper_val += 1
                elif next_move == "Scissor":
                    rock_val += 1
        if paper_val < rock_val > scissor_val:
            self.choice = "Rock"
        if rock_val < paper_val > scissor_val:
            self.choice = "Paper"
        if paper_val < scissor_val > rock_val:
            self.choice = "Scissor"




bot = Bot()
wins = 0
win_rate = 0
total_plays = 0
bot_wins = 0
bot_win_rate = 0

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if paper_button.clicked():
                has_clicked = True
                clicked_item = "Paper"

            if scissor_button.clicked():
                has_clicked = True
                clicked_item = "Scissor"
                
            if rock_button.clicked():
                has_clicked = True
                clicked_item = "Rock"

            if has_clicked:
                total_plays += 1
                bot.all_moves.append(clicked_item)
                win = get_win(clicked_item, bot.choice)
                if win:
                    wins += 1
                if not win:
                    bot_wins += 1
                win_rate = wins/total_plays
                bot_win_rate = bot_wins/total_plays
                has_clicked = False
                bot.update_choice()


    window.fill((180, 180, 255))
    rock_button.display(window)
    paper_button.display(window)
    scissor_button.display(window)

    blit_text(window, "Bot Win Rate:" + str(round(bot_win_rate*10000)/100) + "%", (window_width/2, window_height-150), center=True)
    blit_text(window, "Player Win Rate:" + str(round(win_rate*10000)/100) + "%", (window_width/2, window_height-100), center=True)
    blit_text(window, "Total Plays: " + str(total_plays), (window_width/2, window_height-50), center=True)

    pg.display.update()

pg.quit()
quit()
