from flask import Flask, render_template
from subprocess import check_output
from random import choice
from flask_sqlalchemy import SQLAlchemy

cows = ['apt', 'bud-frogs', 'bunny', 'cheese', 'cock', 'default', 'duck', 'elephant', 'elephant-in-snake',
        'flaming-sheep', 'gnu', 'hellokitty', 'koala', 'milk', 'moofasa', 'moose', 'pony-smaller',
        'sheep', 'skeleton', 'snowman', 'stegosaurus', 'stimpy', 'suse', 'three-eyes', 'turtle', 'tux',
        'unipony-smaller', 'www']


def run(command):
    return check_output(command, shell=True).decode('utf-8')


def get_fortune(fortunes):
    cow = choice(cows)
    return run('/usr/games/fortune %s -e | /usr/games/%s -f %s' % (fortunes, choice(['cowsay', 'cowthink']), cow))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Stat(db.Model):
    page = db.Column(db.String(10), primary_key=True)
    viewcount = db.Column(db.Integer)

    def __repr__(self):
        return self.page


def add_page_view(page):
    q = Stat.query.filter_by(page=page)
    if q.first():
        p = q.first()
        p.viewcount += 1
    else:
        p = Stat(page=page, viewcount=1)
    db.session.add(p)
    print(p.viewcount)
    db.session.commit()


def get_views():
    q = Stat.query.all()
    return ['%s: %s' % (s.page, s.viewcount) for s in q]


@app.route('/')
def index():
    add_page_view('/')
    f = get_fortune('fortunes tao wisdom goedel anarchism platitudes')
    return render_template('index.html', fortune=f)


@app.route('/br')
def br():
    add_page_view('/br')
    f = get_fortune('brasil')
    return render_template('index.html', fortune=f)


if __name__ == '__main__':
    app.run()
