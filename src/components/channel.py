from core.resource import Resource
from core.metadata import Metadata

class Channel(Resource):
    
    def __init__(self, resource_id: str, parent_id: str, metadata: Metadata, channel_id = ''):
        super().__init__(resource_id, parent_id, metadata)
        self.channel_id = channel_id

    def get_editable_attributes(self):
        return ['channel_id'] + super().get_editable_attributes()

    def get_resource_directory_name(self) -> str:
        return self.metadata.name

    def get_subdirectories(self) -> list:
        return ['Misc']

    def get_json_data(self) -> dict:
        return {
            'channel_id': self.channel_id
        }
