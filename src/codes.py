import re
from textnode import *
from htmlnode import *
from blocktypes import BlockType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        current_index = 0
        result_nodes = []

        while current_index < len(text):
            start_index = text.find(delimiter, current_index)

            if start_index == -1:
                if current_index < len(text):
                    result_nodes.append(TextNode(text[current_index:], TextType.TEXT))
                    break
            
            if start_index > current_index:
                result_nodes.append(TextNode(text[current_index:start_index], TextType.TEXT))
            
            end_index = text.find(delimiter, start_index + len(delimiter))

            if end_index == -1:
                raise Exception(f"No closing delimiter found for {delimiter}")

            delimiter_content = text[start_index + len(delimiter): end_index]

            result_nodes.append(TextNode(delimiter_content, text_type))

            current_index = end_index + len(delimiter)
        
        new_nodes.extend(result_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            new_nodes.append(nodes)
            continue

        text = nodes.text
        images = extract_markdown_images(text)

        if images == []:
            new_nodes.append(nodes)
            continue

        for image_alt, image_link in images:
            
            markdown_image = f"![{image_alt}]({image_link})"
            sections = text.split(markdown_image, 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes            
            
def split_nodes_link(old_nodes):
    new_nodes = []

    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            new_nodes.append(nodes)
            continue

        text = nodes.text
        links = extract_markdown_links(text)

        if links == []:
            new_nodes.append(nodes)
            continue

        for alt, link in links:
            
            markdown_link = f"[{alt}]({link})"
            sections = text.split(markdown_link, 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, link))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes              

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" , text)
    return matches

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
            return LeafNode("img", "", {"src": f'{text_node.url}', "alt": f'{text_node.text}'})
        case _:
            raise Exception("text doesn't match any format")



