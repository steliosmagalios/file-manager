from os import path
from uuid import uuid4

from .metadata import Metadata
from .resource import Resource


class Manager:

    def __init__(self, root: str):
        self.root = root
        self.resources = {}
        self.items = {}

    def update_root(self, new_root: str):
        self.root = new_root
        self.scan()

    def scan(self):
        pass

    def add_resource(self, resource: Resource, parent: Resource):
        self.resources[resource.get_type()] = {
            'type': resource.get_type(),
            'parent': parent.get_type() if parent != None else None,
            'items': [],
            'class': resource
        }

    def create_item(self, resource_type: str, data: dict, create_directory=True):
        # If we are creating a new item, make a new uuid for the item
        if create_directory:
            data['id'] = uuid4().hex

        # Create the new item's object
        resource = self.get_resource(resource_type)
        item = None
        if resource != None:
            item = resource['class'].parse(data)
            resource['items'].append(item.id)
            self.items[item.id] = item

        # Create the directory in the disk if needed
        if create_directory and item != None:
            try:
                item.create(self.get_item_directory(item.parent))
            except Exception as ex:
                print(ex)
                # If we get an exception on the creating process, rollback the changes
                resource['items'].remove(item.id)
                self.items.pop(item.id)
                print('Error Enountered')
            print('Created item')

    def update_item(self, resource: Resource, data: dict):
        pass

    def remove_item(self, resource: Resource, data: dict, remove_directory=False):
        pass

    def has_resource(self, resource_type: str) -> bool:
        return resource_type in self.resources

    def get_resource(self, resource_type: str):
        return self.resources[resource_type] if self.has_resource(resource_type) else None
    
    def has_item(self, item_id: str) -> bool:
        return item_id in self.items

    def get_item(self, item_id: str) -> Resource:
        return self.items[item_id] if self.has_item(item_id) else None

    def get_item_directory(self, item_id: str):
        if not item_id:
            return self.root
        item = self.get_item(item_id)
        return path.join(self.get_item_directory(item.parent), item.get_resource_directory_name())
