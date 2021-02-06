import zerorpc

from os import path

from core.metadata import Metadata
from core.manager import Manager

from components.channel import Channel
from components.series import Series
from components.episode import Episode

from api.manager_api import ManagerAPI

# Instantiate the manager with the path to the root of the file structure
m = Manager(path.abspath('./YouTube'))

# Add the types that the structure uses
m.add_resource(Channel, None)
m.add_resource(Series, Channel)
m.add_resource(Episode, Series)

# Scan to get the items from the structure
m.scan()

server = zerorpc.Server(ManagerAPI(m))
server.bind('tcp://127.0.0.1:5000')
server.run()
