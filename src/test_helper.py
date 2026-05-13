import unittest

from helper import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://abeaudoin.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://abeaudoin.com")

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://abeaudoin.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props["src"], "https://abeaudoin.com")
        self.assertEqual(html_node.props["alt"], "This is a image node")

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is a node with **bold text** in it", TextType.TEXT)
        splitted = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(splitted), 3)
        self.assertEqual(splitted[0].text_type, TextType.TEXT)
        self.assertEqual(splitted[1].text_type, TextType.BOLD)
        self.assertEqual(splitted[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_bold_end(self):
        node = TextNode("This is a node with **bold text**", TextType.TEXT)
        splitted = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(splitted), 2)
        self.assertEqual(splitted[0].text_type, TextType.TEXT)
        self.assertEqual(splitted[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is a node with _italic text_ in it", TextType.TEXT)
        splitted = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(splitted), 3)
        self.assertEqual(splitted[0].text_type, TextType.TEXT)
        self.assertEqual(splitted[1].text_type, TextType.ITALIC)
        self.assertEqual(splitted[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is a node with `code text` in it", TextType.TEXT)
        splitted = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(splitted), 3)
        self.assertEqual(splitted[0].text_type, TextType.TEXT)
        self.assertEqual(splitted[1].text_type, TextType.CODE)
        self.assertEqual(splitted[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_not_txt_node(self):
        node = TextNode("This is a node with `code text` in it", TextType.BOLD)
        splitted = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(splitted), 1)
        self.assertEqual(splitted[0].text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
