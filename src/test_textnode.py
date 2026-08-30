#src/tests/test_textnode.py
import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from image_link_extractor import extract_markdown_images, extract_markdown_link
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestTextNode(unittest.TestCase):
	def test_not_eq(self):
		node = TextNode("This is a bold text node", TextType.BOLD)
		node2 = TextNode("This is a different bold text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

		node = TextNode("This is a plain text node", TextType.TEXT)
		node2 = TextNode("This is a different plain text node", TextType.TEXT)
		self.assertNotEqual(node, node2)

		node = TextNode("This is an italic text node", TextType.ITALIC)
		node2 = TextNode("This is a different italic text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

		node = TextNode("This is a code node", TextType.CODE)
		node2 = TextNode("This is a different code node", TextType.CODE)
		self.assertNotEqual(node, node2)

		node = TextNode("This is a link node", TextType.LINK)
		node2 = TextNode("This is a different link node", TextType.LINK)
		self.assertNotEqual(node, node2)

		node = TextNode("This is an image node", TextType.IMAGE)
		node2 = TextNode("This is a different image node", TextType.IMAGE)
		self.assertNotEqual(node, node2)

		node3 = TextNode("This an edge case for different types", TextType.LINK)
		node4 = TextNode("This an edge case for different types", TextType.IMAGE)
		self.assertNotEqual(node3, node4)
				
	def test_eq(self):
		node = TextNode("This is a bold text node", TextType.BOLD)
		node2 = TextNode("This is a bold text node", TextType.BOLD)
		self.assertEqual(node, node2)
	
		node = TextNode("This is a plain text node", TextType.TEXT)
		node2 = TextNode("This is a plain text node", TextType.TEXT)
		self.assertEqual(node, node2)
	
		node = TextNode("This is an italic text node", TextType.ITALIC)
		node2 = TextNode("This is an italic text node", TextType.ITALIC)
		self.assertEqual(node, node2)
	
		node = TextNode("This is a code node", TextType.CODE)
		node2 = TextNode("This is a code node", TextType.CODE)
		self.assertEqual(node, node2)
	
		node = TextNode("This is a link node", TextType.LINK)
		node2 = TextNode("This is a link node", TextType.LINK)
		self.assertEqual(node, node2)
	
		node = TextNode("This is an image node", TextType.IMAGE)
		node2 = TextNode("This is an image node", TextType.IMAGE)
		self.assertEqual(node, node2)	

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold_text(self):
		node = TextNode("This is a bold text node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold text node")

	def test_italic_text(self):
		node = TextNode("This is an italic text node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic text node")

	def test_code_text(self):
		node = TextNode("This is a code text node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code text node")

	def test_link_node(self):
		node = TextNode("This is a link", TextType.LINK, "https://www.forgotten-hill.com/")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link")
		self.assertEqual(html_node.props, {"href": "https://www.forgotten-hill.com/"})

	def test_image_node(self):
		node = TextNode("Image of a peregrine falcon", TextType.IMAGE, "https://images.unsplash.com/photo-1556597386-347226bd1776?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.props, {
			"src": "https://images.unsplash.com/photo-1556597386-347226bd1776?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
			"alt": "Image of a peregrine falcon"
			}
		)

	def test_single_delimited_section(self):
		node = TextNode("This contains **bold text** inside a plain text node", TextType.TEXT)
		self.assertEqual(split_nodes_delimiter([node], '**', TextType.BOLD), [
			TextNode("This contains ", TextType.TEXT),
			TextNode("bold text", TextType.BOLD),
			TextNode(" inside a plain text node", TextType.TEXT),
		])

		node2 = TextNode("This contains `code text` inside a plain text node", TextType.TEXT)
		self.assertEqual(split_nodes_delimiter([node2], '`', TextType.CODE), [
			TextNode("This contains ", TextType.TEXT),
			TextNode("code text", TextType.CODE),
			TextNode(" inside a plain text node", TextType.TEXT),
		])

		node3 = TextNode("This contains _italic text_ inside a plain text node", TextType.TEXT)
		self.assertEqual(split_nodes_delimiter([node3], '_', TextType.ITALIC), [
			TextNode("This contains ", TextType.TEXT),
			TextNode("italic text", TextType.ITALIC),
			TextNode(" inside a plain text node", TextType.TEXT),
		])

		

	def test_multiple_delimited_sections(self):
		# Two separate formatted sections in one string.
		node = TextNode("This contains **1st bold text** and **2nd bold text** inside a plain text node", TextType.TEXT)
		self.assertEqual(split_nodes_delimiter([node], '**', TextType.BOLD), [
			TextNode("This contains ", TextType.TEXT),
			TextNode("1st bold text", TextType.BOLD),
			TextNode(" and ", TextType.TEXT),
			TextNode("2nd bold text", TextType.BOLD),
			TextNode(" inside a plain text node", TextType.TEXT),
		])

		node2 = TextNode("This contains `1st code text` and `2nd code text` inside a plain text node", TextType.TEXT)
		self.assertEqual(split_nodes_delimiter([node2], '`', TextType.CODE), [
			TextNode("This contains ", TextType.TEXT),
			TextNode("1st code text", TextType.CODE),
			TextNode(" and ", TextType.TEXT),
			TextNode("2nd code text", TextType.CODE),
			TextNode(" inside a plain text node", TextType.TEXT),
		])

		node3 = TextNode("This contains _1st italic text_ and _2nd italic text_ inside a plain text node", TextType.TEXT)
		self.assertEqual(split_nodes_delimiter([node3], '_', TextType.ITALIC), [
			TextNode("This contains ", TextType.TEXT),
			TextNode("1st italic text", TextType.ITALIC),
			TextNode(" and ", TextType.TEXT),
			TextNode("2nd italic text", TextType.ITALIC),
			TextNode(" inside a plain text node", TextType.TEXT),
		])

	def test_non_text_node_unchanged(self):
		node = TextNode("![Great tit bird](https://cdn.download.ams.birds.cornell.edu/api/v1/asset/169357911/2400)", TextType.IMAGE,)
		self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [
			node
		])

		node = TextNode("This is a code text block and nothing else", TextType.CODE,)
		self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [
			node
		])
		

	def test_unmatched_delimiter_raises(self):
		# Use assertRaises to verify invalid Markdown is rejected.
		node = TextNode("`This is a plain text with code text inside", TextType.TEXT)
		with self.assertRaises(ValueError):
			split_nodes_delimiter([node], '`', TextType.CODE)

	def test_delimiters_at_text_edges(self):
		node = TextNode("**This is a really giant italic text node**", TextType.ITALIC)
		self.assertEqual(split_nodes_delimiter([node], "**", TextType.ITALIC), [node])

	def test_multiple_input_nodes(self):
		old_nodes = [
			TextNode("Morning ", TextType.TEXT),
			TextNode("already styled", TextType.BOLD),
			TextNode("Use `git status` now", TextType.TEXT),
		]
		self.assertEqual(split_nodes_delimiter(old_nodes, '`', TextType.CODE),
			[
				old_nodes[0],
				old_nodes[1],
				TextNode("Use ", TextType.TEXT),
				TextNode("git status", TextType.CODE),
				TextNode(" now", TextType.TEXT),
			]
		)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

		matches2 = extract_markdown_images("")
		self.assertListEqual([], matches2)

		matches3 = extract_markdown_images("See great tits ![right here](https://cdn.download.ams.birds.cornell.edu/api/v1/asset/169357911/2400)")
		self.assertListEqual([("right here", "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/169357911/2400")], matches3)
		
		
	

	def test_extract_markdown_links(self):
		matches = extract_markdown_link("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
		self.assertListEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

		matches2 = extract_markdown_link("")
		self.assertListEqual([], matches2)

		matches3 = extract_markdown_link("[cool site](https://paint.toys/pixel-art/)")
		self.assertListEqual([("cool site", "https://paint.toys/pixel-art/")], matches3)
				

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
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes,
		)


		node = TextNode(
			"This is text only",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text only", TextType.TEXT),
			],
			new_nodes,
		)


		node = TextNode(
			"![Great tit bird](https://cdn.download.ams.birds.cornell.edu/api/v1/asset/169357911/2400)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("Great tit bird", TextType.IMAGE, "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/169357911/2400"),
			],
			new_nodes,
		)
				
	def test_split_link_with_traditional_image_links(self):
		node = TextNode("This is text with a link to an [image](https://i.imgur.com/zjjcJKZ.png) and another link towards a [second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT,)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a link to an ", TextType.TEXT),
				TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another link towards a ", TextType.TEXT),
				TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes,
		)

	def test_split_link(self):
		node = TextNode("", TextType.TEXT,)
		new_nodes = split_nodes_link([node])
		self.assertListEqual([], new_nodes)


		node = TextNode("Check out our [shady search engine](https://www.google.com/) and [totally legit blog](https://openai.com/news/)", TextType.TEXT, None)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("Check out our ", TextType.TEXT),
				TextNode("shady search engine", TextType.LINK, "https://www.google.com/"), 
				TextNode(" and ", TextType.TEXT),
				TextNode("totally legit blog", TextType.LINK, "https://openai.com/news/")
			], 
			new_nodes
		)

		node = TextNode("Just text only", TextType.TEXT, None)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("Just text only", TextType.TEXT),
			], 
			new_nodes
		)


		node = TextNode("[Just a link](https://flashpointarchive.org/)", TextType.TEXT, None)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("Just a link", TextType.LINK, "https://flashpointarchive.org/"),
			], 
			new_nodes
		)	

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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
			text_to_textnodes(text)
		)

		text = ""
		self.assertListEqual(
			[],
			text_to_textnodes(text)
		)
		
		text = "A `variable` holds _dynamic_ data, and **constants** never change. Check the [docs](https://example.com/docs) or view the ![diagram](https://example.com/diagram.png) for details."
		self.assertListEqual(
			[
				TextNode("A ", TextType.TEXT),
				TextNode("variable", TextType.CODE),
				TextNode(" holds ", TextType.TEXT), 
				TextNode("dynamic", TextType.ITALIC), 
				TextNode(" data, and ", TextType.TEXT),
				TextNode("constants", TextType.BOLD),
				TextNode(" never change. Check the ", TextType.TEXT),
				TextNode("docs", TextType.LINK, "https://example.com/docs"),
				TextNode(" or view the ", TextType.TEXT),
				TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.png"), 
				TextNode(" for details.", TextType.TEXT,), 
			],
			text_to_textnodes(text)
		)

	def test_markdown_to_blocks(self):
			md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
			blocks = markdown_to_blocks(md)
			self.assertEqual(
				blocks,
				[
					"This is **bolded** paragraph",
					"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
					"- This is a list\n- with items",
				],
			)


			md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
			blocks = markdown_to_blocks(md)
			self.assertEqual(
				blocks,
				[
					"# This is a heading",
					"This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
					"- This is the first list item in a list block\n- This is a list item\n- This is another list item",
				],
			)

	def test_block_to_block_type(self):
		heading_block = ("# This is a heading")
		self.assertEqual(BlockType.HEADING, block_to_block_type(heading_block))


		heading_level_3 = "### Subheading title"
		self.assertEqual(BlockType.HEADING, block_to_block_type(heading_level_3))


		code_block = "```\ndef hello():\n    print('world')\n```"
		self.assertEqual(BlockType.CODE, block_to_block_type(code_block))

		quote_block = "> Wisdom begins in wonder.\n> - Socrates"
		self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block))

		
		unordered_list_block = "- First item\n- Second item\n- Third item"
		self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered_list_block))


		ordered_list_block = "1. Gather herbs\n2. Brew potion\n3. Cast spell"
		self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(ordered_list_block))


		paragraph_block = "Just a regular paragraph with some text."
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(paragraph_block))


		fake_heading = "####### Too many hashes"
		self.assertNotEqual(BlockType.HEADING, block_to_block_type(fake_heading))


		broken_ordered_list = "1. First item\n3. Skipped two"
		self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(broken_ordered_list))


		broken_quote = "> First line is quoted\nSecond line is not"
		self.assertNotEqual(BlockType.QUOTE, block_to_block_type(broken_quote))

	def test_paragraphs_to_html(self):
			md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

			node = markdown_to_html_node(md)
			html = node.to_html()
			self.assertEqual(
				html,
				"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
			)


	def test_codeblock_to_html(self):
			md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

			node = markdown_to_html_node(md)
			html = node.to_html()
			self.assertEqual(
				html,
				"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
			)

	def test_headings_to_html(self):
					md = """
# Heading one

## Heading two

###### Heading six
"""
		
					node = markdown_to_html_node(md)
					html = node.to_html()
					self.assertEqual(
						html,
						"<div><h1>Heading one</h1><h2>Heading two</h2><h6>Heading six</h6></div>",
					)


					md = """
## The **ruined** tower
"""
		
					node = markdown_to_html_node(md)
					html = node.to_html()
					self.assertEqual(
						html,
						"<div><h2>The <b>ruined</b> tower</h2></div>",
					)

	def test_quotes_to_html(self):
						md = """
> The tower fell
> in a single night
> and no one saw
"""
						node = markdown_to_html_node(md)
						html = node.to_html()
						self.assertEqual(
							html,
							"<div><blockquote>The tower fell in a single night and no one saw</blockquote></div>",
						)
						md = """
> Wisdom begins in **wonder**
"""
						node = markdown_to_html_node(md)
						html = node.to_html()
						self.assertEqual(
							html,
							"<div><blockquote>Wisdom begins in <b>wonder</b></blockquote></div>",
						)

	def test_lists_to_html(self):
						md = """
- flour
- eggs
- _fresh_ milk 
"""
						node = markdown_to_html_node(md)
						html = node.to_html()
						self.assertEqual(
							html,
							"<div><ul><li>flour</li><li>eggs</li><li><i>fresh</i> milk</li></ul></div>",
						)

						md = """
1. Gather herbs
2. Brew the potion
3. Cast the spell
"""
						node = markdown_to_html_node(md)
						html = node.to_html()
						self.assertEqual(
							html,
							"<div><ol><li>Gather herbs</li><li>Brew the potion</li><li>Cast the spell</li></ol></div>",
						)

	def test_mix_markdown_to_html(self):
								md = """
# Title

A paragraph with `code`. 

- one
- two

> quoted
"""
								node = markdown_to_html_node(md)
								html = node.to_html()
								self.assertEqual(
									html,
									"<div><h1>Title</h1><p>A paragraph with <code>code</code>.</p><ul><li>one</li><li>two</li></ul><blockquote>quoted</blockquote></div>",
								)
	def test_markdown_images_links_to_html(self):
								md = """
See the [docs](https://example.com) and this ![chart](https://example.com/c.png)
"""
								node = markdown_to_html_node(md)
								html = node.to_html()
								self.assertEqual(
									html,
									"<div><p>See the <a href=\"https://example.com\">docs</a> and this <img src=\"https://example.com/c.png\" alt=\"chart\"></img></p></div>",
								)

	
	
if __name__ == "__main__":
	unittest.main()
