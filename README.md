<div align="center">
  <img src="https://img.shields.io/badge/Python-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-green.svg?style=for-the-badge&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/OS-Linux%20%7C%20Windows-lightgrey.svg?style=for-the-badge&logo=linux&logoColor=white" alt="OS">
  <img src="https://img.shields.io/badge/Status-Estable-success.svg?style=for-the-badge" alt="Status">
</div>

<br>
<br>

<img src="assets/logo_1.jpg" alt="Logo Redvisor" width="150">

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

### 3. 🚦 Tráfico de conexiones
Monitor de tráfico en tiempo real controlado mediante botones de `Iniciar / Detener captura`. Detecta y clasifica las conexiones de red en entrantes y salientes, identificando la dirección IP remota, el tipo de protocolo utilizado (TCP, UDP o ICMP) y mostrando qué aplicación o proceso está realizando cada conexión.

  > **Nota**: este módulo combina el sondeo periódico de conexiones (TCP/UDP) con la escucha directa a bajo nivel de paquetes (ICMP). Presenta dos limitaciones clave: <br> 1. Conexiones fugaces: Al comprobar las conexiones mediante intervalos de tiempo, la herramienta omitirá cualquier conexión muy breve que se establezca y finalice entre un escaneo y el siguiente. <br> 2. Privilegios de ejecución: Requiere permisos de administrador (tanto en Linux como en Windows) para interceptar el tráfico de bajo nivel y vincular cada conexión a su proceso correspondiente; de lo contrario, el sistema bloqueará la lectura.

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

10. **_logging_**: módulo estándar para registrar o silenciar mensajes de estado o errores.

12. **_scapy_**: biblioteca que sirve para crear, manipular, enviar y capturar paquetes de red a bajo nivel. Necesita permisos de administrador.

13. **_queue_**: módulo para crear y gestionar colas de datos seguras para la programación concurrente (tareas en paralelo).

14. **_threading_**: módulo que permite crear y administrar hilos dentro de un mismo proceso, permitiendo ejecutar varias tareas en paralelo.

15. **_struct_**: módulo que sirve para convertir datos nativos de Python en estructuras de bytes puras, y viceversa.

---

## Instalación

> ❗ IMPORTANTE: para equipos con Windows, es necesario tener instalado el controlador **_npcap_** [https://npcap.com/] para el escaneo de red. A la hora de instalarlo, marcar la casilla _Install Npcap in WinPcap API-compatible Mode_.

### [Opción 1] Clonación del repositorio.

1. Clonar repositorio:
```
git clone https://github.com/CurroAyala/redvisor
```

2. Crear entorno virtual de Python:
```
python -m venv .venv
```

3. Acceder al entorno virtual:
```
source .venv/bin/activate (Linux)
source .\.venv\Scripts\Activate.ps1 (Windows Powershell)
```

4. Instalar dependencias:
```
pip install -r requirements.txt
```

6. Iniciar aplicación:
```
sudo .venv/bin/python main.py (Linux)
python main.py (Recomendado: iniciar la consola como administrador)
```

### [Opción 2] Descargar ejecutable.

#### Windows:

1. Descargar ejecutable (ver sección _Releases_).

2. Ejecutar.

3. En la primera ejecución, es probable que _Windows Defender_ bloquee el programa. Para evitar esto, **hacer clic** en la notificación de _Windows Defender_ (si la ha habido) o **abrir** _Seguridad de Windows_ e ir a _Protección antivirus y contra amenazas_ > _Historial de protección_. En la entrada más reciente (aceptar el aviso de administración para ver los detalles), **desplegar** el menú de acciones y **seleccionar** _Permitir_.

#### Fedora 42 en adelante y Arch Linux (y derivados):

> Nota: en general, se podrá instalar en distribuciones de Linux con la versión de _glibc_ (GNU C Library) 2.42 en adelante. Comprobar con: ```ldd --version```

1. Descargar y descomprimir el archivo _redvisor-linux.zip_ (ver sección _Releases_).

2. Ejecutar **_install.sh_** para instalar el programa y **_uninstall.sh_** para desinstalarlo.
    - Doble _click_ sobre el script.
    - A través de consola:
      ```
      ./install.sh (para instalar)
      ./uninstall.sh (para desinstalar)
      ```

3. (Opcional) Borrar la carpeta descargada.
