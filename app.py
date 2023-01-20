from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import random

app = Flask(__name__)
class Coin():
    def __init__(self, id, color):
        self.id = id
        self.color = color
        # self.polozenie = ''

    def __repr__(self):
        return f'{self.id} {self.color}'


class Dice():
    def roll(self):
        min = 1
        max = 6
        roll_result = random.randint(min, max)
        return roll_result

class Board():
    def __init__(self):
        self.list = []
        for x in range (40): self.list.append(None)

class Game():
    def __init__(self, names):
        self.active_player = 0
        self.players = list()
        #self.plansza = []
        self.dice = Dice()
        self.board = Board()
        self.board_for_jinja = []
        id = 0
        for name in names:
            self.players.append(Player(id, name))
            id += 1
        self.assign_colors_for_players()
        self.assign_coins_for_players()
        self.assigns_coins_to_storage()
        self.make_board_for_jinja()
        self.starting_positions_dict = {
            0: 0,
            1: 10,
            2: 20,
            3: 30
        }

    def assign_colors_for_players(self):
        color = ['Red', 'Blue', 'Green', 'Yellow' ]
        x = 0
        for player in self.players:
            player.color = color[x]
            x += 1
            #print(player.player_name, player.id, player.color)

    def assign_coins_for_players(self):
        for player in self.players:
            for id in range (0,4):
                player.coins.append(Coin(id, player.color))

    def assigns_coins_to_storage(self):
        for player in self.players:
            for coin in player.coins:
                #print(coin)
                player.coins_storage.append(coin)
            #print(player.player_name, player.id, player.coins[0].color)

    def make_board_for_jinja(self):
        self.board_for_jinja = [[0 for col in range(11)] for row in range(11)]
        #for i in range(11):
        #    for j in range(11):
        #        self.board_for_jinja.append('x')
           # self.board_for_jinja.append(self.board_for_jinja)

    def check_if_there_is_players_coin_on_board(self):
        pass




    # def starting_positions(self, player):
    #     if self.players[player].color == 'Red':
    #         start_position = 0#pozcja startowa dla kazdego pionka na liście- planszy
    #     elif self.players[player].color == 'Blue':
    #         start_position = 10
    #     elif self.players[player].color == 'Green':
    #         start_position = 20
    #     elif self.players[player].color == 'Yellow':
    #         start_position = 30


class Player():
    def __init__(self, id, name='Anonimowy'):
        self.id = id
        self.player_name = name
        self.coins = []
        self.coins_storage = []
        self.coins_home =[]
        # self.id = ''
        # self.color



@app.route('/')
def home():
    return render_template('home.htm')

@app.route('/single/form', methods=['GET', 'POST'])
def single_form():
    if request.method == 'POST':
        players = [x for x in request.form.getlist('names') if x]
        #print(players)

        if len(players) == 4:
            return single_phase0(players)
    return render_template('single/form.htm')

def single_phase0(name):
    global game
    game = Game(name)
    return redirect('/single/phase1', code=302)

@app.route('/single/phase1')
def single_phase1():
    #print(game.players)
    #print(game.players[game.active_player].player_name)
    # if game.active_player != 3:
    #     game.active_player +=1
    # elif game.active_player == 3:
    #     game.active_player = 0
    if len(game.players[game.active_player].coins_home) == 4:
        return single_phase1()
    throw_result = game.dice.roll()
    print(throw_result)
    if throw_result == 6:
        coin_start = game.players[game.active_player].coins_storage.pop()
        game.board.list[game.starting_positions_dict[game.active_player]] = coin_start
        return single_phase1()
    else:
        if len(game.players[game.active_player].coins_storage) < 4:
            a = game.board.list[game.starting_positions_dict[game.active_player]]
            game.board.list[game.starting_positions_dict[game.active_player]] = None
            
            game.board.list[game.starting_positions_dict[game.active_player] + throw_result] = a
        if game.active_player != 3:
            game.active_player += 1
        elif game.active_player == 3:
            game.active_player = 0

    print(game.players[game.active_player].coins_storage)
    #print(throw_result)

   # print(game.dice.roll())

    return render_template('single/phase1.htm', game= game, throw_result= throw_result)

@app.route('/test')
def test():  # put application's code here
    return 'test!'


if __name__ == '__main__':
    app.run(host="wierzba.wzks.uj.edu.pl", port=5106, debug=True)
