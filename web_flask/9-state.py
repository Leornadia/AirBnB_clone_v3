#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """
    Displays an HTML page with a list of all states
    """
    states = storage.all('State').values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state(id):
    """
    Displays an HTML page with details of a specific state
    """
    state = storage.get('State', id)
    if state:
        cities = state.cities
        return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html', state=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
