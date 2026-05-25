from build import copy_static_to_public
from helper import generate_pages_recursive

def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")

main()
