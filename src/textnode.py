#src/classes/textnode.py
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "Plain text"
    BOLD = "Bold text"
    ITALIC = "Italicized text"
    CODE = "Code text"
    LINK = "Link"
    IMAGE = "Image"


class TextNode():
    text: str
    text_type: TextType
    url: str | None
    
    def __init__(self, text, text_type, url=None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other):
        return (self.url == other.url) and (self.text == other.text) and (self.text_type == other.text_type)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text,)
        case TextType.BOLD:
            return LeafNode("b", text_node.text,)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text,)
        case TextType.CODE:
            return LeafNode("code", text_node.text,)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "",{"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"{text_node.text_type} is not a supported TextType")
    