# import subprocess
# import json
# import re
#
# # ---------- 配置 ----------
# katago_path = 'KataGo\\katago.exe'
# config_path = 'KataGo\\gtp_custom.cfg'
# model_path = 'KataGo\\kata1-b18c384nbt-s9996604416-d4316597426.bin.gz'
#
# # 默认贴目
# KOMI = 7.5
# # 您希望执黑还是执白？ ('b' 或 'w')
# USER_COLOR = 'b'
# AI_COLOR = 'w' if USER_COLOR == 'b' else 'b'
#
# # ---------- 启动 KataGo ----------
# print("正在启动 KataGo...")
# process = subprocess.Popen([katago_path, 'gtp',
#                             '-model', model_path,
#                             '-config', config_path],
#                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
#                            stderr=subprocess.STDOUT, text=True, bufsize=1)
#
# # 等待就绪
# ready_str = "GTP ready, beginning main protocol loop"
# while True:
#     line = process.stdout.readline()
#     if line == '' and process.poll() is not None:
#         raise RuntimeError("KataGo 进程意外退出")
#     if ready_str in line:
#         print("KataGo 就绪！\n")
#         break
#
# def send_command(cmd):
#     """发送 GTP 命令，返回所有非空响应行（去掉状态前缀 '=' 或 '?'）"""
#     process.stdin.write(cmd + '\n')
#     process.stdin.flush()
#     response = []
#     while True:
#         line = process.stdout.readline().strip()
#         if line == '':
#             break
#         response.append(line)
#     return response
#
# def get_winrate():
#     """
#     调试版本：获取胜率，并打印原始响应，帮助定位问题。
#     """
#     print("\n--- DEBUG: 发送 kata-analyze 命令 ---")
#     # 发送命令，适当降低 maxVisits 可以加快测试速度
#     resp = send_command("kata-analyze interval 0 maxVisits 100")
#
#     print("--- DEBUG: 接收到原始响应 ---")
#     for i, line in enumerate(resp):
#         # 打印原始响应的每一行，方便检查
#         print(f"[{i}] {line}")
#     print("--- DEBUG: 响应结束 ---")
#
#     # 尝试解析
#     info_line = None
#     for line in resp:
#         # GTP 协议中，成功响应通常以 '=' 开头，我们将其移除方便处理
#         if line.startswith('='):
#             line = line[1:].strip()
#
#         # 寻找包含分析数据的行
#         if 'info' in line:
#             info_line = line
#             break
#
#     if not info_line:
#         # 如果没有 'info'，检查是否在 '='
#         for line in resp:
#             if line.startswith('='):
#                 content = line[1:].strip()
#                 if content:
#                     info_line = content
#                     print(f"尝试解析无'info'标识的行: {info_line}")
#                     break
#
#     if not info_line:
#         return "调试：未在响应中找到有效数据行"
#
#     # 使用正则表达式提取 JSON 部分
#     json_match = re.search(r'(\{.*\})', info_line)
#     if json_match:
#         json_str = json_match.group(1)
#         try:
#             data = json.loads(json_str)
#             # 更稳健的字段访问
#             root_info = data.get('rootInfo')
#             if root_info:
#                 winrate = root_info.get('winrate')
#                 score_lead = root_info.get('scoreLead')
#                 current_player = root_info.get('currentPlayer')
#
#                 if winrate is None:
#                     return f"调试：成功解析JSON，但未找到 'winrate' 字段。数据: {root_info}"
#
#                 # 转换为黑方视角
#                 if current_player == 'B':
#                     black_winrate = winrate
#                 else:
#                     black_winrate = 1.0 - winrate
#
#                 return (f"黑胜率: {black_winrate:.2%} | "
#                         f"白胜率: {1.0 - black_winrate:.2%} | "
#                         f"目差: {score_lead:.1f}")
#             else:
#                 return f"调试：成功解析JSON，但未找到 'rootInfo' 字段。数据: {data}"
#         except json.JSONDecodeError as e:
#             return f"调试：JSON解析失败: {e}\n字符串: {json_str}"
#     else:
#         return f"调试：未在行中找到JSON数据。行内容: {info_line}"
#
# # ---------- 初始化对局 ----------
# send_command("clear_board")
# send_command(f"komi {KOMI}")
# print(f"棋盘已清空，贴目 {KOMI}。")
# print(f"您执 {'黑' if USER_COLOR == 'b' else '白'}，输入 GTP 坐标（如 Q16）落子。")
# print("特殊命令：PASS（停着）、RESIGN（认输）、quit（退出程序）\n")
#
# # 如果用户执白，需要先让 AI（黑）走一步
# if USER_COLOR == 'w':
#     print("AI（黑）思考中...")
#     response = send_command("genmove b")
#     if response and response[0].startswith('='):
#         ai_move = response[0][1:].strip().upper()
#         print(f"AI 落子: {ai_move}")
#         # 显示胜率
#         winrate_info = get_winrate()
#         print(f"[胜率] {winrate_info}\n")
#     else:
#         print("AI 生成着法失败。")
#         ai_move = None
#
# # ---------- 主循环 ----------
# move_count = 0
# pass_count = 0
# current_player = USER_COLOR  # 从用户开始
#
# while True:
#     if current_player == USER_COLOR:
#         # 用户回合
#         user_input = input("您的着法: ").strip()
#         if user_input.lower() == 'quit':
#             break
#         if user_input.upper() in ('PASS', 'RESIGN'):
#             move_str = user_input.upper()
#         else:
#             # 简单校验一下是否为合法 GTP 坐标（可进一步用函数验证）
#             move_str = user_input.upper()
#
#         # 发送 play 命令
#         if move_str != 'RESIGN':
#             send_command(f"play {USER_COLOR} {move_str}")
#         move_count += 1
#         print(f"第 {move_count} 手 (您): {move_str}")
#
#         if move_str == 'RESIGN':
#             print("您认输了。对局结束。")
#             break
#         elif move_str == 'PASS':
#             pass_count += 1
#             if pass_count >= 2:
#                 print("双方连续停着，对局结束。")
#                 break
#         else:
#             pass_count = 0
#
#         # 显示当前胜率
#         winrate_info = get_winrate()
#         print(f"[胜率] {winrate_info}\n")
#
#         # 切换玩家
#         current_player = AI_COLOR
#
#     else:
#         # AI 回合
#         print("AI 思考中...")
#         response = send_command(f"genmove {AI_COLOR}")
#         if not response:
#             print("错误：未收到 AI 响应。")
#             break
#         status_line = response[0]
#         if status_line.startswith('='):
#             ai_move = status_line[1:].strip().upper()
#         else:
#             print(f"引擎返回错误: {status_line}")
#             break
#
#         move_count += 1
#         player_name = "黑方" if AI_COLOR == 'b' else "白方"
#         print(f"第 {move_count} 手 (AI/{player_name}): {ai_move}")
#
#         if ai_move == 'RESIGN':
#             print(f"AI 认输。对局结束。")
#             break
#         elif ai_move == 'PASS':
#             pass_count += 1
#             if pass_count >= 2:
#                 print("双方连续停着，对局结束。")
#                 break
#         else:
#             pass_count = 0
#
#         # AI 的着法已经由 genmove 自动应用，无需再 play
#         # 显示胜率
#         winrate_info = get_winrate()
#         print(f"[胜率] {winrate_info}\n")
#
#         # 切换玩家
#         current_player = USER_COLOR
#
# # ---------- 对局结束 ----------
# print("\n对局结束。")
# result = send_command("final_score")
# if result:
#     print(f"最终得分: {result[0]}")
#
# send_command("quit")
# process.terminate()
# process.wait(timeout=5)
# print("KataGo 已退出。")