from flask import Flask, render_template, url_for, request, redirect, session, g
import spotify

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def index():
    x = spotify.get_stuff()
    return render_template('index.html', s=x['s'], a=x['a'], lb=x['lb'], ac=x['ac'],tc=x['tc'])


if __name__ == '__main__':
    app.run(debug=True)
