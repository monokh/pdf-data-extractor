from PDFDataExtractor.models.type_value_pair import TypeValuePair


class DefinitionField:
    def __init__(self, name, data):
        self.name = name
        self.find = TypeValuePair(data.get('find'))
        self.extract = TypeValuePair(data.get('extract'))
        self.transforms = None
        if data.get('transforms'):
            self.transforms = [TypeValuePair(transform) for transform in data.get('transforms')]
