from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from selenium import webdriver

from ProxyType import ProxyType
from Proxy import Proxy

driver = webdriver.Firefox()

app = Flask(__name__)

proxies = {
    ProxyType.HTTP: [],
    ProxyType.SOCKS5: []
}


@app.route('/get_proxy/<proxy_type>')
def hello_world(proxy_type):
    host, port, error = '', '', ''

    if proxy_type.upper() == ProxyType.HTTP.value:
        proxy = proxies[ProxyType.HTTP][0]
        host = proxy.host
        port = proxy.port
        print('popped: ' + str(proxy))
    elif proxy_type.upper() == ProxyType.SOCKS5.value:
        proxy = proxies[ProxyType.SOCKS5][0]
        host = proxy.host
        port = proxy.port
    else:
        error = 'Type ' + proxy_type + ' is not supported'
    return jsonify(
        host=host,
        port=port,
        error=error
    )


def find_proxy():
    print('start proxy search')
    base_url = 'http://spys.one/proxies/'
    temp_proxies = []
    for i in range(5):
        url = base_url + str(i) + "/"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        table = soup.select("table")[2]
        rows = table.select("tr")
        for row in rows:
            cols = row.select("td")
            if len(cols) > 4:
                if cols[0].text != 'Proxy адрес:порт':
                    host_string = cols[0].select("font")[1].text
                    split_by_colon = host_string.split(':')
                    host = split_by_colon[0].split('document')[0]
                    port = split_by_colon[2]

                    proxy_type = str(cols[1].select("font")[0].contents[0])

                    latency = cols[3].select("font")[0].text

                    country = str(cols[4].select("font")[0].contents[0])

                    proxy = Proxy(host, port, proxy_type, latency, country)

                    temp_proxies.append(proxy)

    proxies[ProxyType.HTTP].clear()
    proxies[ProxyType.SOCKS5].clear()

    for proxy_item in temp_proxies:
        item_proxy_type = proxy_item.proxy_type.upper()
        if item_proxy_type == ProxyType.HTTP.value:
            proxies[ProxyType.HTTP].append(proxy_item)
        elif item_proxy_type == ProxyType.SOCKS5.value:
            proxies[ProxyType.SOCKS5].append(proxy_item)

    proxies[ProxyType.HTTP].sort()
    proxies[ProxyType.SOCKS5].sort()

    print(str(len(proxies[ProxyType.HTTP])) + ' HTTP proxies found')
    print(str(len(proxies[ProxyType.SOCKS5])) + ' SOCKS proxies found')


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(find_proxy, 'interval', minutes=5)
scheduler.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
