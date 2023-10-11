from flask import Flask, render_template, jsonify
from bot_logic2 import find_arbitrage_opportunities

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_opportunities', methods=['GET'])
def get_opportunities():
    opportunities = find_arbitrage_opportunities()
    return jsonify({'opportunities': opportunities})

if __name__ == "__main__":
    app.run(debug=True)
