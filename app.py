from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, reqparse
from models import db
from views import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:0000@192.168.31.149:5433/pi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)  # Flask REST Api code

api.add_resource(UniquesView, '/api/uniques')
api.add_resource(UniqueView, '/api/unique/<string:unique>')
api.add_resource(SizesViews, '/api/sizes_view')
api.add_resource(SizeHistoryToSize, '/api/sizes_history/<string:unique>')


app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=4000)
