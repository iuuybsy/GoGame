import subprocess

katago_path = 'D:\\coding\\katago\\katago.exe'
config_path = 'D:\\coding\\katago\\gtp_human9d_search_example.cfg'
model_path = 'D:\\coding\\katago\\kata1-b28c512nbt-s7915807488-d4517482653.bin.gz'
human_model = 'D:\\coding\\katago\\b18c384nbt-humanv0.bin.gz'


class KatagoAI:
    def __init__(self):
        self.process = subprocess.Popen([katago_path, 'gtp',
                                         '-model', model_path,
                                         '-config', config_path,
                                         '-human-model', human_model],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    def send_command(self, command):
        self.process.stdin.write(command + '\n\n')
        self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline().strip()
            if line.startswith('='):
                break
        return line
