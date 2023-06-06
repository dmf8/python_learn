import re
from tree import TreeNode


templ_repl = "，。？、：（）%"

root = TreeNode("")


def traverseNode(node, fw):
    for child in node.children:
        line = f"{node.value}-->{child.value}"
        fw.write(line)
        fw.write("\n")
        traverseNode(child, fw)


def traverseRoot(fw):
    if (0 == len(root.children)):
        return
    traverseNode(root.children[0], fw)


def specialCharRep(_string):
    ret = _string
    for ch in templ_repl:
        str_repl = f"&#{ord(ch)}"
        ret = re.sub(ch, str_repl, ret)
    return ret


def formatData(line):
    n = root
    # print(line)
    for i in range(len(line)):

        if not (n.containsChild(line[i])):
            n.add_child(TreeNode(line[i]))
        n = n.children[n.indexOfValue(line[i])]
        pass


fw = open("abc.txt", "w")
fw.write("flowchart LR\n")

with open("test.csv", "r") as f:
    for line in f:
        line = line.strip()
        items = line.split(',')
        for i in range(len(items)):
            items[i] = specialCharRep(items[i])

        # formatData(items)
        new_line = "-->".join(items)
        fw.write(new_line)
        fw.write("\n")
    # traverseRoot(fw)

fw.close()
