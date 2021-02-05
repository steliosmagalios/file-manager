from core.resource import Resource
from core.metadata import Metadata
from core.constants import Constants

class Episode(Resource):
    
    def __init__(self, resource_id: str, parent_id: str, metadata: Metadata, episode_number=-1, video_id='', category_id=20, uploaded_at=''):
        super().__init__(resource_id, parent_id, metadata)
        self.episode_number = episode_number
        self.video_id = video_id
        self.category_id = category_id
        self.uploaded_at = uploaded_at

    def get_editable_attributes(self):
        return ['episode_number', 'video_id', 'category_id', 'uploaded_at'] + super().get_editable_attributes()

    def get_resource_directory_name(self) -> str:
        return f'{Constants.EPISODE_PREFIX} {self.episode_number:02d}'

    def get_subdirectories(self) -> list:
        return ['Footage', 'Misc']

    def get_json_data(self) -> dict:
        return {
            'episode_number': self.episode_number,
            'video_id': self.video_id,
            'category_id': self.category_id,
            'uploaded_at': self.uploaded_at
        }
