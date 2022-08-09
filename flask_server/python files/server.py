from flask import Flask, send_from_directory
from get_arb_opp import get_arbitrage_opps
from flask_cors import CORS, cross_origin


app = Flask(__name__,static_folder='my-app/bulild',static_url_path='')
CORS(app)

@app.route('/members')
def members():
    return {'members': ['m1', 'm2']}

@app.route('/')
def fun():
    return "Don't worry ...your server is live"
@app.route('/arbitrage')
@cross_origin()
def arbitrage():
    print('here')
    print(get_arbitrage_opps())
    print('ieweo')
    return get_arbitrage_opps()
@app.route('/')
@cross_origin() 
def server():
    return send_from_directory(app.static_folder,'index.html')
    

if __name__ == '__main__':
    app.run(debug=True)
