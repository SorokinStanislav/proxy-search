class Proxy:
    host = '127.0.0.1'
    port = 0
    proxy_type = 'HTTP'
    latency = 1000
    country = 'RU'

    def __init__(self, host, port, proxy_type, latency, country):
        self.host = host
        self.port = port
        self.proxy_type = proxy_type
        self.latency = latency
        self.country = country

    def __str__(self) -> str:
        return "{host: " + self.host + ", port: " + self.port + ", type: " + \
               self.proxy_type + ", latency: " + self.latency + ", country: " + self.country + "}"

    def __eq__(self, other):
        return self.host == other.host and self.port == other.port

    def __lt__(self, other):
        return self.latency < other.latency

