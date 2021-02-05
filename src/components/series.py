from core.resource import Resource
from core.metadata import Metadata

class Series(Resource):
    
    def __init__(self, resource_id: str, parent_id: str, metadata: Metadata, playlist_id = ''):
        super().__init__(resource_id, parent_id, metadata)
        self.playlist_id = playlist_id

    def get_editable_attributes(self):
        return ['playlist_id'] + super().get_editable_attributes()

    def get_resource_directory_name(self) -> str:
        return self.metadata.name

    def get_subdirectories(self) -> list:
        return ['Misc']

    def get_json_data(self) -> dict:
        return {
            'playlist_id': self.playlist_id
        }
