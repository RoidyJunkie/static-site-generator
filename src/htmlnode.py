#src/classes/htmlnode.py

class HTMLNode():
    tag: str | None
    value: str | None
    children: list["HTMLNode"] | None
    props: dict[str, str] | None

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None | str:
        raise NotImplementedError("to_html is implemented in child classes")

    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""
        result = ""
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNodes should have non-empty values")
        if self.tag is None or self.tag == "":
            return self.value
       
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
    def __repr__(self):
            return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children: list[HTMLNode], props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent Node has no tag!")
        if self.children is None:
            raise ValueError("Node can't be a parent if there are no children!")
        children_str = "".join(child.to_html() for child in self.children) # pyright: ignore[reportCallIssue, reportArgumentType]
        
        
        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"            
         