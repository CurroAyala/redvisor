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

5. **_psutils_**: biblioteca utilizada para extraer información en tiempo real sobre el _hardware_.

6. **_subprocess_**: módulo que sirve para lanzar nuevos procesos y ejecutar comandos externos.

7. **_os_**: módulo que permite interactuar de forma estandarizada con las funciones del sistema operativo

---

