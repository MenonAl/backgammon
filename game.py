from flask import Flask, request, render_template, jsonify
import random

app = Flask(__name__)
# dataclass -> class
# White - 0
# Black - 1
global map_stacs, white_checkers, black_checkers, dice, move, double, action, checkers, point, player, checkers_quantity

checkers_quantity = 0
player = None
map_stacs = []
white_checkers = 0
black_checkers = 0
dice = [0, 0, 0, 0]
move = 0
double = 0
checkers = 0
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

    return render_template("game.html")


@app.route('/game/checkers_quantity', methods=["POST"])
def game_checkers_quantity():
    global black_checkers, white_checkers, checkers_quantity
    action_move = request.form.get("game_checkers_quantity")
    checkers_quantity = int(action_move)
    for i in range(0, checkers_quantity):
        white_checkers += 1
        black_checkers += 1
        map_stacs[0].append('0')# white checkers -> 0
        map_stacs[-1].append('1')# black checers -> 1
        for j in range(1, len(map_stacs) - 1):
            map_stacs[j].append("-1")
    return render_template("game.html")


@app.route('/game/player_number', methods=["POST"])
def game_player_number():
    global player
    player = request.form.get("/game/player_number")
    if player == "0":
        return render_template("game.html", player_color="You are white", player=player)
    elif player == "1":
        return render_template("game.html", player_color="You are black", player=player)
    else:
        return render_template("game.html", messages="Wrong player number")


@app.route('/game', methods=["POST"])
def start_game():
    global move, double, checkers, map_stacs, action, black_checkers, white_checkers
    return render_template('move.html', message1="Map is done.", size=len(map_stacs), checkers_quantity=len(map_stacs[0]), field=map_stacs)



@app.route('/game/move/roll', methods=['POST'])
def roll_dice():
    global move, double, checkers, map_stacs, action, black_checkers, white_checkers, checkers_quantity

    dice[0] = random.randint(1, 6)
    dice[1] = random.randint(1, 6)
    dice[2] = 0
    dice[3] = 0
    if dice[0] == dice[1]:
        dice[2] = dice[0]
        dice[3] = dice[0]
        double += 1
        return render_template('move.html', message4=str(dice[0]) + ' ' + str(dice[1]) + ' ' + str(dice[2]) + ' ' + str(dice[3]) + ' ' + "A double has been rolled, moves2.", size=len(map_stacs),checkers_quantity=checkers_quantity)
    else:
        return render_template('move.html', message4=str(dice[0]) + ' ' + str(dice[1]), size=len(map_stacs), checkers_quantity=checkers_quantity)

@app.route('/game/move/transition_move', methods=['POST'])
def transition_move():
    global move, checkers
    move += 1
    checkers = move % 2
    return render_template("move.html", size=len(map_stacs), checkers_quantity=checkers_quantity)

@app.route('/game/move/try', methods=['GET'])
def check_move():
    return jsonify(map_stacs)


@app.route('/game/move', methods=['POST'])
def game():
    global map_stacs, dice, move, double, checkers, point, checkers_quantity
    if str(checkers) == player:
        point = int(request.form.get('tasks'))
        if not map_stacs[int(point) - 1]:
            return render_template("move.html", message2="Impossible move", size=len(map_stacs), checkers_quantity=checkers_quantity)
        elif map_stacs[int(point) - 1][0] != str(checkers):
            return render_template("move.html", message2="Impossible move", size=len(map_stacs), checkers_quantity=checkers_quantity)
        else:
            return render_template('move.html', message2="Please, roll dices", size=len(map_stacs), checkers_quantity=checkers_quantity)
    else:
        return render_template("move.html", message2="It's not your turn", size=len(map_stacs), checkers_quantity=checkers_quantity)


@app.route('/game/move/dice', methods=['POST'])
def game_move():
    global map_stacs, dice, move, double, action, checkers, point, checkers_quantity

    dice_move_str = request.form.get("dice") # player pick what dice he will play.
    dice_move = 0

    # dice calculations
    if len(dice_move_str) > 1:
        for i in range(0, len(dice_move_str)):
            dice_move += dice[int(dice_move_str[i])]
    elif len(dice_move_str) > 4:
        return render_template("move.html", message3="There is only two dice", size=len(map_stacs), checkers_quantity=checkers_quantity)
    else:
        dice_move = dice[int(dice_move_str) - 1]

    if point - 1 + dice_move > len(map_stacs) - 1 or point - 1 - dice_move < 0:
        return render_template("move.html", message3="Impossible move", size=len(map_stacs), checkers_quantity=checkers_quantity)

    # make move
    if move % 2 == 0:
        # white move
        if map_stacs[point - 1 + dice_move][0] != str(checkers) and map_stacs[point - 1 + dice_move][0] != "-1":
            return render_template("move.html", message3="Impossible move", size=len(map_stacs), checkers_quantity=checkers_quantity)
        else:
            i = 0
            j = 0
            for i in range(0, checkers_quantity):
                if map_stacs[point - 1][i] == "-1":
                    break
            map_stacs[point - 1][i] = "-1"
            for j in range(0, checkers_quantity):
                if map_stacs[point - 1 + dice_move][j] == "-1":
                    break
            map_stacs[point - 1 + dice_move][j] = str(checkers)
            return str(len(map_stacs[point - 1 + dice_move - 1])) + render_template("move.html", message3="Move is done", size=len(map_stacs), checkers_quantity=checkers_quantity)
    else:
        #black move
        if map_stacs[point - dice_move - 1][0] != str(checkers) and map_stacs[point - dice_move - 1][0] != "-1":
            return render_template("move.html", message3="Impossible move", size=len(map_stacs), checkers_quantity=checkers_quantity)
        else:
            i = 0
            j = 0
            for i in range(0, checkers_quantity):
                if map_stacs[point - 1][i] == "-1":
                    break

            for j in range(0, checkers_quantity):
                if map_stacs[point - 1 - dice_move][j] == "-1":
                    break

            map_stacs[point - 1][i] = "-1"
            map_stacs[point - dice_move - 1][j] = str(checkers)
            return str(len(map_stacs[point - dice_move])) + render_template("move.html", message3="Move is done", size=len(map_stacs), checkers_quantity=checkers_quantity)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
