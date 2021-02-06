import sys
import json

from os import path

from flask import Flask, request

from core.metadata import Metadata
from core.manager import Manager

from components.channel import Channel
from components.series import Series
from components.episode import Episode

app = Flask(__name__)

# Instantiate the manager with the path to the root of the file structure
m = Manager(path.abspath('./YouTube'))

# Add the types that the structure uses
m.add_resource(Channel, None)
m.add_resource(Series, Channel)
m.add_resource(Episode, Series)

# Scan to get the items from the structure
m.scan()

def create_json_response(data, status=200):
    res = app.response_class(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def get_as_json(data):
    return list(map(lambda x: x.asJSON(), data))

@app.route('/api/<item_id>')
def fetch_item(item_id):
    item = m.get_item(item_id)
    return create_json_response(
        item.asJSON() if item != None else {'message': 'Not available'}
    )

@app.route('/api/items/<resource_type>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_resource(resource_type):
    if request.method == 'GET':
        return create_json_response(get_as_json(m.get_items(lambda x: x.get_type() == resource_type)))
    else:
        body = request.get_json()
        item = None
        if request.method == 'POST':
            item = m.create_item(body)
        elif request.method == 'PUT':
            item = m.update_item(body)
        elif request.method == 'DELETE':
            item = m.remove_item(request.args.get('id'), request.args.get('remove_directory') == 'true')

        if item != None:
            return create_json_response(item.asJSON())
        else:
            return create_json_response({'message': 'Item not created'}, status=403)

@app.route('/api/items')
def fetch_all_items():
    return create_json_response( get_as_json(m.get_items()))

@app.route('/api/resources')
def fetch_all_resources():
    return create_json_response(m.get_resources())

if __name__ == '__main__':
    app.run()
