from os import path

from core.metadata import Metadata
from core.manager import Manager

from components.channel import Channel
from components.series import Series


m = Manager(path.abspath('./YouTube'))
m.add_resource(Channel, None)
m.add_resource(Series, Channel)

m.scan()

