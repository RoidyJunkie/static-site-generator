from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from nodesplitter import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "Paragraph block", 
    HEADING = "Heading block", 
    CODE = "Code block", 
    QUOTE = "Quote block",
    UNORDERED_LIST = "Unordered list block", 
    ORDERED_LIST = "Ordered list block"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block != "":
            cleaned_blocks.append(cleaned_block)
    return cleaned_blocks

def block_to_block_type(markdown: str) -> BlockType:
    lines = markdown.split("\n")
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and (lines[0].startswith("```") and lines[-1].endswith("```")):
        return BlockType.CODE 
    elif markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif markdown.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def block_type_to_ParentNode(block_text: str, block_type: BlockType) -> ParentNode:
    match(block_type):
        case BlockType.QUOTE:
            lines = block_text.split("\n")
            stripped: list[str] = []
            for line in lines:
                line = line.removeprefix(">").removeprefix(" ")
                stripped.append(line)
            block_text = " ".join(stripped)
            return ParentNode("blockquote", text_to_children(block_text))
        case BlockType.UNORDERED_LIST:
            lines = block_text.split("\n")
            items = []
            for line in lines:
                text = line.removeprefix("- ")
                items.append(ParentNode("li", text_to_children(text)))
            return ParentNode("ul", items)
        case BlockType.ORDERED_LIST:
            lines = block_text.split("\n")
            items = []
            i = 1
            for line in lines:
                text = line.removeprefix(f"{i}. ")
                items.append(ParentNode("li", text_to_children(text)))
                i += 1
            return ParentNode("ol", items)
        case BlockType.CODE:
            text = block_text.removeprefix("```\n").removesuffix("```")
            raw = TextNode(text, TextType.TEXT)
            code_child = text_node_to_html_node(raw)
            return ParentNode("pre", [ParentNode("code", [code_child])])
        case BlockType.HEADING:
            marker, text = block_text.split(" ", 1)
            return ParentNode(f"h{len(marker)}", text_to_children(text))
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block_text.replace("\n", " ")))


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown=markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_type_to_ParentNode(block, block_type=block_type)
        children.append(block_node)
    return ParentNode("div", children=children)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise ValueError("No actual h1 headings found")

