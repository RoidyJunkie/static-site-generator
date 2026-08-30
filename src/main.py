from textnode import TextNode, TextType
from htmlnode import HTMLNode
from markdown_blocks import markdown_to_html_node, extract_title
from pathlib import Path
import os, shutil




def copy_dir_contents(src: str, dest: str, call_tracker=1):
    if call_tracker == 1 and os.path.exists(dest):
        shutil.rmtree(os.path.relpath(dest))
    if not os.path.exists(dest):
        os.mkdir(dest)
    if os.path.exists(os.path.relpath(src)): 
        for subpath in os.listdir(os.path.relpath(src)):
            source_path, destination_path = os.path.join(src, subpath), os.path.join(dest, subpath)
            if os.path.isdir(source_path):
                print(f"Creating {source_path} to {destination_path} as a directory")
                copy_dir_contents(source_path, destination_path, call_tracker = call_tracker + 1)
            if os.path.isfile(source_path):
                print(f"Copying {source_path} to {destination_path} as a file")
                shutil.copy(source_path, destination_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_md, temp_html= "", ""
    with open(from_path, "r") as file:
        from_md = file.read()
    with open(template_path, "r") as file:
        temp_html = file.read()
    from_html = markdown_to_html_node(from_md).to_html()
    title = extract_title(from_md)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    full_html = temp_html.replace("{{ Title }}", title).replace("{{ Content }}", from_html)
    with open(dest_path, "w") as file:
        file.write(full_html)
        file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        full_content_path = os.path.join(dir_path_content, entry)
        full_dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(full_content_path):
            generate_page(full_content_path, template_path, Path(full_dest_path).with_suffix(".html"))
        else:
            generate_pages_recursive(full_content_path, template_path, full_dest_path)




def main():
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    copy_dir_contents("static", "public", call_tracker=1)
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()