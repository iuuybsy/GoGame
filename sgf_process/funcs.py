import re


def sgf_read(file_path: str):
    with open(file_path, 'r') as file:
        sgf_content = file.read()

        clean_str = sgf_content.strip().strip('<').strip('>').strip('(').strip(')').strip(';')
        parts = clean_str.split(';')

        moves = []
        for part in parts:
            match_black = re.match(r'B\[([a-z]+)', part, re.IGNORECASE)
            match_white = re.match(r'W\[([a-z]+)', part, re.IGNORECASE)
            if match_black or match_white:
                info_list = list(match_black.group(1)) if match_black else list(match_white.group(1))
                x = ord(info_list[0]) - ord('a')
                y = ord(info_list[1]) - ord('a')
                moves.append((x, y))
        return moves
