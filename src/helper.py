from textnode import TextNode, TextType
from htmlnode import LeafNode

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


