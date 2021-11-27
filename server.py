from flask import Flask, request, Response, jsonify, make_response
from config import Config
import json
from flask_cors import CORS, cross_origin
from apis import APIs
from mysqlpool import MysqlPool

dbpool = MysqlPool()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api_mauhy_summary = APIs.api_mauhy_summary
api_mauhy_target = APIs.api_mauhy_target
api_mauhy_month = APIs.api_mauhy_month


@app.route(api_mauhy_month['urls']['getMauHyMonth'])
def getMauHyMonth():
    dt_year = request.args.get('dt_year')
    dt_month = request.args.get('dt_month')
    sql = '''SELECT * FROM %s WHERE dt_year=%s AND dt_month=%s;''' % (api_mauhy_month['name'], dt_year, dt_month)
    data = dbpool.fetch_all(sql)
    return jsonify(data)


@app.route(api_mauhy_summary['urls']['getMauHyLatestYearMonth'])
def getMauHyLatestYearMonth():
    sql_year = '''SELECT MAX(dt_year) AS dt_year FROM %s; ''' % api_mauhy_summary['name']
    data_year = dbpool.fetch_one(sql_year)
    sql = '''SELECT MAX(dt_month) AS dt_month FROM %s WHERE dt_year=%s; ''' % (api_mauhy_summary['name'], data_year['dt_year'])
    data = dbpool.fetch_one(sql)
    data.update(data_year)
    return jsonify(data)


@app.route(api_mauhy_summary['urls']['checkMauHySummary'])
def checkMauHySummary():
    dt_year = request.args.get('dt_year')
    dt_month = request.args.get('dt_month')
    sql = '''SELECT 1 FROM %s WHERE dt_year=%s AND dt_month=%s LIMIT 1;''' % (api_mauhy_summary['name'], dt_year, dt_month)
    data = dbpool.fetch_one(sql)
    if data:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route(api_mauhy_summary['urls']['getMauHySummary'])
def getMauHySummary():
    dt_year = request.args.get('dt_year')
    dt_month = request.args.get('dt_month')
    sql = '''SELECT * FROM %s WHERE dt_year=%s AND dt_month=%s;''' % (api_mauhy_summary['name'], dt_year, dt_month)
    data = dbpool.fetch_all(sql)
    # return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    return jsonify(data)


@app.route(api_mauhy_summary['urls']['getMauHyMaxrate'], methods=['POST'])
def getMauHyMaxrate():
    dt_year = request.args.get('dt_year')
    dt_month = request.args.get('dt_month')
    data_type = request.args.get('data_type')
    name_level = request.args.get('name_level')
    name_labels = request.json['namelabels']
    databack = []
    for name_label in name_labels:
        sql = '''SELECT MAX(phone_rate) AS phone_rate,MAX(login_rate) AS login_rate,MAX(live_rate) AS live_rate,MAX(pphone_rate) AS pphone_rate,MAX(plogin_rate) AS plogin_rate,MAX(plive_rate) AS plive_rate FROM %s WHERE data_type='%s' AND name_level='%s' AND name_label='%s' AND dt_year=%s;''' % (api_mauhy_summary['name'], data_type, name_level, name_label, dt_year)
        data = dbpool.fetch_one(sql)
        row = {'data_type': data_type, 'name_level': name_level, 'name_label': name_label, 'valuemax': [data['phone_rate'],data['login_rate'],data['live_rate'],data['pphone_rate'],data['plogin_rate'],data['plive_rate']]}
        databack.append(row)
    # return Response(json.dumps(databack, ensure_ascii=False), mimetype='application/json')
    return jsonify(databack)


@app.route(api_mauhy_target['urls']['getMauHyTarget'])
def getMauHyTarget():
    dt_year = request.args.get('dt_year')
    dt_month = request.args.get('dt_month')
    sql = '''SELECT * FROM %s WHERE dt_year=%s AND dt_month=%s;''' % (api_mauhy_target['name'], dt_year, dt_month)
    data = dbpool.fetch_all(sql)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9005, debug=True)
