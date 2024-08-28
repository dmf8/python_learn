import re
import sys
from tree import TreeNode


templ_repl = "，。？、：（）%"


def readRawCsv(file_name):
    lines = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            items = line.split(',')
            lines.append(items)
    return lines


def removeDupData(lines):
    for i in range(len(lines)-1, 0, -1):
        cur_line = lines[i]
        last_line = lines[i-1]
        for j in range(1, len(cur_line)):
            if len(last_line) <= j:
                break
            if cur_line[j] == last_line[j]:
                cur_line[j-1] = ""


def specialCharRep(_string):
    ret = _string
    for ch in templ_repl:
        str_repl = f"&#{ord(ch)}"
        ret = re.sub(ch, str_repl, ret)
    return ret


# if (len(sys.argv) < 2):
#     print("input file name error")
#     sys.exit()
# if (len(sys.argv) < 3):
#     print("output file name error")
#     sys.exit()
# file_input = sys.argv[1]
file_input = "thunder10.csv"
# file_output = sys.argv[2]
file_output = "thunder10_2.csv"

lines = readRawCsv(file_input)
removeDupData(lines)

fw = open(file_output, "w")
# fw.write("flowchart LR\n")
for line in lines:
    # filtered_line = list(filter(None, line))
    new_line = ",".join(line)
    # new_line = specialCharRep(new_line)
    fw.write(new_line)
    fw.write("\n")

fw.close()
