CORD_DICT = {}
for i in range(19):
    CORD_DICT[chr(97 + i)] = i


def load_sgf_file(file_name: str):
    cord_list = []
    index: int = -1

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        # print(content)
        for k in range(0, len(content) - 2):
            if content[k] == ';' and content[k + 1] == 'B' and content[k + 2] == '[':
                index = k
                break
        # if index >= 0:
        #     another_str = content[index: len(content)]
        #     print("--------------------------------------")
        #     print(another_str)
        #     print("--------------------------------------")

        while 0 <= index < len(content):
            if content[index] == '\n':
                index += 1
            if index + 4 < len(content):
                x_cord = CORD_DICT[content[index + 3]]
                y_cord = CORD_DICT[content[index + 4]]
                cord_list.append((x_cord, y_cord))
            index += 6

    return cord_list


