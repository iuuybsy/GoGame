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
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

print("Process started.\n\n\n")

command = "genmove b"
process.stdin.write(command + '\n')
process.stdin.flush()
feedback = process.stdout.readline()
print(feedback)

# 关闭KataGo进程
process.stdin.write('quit\n')
process.stdin.flush()
process.terminate()  # 确保进程结束