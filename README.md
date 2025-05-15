# Seyfer Studios Official Website Backend

Seyfer Studios Official Website Backend code.

## Routes

<!-- - **Index**: `/` -->

- **Admin**: `/admin`
- **DJ**:
  - **API**:
    - `/api/dj/beatport`
    - `/api/dj/beatport/artists/yes`
    - `/api/dj/beatport/artists/ban`

## Módulos estándar (internos)

- [os](https://docs.python.org/3/library/os.html): este módulo ofrece una forma portátil de utilizar funcionalidades dependientes del sistema operativo.

- [sys](https://docs.python.org/3/library/sys.html): este módulo proporciona acceso a algunas variables utilizadas o mantenidas por el intérprete y a funciones que interactúan estrechamente con él. Siempre está disponible. A menos que se indique explícitamente lo contrario, todas las variables son de solo lectura.

- [time](https://docs.python.org/3/library/time.html):

## Paquetes de terceros (externos)

- [Django](https://www.djangoproject.com/): es un framework web de alto nivel para [Python](https://www.python.org/) que fomenta el desarrollo rápido y un diseño limpio y pragmático. Creado por desarrolladores con experiencia, se encarga de gran parte del trabajo tedioso del desarrollo web, por lo que puedes concentrarte en escribir tu aplicación sin necesidad de reinventar la rueda. Es gratuito y de código abierto.

- [mutagen](https://mutagen.readthedocs.io/en/latest/): es un módulo de [Python](https://www.python.org/) para manejar metadatos de archivos de audio. Es compatible con archivos de audio ASF, FLAC, MP4, Monkey’s Audio, MP3, Musepack, Ogg Opus, Ogg FLAC, Ogg Speex, Ogg Theora, Ogg Vorbis, True Audio, WavPack, OptimFROG y AIFF. Soporta todas las versiones de ID3v2, y analiza todos los cuadros estándar de ID3v2.4. Puede leer cabeceras Xing para calcular con precisión la tasa de bits y la duración de archivos MP3. Las etiquetas ID3 y APEv2 se pueden editar independientemente del formato de audio. También puede manipular flujos Ogg a nivel de paquetes o páginas individuales.

- [Selenium](https://www.selenium.dev/): es una herramienta de automatización de navegadores web. Permite simular el comportamiento de un usuario real al interactuar con una página web, lo cual es útil para tareas como:

  - Automatizar pruebas de interfaz de usuario (UI).
  - Rellenar formularios automáticamente.
  - Extraer contenido dinámico que depende de JavaScript.
  - Navegar por sitios como si fueras un humano (clics, scroll, etc.).

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): es una biblioteca de [Python](https://www.python.org/) para extraer datos de archivos **HTML** y **XML**. Funciona con tu analizador (_parser_) favorito para ofrecer formas intuitivas de navegar, buscar y modificar el árbol de análisis. Comúnmente ahorra a los programadores horas o incluso días de trabajo.
