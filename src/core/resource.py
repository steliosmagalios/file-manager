import os
import json
import shutil

from os import path

from .metadata import Metadata
from .utils import create_hidden_file
from .constants import Constants

class Resource:
    
    def __init__(self, resource_id: str, parent_id: str, metadata: Metadata):
        self.id = resource_id
        self.parent = parent_id
        self.metadata = metadata
    
    def __repr__(self):
        return f'{self.get_type()}: {self.get_resource_directory_name()}'
    
    def create(self, root: str):
        # Create the directory
        resource_path = path.join(root, self.get_resource_directory_name())
        os.mkdir(resource_path)

        # Create the subdirectories
        for directory in self.get_subdirectories():
            subdir_path = path.join(resource_path, directory)
            os.mkdir(subdir_path)

        # Create the info.json file
        info_file_path = path.join(resource_path, Constants.INFO_FILE_NAME)
        create_hidden_file(info_file_path, self.toJSON())

    def update(self, root:str, attr_to_update: dict):
        # Get the last known basename before the update
        last_basename = self.get_resource_directory_name()

        # Update the values
        self.update_attributes(attr_to_update)

        # Rename the directory if the basename has changed
        if self.get_resource_directory_name() != last_basename:
            os.rename(path.join(root, last_basename), path.join(root, self.get_resource_directory_name()))

        # Recreate the info.json file
        resource_path = path.join(root, self.get_resource_directory_name())
        info_file_path = path.join(resource_path, Constants.INFO_FILE_NAME)
        create_hidden_file(info_file_path, self.toJSON())

    def remove(self, root: str, remove_directory: bool):
        resource_path = path.join(root, self.get_resource_directory_name())
        if remove_directory:
            # Remove the entire directory
            shutil.rmtree(resource_path)
        else:
            # Just remove the info.json file
            os.remove(path.join(resource_path, Constants.INFO_FILE_NAME))

    def update_attributes(self, attr_to_update: dict):
        for attr in attr_to_update:
            # Check if the attribute can be updated
            if attr in self.get_editable_attributes():
                if attr == 'metadata':
                    self.metadata.update_attributes(attr_to_update[attr])
                else:
                    setattr(self, attr, attr_to_update[attr])

    def get_editable_attributes(self) -> list:
        return ['metadata']

    def get_resource_directory_name(self) -> str:
        raise NotImplementedError('Subclasses need to implement this method')

    def get_subdirectories(self) -> list:
        raise NotImplementedError('Subclasses need to implement this method')

    def get_json_data(self) -> dict:
        raise NotImplementedError('Subclasses need to implement this method')

    def toJSON(self):
        return json.dumps(self.asJSON(), ensure_ascii=False, indent=2)
    
    def asJSON(self):
        return {
            'type': self.get_type(),
            'id': self.id,
            'parent': self.parent,
            'metadata': self.metadata.get_json_data(),
            'other': self.get_json_data()
        }

    @classmethod
    def parse(cls, data):
        args = [data[x] for x in ['id', 'parent']] # Get the ids in args
        args.append(Metadata.parse(data['metadata'])) # Add the metadata to the args
        kwargs = data['other'] if 'other' in data else {} # Create the kwargs
        return cls(*args, **kwargs)
   
    @classmethod
    def get_type(cls) -> str:
        return cls.__name__.lower()
