import os
import json

from os import path
from uuid import uuid4

from .metadata import Metadata
from .resource import Resource
from .constants import Constants


class Manager:

    def __init__(self, root: str):
        self.root = root
        self.resources = {}
        self.items = {}

    def update_root(self, new_root: str):
        self.root = new_root
        self.scan()

    def scan(self):
        # Clear the previous structure
        self.items = {}

        for dirpath, dirnames, filenames in os.walk(self.root):
            if Constants.INFO_FILE_NAME in filenames:
                # If the info file exist, create the resource from the file
                with open(path.join(dirpath, Constants.INFO_FILE_NAME), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.create_item(data, create_directory=False) # What should happen if the ids don't match?
            elif dirpath != self.root:
                # If the info file does not exist, all subfolders should be excluded
                dirnames.clear()

    def add_resource(self, resource: Resource, parent: Resource):
        self.resources[resource.get_type()] = {
            'type': resource.get_type(),
            'parent': parent.get_type() if parent != None else None,
            'items': [],
            'class': resource
        }

    def create_item(self, data: dict, create_directory=True) -> Resource:
        # Check if the parent is a valid item
        resource = self.get_resource(data['type'])
        if resource == None or 'parent' not in data:
            return None

        # If we are creating a new item, make a new uuid for the item
        if create_directory:
            data['id'] = uuid4().hex

        # Create the new item's object
        item = None
        if resource != None:
            item = resource['class'].parse(data)
            resource['items'].append(item.id)
            self.items[item.id] = item

        # Create the directory in the disk if needed
        if create_directory and item != None:
            try:
                item.create(self.get_item_directory(item.parent))
            except:
                # If we get an exception on the creating process, rollback the changes
                resource['items'].remove(item.id)
                self.items.pop(item.id)
                return None
        return item

    def update_item(self, data: dict) -> Resource:
        item = self.get_item(data['id'])
        if item != None:
            item.update(self.get_item_directory(item.parent), data)
        return item

    def remove_item(self, item_id: str, remove_directory=False) -> Resource:
        item = self.get_item(item_id)
        if item != None:
            resource = self.get_resource(item.get_type())

            # Remove the item from code
            resource['items'].remove(item.id)
            self.items.pop(item.id)

            # Remove the item from the disk
            item.remove(self.get_item_directory(item.parent), remove_directory)
        return item

    def has_resource(self, resource_type: str) -> bool:
        return resource_type in self.resources

    def get_resource(self, resource_type: str) -> dict:
        return self.resources[resource_type] if self.has_resource(resource_type) else None
    
    def has_item(self, item_id: str) -> bool:
        return item_id in self.items

    def get_item(self, item_id: str) -> Resource:
        return self.items[item_id] if self.has_item(item_id) else None

    def get_item_directory(self, item_id: str) -> str:
        if not item_id:
            return self.root
        item = self.get_item(item_id)
        return path.join(self.get_item_directory(item.parent), item.get_resource_directory_name())

    def get_items(self, predicate=lambda x: x) -> list:
        return list(filter(predicate, self.items.values()))

    def get_resources(self, predicate=lambda x: x) -> list:
        return [{k : r[k] for k in ['type', 'parent']} for r in self.resources.values()]
