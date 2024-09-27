# EN
**GenWiFiFaker** is a tool for creating fake WiFi access points. It can be used for testing network security, performing demonstrations, or other educational purposes. This tool generates fake SSIDs and MAC addresses and broadcasts them over a specified WiFi interface.

## Features
- **Generate Fake SSIDs**: Create multiple fake WiFi networks with customizable names.
- **Customizable**: Define the number of networks, their names, and the interface to use.
- **Cross-Platform**: Works on both Windows and Linux.

## Requirements
- **Python 3.x**
- **Scapy Library**: Used for network packet crafting and sending.
- **Npcap (Windows) / libpcap (Linux)**: Required for capturing and sending packets.

## Installation
- **Install Python 3.x** from the official website.
- **Install Scapy**: `pip install scapy`
- **Install Faker**: `pip install faker`
- **Install Npcap (Windows)**: Download and install from Npcap's official site.

## Usage
To run the program, use the following command:
```bash
python GenWiFiFaker.py -i [interface] -c [number_of_networks] -wn [network_name]
```

## Examples
- **Create 10 random networks**:
```bash
python GenWiFiFaker.py -i wlan0mon -c 10
```
- **Create a network with a specific name**:
```bash
python GenWiFiFaker.py -i wlan0mon -wn MyNetwork
```
- **Create 5 networks with a specific name**:
```bash
python GenWiFiFaker.py -i wlan0mon -c 5 -wn MyNetwork
```

## Notes
- Ensure your WiFi adapter supports monitoring mode and is enabled.
- **Run as Administrator**: On Windows, run the script as an administrator for full functionality.

## Disclaimer
This tool is for educational purposes only. Use it responsibly and only on networks you own or have permission to test.



# RU
**GenWiFiFaker** - это инструмент для создания фальшивых точек доступа WiFi. Он может использоваться для тестирования безопасности сети, проведения демонстраций или других образовательных целей. Этот инструмент генерирует фальшивые SSID и MAC-адреса и транслирует их через указанный WiFi-интерфейс.

## Возможности
- **Генерация фальшивых SSID**: Создание нескольких фальшивых сетей WiFi с настраиваемыми именами.
- **Настраиваемость**: Определение количества сетей, их имен и используемого интерфейса.
- **Мультиплатформенность**: Работает как в Windows, так и в Linux.

## Требования
- **Python 3.x**
- **Библиотека Scapy**: Используется для создания и отправки сетевых пакетов.
- **Npcap (Windows) / libpcap (Linux)**: Необходим для захвата и отправки пакетов.

## Установка
- **Установите Python 3.x** с официального сайта.
- **Установите Scapy**: `pip install scapy`
- **Установите Faker**: `pip install faker`
- **Установите Npcap (Windows)**: Скачайте и установите с официального сайта Npcap.

## Использование
Для запуска программы используйте следующую команду:
```bash
python GenWiFiFaker.py -i [интерфейс] -c [кол-во сетей] -wn [имя сети]
```

## Examples
- **Создание 10 случайных сетей**:
```bash
python GenWiFiFaker.py -i wlan0mon -c 10
```
- **Создание сети с конкретным именем**:
```bash
python GenWiFiFaker.py -i wlan0mon -wn MyNetwork
```
- **Создание 5 сетей с конкретным именем**:
```bash
python GenWiFiFaker.py -i wlan0mon -c 5 -wn MyNetwork
```

## Примечания
- Убедитесь, что ваш WiFi-адаптер поддерживает режим мониторинга и включен.
- **Запуск от имени администратора**: В Windows запускайте скрипт от имени администратора для полной функциональности.

## Отказ от ответственности
Этот инструмент предназначен только для образовательных целей. Используйте его ответственно и только на сетях, которыми вы владеете или на которые у вас есть разрешение.
