
class Metadata:

    def __init__(self, name='', tags=[], info=''):
        self.name = name
        self.tags = tags
        self.info = info

    def get_json_data(self) -> dict:
        return {
            'name': self.name,
            'tags': self.tags,
            'info': self.info
        }
    
    def update_attributes(self, attr_to_update: dict):
        for attr in attr_to_update:
            # Check if the attribute can be updated
            if attr in ['name', 'tags', 'info']: 
                setattr(self, attr, attr_to_update[attr])

    @classmethod
    def parse(cls, data):
        return cls(**data)
