from typing import List

class ASTNode:

    indent_width = 1

    def __init__(self, name: str):
        self.children: List[ASTNode] = []
        self.name = name

    def visualize(self, depth: int) -> List[str]:
        output = [' '] * depth * self.__class__.indent_width
        output.extend([self.name, '-', str(len(self.children)), '\n'])
        for child in self.children:
            output.extend([' '] * (depth + 1) * self.__class__.indent_width)
            output.extend(child.visualize(depth + 2))

        return output
    def __repr__(self):
        return ''.join(self.visualize(0))
