from core.manager import Manager
from core.resource import Resource


class ManagerAPI(object):

    def __init__(self, manager: Manager):
        self.manager = manager

    def echo(self, message):
        return message

    def set_root(self, new_root: str):
        self.manager.update_root(new_root)

    def get_item(self, item_id: str) -> Resource:
        return self.manager.get_item(item_id).toJSON()

    def has_item(self, item_id: str) -> bool:
        return self.manager.has_item(item_id)

    def create_item(self, data: dict) -> Resource:
        return self.manager.create_item(data).toJSON()

    def update_item(self, data: dict) -> Resource:
        return self.manager.update_item(data).toJSON()

    def remove_item(self, item_id: str, remove_directory: bool) -> Resource:
        return self.manager.remove_item(item_id, remove_directory=remove_directory).toJSON()
