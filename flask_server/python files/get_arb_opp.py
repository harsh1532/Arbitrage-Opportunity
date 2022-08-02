from pymongo import MongoClient
import certifi
import json 


def get_arbitrage_opps():
    cluster = MongoClient('mongodb+srv://harsh:harsh1234@cluster0.bdk55.mongodb.net/?retryWrites=true&w=majority',
                          tlsCAFile=certifi.where())

    mdb_db = cluster['currency_exchange_data']
    mdb_hist_opp = mdb_db['historic_opportunities']

    arb_ops = []
    for arb_op in mdb_hist_opp.find({}):
        opr_dict = {}
        opr_dict['timestamp'] = arb_op['_id']
        for opr in arb_op['opportunities']:
            opr_dict['src'], path, opr_dict['profit'] = opr['src'], opr['path'], opr['profit']
            opr_dict['dst'] = path[-1][0]

            arb_ops.append(opr_dict)
    print(arb_ops)

    return json.dumps({'oppr': arb_ops})
