'''
Tabla de referencia puerto -> servicio habitual (usada como respaldo
si no se consigue identificar el servicio real mediante banner grabbing)
'''

SERVICIOS_CONOCIDOS = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    67: "dhcp-server", 68: "dhcp-client", 69: "tftp", 80: "http",
    88: "kerberos", 110: "pop3", 111: "rpcbind", 123: "ntp",
    135: "msrpc", 137: "netbios-ns", 138: "netbios-dgm",
    139: "netbios-ssn", 143: "imap", 161: "snmp", 162: "snmptrap",
    179: "bgp", 389: "ldap", 443: "https", 445: "smb", 465: "smtps",
    514: "syslog", 515: "printer (lpd)", 548: "afp", 554: "rtsp",
    587: "smtp (submission)", 631: "ipp", 636: "ldaps", 873: "rsync",
    993: "imaps", 995: "pop3s", 1080: "socks", 1194: "openvpn",
    1433: "mssql", 1521: "oracle-db", 1723: "pptp", 1883: "mqtt",
    2049: "nfs", 2181: "zookeeper", 3000: "http-alt (dev)",
    3128: "proxy (squid)", 3268: "ldap-gc", 3306: "mysql",
    3389: "rdp", 3690: "svn", 4443: "https-alt", 5000: "http-alt",
    5060: "sip", 5432: "postgresql", 5601: "kibana", 5900: "vnc",
    5985: "winrm-http", 5986: "winrm-https", 6379: "redis",
    6443: "kubernetes-api", 6667: "irc", 7001: "weblogic",
    7070: "realserver", 7077: "spark", 7443: "https-alt",
    8000: "http-alt", 8008: "http-alt", 8080: "http-proxy",
    8081: "http-alt", 8086: "influxdb", 8088: "http-alt",
    8090: "http-alt", 8443: "https-alt", 8888: "http-alt",
    9000: "http-alt / php-fpm", 9042: "cassandra", 9090: "prometheus",
    9092: "kafka", 9200: "elasticsearch", 9300: "elasticsearch-transport",
    9418: "git", 10000: "webmin", 11211: "memcached",
    15672: "rabbitmq-mgmt", 27017: "mongodb", 27018: "mongodb-shard",
    32400: "plex"
}
