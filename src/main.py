from os import path

from core.metadata import Metadata
from core.manager import Manager

from components.channel import Channel
from components.series import Series
from components.episode import Episode

# Instantiate the manager with the path to the root of the file structure
m = Manager(path.abspath('./YouTube'))

# Add the types that the structure uses
m.add_resource(Channel, None)
m.add_resource(Series, Channel)
m.add_resource(Episode, Series)

# Scan to get the items from the structure
m.scan()

# The world is your canvas :)
