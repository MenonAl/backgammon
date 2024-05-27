from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)
# dataclass -> class
# White - 0
# Black - 1
global bar_white, bar_black, map_stacs, white_checkers, black_checkers, dice, move, double, impossible_move_Black, impossible_move_White, action, checkers, point, player

player = None
map_stacs = []
white_checkers = 0
black_checkers = 0
dice = [0, 0, 0, 0]
move = 0
impossible_move_White = 0
impossible_move_Black = 0
double = 0
checkers = -1
point = 0


@app.route('/', methods=['GET'])
def tests_HTML():
    return render_template('game.html')


@app.route('/game/size', methods=["POST"])
def game_size():
    global map_stacs
    action_move = request.form.get("game")
    checkers_moves = int(action_move)
    for i in range(0, checkers_moves):
        map_stacs.append([])
        print(map_stacs)
    return render_template("game.html")


@app.route('/game/checkers_quantity', methods=["POST"])
def game_checkers_quantity():
    global black_checkers, white_checkers
    action_move = request.form.get("game_checkers_quantity")
    checkers_quantity = int(action_move)
    for i in range(0, checkers_quantity):
        white_checkers += 1
        black_checkers += 1
        map_stacs[0].append('-1')
        map_stacs[-1].append('1')
    return render_template("game.html")


@app.route('/game/player_number', methods=["POST"])
def game_player_number():
    global player
    player = request.form.get("/game/player_number")
    if player == "-1":
        return render_template("game.html", player_color="You are white", player=player)
    else:
        return render_template("game.html", player_color="You are black", player=player)


@app.route('/game', methods=["POST"])
def start_game():
    global move, double, checkers, map_stacs, action, black_checkers, white_checkers
    return render_template('move.html', message1="Map is done.", size=len(map_stacs))
    """
            elif action == 'Transition move':  # убрать это отсюда попробовать, что то другое
                move += 1
                if move % 2 == 0:
                    checkers = 0
                else:
                    checkers = 1
                dice[0] = random.randint(1, 6)
                dice[1] = random.randint(1, 6)
                dice[2] = 0
                dice[3] = 0
                if dice[0] == dice[1]:
                    dice[2] = dice[0]
                    dice[3] = dice[0]
                    double += 1
                    return str(dice[0]) + ' ' + str(dice[1]) + ' ' + str(dice[2]) + ' ' + str(
                        dice[3]) + ' ' + "A double has been rolled, moves2." + render_template('move.html')
                else:
                    return str(dice[0]) + ' ' + str(dice[1]) + render_template('move.html')
            """  #  Transition  move



@app.route('/game/move/roll', methods=['POST'])
def roll_dice():
    global move, double, checkers, map_stacs, action, black_checkers, white_checkers

    dice[0] = random.randint(1, 6)
    dice[1] = random.randint(1, 6)
    dice[2] = 0
    dice[3] = 0
    if dice[0] == dice[1]:
        dice[2] = dice[0]
        dice[3] = dice[0]
        double += 1
        return render_template('move.html', message4=str(dice[0]) + ' ' + str(dice[1]) + ' ' + str(dice[2]) + ' ' + str(dice[3]) + ' ' + "A double has been rolled, moves2.", size=len(map_stacs))
    else:
        return render_template('move.html', message4=str(dice[0]) + ' ' + str(dice[1]), size=len(map_stacs))

@app.route('/game/move/transition_move', methods=['POST'])
def transition_move():
    global move, checkers
    move += 1
    if move % 2 == 0:
        checkers = -1
    else:
        checkers = 1
    return render_template("move.html", size=len(map_stacs))

@app.route('/game/move/try', methods=['POST'])
def check_move():
    return jsonify(map_stacs)


@app.route('/game/move', methods=['POST'])
def game():
    global bar_white, bar_black, map_stacs, white_checkers, black_checkers, dice, move, double, impossible_move_Black, impossible_move_White, checkers, point
    if str(checkers) == player:
        point = int(request.form.get('tasks'))
        print(map_stacs[int(point) - 1])
        if not map_stacs[int(point) - 1]:
            return render_template("move.html", message2="Impossible move", size=len(map_stacs))
        elif map_stacs[int(point) - 1][-1] != str(checkers):
            return render_template("move.html", message2="Impossible move", size=len(map_stacs))
        else:
            return "Good" + render_template('move.html', size=len(map_stacs))
    else:
        return render_template("move.html", message2="It's not your turn", size=len(map_stacs))


@app.route('/game/move/dice', methods=['GET'])
def game_move():
    global bar_white, bar_black, map_stacs, white_checkers, black_checkers, dice, move, double, impossible_move_Black, impossible_move_White, action, checkers, point

    dice_move_str = request.args.get("dice")
    print(request.args)
    print(dice_move_str)  # player pick what dice he will play.
    dice_move = 0

    if len(dice_move_str) > 1:
        for i in range(0, len(dice_move_str)):
            dice_move += dice[int(dice_move_str[i])]
    elif len(dice_move_str) > 4:
        return render_template("move.html", message3="There is only two dice", size=len(map_stacs))
    else:
        dice_move = dice[int(dice_move_str)]
    if move % 2 == 0:
        if map_stacs[point - 1 + dice_move - 1] == str(checkers * -1):
            return render_template("move.html", message3="Impossible move", size=len(map_stacs))
        else:
            map_stacs[point - 1 + dice_move - 1].append(str(checkers))
            print("------")
            print(map_stacs)
            print("------")
            map_stacs[point - 1].pop()
            print("------")
            print(map_stacs)
            print("------")
            return str(len(map_stacs[point - 1 + dice_move - 1])) + render_template("move.html", message3="Move is done", size=len(map_stacs))
    else:
        if map_stacs[point - dice_move] == str(checkers * -1):
            return render_template("move.html", message3="Impossible move", size=len(map_stacs))
        else:
            map_stacs[point - 1].pop()
            map_stacs[point - dice_move].append(str(checkers))
            return str(len(map_stacs[point - dice_move])) + render_template("move.html", message3="Move is done", size=len(map_stacs) )



if __name__ == '__main__':
    app.run(debug=True, port=5000)
