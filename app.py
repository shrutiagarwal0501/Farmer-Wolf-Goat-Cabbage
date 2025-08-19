from flask import Flask, render_template, request, redirect, url_for
from puzzle_game import Puzzle, move

app = Flask(__name__)

# initial and goal states
init_state = Puzzle('left', 'left', 'left', 'left')
goal_state = Puzzle('right', 'right', 'right', 'right')
c_state = init_state

@app.route('/')
def start():
    global c_state
    c_state = init_state  # reset game every time start is visited
    return render_template('start.html')

@app.route('/game')
def index():
    return render_template('index.html', state=c_state)

@app.route('/move', methods=['POST'])
def move_item():
    global c_state
    item = request.form.get('item')
    c_state = move(c_state, None if item == 'n' else item)

    if not c_state.is_valid():
        return render_template('invalid.html')
    if c_state == goal_state:
        return render_template('win.html')
    return render_template('index.html', state=c_state)

@app.route('/restart')
def restart():
    return redirect(url_for('start'))

if __name__ == '__main__':
    app.run(debug=True)