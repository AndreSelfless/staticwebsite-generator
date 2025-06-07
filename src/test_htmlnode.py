import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("A tag", "a value")
        node2 = HTMLNode("a tag", "a value", ["a children", "another children"])
        node3 = HTMLNode("a tag", "a value", ["a children", "another children"])
        # A node with props to test props_to_html
        link_node = HTMLNode("a", "Click me!", None, {"href": "https://boot.dev", "target": "_blank"})
        # A node with multiple props
        image_node = HTMLNode("img", None, None, {"src": "image.jpg", "alt": "An image", "width": "500"})
        # A node with no props
        plain_node = HTMLNode("p", "Just a paragraph")
        # Testing representation
        nested_node = HTMLNode("div", None, [HTMLNode("span", "Hello")], {"class": "container"})
    
        # Test with multiple props
        link_props = link_node.props_to_html()
        assert ' href="https://boot.dev" target="_blank"' in link_props or ' target="_blank" href="https://boot.dev"' in link_props
    
         # Test with no props
        assert plain_node.props_to_html() == ""

         # Test with more props
        img_props = image_node.props_to_html()
        # Check that all required attributes are in the result
        assert 'src="image.jpg"' in img_props
        assert 'alt="An image"' in img_props
        assert 'width="500"' in img_props

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode("img", "",{"src": "https://imgur.snthspic", "alt": "some pics"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node3.to_html(), '<img src="https://imgur.snthspic" alt="some pics"/>' )
    def test_leaf_node_with_none_value(self):
    # Test that a ValueError is raised when value is None
        with self.assertRaises(ValueError):
            node = LeafNode("div", None)
            node.to_html()

    def test_leaf_node_with_no_tag(self):
    # Test that raw text is returned when tag is None
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
        
    def test_parent_node_with_no_children(self):
        """Test that a ParentNode with an empty children list works correctly"""
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_node_with_props(self):
        """Test that a ParentNode correctly renders HTML props"""
        parent_node = ParentNode("div", [], {"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="container" id="main"></div>')

    def test_parent_node_with_multiple_children(self):
        """Test a parent with multiple children at the same level"""
        parent_node = ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "Item 1")]),
            ParentNode("li", [LeafNode(None, "Item 2")]),
            ParentNode("li", [LeafNode(None, "Item 3")])
            ])
        self.assertEqual(
            parent_node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
            )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2= TextNode("you know google?", TextType.LINK, "www.google.com")
        node3 = TextNode("here's a nice pic", TextType.IMAGE, "https://imgur.asjdjs")
        node4 = TextNode("very bold indeed", TextType.BOLD)
        italic_node = TextNode("you feeling fancy?", TextType.ITALIC)
        raiser_node = TextNode("this raises exception", None)
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)
        html_node4 = text_node_to_html_node(node4)
        italic_html = text_node_to_html_node(italic_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "a")
        self.assertEqual(html_node3.tag, "img")
        self.assertEqual(html_node3.props, {"src": "https://imgur.asjdjs", "alt": "here's a nice pic"})
        self.assertEqual(html_node4.tag, "b")
        self.assertEqual(italic_html.tag, "i")
        self.assertEqual(italic_html.to_html(), "<i>you feeling fancy?</i>")
        with self.assertRaises(Exception):
            text_node_to_html_node(raiser_node)

if __name__ == "__main__":
    unittest.main()