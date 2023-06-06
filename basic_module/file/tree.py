class TreeNode:
    def __init__(self, value=""):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children.remove(child_node)

    def traverse_tree(self):
        print(self.value)
        for child in self.children:
            child.traverse_tree()

    def containsChild(self, value):
        for child in self.children:
            if child.value == value:
                return True
        return False

    def indexOfValue(self, value):
        for i in range(len(self.children)):
            if value == self.children[i].value:
                return i
        return -1

    def getValue(self):
        return self.value
