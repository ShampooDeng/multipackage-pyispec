import re
import os

# ----------------- Global variable -----------------
# PROJECT_NAME = "<Your_Project_name>"
PROJECT_NAME = "nice"

src_file_paths = [
    ## For examaple:
    "./say_hi.py",
    "./main.py",
    "./say_fvck.py"
]
# ----------------- Global variable -----------------


# ----------------- start of helper function -----------------
def generate_specs(filepaths):
    ret = []
    for file in filepaths:
        os.system("pyi-makespec " + file)
        res = re.match("(.*)\.py", file)
        if res != None:
            ret.append(res.groups(0)[0])
    ret = [x + ".spec" for x in ret]
    return ret


def extract_filename(file_path):
    res = re.match(".*/(.*)\.spec", file_path)
    if res == None:
        return None
    return res.groups(0)[0] + "_"


def replace_word(line: str, head_index: int, tail_index: int, body: str):
    head = line[:head_index]
    body = body + line[head_index:tail_index]
    tail = line[tail_index:]
    return head + body + tail


def gather_collect(content: list):
    content_head = [
        "coll = COLLECT(\n",
    ]
    content_tail = [
        "        strip=False,\n",
        "        upx=True,\n",
        "        upx_exclude=[],\n",
        f"        name='{PROJECT_NAME}',\n",
        "    )\n",
    ]
    content_body = ["    " + x for x in content]
    return content_head + content_body + content_tail
# ----------------- end of helper function -----------------


if __name__ == "__main__":
    if PROJECT_NAME == "<Your_Project_name>":
        raise Exception("Define your project name!")
    if len(src_file_paths) == 0:
        raise Exception("src_file_paths is empty")

    spec_file_paths = generate_specs(src_file_paths)
    contents = []
    collect_content = []

    # --------- main loop ----------
    for filepath in spec_file_paths:
        filename = extract_filename(filepath)

        collect_content_pos = []
        with open(filepath, mode="r") as file:
            if not file.readable():
                raise BufferError(f"{filepath} is not readable")

            lines = file.readlines()
            # I assume the total length of all the
            # spec files would exceed 65535.
            stop_marker = 65535
            for i in range(len(lines)):
                if i > 65535:
                    raise OverflowError("The spec files are too big!")

                if (res := re.search("^a", lines[i])) != None:
                    head_mark, tail_mark = res.span()
                    lines[i] = replace_word(lines[i], head_mark, tail_mark, filename)
                    if i > stop_marker and (i not in collect_content_pos):
                        collect_content_pos.append(i)
                if (res := re.search("pyz", lines[i])) != None:
                    head_mark, tail_mark = res.span()
                    lines[i] = replace_word(lines[i], head_mark, tail_mark, filename)
                    if i > stop_marker and (i not in collect_content_pos):
                        collect_content_pos.append(i)
                if (res := re.search("exe", lines[i])) != None:
                    head_mark, tail_mark = res.span()
                    lines[i] = replace_word(lines[i], head_mark, tail_mark, filename)
                    if i > stop_marker and (i not in collect_content_pos):
                        collect_content_pos.append(i)
                if (res := re.search("a\.", lines[i])) != None:
                    head_mark, tail_mark = res.span()
                    lines[i] = replace_word(lines[i], head_mark, tail_mark, filename)
                    if i > stop_marker and (i not in collect_content_pos):
                        collect_content_pos.append(i)
                if (res := re.search("COLLECT", lines[i])) != None:
                    stop_marker = i
            # 1 here means dropping the first line of each spec files
            contents.append(lines[1:stop_marker])
            collect_content.extend([lines[pos] for pos in collect_content_pos])

    with open(f"./{PROJECT_NAME}.spec", mode="w") as file:
        file.write("# -*- mode: python ; coding: utf-8 -*-")
        for content in contents:
            file.writelines(content)
        file.writelines(gather_collect(collect_content))

    for file in spec_file_paths:
        os.remove(file)