from pythonic_way_proxy_checker import HttpProxyChecker, Socks4ProxyChecker, Socks5ProxyChecker
from colorama import Fore, init
from threading import Thread
from time import sleep
from datetime import datetime
import os


def init_colors():
    init()

def load_proxies(proxyFile) -> list:

    proxies = open(proxyFile, 'r', encoding='utf-8').read().splitlines()

    return proxies


def save_working_proxy(proxy: str, proxy_type: str):

    with open(proxy_type + '.txt', 'a') as f:
        f.writelines([proxy,'\n'])


http_proxies = []
socks4_proxies = []
socks5_proxies = []
errors = []

def checker(proxy: str):
    red = Fore.RED
    green = Fore.GREEN

    http_checker = HttpProxyChecker(proxy, 10).start_checker()
    socks4_checker = Socks4ProxyChecker(proxy, 10).start_checker()
    socks5_checker = Socks5ProxyChecker(proxy, 10).start_checker()

    if http_checker:
        http_proxies.append(proxy)
        save_working_proxy(proxy, proxy_type='http')

    elif socks4_checker:
        socks4_proxies.append(proxy)
        save_working_proxy(proxy, proxy_type='socks4')

    elif socks5_checker:
        socks5_proxies.append(proxy)
        save_working_proxy(proxy, proxy_type='socks5')

    else:
        errors.append(proxy)


if __name__ == '__main__':
    red = Fore.RED
    green = Fore.GREEN
    white = Fore.WHITE
    os.system('cls')
    proxies_list = load_proxies(input('[+] Drag Proxies File Here ==> '))
    os.system('cls')

    threads = []

    for i in range(200):

        for proxy in proxies_list:
            os.system('cls')
            th = Thread(target=checker, args=(proxy,))
            th.start()
            threads.append(th)
            print(f'{white}[{str(datetime.time(datetime.now())).split(".")[0]}] {green}[+] Http: [{len(http_proxies)}] | {green}[+] Socks4: [{len(socks4_proxies)}] | [+] Socks5: [{len(socks5_proxies)}] | {red}[-] Dead: [{len(errors)}]', end=f'{green} ----> I / R / A / Q ', flush=True)
            
    for thread in threads:
        thread.join() 