from textnode import TextType, TextNode
import re

def extract_markdown_images(input: str) -> list[tuple[str, str]]: 
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", input)
    return matches

def extract_markdown_link(input: str) -> list[tuple[str, str]]: 
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", input)
    return matches
                        