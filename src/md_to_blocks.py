def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block != "":
            cleaned_blocks.append(cleaned_block)
    return cleaned_blocks