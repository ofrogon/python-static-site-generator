from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdownBlock: str) -> BlockType:
    if re.match(r"^#{1,6}\s", markdownBlock):
        return BlockType.HEADING

    if re.match(r"^```.*?```$", markdownBlock, re.DOTALL) is not None:
        return BlockType.CODE

    lines = markdownBlock.splitlines()

    if len(re.findall(r"^>.*$", markdownBlock, re.MULTILINE)) == len(lines):
        return BlockType.QUOTE

    if len(re.findall(r"^- .*$", markdownBlock, re.MULTILINE)) == len(lines):
        return BlockType.UNORDERED_LIST

    if len(re.findall(r"^\d*?\..*$", markdownBlock, re.MULTILINE)) == len(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

