import unittest

from block import BlockType, block_to_block_type

text_header = """
# Title 1
## Title 2
### Title 3
#### Title 4
##### Title 5
###### Title 6
####### Invalid Title
"""

text_code = """
```python
print("Hello")
```
"""

text_quote = """
> This is a block quote
>This is still the same block quote
> Forever and ever
"""

text_unordered_list = """
- unbordered list 1
- unbordered list 2
- unbordered list 3
- unbordered list 4
"""

text_ordered_list = """
1. allo
2. bonjour
11. Allo
111. Allo
910284390829048. Hola
"""

text_paragraph = """
Ths is a normal paragraph
"""

class TestTextNode(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type(text_header), BlockType.HEADING)

    def test_heading(self):
        self.assertEqual(block_to_block_type(text_code), BlockType.CODE)

    def test_heading(self):
        self.assertEqual(block_to_block_type(text_quote), BlockType.QUOTE)

    def test_heading(self):
        self.assertEqual(block_to_block_type(text_unordered_list), BlockType.UNORDERED_LIST)

    def test_heading(self):
        self.assertEqual(block_to_block_type(text_ordered_list), BlockType.ORDERED_LIST)

    def test_heading(self):
        self.assertEqual(block_to_block_type(text_header), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
