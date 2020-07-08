from flask import Flask, render_template
from subprocess import check_output
from random import choice

cows = ['apt', 'bud-frogs', 'bunny', 'cheese', 'cock', 'default', 'duck', 'elephant', 'elephant-in-snake',
        'flaming-sheep', 'fox', 'gnu', 'hellokitty', 'koala', 'milk', 'moofasa', 'moose', 'pony-smaller',
        'sheep', 'skeleton', 'snowman', 'stegosaurus', 'stimpy', 'suse', 'three-eyes', 'turtle', 'tux',
        'unipony-smaller', 'www']


def run(command):
    return check_output(command, shell=True).decode('utf-8')


def get_fortune(fortunes):
    cow = choice(cows)
    return run('fortune %s -e | %s -f %s' % (fortunes, choice(['cowsay', 'cowthink']), cow))


app = Flask(__name__)


@app.route('/')
def index():
    f = get_fortune('fortunes tao wisdom goedel anarchism platitudes')
    return render_template('index.html', fortune=f)


@app.route('/br/')
def br():
    f = get_fortune('brasil')
    return render_template('index.html', fortune=f)


if __name__ == '__main__':
    app.run()
