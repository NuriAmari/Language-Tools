from __future__ import annotations
from typing import List, Dict, Optional, Set


class ASTNode:

    indent_width = 1

    @classmethod
    def from_dict_literal(cls, literal: Dict) -> ASTNode:
        """Used to construct an entire AST from composed dict literals, particularly useful for testing"""

        name = list(literal.keys())[0]
        root = cls(name)
        root.children = [cls.from_dict_literal(child) for child in literal[name]]
        return root

    def __init__(self, name: str, lexme: Optional[str] = None):
        self.children: List[ASTNode] = []
        self.name = name
        self.lexme = lexme

    def visualize(self, depth: int) -> List[str]:
        output = [" "] * depth * self.__class__.indent_width
        output.extend(
            [
                self.name,
                ":",
                str(len(self.children)) if self.lexme is None else self.lexme,
                "\n",
            ]
        )
        for child in self.children:
            output.extend([" "] * (depth + 1) * self.indent_width)
            output.extend(child.visualize(depth + 2))

        return output

    # Used to flatten AST when recursive rules to form things like lists make the tree unecesssarily tall
    # Name aliases is used to alias node names that shouldn't be direclty related
    # Ex. If A is aliased to B, you'll never have an A node with B as a direct child
    def flatten(self, name_aliases: Dict[str, Set[str]]):
        flattened_children: List[ASTNode] = []
        for child in self.children:
            if (
                child.name == self.name
                or self.name in name_aliases
                and child.name in name_aliases[self.name]
            ):
                flattened_children.extend(child.flatten(name_aliases))
            else:
                child.flatten(name_aliases)
                flattened_children.append(child)

        self.children = flattened_children
        return flattened_children

    def __repr__(self):
        return "".join(self.visualize(0))
