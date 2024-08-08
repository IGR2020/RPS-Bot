import pygame as pg
from pygame.image import load
import json
from bots import *


pg.font.init()

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
background = Button((window_width, window_height), load("Background.png"))

run = True
fps = 0
clock = pg.time.Clock()

has_clicked = False
clicked_item = None

# returns true if play1 wins and None if tie
def get_win(play1, play2):
    if play1 == "Rock" and play2 == "Scissor": return True
    if play1 == "Scissor" and play2 == "Paper": return True
    if play1 == "Paper" and play2 == "Rock": return True
    if play1 == play2: return None
    return False


pg.mixer.init()
incorrect_sound = pg.mixer.Sound("incorrect.mp3")
correct_sound = pg.mixer.Sound("correct.mp3")

bot1 = BotV3(35, 4)
bot2 = BotV1()
bot2.clear_memory()
bot1.update_choice()
bot2.update_choice()


bot_game = True
wins = 0
win_rate = 0
total_plays = 0
bot_wins = 0
bot_win_rate = 0

while run:
    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            
            if not bot_game:
                file = open("data.json", "w")
                json.dump(bot1.all_moves, file)
                file.close()
            else:
                file = open("data bot1.json", "w")
                json.dump(bot1.all_moves, file)
                file.close()
                file = open("data bot2.json", "w")
                json.dump(bot2.all_moves, file)
                file.close()

            run = False

        if event.type == pg.MOUSEBUTTONDOWN and not bot_game:
            if paper_button.clicked():
                background.topleft = paper_button.topleft
                background.x -= 5
                background.y -= 5

            if scissor_button.clicked():
                background.topleft = scissor_button.topleft
                background.x -= 5
                background.y -= 5
                
            if rock_button.clicked():
                background.topleft = rock_button.topleft
                background.x -= 5
                background.y -= 5

        if event.type == pg.MOUSEBUTTONUP and not bot_game:
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
                background.topleft = (window_width, window_height)
                total_plays += 1
                bot1.all_moves.append(clicked_item)
                win = get_win(clicked_item, bot1.choice)
                if win:
                    wins += 1
                    correct_sound.play()
                if win is False:
                    bot_wins += 1
                    incorrect_sound.play()
                win_rate = wins/total_plays
                bot_win_rate = bot_wins/total_plays
                has_clicked = False
                bot1.update_choice()

    if bot_game:
        bot1.update_choice()
        bot2.update_choice()
        bot1.all_moves.append(bot2.choice)
        bot2.all_moves.append(bot1.choice)
        total_plays += 1
        win = get_win(bot2.choice, bot1.choice)
        if win:
            wins += 1
            correct_sound.play()
        if win is False:
            bot_wins += 1
            incorrect_sound.play()
        win_rate = wins/total_plays
        bot_win_rate = bot_wins/total_plays
        has_clicked = False
        bot1.update_choice()



    window.fill((180, 180, 255))

    background.display(window)

    rock_button.display(window)
    paper_button.display(window)
    scissor_button.display(window)

    if not bot_game:
        blit_text(window, "Bot Picks: " + bot1.choice, (window_width/2, 50), center=True)
        blit_text(window, "Tie Rate: " + str(round((1-bot_win_rate-win_rate)*10000)/100), (window_width/2, window_height-200), center=True)
        blit_text(window, "Bot Win Rate:" + str(round(bot_win_rate*10000)/100) + "%", (window_width/2, window_height-150), center=True)
        blit_text(window, "Player Win Rate:" + str(round(win_rate*10000)/100) + "%", (window_width/2, window_height-100), center=True)
        blit_text(window, "Total Plays: " + str(total_plays), (window_width/2, window_height-50), center=True)
    else:
        blit_text(window, "Bot1 Picks: " + bot1.choice, (window_width/2, 50), center=True)
        blit_text(window, "Tie Rate: " + str(round((1-bot_win_rate-win_rate)*10000)/100), (window_width/2, window_height-200), center=True)
        blit_text(window, "Bot1 Win Rate:" + str(round(bot_win_rate*10000)/100) + "%", (window_width/2, window_height-150), center=True)
        blit_text(window, "Bot2 Win Rate:" + str(round(win_rate*10000)/100) + "%", (window_width/2, window_height-100), center=True)
        blit_text(window, "Total Plays: " + str(total_plays), (window_width/2, window_height-50), center=True)
    pg.display.update()

pg.quit()
quit()
