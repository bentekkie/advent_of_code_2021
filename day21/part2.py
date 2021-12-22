from collections import Counter, defaultdict

with open("input.txt") as f:
    p1 = int(f.readline().strip()[-1])
    p2 = int(f.readline().strip()[-1])

turn = list(Counter(a+b+c for a in range(1,4) for b in range(1,4) for c in range(1,4)).items())


wins = [0,0]
scores : dict[tuple[tuple[int,int],tuple[int,int],int],int] = {((p1,p2),(0,0)):1}

whos_turn = False
while len(scores):
    new_scores = defaultdict(int)
    for ((p1_last_pos,p2_last_pos),(p1_total_score,p2_total_score)),num_games in scores.items():
        for new_turn,new_games in turn:
            if whos_turn:
                new_pos = (p1_last_pos, ((p2_last_pos+new_turn-1) % 10) + 1)
                new_score = (p1_total_score,p2_total_score+new_pos[1])
            else:
                new_pos = (((p1_last_pos+new_turn-1) % 10) + 1, p2_last_pos)
                new_score = (p1_total_score+new_pos[0],p2_total_score)
            new_total_games = num_games * new_games
            if new_score[whos_turn] >= 21:
                wins[whos_turn] += new_total_games
            else:
                new_scores[new_pos,new_score] += new_total_games
    scores = new_scores
    whos_turn = not whos_turn

print(max(wins))