import axelrod as axl
import numpy as np
import os

def save(path, name, list):
    if not os.path.exists(path):
        os.makedirs(path)
    array = np.array(list)
    np.save(path + name, array)

def load(path, name):
    return np.load(path + name + ".npy").tolist()


def create_game_history(n_players, n_tours, noise, save_path, itr):
    matches_CD = []
    matches_10 = []
    pw_scores = []
    player_pairs = []
    player_pairs_enum = []
    scores = []
    avg_scores = []
    coop_nums = []
    avg_coop_nums = []

    listoflists = []
    name_list = ['matches_CD', 'matches_10', 'pw_scores', 'player_pairs',
                    'player_pairs_enum', 'scores', 'avg_scores',
                    'coop_nums', 'avg_coop_nums']
    tmp = axl.strategies[0:5]
    for k, P1 in enumerate(tmp): #axl.strategiess:
        for l, P2 in enumerate(tmp): #axl.strategies:
            players = (P1(), P2())
            match = axl.Match(players, turns=n_tours, noise=noise)
            game = match.play()
            temp = [None]*len(game)

            for i,_ in enumerate(game):
                temp[i] = [1 if str(game[i][j]) == 'D' else 0 for j in range(2)]

            matches_10.append(temp)
            matches_CD.append(game)
            pw_scores.append(match.scores())
            scores.append(match.final_score())
            avg_scores.append(match.final_score_per_turn())

            coop_nums.append(match.cooperation())
            avg_coop_nums.append(match.normalised_cooperation())

            player_pairs.append([P1, P2])
            player_pairs_enum.append([k, l])

    listoflists= [matches_10, matches_CD, pw_scores, player_pairs,
                    player_pairs_enum, scores, avg_scores,
                    coop_nums, avg_coop_nums]

    for name,list in zip(name_list, listoflists):
        save(save_path + 'res_%.2f/' %itr, name , list)

n_players = len(axl.strategies)
n_tours = 10
noise_list = np.linspace(0,1,20)

save_path = "/home/kubra/Desktop/cg_project/gt_rl/Axelrod/txts/"
for noise in noise_list:
    create_game_history(n_players, n_tours, noise, save_path, noise)



