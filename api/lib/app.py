from flask import Flask, request
from redis import Redis
from cassandra.cluster import Cluster
from uuid import uuid1
import os
import json

app = Flask(__name__)
r = None

# connect to cassandra cluster and insert report data
cluster = None
session = None
insertStmt = None

CREATE_KEYSPACE = "create keyspace if not exists simulations with replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
CREATE_SIMULATIONS_TABLE = "create table if not exists simulations.reports(id uuid, spellName text, casterLevel int, reportdata map<text, text>, primary key ((spellName, casterLevel), id));"
INSERT_REPORT = "insert into reports(id, spellName, casterLevel, reportdata) values (?, ?, ?, ?);"

def get_redis():
    global r
    if r == None:
        r = Redis(host=os.getenv('REDISADDRESS'), port=6379, db=0)
    return r

def init_db():
    # initialize the cluster connection
    cluster = Cluster(json.loads(os.getenv('CASSANDRACLUSTERADDRESSES')))

    # begin our session
    global session
    session = cluster.connect()

    # make sure we have a keyspace and connect to simulations
    session.execute(CREATE_KEYSPACE)
    session = cluster.connect('simulations')

    # make sure we have a table
    session.execute(CREATE_SIMULATIONS_TABLE)

    # prepare our insert statement
    global insertStmt
    insertStmt = session.prepare(INSERT_REPORT)

@app.route('/sim', methods=['POST', 'GET'])
def sim():
    if request.method == 'POST':
        data = request.json
        get_redis().rpush('sims', data['name'])
        return data['name']
    else:
        name = get_redis().lpop('sims')
        if name:
            return name
        else:
            return "empty"

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    spellName = data['spellName']
    casterLevel = data['casterLevel']
    reportData = data['reportData']
    
    # insert the report
    global insertStmt
    session.execute(insertStmt, (uuid1(), spellName, casterLevel, reportData))

    return 'received'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')