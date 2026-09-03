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
- **Direcciones IP públicas:** IPv4 e IPv6.
- **Dirección MAC.**
- **Escáner de puertos locales:** visualiza qué puertos del dispositivo están abiertos y expuestos a la red.

### 2. 📡 Red
Analiza el entorno de red al que está conectado el equipo:
- **Información general:** nombre de la red (SSID) y tipo de seguridad.
- **Auditoría de seguridad:** análisis del nivel de seguridad de la conexión actual.
- **Escáner de red:** descubre otros dispositivos conectados a la misma red.
  - *Interacción:* al pulsar sobre un dispositivo vecino, REDvisor escanea y muestra sus puertos abiertos.

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

---

