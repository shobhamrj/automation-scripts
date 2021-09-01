 
from subprocess import Popen, PIPE
from typing import List, Dict
from getpass import getpass


class Connect:
    __NM_SCAN_CMD: List[str] = ['nmcli', '-f', 'ssid,bars', 'device', 'wifi', 'list']
    __HEAD_CMD: List[str] = ['head', '-n4', '-']
    __NM_CONNECT_CMD: List[str] = ['nmcli', 'device', 'wifi', 'connect', '--ask']
    __available_conns: List[str]
    __ssid_map: Dict[int, str]
    __display_text: List[str]
    __choice: int

    def __init__(self):
        Connect.__display_wait_banner()
        self.__display_text, self.__ssid_map = Connect.__scan()
        self.show_choices()
        self.__choice = Connect.__get_choice()
        self.__connect()

    @staticmethod
    def __display_wait_banner():
        print('''
        Scanning Please wait...\n
        ''')

    def show_choices(self):
        print('\n', *self.__display_text)

    @staticmethod
    def __get_choice():
        choice = int(input('Enter your choice:\t'))
        return choice

    @staticmethod
    def __get_display_text(all_ssids: List[bytes]):
        proc_input = b''.join(all_ssids)
        process = Popen(Connect.__HEAD_CMD, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        std_out, _ = process.communicate(input=proc_input)
        std_out = std_out.split(b'\n')[1:-1]
        top_ssids = [f'{i + 1}\t{ssid.decode()}\n' for i, ssid in enumerate(std_out)]
        return top_ssids

    @staticmethod
    def __make_ssid_map(display_text: List[str]):
        ssid_map = {i + 1: ssid.split()[1] for i, ssid in enumerate(display_text)}
        return ssid_map

    @staticmethod
    def __scan():
        process = Popen(Connect.__NM_SCAN_CMD, stderr=PIPE, stdout=PIPE)
        process.wait()
        all_ssids = [ssid for ssid in process.stdout.readlines()]
        display_text = Connect.__get_display_text(all_ssids)
        ssid_name_map = Connect.__make_ssid_map(display_text)
        return display_text, ssid_name_map

    def __connect(self):
        ssid = self.__ssid_map[self.__choice]
        password = getpass().encode()
        connect_command = Connect.__NM_CONNECT_CMD + [ssid]
        process = Popen(connect_command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        std_out, _ = process.communicate(input=password)
        print(std_out.decode())


if __name__ == '__main__':
    Connect()
