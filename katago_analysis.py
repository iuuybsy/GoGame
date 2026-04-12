import subprocess
import sys

# 指定KataGo的路径和配置文件
katago_path = 'KataGo\\katago.exe'
config_path = 'KataGo\\gtp_custom.cfg'
model_path = 'KataGo\\kata1-b18c384nbt-s9996604416-d4316597426.bin.gz'

print("Path set.")

# 启动KataGo进程
process = subprocess.Popen([katago_path, 'gtp',
                            '-model', model_path,
                            '-config', config_path],
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, bufsize=1)

print("Process started. Waiting for KataGo to be ready...")

# 等待KataGo就绪信号
ready_str = "GTP ready, beginning main protocol loop"
line = process.stdout.readline()
while not (ready_str in line):
    print(f"line: {line}")
    line = process.stdout.readline()
    if line == '' and process.poll() is not None:
        raise RuntimeError("KataGo进程意外退出，请检查配置。")
    if ready_str in line:
        print("KataGo ready.\n")
        break
    # 可选：打印加载过程中的输出（如模型加载信息）
    # print(line.strip())


def send_command(cmd):
    """向KataGo发送GTP命令，并返回响应列表（直到空行结束）"""
    process.stdin.write(cmd + '\n')
    process.stdin.flush()
    response = []
    while True:
        line = process.stdout.readline().strip()
        if line == '':
            break
        response.append(line)
    return response


# 初始化棋盘
send_command("clear_board")
print("棋盘已清空，对局开始。")

# 设置贴目（可根据需要调整）
send_command("komi 7.5")

# 对局参数
max_moves = 500  # 防止无限循环
move_count = 0
pass_count = 0  # 连续pass计数
current_player = 'b'  # 'b' 黑先

while move_count < max_moves:
    # 请求生成着法
    cmd = f"genmove {current_player}"
    response = send_command(cmd)

    # response的第一行通常是以'='开头的状态行，后面跟着法信息
    if not response:
        print("错误：未收到着法响应。")
        break

    # 解析着法字符串（通常为 '= <move>' 格式）
    status_line = response[0]
    if status_line.startswith('='):
        move_str = status_line[1:].strip().upper()
    else:
        print(f"引擎返回错误: {status_line}")
        break

    move_count += 1
    player_name = "黑方" if current_player == 'b' else "白方"
    print(f"第{move_count}手 ({player_name}): {move_str}")

    # 判断对局结束条件
    if move_str == "RESIGN":
        print(f"{player_name}认输。对局结束。")
        break
    elif move_str == "PASS":
        pass_count += 1
        print(f"{player_name}停着。")
        if pass_count >= 2:
            print("双方连续停着，对局结束。")
            break
    else:
        pass_count = 0  # 有落子则重置pass计数

    # 应用着法到棋盘（除非认输，认输后不再play）
    if move_str != "RESIGN":
        send_command(f"play {current_player} {move_str}")

    # 切换玩家
    current_player = 'w' if current_player == 'b' else 'b'

print("\n对局结束。")

# 可选：获取最终结果
result = send_command("final_score")
if result:
    print(f"最终得分: {result[0]}")

# 关闭KataGo进程
send_command("quit")
process.terminate()
process.wait(timeout=5)
print("KataGo已退出。")