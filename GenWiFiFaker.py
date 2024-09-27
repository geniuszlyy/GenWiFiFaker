from faker import Faker
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp
from os import system, geteuid, path
from threading import Thread
import sys
import colorama
from time import sleep
import platform

colorama.init(autoreset=True)

# Логотип и информация
project_logo = f"""{colorama.Fore.LIGHTRED_EX}
   _____        __          ___ ______ _ ______    _             
  / ____|       \ \        / (_)  ____(_)  ____|  | |            
 | |  __  ___ _ _\ \  /\  / / _| |__   _| |__ __ _| | _____ _ __ 
 | | |_ |/ _ \ '_ \ \/  \/ / | |  __| | |  __/ _` | |/ / _ \ '__|
 | |__| |  __/ | | \  /\  /  | | |    | | | | (_| |   <  __/ |   
  \_____|\___|_| |_|\/  \/   |_|_|    |_|_|  \__,_|_|\_\___|_|   
                                                                 
"""

# Сообщение помощи с инструкциями по запуску
usage_instructions = f"""
{colorama.Fore.LIGHTYELLOW_EX}╭───────────────────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━───────────────────────────╮
| {colorama.Fore.LIGHTGREEN_EX}Использование » python {path.basename(__file__)} -i [интерфейс] -c [кол-во сетей] -wn [имя сети] {colorama.Fore.LIGHTYELLOW_EX} |
| {colorama.Fore.LIGHTGREEN_EX}Примеры: {colorama.Fore.LIGHTYELLOW_EX}                                                                               |
| {colorama.Fore.LIGHTGREEN_EX}python {path.basename(__file__)} -i wlan0mon -c 10                                                |
| {colorama.Fore.LIGHTGREEN_EX}python {path.basename(__file__)} -i wlan0mon -wn MyNetwork                                        |
| {colorama.Fore.LIGHTGREEN_EX}python {path.basename(__file__)} -i wlan0mon -c 5 -wn MyNetwork                                   |
{colorama.Fore.LIGHTYELLOW_EX}╰───────────────────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━───────────────────────────╯
"""

# Список допустимых флагов командной строки
valid_flags = ["-wn", "-i", "-c", "-h", "--h", "--help", "-help"]

class FakeAccessPoint:
    def __init__(self):
        self.total_networks = 1
        self.ssid_name = None
        self.interface_name = None

# Генерация фейковых данных для SSID и MAC-адреса
    def generate_fake_networks(self, num=1, network_name=None): # num - количество фейковых точек доступа | network_name - имя для сети (SSID) (необязательно)
        faker_instance = Faker()
        return [(network_name or faker_instance.domain_word(), faker_instance.mac_address()) for _ in range(num)]

# Отправка фейковых пакетов Beacon в отдельном потоке
    def broadcast_fake_beacon(self, ssid, mac_addr, interface, repeat=1, interval=0.1, verbosity=0): # ssid - имя SSID (сети) | mac_addr - MAC-адрес сети | interface - интерфейс в режиме мониторинга
        print(f"{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}»\n SSID: {colorama.Fore.LIGHTYELLOW_EX}{ssid}{colorama.Fore.RESET} - [MAC: {colorama.Fore.LIGHTBLUE_EX}{mac_addr}{colorama.Fore.RESET}]")
        dot11_layer = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac_addr, addr3=mac_addr)
        beacon_layer = Dot11Beacon(cap="ESS+privacy")
        ssid_element = Dot11Elt(ID="SSID", info=ssid, len=len(ssid))
        packet = RadioTap() / dot11_layer / beacon_layer / ssid_element
        try:
            sendp(packet, inter=interval, loop=repeat, iface=interface, verbose=verbosity)
        except Exception as error:
            print(f'{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.RED}[{mac_addr} - {ssid}] -> Error: {colorama.Fore.GREEN}{error}')

# Парсинг аргументов командной строки
    def parse_arguments(self, argv):
        if len(argv) == 1: # argv - список аргументов
            print(usage_instructions)
            exit()

        arguments = argv[1:]
        if arguments[0] in ["-h", '--h', '--help', '-help']:
            print(usage_instructions)
            exit()

        parsed_args = []
        encountered_flags = set()
        current_flag = None
        for arg in arguments:
            if arg.startswith('-'):
                if arg in encountered_flags:
                    print(f"{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.RED} Дублирующийся флаг:{colorama.Fore.GREEN}", arg)
                    exit()
                encountered_flags.add(arg)
                current_flag = arg
            else:
                if current_flag not in valid_flags:
                    print(f"{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.RED} Неверный флаг {colorama.Fore.GREEN}[{current_flag}]")
                    exit()
                parsed_args.append({'flag': current_flag, 'value': arg})
                current_flag = None
        return parsed_args

# Настройка параметров на основе аргументов.
    def configure_settings(self, args):
        for arg in args: # args - список аргументов
            flag = arg["flag"]
            value = arg['value']
            if flag == '-i':
                self.interface_name = value
            elif flag == '-wn':
                self.ssid_name = value
            elif flag == '-c':
                try:
                    self.total_networks = int(value)
                except ValueError:
                    print(f'{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.YELLOW} Неверный формат количества')
                    exit()
        if not self.interface_name:
            print(f'{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.YELLOW} Обязательный аргумент "-i" отсутствует.\nИспользуйте --help для справки.')
            exit()

# Основная функция программы
    def start(self):
        system("cls" if platform.system() == "Windows" else "clear")
        print(project_logo)
        if platform.system() != "Windows" and geteuid() != 0:
            print(f"{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.YELLOW} Пожалуйста, запустите от имени администратора.")
            exit()
        elif platform.system() == "Windows":
            print(f"{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.YELLOW} Проверка прав администратора пропущена на Windows.")
        self.configure_settings(self.parse_arguments(sys.argv))
        print(f"{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» Интерфейс: {colorama.Fore.GREEN}{self.interface_name}{colorama.Fore.RESET}\nКоличество точек: {colorama.Fore.GREEN}{self.total_networks}{colorama.Fore.RESET}\nИмя для точек: {colorama.Fore.LIGHTYELLOW_EX}{self.ssid_name or 'случайное'}")
        input("\nНажмите любую клавишу для продолжения")
        fake_networks_list = self.generate_fake_networks(self.total_networks, self.ssid_name)
        print(f'{colorama.Fore.LIGHTYELLOW_EX}[ {colorama.Fore.LIGHTRED_EX}GenWiFiFaker {colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.LIGHTBLUE_EX}» {colorama.Fore.LIGHTBLUE_EX}[{colorama.Fore.GREEN}*{colorama.Fore.LIGHTBLUE_EX}]{colorama.Fore.YELLOW} Запуск... [CTRL + C для остановки]')
        for ssid, mac in fake_networks_list:
            Thread(target=self.broadcast_fake_beacon, args=(ssid, mac, self.interface_name)).start()
            sleep(0.2)

if __name__ == "__main__":
    FakeAccessPoint().start()
