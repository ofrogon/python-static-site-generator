import unittest

from helper import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_html_node, extract_title
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png). And even more ![picture](https://i.imgur.com/hH4jfVK.jpeg) that was another."
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("picture", "https://i.imgur.com/hH4jfVK.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://abeaudoin.com) and another [one](https://google.com)..."
        )
        self.assertListEqual([("link", "https://abeaudoin.com"), ("one", "https://google.com")], matches)

    def test_with_link_and_image_mixed(self):
        text = "This is a test with a [link](https://abeaudoin.com) and a ![image](https://i.imgur.com/hH4jfVK.jpeg)"
        self.assertListEqual([("link", "https://abeaudoin.com")], extract_markdown_links(text))
        self.assertListEqual([("image", "https://i.imgur.com/hH4jfVK.jpeg")], extract_markdown_images(text))
 
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://abeaudoin.com) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://abeaudoin.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://google.com"
                ),
            ],
            new_nodes,
        )

    def test_all_text_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   My Title   "), "My Title")

    def test_first_h1_in_document(self):
        md = "Some intro\n\n# The Title\n\nSome content"
        self.assertEqual(extract_title(md), "The Title")

    def test_ignores_h2_and_below(self):
        md = "## Not a title\n### Also not\n# Real Title"
        self.assertEqual(extract_title(md), "Real Title")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Only an h2\n\nSome paragraph")

    def test_empty_raises(self):
        with self.assertRaises(Exception):
            extract_title("")


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        md = "This is **bold** and _italic_ text"
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        p = node.children[0]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.to_html(), "<p>This is <b>bold</b> and <i>italic</i> text</p>")

    def test_heading(self):
        md = "## Hello World"
        node = markdown_to_html_node(md)
        h = node.children[0]
        self.assertEqual(h.tag, "h2")
        self.assertEqual(h.to_html(), "<h2>Hello World</h2>")

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        node = markdown_to_html_node(md)
        pre = node.children[0]
        self.assertEqual(pre.tag, "pre")
        self.assertEqual(pre.to_html(), "<pre><code>print('hello')</code></pre>")

    def test_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        bq = node.children[0]
        self.assertEqual(bq.tag, "blockquote")
        self.assertEqual(bq.to_html(), "<blockquote>This is a quote</blockquote>")

    def test_unordered_list(self):
        md = "- item one\n- item two\n- item three"
        node = markdown_to_html_node(md)
        ul = node.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 3)
        self.assertEqual(ul.to_html(), "<ul><li>item one</li><li>item two</li><li>item three</li></ul>")

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        ol = node.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)
        self.assertEqual(ol.to_html(), "<ol><li>first</li><li>second</li><li>third</li></ol>")

    def test_multiple_blocks(self):
        md = "# Title\n\nA paragraph.\n\n- item one\n- item two"
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "ul")

    def test_inline_markdown_in_list(self):
        md = "- **bold** item\n- _italic_ item"
        node = markdown_to_html_node(md)
        ul = node.children[0]
        self.assertEqual(ul.to_html(), "<ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul>")


if __name__ == "__main__":
    unittest.main()
