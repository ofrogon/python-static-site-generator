from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from block import BlockType, block_to_block_type

import re
import os

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unrecognize TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        nodes = old_node.text.split(delimiter)
        if len(nodes) % 2 != 1:
            raise Exception(f"End delimiter ({delimiter}) not found in {old_node.text}")

        for i, v in enumerate(nodes):
            if v == "":
                continue

            if (i % 2) == 0:
                new_nodes.append(TextNode(v, TextType.TEXT))
            else:
                new_nodes.append(TextNode(v, text_type))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    output = [TextNode(text, TextType.TEXT)]
    output = split_nodes_delimiter(output, "**", TextType.BOLD)
    output = split_nodes_delimiter(output, "_", TextType.ITALIC)
    output = split_nodes_delimiter(output, "`", TextType.CODE)
    output = split_nodes_image(output)
    output = split_nodes_link(output)
    return output

def markdown_to_blocks(markdown: str) -> list[str]:
    output = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if len(block) > 0:
            output.append(block.strip())

    return output

def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block))
            case BlockType.HEADING:
                level = len(re.match(r"^(#+)\s", block).group(1))
                text = block[level + 1:]
                node = ParentNode(f"h{level}", text_to_children(text))
            case BlockType.CODE:
                code_text = re.match(r"^```(.*?)```$", block, re.DOTALL).group(1).strip()
                code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
                node = ParentNode("pre", [code_node])
            case BlockType.QUOTE:
                lines = block.splitlines()
                stripped = "\n".join(line.lstrip(">").strip() for line in lines)
                node = ParentNode("blockquote", text_to_children(stripped))
            case BlockType.UNORDERED_LIST:
                items = block.splitlines()
                li_nodes = [ParentNode("li", text_to_children(item[2:])) for item in items]
                node = ParentNode("ul", li_nodes)
            case BlockType.ORDERED_LIST:
                items = block.splitlines()
                li_nodes = [ParentNode("li", text_to_children(re.sub(r"^\d+\.\s", "", item))) for item in items]
                node = ParentNode("ol", li_nodes)
        block_nodes.append(node)

    return ParentNode("div", block_nodes)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)

def extract_title(markdown):
    for line in markdown.splitlines():
        if re.match(r"^# ", line):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))
        elif entry.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, entry[:-3] + ".html")
            generate_page(entry_path, template_path, dest_path)
