class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""

        output = ""

        for key, value in self.props.items():
            output += f' {key}="{value}"'

        return output

    def __repr__(self):
        tagStart = f'<{self.tag}{self.props_to_html()}>' if self.tag is not None else self.props_to_html()
        tagEnd = f'</{self.tag}>' if self.tag is not None else '';
        value = self.value if self.value is not None else ''
        children = ""
        if self.children is not None and len(self.children) > 0:
            for child in self.children:
                children += child.__repr__()

        # self.children.__repr__() if self.children is not None and len(children) > 0 else ''
        return f'{tagStart}{value}{children}{tagEnd}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return f"{self.value}"

        return self.__repr__()

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag element in ParentNode")

        if self.children is None:
            raise ValueError("Missing children elemennt in ParentNode")

        return self.__repr__()

