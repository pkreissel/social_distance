from flask import Flask, render_template, send_file, make_response
import pandas as pd
from plot import get_data

app = Flask(__name__)

@app.route('/')
def index():
    response = make_response(get_data().to_csv(), 200)
    response.mimetype = "text/plain"
    return response
