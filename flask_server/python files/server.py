from flask import Flask
from get_arb_opp import get_arbitrage_opps


app = Flask(__name__)


@app.route('/members')
def members():
    return {'members': ['m1', 'm2']}

@app.route('/')
def fun():
    return "Don't worry ...your server is live"
@app.route('/arbitrage')
def arbitrage():
    print('here')
    print(get_arbitrage_opps())
    print('ieweo')
    return get_arbitrage_opps()
    
    

if __name__ == '__main__':
    app.run(debug=True)
