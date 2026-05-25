import sys
from build import copy_static_to_public
from helper import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
