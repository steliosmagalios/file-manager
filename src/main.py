from core.metadata import Metadata
from components.channel import Channel

import time

c = Channel('test', '', Metadata('McNoob', [], ''), 'test')
# c.create('YouTube')

# time.sleep(5)

c.update('YouTube', {
    'parent': 'poop',
    'metadata': {
        'name': 'McPoop'
    }
})
