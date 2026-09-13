<div align="center">
  <img src="https://img.shields.io/badge/Python-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-green.svg?style=for-the-badge&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/OS-Linux%20%7C%20Windows-lightgrey.svg?style=for-the-badge&logo=linux&logoColor=white" alt="OS">
  <img src="https://img.shields.io/badge/Status-En%20Desarrollo-orange.svg?style=for-the-badge" alt="Status">
</div>

# REDvisor 

**REDvisor** es una aplicación nativa para Linux y Windows diseñada para monitorizar, auditar y gestionar la información de red de un dispositivo. Actúa como un inspector de conexiones centralizado que permite conocer la huella digital, analizar el entorno de red local y rastrear el tráfico en tiempo real.

---

## Funcionalidades principales

La interfaz principal está dividida en tres secciones:

### 1. 💻 Dispositivo
Muestra la información de red vital del equipo:
- **Direcciones IP públicas y privadas:** IPv4 e IPv6.
- **Dirección MAC.**
- **Escáner de puertos locales:** visualiza qué puertos del dispositivo están abiertos y expuestos a la red.

### 2. 📡 Red
Analiza el entorno de red al que está conectado el equipo:
- **Información general:** SSID y protocolo de cifrado si la conexión es Wi-Fi y la máscara de red.
- **Evaluación de seguridad para conexiones Wi-Fi:** evaluación del nivel de seguridad de la conexión.
- **Escáner de red:** descubre otros dispositivos conectados a la misma red. Al pulsar sobre un dispositivo, REDvisor escanea y muestra sus puertos abiertos.

  > **Nota 1**: el descubrimiento de dispositivos activos en la red se realiza enviando un mensaje de _broadcast_ a nivel de la capa de enlace a todas las IPs de la red o subred, usando el protocolo **ARP (Address Resolution Protocol)** - encargado de traducir las direcciones lógicas (IP) a direcciones físicas (MAC). En este mensaje se pregunta que a qué dispositivo pertenece cada IP. Si existe un dispositivo con esa IP, su sistema operativo está obligado a responder inmediatamente aportando su dirección MAC, lo que revela su presencia en la red de forma instantánea e ineludible, saltándose las restricciones de los cortafuegos que normalmente bloquean los escaneos de puertos convencionales o los _pings_.

  > **Nota 2**: el escáner también deduce o aproxima - de forma no completamente fiable - el sistema operativo o tipo de dispositivo utilizando la dirección MAC asociada a cada IP obtenida en el barrido. Con los primeros caracteres de la MAC (el código OUI), busca el nombre del fabricante de la tarjeta de red en el archivo _oui.csv_ y, finalmente, cruza ese dato con una lista de equivalencias para estimar de forma aproximada qué dispositivo o sistema podría ser.

  > **Nota 3**: el reconocimiento del servicio en cada puerto se realiza mediante _banner grabbing_, por lo que el resultado no es completamente fiable. Esta técnica consiste en conectarse a un puerto abierto de un ordenador o servidor para intentar leer el mensaje de bienvenida (el _banner_) o las cabeceras de respuesta que envía el servicio que está escuchando en ese puerto.

### 3. 🚦 Tráfico y conexiones
Monitor de tráfico en tiempo real controlado mediante botones de `Iniciar / Detener captura`:
- **Conexiones salientes:** dominios a los que el equipo intenta conectarse.
- **Conexiones entrantes:** direcciones IP de los dispositivos externos que intentan conectarse al equipo.

---

## 🛠️ Stack tecnológico

El desarrollo de REDvisor se apoya en tecnologías eficientes y modernas para entornos de escritorio:

- **Backend:** [Python](https://www.python.org/)
- **Frontend:** [PySide6](https://doc.qt.io/qtforpython-6/) (Qt for Python)
- **Empaquetado:** [Nuitka](https://nuitka.net/)

### Módulos y bibliotecas utilizados

1. **_platform_**: módulo con la finalidad de extraer información sobre el entorno exacto en el que se está ejecutando el código.

2. **_socket_**: interfaz de bajo nivel para comunicaciones de red. Permite enviar y recibir datos a través de una red local o Internet, utilizando puertos y protocolos fundamentales como TCP o UDP.

3. **_urllib.request_**: módulo de alto nivel diseñado para abrir y leer _urls_. Permite descargar datos de páginas web o interactuar con APIs.

4. **_errno_**: módulo que contiene los códigos de error estándar que devuelve el sistema operativo.

5. **_psutil_**: biblioteca utilizada para extraer información en tiempo real sobre el _hardware_.

6. **_subprocess_**: módulo que sirve para lanzar nuevos procesos y ejecutar comandos externos.

7. **_os_**: módulo que permite interactuar de forma estandarizada con las funciones del sistema operativo.

8. **_ipaddress_**: módulo para crear, manipular y validar direcciones y redes de manera estructurada.

9. **_concurrent.futures_**: módulo que permite ejecutar tareas en paralelo o de forma asíncrona, permitiendo que tu programa haga varias cosas a la vez.

10. **_logging__*: módulo estándar para registrar o silenciar mensajes de estado o errores.

12. **_scapy__**: biblioteca que sirve para crear, manipular, enviar y capturar paquetes de red a bajo nivel. Necesita permisos de administrador.

---

