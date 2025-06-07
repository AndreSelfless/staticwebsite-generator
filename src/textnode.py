from enum import Enum


class TextType(Enum):
    TEXT = "normal text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code"
    LINK = "link"
    IMAGE = "images"


class TextNode():
    def __init__(self, text, TextType, url=None):
        self.text = text
        self.text_type = TextType
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
