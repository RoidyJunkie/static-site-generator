from textnode import TextNode, TextType
from image_link_extractor import extract_markdown_images, extract_markdown_link

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        splitted_node = node.text.split(delimiter)
        if len(splitted_node) % 2 == 0:
            raise ValueError("Delimiter has no matching closing character!")
        for i in range(0, len(splitted_node)): 
            if splitted_node[i] == "":
                continue
            if i % 2 == 0:
                new_text = TextNode(splitted_node[i], TextType.TEXT)
                result.append(new_text)
            else:
                delimited_node = TextNode(splitted_node[i], text_type=text_type)
                result.append(delimited_node)
    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        matches: list[tuple[str, str]] = extract_markdown_images(old_node.text)
        remaining = old_node.text
        for image_alt, image_url in matches:
            before, remaining = remaining.split(f"![{image_alt}]({image_url})", 1)
            if before != "":
                result.append(TextNode(before, TextType.TEXT,))
            result.append(TextNode(image_alt, TextType.IMAGE, image_url))
        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT,))        
    return result

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        matches: list[tuple[str, str]] = extract_markdown_link(old_node.text)
        remaining = old_node.text
        for link_text, link_url in matches:
            before, remaining = remaining.split(f"[{link_text}]({link_url})", 1)
            if before != "":
                result.append(TextNode(before, TextType.TEXT,))
            result.append(TextNode(link_text, TextType.LINK, link_url))
        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT,))        
    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    first_iter = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    sec_iter = split_nodes_delimiter(first_iter, "_", TextType.ITALIC)
    third_iter = split_nodes_delimiter(sec_iter, "`", TextType.CODE)
    fourth_iter = split_nodes_image(third_iter)
    final_iter = split_nodes_link(fourth_iter)
    return final_iter