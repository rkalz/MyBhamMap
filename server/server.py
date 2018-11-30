from flask import Flask, g, render_template
app = Flask(__name__, template_folder='templates')

from internet_operations import fetch_data_from_web
from local_calculations import calculate_path

import sys

@app.before_first_request
def load_db():
    from graph_builder.build_directed_graph import import_directed_graph
    g.db = import_directed_graph("my_bham_map_graph.json")
    print("Loaded DB", file=sys.stderr)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/directions', methods=["POST"])
def directions():
    return "test"
