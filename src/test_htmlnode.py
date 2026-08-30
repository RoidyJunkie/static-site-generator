#src/tests/test_htmlnode.py
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import extract_title
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode("linked text", None, None, {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        html_node2 = HTMLNode("linked text", None, None, None)
        html_node3 = HTMLNode("linked text", None, None, {
            "href": "https://www.google.com",
            "target": "_blank",
            "color": "#FFFFFF"
        })

        self.assertEqual(html_node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(html_node2.props_to_html(), "")
        self.assertEqual(html_node3.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\" color=\"#FFFFFF\"")
         

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("p", "Hello, world!", {"color": "red"})
        self.assertEqual(node2.to_html(), '<p color="red">Hello, world!</p>')

        node3 = LeafNode("", "Hello, world!")
        self.assertEqual(node3.to_html(), "Hello, world!")

        node4 = LeafNode("b", "Hello!", {"color": "yellow", "width": "45px"})
        self.assertEqual(node4.to_html(), '<b color="yellow" width="45px">Hello!</b>')

        node5 = LeafNode("i", "Hello!", {"color": "yellow", "width": "45px"})
        self.assertEqual(node5.to_html(), '<i color="yellow" width="45px">Hello!</i>')

        node6 = LeafNode("img", "bird", {
                "src": "https://wildambience.com/wp-content/uploads/2021/07/Wild-Ambience_Great_Tit.jpg",
                "alt": "image of great tit bird"
            }
        )
        self.assertEqual(node6.to_html(), '<img src="https://wildambience.com/wp-content/uploads/2021/07/Wild-Ambience_Great_Tit.jpg" alt="image of great tit bird">bird</img>')

        node7 = LeafNode("link", "cool site", {"href": "https://www.mandalagaba.com"})
        self.assertEqual(node7.to_html(), '<link href="https://www.mandalagaba.com">cool site</link>')

        self.assertNotEqual(node.to_html(), "")
        self.assertNotEqual(node2.to_html(), node.to_html())
        self.assertNotEqual(node3.to_html(), node2.to_html())
        self.assertNotEqual(node4.to_html(), node5.to_html())
        self.assertNotEqual(node7.to_html(), node6.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        child_node = LeafNode("b", "This is a bold paragraph with cyan coloring, width of 15px, and 10px of height", {
                "color": "cyan",
                "height": "10px",
                "width": "15px"
            }
        )
        parent_node = ParentNode("p", [child_node], {"padding": "5px", "border": "1px solid #999999"})
        self.assertEqual(parent_node.to_html(), '<p padding="5px" border="1px solid #999999"><b color="cyan" height="10px" width="15px">This is a bold paragraph with cyan coloring, width of 15px, and 10px of height</b></p>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        grandchild_node = LeafNode("a", "cool site", {"href": "https://www.bored.com/arcade/zen-garden/", "color": "#964999"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><a href="https://www.bored.com/arcade/zen-garden/" color="#964999">cool site</a></span></div>')

    def test_extract_title(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual("Hello", result)

        markdown = """
# # This is a heading with 2 seperated #'s
"""
        result = extract_title(markdown)
        self.assertEqual("# This is a heading with 2 seperated #'s", result)

        markdown = """
Normal paragraph 

# ###Heading3

#Heading4
"""
        result = extract_title(markdown)
        self.assertEqual("###Heading3", result)

        markdown = """
##Bullshit

Bullshit

###Bullshit
"""
        with self.assertRaises(ValueError) as e:
             extract_title(markdown)
        self.assertEqual(str(e.exception), "No actual h1 headings found")

        markdown = """
Horseshit
horseshit
horseshit
"""
        with self.assertRaises(ValueError) as e:
             extract_title(markdown)
        self.assertEqual(str(e.exception), "No actual h1 headings found")
if __name__ == "__main__":
	unittest.main()
