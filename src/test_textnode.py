import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("1", TextType.ITALIC)
        node2 = TextNode("1", TextType.ITALIC, "https://abeaudoin.com")
        node3 = TextNode("1", TextType.BOLD)
        node4 = TextNode("2", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    def test_eq_linq(self):
        node = TextNode("1", TextType.BOLD, "https://abeaudoin.com")
        node2 = TextNode("1", TextType.BOLD, "https://abeaudoin.com")
        self.assertEqual(node, node2)

    def test_print(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://abeaudoin.com")
        text = node.__repr__()
        self.assertEqual(text, "TextNode(This is a text node, bold, https://abeaudoin.com)")

if __name__ == "__main__":
    unittest.main()
