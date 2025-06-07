import unittest
import textwrap
from htmlnode import *
from blocktypes import *
from markdown_blocks import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype(self):
        block1 = """##### THIS IS A HEADING TITLE"""
        block2 = """
- this
- is
- an
- unorderder list
""".strip()
        block3 = """
1. this
2. is
3. an
4. ordered list
""".strip()
        block4 = """
1. this
2. is
- a paragraph
""".strip()
        block5 = """```this is code```"""

        quotes = """
>this is true
>sinthia is the most beautiful woman in existence
>and that's facts
""".strip()
        
        self.assertEqual(block_to_blocktype(block1), BlockType.HEADING)
        self.assertEqual(block_to_blocktype(block2), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_blocktype(block3), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype(block4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_blocktype(block5), BlockType.CODE)
        self.assertEqual(block_to_blocktype(quotes), BlockType.QUOTE)

    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
    
    
    
    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class block_to_html(unittest.TestCase):


    def test_paragraphs(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = textwrap.dedent("""
            - Item one
            - Item two
            - Item three
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )
    def test_ordered_list(self):
        md = textwrap.dedent("""
            1. First
            2. Second
            3. Third
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )
    def test_mixed_content(self):
        md = textwrap.dedent("""
            # Header

            Regular paragraph with `inline code`.

            - A list item
            - Another one

            > A quote
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Header</h1><p>Regular paragraph with <code>inline code</code>.</p><ul><li>A list item</li><li>Another one</li></ul><blockquote>A quote</blockquote></div>",
        )

    def test_plain_code_block(self):
        md = textwrap.dedent("""
            ```
            Just plain text
            with no formatting
            ```
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>Just plain text\nwith no formatting\n</code></pre></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_extra_spaces(self):
        self.assertEqual(extract_title("#     Trimmed Heading   "), "Trimmed Heading")

    def test_h1_not_first_block(self):
        markdown = "Some introduction paragraph.\n\n# Actual Title"
        self.assertEqual(extract_title(markdown), "Actual Title")

    def test_multiple_headings_only_first_h1(self):
        markdown = "# First Title\n\n## Subtitle\n\n### Smaller Heading"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_subheading_only_should_raise(self):
        markdown = "## Only Subheading"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 heading found in markdown")

    def test_no_heading_should_raise(self):
        markdown = "Just a regular paragraph.\n\nAnother paragraph."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 heading found in markdown")

    def test_invalid_heading_format_should_raise(self):
        markdown = "#InvalidHeadingWithoutSpace"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 heading found in markdown")

if __name__ == "__main__":
    unittest.main()
