from os import path

from core.metadata import Metadata
from components.channel import Channel
from core.manager import Manager


m = Manager(path.abspath('./YouTube'))
m.add_resource(Channel, None)

m.create_item('channel', {
    'parent': '',
    'metadata': {
        'name': 'Test Channel Name',
        'tags': ['test tags'],
        'info': 'This is information about a channel.'
    },
    'other': {
        'channel_id': 'testtesttest'
    }
}, True)
