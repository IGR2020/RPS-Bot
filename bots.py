import json

winning_move = {"Paper": "Scissor", "Scissor": "Rock", "Rock": "Paper"}

class BotV1:
    def __init__(self) -> None:
        file = open("data.json", "r")
        self.all_moves = json.load(file)
        file.close()
        self.choice = "Rock"
        self.depth = 1000

    def set_val_choice(self, scissor_val, paper_val, rock_val):
        if paper_val < rock_val > scissor_val:
            self.choice = "Rock"
        if rock_val < paper_val > scissor_val:
            self.choice = "Paper"
        if paper_val < scissor_val > rock_val:
            self.choice = "Scissor"

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

        self.set_val_choice(scissor_val, paper_val, rock_val)

class BotV2(BotV1):
    def __init__(self) -> None:
        super().__init__()
        self.search_size = 5
        self.depth = 35

    def update_choice(self):

        scissor_val = 0
        paper_val = 0
        rock_val = 0

        if len(self.all_moves) < 1:
            return
        
        for i, move in enumerate(reversed(self.all_moves)):

            if i < self.search_size:
                continue

            if i > self.depth:
                break
            
            for search in range(self.search_size):
                if move == list(reversed(self.all_moves))[search]:
                    
                    if i-search-1 < 0:
                        continue

                    try:
                        next_move = list(reversed(self.all_moves))[i-search-1]
                    except IndexError:
                        continue


                    if next_move == "Paper":
                        scissor_val += (search+1)/(i+1)
                    elif next_move == "Rock":
                        paper_val += (search+1)/(i+1)
                    elif next_move == "Scissor":
                        rock_val += (search+1)/(i+1)
                    continue
                break

        
        self.set_val_choice(scissor_val, paper_val, rock_val)
