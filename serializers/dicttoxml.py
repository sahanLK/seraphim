try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable



class DictToXML:
    def __init__(
            self, 
            dictionary: dict,
            root_name: str,
            root_attributes: dict = {},
            xml_version: str = "1.0", 
            encoding: str = "utf-8",
        ):
        self.version = xml_version
        self.encoding = encoding
        self.data = dictionary  # The dictionary to be converted
        self.root_name = root_name
        self.root_attributes = root_attributes

    def get_prolog(self) -> str:
        """
        Constructs the xml declaration like below.
        <?xml version="1.0" encoding="utf-8"?>
        """
        return '<?xml version="{}" encoding="{}"?>'.format(self.version, self.encoding)
    
    def get_xml_root() -> str: ...
    
    def add_root(self, xml_str: str) -> str:
        """
        @param: xml_str: xml string to be enclosed within the root node.
        """
        attrib = ""

        for k, v in self.root_attributes.items():
            attrib += ' {}="{}"'.format(k, v)
        return '<{} {}>{}</{}>'.format(self.root_name, attrib, xml_str, self.root_name)

    @staticmethod
    def is_collection(value) -> bool:
        return isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray))
    
    @staticmethod
    def sanitize(val: str) -> str:
        entity_map = {
            '<': "&lt;",
            '>': "&gt;",
            '&': "&amp;",
            "'": "&apos;",
            '"': "&quot;"
        }
        replace = [v for v in set(str(val)) if v in entity_map.keys()]
        sanitized = val

        for char in replace:
            sanitized = sanitized.replace(char, entity_map[char])
        return sanitized

    def __build_xml_tree(self, data):
        """
        Recursively builds the XML tree.
        """
        output = ''

        for key, value in data.items():
            if isinstance(value, dict):
                output += "<{}>{}</{}>".format(
                    key, self.__build_xml_tree(value), key)
            elif isinstance(value, dict):
                for item in value:
                    output += "<{}>{}</{}>".format(
                        key, self.__build_xml_tree(item), key)
            elif self.is_collection(value):
                for item in value:
                    output += self.__build_xml_tree({key: item})
            else:
                output += "<{}>{}</{}>".format(
                    key, "" if value is None else self.sanitize(value), key)
        return output
    
    @staticmethod
    def prettify(): ...
    
    def get_xml(self, prolog=True):
        xml_out = self.add_root(self.__build_xml_tree(self.data))
        if not prolog:
            return xml_out
        prolog = self.get_prolog()
        return "{}{}".format(prolog, xml_out)

