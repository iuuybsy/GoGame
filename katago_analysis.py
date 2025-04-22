import subprocess
import sys

# 指定KataGo的路径和配置文件
katago_path = 'D:\\coding\\katago\\katago.exe'
config_path = 'D:\\coding\\katago\\gtp_human9d_search_example.cfg'
model_path = 'D:\\coding\\katago\\kata1-b28c512nbt-s7915807488-d4517482653.bin.gz'
human_model = 'D:\\coding\\katago\\b18c384nbt-humanv0.bin.gz'

# 启动KataGo进程
process = subprocess.Popen([katago_path, 'gtp',
                            '-model', model_path,
                            '-config', config_path,
                            '-human-model', human_model],
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)


def send_command(command):
    process.stdin.write(command + '\n')
    process.stdin.flush()

    while True:
        line = process.stdout.readline()
        if line.startswith("info"):
            print(line.strip())
        elif line == "\n":
            break
    return line

# 设置棋盘大小
send_command('boardsize 19')

# 清空棋盘
send_command('clear_board')
send_command('kata-set-rules chinese')

send_command('play b Q16')
send_command('play w D4')
send_command('play b Q4')
send_command('play w D16')
send_command('play b F3')

# 查询黑棋的最优走法
best_move = send_command('genmove b')
print(type(best_move))
print(f'The best move is: {best_move}')

analysis = send_command('kata-analyze interval 500 maxmoves 3')

print(type(analysis))
print(f'The analysis is: {analysis}')

final_score = send_command('final_score')
print(type(final_score))
print(f'The final score is: {final_score}')

# 关闭KataGo进程
process.stdin.write('quit\n\n')
process.communicate()
