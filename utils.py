CORD_DICT = {}
for i in range(19):
    CORD_DICT[chr(97 + i)] = i


def load_sgf_file(file_name: str):
    black_first: bool = True

    advanced_placed_black = []
    advanced_placed_white = []
    cord_list = []

    index_advanced_black: int = -1
    index_advanced_white: int = -1
    index: int = -1

    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

        for k in range(0, len(content) - 2):
            if content[k] == 'A' and content[k + 1] == 'B' and content[k + 2] == '[':
                index_advanced_black = k
                index_advanced_black += 3
                while index_advanced_black < len(content):
                    if content[index_advanced_black] not in CORD_DICT.keys():
                        break
                    if index_advanced_black + 4 < len(content):
                        x_cord = CORD_DICT[content[index_advanced_black]]
                        y_cord = CORD_DICT[content[index_advanced_black + 1]]
                        advanced_placed_black.append((x_cord, y_cord))
                    index_advanced_black += 4

        for k in range(0, len(content) - 2):
            if content[k] == 'A' and content[k + 1] == 'W' and content[k + 2] == '[':
                index_advanced_white = k
                index_advanced_white += 3
                while index_advanced_white < len(content):
                    if content[index_advanced_white] not in CORD_DICT.keys():
                        break
                    if index_advanced_white + 4 < len(content):
                        x_cord = CORD_DICT[content[index_advanced_white]]
                        y_cord = CORD_DICT[content[index_advanced_white + 1]]
                        advanced_placed_white.append((x_cord, y_cord))
                    index_advanced_white += 4

        for k in range(0, len(content) - 2):
            test1 = content[k] == ';' and content[k + 1] == 'B' and content[k + 2] == '['
            test2 = content[k] == ';' and content[k + 1] == 'W' and content[k + 2] == '['
            if test1:
                index = k
                break
            if test2:
                index = k
                black_first = False
                break

        while 0 <= index < len(content):
            if content[index] == '\n':
                index += 1
            if index + 4 < len(content):
                x_cord = CORD_DICT[content[index + 3]]
                y_cord = CORD_DICT[content[index + 4]]
                cord_list.append((x_cord, y_cord))
            index += 6

    return advanced_placed_black, advanced_placed_white, cord_list, black_first


