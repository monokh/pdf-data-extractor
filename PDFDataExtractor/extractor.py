from PyPDF2 import PdfFileReader
import yaml
import re
from functools import lru_cache
from PDFDataExtractor.models.definition_field import DefinitionField


class PDFDataExtractor:
    def __init__(self, file, def_file):
        self.file = file
        self.pdf_obj = PdfFileReader(open(self.file, 'rb'))
        self.fields = self._load_definitions(def_file)

    def _normalize_string(self, text):
        if not text:
            return ''

        return text.replace('\t', '').replace('\n', '').strip()

    @lru_cache()
    def _get_page_by_numer(self, number):
        page = self.pdf_obj.getPage(number)
        text = page.extractText()
        return self._normalize_string(text)

    @lru_cache()
    def _get_page_by_pattern(self, pattern):
        for page in self.pdf_obj.pages:
            text = page.extractText()
            text = self._normalize_string(text)
            match = re.search(pattern, text)
            if match:
                return text

    def _find_text(self, find):
        if find.type == 'pageNumber':
            return self._get_page_by_numer(find.value)
        if find.type == 'pagePattern':
            return self._get_page_by_pattern(find.value)

    def _extract_by_pattern(self, text, pattern):
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def _extract_value(self, text, extract):
        if extract.type == 'pattern':
            value = self._extract_by_pattern(text, extract.value)
            return self._normalize_string(value)

    def _transform_list_pattern(self, value, pattern):
        return re.findall(pattern, value)

    def _transform_filter(self, value, contain):
        return [item for item in value if contain in item]

    def _apply_transforms(self, value, transforms):
        transformed_value = value
        for transform in transforms:
            if transformed_value and transform.type == 'listPattern':
                transformed_value = self._transform_list_pattern(transformed_value, transform.value)
            if transformed_value and transform.type == 'filter':
                transformed_value = self._transform_filter(transformed_value, transform.value)
        return transformed_value

    def _get_value(self, field):
        value = None
        text = self._find_text(field.find)
        if text:
            value = self._extract_value(text, field.extract)
            if field.transforms:
                value = self._apply_transforms(value, field.transforms)
        return value

    def get_data(self):
        data = {}
        for field in self.fields:
            field_value = self._get_value(field)
            data[field.name] = field_value
        return data

    def _load_definitions(self, def_file):
        with open(def_file, 'r') as stream:
            try:
                fields = []
                field_obj = yaml.load(stream)['fields']
                for field in field_obj:
                    report_field = DefinitionField(field, field_obj[field])
                    fields.append(report_field)

                return fields
            except yaml.YAMLError as exc:
                print(exc)
