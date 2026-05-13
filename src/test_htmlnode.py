import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_print_simple(self):
        node = HTMLNode("p", "This is the value")
        text = node.__repr__()
        self.assertEqual(text, '<p>This is the value</p>')

    def test_print_empty(self):
        node = HTMLNode()
        text = node.__repr__()
        self.assertEqual(text, '')

    def test_print_with_children_and_props(self):
        children_node = []
        children_node.append(HTMLNode("p", "This is some text"))
        props = {
            "class": "presenter",
            "style": "display: inline-block"
        }
        node = HTMLNode("div", "This is the value", children_node, props)
        text = node.__repr__()
        self.assertEqual(text, '<div class="presenter" style="display: inline-block">This is the value<p>This is some text</p></div>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link", {"href": "https://abeaudoin.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://abeaudoin.com" target="_blank">This is a link</a>')

    def test_leaf_to_html_text_only(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"class": "something"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="something"><span><b>grandchild</b></span></div>',
        )

if __name__ == "__main__":
    unittest.main()
