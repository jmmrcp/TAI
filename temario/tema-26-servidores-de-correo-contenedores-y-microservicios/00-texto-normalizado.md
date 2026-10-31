Bloque 4 - Punto 3: Administración de servidores de correo
electrónico sus protocolos. Administración de contenedores
                     y microservicios.




                            1
                            Correo electrónico. Contenedores y microservicios



Contents

1. Administración de servidores de correo electrónico                                                         3
   1.1. Conceptos fundamentales del correo electrónico . . . . . . . . . . . . . . . . . . . . . .            3
   1.2. Protocolos de correo electrónico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     11
   1.3. Instalación y configuración de servidores de correo . . . . . . . . . . . . . . . . . . . .          22
   1.4. Seguridad en servidores de correo . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      32
   1.5. Gestión de spam y filtrado . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   45
   1.6. Administración y mantenimiento . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         52

2. Administración de contenedores                                                                              63
   2.1. Introducción a la contenedorización . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 63
   2.2. Docker . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 69
   2.3. Otras tecnologías de contenedores . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 86
   2.4. Orquestación de contenedores . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 93
   2.5. Seguridad en contenedores . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107

3. Administración de microservicios                                                                        119
   3.1. Arquitectura de microservicios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
   3.2. Diseño de microservicios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 128
   3.3. Despliegue de microservicios . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 138
   3.4. Monitorización y observabilidad . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 147
   3.5. Gestión de configuración y secretos . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157




Bloque IV - Punto 3                                 2 de 164                                   January 31, 2026
                         Correo electrónico. Contenedores y microservicios



1. Administración de servidores de correo electrónico

1.1. Conceptos fundamentales del correo electrónico
El correo electrónico, o e-mail, es un servicio de red que permite a los usuarios enviar y recibir
mensajes de forma asíncrona a través de sistemas de comunicación electrónica. A diferencia de la
mensajería instantánea, el correo electrónico se basa en un modelo de almacenamiento y reenvío
(store-and-forward), donde los mensajes no se entregan directamente al destinatario en tiempo
real, sino que se depositan en servidores intermedios hasta que el receptor decide acceder a ellos.
Para que este proceso sea exitoso y universal, la administración de servidores de correo debe
apoyarse en una arquitectura estandarizada que garantice la interoperabilidad entre diferentes
proveedores y plataformas. Esta arquitectura no es un bloque monolítico, sino un ecosistema
de agentes especializados que interactúan entre sí bajo reglas estrictas (protocolos) y formatos
normalizados. Entender el flujo de un mensaje implica comprender desde la interfaz que utiliza
el usuario final hasta la lógica de transporte que mueve los datos a través de Internet, así como la
estructura técnica que define qué es, exactamente, un mensaje de correo válido.
A continuación, se presenta una tabla resumen de los pilares que componen estos conceptos
fundamentales y que se detallarán en los siguientes apartados:


Concepto Clave                                     Descripción

Arquitectura de Red                                El diseño jerárquico y distribuido que permite
                                                   el salto del correo entre distintos nodos de la
                                                   red.
Agentes (MUA, MTA, MDA, MSA)                       Los distintos roles de software encargados de la
                                                   composición, transporte, entrega y envío del
                                                   mensaje.
Estándares de Formato                              Las normativas (como la RFC 5322) que
                                                   definen la estructura del mensaje: cabeceras,
                                                   cuerpo y metadatos.
Modelo Cliente-Servidor                            La relación de dependencia entre los
                                                   terminales de usuario y los servidores que
                                                   custodian la información.


Administrar este servicio requiere, por tanto, una visión integral que combine el conocimiento
de la infraestructura física con el dominio de la lógica de software, asegurando que cada pieza del
engranaje cumpla con su función específica para evitar la pérdida de información o el rechazo de
los envíos.

1.1.1. Arquitectura del sistema de correo electrónico

El sistema de correo electrónico en Internet es, fundamentalmente, un sistema especializado
de transferencia de archivos que opera bajo el modelo de almacenamiento y reenvío (store-
and-forward). Esta arquitectura permite que el mensaje atraviese múltiples redes y sistemas
operativos de manera asíncrona, garantizando que el receptor pueda acceder al contenido
independientemente de si el emisor está conectado simultáneamente.


Bloque IV - Punto 3                           3 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


Para comprender su funcionamiento de cara al examen, es imprescindible descomponer el sistema
en sus agentes de software funcionales. Aunque en implementaciones pequeñas varios roles
pueden residir en el mismo servidor físico, lógicamente son distintos.

Agentes del Sistema de Mensajería (MHS)

El sistema de manejo de mensajes (Message Handling Service - MHS) se divide en roles específicos
encargados de una fase del ciclo de vida del correo.


Agente                  Nombre Completo            Función Principal          Protocolos Típicos

MUA                     Mail User Agent            Aplicación cliente que     SMTP (envío),
                                                   interactúa con el          IMAP/POP3
                                                   usuario. Permite           (recepción)
                                                   redactar, leer y
                                                   organizar mensajes.
MSA                     Mail Submission Agent      Primer punto de            SMTP (puerto 587)
                                                   contacto en el
                                                   servidor. Recibe el
                                                   correo del MUA, valida
                                                   políticas
                                                   (autenticación) y lo
                                                   pasa al MTA.
MTA                     Mail Transfer Agent        El “enrutador” del         SMTP (puerto 25)
                                                   correo. Transfiere
                                                   mensajes entre
                                                   servidores (hosts) a
                                                   través de Internet.
MDA                     Mail Delivery Agent        Responsable de la          LMTP, Local
                                                   entrega final. Recibe el
                                                   mensaje del MTA y lo
                                                   deposita en el buzón
                                                   local del usuario.
MAA                     Message Access Agent       Intermediario que          IMAP, POP3
                                                   permite al MUA
                                                   recuperar mensajes
                                                   almacenados en el
                                                   servidor.
MS                      Message Store              Repositorio físico         mbox, Maildir
                                                   (base de datos o
                                                   sistema de ficheros)
                                                   donde residen los
                                                   mensajes hasta su
                                                   lectura.




Bloque IV - Punto 3                           4 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


1.1.1.1. Flujo de la Comunicación

El trayecto de un correo electrónico desde el remitente hasta el destinatario implica una cadena
de custodia entre los agentes mencionados. El proceso se estructura en las siguientes fases:




                                     Figure 1: Flujo del correo


1. Composición y Envío (MUA → MSA)

El usuario redacta el mensaje en su MUA (ej. Outlook, Thunderbird, Webmail). El MUA envía el
mensaje al servidor de correo saliente del usuario, específicamente al MSA.
    • Nota de examen: El MSA suele requerir autenticación para evitar el relay abierto y el spam.

2. Enrutamiento y Transferencia (MTA → MTA)

El MSA transfiere el mensaje al MTA del remitente. El MTA analiza la dirección del destinatario y
utiliza el DNS (Sistema de Nombres de Dominio) para buscar el registro MX (Mail Exchange) del
dominio de destino.
    • El MTA de origen establece una conexión TCP con el MTA de destino y transfiere el mensaje
      mediante el protocolo SMTP.
    • Si el destino no está disponible, el MTA almacena el mensaje en una cola (spool) para
      reintentarlo más tarde.

3. Entrega Local (MTA → MDA → MS)

Una vez que el mensaje llega al MTA del destinatario, este lo pasa al MDA. El MDA realiza
comprobaciones finales (filtros de spam locales, reglas de usuario) y deposita el mensaje en el
Message Store (MS) del usuario.

4. Acceso y Recuperación (MAA → MUA)

El mensaje permanece en el servidor hasta que el usuario destinatario conecta su MUA. El MUA
utiliza un MAA (mediante protocolos POP3 o IMAP) para descargar o sincronizar los mensajes
desde el servidor a su dispositivo.

1.1.1.2. Componentes de Infraestructura Adicionales

Para que la arquitectura funcione correctamente, se requieren servicios de red de apoyo críticos:




Bloque IV - Punto 3                          5 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  1. DNS y Registros MX: El sistema de correo depende absolutamente del DNS. Los registros
     MX (Mail Exchange) indican qué servidor está autorizado para recibir correo en nombre de
     un dominio.
        • Prioridad MX: Un dominio puede tener múltiples registros MX con diferentes
          prioridades. El MTA emisor intentará contactar primero con el de menor valor
          numérico (mayor prioridad).
  2. Webmail: El Webmail es una implementación particular de un MUA que se ejecuta en un
     servidor web y se accede mediante un navegador. Detrás de escena, el servidor de Webmail
     actúa como un cliente IMAP/SMTP contra la infraestructura de correo.

Probables Focos de Examen

    • Distinción MTA vs MDA: Es común que pregunten quién “transporta” el correo a través de
      Internet (MTA) frente a quién lo “deposita” en el buzón final (MDA).
    • Protocolos por fase:
        – Transferencia entre servidores: SMTP.
        – Descarga/Acceso por el usuario: POP3 / IMAP.
        – Nunca confundir: El usuario envía usando SMTP (vía MSA/MTA) pero recibe usando
           POP/IMAP.
    • Registro DNS: Identificar el registro MX como el esencial para la recepción de correo.

1.1.2. Componentes: MUA, MTA, MDA y MSA

Para el aspirante a TAI, es fundamental no solo conocer las siglas, sino comprender la
responsabilidad exclusiva de cada componente en la cadena de transmisión. El sistema de
correo electrónico no es monolítico, sino un conjunto de agentes especializados que cooperan
secuencialmente.
A continuación, se desglosan los cuatro componentes principales según la arquitectura estándar
de Internet.

1.1.2.1. MUA (Mail User Agent) – Agente de Usuario de Correo

El MUA es la aplicación que actúa como interfaz directa con el usuario final. Su función es permitir
la composición, lectura y gestión de los mensajes de correo electrónico.
    • Funciones Principales:
       1. Composición: Proporciona un editor para redactar el cuerpo del mensaje y definir las
          cabeceras (To, Cc, Subject).
       2. Envío: Entrega el mensaje generado al MSA (o directamente a un MTA en configuraciones
          antiguas) utilizando el protocolo SMTP.
       3. Recuperación: Descarga o sincroniza mensajes desde el servidor (Message Store)
          utilizando protocolos de acceso como POP3 o IMAP.
    • Tipos de MUA:
        – Clientes de escritorio: Microsoft Outlook, Mozilla Thunderbird, Apple Mail.
        – Webmail: Aplicaciones basadas en navegador (ej. Roundcube, OWA, Gmail). Aunque
          se ejecutan en un servidor web, funcionalmente actúan como un MUA frente a la
          infraestructura de correo.
      Nota de Examen: El MUA no “envía” el correo a través de Internet hasta el destino final;
      solo lo entrega al primer servidor de la cadena (el MSA/MTA).


Bloque IV - Punto 3                           6 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios




1.1.2.2. MSA (Mail Submission Agent) – Agente de Envío de Correo

El MSA es el punto de entrada al sistema de correo para los mensajes salientes. Actúa como
intermediario entre el MUA y el MTA.
    • Funciones Principales:
       1. Autenticación: Verifica las credenciales del usuario antes de aceptar el mensaje,
          previniendo el relay abierto y el spam.
       2. Normalización: Asegura que el mensaje cumpla con los estándares de Internet (RFC)
          antes de pasarlo al MTA. Puede corregir cabeceras defectuosas o añadir el dominio si
          falta.
       3. Separación de tráfico: Permite distinguir el tráfico de envío de usuarios legítimos del
          tráfico de transferencia entre servidores.
    • Protocolos y Puertos:
        – Utiliza SMTP.
        – El puerto estándar para el MSA es el 587. Históricamente se usaba el 25, pero
          actualmente el 25 se reserva preferentemente para la comunicación MTA-a-MTA.
      Matiz Importante: A menudo, el MSA y el MTA son el mismo software (ej. Postfix o
      Sendmail) ejecutándose con configuraciones diferentes o en puertos distintos, pero
      lógicamente son agentes separados.



1.1.2.3. MTA (Mail Transfer Agent) – Agente de Transferencia de Correo

El MTA es el componente central de la infraestructura, encargado del enrutamiento y la
transferencia del mensaje a través de Internet hasta llegar al servidor del destinatario.
    • Funciones Principales:
       1. Enrutamiento: Consulta el DNS para obtener los registros MX (Mail Exchange) del
          dominio destinatario y resolver la dirección IP del servidor destino.
       2. Transporte: Establece conexiones SMTP (puerto 25) con otros MTAs para transferir el
          mensaje.
       3. Almacenamiento y Reenvío (Store-and-Forward): Si el destino no está disponible,
          almacena el mensaje en una cola (spool) y reintenta el envío periódicamente.
       4. Generación de DSN: Si el mensaje no puede entregarse tras varios intentos, genera un
          mensaje de rebote (Delivery Status Notification) al remitente.
    • Ejemplos de Software MTA:
        – Postfix: Modular, seguro y rápido. El predeterminado en muchas distribuciones Linux.
        – Sendmail: El clásico, monolítico y complejo de configurar (usando macros m4).
        – Microsoft Exchange: Actúa como MTA en entornos Windows.
        – Qmail / Exim.



1.1.2.4. MDA (Mail Delivery Agent) – Agente de Entrega de Correo

El MDA (a veces llamado LDA - Local Delivery Agent) es el responsable de la etapa final: recibir el
mensaje del MTA y depositarlo en el buzón del usuario (Message Store).


Bloque IV - Punto 3                           7 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Funciones Principales:
       1. Entrega Local: Escribe el mensaje en el disco duro del servidor, en el formato de
          almacenamiento correspondiente (ej. mbox o Maildir).
       2. Filtrado: Puede invocar scripts o filtros (como Sieve o Procmail) para clasificar el correo
          en carpetas específicas, rechazar spam o aplicar reglas de vacaciones antes de guardarlo.
    • Protocolos:
        – A menudo el MTA pasa el correo al MDA mediante la ejecución de un comando local o
          usando el protocolo LMTP (Local Mail Transfer Protocol), una variante de SMTP diseñada
          para entregas locales sin cola.
    • Ejemplos de Software MDA:
        – Dovecot: Muy popular, actúa como MDA (entrega) y también como servidor IMAP/POP3.
        – Procmail: Clásico en entornos Unix para filtrado.
        – Bin/mail o Mail.local: MDAs básicos del sistema.



Resumen del Flujo de Correo

El siguiente esquema ilustra la interacción secuencial de estos componentes para un correo
enviado desde Alice (origen) hacia Bob (destino):
      ORIGEN (Alice)                                         DESTINO (Bob)
   +-----------------+                                   +-----------------+
   |      MUA        | (1) Composición                   |       MUA       | (5) Lectura
   | (Outlook/Web)   |                                   | (Outlook/Web)   |
   +--------+--------+                                   +--------^--------+
            | SMTP (587)                                          | IMAP/POP3
            v                                                     |
   +--------+--------+      SMTP (25)      +-------------+        |
   |      MSA        | ------------------> |     MTA     |        |
   | (Autenticación) |      Internet       | (Entrante) |         |
   +--------+--------+                     +------+------+        |
            |                                     |               |
            v                                     v               |
   +--------+--------+                     +------+------+        |
   |      MTA        |                     |     MDA     | -------+
   |   (Saliente)    |                     | (Entrega) |
   +-----------------+                     +-------------+
                                           (Guarda en Buzón)


Probables Focos de Examen

    • Diferencia MTA vs MDA: El examen suele presentar escenarios donde se debe identificar qué
      agente realiza el almacenamiento físico en el buzón (MDA) frente a cuál realiza el transporte
      entre dominios (MTA).
    • Protocolos:
        – MTA ↔ MTA: SMTP (Puerto 25).
        – MUA → MSA: SMTP (Puerto 587/25).
        – MDA → Buzón: Escritura directa o LMTP.
        – MUA ← Buzón: POP3 (110/995) o IMAP (143/993).
    • Identificación de Software: Saber que Postfix y Sendmail son típicamente MTAs, mientras
      que Dovecot suele actuar como MDA y servidor POP/IMAP.
    • Webmail: Recordar que un Webmail (como Roundcube) es técnicamente un MUA.


Bloque IV - Punto 3                           8 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.1.3. Formato de mensajes según RFC 5322

El RFC 5322 (Internet Message Format) es el estándar que define la sintaxis para los mensajes
de texto enviados entre usuarios de computadoras en el marco del correo electrónico. Este
documento, publicado en octubre de 2008, actualiza y obsoleta al RFC 2822, el cual a su vez
sustituyó al histórico RFC 822.
Es fundamental comprender que esta especificación se aplica únicamente al contenido del
mensaje (cabeceras y cuerpo), y no al sobre (envelope) que es gestionado por el protocolo de
transporte SMTP (RFC 5321).

1.1.3.1. Estructura Léxica y Sintáctica General

Un mensaje conforme a RFC 5322 es una secuencia de caracteres US-ASCII (valores del 1 al 127).
La estructura básica se divide en dos partes separadas por una línea vacía:
  1. Sección de Cabecera (Header Section): Conjunto de líneas con campos definidos.
  2. Línea de separación: Una línea vacía (CRLF).
  3. Cuerpo (Body): Secuencia de caracteres que sigue a la cabecera.
Reglas de longitud y delimitación:
    • Delimitador de línea: Las líneas deben estar delimitadas por la secuencia Carriage Return y
      Line Feed (CRLF).
    • Límite de caracteres:
        – Obligatorio (MUST): Ninguna línea puede exceder los 998 caracteres (excluyendo el
           CRLF).
        – Recomendado (SHOULD): Las líneas deberían limitarse a 78 caracteres (excluyendo el
           CRLF) para garantizar la correcta visualización en interfaces de usuario.

1.1.3.2. Campos de Cabecera (Header Fields)

Los campos de cabecera son líneas que comienzan con un nombre de campo, seguido de dos
puntos (:), y posteriormente el cuerpo del campo (field body).
Mecanismo de plegado (Folding): Para sortear los límites de longitud de línea, los campos de
cabecera largos pueden dividirse en múltiples líneas insertando un CRLF seguido de un espacio
en blanco (WSP - White Space). El proceso inverso, para la interpretación semántica, se denomina
“desplegado” (unfolding).
A continuación, se detallan los campos más relevantes para el examen, clasificados por su función:
1. Campos de Origen (Originator Fields)


Campo                            Sintaxis                           Descripción y Reglas,

From:                            From: mailbox-list                 Obligatorio. Especifica el
                                                                    autor(es) del mensaje (quien lo
                                                                    escribió).




Bloque IV - Punto 3                           9 de 164                              January 31, 2026
                           Correo electrónico. Contenedores y microservicios



Campo                              Sintaxis                           Descripción y Reglas,

Sender:                            Sender: mailbox                    Especifica el agente
                                                                      responsable de la transmisión
                                                                      real. Obligatorio si el From
                                                                      contiene múltiples direcciones
                                                                      o si el transmisor difiere del
                                                                      autor. Si es idéntico al From, no
                                                                      debe usarse.
Reply-To:                          Reply-To: address-list             Opcional. Indica la dirección a
                                                                      la que se sugiere enviar las
                                                                      respuestas. Si no existe, se
                                                                      responde al From.


2. Campos de Destino (Destination Address Fields)

Campo                                               Descripción„

To:                                                 Destinatarios principales del mensaje.
Cc:                                                 Carbon Copy. Destinatarios secundarios que
                                                    reciben copia (informativo).
Bcc:                                                Blind Carbon Copy. Destinatarios ocultos.
                                                    Existen múltiples formas de implementación;
                                                    la dirección no debe revelarse a otros
                                                    destinatarios en la cabecera final entregada.


3. Campos de Identificación y Fecha
      • Date: (Obligatorio). Especifica la fecha y hora en la que el creador del mensaje indicó que
        este estaba completo (listo para envío). No es necesariamente la hora de transporte.
      • Message-ID: (Recomendado/Should). Identificador único global para una versión específica
        del mensaje. Su formato suele incluir un identificador a la izquierda y un dominio a la
        derecha (ej. <id-unico@dominio.com>).
4. Campos Informativos y de Referencia
      • Subject: Cadena corta que identifica el tema del mensaje. En respuestas, puede prefijarse
        con “Re:”.
      • In-Reply-To: Contiene el Message-ID del mensaje “padre” al que se está respondiendo.
      • References: Identifica el “hilo” de la conversación, conteniendo los Message-ID de mensajes
        anteriores y del padre.

1.1.3.3. Relación con MIME

El RFC 5322 especifica una sintaxis solo para mensajes de texto US-ASCII. No prevé la transmisión
de imágenes, audio u otros datos estructurados. Para superar esta limitación, se utilizan las
extensiones MIME (RFC 2045, 2046, 2049), las cuales estructuran los mensajes para que se ajusten
a la sintaxis del RFC 5322.

Bloque IV - Punto 3                            10 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.1.3.4. Probables focos de examen

En las preguntas tipo test para TAI, es frecuente encontrar cuestiones sobre los límites técnicos y
la obligatoriedad de ciertos campos.
  1. Límite de caracteres por línea:
        • Recordar la cifra exacta: 998 caracteres como límite máximo obligatorio (Hard limit).
        • No confundir con la recomendación de interoperabilidad de 78 caracteres.
  2. Campos Obligatorios:
        • Pregunta clásica: “¿Qué campos son estrictamente obligatorios en una cabecera RFC
          5322?”.
        • Respuesta: Date y From (y Sender bajo condiciones específicas). El campo Subject o
          Message-ID, aunque recomendados, no son sintácticamente obligatorios para la validez
          mínima, aunque casi siempre están presentes.
  3. Diferencia From vs Sender:
        • El From es el autor intelectual.
        • El Sender es quien lo envía/transmite.
        • El Sender solo aparece si es diferente del From o si hay múltiples From.
  4. Separación Cabecera/Cuerpo:
        • Identificar que la separación es una línea vacía (secuencia CRLF CRLF).
  5. Codificación:
        • Saber que el estándar base es US-ASCII (7 bits). Cualquier otro carácter (tildes, eñes)
          requiere codificación MIME.

1.2. Protocolos de correo electrónico
Esta sección analiza el conjunto de reglas y estándares técnicos que permiten la comunicación
entre los diferentes agentes del sistema de correo. Sin estos protocolos, el intercambio de mensajes
entre servidores de distintos fabricantes o países sería imposible, ya que actúan como el lenguaje
común de la red.
En el ecosistema del correo electrónico, los protocolos se dividen fundamentalmente en dos
categorías según su función: el transporte (envío) y el acceso (recepción/consulta). Mientras
que el envío está estandarizado globalmente bajo un único protocolo, el acceso al buzón ofrece
distintas filosofías de trabajo dependiendo de si el usuario necesita movilidad, sincronización
múltiple o ahorro de recursos en el servidor.
La siguiente tabla resume los protocolos que se desarrollarán en este apartado, destacando su
función principal y los puertos estandarizados por la IANA (Internet Assigned Numbers Authority):

                                                   Puertos Estándar
Protocolo                Función Principal         (Cifrado)                 Tipo

SMTP                     Transferencia y envío     25, 465, 587              Transporte
                         de mensajes entre
                         servidores.
POP3                     Descarga de mensajes      110, 995                  Acceso
                         del servidor al
                         dispositivo local.




Bloque IV - Punto 3                          11 de 164                                January 31, 2026
                        Correo electrónico. Contenedores y microservicios



                                                 Puertos Estándar
Protocolo               Función Principal        (Cifrado)                  Tipo

IMAP                    Acceso y gestión de      143, 993                   Acceso
                        mensajes
                        directamente en el
                        servidor.


Es importante destacar que, aunque estos protocolos nacieron en una era donde la seguridad
no era la prioridad, la administración moderna de servidores exige el uso de sus variantes
cifradas mediante TLS/SSL. El dominio de estos protocolos es el pilar básico para cualquier
administrador, ya que permite diagnosticar fallos de conexión, optimizar el tráfico de red y
garantizar la integridad de las comunicaciones.

1.2.1. SMTP (Simple Mail Transfer Protocol)

El Simple Mail Transfer Protocol (SMTP) es el estándar de facto para la transmisión de correo
electrónico a través de redes IP. Definido originalmente en la RFC 821 (1982) y actualizado
actualmente por la RFC 5321 (2008), este protocolo se encarga del transporte fiable y ordenado
de mensajes desde el servidor del remitente hasta el servidor del destinatario, actuando como un
mecanismo de “retransmisión” (relaying) a través de diversos Agentes de Transferencia de Correo
(MTA).
Es fundamental comprender que SMTP se ocupa exclusivamente del transporte y la entrega al
servidor destino; no gestiona el almacenamiento final en el buzón del usuario ni la recuperación
del mismo por parte del cliente, funciones reservadas para MDA, POP3 e IMAP.

1.2.1.1. Características Técnicas y Modelo de Funcionamiento

SMTP opera sobre el protocolo TCP (Transmission Control Protocol) en la capa de transporte,
garantizando una entrega fiable de los datos. Su funcionamiento se basa en el envío de comandos
en formato ASCII de 7 bits y la recepción de códigos de estado numéricos.
Puertos Estándar:

Puerto                          Uso Principal                      Descripción

25                              MTA a MTA                          Puerto estándar original para
                                                                   la retransmisión de correo
                                                                   entre servidores a través de
                                                                   Internet. A menudo bloqueado
                                                                   por ISPs para usuarios finales
                                                                   para evitar spam.




Bloque IV - Punto 3                         12 de 164                                January 31, 2026
                        Correo electrónico. Contenedores y microservicios



Puerto                          Uso Principal                      Descripción

587                             MUA a MSA                          Puerto estándar para la
                                                                   sumisión de correo
                                                                   (Submission). Requiere
                                                                   habitualmente autenticación
                                                                   y es el utilizado por clientes de
                                                                   correo (Outlook, Thunderbird)
                                                                   para enviar mensajes.
465                             SMTPS                              Puerto “legacy” para SMTP
                                                                   sobre SSL. Aunque obsoleto en
                                                                   favor de STARTTLS sobre
                                                                   587/25, sigue siendo
                                                                   soportado por muchos
                                                                   proveedores para
                                                                   compatibilidad.


Modelo de Comunicación: La comunicación es unidireccional durante una sesión. Si el servidor
receptor necesita enviar mensajes al emisor original, debe establecer una nueva conexión TCP en
sentido inverso.

1.2.1.2. Fases de una Sesión SMTP

Una transacción SMTP estándar se estructura en tres fases lógicas secuenciales:
  1. Establecimiento de conexión (Connection Setup):
        • El cliente SMTP abre una conexión TCP con el servidor.
        • El servidor responde con un código 220 (Service Ready).
        • El cliente se identifica mediante el comando HELO (SMTP clásico) o EHLO (Extended SMTP)
          indicando su dominio FQDN.
  2. Transferencia de correo (Mail Transfer): Esta fase implica una secuencia estricta de
     comandos para definir el “sobre” (envelope) y el contenido:
        • MAIL FROM: Identifica al originador del mensaje (remitente del sobre o Return-Path).
          Es el inicio lógico de la transacción de un mensaje específico.
        • RCPT TO: Identifica al destinatario. Puede repetirse múltiples veces para enviar el
          mismo mensaje a varios destinatarios. El servidor confirma cada receptor aceptado
          con un 250 OK.
        • DATA: Indica al servidor que a continuación se enviará el contenido del mensaje
          (cabeceras RFC 5322 y cuerpo). El servidor suele responder con 354 Start mail input.
        • Finalización de datos: El cliente indica el fin del mensaje enviando una línea que
          contiene únicamente un punto (<CRLF>.<CRLF>).
  3. Cierre de conexión (Connection Termination):
        • El cliente envía el comando QUIT.
        • El servidor responde (normalmente 221) y cierra el canal TCP.

1.2.1.3. Comandos y Códigos de Respuesta

Para el examen, es crítico distinguir entre los comandos que emite el cliente y los códigos
numéricos que devuelve el servidor.

Bloque IV - Punto 3                         13 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


Comandos Principales (RFC 5321):


Comando                                            Función

HELO / EHLO                                        Identificación del cliente. EHLO solicita el modo
                                                   extendido (ESMTP) para ver capacidades
                                                   soportadas (ej. STARTTLS, AUTH).
MAIL FROM                                          Inicia la transacción e indica la dirección de
                                                   retorno (envelope sender).
RCPT TO                                            Especifica un destinatario (envelope recipient).
DATA                                               Inicia la transmisión del contenido del
                                                   mensaje.
RSET                                               Reset. Aborta la transacción actual sin cerrar la
                                                   conexión TCP.
VRFY                                               Verifica si un buzón existe en el servidor (a
                                                   menudo deshabilitado por seguridad para
                                                   evitar enumeración de usuarios).
NOOP                                               No Operation. Mantiene la sesión activa sin
                                                   realizar acciones.
QUIT                                               Cierra la sesión.


Códigos de Estado (Status Codes): Los servidores responden con códigos de tres dígitos. El primer
dígito es el más relevante para la gestión de errores:
    • 2xx (Éxito): La acción se completó correctamente (ej. 250 OK, 220 Service Ready).
    • 3xx (Pendiente): El comando fue aceptado, pero se requiere más información (ej. 354 tras el
      comando DATA).
    • 4xx (Error Temporal): El fallo es transitorio; el cliente debería reintentar más tarde (ej. 421
      Service not available, 450 Mailbox busy). Es la base del Greylisting.
    • 5xx (Error Permanente): La acción falló y no debe reintentarse (ej. 550 User unknown, 500
      Syntax error, 554 Transaction failed).


1.2.1.4. Limitaciones y ESMTP

El protocolo SMTP original (RFC 821) presenta limitaciones significativas que se abordan mediante
ESMTP (Extended SMTP) y extensiones MIME:
  1. Restricción ASCII 7-bits: SMTP fue diseñado para texto ASCII de 7 bits. No soporta
     nativamente caracteres internacionales (tildes, eñes) ni archivos binarios (imágenes,
     ejecutables).
        • Solución: Uso de MIME (Multipurpose Internet Mail Extensions) para codificar estos
          datos en texto ASCII antes de la transmisión.
  2. Falta de Seguridad: SMTP transmite en texto claro (cleartext).
        • Solución: La extensión STARTTLS (RFC 3207) permite elevar una conexión de texto
          plano a una cifrada (TLS) sobre el mismo puerto.



Bloque IV - Punto 3                           14 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  3. Autenticación: Originalmente no requería autenticación, facilitando el Email Spoofing y los
     Open Relays.
       • Solución: SMTP-AUTH (RFC 4954) utiliza SASL para autenticar al cliente ante el servidor.

1.2.1.5. Probables focos de examen

    • Puertos de servicio:
        – Pregunta frecuente: Diferenciar el puerto 25 (intercambio entre servidores/MTA) del
          puerto 587 (envío desde cliente/MSA).
        – El puerto 465 suele aparecer como opción incorrecta para estándares modernos
          (asociado a SMTPS legacy), aunque se usa en implementaciones específicas.
    • Secuencia de comandos:
        – Memorizar el orden estricto: HELO → MAIL FROM → RCPT TO → DATA.
        – Saber que el comando DATA finaliza con <CRLF>.<CRLF> (un punto en una línea sola).
    • Diferencia Envelope vs. Header:
        – SMTP procesa el sobre (comandos MAIL FROM / RCPT TO).
        – SMTP no analiza el contenido del mensaje (Cabeceras From: o To: del RFC 5322). Esto
          explica por qué el remitente técnico puede ser diferente al que ve el usuario.
    • Códigos de error:
        – Distinguir entre un error 4xx (reintentar, soft bounce) y un error 5xx (fallo fatal, hard
          bounce).
    • RFC de referencia:
        – La norma actual que define el protocolo es la RFC 5321 (sustituye a la 2821 y 821).

1.2.2. POP3 (Post Office Protocol v3)

El Post Office Protocol versión 3 (POP3) es un protocolo estándar de la capa de aplicación, definido
en la RFC 1939, diseñado para permitir que un cliente de correo (MUA) recupere los mensajes de
correo electrónico situados en un servidor remoto (MDA/Mail Store) a través de una conexión
TCP/IP.
A diferencia de SMTP, que se utiliza para la transmisión y entrega de correo entre servidores
(“push”), POP3 es un protocolo de tipo “pull” o descarga, diseñado originalmente para usuarios
con conexiones intermitentes a Internet.

1.2.2.1. Características Técnicas y Funcionamiento

POP3 se basa en un modelo de diseño simple orientado a la desconexión: conecta, descarga los
mensajes y desconecta. Su funcionamiento implica que, en su configuración estándar, el correo
se mueve del servidor al equipo local del usuario.
Parámetros de Conexión:

Configuración                     Puerto Estándar                   Descripción

POP3 (No cifrado/STARTTLS)        110 TCP                           Puerto predeterminado para
                                                                    conexiones en texto claro.
                                                                    Puede escalar a cifrado con
                                                                    STLS (RFC 2595).




Bloque IV - Punto 3                          15 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Configuración                    Puerto Estándar                    Descripción

POP3S (SSL Implícito)            995 TCP                            Conexión cifrada desde el
                                                                    inicio mediante SSL/TLS. Es la
                                                                    configuración recomendada
                                                                    por seguridad.


Modos de Operación:
  1. Modo de Eliminación (Delete Mode): Es el comportamiento original y predeterminado. El
     cliente recupera los mensajes y luego instruye al servidor para que los borre.
        • Consecuencia: El correo solo reside en el equipo local. Si el usuario accede desde otro
          dispositivo, no verá los mensajes descargados previamente.
  2. Modo de Conservación (Keep Mode): El cliente descarga los mensajes pero no emite la orden
     de borrado (o utiliza el comando UIDL para sincronizar qué mensajes ya ha descargado).
        • Consecuencia: Permite cierta movilidad, pero carece de sincronización de estado (si se
          lee un correo en el móvil, sigue apareciendo como “no leído” en el PC).

1.2.2.2. Estados de una Sesión POP3

El ciclo de vida de una conexión POP3 es estrictamente secuencial y se divide en tres estados o
fases lógicas definidas en el estándar:
  1. Estado de Autorización (Authorization State):
        • El cliente establece la conexión TCP (puerto 110) y el servidor envía un saludo (+OK).
        • El cliente debe identificarse (comandos USER y PASS). Hasta que no se autentica
          correctamente, no puede acceder a los mensajes.
  2. Estado de Transacción (Transaction State):
        • Una vez autenticado, el cliente puede solicitar información y descargar mensajes.
        • En esta fase, los mensajes no se borran realmente; se “marcan para eliminación”. Si la
          conexión se cae antes de llegar al estado de actualización, los mensajes marcados no se
          eliminan.
  3. Estado de Actualización (Update State):
        • Se inicia cuando el cliente envía el comando QUIT.
        • El servidor elimina físicamente todos los mensajes marcados para borrado durante la
          fase de transacción y cierra la conexión TCP.

1.2.2.3. Comandos POP3 Principales

La comunicación se realiza mediante comandos ASCII simples enviados por el cliente y respuestas
del servidor que comienzan con +OK (éxito) o -ERR (fallo).
Comandos de Autorización:
    • USER [nombre]: Identifica al usuario.
    • PASS [clave]: Envía la contraseña (en texto claro, salvo que se use SSL/TLS).
Comandos de Transacción:
    • STAT: Devuelve el número total de mensajes y el tamaño total en bytes del buzón (drop
      listing).


Bloque IV - Punto 3                          16 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • LIST [msg]: Lista los mensajes disponibles con sus tamaños. Si se añade un número, muestra
      info de ese mensaje específico.
    • RETR [msg]: Retrieves. Descarga el contenido completo del mensaje especificado por su
      número.
    • DELE [msg]: Marca el mensaje especificado para ser eliminado al final de la sesión.
    • TOP [msg] [n]: Descarga las cabeceras del mensaje más las n primeras líneas del cuerpo. Útil
      para previsualizar sin descargar adjuntos grandes.
    • UIDL: Obtiene el identificador único del mensaje. Esencial para que el cliente sepa qué
      mensajes ya ha descargado en sesiones anteriores (“Dejar copia en el servidor”).
Comandos de Finalización:
    • RSET: Desmarca todos los mensajes marcados para eliminación (revierte los DELE).
    • QUIT: Termina la sesión y ejecuta la eliminación física de mensajes marcados.

1.2.2.4. Probables focos de examen

En las pruebas selectivas para TAI, es imprescindible dominar los siguientes puntos sobre POP3:
  1. Puertos de Escucha:
        • Identificar el puerto 110 para POP3 estándar y 995 para POP3 sobre SSL (POP3S). Es una
          pregunta directa muy frecuente.
  2. Gestión de Carpetas:
        • POP3 no soporta carpetas en el servidor. Solo gestiona un único buzón (INBOX).
          Cualquier organización en carpetas que vea el usuario se realiza localmente en su cliente
          (Outlook, Thunderbird).
        • Pregunta tipo: “¿Qué protocolo permite gestionar carpetas en el servidor?” (Respuesta:
          IMAP, no POP3).
  3. Fases del Protocolo:
        • Recordar los tres estados: Autorización, Transacción y Actualización.
        • Saber que el borrado real ocurre en la fase de Actualización (al hacer QUIT).
  4. Diferencia funcional con IMAP:
        • POP3 está orientado a la descarga y desconexión (offline access).
        • No sincroniza el estado (leído/no leído) entre dispositivos.
        • Es más ligero en recursos del servidor que IMAP, ya que delega el almacenamiento en el
          cliente.
  5. Comandos específicos:
        • Relacionar RETR con la descarga del mensaje y DELE con su borrado.
        • STAT para ver el estado del buzón (cantidad de mensajes).

1.2.3. IMAP (Internet Message Access Protocol)

El protocolo IMAP (Internet Message Access Protocol), cuya versión actual (IMAP4rev1) está
estandarizada en la RFC 3501, es un protocolo de la capa de aplicación diseñado para permitir
a los clientes de correo (MUA) acceder y manipular mensajes electrónicos almacenados en un
servidor remoto.
A diferencia de POP3, que está orientado a la descarga y desconexión, IMAP está diseñado para
mantener los mensajes en el servidor, permitiendo a los usuarios organizar, buscar y gestionar su
correo desde múltiples dispositivos de forma sincronizada.




Bloque IV - Punto 3                          17 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.2.3.1. Características Técnicas y Funcionamiento

El funcionamiento de IMAP se basa en un modelo cliente-servidor persistente sobre TCP. Su
arquitectura permite que el MUA actúe como una interfaz o “ventana” directa al almacén de
mensajes (Message Store) del servidor.
Parámetros de Conexión:

Configuración                    Puerto Estándar                    Descripción

IMAP (No cifrado/STARTTLS)       143 TCP                            Puerto predeterminado.
                                                                    Puede escalar a cifrado
                                                                    mediante el comando
                                                                    STARTTLS.

IMAPS (SSL Implícito)            993 TCP                            Conexión cifrada desde el
                                                                    inicio (SSL/TLS). Es el estándar
                                                                    recomendado actualmente.


Funcionalidades Clave:
  1. Acceso Remoto y Sincronización: Los mensajes permanecen en el servidor hasta que el
     usuario los elimina explícitamente. Esto permite el acceso simultáneo desde múltiples
     clientes (ej. móvil, portátil, webmail).
  2. Gestión de Estado (Flags): IMAP utiliza “banderas” (flags) almacenadas en el servidor
     para rastrear el estado de cada mensaje. Si un usuario marca un correo como leído en un
     dispositivo, el cambio se refleja en todos los demás.
        • Flags del sistema comunes: \Seen (leído), \Answered (contestado), \Flagged
          (marcado/urgente), \Deleted (marcado para borrar), \Draft (borrador), \Recent.
  3. Estructura de Carpetas: Permite crear, renombrar y borrar buzones (carpetas) jerárquicos
     directamente en el servidor.
  4. Descarga Selectiva (On-demand): El cliente puede solicitar solo las cabeceras del mensaje o
     partes específicas de la estructura MIME (por ejemplo, descargar el texto pero no los adjuntos
     pesados) para optimizar el ancho de banda.
  5. Búsqueda en el Servidor: Permite ejecutar consultas complejas de búsqueda en el servidor
     sin necesidad de descargar los correos al cliente.

1.2.3.2. Comandos y Estados del Protocolo

El protocolo IMAP es más complejo que POP3 y maneja una sesión con estados definidos. Los
comandos son etiquetas alfanuméricas generadas por el cliente (ej. a001, a002).
Ciclo de vida de una sesión IMAP:
   +----------------+
   |     CLIENTE    |                                     +----------------+
   |      (MUA)     |                                     |    SERVIDOR    |
   +----------------+                                     | (Dovecot/Cyrus)|
           |                                              +----------------+
           | (1) Conexión TCP (Puerto 143/993)                    |
           |----------------------------------------------------->|
           |<-----------------------------------------------------|
           |          * OK IMAP4rev1 Service Ready                |


Bloque IV - Punto 3                          18 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


              |                                                      |
              | (2) Autenticación                                    |
              | a001 LOGIN usuario contraseña                        |
              |----------------------------------------------------->|
              |<-----------------------------------------------------|
              |          a001 OK LOGIN completed                     |
              |                                                      |
              | (3) Selección de Buzón                               |
              | a002 SELECT INBOX                                    |
              |----------------------------------------------------->|
              |<-----------------------------------------------------|
              |          * 172 EXISTS                                |
              |          * 1 RECENT                                  |
              |          a002 OK [READ-WRITE] SELECT completed       |
              |                                                      |
              | (4) Operaciones (Listar, Leer, Buscar)               |
              | a003 FETCH 172 (FLAGS BODY[HEADER.FIELDS (DATE)])    |
              |----------------------------------------------------->|
              |<-----------------------------------------------------|
              |          * 172 FETCH (...)                           |
              |          a003 OK FETCH completed                     |
              |                                                      |
              | (5) Cierre                                           |
              | a004 LOGOUT                                          |
              |----------------------------------------------------->|
              |<-----------------------------------------------------|
              |          * BYE IMAP4rev1 Server logging out          |
              |          a004 OK LOGOUT completed                    |

Comandos IMAP Principales:
    • LOGIN / AUTHENTICATE: Identificación del usuario ante el servidor.
    • LIST: Muestra las carpetas (buzones) disponibles en el servidor.
    • SELECT: Selecciona una carpeta específica para realizar operaciones sobre ella (ej. INBOX).
    • FETCH: Recupera datos de un mensaje (cabeceras, cuerpo, estructura MIME o partes
      específicas).
    • SEARCH: Busca mensajes que cumplan ciertos criterios (fecha, remitente, texto, etc.).
    • STORE: Modifica los atributos de un mensaje (ej. añadir el flag \Seen o \Deleted).
    • EXPUNGE: Elimina físicamente los mensajes que tienen el flag \Deleted.
    • IDLE: Extensión (RFC 2177) que permite al cliente esperar notificaciones de nuevos correos
      en tiempo real sin hacer polling constante.
    • NOOP: Comando “No Operation”, usado para mantener la sesión viva y recibir actualizaciones
      de estado.

1.2.3.3. Probables focos de examen

En las oposiciones a TAI, el protocolo IMAP suele ser objeto de preguntas comparativas y técnicas.
  1. Puertos de Servicio:
       • Pregunta recurrente: Identificar el puerto 143 para IMAP y 993 para IMAPS (IMAP sobre
         SSL).
       • Trampa: Confundirlo con los puertos de POP3 (110/995) o SMTP (25/587).
  2. Ubicación del Mensaje (Diferencia Fundamental):
       • Es vital recordar que en IMAP los mensajes residen en el servidor. El examen suele
         plantear escenarios de “usuarios móviles” o “acceso desde varios ordenadores” donde


Bloque IV - Punto 3                           19 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


         la respuesta correcta es el uso de IMAP.
  3. RFC de Referencia:
       • La norma que define la versión actual (IMAP4rev1) es la RFC 3501. Aunque existen
         extensiones, esta es la referencia base.
  4. Gestión de Recursos:
       • IMAP consume más recursos (CPU, memoria y almacenamiento) en el servidor que
         POP3, ya que el servidor debe realizar el procesamiento de búsquedas, mantener el
         estado de las sesiones y almacenar todo el correo.
  5. Capacidades de Búsqueda:
       • Saber que IMAP permite realizar búsquedas en el lado del servidor (server-side searching),
         lo cual evita tener que descargar todo el correo para encontrar un mensaje específico.

1.2.4. Diferencias entre POP3 e IMAP

La elección entre POP3 (Post Office Protocol version 3) e IMAP (Internet Message Access Protocol)
determina la arquitectura de almacenamiento del correo, la experiencia del usuario y los
requisitos de recursos del servidor. Mientras que POP3 fue diseñado bajo la premisa de que
el almacenamiento en el servidor era costoso y transitorio, IMAP se diseñó asumiendo que el
servidor es el repositorio principal y permanente de la información.
A continuación, se detallan las diferencias estructurales y funcionales clave, esenciales para el
examen de TAI.

1.2.4.1. Modelo de Acceso y Ubicación del Mensaje

La diferencia fundamental radica en dónde residen los mensajes y cómo se manipulan:
    • POP3 (Modelo de descarga y desconexión): Su filosofía es “almacenamiento y reenvío”
      hasta el cliente final. El MUA se conecta, descarga todos los mensajes nuevos al dispositivo
      local y, por defecto, los elimina del servidor. Aunque la mayoría de clientes permiten la
      configuración “dejar copia en el servidor” (Keep Mode), el protocolo no está optimizado para
      ello y carece de mecanismos para gestionar el estado de esos mensajes (leído/no leído) entre
      diferentes sesiones o dispositivos.
    • IMAP (Modelo de acceso remoto y sincronización): Considera al servidor como el almacén
      principal (Message Store). El MUA actúa como una ventana o interfaz para visualizar y
      manipular los correos que residen físicamente en el servidor. Los mensajes no se descargan
      completamente por defecto; se recuperan primero las cabeceras y el cuerpo se descarga bajo
      demanda.
Tabla comparativa de arquitectura:


Característica                   POP3                               IMAP

Ubicación principal              Dispositivo del usuario (Local)    Servidor de correo (Remoto)
Acceso multidispositivo          Limitado/Problemático. No          Nativo. Los cambios se reflejan
                                 hay sincronización de estado       en todos los dispositivos
                                 entre dispositivos,                simultáneamente,




Bloque IV - Punto 3                          20 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Característica                   POP3                               IMAP

Gestión de carpetas              Solo local. El servidor solo       Soporte completo en servidor.
                                 tiene un buzón (INBOX). No         Permite crear, borrar y
                                 permite carpetas remotas,          renombrar carpetas remotas,
Conectividad                     Orientado a la desconexión         Orientado a la conexión
                                 (Offline). Conecta, descarga y     (Online). Mantiene sesiones
                                 cierra                             largas y sincronización en
                                                                    tiempo real (IDLE),


1.2.4.2. Funcionalidades y Gestión de Estado

El protocolo IMAP incluye funcionalidades avanzadas de las que POP3 carece, definidas en sus
respectivos RFCs (RFC 1939 para POP3 y RFC 3501 para IMAP).
  1. Banderas de Estado (Flags):
       • IMAP: Almacena el estado del mensaje en el servidor mediante flags (\Seen, \Answered,
         \Deleted). Si un usuario lee un correo en el móvil, aparece como leído en el PC de
         escritorio.
       • POP3: No tiene concepto de estado en el servidor. El estado de “leído” es una propiedad
         puramente local del cliente de correo.
  2. Búsqueda (Searching):
       • IMAP: Permite realizar búsquedas complejas en el lado del servidor (server-side search)
         sin descargar los mensajes (ej. buscar en el cuerpo de correos antiguos).
       • POP3: No soporta búsquedas en el servidor; el cliente debe descargar todo el correo y
         buscar localmente.
  3. Descarga Selectiva (MIME):
       • IMAP: Permite descargar partes específicas de un mensaje MIME. Por ejemplo, un usuario
         puede descargar solo el texto de un correo sin bajar un adjunto pesado de 20 MB hasta
         que lo solicite explícitamente.
       • POP3: Generalmente requiere la descarga del mensaje completo (cabeceras y cuerpo)
         para poder procesarlo.

1.2.4.3. Consumo de Recursos y Rendimiento

Desde la perspectiva del administrador de sistemas (rol del TAI), la elección del protocolo impacta
en la infraestructura:
    • Almacenamiento (Storage):
        – POP3: Minimiza el uso de disco en el servidor, ya que los correos se mueven al cliente.
          Ideal para servidores con cuotas limitadas.
        – IMAP: Exige gran capacidad de almacenamiento en el servidor, ya que todo el historial
          de correos de todos los usuarios reside allí.
    • Carga de CPU y Memoria:
        – POP3: Protocolo ligero. Consume pocos recursos de CPU ya que su operativa es lineal y
          simple.
        – IMAP: Consume más CPU y memoria RAM en el servidor. El servidor debe indexar
          correos, gestionar estados, realizar búsquedas y mantener múltiples conexiones TCP
          abiertas (IDLE). Estudios de rendimiento con OPNET muestran que IMAP presenta un


Bloque IV - Punto 3                          21 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


          retardo TCP promedio mayor debido a la complejidad de la sincronización.
    • Copias de Seguridad (Backup):
        – POP3: Si el usuario pierde su PC o se daña su disco duro, pierde sus correos (a menos
          que el usuario haga sus propios backups). Es difícil de respaldar centralizadamente.
        – IMAP: Facilita el backup centralizado. El administrador puede respaldar el Message Store
          completo, garantizando la seguridad de los datos corporativos.

1.2.4.4. Probables focos de examen

En las oposiciones, las preguntas sobre diferencias suelen centrarse en escenarios de uso y
limitaciones técnicas.
  1. Escenario de Movilidad:
        • Ante un supuesto práctico donde un usuario necesita acceder al correo desde el PC de
          la oficina, un portátil y un móvil, la respuesta correcta siempre será IMAP. POP3 es la
          respuesta incorrecta por la falta de sincronización de carpetas y estados.
  2. Gestión de Carpetas:
        • Es frecuente preguntar qué protocolo permite gestionar carpetas en el servidor.
        • IMAP: Sí permite carpetas (buzones) jerárquicos en el servidor.
        • POP3: No, solo gestiona la bandeja de entrada (INBOX); las carpetas son locales del
          cliente.
  3. Privacidad y “Keep Mode”:
        • Aunque POP3 borra por defecto, existe el “Keep Mode” (dejar copia). Sin embargo, el
          examen puede preguntar qué protocolo es mejor para la privacidad si el servidor no
          es de confianza: POP3 (en modo borrado) minimiza la huella de datos en el servidor
          remoto.
  4. Protocolos y Puertos (Distinción):
        • El aspirante debe asociar correctamente los pares de puertos seguros e inseguros para
          diferenciar los servicios en un firewall:
            – IMAP: 143 / 993 (SSL/TLS).
            – POP3: 110 / 995 (SSL/TLS).
  5. Recuperación ante desastres:
        • Si se pregunta qué protocolo garantiza mejor la recuperación de datos ante un fallo
          del equipo del usuario (endpoint), la respuesta es IMAP, debido al almacenamiento
          centralizado.

1.3. Instalación y configuración de servidores de correo
Esta sección aborda la implementación práctica del software encargado de materializar las
funciones de transporte y acceso estudiadas anteriormente. La elección y el despliegue de estas
herramientas definen la robustez, la escalabilidad y la facilidad de administración del sistema de
correo de una organización.
La administración de estos servicios suele requerir una combinación de dos tipos de software: por
un lado, el Agente de Transferencia de Correo (MTA), que se encarga del intercambio de mensajes
mediante SMTP; y por otro, el servidor de acceso, que permite a los usuarios interactuar con
sus buzones. Dependiendo del sistema operativo y las necesidades del negocio, el administrador
puede optar por soluciones modulares de código abierto (típicas en entornos Unix/Linux) o
soluciones integrales propietarias que combinan correo, calendario y gestión de contactos.
A continuación, se presenta una tabla comparativa de las soluciones que se detallarán en este
apartado para entender su posicionamiento en el mercado:

Bloque IV - Punto 3                          22 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios



                                                                             Filosofía /
Software                 Rol Principal            Plataforma                 Características

Postfix                  MTA                      Linux / Unix               Modular, seguro y
                                                                             fácil de configurar;
                                                                             sucesor moderno de
                                                                             Sendmail.
Sendmail                 MTA                      Linux / Unix               Clásico y complejo;
                                                                             altamente flexible
                                                                             mediante macros M4.
MS Exchange              Integral            Windows Server                  Solución corporativa
                         (MTA+MDA+Groupware)                                 con integración
                                                                             profunda en Active
                                                                             Directory.
Dovecot                  Servidor POP3/IMAP       Linux / Unix               Excelente
                                                                             rendimiento en la
                                                                             entrega y gestión de
                                                                             buzones (MDA).


La correcta instalación no solo implica el despliegue del binario, sino la configuración de los
archivos de sistema, la gestión de los permisos sobre los directorios de los buzones (Maildir o
Mbox) y la integración con las bases de datos de usuarios. Un servidor mal configurado puede
convertirse rápidamente en una fuente de problemas de seguridad o en un relevo abierto (open
relay) para el envío de spam, por lo que el proceso de configuración inicial es crítico.

1.3.1. Postfix

Postfix es un Agente de Transferencia de Correo (MTA) de código abierto, diseñado originalmente
como una alternativa segura y eficiente a Sendmail. Actualmente es el MTA predeterminado en
muchas distribuciones de Linux, como Red Hat Enterprise Linux (RHEL) y Ubuntu, destacando
por su arquitectura modular, facilidad de administración y rendimiento bajo alta carga.

1.3.1.1. Arquitectura y Diseño

A diferencia de los diseños monolíticos, Postfix utiliza una arquitectura modular basada en
múltiples procesos pequeños y especializados que se ejecutan en segundo plano.
    • Demonio Maestro (master): Es el proceso residente que controla el sistema de correo.
      Supervisa y lanza otros procesos bajo demanda, definidos en el archivo master.cf.
    • Procesos de Manejo: Incluyen smtpd (recibe correo entrante), qmgr (gestiona la cola), cleanup
      (procesa cabeceras y direcciones), pickup (recoge correo local) y agentes de entrega como
      local, virtual o pipe.
    • Seguridad: Postfix se ejecuta con el menor privilegio posible. La mayoría de los procesos
      corren bajo un usuario no privilegiado (típicamente postfix), y muchos se ejecutan dentro
      de un entorno chroot para limitar el daño en caso de compromiso.




Bloque IV - Punto 3                          23 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.3.1.2. Archivos de Configuración

La configuración de Postfix reside habitualmente en el directorio /etc/postfix/. Los dos archivos
principales son:
  1. main.cf: Contiene la configuración global del servidor. Define parámetros como el nombre
     del host, dominios aceptados, rutas de red y políticas de seguridad.
  2. master.cf: Especifica cómo interactúan los procesos de Postfix, los servicios que se ejecutan
     (como smtp, submission), sus límites y argumentos de línea de comandos.
Existen otros archivos auxiliares para tablas de búsqueda (Lookups), como access (control de
acceso), transport (mapas de transporte), virtual (dominios y usuarios virtuales) y aliases (alias
de sistema).

1.3.1.3. Parámetros Críticos en main.cf

Para la administración y el examen, es esencial dominar los siguientes parámetros de
configuración:


Parámetro                        Función                            Ejemplo Típico

myhostname                       Define el nombre de dominio        smtp.example.com
                                 completamente cualificado
                                 (FQDN) del servidor.
myorigin                         Dominio que se añade a los         $mydomain
                                 correos enviados localmente
                                 que carecen de dominio.
inet_interfaces                  Interfaces de red donde Postfix    all o loopback-only
                                 escucha peticiones. Para
                                 seguridad, por defecto suele
                                 ser solo loopback.
mydestination                    Lista de dominios para los      $myhostname,
                                 cuales el servidor acepta       localhost.$mydomain
                                 entrega local final. Si se deja
                                 vacío, actúa como “null client”
                                 (solo reenvío).
relayhost                        Servidor al que se reenvían        [smtp.proveedor.com]
                                 todos los correos salientes
                                 (Smart Host).
mynetworks                       Lista de redes de confianza        127.0.0.0/8,
                                 (IPs) autorizadas a enviar         192.168.1.0/24
                                 correo a través del servidor
                                 (relay) sin autenticación.




Bloque IV - Punto 3                          24 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios



home_mailbox                      Define el formato y ubicación     Maildir/
                                  del buzón de usuario. Para
                                  usar el formato Maildir, es
                                  obligatorio terminar la ruta
                                  con una barra /.


1.3.1.4. Gestión de Tablas y Bases de Datos

Postfix utiliza tablas de búsqueda para alias, control de acceso y enrutamiento. Estas tablas suelen
ser archivos de texto que deben compilarse a un formato binario indexado (como Berkeley DB)
para su uso eficiente.
    • Comando postmap: Se utiliza para crear o actualizar la base de datos binaria (.db) a partir de
      un archivo de texto plano.
         – Sintaxis: postmap /etc/postfix/virtual (genera /etc/postfix/virtual.db).
    • Comando newaliases: Específico para actualizar la base de datos de alias (/etc/aliases). Es
      un enlace de compatibilidad con Sendmail que ejecuta internamente las rutinas de Postfix.
    • LDAP/SQL: Postfix puede configurarse para realizar búsquedas directas en directorios LDAP
      o bases de datos SQL en lugar de usar archivos locales, centralizando la gestión de usuarios.

1.3.1.5. Herramientas de Administración

El administrador interactúa con Postfix mediante comandos específicos:
    • postfix: Herramienta de control principal.
        – postfix check: Verifica la sintaxis de la configuración y permisos de archivos.
        – postfix reload: Recarga la configuración sin detener el servicio.
    • postconf: Permite visualizar y modificar la configuración actual.
        – postconf -n: Muestra los parámetros modificados respecto a los valores por defecto.
        – postconf -e 'parametro = valor': Edita el archivo main.cf directamente desde la
          línea de comandos.
    • mailq: Muestra el contenido de la cola de correo.

1.3.1.6. Seguridad: SMTP-AUTH y TLS

Para asegurar el servicio, Postfix implementa mecanismos modernos:
  1. SMTP-AUTH (SASL): Permite autenticar a los usuarios antes de aceptar correo para reenvío
     (Relay). Postfix soporta implementaciones SASL como Cyrus SASL y Dovecot SASL.
        • Se configura en main.cf mediante smtpd_sasl_auth_enable = yes y smtpd_sasl_type
          = dovecot.
  2. TLS (Transport Layer Security): Cifra la comunicación SMTP. Se pueden configurar
     certificados para el servidor (smtpd_tls_cert_file) y forzar el uso de TLS para autenticación
     (smtpd_tls_auth_only = yes).

1.3.1.7. Probables focos de examen

  1. Formato Maildir:
       • Es crucial recordar que para configurar el formato Maildir en el parámetro home_mailbox,
         el valor debe terminar en barra (/), p. ej., Maildir/. Si no la tiene, Postfix asumirá
         formato mbox.

Bloque IV - Punto 3                          25 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


  2. Archivos de configuración:
       • Diferenciar entre main.cf (parámetros globales) y master.cf (definición de
         procesos/servicios daemon).
  3. Restricción de Relay:
       • El parámetro mynetworks es la primera línea de defensa para evitar ser un Open Relay.
         Define qué clientes IP pueden enviar correo a través del servidor sin autenticarse.
  4. Comando de actualización de mapas:
       • Saber que tras editar un archivo de tabla (como virtual o access), se debe ejecutar
         postmap; sin embargo, tras editar /etc/aliases, se usa newaliases.
  5. Postfix como Null Client:
       • Configuración donde mydestination está vacío y relayhost está definido, indicando que
         el servidor no entrega correo localmente, sino que reenvía todo a un servidor central.

1.3.2. Sendmail

Sendmail es un Agente de Transferencia de Correo (MTA) de propósito general que, históricamente,
ha sido el estándar de facto en sistemas UNIX para el enrutamiento de correo electrónico. Aunque
ha sido desplazado en muchas implementaciones modernas por Postfix debido a su complejidad,
sigue siendo vital en el temario de oposiciones por su arquitectura base y los estándares que
definió.
Su función principal es actuar como un conmutador (“crossbar switch”), retransmitiendo
mensajes de un dominio a otro y realizando la edición de cabeceras necesaria para cumplir con
los estándares (RFC 821, RFC 5322, entre otros).

1.3.2.1. Arquitectura de Configuración: M4 y sendmail.cf

La característica más distintiva y examinable de Sendmail es su sistema de configuración. El
archivo de configuración principal, leído por el demonio al arrancar, es sendmail.cf. Sin embargo,
la sintaxis de este archivo es extremadamente compleja y difícil de editar para un humano.
Para solucionar esto, se utiliza un sistema de macros basado en el procesador M4.
  1. Archivos .mc (Master Configuration): El administrador edita archivos con extensión .mc
     (por ejemplo, sendmail.mc), que contienen macros de alto nivel legibles.
  2. Procesamiento M4: Se utiliza el comando m4 para compilar el archivo .mc y generar el archivo
     .cf final.
        • Comando típico: m4 /etc/mail/m4/cf.m4 config.mc > sendmail.cf.
Estructura del archivo .mc: El archivo .mc se compone de varias directivas clave:
    • OSTYPE: Define el sistema operativo para ajustar rutas de archivos y banderas (flags)
      automáticamente. Debe ir al principio.
    • DOMAIN: Carga configuraciones específicas para el dominio de la organización.
    • FEATURE: Activa funcionalidades específicas (ej. FEATURE(access_db) para control de spam).
    • MAILER: Define los agentes de entrega a utilizar (ej. MAILER(smtp), MAILER(local)).

1.3.2.2. Archivos y Directorios Críticos

Para el examen, es fundamental memorizar la ubicación y función de los siguientes ficheros, que
suelen residir en /etc/mail/:




Bloque IV - Punto 3                         26 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Archivo / Directorio             Función                            Notas para el examen

/etc/mail/sendmail.cf            Configuración principal del        No se edita directamente; se
                                 MTA.                               genera desde el .mc.
/etc/mail/submit.cf              Configuración para el MSP          Usado para la entrega inicial
                                 (Mail Submission Program).         de correo local (no root).
/etc/mail/aliases                Define alias de correo y listas    Requiere ejecutar newaliases
                                 de distribución locales.           tras su edición.
/etc/mail/access                 Base de datos de control de        Permite aceptar/rechazar
                                 acceso (retransmisión,             correo por IP o dominio.
                                 rechazo).
/etc/mail/local-host-names       Lista de dominios para los que     Anteriormente conocido
                                 el servidor acepta correo final.   como sendmail.cw.
/var/spool/mqueue                Directorio de cola de correo       Donde se almacenan los
                                 (Queue).                           mensajes en tránsito.


1.3.2.3. Bases de Datos y Comandos de Mantenimiento

Sendmail utiliza bases de datos indexadas (mapas) para mejorar el rendimiento en la lectura de
alias y reglas de acceso.
  1. Gestión de Alias (/etc/mail/aliases): Permite redirigir correo de un usuario a otro o a un
     programa.
        • Formato: nombre: destino1, destino2.
        • Comando newaliases: Es obligatorio ejecutar este comando (o sendmail -bi) cada vez
          que se modifica el archivo de texto /etc/mail/aliases para regenerar la base de datos
          binaria (aliases.db).
  2. Mapas de Acceso (makemap): Para archivos como access, virtusertable o domaintable, se
     debe convertir el archivo de texto a formato de base de datos (generalmente hash o dbm)
     usando el comando makemap.
        • Sintaxis típica: makemap hash /etc/mail/access < /etc/mail/access.
  3. Gestión de la Cola (mailq):
        • El comando mailq (o sendmail -bp) imprime el contenido actual de la cola de correo,
          mostrando IDs, remitentes y destinatarios de mensajes pendientes.
        • Para forzar el procesado de la cola inmediatamente, se usa sendmail -q.

1.3.2.4. Seguridad y smrsh

Sendmail históricamente se ejecutaba como setuid root, lo que presentaba riesgos de seguridad.
Las versiones modernas (V8.12+) utilizan un modelo de separación de privilegios con un usuario
smmsp para la sumisión de correo.

    • SMRSH (SendMail Restricted SHell): Es una herramienta crítica de seguridad que restringe
      qué programas pueden ser ejecutados por sendmail (a través de archivos .forward o alias que
      invoquen tuberías |). Sendmail solo ejecutará programas que estén enlazados en el directorio
      de smrsh (usualmente /usr/adm/sm.bin o /etc/smrsh), evitando la ejecución arbitraria de
      comandos en el servidor.


Bloque IV - Punto 3                          27 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.3.2.5. Probables focos de examen

  1. Diferencia .cf vs .mc:
        • Pregunta recurrente: “¿Qué archivo debe editar el administrador para configurar
          Sendmail?”.
        • Respuesta: El archivo .mc, que luego se procesa con m4 para crear el sendmail.cf. Editar
          el .cf directamente se considera mala práctica.
  2. Comando newaliases:
        • Es imprescindible saber que tras modificar /etc/aliases, los cambios no surten efecto
          hasta ejecutar newaliases (o sendmail -bi).
  3. Uso de makemap:
        • Identificar makemap como la herramienta para generar las bases de datos binarias (mapas)
          a partir de archivos de texto plano como access o virtusertable.
  4. Función de smrsh:
        • Relacionar smrsh con la restricción de ejecución de programas externos por parte del
          servidor de correo.
  5. Control de Relay (Retransmisión):
        • Saber que, por defecto, las versiones modernas de Sendmail deniegan el relay
          (retransmisión de correo desde terceros hacia terceros) para evitar el spam, a menos
          que se configure explícitamente en el archivo access.

1.3.3. Microsoft Exchange Server

Microsoft Exchange Server es una plataforma de mensajería y colaboración empresarial
propietaria que va más allá de un simple servidor de correo (MTA). Proporciona servicios
integrados de correo electrónico, calendario, contactos, tareas y gestión de recursos. A diferencia
de soluciones modulares en entornos Unix (como Postfix + Dovecot), Exchange es una solución
integral diseñada para entornos Windows Server, caracterizada por su estrecha integración con
Active Directory (AD).

1.3.3.1. Arquitectura y Roles del Servidor

La arquitectura de Exchange ha evolucionado hacia la consolidación de roles para simplificar
el despliegue y la gestión. En las versiones modernas (específicamente Exchange 2019), la
arquitectura se define principalmente por dos roles de servidor:
  1. Rol de Buzón (Mailbox Role):
       • Es el rol principal en la red interna (LAN). Consolida las funciones que en versiones
          antiguas (2007/2010) estaban separadas en Client Access Server (CAS) y Hub Transport.
       • Gestiona las bases de datos de correo, procesa las solicitudes de los clientes (Outlook,
          OWA, ActiveSync) y enruta el correo.
       • Aloja los servicios de frontend (acceso de cliente) y backend (procesamiento de datos) en
          el mismo servidor.
  2. Rol de Transporte Perimetral (Edge Transport Role):
       • Se sitúa en la red perimetral (DMZ), fuera del dominio de Active Directory.
       • Su función es minimizar la superficie de ataque, actuando como pasarela SMTP para
          el correo entrante y saliente de Internet. Proporciona filtrado de spam y reglas de
          transporte antes de que el tráfico toque la red interna.
       • No es obligatorio, pero sí recomendado para seguridad perimetral.
      Nota Técnica: En Exchange 2019, funciones como el acceso de cliente (protocolos


Bloque IV - Punto 3                          28 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      HTTP, POP3, IMAP) son servicios que se ejecutan dentro del Rol de Buzón, no roles de
      servidor independientes.

1.3.3.2. Estructura de Almacenamiento y Base de Datos

Exchange utiliza el motor de base de datos ESE (Extensible Storage Engine), también conocido como
JET Blue. El almacenamiento se basa en una estructura transaccional crítica para la integridad de
los datos.
    • Archivos de Base de Datos (.edb): Contienen la información real de los buzones (mensajes,
      adjuntos, carpetas). Exchange 2019 optimiza el diseño para soportar discos de gran
      capacidad y menor velocidad, reduciendo los requisitos de IOPS (operaciones de
      entrada/salida).
    • Archivos de Registro de Transacciones (Transaction Logs): Registran todos los cambios
      realizados en la base de datos antes de que se confirmen en el archivo .edb. Son fundamentales
      para la recuperación ante desastres y la consistencia de la base de datos.
        – Truncamiento de logs: Los logs se eliminan o truncan solo tras una copia de seguridad
           completa o incremental exitosa, para evitar llenar el disco.
    • Meta Cache Database (MCDB): Introducida en Exchange 2019, permite usar discos SSD para
      cachear metadatos y acelerar el acceso, mientras los datos fríos residen en discos mecánicos
      más económicos.

1.3.3.3. Alta Disponibilidad: DAG (Database Availability Group)

El DAG es el componente arquitectónico que proporciona alta disponibilidad y recuperación ante
desastres a nivel de base de datos.
    • Funcionamiento: Un DAG es un grupo de hasta 16 servidores de buzones que alojan
      copias de bases de datos. Si un servidor falla, una copia pasiva en otro servidor se activa
      automáticamente.
    • Replicación: Utiliza la tecnología de replicación continua para mantener las copias
      sincronizadas entre servidores locales o en centros de datos remotos (resiliencia de sitio).
    • Active Manager: Es el componente interno que decide qué copia de la base de datos debe
      estar activa y montada.

1.3.3.4. Instalación e Integración con Active Directory

Exchange Server depende absolutamente de Active Directory (AD) para almacenar la
configuración de la organización y los atributos de los usuarios. La instalación requiere
un proceso secuencial de preparación del directorio:
  1. Extensión del Esquema (/PrepareSchema): Modifica el esquema de AD para añadir clases y
     atributos específicos de Exchange (ej. ms-Exch-Schema-Version-Pt). Requiere permisos de
     Schema Admins.
  2. Preparación de AD (/PrepareAD): Crea los contenedores y objetos de configuración en la
     partición de configuración de AD y define el nombre de la Organización Exchange.
  3. Preparación del Dominio (/PrepareDomain): Crea grupos de seguridad y permisos necesarios
     en cada dominio donde se instalen servidores o existan usuarios de correo.
La administración posterior se realiza mediante dos herramientas principales:
    • Exchange Admin Center (EAC): Consola de gestión basada en web.


Bloque IV - Punto 3                          29 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Exchange Management Shell (EMS): Interfaz de línea de comandos basada en PowerShell,
      necesaria para tareas avanzadas y automatización.

1.3.3.5. Probables focos de examen

En las oposiciones a TAI, las preguntas sobre Exchange suelen centrarse en su arquitectura única
y dependencias.
1.3.3.5.1. Dependencia de Active Directory
    • Es fundamental saber que Exchange no puede funcionar sin Active Directory. Guarda su
      configuración en la partición de Configuración de AD y los datos de usuarios en la partición
      de Dominio.
    • Pregunta tipo: “¿Qué servicio es imprescindible para el funcionamiento de Microsoft
      Exchange?” → Active Directory.
1.3.3.5.2. Motor de Base de Datos y Logs
    • Identificar el uso de logs de transacciones. El sistema escribe primero en el log y luego en la
      base de datos (Write-Ahead Logging).
    • Si se borran los logs manualmente sin un backup, la base de datos puede quedar inconsistente
      o corrupta.
    • Extensión de archivo de base de datos: .edb.
1.3.3.5.3. Concepto de DAG
    • Definición: Database Availability Group. Es el mecanismo nativo para Alta Disponibilidad
      en Exchange 2010/2013/2016/2019.
    • Saber que permite la replicación de bases de datos entre servidores distintos.
1.3.3.5.4. Roles de Servidor (Simplificación)
    • En versiones recientes (2016/2019), reconocer que NO existen roles separados de “Client
      Access Server” (CAS) o “Hub Transport” como roles instalables independientes en la LAN;
      están consolidados en el Rol de Buzón (Mailbox). El único rol separado es el Edge Transport.
1.3.3.5.5. Protocolo MAPI
    • Diferenciar que los clientes Outlook nativos utilizan MAPI (sobre HTTP o RPC) para
      comunicarse con Exchange, ofreciendo más funcionalidades (calendario, notas) que los
      protocolos estándar IMAP/POP3.

1.3.4. Dovecot como servidor IMAP/POP3

Dovecot es un servidor de correo electrónico de código abierto diseñado principalmente
como Agente de Acceso a Mensajes (MAA) y Agente de Entrega de Correo (MDA). Su función
principal es permitir que los clientes de correo (MUA) accedan a los buzones almacenados en el
servidor utilizando los protocolos IMAP y POP3. Es ampliamente reconocido en el ámbito de la
administración de sistemas por su enfoque en la seguridad, su alto rendimiento y su capacidad
de “autocuración” (capacidad de corregir índices rotos automáticamente).
En el contexto del examen TAI, es fundamental entender que Dovecot no es un MTA (como Postfix
o Sendmail); no transfiere correo entre servidores a través de Internet (SMTP puerto 25), sino que
gestiona el almacenamiento local y el acceso de los usuarios a dicho correo.




Bloque IV - Punto 3                           30 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


1.3.4.1. Arquitectura y Funcionalidades

Dovecot opera mediante una arquitectura modular que separa los procesos para mejorar la
seguridad. Sus funcionalidades clave incluyen:
  1. Servidor IMAP/POP3: Permite a los usuarios leer y gestionar su correo. Soporta las versiones
     seguras de estos protocolos (IMAPS en puerto 993 y POP3S en puerto 995) mediante TLS.
  2. Servicio de Autenticación (SASL): Dovecot proporciona mecanismos de autenticación no
     solo para sus propios servicios, sino que actúa como backend de autenticación para el MTA
     (Postfix). Esto permite que Postfix utilice la base de datos de usuarios de Dovecot para
     autenticar los envíos SMTP (SMTP-AUTH).
  3. Entrega Local (LMTP): Incluye un servidor LMTP (Local Mail Transfer Protocol) que permite
     recibir correos desde el MTA para depositarlos en los buzones de los usuarios, permitiendo
     aplicar filtros y comprobaciones de cuota en el momento de la entrega.
  4. Soporte de Formatos de Buzón: Dovecot es muy flexible y soporta múltiples formatos de
     almacenamiento, siendo los más relevantes para el examen:
        • mbox: Un solo archivo por carpeta de correo. Tradicional pero con problemas de
          bloqueo.
        • Maildir: Un archivo por cada mensaje. Estándar de facto moderno, ideal para evitar
          bloqueos y facilitar backups incrementales.
        • dbox (sdbox/mdbox): Formatos propios de alto rendimiento de Dovecot.

1.3.4.2. Instalación y Ficheros de Configuración

En distribuciones basadas en Red Hat/CentOS (comunes en el temario), el servicio se gestiona
mediante el paquete dovecot.
    • Fichero Principal: /etc/dovecot/dovecot.conf.
    • Directorio de Configuración Modular: /etc/dovecot/conf.d/. Dovecot incluye ficheros
      específicos para cada área funcional, lo que facilita la administración.
Estructura típica de conf.d/:
    • 10-auth.conf: Configuración de mecanismos de autenticación (PAM, SQL, LDAP).
    • 10-mail.conf: ubicación de los buzones (mail_location).
    • 10-master.conf: Definición de listeners (puertos y sockets).
    • 10-ssl.conf: Certificados y claves privadas para cifrado.

1.3.4.3. Parámetros Críticos de Configuración

Para el desempeño de un TAI, es necesario identificar los parámetros que definen el
comportamiento del servidor.
1. Protocolos Habilitados Se definen en dovecot.conf. Para un servidor estándar seguro:
protocols = imap pop3 lmtp

Nota: Es buena práctica deshabilitar los protocolos no seguros si no se usan.
2. Ubicación del Buzón (mail_location) Define dónde y cómo se guardan los correos. Se configura
en 10-mail.conf.
    • Para formato Maildir en el directorio home del usuario:
      mail_location = maildir:~/Maildir



Bloque IV - Punto 3                            31 de 164                          January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Para formato mbox:
      mail_location = mbox:~/mail:INBOX=/var/mail/%u

      La sintaxis suele usar variables como %u (usuario) o %n (nombre de usuario sin dominio).
3. Autenticación y SASL para Postfix Esta es una de las configuraciones más preguntadas: la
integración Postfix-Dovecot. Se configura en 10-master.conf. Dovecot crea un socket UNIX que
Postfix lee para validar usuarios.
service auth {
  # Socket para que Postfix autentique usuarios (SMTP-AUTH)
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix
  }
}

Adicionalmente, en 10-auth.conf se definen los mecanismos aceptados, típicamente plain y
login.

4. Filtrado con Sieve (Pigeonhole) Dovecot utiliza el plugin Pigeonhole para implementar el
lenguaje de filtrado Sieve. Esto permite ejecutar reglas (mover a carpetas, vacaciones, rechazar)
en el servidor al momento de la entrega (vía LMTP), antes de que el usuario descargue el correo.

1.3.4.4. Probables focos de examen

  1. Diferencia funcional:
        • Distinguir claramente que Dovecot es un servidor IMAP/POP3 (acceso) y MDA (entrega),
          mientras que Postfix es un MTA (transporte SMTP).
  2. Puertos de servicio:
        • IMAP: 143 / IMAPS: 993.
        • POP3: 110 / POP3S: 995.
        • LMTP: 24 (si es por red, aunque suele usarse socket UNIX).
  3. Integración SASL:
        • Pregunta frecuente: “¿Qué servicio proporciona la autenticación para SMTP-AUTH en
          una configuración Postfix+Dovecot?”.
        • Respuesta: Dovecot SASL (a través de un socket UNIX en /var/spool/postfix/private/auth).
  4. Formatos de buzón:
        • Saber que Maildir almacena cada mensaje en un fichero independiente dentro de
          directorios (new, cur, tmp), evitando problemas de bloqueo concurrente, a diferencia de
          mbox que es un fichero monolítico.
  5. Usuarios Virtuales:
        • Dovecot permite gestionar usuarios que no tienen cuenta de sistema (/etc/passwd),
          almacenándolos en bases de datos SQL o LDAP, y asignándoles un único UID/GID físico
          (ej. usuario vmail) para acceder al sistema de ficheros.

1.4. Seguridad en servidores de correo
Esta sección se centra en el blindaje del servicio de correo electrónico, un aspecto crítico
dado que los protocolos originales se diseñaron sin mecanismos de seguridad intrínsecos. La
administración moderna no solo debe garantizar que los mensajes lleguen a su destino, sino



Bloque IV - Punto 3                          32 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


también asegurar la confidencialidad de los datos, la identidad del remitente y la reputación del
dominio corporativo.
La seguridad en el correo electrónico se aborda desde dos vertientes complementarias: la
protección del canal de comunicación, que evita la interceptación de datos mediante técnicas
de cifrado y autenticación de usuarios; y la validación de la identidad del emisor, mediante
registros DNS específicos que combaten el fraude y el phishing. Implementar correctamente
estos mecanismos es la única forma de evitar que nuestro servidor sea utilizado para actividades
ilícitas y asegurar que nuestros correos legítimos no terminen en la carpeta de correo no deseado.
A continuación, se resumen los mecanismos de seguridad que se desarrollarán en este apartado:


Mecanismo                        Objetivo Principal                 Nivel de Acción

SMTP-AUTH / TLS                  Control de acceso y privacidad.    Conexión y sesión
SPF                              Autoriza qué IPs pueden            Validación DNS
                                 enviar correos en nombre de
                                 un dominio.
DKIM                             Garantiza que el contenido del     Firma Digital
                                 mensaje no ha sido alterado.
DMARC                            Indica al receptor qué hacer si    Política de Gestión
                                 SPF o DKIM fallan.


El dominio de estas herramientas permite al administrador construir una infraestructura de
confianza, protegiendo tanto a los usuarios internos como la imagen externa de la organización
frente a amenazas globales.

1.4.1. Autenticación SMTP-AUTH

La autenticación SMTP-AUTH es una extensión del protocolo SMTP original que permite a
un cliente SMTP (MUA o un MTA actuando como cliente) identificarse ante un servidor SMTP.
Esta funcionalidad es crítica en la infraestructura de correo moderna para evitar el Open Relay
(retransmisión abierta), asegurando que solo los usuarios autorizados puedan utilizar el servidor
para enviar correos a dominios externos.
La especificación técnica base se definió originalmente en la RFC 2554 (SMTP Service Extension for
Authentication) y ha sido actualizada por la RFC 4954.

1.4.1.1. Framework SASL (Simple Authentication and Security Layer)

SMTP-AUTH no define los mecanismos de autenticación por sí mismo, sino que utiliza un marco
de trabajo modular denominado SASL (definido en la RFC 4422). SASL desacopla el protocolo de
aplicación (SMTP) del método de autenticación, permitiendo negociar diferentes mecanismos de
seguridad.
Implementaciones comunes de SASL en Linux:
    • Cyrus SASL: Una librería muy extendida utilizada tradicionalmente por Sendmail y
      versiones antiguas de Postfix.


Bloque IV - Punto 3                          33 de 164                                January 31, 2026
                          Correo electrónico. Contenedores y microservicios


    • Dovecot SASL: Implementación moderna y eficiente. Postfix puede configurarse para
      “hablar” con el servicio de autenticación de Dovecot (generalmente a través de un socket
      UNIX), evitando tener que configurar dos bases de datos de usuarios separadas.

1.4.1.2. Mecanismos de Autenticación

La negociación SASL permite al cliente y servidor acordar un método de autenticación. Los más
relevantes para el examen son:


Mecanismo                                          Descripción y Seguridad

PLAIN                                              Envía el usuario y la contraseña en un solo
                                                   mensaje codificado en Base64. Es inseguro por
                                                   sí solo (texto claro) y debe ir acompañado de
                                                   cifrado TLS (STARTTLS).
LOGIN                                              Similar a PLAIN, pero solicita el usuario y la
                                                   contraseña en pasos separados. También
                                                   requiere TLS para ser seguro.
CRAM-MD5                                           Challenge-Response Authentication Mechanism.
                                                   El servidor envía un desafío, y el cliente
                                                   responde con un hash MD5 calculado. La
                                                   contraseña no viaja por la red. Es más seguro
                                                   que PLAIN en canales no cifrados, pero
                                                   requiere almacenar las contraseñas en texto
                                                   claro o formato específico en el servidor.
GSSAPI                                             Utiliza Kerberos V5. Proporciona
                                                   autenticación robusta en entornos
                                                   corporativos (como Active Directory) sin
                                                   transmitir contraseñas.
DIGEST-MD5                                         Similar a CRAM-MD5 pero más robusto.
                                                   Actualmente considerado obsoleto en favor de
                                                   TLS + PLAIN.


1.4.1.3. Funcionamiento de la Sesión

El proceso de autenticación se integra en el diálogo SMTP estándar.
  1. Anuncio de Capacidad (EHLO): El servidor anuncia que soporta autenticación y lista los
     mecanismos disponibles en la respuesta al comando EHLO.
      S: 250-AUTH PLAIN LOGIN CRAM-MD5

  2. Inicio de Autenticación (AUTH): El cliente envía el comando AUTH seguido del mecanismo
     elegido y, opcionalmente, las credenciales codificadas.
      C: AUTH PLAIN dGVzdAB0ZXN0ADEyMzQ=

  3. Resultado:
          • 235 Authentication successful: El cliente puede proceder a enviar correo (relay).


Bloque IV - Punto 3                           34 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


          • 535 Authentication failed: Credenciales inválidas.
      Importante para TAI: Si se utiliza autenticación PLAIN o LOGIN, el puerto de escucha
      debe envolverse en TLS (puerto 465) o actualizarse mediante STARTTLS (puerto
      587/25) antes de enviar las credenciales para evitar que sean interceptadas.

1.4.1.4. Configuración en Servidores Principales

El administrador debe habilitar explícitamente estas directivas para proteger el servidor.
Postfix (main.cf ): Para utilizar la autenticación proporcionada por Dovecot (la configuración
más común en el temario actual):
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth          # Socket UNIX relativo a la cola
smtpd_sasl_auth_enable = yes            # Habilita SMTP-AUTH
smtpd_tls_auth_only = yes               # Prohíbe autenticación sin cifrado TLS
smtpd_recipient_restrictions = permit_sasl_authenticated, reject_unauth_destination

La directiva permit_sasl_authenticated es la que autoriza el relay a los usuarios validados,
previniendo el error “Relay access denied”.
Sendmail (sendmail.mc): Se define mediante la macro TRUST_AUTH_MECH para indicar qué
mecanismos se consideran seguros para permitir el relay.
TRUST_AUTH_MECH(`EXTERNAL DIGEST-MD5 CRAM-MD5 LOGIN PLAIN')
define(`confAUTH_MECHANISMS', `EXTERNAL GSSAPI DIGEST-MD5 CRAM-MD5 LOGIN PLAIN')

La regla trust_auth determina si el parámetro AUTH= es confiable.

1.4.1.5. Probables focos de examen

En las oposiciones a TAI, las preguntas sobre SMTP-AUTH suelen centrarse en la seguridad y el
puerto de servicio.
  1. Prevención de Open Relay:
        • SMTP-AUTH es el mecanismo principal para permitir que usuarios legítimos envíen
          correo desde redes externas (ej. desde casa) sin convertir el servidor en un Open Relay
          (repetidor abierto) para spammers.
  2. Relación con el Puerto 587 (Submission):
        • El puerto 587 (definido en RFC 2476) está dedicado a la sumisión de mensajes por
          parte de clientes (MUAs). A diferencia del puerto 25, el puerto 587 requiere casi
          universalmente autenticación (SMTP-AUTH) y cifrado STARTTLS.
  3. Seguridad de PLAIN/LOGIN:
        • Pregunta trampa común: “¿Es seguro el mecanismo AUTH PLAIN?”.
        • Respuesta: No, salvo que se tunelice a través de una sesión cifrada (TLS/SSL). Envía
          credenciales en Base64, que es una codificación reversible, no un cifrado.
  4. Integración SASL:
        • Identificar a SASL como la capa de abstracción que proporciona servicios de
          autenticación a protocolos como SMTP, IMAP y LDAP.

1.4.2. Cifrado TLS/SSL

El uso de TLS (Transport Layer Security) y su predecesor obsoleto SSL (Secure Sockets Layer)
en la infraestructura de correo electrónico es el mecanismo fundamental para garantizar la


Bloque IV - Punto 3                           35 de 164                           January 31, 2026
                         Correo electrónico. Contenedores y microservicios


confidencialidad e integridad de los datos en tránsito, así como la autenticación de los servidores
involucrados.
Dada la naturaleza del protocolo SMTP original, que transmite información en texto plano
(cleartext), la implementación de TLS es crítica para prevenir la interceptación pasiva
(eavesdropping) y ataques activos de “hombre en el medio” (MITM).

1.4.2.1. Modos de Implementación: Implícito vs. Explícito

Existen dos arquitecturas principales para integrar el cifrado en los protocolos de correo (SMTP,
POP3, IMAP), diferenciadas por cómo se inicia la sesión segura:
1. Cifrado Implícito (Legacy / Wrapper Mode)
    • Funcionamiento: El cliente y el servidor negocian la sesión TLS/SSL inmediatamente al
      establecer la conexión TCP, antes de enviar cualquier comando de aplicación. Si el handshake
      falla, la conexión se corta.
    • Puertos Estándar:
         – SMTPS: Puerto 465 (Aunque obsoleto oficialmente por IETF en favor de STARTTLS,
           sigue siendo ampliamente soportado y usado por MUAs para la sumisión).
         – IMAPS: Puerto 993.
         – POP3S: Puerto 995.
2. Cifrado Explícito (Opportunistic / STARTTLS)
    • Funcionamiento: La conexión comienza en texto plano. El servidor anuncia su capacidad
      de cifrado en la respuesta al comando EHLO (SMTP) o CAPA (POP3). El cliente solicita entonces
      elevar la conexión a cifrada enviando el comando STARTTLS (RFC 3207 para SMTP).
    • Puertos Estándar:
         – SMTP (Relay): Puerto 25.
         – SMTP (Submission): Puerto 587.
         – IMAP/POP3: Puertos 143 y 110 respectivamente.
      Nota Técnica: El modo explícito introduce el riesgo de ataques de degradación
      (downgrade attacks o TLS stripping), donde un atacante intercepta el comando STARTTLS
      o elimina el anuncio de la capacidad, forzando a las partes a comunicarse en texto
      claro.

1.4.2.2. Certificados y Perfect Forward Secrecy (PFS)

Para establecer el túnel TLS, los servidores utilizan certificados X.509.
  1. Tipos de Certificados:
        • Firmados por CA (Autoridad de Certificación): Necesarios para servidores públicos
          y producción. Garantizan que el servidor es quien dice ser ante los clientes (MUAs) y
          otros MTAs.
        • Autofirmados (Self-signed): Generados localmente. Útiles para cifrado interno, pero
          provocan advertencias de seguridad en los clientes y fallos de validación en MTAs
          estrictos.
  2. Perfect Forward Secrecy (PFS):
        • Es una propiedad criptográfica esencial recomendada en configuraciones modernas.
          Asegura que, si la clave privada del servidor es comprometida en el futuro, las sesiones
          pasadas no puedan ser descifradas.


Bloque IV - Punto 3                          36 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


          • Se logra utilizando algoritmos de intercambio de claves efímeros como ECDHE (Elliptic
            Curve Diffie-Hellman Ephemeral) o DHE.

1.4.2.3. Estándares de Refuerzo de Seguridad

Para mitigar la debilidad del modelo oportunista (“fail-open”) de STARTTLS, se han desarrollado
estándares que permiten a los dominios publicar políticas estrictas de cifrado:


Estándar                          Descripción                        Dependencia Clave

MTA-STS (RFC 8461)                SMTP MTA Strict Transport          HTTPS y registro TXT en DNS.
                                  Security. Permite al dominio
                                  declarar que solo acepta
                                  conexiones cifradas y
                                  autenticadas, previniendo
                                  ataques de degradación y
                                  MITM.
DANE (RFC 7672)                   DNS-based Authentication of        DNSSEC.
                                  Named Entities. Vincula
                                  certificados TLS a nombres de
                                  dominio usando DNSSEC
                                  (registros TLSA), eliminando
                                  la dependencia exclusiva de
                                  las CAs comerciales.


1.4.2.4. Configuración en Postfix y Dovecot

En el entorno de examen TAI, es frecuente encontrar preguntas sobre parámetros de configuración
en Linux.
Postfix (main.cf):
    • Habilitar TLS: smtpd_tls_security_level = may (oportunista) o encrypt (obligatorio).
    • Ruta a certificados:
      smtpd_tls_cert_file = /etc/pki/tls/certs/postfix.pem
      smtpd_tls_key_file = /etc/pki/tls/private/postfix.key

    • Forzar TLS para autenticación (recomendado): smtpd_tls_auth_only = yes.
Dovecot (conf.d/10-ssl.conf):
    • Habilitar SSL: ssl = yes o ssl = required.
    • Ruta a certificados:
      ssl_cert = </etc/pki/dovecot/certs/server.crt
      ssl_key = </etc/pki/dovecot/private/server.key

    • Parámetros DH para PFS: ssl_dh = </etc/dovecot/dh.pem>.




Bloque IV - Punto 3                           37 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.4.2.5. Probables focos de examen

  1. Asociación Puerto-Protocolo-Cifrado:
        • Pregunta clásica: Identificar que el puerto 993 corresponde a IMAPS (IMAP sobre SSL
          implícito) y el 995 a POP3S.
        • Distinguir que el puerto 587 usa STARTTLS (explícito), mientras que el 465 usa cifrado
          implícito desde la conexión.
  2. Concepto de STARTTLS:
        • Entender que STARTTLS es un comando para elevar una conexión insegura a segura,
          no un protocolo distinto.
        • Saber que si la negociación STARTTLS falla en modo oportunista, la transmisión puede
          continuar en texto claro (riesgo de seguridad).
  3. Diferencia DANE vs MTA-STS:
        • DANE requiere obligatoriamente DNSSEC.
        • MTA-STS se basa en políticas publicadas vía HTTPS y registros DNS TXT, y usa
          certificados de CA (PKIX), siendo una alternativa si no se tiene DNSSEC.
  4. Certificados en Postfix/Dovecot:
        • Identificar las directivas smtpd_tls_cert_file (Postfix) y ssl_cert (Dovecot) como las
          encargadas de apuntar al certificado público.
        • Recordar que la clave privada (.key) debe tener permisos restrictivos (solo lectura por
          root o el usuario del servicio).

1.4.3. SPF (Sender Policy Framework)

El Sender Policy Framework (SPF) es un estándar abierto y un mecanismo de autenticación de
correo electrónico diseñado para prevenir la suplantación de identidad del remitente (spoofing)
mediante la verificación de las direcciones IP.
Actualmente definido en la RFC 7208 (que deja obsoleta la RFC 4408), SPF permite a los
administradores de un dominio especificar explícitamente qué servidores de correo (hosts) están
autorizados para enviar correos en nombre de dicho dominio.

1.4.3.1. Funcionamiento Técnico y Registro DNS

SPF funciona mediante la publicación de registros de recursos (RR) en el DNS (Sistema de Nombres
de Dominio) del propietario del dominio. Específicamente, utiliza un registro de tipo TXT.
Cuando un servidor de correo receptor (MTA) acepta una conexión entrante, realiza los siguientes
pasos:
  1. Extrae la dirección del dominio del remitente indicada en el comando MAIL FROM del sobre
     SMTP (Envelope Sender).
  2. Consulta el DNS de dicho dominio buscando el registro TXT que comienza con la cadena de
     versión v=spf1.
  3. Compara la dirección IP del servidor que está intentando entregar el correo con la lista de
     direcciones IP autorizadas definidas en el registro SPF.
  4. Aplica la política de resultado (aceptar, rechazar o marcar) según lo especificado.
      Importante para el examen: SPF valida el Envelope Sender (MAIL FROM en la sesión
      SMTP), no la dirección que el usuario ve en el campo From: del encabezado del mensaje
      (RFC 5322). Esta distinción es crítica porque un atacante puede usar un dominio propio



Bloque IV - Punto 3                          38 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      válido en el MAIL FROM (pasando SPF) pero mostrar una dirección falsificada en el From:
      visible.

1.4.3.2. Sintaxis del Registro y Mecanismos

Un registro SPF se evalúa secuencialmente de izquierda a derecha. Se compone de la versión, una
serie de mecanismos y calificadores.
Estructura típica: v=spf1 [mecanismo] [mecanismo] [calificador]all
Tabla de Mecanismos Comunes:

Mecanismo                         Descripción                        Ejemplo

ip4 / ip6                         Autoriza una dirección IP o        ip4:192.168.0.1
                                  rango de red (CIDR) específico.
a                                 Autoriza la IP a la que resuelve   a:mail.ejemplo.com
                                  el registro A o AAAA del
                                  dominio.
mx                                Autoriza las IPs de los            mx
                                  servidores listados en los
                                  registros MX del dominio.
include                           Incluye recursivamente las         include:_spf.google.com
                                  políticas SPF de otro dominio.
                                  Fundamental para autorizar
                                  servicios de terceros (ej.
                                  Google, Office 365).
all                               Coincide con cualquier IP.         -all
                                  Siempre se coloca al final para
                                  definir la política por defecto.


Tabla de Calificadores (Prefijos): El calificador indica qué acción tomar si el mecanismo coincide.
Si no se especifica, se asume + (Pass).


Calificador                       Resultado                          Significado Técnico y Uso

+                                 Pass                               La IP está autorizada. El correo
                                                                     debe aceptarse. (Por defecto).
-                                 Fail (Hardfail)                    La IP no está autorizada. El
                                                                     correo debe ser rechazado
                                                                     taxativamente.
~                                 SoftFail                           La IP no está autorizada, pero
                                                                     se permite el paso
                                                                     (usualmente marcándolo
                                                                     como sospechoso o spam).
                                                                     Útil en transiciones.


Bloque IV - Punto 3                           39 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios



Calificador                        Resultado                         Significado Técnico y Uso

?                                  Neutral                           No hay política definida sobre
                                                                     la IP. El resultado es “neutral”.


Ejemplo de registro completo: v=spf1 mx include:_spf.google.com ip4:203.0.113.0/24 -all
Interpretación: Autoriza a los servidores MX del dominio, a los servidores de Google y a la red
203.0.113.0/24. Rechaza (-all) cualquier otra IP.

1.4.3.3. Limitaciones Críticas

Para el desempeño de un TAI, es vital conocer las debilidades del protocolo, que suelen ser objeto
de preguntas prácticas:
    1. Límite de Búsquedas DNS (DNS Lookup Limit): Para evitar ataques de denegación de servicio
       (DoS), el estándar impone un límite máximo de 10 consultas DNS (lookups) necesarias para
       resolver un registro SPF completo (esto incluye los mecanismos include, a, mx, ptr y exists).
       Si se supera, el resultado es PermError y el SPF falla.
    2. Problema del Reenvío (Forwarding): SPF rompe el reenvío automático de correos. Si el
       servidor A envía un correo al servidor B, y B lo reenvía automáticamente a C, el servidor C
       verá la IP de conexión de B, pero el MAIL FROM seguirá diciendo que viene de A. Como B no
       está en el registro SPF de A, la validación fallará.
    3. Falta de Protección de Integridad: SPF no valida el contenido del mensaje ni protege contra
       la modificación del mismo en tránsito (para esto se usa DKIM).

1.4.3.4. Probables focos de examen

     • RFC de Referencia: Identificar la RFC 7208 como el estándar actual (sustituye a la 4408).
     • Significado de los Calificadores: Diferenciar claramente entre -all (HardFail - rechazo) y
       ~all (SoftFail - aceptar pero marcar/sospechoso).
     • Límite de 10 consultas: Es una pregunta técnica frecuente sobre por qué un registro SPF
       válido sintácticamente puede fallar en producción.
     • Alcance de la Protección: Saber que SPF protege el Envelope Sender (MAIL FROM), no el
       encabezado From: que ve el usuario. Esta es la razón por la que SPF por sí solo no detiene
       todo el spoofing visual.
     • Tipo de Registro DNS: Identificar que se implementa mediante un registro TXT.

1.4.4. DKIM (DomainKeys Identified Mail)

DKIM (DomainKeys Identified Mail) es un protocolo de autenticación de correo electrónico definido
actualmente en la RFC 6376 (que obsoleta a la RFC 4871). Su propósito fundamental es permitir
que una organización se responsabilice del envío de un mensaje, asociando un nombre de dominio
al correo mediante una firma digital criptográfica.
A diferencia de SPF, que valida la dirección IP del remitente, DKIM valida la identidad del dominio
firmante y garantiza la integridad del mensaje, asegurando que el contenido (cuerpo y cabeceras
seleccionadas) no ha sido alterado durante el tránsito.



Bloque IV - Punto 3                            40 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.4.4.1. Funcionamiento Técnico y Arquitectura

El sistema DKIM se basa en criptografía asimétrica (clave pública y clave privada). El proceso se
divide en dos fases: firma (en el servidor de salida) y verificación (en el servidor de destino).
  1. Generación de Claves y Publicación en DNS: El administrador del dominio genera un par de
     claves (pública y privada). La clave privada se instala en el servidor de correo saliente (MTA).
     La clave pública se publica en el servidor DNS del dominio como un registro de tipo TXT.
  2. Firma del Mensaje (Signing): Cuando el MTA envía un correo, utiliza la clave privada para
     generar un hash del cuerpo del mensaje y de una selección de cabeceras. Este hash se cifra y
     se adjunta al correo como una nueva cabecera denominada DKIM-Signature.
  3. Verificación del Mensaje (Verifying): El servidor receptor (MTA o MDA) detecta la cabecera
     DKIM-Signature. Extrae el dominio (d=) y el selector (s=) de dicha cabecera. Con estos datos,
     realiza una consulta DNS para obtener la clave pública del remitente. Si la firma descifrada
     con la clave pública coincide con el hash calculado del mensaje recibido, se confirma la
     autenticidad y la integridad.

1.4.4.2. El Selector y el Registro DNS

Un concepto crítico en DKIM es el selector. El selector es una cadena arbitraria que permite
diferenciar múltiples claves públicas bajo un mismo dominio (por ejemplo, para distintos
departamentos, proveedores externos o rotación de claves).
La ubicación en el DNS donde se debe buscar la clave pública sigue una estructura jerárquica
estricta:
selector._domainkey.dominio.tld

     • _domainkey: Es un subdominio reservado y obligatorio en la especificación para alojar las
       claves DKIM.
     • Registro TXT: El contenido del registro suele tener el formato: v=DKIM1; k=rsa;
       p=<clave_pública_en_base64>.


1.4.4.3. Estructura de la Cabecera DKIM-Signature

La cabecera insertada en el correo contiene diversas etiquetas (tags) que instruyen al receptor
sobre cómo validar la firma. Los campos más relevantes para el examen son:


Etiqueta                          Significado                       Descripción Técnica

v=                                Versión                           Siempre debe ser 1.
a=                                Algoritmo                         Algoritmo usado para la firma,
                                                                    típicamente rsa-sha256
                                                                    (recomendado) o rsa-sha1
                                                                    (obsoleto).
d=                                Dominio                           El dominio que firma el
                                                                    mensaje (SDID - Signing
                                                                    Domain Identifier).




Bloque IV - Punto 3                           41 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios



Etiqueta                         Significado                       Descripción Técnica

s=                               Selector                          Identificador para localizar la
                                                                   clave pública en el DNS.
h=                               Cabeceras                         Lista de las cabeceras del
                                                                   correo que han sido firmadas
                                                                   (ej. From:Subject:Date).
bh=                              Body Hash                         El hash del cuerpo del mensaje.
                                                                   Asegura que el contenido no
                                                                   ha sido modificado.
b=                               Firma                             La firma digital propiamente
                                                                   dicha de las cabeceras y el
                                                                   hash del cuerpo.
c=                               Canonicalización                  Método para tratar los
                                                                   espacios en blanco antes de
                                                                   firmar. Puede ser simple
                                                                   (estricto) o relaxed (tolera
                                                                   cambios menores de formato
                                                                   por servidores intermedios).


1.4.4.4. Probables focos de examen

En las oposiciones a TAI, DKIM suele ser objeto de preguntas técnicas sobre su implementación y
diferencias con otros protocolos.
  1. Diferencia clave con SPF:
        • SPF valida la IP del servidor remitente (autorización de transporte).
        • DKIM valida la integridad del mensaje y la identidad del dominio mediante criptografía
          (no depende de la IP).
        • Pregunta tipo: “¿Qué protocolo garantiza que el contenido de un correo no ha sido
          modificado en tránsito?” → DKIM.
  2. Construcción del registro DNS:
        • Es vital recordar la sintaxis de la consulta DNS: <selector>._domainkey.<dominio>. El
          uso de la palabra reservada _domainkey es una pregunta frecuente de sintaxis.
  3. Tipo de Registro DNS:
        • Se implementa mediante un registro TXT.
  4. Resistencia al reenvío (Forwarding):
        • A diferencia de SPF, que suele fallar cuando un correo es reenviado automáticamente
          (ya que cambia la IP de origen pero no el remitente), DKIM sobrevive al reenvío siempre
          que el servidor intermediario no modifique el cuerpo o las cabeceras firmadas.
  5. Relación con DMARC:
        • DKIM por sí solo no verifica que el dominio de la firma (d=) coincida con el dominio que
          ve el usuario en el campo From:. Esa validación de “alineación” la realiza DMARC.




Bloque IV - Punto 3                          42 de 164                             January 31, 2026
                        Correo electrónico. Contenedores y microservicios


1.4.5. DMARC (Domain-based Message Authentication, Reporting, and Conformance)

DMARC (Autenticación de Mensajes, Informes y Conformidad Basada en Dominios) es un estándar
técnico y un mecanismo de política que unifica los protocolos SPF y DKIM con el objetivo de
proteger el dominio de correo electrónico contra la suplantación de identidad (spoofing) y el
phishing.
Definido en la RFC 7489„ DMARC resuelve una limitación crítica de SPF y DKIM: ninguno de
estos protocolos valida explícitamente la dirección que el usuario final ve en el campo From:
de su cliente de correo. DMARC añade una capa de validación que vincula el dominio de ese
encabezado con los dominios validados por SPF y DKIM, un concepto conocido como alineación
de identificadores.

1.4.5.1. Arquitectura y Alineación de Identificadores

El funcionamiento de DMARC se basa en que el receptor verifique si el mensaje cumple con SPF
y/o DKIM y, crucialmente, si los dominios autenticados coinciden con el dominio del remitente
visible (Header From).
Concepto de Alineación (Alignment): Para que DMARC pase (“Pass”), el mensaje debe pasar la
autenticación SPF o DKIM y, además, existir una alineación de dominios:
  1. Alineación SPF: El dominio en el campo MAIL FROM (Envelope Sender) debe coincidir con el
     dominio del encabezado From: (RFC 5322).
  2. Alineación DKIM: El dominio especificado en la etiqueta d= de la firma DKIM debe coincidir
     con el dominio del encabezado From:.
Modos de Alineación: El propietario del dominio puede configurar la rigurosidad de esta
coincidencia mediante las etiquetas aspf y adkim:
    • Relaxed (r): (Por defecto). Permite coincidencias de subdominios (ej. mail.ejemplo.com
      alinea con ejemplo.com).
    • Strict (s): Exige una coincidencia exacta del dominio.
Esquema del Flujo de Validación DMARC:
   +---------------------+
   | Correo Entrante     |
   | Header From:        |
   | usuario@banco.com |
   +----------+----------+
              |
              v
   +----------+-----------+       +-----------+----------+
   | Verificación SPF     |       | Verificación DKIM    |
   | (Envelope From)      |       | (Firma d=...)        |
   +----------+-----------+       +-----------+----------+
              |                               |
              v                               v
   +----------+-----------+       +-----------+----------+
   | ¿Alineación con      |       | ¿Alineación con      |
   | Header From?          |      | Header From?         |
   +----------+-----------+       +-----------+----------+
              |                               |
              +---------------+---------------+
                              |
                              v


Bloque IV - Punto 3                         43 de 164                           January 31, 2026
                             Correo electrónico. Contenedores y microservicios


                          +---------+---------+
                          | Resultado DMARC |
                          |   (Pass / Fail)   |
                          +---------+---------+
                                    |
                      Si falla ambos, aplicar Política (p=)


1.4.5.2. El Registro DNS y Políticas de Aplicación

Para implementar DMARC, el administrador del dominio debe publicar un registro TXT en el DNS
en la ubicación específica _dmarc.<dominio> (ej. _dmarc.ejemplo.com).
Este registro contiene una serie de etiquetas separadas por punto y coma. Las más relevantes
para el examen son:


Etiqueta                             Nombre                             Descripción y Valores

v=                                   Versión                            Obligatorio. Siempre debe ser
                                                                        DMARC1. Debe ser la primera
                                                                        etiqueta.
p=                                   Política                           Obligatorio. Indica al receptor
                                                                        qué hacer si el mensaje falla
                                                                        DMARC. Valores: none
                                                                        (monitoreo), quarantine
                                                                        (spam), reject (rechazar).
rua=                                 Reporting URI (Aggregate)          Dirección de correo (URI
                                                                        mailto:) donde enviar
                                                                        informes agregados XML
                                                                        periódicos sobre el tráfico del
                                                                        dominio.
ruf=                                 Reporting URI (Forensic)           Dirección para enviar
                                                                        informes forenses detallados
                                                                        de fallos individuales (menos
                                                                        común por privacidad).
pct=                                 Porcentaje                         Porcentaje de mensajes a los
                                                                        que se aplica la política (útil
                                                                        para despliegue gradual). Por
                                                                        defecto es 100.
sp=                                  Subdomain Policy                   Política específica para
                                                                        subdominios. Si no se define,
                                                                        heredan la política p.


Ejemplo de registro en modo monitoreo: v=DMARC1; p=none; rua=mailto:admin@ejemplo.com.
Ejemplo de registro en modo rechazo estricto: v=DMARC1; p=reject; sp=reject; adkim=s;
aspf=s.




Bloque IV - Punto 3                               44 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


1.4.5.3. Informes y Visibilidad (Reporting)

Una característica distintiva de DMARC es que proporciona retroalimentación (feedback) al
propietario del dominio. Esto permite a los administradores detectar si alguien está suplantando
su dominio o si hay servidores legítimos mal configurados.
  1. Informes Agregados (Aggregate Reports - RUA): Se envían diariamente en formato XML.
     Proporcionan estadísticas sobre IPs que envían correo en nombre del dominio y el resultado
     de las validaciones SPF/DKIM.
  2. Informes Forenses (Failure Reports - RUF): Se envían en tiempo real cuando ocurre un fallo.
     Incluyen detalles del mensaje y cabeceras, lo que puede implicar datos personales (PII).

1.4.5.4. Probables focos de examen

En las oposiciones a TAI, DMARC es un tema creciente en seguridad. Puntos clave a memorizar:
  1. RFC de Referencia:
        • La norma que define DMARC es la RFC 7489.
  2. Las Tres Políticas (p=):
        • Saber distinguir y ordenar por severidad:
           1. none: Solo monitoreo, no afecta la entrega. Es el paso inicial recomendado.
           2. quarantine: Marca como sospechoso (carpeta de spam/junk).
           3. reject: Rechaza el mensaje a nivel SMTP. Máxima seguridad.
  3. Dependencia de Protocolos:
        • DMARC no funciona por sí solo como mecanismo de autenticación criptográfica o de IP;
          se apoya en los resultados de SPF y DKIM.
        • Para que DMARC pase, basta con que uno de los dos (SPF o DKIM) pase y esté alineado.
  4. Nombre del Registro DNS:
        • El registro TXT debe publicarse obligatoriamente en el subdominio _dmarc (con guion
          bajo).
        • Pregunta trampa: Omitir el guion bajo o ubicarlo en la raíz del dominio.
  5. Alineación (Alignment):
        • Entender que DMARC soluciona la discrepancia entre el MAIL FROM (técnico) y el From:
          (visible) que SPF no cubre por defecto.

1.5. Gestión de spam y filtrado
Esta sección aborda uno de los desafíos más persistentes y costosos en la administración de
servidores de correo: la lucha contra el correo no deseado o spam. Dado que se estima que una
gran mayoría del tráfico de correo global es ilegítimo, la implementación de sistemas de filtrado
eficaces no es opcional, sino un requisito indispensable para preservar el ancho de banda, el
almacenamiento y la productividad de los usuarios.
La gestión de spam no se basa en una única herramienta, sino en una estrategia de “defensa en
profundidad” que aplica capas sucesivas de filtrado. El objetivo es descartar la mayor cantidad de
correo basura lo antes posible (durante la conexión SMTP) para ahorrar recursos de procesamiento,
y someter el correo restante a un análisis de contenido más exhaustivo. Esta estrategia combina
el uso de fuentes de reputación externas, análisis heurístico del contenido y algoritmos de
aprendizaje automático que se adaptan a los patrones cambiantes de los spammers.
A continuación, se detalla la función de las tres barreras principales que se estudiarán en este
bloque:


Bloque IV - Punto 3                         45 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Mecanismo                Método de Análisis        Momento de Acción         Objetivo

Listas Negras (RBL) y    Reputación de la IP y     Durante la conexión       Bloquear fuentes
Grises                   comportamiento            SMTP.                     conocidas de spam o
                         temporal.                                           bots mal
                                                                             configurados.
SpamAssassin             Sistema de                Tras recibir el mensaje   Evaluar cabeceras y
                         puntuación basado en      (Pre-entrega).            cuerpo para detectar
                         reglas y pruebas                                    patrones sospechosos.
                         múltiples.
Filtros Bayesianos       Probabilidad              Continuo                  “Aprender” del
                         estadística y             (Entrenamiento).          usuario para
                         aprendizaje.                                        distinguir vocabulario
                                                                             legítimo (ham) de
                                                                             basura (spam).


El éxito en la administración de estos filtros radica en encontrar el equilibrio perfecto entre la
agresividad del bloqueo y la minimización de los “falsos positivos” (correos legítimos marcados
erróneamente como spam), un escenario que puede ser crítico para la operativa de una empresa.

1.5.1. Listas negras y grises

La gestión del correo no deseado (spam) se apoya en mecanismos de filtrado basados en la
reputación del remitente. A diferencia del filtrado de contenido (que analiza el texto del mensaje),
estos métodos evalúan la legitimidad del servidor de origen antes o durante la transacción SMTP.
Los dos mecanismos más relevantes en esta categoría son las Listas Negras (DNSBL/RBL) y las
Listas Grises (Greylisting).

1.5.1.1. Listas Negras Basadas en DNS (DNSBL / RBL)

Las DNSBL (DNS-based Blacklists) o RBL (Real-time Blackhole Lists) son bases de datos consultables
en tiempo real que contienen direcciones IP o dominios identificados como fuentes de spam,
relays abiertos o servidores comprometidos.
1. Fundamento Técnico y RFC 5782 El funcionamiento de estas listas está documentado en la
RFC 5782. El mecanismo aprovecha el protocolo DNS para publicar listas de direcciones IP de
servidores SMTP conocidos por enviar spam o por ser servidores legítimos (listas blancas).
2. Mecanismo de Consulta Cuando un servidor de correo recibe una conexión entrante, realiza
una consulta DNS para verificar la reputación de la IP del remitente. El proceso técnico estándar
es el siguiente:
  1. Se toman los octetos de la dirección IP del remitente.
  2. Se invierten los octetos (similar a la resolución inversa en DNS).
  3. Se añade el nombre de dominio del proveedor de la lista negra (por ejemplo, zen.spamhaus.org).
  4. Se realiza una consulta de tipo A o TXT.
Si la IP está listada, el servidor DNS devuelve una respuesta (típicamente 127.0.0.x), lo que indica
al servidor de correo que debe rechazar la conexión o marcar el mensaje. Las listas negras también
suelen proporcionar un registro DNS TXT con la razón del bloqueo.

Bloque IV - Punto 3                           46 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3. Clasificación de Fuentes de Spam Los sistemas de reputación IP identifican tres categorías
principales de remitentes que suelen poblar estas listas:
    • Servidores legítimos: Infraestructura privada configurada para enviar correo lícito (suelen
      estar en listas blancas o whitelists).
    • Hosts finales (End-hosts): Máquinas de usuarios finales que no deberían enviar correo
      directamente, a menudo infectadas por malware (botnets) con capacidades SMTP.
    • Bandas de Spam (Spam gangs): Spammers sofisticados que configuran mecanismos
      elaborados para simular legitimidad.
4. Terminología de Examen Es común referirse a los servidores que alojan estas listas como
“black-hole servers” (servidores de agujero negro). Su uso se considera la “primera línea de
defensa” en una estrategia de seguridad en profundidad, ya que permite rechazar conexiones
antes de consumir recursos en el procesamiento del contenido del mensaje.

1.5.1.2. Listas Grises (Greylisting)

El Greylisting es una técnica de filtrado de spam ligera que rechaza temporalmente el correo
electrónico de un remitente desconocido, basándose en la premisa de que los servidores de correo
legítimos reintentarán el envío, mientras que el software de envío de spam (generalmente scripts
simples o botnets) no lo hará.
1. Funcionamiento del Protocolo (La “tripleta”) El greylisting no analiza el contenido, sino que
registra tres datos fundamentales de cualquier mensaje entrante, conocidos como la tripleta
(triplet):
  1. Dirección IP del host que intenta la entrega.
  2. Dirección del remitente (Envelope sender).
  3. Dirección del destinatario (Envelope recipient).
2. Flujo de Decisión El proceso sigue una lógica estricta de “Fallo Temporal”:
  1. Primer intento: Si la tripleta no se ha visto antes en la base de datos local, el servidor rechaza
     el mensaje con un código de error temporal (códigos 4xx del protocolo SMTP).
  2. Periodo de espera: Se impone un intervalo de tiempo durante el cual cualquier reintento
     será rechazado.
  3. Reintento legítimo: Un servidor MTA que cumpla con los RFCs (como Postfix o Sendmail)
     interpretará el error 4xx como transitorio y reintentará el envío tras unos minutos.
  4. Aceptación: Si el reintento ocurre después del periodo de espera, el servidor acepta el
     mensaje y añade la tripleta a una lista blanca interna para no retrasar futuros correos de ese
     remitente.
3. Ventajas y Desafíos
    • Eficacia: Es altamente efectivo porque la mayoría de los spammers utilizan software de
      “disparar y olvidar” (fire-and-forget) que no gestiona colas de reintento para maximizar el
      volumen de envío.
    • Limitaciones (Granjas de Servidores): Un problema conocido surge con grandes
      proveedores (como Gmail o Outlook) que utilizan granjas de servidores salientes. El primer
      intento puede venir de la IP A, y el reintento de la IP B. Como la tripleta incluye la IP, el
      greylisting estricto fallaría. Para solucionar esto, existen implementaciones de “greylisting
      adaptativo” o de dos niveles que consideran rangos de red o dominios en lugar de IPs
      individuales.



Bloque IV - Punto 3                           47 de 164                                January 31, 2026
                          Correo electrónico. Contenedores y microservicios


1.5.1.3. Listas Blancas (Whitelists)

Aunque el epígrafe se centra en listas negras y grises, el concepto de DNSWL (DNS Whitelist) es
complementario y examinable. Permite identificar servidores SMTP legítimos para evitar que sean
filtrados por falsos positivos en las listas negras o retrasados por el greylisting. En la configuración
de seguridad (como DMARC), se recomienda incluir en listas blancas a los reenviadores conocidos
para evitar fallos de autenticación.

1.5.1.4. Probables focos de examen

En las oposiciones para TAI, es frecuente que se evalúe la capacidad de distinguir el
comportamiento técnico de estos mecanismos.
1.5.1.4.1. Distinción de Códigos de Error SMTP
    • Greylisting: Debe asociarse obligatoriamente con códigos de error temporales (4xx),
      típicamente 450 o 451. Si devolviera un error permanente (5xx), el correo se perdería y no se
      reintentaría.
    • Blacklisting: Generalmente resulta en un rechazo permanente o marcado, dependiendo
      de la política, pero el rechazo a nivel de conexión suele usar códigos 5xx (ej. 554 Service
      unavailable).

1.5.1.4.2. Composición de la Tripleta (Greylisting)
    • Es muy probable una pregunta tipo test sobre qué datos componen la tripleta del greylisting.
    • Respuesta correcta: IP origen, Remitente (Envelope Sender), Destinatario (Envelope
      Recipient).
1.5.1.4.3. RFC de Referencia DNSxL
    • Identificar la RFC 5782 como el documento que estandariza las listas negras y blancas
      basadas en DNS.
1.5.1.4.4. Mecanismo de Consulta DNSBL
    • Saber que la consulta DNS se realiza invirtiendo los octetos de la dirección IP.
    • Ejemplo: Para verificar la IP 1.2.3.4 en la lista rbl.ejemplo.com, se consulta 4.3.2.1.rbl.ejemplo.com.
1.5.1.4.5. Ubicación en la Arquitectura
    • Tanto las listas negras como el greylisting actúan sobre las propiedades del servidor
      remitente (nivel de transporte/conexión) y no sobre el contenido del mensaje (nivel de
      aplicación/datos), lo que las hace “ligeras” en consumo de CPU.

1.5.2. SpamAssassin

Apache SpamAssassin es una plataforma de clasificación de correo electrónico de código
abierto, escrita principalmente en Perl, que utiliza una amplia variedad de pruebas heurísticas y
estadísticas para identificar correo no deseado (spam). A diferencia de los filtros de conexión
(como las listas negras DNSBL) que actúan durante la transacción SMTP, SpamAssassin analiza el
contenido completo del mensaje (cabeceras y cuerpo) una vez que ha sido aceptado por el sistema
o durante la fase de datos.




Bloque IV - Punto 3                            48 de 164                                January 31, 2026
                          Correo electrónico. Contenedores y microservicios


1.5.2.1. Arquitectura y Funcionamiento: Sistema de Puntuación

El núcleo de SpamAssassin es un sistema basado en reglas y puntuaciones. El funcionamiento
sigue una lógica acumulativa:
  1. Análisis: Cada mensaje entrante es sometido a cientos de pruebas diferentes.
  2. Puntuación (Scoring): Cada prueba tiene asignada una puntuación (positiva para
     indicadores de spam, negativa para indicadores de correo legítimo o ham).
  3. Evaluación: Se suman las puntuaciones de todas las reglas activadas.
  4. Veredicto: Si la suma total supera un umbral (threshold) predefinido (por defecto suele ser
     5.0), el correo se etiqueta como spam.

1.5.2.2. Métodos de Análisis y Filtros

SpamAssassin no confía en un único método, sino que emplea una estrategia híbrida que combina
múltiples técnicas:
  1. Análisis de Cabeceras y Texto (Reglas Estáticas): Utiliza expresiones regulares para buscar
     patrones sospechosos en las cabeceras (ej. Message-ID mal formados, fechas incorrectas) y
     en el cuerpo del mensaje (palabras clave, ofuscación de texto, HTML inválido).
  2. Filtrado Bayesiano (Naive Bayes): Incorpora un clasificador bayesiano propio que aprende
     de los correos recibidos. Analiza la frecuencia de palabras (tokens) en correos marcados
     previamente como spam o ham para calcular la probabilidad de que un nuevo mensaje sea
     no deseado. Este componente permite que el filtro se adapte al entorno específico de la
     organización.
  3. Consultas de Red (Network Tests):
          • DNSBL/RBL: Consulta listas negras en tiempo real para verificar la reputación de la IP
            del remitente.
          • DCC/Razor/Pyzor: Utiliza redes de checksums distribuidos para detectar correos
            masivos idénticos enviados a múltiples destinatarios.
          • Autenticación: Verifica los registros SPF, DKIM y DMARC del remitente.

1.5.2.3. Integración en la Infraestructura de Correo

SpamAssassin raramente actúa como un demonio aislado expuesto a Internet; se integra en el
flujo de correo mediante herramientas intermediarias o “pegamento” (glue).
    • Arquitectura spamd/spamc: Para mejorar el rendimiento en sistemas de alta carga, se utiliza
      un modelo cliente-servidor.
         – spamd: Demonio persistente que carga las reglas en memoria.
         – spamc: Cliente ligero escrito en C que pasa el correo a spamd para su análisis, reduciendo
           la sobrecarga de iniciar el intérprete de Perl para cada mensaje.
    • Amavisd-new: Es la forma más común de integración en entornos Postfix. Amavisd actúa
      como interfaz entre el MTA y los analizadores de contenido (SpamAssassin para spam y
      ClamAV para virus), permitiendo descomprimir adjuntos y aplicar políticas antes de la
      entrega final.
    • Procmail/Sieve: Pueden invocar a SpamAssassin en el momento de la entrega local (MDA)
      para clasificar el correo en carpetas de usuario basadas en las etiquetas añadidas.



Bloque IV - Punto 3                           49 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


1.5.2.4. Modificación del Mensaje y Etiquetado

Cuando SpamAssassin procesa un correo, no lo borra por defecto (aunque puede configurarse para
hacerlo). Su función estándar es etiquetar el mensaje añadiendo cabeceras X-Header para que el
MUA (cliente de correo) o el MDA (agente de entrega) tomen la decisión final (mover a carpeta de
Spam, borrar, etc.).
Las cabeceras típicas inyectadas son:
    • X-Spam-Status: Indica “Yes” o “No”, la puntuación obtenida, el umbral requerido y las
      pruebas que fallaron.
    • X-Spam-Flag: Booleano (YES/NO) para facilitar el filtrado simple.
    • X-Spam-Level: Una representación visual de la puntuación mediante asteriscos (ej. *****
      para una puntuación de 5), útil para reglas de filtrado en clientes de correo.

1.5.2.5. Probables focos de examen

  1. Naturaleza del Filtrado:
        • SpamAssassin es un filtro de contenido (Capa 7 Aplicación), a diferencia de las Listas
          Grises o Firewalls que operan a nivel de conexión. Consume significativamente más
          CPU y memoria que los filtros de conexión.
  2. Cabeceras Específicas:
        • Identificar X-Spam-Flag: YES y X-Spam-Level como las marcas estándar que añade
          el software para que el cliente de correo (Outlook, Thunderbird) filtre el mensaje
          automáticamente.
  3. Relación con Amavis:
        • En preguntas sobre arquitectura de servidores Linux (Postfix), la respuesta correcta
          sobre cómo integrar antivirus y antispam suele ser mediante Amavisd-new, que
          orquesta la llamada a SpamAssassin.
  4. Falsos Positivos vs. Negativos:
        • Un falso positivo es un correo legítimo marcado como spam.
        • SpamAssassin utiliza un sistema de puntuación (scoring). Aumentar el umbral (ej.
          de 5.0 a 8.0) reduce los falsos positivos pero aumenta los falsos negativos (entra más
          spam).
  5. Entrenamiento Bayesiano:
        • Saber que SpamAssassin incluye un módulo bayesiano que requiere “entrenamiento”
          (aprender qué es spam y qué es ham para ese usuario específico) para ser efectivo.

1.5.3. Filtros bayesianos

Los filtros bayesianos representan una de las técnicas más eficaces y extendidas en la lucha
contra el correo no deseado (spam). A diferencia de las listas negras (basadas en la reputación del
origen) o los filtros de reglas estáticas, los filtros bayesianos son sistemas de filtrado basado en
contenido que utilizan algoritmos de aprendizaje automático (Machine Learning) para calcular la
probabilidad de que un mensaje sea spam basándose en las palabras o “tokens” que contiene.
Su fundamento matemático reside en el Teorema de Bayes, utilizado para predecir la
probabilidad de un evento basándose en el conocimiento previo de las condiciones que podrían
estar relacionadas con ese evento.




Bloque IV - Punto 3                          50 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


1.5.3.1. Arquitectura y Modelo Naïve Bayes

La implementación más común es el Naïve Bayes (Bayes ingenuo). Este clasificador asume
la hipótesis “ingenua” de que la presencia de una característica (palabra) en un mensaje es
estadísticamente independiente de la presencia de cualquier otra característica. Aunque esta
asunción es lingüísticamente incorrecta (las palabras en un texto están correlacionadas), el
modelo resulta computacionalmente eficiente y sorprendentemente preciso en la práctica.
El núcleo del cálculo se basa en estimar la probabilidad posterior. La fórmula básica aplicada a
una palabra específica es:

                                              𝑃(𝑃𝑎𝑙𝑎𝑏𝑟𝑎|𝑆𝑝𝑎𝑚) ⋅ 𝑃(𝑆𝑝𝑎𝑚)
                          𝑃(𝑆𝑝𝑎𝑚|𝑃𝑎𝑙𝑎𝑏𝑟𝑎) =
                                                      𝑃(𝑃𝑎𝑙𝑎𝑏𝑟𝑎)

Donde el sistema evalúa la frecuencia de aparición de un término en correos previamente
clasificados como spam frente a su aparición en correos legítimos (ham).

1.5.3.2. Fases del Proceso de Filtrado

El funcionamiento de un filtro bayesiano es dinámico y se adapta al flujo de correo de la
organización.
  1. Entrenamiento (Training): El filtro necesita ser alimentado inicialmente con dos corpus
     de mensajes: uno de Spam (correo basura confirmado) y otro de Ham (correo legítimo).
     El sistema analiza estos textos y construye una base de datos de frecuencias de palabras
     (tokens).
        • Existen métodos de entrenamiento como TEFT (Train Every Thing), TOE (Train Only
          Errors) o TUNE (Train Until No Errors).
  2. Tokenización y Cálculo de Probabilidades Locales: Cuando llega un nuevo mensaje, el
     sistema lo descompone en tokens (palabras o n-gramas). Para cada token, calcula una
     probabilidad local de ser spam.
        • Suavizado (Smoothing): Dado que algunas palabras pueden no haber aparecido nunca
          en el entrenamiento (frecuencia cero), se aplican técnicas matemáticas (como la Ley de
          Lidstone o parámetros 𝜖) para evitar divisiones por cero o probabilidades absolutas de 0
          o 1, que desestabilizarían el cálculo total.
  3. Combinación y Puntuación (Scoring): Las probabilidades individuales de las palabras más
     significativas del mensaje se combinan utilizando la regla de la cadena de Bayes (Bayesian
     chain rule) para generar una probabilidad global para todo el mensaje.
        • Si la probabilidad final supera un umbral predefinido (típicamente 0.5 o superior,
          dependiendo de la agresividad deseada), el mensaje se clasifica como spam.

1.5.3.3. Adaptabilidad y Contramedidas

Una de las mayores fortalezas del filtrado bayesiano es su capacidad de aprendizaje continuo. A
medida que los usuarios marcan falsos positivos o falsos negativos, el filtro actualiza su base de
datos de probabilidades, adaptándose al vocabulario específico de la organización y a las nuevas
tácticas de los spammers.
Sin embargo, los spammers han desarrollado técnicas para engañar a estos filtros, conocidas
como:




Bloque IV - Punto 3                           51 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Ensalada de palabras (Word Salad/Dictionary Salad): Inclusión de grandes bloques de
      palabras aleatorias o texto legítimo invisible para diluir la probabilidad de spam de las
      palabras clave prohibidas.
    • Ataques de palabras buenas (Good Word Attacks): Inserción deliberada de palabras que
      típicamente tienen una alta probabilidad de ser ham para sesgar el cálculo bayesiano hacia
      la legitimidad.
Para superar las limitaciones del modelo “ingenuo” y estos ataques, se han propuesto modelos
más avanzados como el Filtrado Markoviano, que considera la secuencia y relación entre palabras
adyacentes, logrando mayor precisión a costa de mayor carga computacional.

1.5.3.4. Probables focos de examen

En el contexto de la oposición a TAI, es fundamental dominar los siguientes aspectos:
  1. Naturaleza del Filtro:
       • Identificar que es un filtro basado en contenido y estadístico (probabilístico), a
         diferencia de las listas negras (RBL) que se basan en la reputación de la IP.
       • Saber que requiere entrenamiento (aprendizaje supervisado) para funcionar
         eficazmente.
  2. Concepto de Falso Positivo:
       • Entender que un filtro bayesiano mal entrenado puede clasificar correo legítimo como
         spam (falso positivo), lo cual es más crítico en entornos corporativos que dejar pasar
         spam (falso negativo).
  3. Software Relacionado:
       • Asociar SpamAssassin como la herramienta de código abierto más emblemática que
         implementa clasificadores Naïve Bayes (junto con reglas heurísticas).
       • Otros nombres relevantes: Bogofilter, SpamBayes.
  4. Terminología Específica:
       • Ham: Correo legítimo (no spam).
       • Token: Unidad básica de análisis (palabra).
       • Bayes Ingenuo (Naïve): Asunción de independencia entre palabras.

1.6. Administración y mantenimiento
Esta sección cierra el bloque de correo electrónico enfocándose en la operativa diaria y la
continuidad del servicio. Un servidor de correo no es un sistema estático; es un entorno dinámico
donde miles de transacciones de entrada y salida ocurren constantemente, consumiendo recursos
y generando registros de actividad que requieren supervisión constante.
La administración y el mantenimiento se centran en garantizar la disponibilidad y la integridad
del sistema a largo plazo. Esto implica pasar de una postura reactiva (arreglar lo que se rompe)
a una proactiva (detectar anomalías antes de que afecten al servicio). El administrador debe
vigilar el flujo de mensajes para evitar atascos, asegurar que el espacio en disco no se agote por la
acumulación de correos y disponer de mecanismos de recuperación ante desastres.
A continuación, se describen las cuatro áreas críticas de gestión que componen este apartado:




Bloque IV - Punto 3                           52 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios



Área de Gestión                 Descripción                        Impacto en el Servicio

Gestión de Colas                Monitorización de los estados      Evita retrasos en la entrega y
                                del mensaje (activa, diferida,     detecta bucles de envío o
                                en espera).                        ataques masivos.
Logs y Monitorización           Análisis de los registros del      Permite la auditoría forense, el
                                sistema (mail.log, syslog).        rastreo de mensajes perdidos y
                                                                   la detección de errores.
Cuotas de Usuario               Limitación del espacio de          Previene que un solo usuario
                                almacenamiento por buzón.          sature el disco duro,
                                                                   bloqueando el servicio para
                                                                   todos.
Copias de Seguridad             Respaldo de configuraciones y      Garantiza la recuperación de
                                buzones de usuario.                datos ante fallos de hardware
                                                                   o corrupción de ficheros.


Sin una política de mantenimiento adecuada, incluso el servidor mejor configurado degradará su
rendimiento con el tiempo debido a la fragmentación, el crecimiento incontrolado de logs o la
acumulación de correos “rebotados” en las colas de espera.

1.6.1. Gestión de colas de correo

El sistema de colas (mail queue) es el mecanismo fundamental que permite el funcionamiento
asíncrono y robusto del correo electrónico (arquitectura store-and-forward). Cuando un MTA no
puede entregar un mensaje inmediatamente (por fallo en la resolución DNS, carga del sistema,
o indisponibilidad del destino), este se almacena en un directorio de “spool” para ser procesado
posteriormente por los “corredores de cola” (queue runners).
En entornos de producción, la gestión eficiente de la cola es crítica para evitar el colapso del
servidor ante picos de tráfico o ataques de denegación de servicio.

1.6.1.1. Estructura y Archivos de la Cola

La ubicación estándar del directorio de colas es /var/spool/mqueue. En sistemas de alto
rendimiento, es común dividir esta cola en múltiples subdirectorios o grupos de colas (Queue
Groups) para mejorar el paralelismo y el acceso al disco.
Un mensaje en la cola no es un único fichero monolítico. El sistema (específicamente en
arquitecturas tipo Sendmail, referencia histórica y técnica principal) descompone el mensaje en
varios archivos que comparten un identificador único (ID). Los tipos de archivo más relevantes
para el examen son:




Bloque IV - Punto 3                         53 de 164                               January 31, 2026
                            Correo electrónico. Contenedores y microservicios



Prefijo                              Nombre Técnico                      Contenido y Función

qf                                   Queue Control File                  Contiene la información de
                                                                         control: remitente,
                                                                         destinatarios, cabeceras y
                                                                         prioridad. Es el “cerebro” del
                                                                         envío.
df                                   Data File                           Contiene el cuerpo del
                                                                         mensaje. El contenido real que
                                                                         se va a transmitir.
xf                                   Transcript File                     Fichero temporal que registra
                                                                         la sesión o transacción actual
                                                                         (logs de errores SMTP) durante
                                                                         el intento de entrega.
hf                                   Held/Quarantined File               Variante del fichero qf para
                                                                         mensajes que han sido puestos
                                                                         en cuarentena y no deben
                                                                         procesarse automáticamente.
tf                                   Temporary File                      Imagen temporal del qf
                                                                         utilizada durante la
                                                                         reconstrucción de la cola.


      Nota Técnica: El ID del mensaje suele tener el formato ttYMDhmsNNppppp, donde se
      codifica la fecha, hora y el PID del proceso, garantizando unicidad.

1.6.1.2. Priorización y Orden de Procesamiento

Contrario a la intuición, los mensajes en la cola no siempre se procesan en orden de llegada (FIFO).
El servidor asigna una prioridad a cada mensaje para determinar el orden de procesamiento. Un
valor de prioridad más bajo indica una mayor urgencia (se procesa antes).
La fórmula de cálculo de la prioridad inicial es un foco técnico importante:


                 𝑃𝑟𝑖𝑜𝑟𝑖𝑑𝑎𝑑 = 𝑇 𝑎𝑚𝑎𝑜 − (𝐶𝑙𝑎𝑠𝑒 × 𝐶𝑙𝑎𝑠𝑠𝐹𝑎𝑐𝑡𝑜𝑟) + (𝑅𝑒𝑐𝑒𝑝𝑡𝑜𝑟𝑒𝑠 × 𝑅𝑒𝑐𝑖𝑝𝑖𝑒𝑛𝑡𝐹𝑎𝑐𝑡𝑜𝑟)
     • Tamaño (msgsize): Los mensajes grandes tienen una prioridad base más alta (se penalizan)
       para no bloquear mensajes pequeños.
     • Clase (class): Valor derivado de la cabecera Precedence: (ej. “urgent”, “bulk”). Una
       precedencia alta resta valor, mejorando la prioridad.
     • Receptores (nrcpt): Un alto número de destinatarios aumenta el valor, penalizando el
       mensaje.
Además, cada vez que falla un intento de entrega, se suma el valor de RetryFactor a la prioridad,
lo que retrasa progresivamente los mensajes problemáticos para no saturar los recursos.

1.6.1.3. Comandos de Administración

El administrador dispone de herramientas para inspeccionar y manipular el flujo de la cola.


Bloque IV - Punto 3                               54 de 164                                January 31, 2026
                        Correo electrónico. Contenedores y microservicios


1. Visualización (mailq) El comando mailq (o sendmail -bp) imprime el estado actual de la cola.
    • Muestra: ID de cola, tamaño, fecha de entrada, remitente y destinatarios.
    • Si un mensaje está bloqueado, suele mostrar la razón (ej. “Connection refused”, “MX lookup
      failed”).
2. Procesamiento Forzado (-q) Aunque el demonio procesa la cola periódicamente (definido por
el intervalo -q, ej. -q30m para 30 minutos), el administrador puede forzar ejecuciones manuales o
selectivas:
    • sendmail -q: Procesa toda la cola inmediatamente.
    • sendmail -qI<ID>: Procesa solo el mensaje con el ID especificado (útil para desatascar un
      correo urgente).
    • sendmail -qR<string>: Procesa mensajes cuyos destinatarios contengan la cadena (ej. -
      qRgmail.com para forzar la salida a Gmail).
    • sendmail -qS<string>: Procesa mensajes de un remitente específico.
3. Gestión de Cuarentena Los mensajes sospechosos pueden ser puestos en cuarentena
(renombrando qf a hf). Para liberar o procesar estos elementos se usa el flag -Q.

1.6.1.4. Control de Carga y Rendimiento (Tuning)

Para evitar que el servidor colapse bajo carga, se configuran parámetros de “Load Limiting” que
alteran el comportamiento de la cola según la carga del sistema (Load Average):
  1. QueueLA (Queue Load Average): Si la carga del sistema supera este valor, el servidor deja de
     entregar correo inmediatamente y solo lo encola (pasa a modo queue-only).
        • Lógica: Carga > QueueLA → Encolar, no entregar.
  2. RefuseLA (Refuse Load Average): Si la carga supera este umbral crítico, el servidor rechaza
     nuevas conexiones SMTP entrantes (normalmente con un error temporal 4xx) para
     protegerse.
        • Lógica: Carga > RefuseLA → Rechazar conexión.
  3. Tiempos de Vida (Timeouts):
        • Timeout.queuereturn: Tiempo máximo que un mensaje permanece en cola antes de ser
          devuelto al remitente como fallido (bounced). El valor estándar recomendado es 5 días
          (5d).
        • Timeout.queuewarn: Tiempo tras el cual se envía una notificación al remitente avisando
          que su mensaje sigue retrasado (ej. 4 horas).



1.6.1.5. Probables focos de examen

    • Diferencia de archivos: Distinguir entre el archivo de control (qf - cabeceras/sobre) y el
      archivo de datos (df - cuerpo del mensaje).
    • Significado de Prioridad: Recordar que en la gestión de colas, un valor numérico más bajo
      significa mayor prioridad (se procesa antes).
    • Comandos de filtrado: Preguntas sobre cómo forzar el envío de correos a un dominio
      específico (uso de -qR).
    • Parámetros de carga: Diferenciar entre QueueLA (sigue aceptando correo pero lo encola) y
      RefuseLA (rechaza la conexión entrante).
    • Directorio estándar: Identificar /var/spool/mqueue como la ruta por defecto.



Bloque IV - Punto 3                         55 de 164                             January 31, 2026
                           Correo electrónico. Contenedores y microservicios


1.6.2. Logs y monitorización

La capacidad de registrar eventos (logging) y monitorizar el estado del servicio en tiempo real es
una competencia crítica para el administrador de correo. Estos registros no solo son herramientas
de diagnóstico ante fallos, sino evidencias legales y de seguridad imprescindibles para la auditoría
forense y la detección de intrusiones.
En sistemas Unix/Linux, la gestión de logs de correo se delega casi universalmente en el demonio
del sistema Syslog (o sus variantes modernas como rsyslog o syslog-ng), utilizando la facilidad
(facility) denominada mail o LOG_MAIL.

1.6.2.1. Niveles y Arquitectura de Logging (Sendmail/Postfix)

El control de la granularidad de los logs se define mediante niveles de severidad. Es fundamental
para el examen conocer la escala estándar utilizada por Sendmail y heredada conceptualmente
por otros MTAs.
1. Configuración en Sendmail (LogLevel) El parámetro LogLevel (opción O LogLevel=n en
sendmail.cf) controla el detalle. Los niveles se organizan jerárquicamente:


Nivel                              Descripción y Uso                  Relevancia para el Examen

0-1                                Fallos críticos del sistema y      Mínimo absoluto.
                                   problemas de seguridad
                                   graves.
9                                  Nivel por defecto. Registra        Estándar recomendado por
                                   deferrals (retrasos), fallos de    fabricantes como ArcSight y
                                   entrega y estadísticas básicas.    Sendmail.
12                                 Registra todas las conexiones      Útil para trazabilidad de
                                   SMTP.                              conexiones.
15                                 Registra todos los comandos        Usado para depuración
                                   SMTP entrantes y salientes.        profunda. Genera gran
                                                                      volumen de datos.
>64                                Reservado para depuración de       No usar en producción.
                                   código extremadamente
                                   verbosa.


2. Configuración en Postfix Postfix envía sus mensajes a /var/log/mail.log (o maillog en
sistemas Red Hat). Además, permite separar errores y advertencias en /var/log/mail.err y
/var/log/mail.warn respectivamente.

      • Incremento de verbosidad:
          – Para aumentar el detalle de un demonio específico (ej. smtp o smtpd), se debe editar el
            archivo /etc/postfix/master.cf añadiendo la bandera -v al final de la línea del proceso.
          – Ejemplo: smtp unix - - - - - smtp -v
      • Depuración específica:
          – debug_peer_list: Permite activar el modo verbose solo para IPs o dominios específicos
            que están dando problemas, evitando inundar los logs con todo el tráfico.


Bloque IV - Punto 3                            56 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


         – smtpd_tls_loglevel: Controla específicamente la traza de la negociación TLS (valores
           1 a 4).

1.6.2.2. Monitorización en Tiempo Real y Herramientas

El administrador debe conocer las herramientas de línea de comandos para la inspección
inmediata y los protocolos para la gestión remota.
1. Visualización de Logs en Unix/Linux
    • tail -f: El comando por excelencia para monitorizar los logs en tiempo real a medida que
      se escriben.
         – Sintaxis: tail -f /var/log/mail.log.
         – Permite ver la transacción SMTP “en vivo” para diagnosticar rechazos o errores de
           conexión.
2. Protocolo SNMP (Simple Network Management Protocol) SNMP es el estándar para la gestión
y monitorización de dispositivos de red y servidores.
    • Arquitectura: Se basa en un Gestor (NMS) y un Agente (en el servidor de correo) que
      intercambian información definida en una MIB (Management Information Base).
    • Operaciones:
         – GET/GETBULK: El gestor solicita información al agente (polling).
         – SET: El gestor modifica una configuración en el agente.
         – TRAP: El agente envía una notificación asíncrona al gestor ante un evento crítico (ej.
           “Cola de correo llena” o “Servicio caído”).
    • Versiones:
         – SNMPv1/v2c: Transmiten comunidades (contraseñas) en texto claro. Vulnerables.
         – SNMPv3: Introduce autenticación robusta y cifrado (AES/DES), siendo el estándar
           recomendado para seguridad.
3. Monitorización en Microsoft Exchange Exchange utiliza una arquitectura diferente basada en
logs transaccionales y el Visor de Eventos de Windows.
    • Transaction Logs: Registran cada operación antes de que se confirme en la base de datos
      (.edb). Son críticos para la recuperación ante desastres y para mantener la integridad ACID.
      No se deben borrar manualmente; se purgan automáticamente tras un backup completo.
    • Message Tracking Logs: Permiten rastrear el flujo de un mensaje específico a través de la
      organización (remitente, destinatario, hora, estado).

1.6.2.3. Probables focos de examen

En las pruebas para TAI, las preguntas sobre logs suelen centrarse en la identificación de comandos,
niveles de severidad y protocolos de gestión.
1.6.2.3.1. Identificación de Niveles de Log
    • Pregunta frecuente: “¿Qué nivel de log en Sendmail permite registrar todos los comandos
      SMTP para depuración?”.
    • Respuesta: Nivel 15.
    • Es importante saber que el nivel por defecto es 9.
1.6.2.3.2. Comandos de Monitorización
    • Asociar el comando tail -f con la visualización en tiempo real de ficheros de log.


Bloque IV - Punto 3                           57 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Conocer que para aumentar la verbosidad en Postfix se usa la bandera -v en el archivo
      master.cf.

1.6.2.3.3. Conceptos de SNMP
    • Definición de TRAP: Notificación asíncrona enviada por el agente al gestor sin solicitud
      previa.
    • Puertos estándar: 161 (Polling/Consultas) y 162 (Traps).
    • Seguridad: SNMPv3 es la única versión que ofrece cifrado y autenticación fuerte.
1.6.2.3.4. Logs Transaccionales en Bases de Datos (Exchange)
    • Comprender que el Transaction Log es vital para la consistencia y recuperación de la base
      de datos ante fallos, y no es un simple archivo de texto para lectura humana como en Unix.
1.6.2.3.5. Herramientas de Monitorización
    • Identificar herramientas como Nagios como software de monitorización de infraestructuras
      basado en sondas y alertas.

1.6.3. Cuotas de almacenamiento

La gestión de cuotas de almacenamiento es un mecanismo crítico en la administración de
servidores de correo para garantizar la disponibilidad del servicio y evitar la denegación de
servicio (DoS) por agotamiento del espacio en disco. Las cuotas limitan la cantidad de datos o el
número de inodos (archivos) que un usuario puede almacenar en su buzón.

1.6.3.1. Tipos de implementación de cuotas

Existen dos enfoques principales para implementar cuotas, dependiendo de si los usuarios del
correo son usuarios del sistema operativo o usuarios virtuales.
1. Cuotas de Sistema de Ficheros (Filesystem Quotas) Son gestionadas directamente por el kernel
del sistema operativo sobre el sistema de archivos (ej. ext4, XFS).
    • Funcionamiento: Se aplican sobre el UID (User ID) o GID (Group ID) del sistema.
    • Caso de uso: Ideales cuando los usuarios de correo tienen cuentas reales en el servidor Linux
      (/etc/passwd) y su correo reside en su directorio $HOME.
    • Limitación crítica: No funcionan adecuadamente con usuarios virtuales (donde todos
      los correos de un dominio pertenecen al mismo UID, por ejemplo, el usuario vmail), ya que
      el sistema operativo no puede distinguir entre los buzones individuales de los usuarios
      virtuales.
    • Herramientas: quota, edquota, repquota, xfs_quota.
2. Cuotas de Aplicación (Application/Virtual Quotas) Son gestionadas por el software MDA
(como Dovecot) o el servidor de correo (como Exchange).
    • Funcionamiento: El software lleva un registro del uso de espacio, independientemente de
      los permisos del sistema de archivos subyacente.
    • Maildir++: Es una extensión del formato Maildir utilizada frecuentemente (por Dovecot,
      Courier) para soportar cuotas en usuarios virtuales. Almacena el tamaño actual del buzón
      en un fichero oculto (ej. maildirsize) dentro del directorio del usuario, permitiendo un
      cálculo rápido sin recorrer todo el árbol de directorios.
    • Integración: Dovecot puede consultar y aplicar límites definidos en bases de datos externas
      o directorios LDAP.


Bloque IV - Punto 3                          58 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


1.6.3.2. Conceptos de Límites: Soft vs. Hard

Tanto en cuotas de sistema como de aplicación, se definen dos umbrales clave que determinan el
comportamiento del sistema ante la saturación:


Tipo de Límite                  Descripción                        Comportamiento

Soft Limit (Límite Blando)      Umbral de advertencia.             El usuario puede exceder este
                                                                   límite temporalmente durante
                                                                   un periodo de gracia (grace
                                                                   period). Se suelen generar
                                                                   avisos al usuario.
Hard Limit (Límite Duro)        Umbral absoluto.                   El sistema impide físicamente
                                                                   la escritura de nuevos datos
                                                                   una vez alcanzado. En correo,
                                                                   esto provoca un rechazo
                                                                   inmediato del mensaje
                                                                   entrante.


1.6.3.3. Configuración en Servidores Principales

1. Dovecot (MDA) Dovecot permite una gestión granular, pudiendo monitorizar cuotas
individualmente y enviar advertencias automáticas a los usuarios cuando alcanzan porcentajes
críticos de ocupación (ej. al 80% o 95%).
    • Soporta el backend dict para almacenar cuotas en SQL o Redis, o el backend maildir para
      usar el archivo maildirsize (Maildir++).
2. Microsoft Exchange Exchange maneja las cuotas a nivel de base de datos o de buzón individual
mediante tres parámetros escalonados:
  1. Emitir advertencia: Envía un correo al usuario.
  2. Prohibir envío: El usuario puede recibir pero no enviar.
  3. Prohibir envío y recepción: El buzón deja de funcionar por completo.

1.6.3.4. Probables focos de examen

En las oposiciones a TAI, las preguntas sobre cuotas suelen centrarse en el comportamiento ante
la saturación y las diferencias técnicas de implementación.
  1. Consecuencia de buzón lleno:
        • Si un buzón supera su Hard Limit (o la capacidad máxima definida, ej. 500 MB), el
          servidor no aceptará nuevos mensajes.
        • El remitente recibirá un mensaje de rebote (NDR - Non-Delivery Report) con un código
          de error permanente (generalmente 5.2.2 Mailbox full).
  2. Cuotas para Usuarios Virtuales:
        • Pregunta técnica: “¿Es posible usar cuotas de sistema (quota del kernel) para limitar
          buzones de usuarios virtuales que comparten el mismo UID?”.
        • Respuesta: No (o no de forma efectiva individualmente). Se deben usar cuotas de
          aplicación (como Maildir++ o plugins de dict en Dovecot).
  3. Periodo de Gracia (Grace Period):

Bloque IV - Punto 3                         59 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


       • Entender que el Grace Period aplica solo cuando se supera el Soft Limit. Si expira el
         tiempo y el usuario sigue por encima del Soft Limit, este se convierte en Hard Limit y se
         bloquea la escritura.
  4. Formatos de Almacenamiento:
       • Relacionar Maildir++ con la gestión eficiente de cuotas en sistemas de ficheros que
         alojan miles de usuarios, evitando la sobrecarga de calcular el tamaño de directorio (du)
         en cada entrega.
  5. Herramientas de línea de comandos (Linux):
       • repquota -a: Reporte de uso de cuotas de todos los sistemas de archivos.
       • edquota -u [usuario]: Editar los límites soft/hard de un usuario.
       • xfs_quota: Herramienta específica para sistemas de ficheros XFS.

1.6.4. Copias de seguridad

La realización de copias de seguridad (backups) es la medida fundamental para garantizar la
disponibilidad e integridad de los datos frente a fallos de hardware, errores humanos, corrupción
de software o desastres naturales. En la administración de servidores de correo, una estrategia de
respaldo efectiva debe considerar no solo los buzones de los usuarios, sino también las bases de
datos de configuración, logs de transacciones y certificados de seguridad.

1.6.4.1. Conceptos Métricos Fundamentales: RTO y RPO

Para diseñar una política de copias de seguridad adecuada, el administrador debe definir dos
parámetros críticos de negocio:
    • RTO (Recovery Time Objective): Es el tiempo máximo tolerable que el servicio puede estar
      interrumpido tras un desastre. Determina la urgencia de la restauración.
    • RPO (Recovery Point Objective): Es la cantidad máxima de datos (medida en tiempo) que
      la organización tolera perder. Por ejemplo, un RPO de 4 horas implica que las copias deben
      realizarse al menos cada 4 horas. La frecuencia de los backups impacta directamente en el
      RPO: a mayor frecuencia, menor pérdida de datos.

1.6.4.2. Tipos de Copias de Seguridad y Estrategias de Rotación

La elección del tipo de copia afecta tanto al consumo de almacenamiento como a la velocidad de
restauración.
1. Tipos de Copia:


Tipo de Copia            Descripción Técnica      Ventajas                   Desventajas

Completa (Full)          Copia la totalidad de    Restauración más           Alto consumo de
                         los datos                rápida y sencilla (solo    espacio y tiempo de
                         seleccionados,           se necesita el último      ejecución largo.
                         independientemente       Full).
                         de si han cambiado o
                         no.




Bloque IV - Punto 3                          60 de 164                              January 31, 2026
                           Correo electrónico. Contenedores y microservicios



Tipo de Copia              Descripción Técnica      Ventajas                   Desventajas

Incremental                Copia solo los datos     Backup muy rápido y        Restauración lenta:
                           modificados desde el     mínimo espacio.            requiere el último Full
                           último backup                                       + todos los
                           realizado (ya sea                                   incrementales
                           completo o                                          secuenciales.
                           incremental).
Diferencial                Copia todos los datos    Restauración               El tamaño de la copia
                           modificados desde el     moderada: requiere el      crece
                           último backup            último Full + el último    progresivamente
                           COMPLETO.                Diferencial.               hasta el siguiente Full.


2. Estrategias de Rotación: El esquema más común es el GFS (Grandfather-Father-Son) o Abuelo-
Padre-Hijo, que permite mantener un histórico de versiones eficiente:
    • Hijo (Diario): Copias incrementales o diferenciales (retención corta, ej. 2 semanas).
    • Padre (Semanal): Copia completa semanal (retención media, ej. 4 semanas).
    • Abuelo (Mensual): Copia completa mensual (retención larga/archivado).

1.6.4.3. Copias de Seguridad en Microsoft Exchange

Exchange Server utiliza una arquitectura de base de datos transaccional que requiere métodos de
respaldo “conscientes de la aplicación” (application-aware). No basta con copiar los archivos .edb
o .log a nivel de sistema de archivos mientras el servicio está activo.
  1. Dependencia de VSS (Volume Shadow Copy Service): Para realizar una copia consistente
     sin detener el servicio, es imprescindible utilizar el servicio VSS de Windows. VSS congela
     las operaciones de escritura momentáneamente para crear una “instantánea” (snapshot)
     estable de la base de datos, permitiendo que el backup copie los datos mientras Exchange
     sigue atendiendo peticiones.
  2. Gestión de Logs de Transacciones:
          • En Exchange, los datos se escriben primero en archivos de registro (logs) y luego en la
            base de datos.
          • Una Copia Completa (Full) realiza el truncamiento (purga) de los logs de transacciones
            antiguos tras confirmar que la base de datos se ha respaldado correctamente.
          • Circular Logging: Si está habilitado el “registro circular”, Exchange sobrescribe los logs
            automáticamente para ahorrar espacio. Esto impide realizar copias incrementales o
            diferenciales efectivas, ya que se pierde el historial de cambios necesario.
  3. Recuperación: Exchange permite la creación de una Base de Datos de Recuperación (RDB),
     una base de datos especial que permite montar una copia de seguridad restaurada y extraer
     datos de buzones específicos sin perturbar el acceso de los usuarios a la base de datos de
     producción actual.

1.6.4.4. Deduplicación y Seguridad del Backup

    • Deduplicación: Tecnología esencial en sistemas de correo donde múltiples usuarios reciben
      el mismo adjunto. El software de backup (como Bacula Enterprise) divide los datos en bloques

Bloque IV - Punto 3                            61 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      (chunks) y calcula un hash. Si el bloque ya existe en el almacenamiento, solo se guarda un
      puntero, reduciendo drásticamente el espacio necesario.
    • Cifrado: Para cumplir con normativas de protección de datos y el Esquema Nacional
      de Seguridad (ENS), los soportes de respaldo (cintas, discos externos, nube) deben estar
      cifrados. Esto asegura que la pérdida física del medio no comprometa la confidencialidad de
      la información.

1.6.4.5. Probables focos de examen

  1. Diferencia Incremental vs. Diferencial (Restauración):
        • Pregunta clásica: “¿Qué secuencia de cintas/archivos se necesita para restaurar el
          sistema tras un fallo el jueves, si se hace un Full el domingo?”.
        • Incremental: Full (Dom) + Inc (Lun) + Inc (Mar) + Inc (Mié). (Más cintas, más lento).
        • Diferencial: Full (Dom) + Diff (Mié). (Menos cintas, más rápido).
  2. Papel de VSS en Exchange:
        • Identificar que VSS es el mecanismo que permite hacer copias de seguridad “en caliente”
          (online) garantizando la consistencia de la base de datos Exchange. Copiar los archivos
          .edb abiertos directamente sin VSS resulta en copias corruptas.
  3. Truncado de Logs en Exchange:
        • Saber que la Copia Completa (Full) es la encargada de purgar (truncar) los logs de
          transacciones acumulados en el servidor Exchange para liberar espacio en disco.
  4. Definiciones RTO/RPO:
        • Asociar RPO con la pérdida de datos admisible (tiempo hacia atrás) y RTO con el tiempo
          de inactividad admisible (tiempo hacia adelante).
  5. Regla 3-2-1:
        • Aunque es un concepto general, suele preguntarse: 3 copias de los datos, en 2 medios
          diferentes, 1 de ellas fuera de la sede (offsite).




Bloque IV - Punto 3                          62 de 164                            January 31, 2026
                        Correo electrónico. Contenedores y microservicios



2. Administración de contenedores

2.1. Introducción a la contenedorización
Esta sección establece las bases del segundo bloque temático, introduciendo una tecnología que
ha revolucionado la forma en que se empaqueta, distribuye y ejecuta el software en la última
década. La contenedorización soluciona el clásico problema de “funciona en mi máquina pero no
en producción”, proporcionando un entorno predecible y aislado para las aplicaciones.
La contenedorización es una forma de virtualización a nivel de sistema operativo que permite
empaquetar una aplicación junto con todas sus dependencias (librerías, archivos de configuración
y binarios) en una unidad estandarizada llamada “contenedor”. A diferencia de la virtualización
tradicional, que emula un hardware completo para ejecutar un sistema operativo invitado
completo, los contenedores comparten el núcleo (kernel) del sistema operativo anfitrión, pero se
ejecutan en espacios de usuario aislados. Esta diferencia arquitectónica los hace extremadamente
ligeros y portátiles.
Mientras que las máquinas virtuales (VM) abstraen el hardware físico, los contenedores abstraen
el sistema operativo. Esto permite ejecutar múltiples contenedores sobre una misma máquina con
un consumo de recursos significativamente menor y una velocidad de arranque casi instantánea.
Entender esta tecnología es fundamental para la administración moderna de sistemas, ya que es
la base sobre la que se construyen las arquitecturas de microservicios y las metodologías DevOps.
A continuación, se presenta una tabla comparativa fundamental para distinguir los dos modelos
de virtualización que conviven en los centros de datos actuales:

Característica                  Máquinas Virtuales (VM)            Contenedores

Abstracción                     Hardware (mediante                 Sistema Operativo (mediante
                                Hipervisor).                       Motor de Contenedores).
Sistema Operativo               Cada VM tiene su propio SO         Comparten el kernel del SO
                                completo (Guest OS).               anfitrión.
Tamaño en disco                 Pesado (Gigabytes).                Ligero (Megabytes).
Tiempo de arranque              Lento (minutos para iniciar el     Muy rápido (segundos o
                                SO).                               milisegundos).
Aislamiento                     Total (fuerte aislamiento de       Procesos aislados (menor
                                seguridad).                        aislamiento por defecto).


El uso de contenedores no busca reemplazar completamente a las máquinas virtuales, sino
complementarlas. Son ideales para escenarios donde se requiere alta densidad de aplicaciones,
escalabilidad rápida y ciclos de desarrollo ágiles (CI/CD), permitiendo a los administradores
desplegar actualizaciones de software de manera consistente en cualquier infraestructura, ya sea
un servidor físico local o una instancia en la nube.

2.1.1. Concepto y ventajas de los contenedores

El concepto de contenedor representa una evolución fundamental en la virtualización, pasando
de la abstracción del hardware (máquinas virtuales) a la abstracción del espacio de usuario y
sistema operativo.

Bloque IV - Punto 3                         63 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.1.1.1. Definición y naturaleza técnica

La contenedorización se define técnicamente como una forma de virtualización a nivel
de sistema operativo. Esta tecnología permite la ejecución de múltiples unidades aisladas,
denominadas contenedores, sobre un único host de control y compartiendo el mismo kernel.
A diferencia de una máquina virtual (VM), un contenedor no es una entidad física simulada ni
incluye un sistema operativo invitado completo. Es una construcción lógica que empaqueta una
aplicación junto con todas sus dependencias (binarios, librerías, archivos de configuración) para
garantizar su funcionamiento autónomo y uniforme.
Desde una perspectiva arquitectónica, los contenedores son posibles gracias a tres tecnologías
fundamentales del kernel de Linux:
  1. Namespaces (Espacios de nombres): Proporcionan el aislamiento de la vista del sistema.
     Cada contenedor tiene su propia visión de los procesos, redes, usuarios y montajes,
     impidiendo que vea o afecte a otros contenedores o al host.
  2. Cgroups (Grupos de control): Gestionan, limitan y auditan el uso de recursos físicos (CPU,
     memoria, E/S de disco) para evitar que un contenedor monopolice el sistema.
  3. Union File Systems (Sistemas de archivos de unión): Permiten la construcción de imágenes
     mediante capas inmutables y eficientes, utilizando estrategias como Copy-on-Write para
     optimizar el almacenamiento.

2.1.1.2. Ventajas del modelo de contenedores

La adopción de contenedores ofrece beneficios significativos tanto para el desarrollo de software
(Dev) como para las operaciones (Ops), resolviendo ineficiencias de la virtualización tradicional.
Tabla comparativa de ventajas técnicas y operativas


Ventaja                          Descripción Técnica                Impacto en el Sistema

Eficiencia de Recursos           Los contenedores comparten         Mayor densidad de carga por
                                 el kernel del host, eliminando     servidor físico y reducción del
                                 la sobrecarga de ejecutar          consumo de RAM y CPU.
                                 múltiples sistemas operativos
                                 invitados.
Velocidad de Arranque            Al ser procesos del sistema y      Escalado horizontal casi
                                 no requerir el inicio de un SO     instantáneo ante picos de
                                 completo, arrancan en              demanda.
                                 milisegundos.
Portabilidad                     Empaquetado autocontenido         Elimina el problema de
                                 de la aplicación y sus            “funciona en mi máquina”;
                                 dependencias (paradigma           consistencia garantizada entre
                                 Build, Ship, Run).                desarrollo, pruebas y
                                                                   producción.
Inmutabilidad                    Las imágenes de contenedor         Facilita las reversiones
                                 son de solo lectura; para          (rollbacks), la recuperación
                                 actualizar, se reemplaza el        ante desastres y la
                                 contenedor, no se modifica.        predictibilidad del despliegue.


Bloque IV - Punto 3                          64 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Ventaja                           Descripción Técnica               Impacto en el Sistema

Aislamiento Lógico                Uso de Namespaces para            Seguridad multitenant y
                                  segregar procesos, redes y        prevención de conflictos entre
                                  sistemas de archivos.             librerías o versiones de
                                                                    software.


2.1.1.3. El ciclo de vida y la inmutabilidad

Un concepto clave en la ventaja de los contenedores es su naturaleza efímera e inmutable. Se
recomienda operar los contenedores como entidades sin estado (stateless). Si un contenedor
necesita ser actualizado, se destruye y se reemplaza por uno nuevo generado desde una imagen
actualizada, en lugar de parchearlo en caliente.
Esta característica obliga a desacoplar los datos de la aplicación. La persistencia de datos no debe
depender del sistema de archivos del contenedor (que desaparece al destruirse), sino de volúmenes
externos o bases de datos, garantizando la integridad de la información a través del ciclo de vida
del contenedor.

2.1.1.4. Probables Focos de Examen

En las preguntas de examen para TAI, es frecuente que se evalúen los matices técnicos que
diferencian un contenedor de un simple proceso o de una máquina virtual.
    • Kernel Compartido vs. Kernel Propio: Es fundamental recordar que todos los contenedores
      en un host comparten el mismo kernel. Si el kernel del host falla, todos los contenedores
      fallan. Esto es una diferencia crítica de seguridad y arquitectura frente a las VMs.
    • Funciones de Cgroups vs. Namespaces:
         – Si la pregunta se refiere a “aislamiento” o “visión del sistema” (qué puede ver el
           contenedor), la respuesta es Namespaces.
         – Si la pregunta se refiere a “recursos”, “límites” o “cuotas” (cuánto puede usar el
           contenedor), la respuesta es Cgroups.
    • Copy-on-Write (CoW): Se suele preguntar por el mecanismo de ahorro de espacio. Los
      contenedores comparten capas de imagen de solo lectura y solo escriben en una capa superior
      delgada y efímera. Esto optimiza el almacenamiento y el inicio.
    • Diferencia Imagen/Contenedor: La imagen es la plantilla estática (clase en POO); el
      contenedor es la instancia en ejecución (objeto en POO).

2.1.2. Diferencias entre contenedores y máquinas virtuales

La distinción entre contenedores y máquinas virtuales (VM) es fundamental en la arquitectura
de sistemas modernos. Ambas tecnologías permiten que múltiples aplicaciones compartan una
misma infraestructura física, pero difieren drásticamente en el nivel de abstracción y en cómo
aíslan los recursos.

2.1.2.1. Nivel de abstracción y arquitectura

La diferencia principal radica en qué capa del sistema se virtualiza:
  1. Máquinas Virtuales (Hardware Virtualization): Se basan en un hipervisor (monitor de
     máquina virtual) que simula un entorno de hardware completo. Cada VM incluye su propio

Bloque IV - Punto 3                            65 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      sistema operativo invitado (Guest OS) completo, además de los binarios, librerías y la
      aplicación. Esto permite ejecutar sistemas operativos diferentes al del host (por ejemplo,
      Windows sobre un servidor Linux).
  2. Contenedores (OS-level Virtualization): Se ejecutan sobre un motor de contenedores (como
     Docker Engine). No simulan hardware ni incluyen un sistema operativo completo. En su
     lugar, todos los contenedores comparten el mismo kernel del sistema operativo anfitrión.
     El contenedor es, en esencia, un proceso aislado en el espacio de usuario que empaqueta la
     aplicación y sus dependencias.

2.1.2.2. Comparativa técnica de rendimiento y recursos

Debido a que los contenedores evitan la sobrecarga de ejecutar múltiples núcleos de sistema
operativo, son significativamente más ligeros y eficientes que las VMs.
Tabla comparativa: Contenedores vs. Máquinas Virtuales

Atributo                         Máquinas Virtuales (VM)            Contenedores

Abstracción                      Nivel de Hardware                  Nivel de Sistema Operativo
                                 (Hipervisor)                       (User Space)
Kernel                           Propio de cada instancia           Compartido con el host (Host
                                 (Guest Kernel)                     Kernel)
Tamaño en disco                  Grande (Gigabytes), incluye OS     Pequeño (Megabytes), solo
                                 completo                           aplicación y librerías
Tiempo de arranque               Lento (Minutos), requiere boot     Casi instantáneo
                                 del OS                             (Milisegundos)
Rendimiento                      Sobrecarga por emulación de        Nativo o casi nativo
                                 hardware
Portabilidad                     Media (depende del formato de      Alta (consistente en cualquier
                                 imagen/hipervisor)                 host con el runtime)


2.1.2.3. Aislamiento y Seguridad

Aunque los contenedores proporcionan un aislamiento efectivo mediante namespaces y cgroups,
este se considera lógico y menos robusto que el aislamiento físico/hardware que ofrece un
hipervisor.
    • Superficie de ataque: En una VM, el aislamiento es fuerte; un fallo en el Guest OS de una
      VM raramente afecta al Host. En contenedores, dado que comparten el kernel, un fallo o
      vulnerabilidad en el kernel del host puede comprometer a todos los contenedores residentes.
    • Privilegios: Por defecto, muchos procesos en contenedores se ejecutan con el UID 0 (root). Si
      un atacante logra “escapar” del contenedor (container breakout), podría obtener acceso root
      al servidor anfitrión, un riesgo mitigado pero no eliminado completamente por tecnologías
      como User Namespaces.
Debido a estas diferencias, es una práctica común en entornos empresariales desplegar
contenedores dentro de máquinas virtuales. Esto combina la densidad y agilidad de los
contenedores con la seguridad y el aislamiento de hardware de las VMs.

Bloque IV - Punto 3                          66 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.1.2.4. Probables Focos de Examen

De cara a la preparación del examen TAI, preste especial atención a las siguientes distinciones que
suelen ser objeto de pregunta tipo test:
    • El Kernel Compartido: Es el concepto más preguntado. Los contenedores no tienen su propio
      kernel; usan el del anfitrión. Las VMs sí tienen su propio kernel. Esto implica que en un host
      Linux no se pueden ejecutar contenedores nativos con kernel de Windows (requerirían una
      VM intermedia).
    • Gestión de Recursos: Las VMs requieren una asignación estática y pesada de recursos (ej.
      reservar 4GB de RAM). Los contenedores son elásticos; consumen solo lo que el proceso
      necesita en ese momento, hasta el límite impuesto por los cgroups.
    • Persistencia: Las VMs suelen tratarse como servidores duraderos (pets). Los contenedores
      están diseñados para ser efímeros e inmutables (cattle); si se necesita un cambio, se reemplaza
      el contenedor, no se actualiza internamente.
    • Concepto de “Guest OS”: Si la pregunta menciona “Sistema Operativo Invitado” (Guest OS),
      se refiere casi invariablemente a una Máquina Virtual. Los contenedores solo tienen librerías
      y binarios (user space), no un OS completo.

2.1.3. Casos de uso

La flexibilidad, ligereza y portabilidad de la tecnología de contenedores ha propiciado su adopción
masiva en la industria, trascendiendo el simple empaquetado de software para convertirse en
habilitadores de nuevas arquitecturas y metodologías de trabajo. A continuación, se detallan los
escenarios de implementación más relevantes.

2.1.3.1. Arquitectura de Microservicios

El caso de uso más extendido y nativo para los contenedores es el desarrollo de aplicaciones
basadas en microservicios. En este modelo, las aplicaciones monolíticas tradicionales se
descomponen en componentes funcionales pequeños, autónomos y desacoplados.
    • Independencia: Cada microservicio se empaqueta en su propio contenedor, lo que permite
      que diferentes equipos desarrollen, desplieguen y escalen partes específicas de la aplicación
      de forma independiente, utilizando incluso diferentes lenguajes de programación o
      versiones de librerías sin conflictos.
    • Escalabilidad Granular: A diferencia de una arquitectura monolítica donde se debe escalar
      toda la aplicación, los contenedores permiten escalar horizontalmente (scale-out) solo
      aquellos microservicios que experimentan mayor carga, optimizando el uso de recursos.

2.1.3.2. Integración y Despliegue Continuo (CI/CD)

Los contenedores actúan como la piedra angular de las canalizaciones modernas de DevOps,
facilitando la Integración Continua (CI) y el Despliegue Continuo (CD).
    • Paridad de Entornos: Al empaquetar la aplicación con todas sus dependencias (librerías,
      binarios, configuración), los contenedores garantizan la consistencia entre los entornos
      de desarrollo, pruebas y producción. Esto elimina el clásico problema de “funciona en mi
      máquina” (it works on my machine), ya que el artefacto que se prueba es idéntico, bit a bit, al
      que se despliega.
    • Agilidad: La naturaleza ligera de los contenedores permite crear y destruir entornos de
      prueba rápidamente, acelerando los ciclos de retroalimentación y la entrega de software.


Bloque IV - Punto 3                           67 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


2.1.3.3. Modernización de Aplicaciones Legadas (“Lift and Shift”)

Las organizaciones utilizan contenedores para modernizar aplicaciones antiguas sin necesidad
de reescribir todo su código fuente.
    • Estrategia Lift and Shift: Consiste en encapsular una aplicación existente tal cual está
      dentro de un contenedor para migrarla a una infraestructura moderna o a la nube. Aunque
      esta estrategia no aprovecha todas las ventajas de una arquitectura nativa de nube (como la
      elasticidad de los microservicios), simplifica la gestión, el despliegue y reduce la dependencia
      del sistema operativo subyacente.
    • Refactorización: En etapas más avanzadas, las aplicaciones legadas pueden ser
      refactorizadas parcialmente para extraer funcionalidades críticas como microservicios
      containerizados.

2.1.3.4. Computación en el Borde (Edge Computing) e IoT

Debido a su baja huella de recursos en comparación con las máquinas virtuales, los contenedores
son ideales para despliegues en dispositivos con limitaciones de hardware, conocidos como el
Borde (Edge).
    • Eficiencia: Permiten ejecutar aplicaciones complejas en dispositivos IoT o nodos de borde
      donde la CPU y la memoria son limitadas.
    • Gestión Remota: Facilitan la actualización y gestión del ciclo de vida del software en
      dispositivos distribuidos geográficamente, reduciendo la latencia al procesar datos cerca de
      la fuente.

2.1.3.5. Procesamiento de Datos y Aplicaciones Efímeras

La capacidad de los contenedores para arrancar y detenerse en milisegundos los hace perfectos
para cargas de trabajo temporales.
    • Trabajos por lotes (Batch Jobs): Tareas de procesamiento que se ejecutan bajo demanda y
      liberan los recursos inmediatamente al finalizar.
    • Ciencia de Datos e IA: Empaquetado de flujos de trabajo de Inteligencia Artificial y Machine
      Learning (ej. TensorFlow), garantizando que los modelos sean reproducibles y portables
      entre diferentes clústeres, incluidos aquellos con soporte para GPU.

2.1.3.6. Probables Focos de Examen

Para el examen de TAI, es importante distinguir los matices entre los distintos usos para responder
correctamente a preguntas de escenario.
    • Microservicios vs. Monolito: Las preguntas suelen asociar “contenedores” con
      “microservicios”. Recuerde que la ventaja clave aquí es el desacoplamiento y el escalado
      independiente de componentes.
    • Concepto de “Lift and Shift”: Si el examen plantea un escenario de “migración rápida a la
      nube sin reescribir código”, la respuesta correcta suele referirse a esta estrategia. Es una
      forma de mover aplicaciones legacy a contenedores, pero no las convierte automáticamente
      en cloud-native.
    • Entornos Consistentes: Un foco habitual es la resolución de problemas de configuración
      entre desarrollo y producción. La respuesta clave es que los contenedores garantizan
      la inmutabilidad y la paridad de entornos, solucionando inconsistencias de librerías o
      versiones.

Bloque IV - Punto 3                           68 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Efimeridad: Se debe tener claro que los contenedores son adecuados para aplicaciones
      sin estado (stateless) y tareas efímeras. Si la pregunta involucra persistencia de datos
      crítica dentro del sistema de archivos del contenedor para una base de datos a largo plazo,
      generalmente es un “anti-patrón” o requiere volúmenes externos.
Esta sección profundiza en la herramienta que democratizó el uso de contenedores y se convirtió
en el estándar de la industria. Docker no es solo un motor de ejecución, sino una plataforma
completa (PaaS) que proporciona las herramientas necesarias para empaquetar, distribuir y
gestionar aplicaciones de forma aislada y reproducible.

2.2. Docker
Docker implementa una arquitectura cliente-servidor que facilita el ciclo de vida del desarrollo
de software bajo la filosofía “Build, Ship, and Run Any App, Anywhere” (Construir, enviar y ejecutar
cualquier aplicación, en cualquier lugar). Su éxito radica en la estandarización: permite a los
desarrolladores definir entornos complejos mediante código y garantiza que estos se ejecuten
exactamente igual en un portátil de desarrollo, en un servidor de pruebas o en una instancia en la
nube.
El ecosistema de Docker se compone de varios objetos y componentes interconectados
que permiten desde la construcción de la imagen base hasta la orquestación de servicios
multicontenedor. Entender cómo interactúan el demonio de Docker (dockerd), el cliente de línea
de comandos y los registros remotos es esencial para cualquier administrador de sistemas.
A continuación, se presenta una tabla que estructura los conceptos clave que se desarrollarán en
los subapartados, clasificándolos según su función dentro del flujo de trabajo:


Componente / Concepto             Función Principal                  Analogía Técnica

Docker Engine (Daemon)            El “cerebro” que gestiona los      El servidor de base de datos.
                                  objetos de Docker en el host.
Imagen                            Plantilla de solo lectura con el   La “clase” en POO o una ISO de
                                  código y librerías.                instalación.
Contenedor                        Instancia ejecutable y aislada     El “objeto” en POO o la
                                  de una imagen.                     máquina encendida.
Dockerfile                        Script con las instrucciones       Una receta de cocina o un
                                  para crear una imagen.             Makefile.
Docker Hub / Registry             Repositorio centralizado para      GitHub (pero para
                                  almacenar y compartir              binarios/imágenes).
                                  imágenes.
Volúmenes                         Mecanismo para persistir           Un disco duro externo o
                                  datos fuera del ciclo de vida      montaje NFS.
                                  del contenedor.
Docker Compose                    Herramienta para definir y         Un director de orquesta para
                                  ejecutar aplicaciones              un grupo pequeño.
                                  multi-contenedor.




Bloque IV - Punto 3                          69 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


Para visualizar cómo interactúan estos elementos, es fundamental comprender el flujo de datos
entre el Cliente (donde el usuario escribe los comandos), el Host (donde reside el demonio y los
contenedores) y el Registro (Internet/Nube):




                                  Figure 2: Arquitectura de Docker

El dominio de Docker implica aprender a gestionar la volatilidad de los contenedores (que son
efímeros por naturaleza) frente a la necesidad de persistencia de datos (bases de datos, logs), así
como configurar las redes virtuales que permiten que los contenedores se comuniquen entre sí
sin exponer puertos innecesarios al exterior.

2.2.1. Arquitectura de Docker

La arquitectura de Docker se basa en un modelo cliente-servidor. Este diseño desacopla la interfaz
de usuario (Cliente) del proceso que ejecuta y gestiona los contenedores (Demonio), permitiendo
que ambos componentes residan en el mismo sistema o se comuniquen a través de una red.

2.2.1.1. Componentes principales

El sistema se estructura en torno a tres pilares fundamentales que interactúan entre sí:
  1. Docker Client (Cliente): Es la interfaz principal de interacción para los usuarios (CLI docker).
     Su función es enviar órdenes (como docker build, docker pull, docker run) al demonio. El
     cliente utiliza la API REST de Docker para comunicarse con el demonio a través de sockets
     UNIX o interfaces de red.
  2. Docker Host (Anfitrión): Es la máquina (física o virtual) que ejecuta el demonio de Docker y
     almacena los objetos locales (imágenes, contenedores, redes, volúmenes). Es donde ocurre el
     procesamiento real. Dentro del Host, el componente crítico es el Docker Daemon (dockerd).
  3. Docker Registry (Registro): Es el componente de almacenamiento y distribución. Funciona
     como un repositorio centralizado (público como Docker Hub o privado) donde se almacenan
     las imágenes. El demonio interactúa con el registro para descargar (pull) o subir (push)
     imágenes.




Bloque IV - Punto 3                          70 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


2.2.1.2. Estructura interna del Docker Engine

El motor de Docker no es monolítico; en versiones modernas, el demonio (dockerd) delega tareas
críticas a componentes especializados para cumplir con los estándares de la Open Container
Initiative (OCI) y mejorar la estabilidad.
Tabla de componentes internos del Engine

Componente                      Función Técnica                    Detalle Importante

dockerd                         Proceso persistente principal      Gestiona la orquestación de
                                (API Server).                      alto nivel, la API, la seguridad
                                                                   y la red. Delega la ejecución a
                                                                   containerd.

containerd                      Supervisor de ciclo de vida        Gestiona la transferencia de
                                (High-level runtime).              imágenes, el almacenamiento
                                                                   y la ejecución de contenedores.
                                                                   Es un estándar de la industria
                                                                   (CNCF).
runc                            Ejecutor de contenedores           Herramienta CLI que
                                (Low-level runtime).               interactúa directamente con el
                                                                   kernel (namespaces/cgroups)
                                                                   para crear el contenedor.
                                                                   Cumple la especificación OCI.
                                                                   Se cierra tras arrancar el
                                                                   contenedor.
containerd-shim                 Proceso intermedio (Padre del      Se sitúa entre containerd y el
                                contenedor).                       proceso del contenedor.
                                                                   Permite que el contenedor siga
                                                                   ejecutándose si el demonio se
                                                                   reinicia (daemonless
                                                                   containers).


2.2.1.3. Mecanismos de comunicación y red

La comunicación entre el Cliente y el Demonio se realiza mediante la API REST de Docker,
soportando tres canales principales:
  1. Unix Domain Socket: Es el método predeterminado y más seguro para comunicaciones
     locales. Se ubica típicamente en /var/run/docker.sock. Requiere privilegios de root o
     pertenencia al grupo docker.
  2. TCP (No encriptado): Puerto predeterminado 2375. Se utiliza para acceso remoto, pero es
     inseguro por defecto.
  3. TCP (Encriptado con TLS): Puerto predeterminado 2376. Es la forma segura de exponer el
     demonio en la red.
Adicionalmente, para gestionar el tráfico de red hacia los contenedores (Port Mapping), Docker
utiliza un proceso llamado docker-proxy (userland proxy), que redirige el tráfico del host
al contenedor, aunque también se apoya fuertemente en reglas de iptables (NAT) para el
rendimiento.

Bloque IV - Punto 3                         71 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


2.2.1.4. Probables Focos de Examen

En el contexto de una oposición para TAI, las preguntas sobre arquitectura suelen centrarse en la
seguridad, los puertos y la descomposición del demonio.
    • Socket vs. TCP: Es vital recordar que la comunicación por defecto es a través del socket Unix
      (/var/run/docker.sock). Si el examen pregunta por la configuración segura por defecto, la
      respuesta nunca es TCP 2375.
    • Puertos Estándar: Memorizar los puertos IANA asignados a Docker:
         – 2375: HTTP (texto plano, inseguro).
         – 2376: HTTPS (TLS, seguro).
    • Relación containerd/runc: Diferenciar sus roles.
         – Si la pregunta habla de “interactuar con el kernel” o “crear los namespaces”, la respuesta
           es runc.
         – Si la pregunta habla de “gestionar la descarga de imágenes” o “ciclo de vida”, la respuesta
           es containerd.
    • Implicaciones de Seguridad del Grupo Docker: Pertenecer al grupo de usuarios docker
      en Linux equivale funcionalmente a tener privilegios de root, ya que permite controlar el
      demonio y, por ende, el sistema host. Esto es una pregunta clásica de seguridad.

2.2.2. Imágenes y contenedores

La relación entre imágenes y contenedores constituye el núcleo operativo de Docker. Ambos
conceptos son inseparables y representan diferentes estados en el ciclo de vida de una aplicación
virtualizada a nivel de sistema operativo.

2.2.2.1. Definición y analogía conceptual

Para comprender la distinción técnica, se suele utilizar la analogía de la Programación Orientada
a Objetos (POO):
  1. Imagen (La Clase): Es una plantilla de solo lectura e inerte. Contiene el código de la
     aplicación, las librerías, las herramientas del sistema, las dependencias y los archivos de
     configuración necesarios para ejecutar la aplicación. Es un artefacto estático que define el
     entorno.
  2. Contenedor (El Objeto): Es la instancia en tiempo de ejecución (runtime instance) de una
     imagen. Es una entidad activa que ejecuta los procesos definidos en la imagen dentro de un
     entorno aislado.
Tabla comparativa: Entidades del ecosistema Docker

Entidad                   Estado                     Mutabilidad              Propósito

Imagen                    En reposo (At rest)        Inmutable (Solo          Definición,
                                                     lectura)                 empaquetado y
                                                                              distribución del
                                                                              software.
Contenedor                En ejecución               Mutable (Capa de         Ejecución de la
                          (Running)                  escritura)               aplicación y
                                                                              procesamiento de
                                                                              datos.


Bloque IV - Punto 3                             72 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


Fuente: Basado en tabla de referencia técnica.

2.2.2.2. Arquitectura de capas y Union File Systems

Técnicamente, una imagen de Docker no es un bloque monolítico, sino una colección ordenada
de capas de sistema de archivos (filesystem layers).
  1. Estructura de la Imagen (Image Layers):
        • Las imágenes se construyen apilando capas mediante un Union File System (UFS)
          (como Overlay2 o AUFS).
        • Cada instrucción en el proceso de construcción (por ejemplo, en un Dockerfile) genera
          una nueva capa que contiene solo las diferencias (deltas) respecto a la capa anterior.
        • Estas capas son de solo lectura y pueden ser compartidas entre diferentes imágenes.
          Por ejemplo, si múltiples imágenes se basan en ubuntu:latest, todas compartirán las
          mismas capas base en el disco, optimizando el almacenamiento y el ancho de banda.
  2. Capa del Contenedor (Container Layer):
        • Cuando se inicia un contenedor, Docker toma las capas de la imagen (R/O) y añade una
          fina capa de lectura/escritura (thin R/W layer) en la parte superior.
        • Cualquier modificación realizada por el contenedor (creación de archivos, logs,
          modificaciones de configuración) se escribe exclusivamente en esta capa superior.
        • Si el contenedor se elimina, esta capa de escritura se destruye, perdiéndose los datos
          almacenados en ella (a menos que se utilicen volúmenes externos), mientras que la
          imagen subyacente permanece intacta.
  3. Estrategia Copy-on-Write (CoW):
        • Docker utiliza la estrategia Copy-on-Write para la eficiencia. Si un contenedor necesita
          modificar un archivo que reside en una capa inferior (de la imagen), primero copia ese
          archivo a la capa superior de escritura y luego aplica los cambios. El archivo original en
          la imagen permanece inalterado.

2.2.2.3. Identificación y direccionamiento

La gestión de imágenes y contenedores depende de un sistema preciso de identificación:
    • Tags (Etiquetas): Son alias mutables y legibles por humanos (ej. redis:2.8 o ubuntu:latest).
      La etiqueta latest es simplemente una convención para la última versión construida, pero no
      garantiza inmutabilidad ni que sea la versión más reciente si no se actualiza explícitamente.
    • Digests (Resúmenes): Son identificadores inmutables generados mediante un hash
      criptográfico (SHA256) del contenido de la imagen (ej. sha256:4ccb...). El uso de digests
      garantiza que se está ejecutando exactamente el código esperado, evitando ataques de
      suplantación o inconsistencias entre entornos.
    • IDs: Tanto las imágenes como los contenedores poseen un ID único (UUID). Los comandos de
      Docker suelen aceptar una versión corta de este ID (los primeros 12 caracteres) para facilitar
      la gestión.

2.2.2.4. Probables Focos de Examen

En las oposiciones a TAI, es crítico dominar los conceptos de persistencia y estructura de capas.
    • Naturaleza aditiva de las capas: Es un concepto técnico recurrente. Al construir una imagen,
      las capas son estrictamente aditivas. Si se añade un archivo de 100MB en una capa y se
      borra en la siguiente, la imagen final no reduce su tamaño; el archivo sigue existiendo en la


Bloque IV - Punto 3                              73 de 164                          January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      capa inferior aunque esté “enmascarado” en la vista final. Para reducir tamaño, los archivos
      deben borrarse en la misma capa (instrucción) en la que se crearon.
    • Volatilidad de la capa del contenedor: Pregunta clásica sobre persistencia. Los datos escritos
      en la capa R/W del contenedor son efímeros. Al ejecutar docker rm <contenedor>, esos datos
      se pierden irrecuperablemente. La persistencia debe delegarse siempre a volúmenes.
    • Imagen Base vs. Scratch:
         – Las imágenes suelen partir de una base (ej. Ubuntu, Alpine).
         – Existe una imagen especial vacía llamada scratch. Se utiliza para construir imágenes
           mínimas que contienen únicamente binarios estáticos compilados (ej. Go o C), sin
           sistema operativo invitado, ofreciendo la máxima seguridad y el mínimo tamaño.
    • Diferencia docker run vs docker start:
         – docker run: Crea un nuevo contenedor a partir de una imagen (crea la capa R/W) y lo
           inicia.
         – docker start: Inicia un contenedor existente que estaba detenido (reutiliza la capa
           R/W existente y su configuración).

2.2.3. Dockerfile y construcción de imágenes

El Dockerfile es el elemento central para la automatización y definición de contenedores en Docker.
Se trata de un archivo de texto plano que contiene una lista ordenada de instrucciones que el
demonio de Docker lee y ejecuta secuencialmente para ensamblar una imagen final. Este enfoque
permite que la infraestructura sea tratada como código (Infrastructure as Code), garantizando que
la creación de imágenes sea un proceso repetible, versionable y transparente.

2.2.3.1. Estructura y ciclo de vida de construcción

El proceso de construcción (docker build) transforma el código fuente y las definiciones del
Dockerfile en una imagen ejecutable. Este proceso implica conceptos clave:
  1. Contexto de construcción (Build Context): Al ejecutar docker build, el cliente envía al
     demonio todos los archivos del directorio especificado (el contexto). Para optimizar este
     proceso y evitar enviar archivos innecesarios (como .git o archivos temporales), se utiliza
     el archivo .dockerignore, que funciona de manera similar a .gitignore.
  2. Generación de Capas (Layering): Cada instrucción en el Dockerfile (como RUN, COPY, ADD)
     genera una nueva capa intermedia en la imagen. Docker utiliza una caché de capas
     inteligente: si una instrucción y su contexto no han cambiado, Docker reutiliza la capa
     existente en lugar de reconstruirla, acelerando drásticamente el proceso.
  3. Contenedores Intermedios: Durante la construcción, Docker crea contenedores temporales
     para ejecutar cada instrucción, guarda el estado resultante como una nueva capa y elimina
     el contenedor temporal antes de pasar a la siguiente instrucción.

2.2.3.2. Instrucciones principales del Dockerfile

El dominio de las instrucciones es esencial para el examen. A continuación, se detallan las más
relevantes técnica y funcionalmente:




Bloque IV - Punto 3                          74 de 164                               January 31, 2026
                      Correo electrónico. Contenedores y microservicios



Instrucción                   Función Técnica                    Detalles Críticos para Examen

FROM                          Define la imagen base sobre la     Debe ser la primera
                              que se construye.                  instrucción (salvo ARG).
                                                                 Ejemplo: FROM ubuntu:20.04 o
                                                                 FROM scratch (vacía).

RUN                           Ejecuta comandos durante la        Crea una nueva capa con los
                              fase de construcción (build        cambios (ej. instalar paquetes).
                              time).                             Tiene dos formas: Shell (RUN
                                                                 command) y Exec (RUN ["exe",
                                                                 "param"]).

COPY                          Copia archivos del contexto        Copia literal. Es la opción
                              local al sistema de archivos del   preferida sobre ADD por
                              contenedor.                        transparencia y seguridad.
ADD                           Similar a COPY, pero con           1. Permite descargar desde
                              funcionalidades avanzadas.         URL remotas. 2.
                                                                 Descomprime
                                                                 automáticamente archivos
                                                                 .tar locales en el destino.

CMD                           Define el comando por defecto      Puede ser sobrescrito
                              al iniciar el contenedor.          fácilmente por argumentos al
                                                                 ejecutar docker run. Solo
                                                                 puede haber un CMD efectivo (el
                                                                 último).
ENTRYPOINT                    Configura el contenedor para       El comando definido no se
                              correr como un ejecutable.         sobrescribe fácilmente; los
                                                                 argumentos de docker run se
                                                                 añaden (append) a este
                                                                 comando.
WORKDIR                       Establece el directorio de         Si no existe, lo crea.
                              trabajo para instrucciones         Recomendado usar rutas
                              siguientes (RUN, CMD, COPY).       absolutas en lugar de cd.
ENV                           Define variables de entorno        Disponibles tanto en tiempo
                              persistentes.                      de construcción como de
                                                                 ejecución.
EXPOSE                        Documenta qué puertos              Informativo. No publica el
                              escucha la aplicación.             puerto al host; para ello se
                                                                 requiere la opción -p en
                                                                 docker run.

VOLUME                        Crea un punto de montaje para      Asegura que los datos en esa
                              volúmenes externos.                ruta sean persistentes y no se
                                                                 guarden en la capa de
                                                                 escritura del contenedor.




Bloque IV - Punto 3                       75 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Instrucción                      Función Técnica                    Detalles Críticos para Examen

USER                             Cambia el usuario (UID) para       Crítico para seguridad: evita
                                 las siguientes instrucciones.      ejecutar procesos como root
                                                                    dentro del contenedor.


2.2.3.3. Optimización y Multistage Builds

La eficiencia y el tamaño de la imagen son métricas de calidad críticas.
    • Minimización de Capas: Dado que las capas son aditivas, borrar un archivo en una
      instrucción RUN posterior no reduce el tamaño final de la imagen (el archivo sigue existiendo
      en la capa anterior, aunque oculto).
        – Técnica: Encadenar comandos con && en una sola instrucción RUN para instalar, limpiar
           caché y borrar temporales en la misma capa.
        – Ejemplo: RUN apt-get update && apt-get install -y paquete && rm -rf /var/lib/apt/lists/
    • Construcciones Multi-etapa (Multistage Builds): Introducidas para solucionar el problema
      de imágenes infladas con herramientas de compilación. Permiten usar múltiples sentencias
      FROM en un solo Dockerfile.
        – Fase 1 (Builder): Compila el código fuente usando todas las herramientas necesarias
           (compiladores, SDKs, Maven, etc.).
        – Fase 2 (Runtime): Copia solo el binario compilado desde la fase anterior (COPY
           --from=builder ...) a una imagen base mínima (como Alpine o Distroless).
        – Resultado: Imágenes de producción minúsculas y seguras, sin código fuente ni
           herramientas de desarrollo.

2.2.3.4. Probables Focos de Examen

En el examen de TAI, las preguntas sobre Dockerfile suelen centrarse en diferencias sutiles y
buenas prácticas de seguridad.
    • Diferencia clave COPY vs ADD:
        – Pregunta típica: “¿Qué instrucción permite descomprimir automáticamente un archivo
          tar local?” -> Respuesta: ADD.
        – Seguridad: Se desaconseja ADD para URLs remotas por riesgo de inyección de contenido
          malicioso o Man-in-the-Middle; se prefiere usar curl/wget dentro de un RUN para verificar
          hash.
    • Diferencia CMD vs ENTRYPOINT:
        – CMD: “Argumentos por defecto”. Se usa cuando quieres que el usuario pueda cambiar el
          comando fácilmente.
        – ENTRYPOINT: “Contenedor como ejecutable”. Se usa cuando quieres que el contenedor
          actúe como un binario único (ej. ping) y el usuario solo aporte parámetros.
        – Matiz: Si se usan ambos, CMD provee los argumentos por defecto para el ENTRYPOINT.
    • Persistencia de datos en la construcción:
        – Los datos escritos en un directorio declarado como VOLUME durante la construcción
          (instrucciones RUN posteriores a VOLUME) pueden ser descartados o no persistir en la
          imagen final según la implementación, por lo que se recomienda configurar datos
          en volúmenes solo en tiempo de ejecución o mediante scripts de entrada (entrypoint
          scripts).
    • Orden de las instrucciones (Caché):

Bloque IV - Punto 3                          76 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


        – Las instrucciones que cambian frecuentemente (como COPY . . con el código fuente)
          deben ir al final del Dockerfile. Las dependencias estables (librerías) deben instalarse
          antes. Esto maximiza el uso de la caché de Docker y reduce tiempos de compilación.
    • Shell form vs Exec form:
        – Shell form (CMD comando param): Ejecuta el comando bajo /bin/sh -c. El proceso
          principal es la shell, no la aplicación, lo que puede impedir que la aplicación reciba
          señales de parada (SIGTERM).
        – Exec form (CMD ["comando", "param"]): Ejecuta el comando directamente (JSON array).
          Es la forma recomendada porque el proceso recibe señales del sistema operativo (PID
          1).

2.2.4. Docker Hub y registros de imágenes

El componente de distribución en el ecosistema de contenedores es fundamental para el ciclo de
vida del software, actuando como el nexo entre la construcción (build) y la ejecución (run). Los
registros son servicios centralizados que almacenan y distribuyen imágenes de contenedores.

2.2.4.1. Concepto de Registro y Repositorio

Es crucial distinguir técnicamente entre un Registro y un Repositorio, ya que, aunque
coloquialmente se usan de forma intercambiable, representan entidades jerárquicas distintas:
  1. Registro (Registry): Es el servicio o infraestructura (servidor) que almacena y distribuye
     imágenes Docker. Puede ser público o privado y gestiona el control de acceso y la API de
     almacenamiento.
  2. Repositorio (Repository): Es una colección de imágenes relacionadas dentro de un
     registro, usualmente diferenciadas por sus etiquetas (tags). Por ejemplo, en nginx:latest y
     nginx:1.19, ambas imágenes pertenecen al mismo repositorio nginx.

La nomenclatura estándar de una imagen refleja esta jerarquía y le indica al demonio de Docker
dónde buscar la imagen:
[hostname[:port]] / [username] / [reponame] : [tag]

    • Hostname: Dirección del registro. Si se omite, el cliente asume por defecto Docker Hub.
    • Username: Espacio de nombres (usuario u organización). En Docker Hub, si se omite, se
      asume library (imágenes oficiales).
    • Tag: Versión de la imagen. Si se omite, se asume latest.

2.2.4.2. Docker Hub

Docker Hub es el registro público predeterminado y el más grande del mundo, operado como
un servicio SaaS por Docker Inc. Su función principal es facilitar el intercambio de aplicaciones
empaquetadas.
    • Imágenes Oficiales: Son mantenidas por Docker y los proveedores de software (upstream),
      ofreciendo una base segura y optimizada para construir otras aplicaciones (ej. ubuntu, python,
      redis).
    • Imágenes de la Comunidad: Subidas por usuarios individuales u organizaciones. No tienen
      la misma garantía de mantenimiento o seguridad que las oficiales.




Bloque IV - Punto 3                          77 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.2.4.3. Registros Privados y Alternativas

Aunque Docker Hub es conveniente, las organizaciones suelen requerir registros privados para
proteger su propiedad intelectual, reducir la latencia de red, asegurar alta disponibilidad y cumplir
con normativas de seguridad estrictas.
Tipos de implementación:
  1. Docker Registry (Self-hosted): Es una implementación de código abierto (docker-
     distribution-registry) que permite alojar un registro propio. Por defecto, carece de
     interfaz gráfica y autenticación avanzada, escuchando habitualmente en el puerto 5000.
  2. Soluciones Empresariales y Cloud: Proveedores de nube y terceros ofrecen registros con
     funciones avanzadas como escaneo de vulnerabilidades y gestión de accesos basada en roles
     (RBAC). Ejemplos destacados incluyen:
        • Harbor: Proyecto de la CNCF, enfocado en seguridad y firma de imágenes.
        • Amazon ECR, Azure ACR, Google GCR: Registros integrados en nubes públicas.
        • Quay: Registro desarrollado por Red Hat/CoreOS.
Tabla comparativa: Docker Hub vs. Registro Privado

                                                                    Registro Privado
Característica                    Docker Hub                        (On-Premise/Cloud)

Acceso                            Público por defecto (Internet).   Restringido (Red
                                                                    interna/VPN).
Seguridad                         Escaneo básico (en planes Pro).   Control total, escaneo
                                                                    mandatorio.
Latencia                          Depende de la conexión a          Baja latencia (LAN/VPC).
                                  Internet.
Coste                             Gratuito (limitado) /             Coste de infraestructura y
                                  Suscripción.                      mantenimiento.


2.2.4.4. Seguridad en Registros: Confianza y Autenticación

La seguridad en la cadena de suministro de software depende de la integridad del registro.
  1. Docker Content Trust (DCT): Utiliza firmas digitales para garantizar la procedencia e
     integridad de las imágenes. Permite verificar que una imagen fue firmada por un editor
     confiable y no ha sido alterada en tránsito o en reposo.
  2. Escaneo de Vulnerabilidades: Es una práctica crítica analizar las imágenes almacenadas en
     el registro contra bases de datos de CVEs (vulnerabilidades conocidas). Herramientas como
     Clair, Trivy o las integradas en registros comerciales bloquean la descarga de imágenes
     comprometidas.
  3. Autenticación: El comando docker login se utiliza para autenticarse contra un registro.
     Las credenciales suelen almacenarse en el archivo ~/.docker/config.json (o a través de
     credential helpers). Es un riesgo de seguridad conocido que, en configuraciones básicas, estas
     credenciales puedan almacenarse solo en base64.




Bloque IV - Punto 3                           78 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.2.4.5. Probables Focos de Examen

Para el examen de TAI, es esencial dominar los comandos de interacción y los archivos de
configuración:
    • Comandos Básicos:
         – docker push <imagen>: Sube una imagen al registro. Requiere que la imagen esté
           etiquetada correctamente con la dirección del registro.
         – docker pull <imagen>: Descarga una imagen del registro.
         – docker tag <origen> <destino>: Crea un alias de la imagen con el nombre del registro
           destino para poder hacer push.
    • Puerto Estándar del Registro: El puerto por defecto para un registro privado Docker
      autohospedado es el 5000.
    • Riesgo de la etiqueta latest: En entornos de producción, se desaconseja usar la etiqueta
      latest porque es mutable y no garantiza que todos los nodos tengan la misma versión
      del software. Se debe usar un digest (hash SHA256) o una etiqueta de versión específica e
      inmutable.
    • Ubicación de credenciales: Las credenciales de autenticación del registro se almacenan
      localmente en ~/.docker/config.json (o $HOME/.docker/config.json). Una pregunta
      frecuente versa sobre dónde busca Docker las credenciales de login.

2.2.5. Redes en Docker

La gestión de redes en Docker se basa en la abstracción de la complejidad de la red física mediante
el uso de controladores (drivers) y la manipulación de namespaces de red del kernel de Linux.
Docker crea una capa de virtualización que permite a los contenedores comunicarse entre sí, con
el host anfitrión y con redes externas, manteniendo el aislamiento necesario para la seguridad y
la estabilidad del sistema.

2.2.5.1. Controladores de red nativos (Network Drivers)

Docker implementa un modelo de red conectable (pluggable), donde diferentes controladores
gestionan la topología y el comportamiento de la red. Los controladores nativos más relevantes
para el examen son:
Tabla comparativa de controladores de red en Docker


Controlador                      Descripción Técnica y Uso          Nivel de Aislamiento

Bridge (Puente)                  Es el controlador                  Alto (Namespace de red
                                 predeterminado. Crea un            propio). Requiere mapeo de
                                 puente virtual (usualmente         puertos (-p) para acceso
                                 docker0) en el host. Los           externo.
                                 contenedores obtienen su
                                 propia pila de red y dirección
                                 IP interna. Se comunican con
                                 el exterior mediante NAT
                                 (Enmascaramiento IP) a través
                                 de la IP del host.




Bloque IV - Punto 3                          79 de 164                             January 31, 2026
                        Correo electrónico. Contenedores y microservicios



Controlador                      Descripción Técnica y Uso           Nivel de Aislamiento

Host                             Elimina el aislamiento de red.      Nulo a nivel de red. Maximiza
                                 El contenedor comparte el           el rendimiento al eliminar la
                                 mismo namespace de red que          sobrecarga de NAT.
                                 el host anfitrión. No recibe
                                 una IP propia; usa la IP del host
                                 y sus puertos directamente.
None                             Deshabilita toda la red para el     Total (Aislado de la red).
                                 contenedor. Solo dispone de la
                                 interfaz de loopback
                                 (127.0.0.1). Útil para trabajos
                                 por lotes que no requieren red
                                 o por máxima seguridad.
Overlay                          Permite la comunicación entre       Alto. Abstrae la red física entre
                                 contenedores que se ejecutan        múltiples servidores.
                                 en diferentes hosts (nodos).
                                 Es la base de Docker Swarm.
                                 Utiliza túneles VXLAN para
                                 enrutar el tráfico de capa 2
                                 sobre una red IP subyacente.
Macvlan                          Permite asignar una dirección       Medio/Alto. Ideal para
                                 MAC única a un contenedor,          aplicaciones legacy que
                                 haciéndolo aparecer como un         requieren estar en la misma
                                 dispositivo físico                  subred física.
                                 independiente en la red. Se
                                 conecta directamente a la
                                 interfaz física del host sin
                                 pasar por el puente NAT.


2.2.5.2. Arquitectura de red Bridge (Predeterminada)

La red bridge es la configuración estándar y la más preguntada en exámenes técnicos. Su
funcionamiento se basa en los siguientes componentes:
  1. Interfaz docker0: Al iniciar el demonio Docker, se crea un puente virtual en el host llamado
     docker0 (generalmente con la subred 172.17.0.0/16).
  2. Pares veth (Virtual Ethernet): Cuando arranca un contenedor, Docker crea un par de
     interfaces virtuales. Una se queda en el host conectada al puente docker0 (ej. vethxxx)
     y la otra se coloca dentro del namespace del contenedor renombrada como eth0.
  3. Comunicación:
        • Entre contenedores (mismo host): Se comunican directamente a través del puente
          docker0 si están en la misma red.
        • Hacia el exterior: El tráfico saliente utiliza NAT (Network Address Translation). Docker
          configura reglas de iptables (IP Masquerade) para que el tráfico parezca originarse desde
          la IP del host.




Bloque IV - Punto 3                          80 de 164                                January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.2.5.3. Publicación de puertos y Docker Proxy

Dado que los contenedores en modo bridge tienen IPs privadas no enrutables desde el exterior,
para exponer un servicio se debe realizar la publicación de puertos.
    • Comando: Se utiliza la bandera -p o --publish en docker run.
         – Sintaxis: -p <puerto_host>:<puerto_contenedor> (ej. -p 8080:80 redirige el tráfico del
           puerto 8080 del host al 80 del contenedor).
    • Mecanismo interno: Docker utiliza una combinación de reglas DNAT en iptables y un proceso
      de espacio de usuario llamado docker-proxy. Este proxy escucha en el puerto del host y
      reenvía el tráfico al contenedor, aunque en sistemas modernos se prioriza el uso de NAT
      (“hairpin NAT”) por rendimiento.

2.2.5.4. Probables Focos de Examen

Para el examen de TAI, es fundamental dominar las diferencias entre los modos de red y la sintaxis
de exposición de puertos.
    • Red por defecto: Si no se especifica la opción --net o --network, Docker utiliza por defecto
      el driver bridge. La interfaz en el host se llama típicamente docker0.
    • Modo Host vs. Bridge:
         – Pregunta típica: “¿Qué modo de red ofrece el mayor rendimiento de red al eliminar el
           NAT?”. Respuesta: Host.
         – Consecuencia del modo Host: No se pueden mapear puertos (-p es ignorado o
           irrelevante) porque el contenedor ya usa los puertos del host. Si dos contenedores
           intentan usar el puerto 80 en modo host, habrá un conflicto de puertos.
    • Sintaxis -p: Recordar siempre el orden: HOST:CONTENEDOR.
         – -p 8080:80 significa “accedo a mi máquina por el 8080 y llego al 80 del contenedor”.
    • Aislamiento:
         – La red none ofrece el máximo aislamiento de red (solo loopback).
         – La red overlay es necesaria para la comunicación entre contenedores en distintos nodos
           de un clúster Swarm.
    • DNS embebido: Docker tiene un servidor DNS interno en 127.0.0.11 (en el contenedor) que
      permite que los contenedores se resuelvan por nombre de servicio o nombre de contenedor,
      pero esto solo funciona automáticamente en redes definidas por el usuario (docker network
      create), no en el bridge por defecto (docker0) donde se requiere --link (obsoleto) o usar IPs.


2.2.6. Volúmenes y persistencia de datos

La gestión de datos en Docker es un aspecto crítico debido a la naturaleza efímera e inmutable de
los contenedores. Por diseño, los datos generados o modificados dentro de la capa de escritura
(container layer) de un contenedor tienen el mismo ciclo de vida que el proceso que los generó: si
el contenedor se elimina, esos datos se pierden irrecuperablemente.
Para garantizar la persistencia de la información (como bases de datos o logs históricos) y permitir
el intercambio de datos entre contenedores o con el host, Docker proporciona mecanismos de
montaje que desacoplan el almacenamiento del ciclo de vida del contenedor.

2.2.6.1. Mecanismos de montaje y tipos de almacenamiento

Docker ofrece tres formas principales de montar almacenamiento en un contenedor, cada una
con características y casos de uso específicos:


Bloque IV - Punto 3                          81 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


Tabla comparativa de tipos de montaje

                      Descripción                              Ubicación en       Caso de Uso
Tipo de Montaje       Técnica             Persistencia         Host               Principal

Volúmenes             Gestionados         Alta (Persisten                       Bases de datos,
                                                               /var/lib/docker/volumes/
(Volumes)             íntegramente        tras borrar el       (en Linux)         datos
                      por Docker. Son     contenedor)                             compartidos
                      independientes                                              entre
                      del ciclo de vida                                           contenedores,
                      del contenedor y                                            copias de
                      la opción                                                   seguridad.
                      preferida para
                      persistencia.
Bind Mounts           Mapean un           Alta (Datos en el    Cualquier ruta     Desarrollo
                      archivo o           host)                especificada por   (compartir
                      directorio                               el usuario         código fuente),
                      específico del                                              archivos de
                      host al                                                     configuración
                      contenedor.                                                 del host.
                      Dependen de la
                      estructura de
                      directorios del
                      host.
tmpfs Mounts          Almacenamiento      Nula (Se pierde al   Memoria RAM        Datos sensibles
                      en la memoria       detener el                              (secretos) o datos
                      volátil del host.   contenedor)                             temporales de
                      Nunca se escribe                                            alto rendimiento.
                      en el sistema de
                      archivos del
                      contenedor ni
                      del host.


2.2.6.2. Gestión del ciclo de vida de los volúmenes

Los volúmenes son ciudadanos de primera clase en Docker y poseen su propio ciclo de vida,
gestionado a través de la CLI docker volume. A diferencia de la capa de escritura del contenedor,
los volúmenes no utilizan el sistema Copy-on-Write (CoW), lo que ofrece un rendimiento nativo
para E/S intensiva.
Comandos esenciales para la administración:
    • Creación explícita: docker volume create <nombre> permite crear un volumen antes de
      usarlo.
    • Listado: docker volume ls muestra los volúmenes disponibles en el host.
    • Inspección: docker volume inspect <nombre> devuelve detalles en formato JSON, como la
      ruta física en el host (Mountpoint).
    • Eliminación: docker volume rm <nombre> borra un volumen. Importante: Docker no borra
      volúmenes automáticamente cuando se elimina un contenedor para evitar pérdida de datos.


Bloque IV - Punto 3                           82 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


    • Limpieza: docker volume prune elimina todos los volúmenes que no están siendo utilizados
      por ningún contenedor.

2.2.6.3. Sintaxis de montaje: -v vs --mount

Existen dos formas de adjuntar almacenamiento a un contenedor durante el arranque (docker
run). Es fundamental distinguirlas de cara al examen:

  1. Flag -v o --volume (Sintaxis clásica): Consiste en tres campos separados por dos puntos (:):
     ORIGEN:DESTINO:OPCIONES.
        • Ejemplo Volumen: -v mi_volumen:/data (Si mi_volumen no existe, Docker lo crea
          automáticamente, a menudo como local).
        • Ejemplo Bind Mount: -v /home/user/app:/app (Ruta absoluta del host).
        • Opción Read-Only: Se añade :ro al final para que el contenedor solo pueda leer los datos
          (ej. -v /datos:/app/datos:ro).
  2. Flag --mount (Sintaxis moderna y explícita): Utiliza pares clave-valor separados por comas.
     Es más verbosa pero permite configuraciones más complejas (como drivers de volumen o
     tmpfs).
        • Sintaxis: --mount type=volume,source=mi_volumen,target=/data.
        • Bind: --mount type=bind,source=/ruta/host,target=/ruta/contenedor.

2.2.6.4. Drivers de almacenamiento (Storage Drivers) vs. Volúmenes

Es crucial no confundir los Storage Drivers (como Overlay2, devicemapper, btrfs) con los
Volúmenes.
    • Storage Drivers: Gestionan las imágenes y la capa de escritura del contenedor.
      Implementan el sistema de unión de capas y Copy-on-Write (CoW). Son más lentos
      para escrituras intensivas.
    • Data Volumes: Bypass del Storage Driver. Escriben directamente en el sistema de archivos
      del host, ofreciendo rendimiento nativo y persistencia independiente.
Docker también soporta Plugins de Volumen (como REX-Ray, plugins de nube AWS/Azure) que
permiten que el volumen resida en almacenamiento externo (NFS, SAN, Cloud Block Storage),
facilitando que los datos sigan al contenedor si este se mueve a otro host del clúster.

2.2.6.5. Probables Focos de Examen

En el examen de TAI, las preguntas sobre almacenamiento suelen centrarse en la seguridad, la
persistencia y la sintaxis.
    • Diferencia funcional Bind Mount vs Volumen:
        – Pregunta típica: “¿Qué mecanismo permite editar código en el host y verlo reflejado
          inmediatamente en el contenedor?”. Respuesta: Bind Mount.
        – Si la pregunta se refiere a “gestión por parte de Docker” o “independencia del sistema
          operativo”, la respuesta es Volumen.
    • Persistencia tras docker rm:
        – Los datos en la capa del contenedor (Container Layer) se pierden al borrar el contenedor.
        – Los datos en un Volumen persisten tras borrar el contenedor.
    • Ubicación de los volúmenes: Memorizar la ruta por defecto en Linux: /var/lib/docker/volumes/.




Bloque IV - Punto 3                           83 de 164                            January 31, 2026
                        Correo electrónico. Contenedores y microservicios


    • Modo solo lectura (:ro): Es frecuente que pregunten cómo proteger los datos del host para
      que el contenedor no pueda modificarlos. La respuesta es montar el volumen/bind con la
      opción read-only (:ro).
    • Volúmenes huérfanos (Dangling volumes): Al borrar un contenedor con docker rm -v, se
      borra el volumen asociado solo si es anónimo. Si es un volumen nombrado, persiste. El
      comando para limpiar volúmenes no usados es docker volume prune.

2.2.7. Docker Compose

Docker Compose es una herramienta diseñada para definir y ejecutar aplicaciones multi-
contenedor. Mientras que la CLI de Docker (docker run) es adecuada para gestionar contenedores
individuales, Compose permite describir una arquitectura completa de servicios interconectados
(frontend, backend, base de datos) en un solo archivo de texto declarativo, simplificando
drásticamente el despliegue en entornos de desarrollo y pruebas.

2.2.7.1. Definición y Archivo de Configuración

El núcleo de Docker Compose es el archivo de configuración, denominado por defecto docker-
compose.yml (o .yaml). Este archivo utiliza formato YAML para definir los servicios, redes y
volúmenes de la aplicación, sustituyendo la necesidad de ejecutar múltiples comandos de shell o
scripts manuales propensos a errores.
La estructura básica del archivo incluye tres secciones principales:
  1. version: Indica la versión de la sintaxis del archivo Compose. Las versiones más recientes
     (v3) son compatibles con Docker Swarm a través de docker stack.
  2. services: Define los contenedores que forman la aplicación. Cada servicio escala y se
     configura de forma independiente.
  3. networks y volumes: Definen la infraestructura de red y almacenamiento compartida por
     los servicios.

2.2.7.2. Elementos Principales del Manifiesto

Dentro de la sección services, se utilizan directivas que son análogas a las banderas de docker
run. Las más relevantes para el examen incluyen:


Directiva                        Descripción y Función             Referencia

image                            Especifica la imagen base a
                                 descargar y ejecutar (ej.
                                 mysql:latest). Si no existe
                                 localmente, intenta
                                 descargarla.
build                            Indica que la imagen debe
                                 construirse a partir de un
                                 Dockerfile. Se especifica el
                                 context (ruta) y
                                 opcionalmente el nombre del
                                 Dockerfile.



Bloque IV - Punto 3                         84 de 164                           January 31, 2026
                           Correo electrónico. Contenedores y microservicios



Directiva                          Descripción y Función               Referencia

ports                              Mapea puertos entre el host y
                                   el contenedor (Sintaxis
                                   HOST:CONTAINER).

volumes                            Define montajes de volúmenes
                                   o bind mounts. Es crítico para
                                   la persistencia de datos (ej.
                                   bases de datos).
environment                        Establece variables de entorno
                                   dentro del contenedor.
                                   Fundamental para
                                   configuración externa
                                   (12-Factor App).
depends_on                         Define el orden de inicio.
                                   Asegura que un servicio no se
                                   inicie hasta que el servicio
                                   listado haya arrancado
                                   (aunque no garantiza que esté
                                   “listo” o healthy).
networks                           Especifica a qué redes
                                   definidas se conecta el servicio.
                                   Por defecto, Compose crea una
                                   red bridge para el stack.


2.2.7.3. Ciclo de Vida y Comandos Principales

Docker Compose gestiona el ciclo de vida completo de la aplicación mediante comandos que
operan sobre el grupo de contenedores definido en el archivo YAML.
    • Levantar el entorno (up): El comando docker-compose up lee el archivo YAML, crea la red
      por defecto, construye las imágenes (si es necesario) y arranca los contenedores.
         – La opción -d (detached) ejecuta los contenedores en segundo plano.
         – Compose prefija los nombres de los contenedores con el nombre del directorio del
           proyecto para evitar conflictos (ej. midirectorio_web_1).
    • Construcción (build): docker-compose build procesa las instrucciones build del YAML para
      crear o actualizar las imágenes locales antes de lanzarlas.
    • Gestión de estado:
         – docker-compose stop: Detiene los contenedores sin eliminarlos.
         – docker-compose start: Inicia contenedores detenidos.
         – docker-compose ps: Lista los contenedores del stack y su estado actual.
    • Destrucción (down): docker-compose down detiene y elimina los contenedores y las redes
      creadas por up. Por defecto, no elimina los volúmenes declarados (para proteger los datos),
      a menos que se especifique la opción -v.



Bloque IV - Punto 3                            85 de 164                             January 31, 2026
                          Correo electrónico. Contenedores y microservicios


    • Ejecución y Logs:
         – docker-compose logs -f: Muestra y sigue la salida estándar combinada de todos los
           servicios.
         – docker-compose exec <servicio> <comando>: Ejecuta un comando dentro de un
           contenedor en ejecución (análogo a docker exec).

2.2.7.4. Probables Focos de Examen

En las oposiciones a TAI, las preguntas sobre Docker Compose suelen centrarse en la sintaxis, el
orden de arranque y la gestión de redes.
    • Limitación de depends_on: Es una pregunta técnica frecuente. depends_on controla el orden
      de inicio (arranca la DB antes que la Web), pero no espera a que la aplicación dentro del
      contenedor esté lista para aceptar conexiones (ej. que MySQL esté escuchando en el puerto
      3306). Para esperar a que esté “listo”, se requieren healthchecks o scripts de espera (como
      wait-for-it).

    • Redes y DNS interno: Docker Compose crea automáticamente una red (tipo bridge) para la
      aplicación. Los contenedores pueden comunicarse entre sí utilizando el nombre del servicio
      definido en el YAML como hostname.
         – Ejemplo: Si el servicio de base de datos se llama db, la aplicación web conecta a
           mysql://db:3306, no a una IP.

    • Diferencia docker-compose up vs build: Si se cambia el código fuente o el Dockerfile, ejecutar
      solo docker-compose up podría no reconstruir la imagen si ya existe. Se debe usar docker-
      compose up --build o ejecutar docker-compose build explícitamente.

    • Persistencia tras down: Es importante recordar que docker-compose down borra
      contenedores y redes, pero preserva los volúmenes externos o nombrados para evitar la
      pérdida accidental de datos persistentes.
    • Variables de entorno: Compose soporta la sustitución de variables en el archivo YAML
      usando la sintaxis ${VARIABLE}. También lee automáticamente un archivo llamado .env si
      existe en el mismo directorio, lo cual es estándar para gestionar secretos o configuración
      dependiente del entorno.

2.3. Otras tecnologías de contenedores
Esta sección amplía la visión del administrador de sistemas más allá del ecosistema
Docker, explorando tecnologías alternativas y complementarias que han surgido gracias
a la estandarización de la industria (Open Container Initiative - OCI). Aunque Docker popularizó
el concepto, hoy en día existen herramientas especializadas que ofrecen mejoras en seguridad,
rendimiento o propósitos arquitectónicos diferentes.
En el panorama actual, el término “contenedor” ya no está atado a un único fabricante.
La evolución del mercado ha llevado a la desagregación de las plataformas monolíticas en
componentes modulares y al nacimiento de alternativas diseñadas para cubrir las carencias de
diseño de Docker. Es crucial que el administrador distinga entre un contenedor de aplicación
(microservicio efímero) y un contenedor de sistema (similar a una VM ligera), así como
comprender las diferencias entre los motores que requieren un proceso en segundo plano
(daemon) y los que no.



Bloque IV - Punto 3                           86 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


Mientras que Docker sigue ser la herramienta por excelencia para el desarrollo, entornos como
Podman están ganando terreno en sistemas de producción (especialmente en distribuciones
basadas en Red Hat) debido a su arquitectura sin demonio (daemonless) y su capacidad para
ejecutarse sin privilegios de root (rootless). Por otro lado, LXC/LXD ofrece una aproximación
más tradicional, proveyendo un sistema operativo completo dentro del contenedor, ideal para
migraciones “lift-and-shift” de servidores antiguos. Finalmente, containerd representa el
estándar industrial de bajo nivel, siendo el motor “invisible” que potencia tanto a Docker como a
Kubernetes modernos.
A continuación, se presenta una tabla comparativa de estas tecnologías para entender su nicho de
uso:

Tecnología              Arquitectura              Tipo de Contenedor        Caso de Uso Principal

Podman                  Sin demonio               Aplicación (OCI)          Sustituto directo de
                        (Daemonless)                                        Docker con mayor
                                                                            seguridad (Rootless).
LXC/LXD                 Basada en procesos        Sistema (System           “VPS ligeros”,
                        del kernel                Container)                entornos de larga
                                                                            duración, simulación
                                                                            de SO completo.
containerd              Demonio ligero            Aplicación (OCI)          Motor subyacente
                        (Runtime)                                           para Kubernetes y
                                                                            orquestadores; no
                                                                            suele usarse
                                                                            manualmente.


Para visualizar la diferencia fundamental de arquitectura, el siguiente gráfico compara el modelo
centralizado de Docker frente al modelo descentralizado de Podman, un concepto clave en la
seguridad de contenedores:




                                   Figure 3: Podman vs. Docker

El conocimiento de estas herramientas permite al administrador elegir la solución adecuada:
usar LXC cuando se necesita persistencia de sistema operativo completo, Podman en entornos
con estrictas políticas de seguridad (como la administración pública o banca), o entender cómo
containerd gestiona los ciclos de vida cuando se opera un clúster de Kubernetes.

2.3.1. Podman

Podman (Pod Manager) es un motor de contenedores de código abierto, desarrollado
principalmente por Red Hat, que permite desarrollar, gestionar y ejecutar contenedores y Pods


Bloque IV - Punto 3                          87 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


bajo los estándares de la Open Container Initiative (OCI). Su diseño se distingue fundamentalmente
por ser sin demonio (daemonless) y por su enfoque nativo en la seguridad mediante la ejecución
sin privilegios (rootless).

2.3.1.1. Arquitectura “Daemonless” y modelo de procesos

A diferencia de Docker, que utiliza una arquitectura cliente-servidor donde un demonio central
(dockerd) con altos privilegios gestiona todos los contenedores, Podman adopta una arquitectura
descentralizada basada en el modelo fork-exec.
  1. Ausencia de Demonio Central: Podman no depende de un proceso en segundo plano
     persistente para funcionar. Cuando se ejecuta un comando de Podman, este interactúa
     directamente con el registro de imágenes, el almacenamiento y el kernel de Linux para
     lanzar el contenedor.
  2. Modelo Fork-Exec: El contenedor se ejecuta como un proceso hijo directo del comando
     Podman ejecutado por el usuario.
  3. Integración con systemd: Al ser un proceso estándar de Linux, Podman se integra
     nativamente con systemd. Esto permite que systemd gestione el ciclo de vida de los
     contenedores (inicio, parada, reinicio) tratándolos como servicios regulares del sistema, lo
     cual es una ventaja significativa en entornos de producción Enterprise Linux.
Tabla: Comparativa arquitectónica Docker vs. Podman


Característica                    Docker                            Podman

Modelo                            Cliente-Servidor (Monolítico)     Fork-Exec (Descentralizado)
Punto de Fallo                    Único (Si dockerd cae, todo       Distribuido (Fallo aislado por
                                  cae)                              contenedor)
Privilegios                       Root por defecto (Demonio)        Rootless por defecto (Usuario)
Supervisión                       El demonio supervisa los hijos    Systemd o el usuario
                                                                    supervisan


2.3.1.2. Seguridad y contenedores “Rootless”

Podman fue diseñado desde su inicio para ejecutar contenedores en modo rootless (sin privilegios
de administrador), lo que reduce drásticamente la superficie de ataque en caso de que un
contenedor sea comprometido.
    • Mapeo de Identidad (User Namespaces): Podman utiliza los espacios de nombres de usuario
      (User Namespaces) del kernel de Linux. Esto permite que un usuario no privilegiado en el
      host (ej. uid=1000) actúe como root (uid=0) dentro del contenedor.
    • Shadow-utils: Para lograr esto sin elevar privilegios reales, Podman aprovecha herramientas
      como newuidmap y newgidmap (del paquete shadow-utils) para asignar rangos de UIDs y GIDs
      subordinados accesibles por el usuario.
    • Aislamiento: Si un atacante escapa del contenedor (container breakout), en el host solo tendrá
      los permisos del usuario que lanzó el contenedor, no los de root, mitigando el impacto en el
      sistema operativo anfitrión.




Bloque IV - Punto 3                          88 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.3.1.3. Concepto de Pods locales

Haciendo honor a su nombre (Pod Manager), Podman introduce el concepto de Pod —tradicionalmente
asociado a Kubernetes— en el entorno local de contenedores.
    • Definición: Un Pod en Podman es un grupo de uno o más contenedores que comparten los
      mismos espacios de nombres de red, IPC y UTS.
    • Infra-contenedor (Infra-container): Al igual que en Kubernetes (con el contenedor pause),
      Podman crea un contenedor de infraestructura invisible que mantiene los namespaces
      abiertos y permite que los contenedores del Pod se comuniquen entre sí a través de
      localhost.
    • Transición a Kubernetes: Podman permite generar manifiestos YAML de Kubernetes a partir
      de contenedores locales (podman generate kube) y, a la inversa, ejecutar Pods definidos en
      YAML localmente (podman play kube).

2.3.1.4. Compatibilidad con Docker

Podman implementa una interfaz de línea de comandos (CLI) casi idéntica a la de Docker para
facilitar la migración.
    • Alias: Es común configurar alias docker=podman en el sistema, ya que la mayoría de los
      comandos (run, push, pull, build) funcionan con la misma sintaxis.
    • Cumplimiento OCI: Podman utiliza imágenes compatibles con OCI (como las de Docker Hub)
      y runtimes OCI (como runc o crun), garantizando interoperabilidad.
    • Almacenamiento de Imágenes: A diferencia de Docker, Podman almacena las imágenes
      en directorios locales del usuario (para el modo rootless) o en directorios del sistema (para
      root), lo que significa que las imágenes no se comparten automáticamente entre el usuario
      root y los usuarios estándar, ni entre Docker y Podman si ambos están instalados.

2.3.1.5. Probables Focos de Examen

Para el examen de TAI, es crucial identificar las diferencias arquitectónicas y de seguridad frente
a Docker:
    • Definición de “Daemonless”: Pregunta fundamental. Podman no tiene demonio. Si el
      examen pregunta qué tecnología elimina el “single point of failure” del demonio, la respuesta
      es Podman.
    • Ejecución Rootless por defecto: Aunque Docker puede configurarse en modo rootless, en
      Podman es la configuración nativa y predeterminada. Se basa en User Namespaces.
    • Restricción de Puertos (Privileged Ports): En modo rootless, Podman no puede enlazar
      puertos por debajo del 1024 (puertos privilegiados) sin configuración adicional en el kernel
      (sysctl). Esto es una diferencia operativa clave frente a Docker corriendo como root.
    • Gestión de Imágenes: Podman y Docker tienen almacenes de imágenes separados. Una
      imagen descargada con docker pull no es visible con podman images y viceversa.
    • Relación con Systemd: Podman está diseñado para que sus contenedores sean gestionados
      por systemd (generando unidades .service), mientras que Docker prefiere gestionar sus
      propios reinicios (--restart policy).

2.3.2. LXC/LXD

LXC (Linux Containers) y su evolución moderna, LXD, representan una aproximación a
la virtualización diferente a la de Docker. Mientras que Docker popularizó el concepto de


Bloque IV - Punto 3                          89 de 164                              January 31, 2026
                           Correo electrónico. Contenedores y microservicios


“contenedor de aplicación”, LXC y LXD se centran en el concepto de “contenedor de sistema”
(System Container).

2.3.2.1. LXC: Contenedores de Sistema

LXC es una tecnología de virtualización a nivel de sistema operativo que permite ejecutar múltiples
sistemas Linux aislados (contenedores) sobre un único host de control, compartiendo el mismo
kernel.
      • Filosofía de Diseño: A diferencia de los contenedores de aplicaciones (como Docker) que
        están diseñados para ejecutar un único proceso o servicio, LXC está diseñado para ejecutar
        un sistema operativo completo dentro del contenedor. Esto significa que un contenedor
        LXC arranca su propio sistema de inicio (init, systemd, SysVinit) y puede ejecutar múltiples
        servicios y procesos en segundo plano, comportándose de manera muy similar a una
        Máquina Virtual (VM) tradicional pero sin la sobrecarga de emular hardware.
      • Componentes Técnicos: LXC combina tecnologías del kernel como cgroups (para gestión de
        recursos), namespaces (para aislamiento), y perfiles de seguridad como AppArmor y SELinux
        para proporcionar un entorno seguro y aislado. Se configura habitualmente mediante
        plantillas (templates) que permiten desplegar distribuciones Linux específicas (Ubuntu,
        CentOS, Debian) compartiendo el kernel del anfitrión.

2.3.2.2. LXD: El “Hipervisor” de Contenedores

LXD se define como la extensión moderna de LXC o un “hipervisor de contenedores”. Desarrollado
por Canonical, LXD actúa como una capa de gestión superior sobre LXC para proporcionar una
experiencia de usuario más cercana a la de una nube pública o un entorno de virtualización
tradicional.
      • Arquitectura: LXD funciona mediante un demonio privilegiado (escrito en Go) que expone
        una API REST. Esto permite gestionar los contenedores a través de comandos simples o
        integraciones de red, proporcionando una interfaz unificada para gestionar el ciclo de vida
        de los contenedores.
      • Funcionalidades Avanzadas: LXD introduce capacidades que tradicionalmente estaban
        reservadas para las máquinas virtuales, tales como:
           – Migración en vivo (Live Migration): Capacidad de mover un contenedor en ejecución
             de un host físico a otro sin detener el servicio.
           – Gestión de almacenamiento y red avanzada: Permite gestionar volúmenes de
             almacenamiento y configuraciones de red complejas de forma nativa.
           – Soporte de Máquinas Virtuales: Versiones modernas de LXD también pueden gestionar
             máquinas virtuales completas junto con contenedores, ofreciendo una plataforma
             unificada.
Tabla comparativa: LXC vs. LXD


Característica                     LXC (Linux Containers)             LXD

Rol                                Tecnología base (Userspace         Gestor / Orquestador
                                   tools)                             (“Hipervisor”)
Enfoque                            Contenedor de Sistema              Experiencia tipo VM / Nube
                                   (OS-level)


Bloque IV - Punto 3                            90 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Característica                   LXC (Linux Containers)             LXD

Arquitectura                     Herramientas de línea de           Demonio con API REST
                                 comandos / Plantillas
Gestión                          Local, configuración manual        Clúster, API remota, Migración
                                                                    en vivo


2.3.2.3. Probables Focos de Examen

Para el examen de TAI, es fundamental distinguir claramente entre el propósito de Docker y el de
LXC/LXD.
    • Contenedor de Aplicación vs. Contenedor de Sistema:
         – Si la pregunta describe un entorno para “empaquetar una aplicación y sus dependencias”
           para microservicios, la respuesta es Docker.
         – Si la pregunta describe un entorno para “ejecutar un sistema operativo completo”,
           “sustituir máquinas virtuales ligeras” o “ejecutar múltiples servicios con su propio
           init”, la respuesta es LXC o LXD.
    • Relación LXC/LXD: Es probable que se pregunte cuál es la relación entre ambos. LXD no
      sustituye a LXC, sino que se construye sobre él. LXD utiliza LXC bajo el capó pero mejora la
      gestión y la experiencia de usuario.
    • Migración en vivo: Una característica distintiva de LXD frente a un uso estándar de Docker
      es la capacidad nativa de realizar migración en vivo de contenedores entre nodos, una
      funcionalidad típicamente asociada a hipervisores de hardware.
    • Persistencia: Mientras que los contenedores Docker suelen ser efímeros, los contenedores
      LXC/LXD se tratan a menudo como servidores persistentes (“mascotas” en lugar de “ganado”),
      donde se realizan actualizaciones y mantenimientos dentro del propio contenedor.

2.3.3. containerd

containerd es un tiempo de ejecución de contenedores (container runtime) estándar en la industria,
diseñado con un enfoque en la simplicidad, robustez y portabilidad. Originalmente formaba
parte del motor de Docker, pero fue extraído como un componente independiente y donado a la
Cloud Native Computing Foundation (CNCF), donde alcanzó el estado de proyecto “graduado”.

2.3.3.1. Función y Responsabilidades

A diferencia de Docker, que es una plataforma completa orientada al usuario final, containerd
está diseñado para ser integrado en sistemas más grandes (como Kubernetes o el propio Docker
Engine) en lugar de ser utilizado directamente por desarrolladores.
Su función principal es gestionar el ciclo de vida completo del contenedor en un solo nodo host,
lo que incluye:
  1. Transferencia de imágenes: Gestión de la descarga (pull) y subida (push) de imágenes de
     contenedores.
  2. Almacenamiento: Gestión del almacenamiento de capas de imágenes y sistemas de archivos.
  3. Ejecución: Supervisión de la ejecución de contenedores.
  4. Red: Gestión de interfaces de red básicas y unión de redes.



Bloque IV - Punto 3                          91 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.3.3.2. Arquitectura Interna y Relación con Docker

La arquitectura moderna de Docker se basa en containerd. Cuando el demonio de Docker (dockerd)
necesita ejecutar un contenedor, no lo hace directamente; delega esta tarea a containerd a través
de una API gRPC.
La cadena de ejecución estándar es la siguiente:
  1. Docker Daemon (dockerd): Recibe la orden del usuario (CLI/API) y orquesta la operación de
     alto nivel.
  2. containerd: Recibe la instrucción de dockerd. Gestiona la imagen y prepara la ejecución.
  3. containerd-shim: Es un proceso ligero que se sitúa entre containerd y el contenedor real.
     Permite que containerd se reinicie sin matar los contenedores en ejecución (arquitectura
     desacoplada) y maneja los flujos de E/S (stdin/stdout).
  4. OCI Runtime (runc): containerd utiliza runc para interactuar con el kernel (namespaces y
     cgroups) y crear el contenedor real. Una vez creado el proceso, runc se cierra, dejando al shim
     como padre inmediato.

2.3.3.3. Integración con Kubernetes (CRI)

En el ecosistema de Kubernetes, containerd ha cobrado una importancia crítica tras la deprecación
de dockershim. Kubernetes utiliza la Container Runtime Interface (CRI) para comunicarse con
los tiempos de ejecución de contenedores.
    • Eliminación de Docker: Históricamente, Kubernetes necesitaba un componente adaptador
      llamado dockershim para comunicarse con Docker, ya que Docker no soportaba CRI
      nativamente.
    • Adopción de containerd: containerd implementa nativamente la interfaz CRI (a menudo
      mediante un plugin habilitado por defecto), permitiendo que el kubelet se comunique
      directamente con él sin la sobrecarga del demonio de Docker. Esto reduce la complejidad y
      mejora la estabilidad del clúster.

2.3.3.4. Probables Focos de Examen

Para el examen de TAI, es fundamental entender el rol de containerd como la pieza intermedia
entre la orquestación y el kernel.
    • Diferencia containerd vs. runc:
        – containerd: Es un demonio de alto nivel (High-level runtime). Gestiona imágenes,
          almacenamiento y el ciclo de vida. No interactúa directamente con el kernel para crear
          el contenedor, delega en runc.
        – runc: Es una herramienta CLI de bajo nivel (Low-level runtime) compatible con
          OCI. Su única función es crear y ejecutar el contenedor usando primitivas del kernel
          (namespaces/cgroups) y luego salir.
    • Relación con CNCF: containerd es un proyecto graduado de la CNCF, lo que garantiza su
      neutralidad y estandarización industrial, a diferencia de Docker que es un producto de una
      compañía.
    • Sustitución en Kubernetes: Es probable que se pregunte qué runtime sustituye a Docker en
      entornos Kubernetes modernos. La respuesta estándar es containerd (o CRI-O), debido a
      que elimina la necesidad de dockershim y cumple con la interfaz CRI.
    • Arquitectura de procesos: En un host ejecutando contenedores modernos, se observará un
      proceso containerd persistente y múltiples procesos containerd-shim (uno por contenedor),


Bloque IV - Punto 3                          92 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      pero no necesariamente un proceso dockerd si se usa Kubernetes directamente.

2.4. Orquestación de contenedores
Esta sección marca un punto de inflexión en el temario: pasamos de gestionar contenedores
individuales “a mano” a administrar flotas enteras de aplicaciones distribuidas. Cuando una
infraestructura crece más allá de unos pocos servidores, gestionar el ciclo de vida, la red y la
disponibilidad de cientos de contenedores se vuelve humanamente imposible sin automatización.
La orquestación es el proceso automatizado de gestión, coordinación y organización de sistemas
informáticos complejos y servicios. En el contexto de los contenedores, el orquestador es el
responsable de mantener el “Estado Deseado” (Desired State) del sistema. Si el administrador
declara que debe haber 3 réplicas de un servidor web, el orquestador se encargará de monitorizar
el sistema y, si un contenedor falla, levantará uno nuevo automáticamente para cumplir con la
declaración, logrando así la autoreparación (self-healing).
Aunque Docker Swarm (2.4.6) ofrece una solución nativa y sencilla para clústeres pequeños, la
industria ha adoptado masivamente Kubernetes (K8s) como el estándar de facto debido a su
robustez y extensibilidad. Kubernetes no es solo una herramienta, es casi un sistema operativo
para la nube que abstrae la infraestructura subyacente (física o virtual) para que las aplicaciones
se ejecuten sin importar dónde están alojadas.
A continuación, desglosamos los componentes lógicos de Kubernetes que se estudiarán, usando
una analogía para facilitar su comprensión:

Concepto K8s                     Función Técnica                    Analogía “Mundo Real”

Cluster                          Conjunto de máquinas (nodos)       La flota completa de barcos.
                                 gestionadas.
Control Plane                    Cerebro del clúster (toma          El capitán y el puente de
                                 decisiones globales).              mando.
Node (Worker)                    Máquina donde se ejecutan las      Un barco de carga individual.
                                 cargas de trabajo.
Pod                              La unidad mínima desplegable       Un contenedor de mercancías.
                                 (uno o más contenedores).
Deployment                       Gestiona las réplicas y            El operador de grúa que
                                 versiones de los Pods.             asegura que haya X
                                                                    contenedores.
Service                          Punto de acceso estable y          La ventanilla de recepción
                                 balanceo de carga interno.         única.
Ingress                          Reglas de acceso externo           La aduana o puerta principal
                                 (HTTP/HTTPS).                      del puerto.
ConfigMap/Secret                 Datos de configuración y           La hoja de ruta y las llaves de
                                 claves desacoplados del            la carga.
                                 código.


Para visualizar la arquitectura de Kubernetes (2.4.1), es vital entender la separación entre el

Bloque IV - Punto 3                          93 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


“Cerebro” (Control Plane) y el “Músculo” (Worker Nodes). He preparado el siguiente diagrama
siguiendo tu indicación de definir los nodos explícitamente:




                                Figure 4: Arquitectura en Kubernetes

El dominio de Kubernetes implica aprender una nueva forma de pensar: declarativa en lugar
de imperativa. El administrador define el “qué” (quiero 3 servidores web) en archivos YAML, y
Kubernetes se encarga del “cómo”.

2.4.1. Kubernetes: arquitectura y componentes

Kubernetes (K8s) se define técnicamente como una plataforma de código abierto portable y
extensible para la gestión de cargas de trabajo y servicios en contenedores, que facilita tanto la
configuración declarativa como la automatización. Su arquitectura sigue un modelo de clúster,
compuesto por un plano de control centralizado y un conjunto de nodos de trabajo donde se
ejecutan las aplicaciones.

2.4.1.1. Arquitectura general del clúster

El diseño arquitectónico de Kubernetes se divide en dos planos funcionales claramente
diferenciados que colaboran para mantener el estado deseado del sistema.
  1. Control Plane (Plano de Control): Es el “cerebro” del clúster. Toma decisiones globales (como
     la planificación de recursos), detecta eventos y responde a ellos (por ejemplo, iniciando un

Bloque IV - Punto 3                          94 de 164                             January 31, 2026
                        Correo electrónico. Contenedores y microservicios


     nuevo Pod si el número de réplicas cae por debajo de lo deseado).
  2. Worker Nodes (Nodos de Trabajo): Son las máquinas (físicas o virtuales) que alojan y
     ejecutan las aplicaciones en contenedores. Cada nodo es gestionado por el plano de control y
     contiene los servicios necesarios para ejecutar Pods.
Esquema de arquitectura de alto nivel:
+-------------------------------------------------------+
|                 Kubernetes Cluster                    |
|                                                       |
| +---------------------+     +----------------------+ |
| |     Control Plane    |    |     Worker Node      | |
| | (Master Components) |     |                      | |
| |                      |--->| +-------+ +-------+ | |
| | - API Server         |    | | Pod | | Pod | | |
| | - etcd               |    | +-------+ +-------+ | |
| | - Scheduler          |    |                      | |
| | - Controller Mgr     |    | - Kubelet            | |
| +---------------------+     | - Kube-proxy         | |
|                             | - Container Runtime | |
|                             +----------------------+ |
+-------------------------------------------------------+


2.4.1.2. Componentes del Plano de Control (Control Plane)

Estos componentes suelen ejecutarse en un nodo maestro (Master Node), aunque en entornos de
alta disponibilidad se replican en múltiples nodos.


Componente                      Función Técnica                    Detalles Críticos

kube-apiserver                  Es el front-end del plano de       Es el único componente que
                                control. Expone la API REST        interactúa directamente con
                                de Kubernetes. Valida y            etcd. Todos los demás
                                configura los datos de los         componentes (internos y
                                objetos (Pods, Services, etc.).    externos) se comunican a
                                                                   través de él. Escala
                                                                   horizontalmente.
etcd                            Almacén de datos clave-valor       Es la “fuente de la verdad” del
                                consistente y de alta              clúster. Si etcd se pierde o
                                disponibilidad. Guarda toda la     corrompe, se pierde el estado
                                configuración y el estado del      del clúster. Requiere copias de
                                clúster.                           seguridad estrictas.
kube-scheduler                  Responsable de la                  Toma decisiones basándose en
                                planificación. Observa los         recursos disponibles
                                Pods recién creados que no         (CPU/RAM), restricciones de
                                tienen un nodo asignado y          políticas,
                                selecciona el nodo más             afinidad/antiafinidad y
                                adecuado para ejecutarlos.         taints/tolerations.




Bloque IV - Punto 3                         95 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Componente                       Función Técnica                     Detalles Críticos

kube-controller-manager          Ejecuta los procesos de             Incluye controladores lógicos
                                 controladores en un único           como el Node Controller
                                 binario. Supervisa el estado        (detecta caídas de nodos),
                                 actual del clúster a través del     Replication Controller
                                 API Server y realiza cambios        (mantiene el número de Pods)
                                 para moverlo hacia el estado        y Endpoint Controller.
                                 deseado.
cloud-controller-manager         Componente opcional que             Separa la lógica de interacción
                                 integra el clúster con la API del   con la nube de la lógica
                                 proveedor de la nube (AWS,          interna de Kubernetes.
                                 Azure, GCP).                        Gestiona balanceadores de
                                                                     carga y volúmenes de nube.


2.4.1.3. Componentes del Nodo (Worker Node)

Estos componentes se ejecutan en cada nodo del clúster y son responsables del entorno de
ejecución de los contenedores y la comunicación de red.
  1. kubelet: Es el agente principal que se ejecuta en cada nodo.
        • Función: Asegura que los contenedores estén ejecutándose dentro de los Pods. Toma
          un conjunto de especificaciones de Pods (normalmente del API Server) y garantiza que
          los contenedores descritos estén funcionando y saludables.
        • Interacción: Se comunica con el Container Runtime a través de la interfaz CRI (Container
          Runtime Interface).
  2. kube-proxy: Es un proxy de red que se ejecuta en cada nodo.
        • Función: Gestiona las reglas de red en el nodo. Permite la comunicación de red hacia
          los Pods desde dentro o fuera del clúster.
        • Implementación: Utiliza mecanismos del kernel del sistema operativo como iptables o
          IPVS para el enrutamiento de tráfico.
  3. Container Runtime (Tiempo de ejecución de contenedores): Es el software responsable de
     ejecutar los contenedores.
        • Soporte: Kubernetes soporta varios runtimes compatibles con la interfaz CRI, como
          containerd, CRI-O, y Docker Engine (mediante adaptadores en versiones antiguas).

2.4.1.4. Probables Focos de Examen

En las oposiciones a TAI, la arquitectura de Kubernetes es un tema recurrente. Preste atención a
las siguientes distinciones técnicas:
    • La función única de etcd: Es vital recordar que etcd es el único lugar donde se persiste el
      estado del clúster. El API Server es “stateless” (sin estado) y delega el almacenamiento en
      etcd. Una pregunta clásica versa sobre qué componente debe respaldarse para recuperar un
      clúster: la respuesta es etcd.
    • Comunicación centralizada: Los componentes del nodo (kubelet) y otros componentes del
      plano de control (scheduler) no hablan entre sí directamente ni hablan con etcd directamente;
      todos pasan a través de kube-apiserver.
    • Diferencia entre Scheduler y Controller Manager:


Bloque IV - Punto 3                          96 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


        – Si la pregunta trata sobre “seleccionar un nodo” o “asignar recursos”, es el kube-
          scheduler.
        – Si la pregunta trata sobre “mantener el número de réplicas” o “detectar un nodo caído”,
          es el kube-controller-manager.
    • Naturaleza del Pod: El Pod es la unidad mínima desplegable en Kubernetes, no el contenedor.
      Un Pod puede contener uno o más contenedores que comparten almacenamiento y red
      (misma IP).
    • Relación Kubelet/Runtime: El kubelet es el “jefe” del nodo que recibe órdenes, pero
      quien realmente ejecuta los procesos de los contenedores es el Container Runtime (como
      containerd).

2.4.2. Pods, deployments y services

En la arquitectura de Kubernetes, la gestión de cargas de trabajo se realiza a través de abstracciones
de alto nivel que desacoplan la definición de la aplicación de la infraestructura subyacente. Los
tres conceptos fundamentales para definir, ejecutar y exponer aplicaciones son los Pods, los
Deployments y los Services.

2.4.2.1. Pods: La unidad atómica de planificación

El Pod es la unidad de ejecución más pequeña y básica que se puede crear y gestionar en Kubernetes.
A diferencia de otros sistemas donde la unidad mínima es el contenedor, Kubernetes utiliza el
Pod como una envolvente lógica.
Características técnicas principales:
  1. Agrupación de contenedores: Un Pod encapsula uno o más contenedores (aunque lo
     más común es uno solo, conocido como single-container pod). Cuando existen múltiples
     contenedores en un mismo Pod (patrones sidecar, adapter o ambassador), estos están
     fuertemente acoplados y siempre se programan en el mismo nodo físico o virtual.
  2. Recursos compartidos: Todos los contenedores dentro de un Pod comparten el mismo
     contexto de ejecución, lo que incluye:
        • Networking: Comparten el mismo espacio de nombres de red (Network Namespace) y,
          por tanto, la misma dirección IP. Los contenedores dentro del Pod se comunican entre
          sí a través de localhost.
        • Almacenamiento: Pueden montar los mismos volúmenes compartidos para
          intercambiar datos.
        • IPC y UTS: Comparten espacios de nombres para comunicación entre procesos y nombre
          de host.
  3. Infraestructura subyacente: Técnicamente, la “magia” de compartir el espacio de nombres
     de red se logra mediante un contenedor de infraestructura invisible llamado “pause
     container”, que mantiene el namespace abierto para el resto de contenedores del Pod.
  4. Efimeridad: Los Pods son efímeros por diseño. Tienen un ciclo de vida definido: se crean, se
     les asigna un ID único (UID) y se ejecutan en un nodo hasta que finalizan o son eliminados.
     Si un nodo muere, los Pods que corrían en él se pierden y deben ser reemplazados (no
     resucitados) por el controlador correspondiente.

2.4.2.2. Deployments: Gestión declarativa del estado

Un Deployment es una abstracción de nivel superior que gestiona la creación y actualización de
Pods de manera declarativa. En lugar de crear Pods manualmente, el usuario describe el estado


Bloque IV - Punto 3                           97 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


deseado en un manifiesto (YAML) y el controlador del Deployment se encarga de cambiar el estado
actual hacia el deseado.
Jerarquía y funcionamiento interno: El Deployment no gestiona los Pods directamente, sino que
gestiona un ReplicaSet.
    • Deployment → Gestiona versiones y actualizaciones.
    • ReplicaSet → Asegura que el número de réplicas (copias) del Pod esté siempre en ejecución.
    • Pod → Ejecuta la carga de trabajo.
Funcionalidades clave:
  1. Self-healing (Auto-recuperación): Si un Pod falla o se elimina, el ReplicaSet subyacente crea
     uno nuevo automáticamente para mantener el número de réplicas especificado.
  2. Estrategias de despliegue: Permite actualizar aplicaciones sin tiempo de inactividad (zero-
     downtime). Las estrategias principales son:
        • RollingUpdate (Por defecto): Actualiza los Pods de forma incremental (uno a uno o en
          lotes), manteniendo siempre una parte de la aplicación disponible. Utiliza parámetros
          como maxSurge (cuántos Pods extra se pueden crear) y maxUnavailable (cuántos pueden
          estar no disponibles).
        • Recreate: Elimina todos los Pods antiguos antes de crear los nuevos. Implica tiempo de
          inactividad, pero garantiza que no convivan dos versiones distintas de la aplicación.
  3. Rollbacks: Permite volver a una versión anterior de la aplicación si se detecta un fallo en la
     nueva versión, ya que Kubernetes mantiene un historial de las revisiones del Deployment.

2.4.2.3. Services: Exposición y descubrimiento de servicios

Dado que los Pods son efímeros y sus direcciones IP cambian al ser recreados, Kubernetes utiliza
el objeto Service para proporcionar un punto de entrada estable y constante.
Concepto y función: Un Service define un conjunto lógico de Pods y una política para acceder a
ellos. Actúa como un balanceador de carga interno frente a los Pods.
    • Selección de Pods: La vinculación entre un Service y los Pods se realiza mediante Labels
      (Etiquetas) y Selectors (Selectores). El Service enviará tráfico a cualquier Pod que tenga las
      etiquetas que coincidan con su selector.
Tipos de Servicios (ServiceTypes): Kubernetes ofrece diferentes tipos de servicios según la
visibilidad necesaria:

Tipo de Servicio                  Descripción y Visibilidad         Caso de Uso

ClusterIP                         Por defecto. Asigna una IP        Bases de datos internas,
                                  virtual accesible solo dentro     backends no públicos.
                                  del clúster. Es el mecanismo
                                  estándar para la comunicación
                                  entre microservicios internos.
NodePort                          Abre un puerto estático (rango    Acceso externo simple o para
                                  30000-32767 por defecto) en       balanceadores externos
                                  la IP de cada nodo del clúster.   propios.
                                  El tráfico que llega a
                                  IP_Nodo:Puerto se redirige al
                                  Servicio.

Bloque IV - Punto 3                          98 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Tipo de Servicio                  Descripción y Visibilidad         Caso de Uso

LoadBalancer                      Solicita al proveedor de nube     Exposición pública en
                                  (AWS, Azure, GCP) que             entornos Cloud gestionados.
                                  provisione un balanceador de
                                  carga externo nativo.
                                  Proporciona una IP pública
                                  fija.
ExternalName                      Mapea el servicio a un nombre     Acceder a servicios externos
                                  DNS externo (devuelve un          (ej. base de datos RDS) usando
                                  registro CNAME), no tiene IP      nombre interno de K8s.
                                  virtual ni proxy.


Adicionalmente, existe el concepto de Headless Service (ClusterIP configurado como None). Este
no tiene una IP virtual única ni balanceo de carga; en su lugar, devuelve las IPs de los Pods
directamente a través de DNS, siendo útil para aplicaciones con estado (StatefulSets) que necesitan
identificar instancias específicas.

2.4.2.4. Probables Focos de Examen

En las preguntas de oposiciones para TAI sobre orquestación, es fundamental dominar las
relaciones y diferencias entre estos objetos:
    • Relación Pod/Contenedor: Un Pod puede contener múltiples contenedores, pero un
      contenedor no puede contener múltiples Pods. Los contenedores dentro de un mismo Pod
      comparten siempre la IP y los puertos (red localhost). Pregunta trampa habitual: “¿Tienen
      los contenedores de un mismo Pod IPs diferentes?”. Respuesta: No.
    • Objeto para persistencia/estado: Los Deployments son ideales para aplicaciones sin estado
      (stateless). Para aplicaciones con estado (bases de datos), se debe usar StatefulSet.
    • Vinculación Service-Pod: Recordar que la asociación no es por nombre ni ID, sino
      exclusivamente mediante Labels y Selectores. Si las etiquetas no coinciden, el servicio no
      tendrá endpoints.
    • Visibilidad ClusterIP vs NodePort:
         – Si la pregunta pide exponer una aplicación al exterior del clúster, la respuesta correcta
           suele ser NodePort o LoadBalancer (o Ingress), nunca ClusterIP.
         – ClusterIP es estrictamente interno.
    • Unidad mínima de escalado: Kubernetes escala añadiendo más Pods (replicas), no
      añadiendo más contenedores dentro de un mismo Pod.

2.4.3. ConfigMaps y Secrets

La gestión de la configuración en Kubernetes se basa en el principio de desacoplar los artefactos
de código de la configuración. Esto permite que las imágenes de contenedor sean inmutables y
portables entre diferentes entornos (desarrollo, pruebas, producción), inyectando la configuración
específica en tiempo de ejecución. Para ello, Kubernetes proporciona dos objetos API nativos:
ConfigMaps y Secrets.




Bloque IV - Punto 3                          99 de 164                               January 31, 2026
                        Correo electrónico. Contenedores y microservicios


2.4.3.1. ConfigMaps: Configuración no confidencial

Un ConfigMap es un objeto de la API utilizado para almacenar datos no confidenciales en pares
clave-valor. Los Pods pueden consumir ConfigMaps como variables de entorno, argumentos de
línea de comandos o como archivos de configuración en un volumen.
    • Estructura: Contiene un campo data donde se definen las claves y valores. Puede almacenar
      desde cadenas simples hasta archivos de configuración completos (como un server.xml o
      nginx.conf).
    • Propósito: Desacoplar la configuración de la imagen del contenedor para mantener la
      portabilidad.
    • Alcance: Es un recurso con espacio de nombres (namespaced). Un Pod solo puede
      referenciar ConfigMaps que residan en su mismo Namespace.

2.4.3.2. Secrets: Gestión de información sensible

Los Secrets son objetos similares a los ConfigMaps pero diseñados específicamente para contener
cantidades pequeñas de información sensible, como contraseñas, tokens OAuth, claves SSH o
certificados TLS.
Características Técnicas Diferenciales:
  1. Codificación Base64: Por defecto, los datos en un Secret se almacenan codificados en Base64
     dentro del campo data del manifiesto YAML. Esto permite almacenar datos binarios, pero
     no es un método de encriptación ni una medida de seguridad robusta por sí misma.
  2. Tipos de Secrets: Kubernetes define varios tipos estándar para validar el formato de los
     datos:
        • Opaque: Tipo por defecto para datos arbitrarios (pares clave-valor).
        • kubernetes.io/service-account-token: Token para identificar al Pod ante la API.
        • kubernetes.io/dockercfg o kubernetes.io/dockerconfigjson: Credenciales para
          descargar imágenes de registros privados.
        • kubernetes.io/tls: Almacena certificados y claves privadas (tls.crt, tls.key).
  3. Almacenamiento en Nodo: Cuando se monta un Secret en un Pod, este se almacena en un
     sistema de archivos en memoria (tmpfs) en el nodo, no en el disco físico, para reducir el
     riesgo de robo de datos.
Entrada de datos (stringData vs data): Para facilitar la creación, se puede usar el campo
stringData en el YAML para introducir valores en texto plano. Kubernetes los codificará
automáticamente a Base64 y los moverá al campo data al persistir el objeto.

2.4.3.3. Mecanismos de consumo en Pods

Tanto ConfigMaps como Secrets pueden inyectarse en los contenedores de dos formas principales,
con implicaciones importantes en el ciclo de vida de la aplicación:
Tabla comparativa de métodos de inyección




Bloque IV - Punto 3                        100 de 164                            January 31, 2026
                          Correo electrónico. Contenedores y microservicios



                                                                     Comportamiento ante
Método                             Descripción                       actualizaciones

Variables de Entorno (env,         Los valores se inyectan como      Estático. Si se actualiza el
envFrom)                           variables del sistema operativo   ConfigMap/Secret, el valor en
                                   al arrancar el contenedor.        el contenedor no cambia. Se
                                                                     requiere reiniciar el Pod para
                                                                     reflejar los cambios.
Volúmenes (volumeMounts)           Se monta el objeto como un        Dinámico (Hot Reload).
                                   directorio. Cada clave se         Kubernetes actualiza
                                   convierte en un archivo y el      automáticamente los archivos
                                   valor en su contenido.            en el volumen cuando cambia
                                                                     el recurso (con un leve retraso).
                                                                     La aplicación debe estar
                                                                     programada para detectar el
                                                                     cambio en el archivo.


2.4.3.4. Seguridad, cifrado y limitaciones

La seguridad de los Secrets es un punto crítico en la administración de Kubernetes.
  1. Cifrado en reposo (Encryption at Rest): Por defecto, los Secrets se almacenan en etcd (la base
     de datos del clúster) simplemente codificados en Base64 (texto plano). Cualquier persona
     con acceso a la API de etcd o a los archivos del sistema del nodo maestro puede leerlos.
          • Solución: Se debe configurar el EncryptionConfiguration en el kube-apiserver para
            usar proveedores de cifrado como aesgcm, aescbc o un KMS (Key Management Service)
            externo (como AWS KMS, Azure Key Vault, etc.) para cifrar los datos antes de escribirlos
            en etcd.
  2. Control de Acceso (RBAC): Es fundamental restringir mediante RBAC qué usuarios o
     ServiceAccounts pueden hacer get, list o watch sobre los Secrets, ya que esto revela su
     contenido decodificado.
  3. Límite de tamaño: Debido a limitaciones en el almacenamiento subyacente (etcd), el tamaño
     máximo de un ConfigMap o Secret es de 1 MB.
  4. Inmutabilidad: Desde versiones recientes, se puede marcar un ConfigMap o Secret como
     immutable: true. Esto protege contra modificaciones accidentales y mejora el rendimiento
     del clúster al reducir la carga en el servidor API (ya que no necesita vigilar cambios).

2.4.3.5. Probables Focos de Examen

Para el examen de TAI, preste especial atención a las diferencias técnicas y de seguridad:
    • Codificación vs. Encriptación: Es una pregunta trampa clásica. Los Secrets NO están
      encriptados por defecto, solo codificados en Base64. Base64 es un esquema de codificación,
      no de seguridad.
    • StringData: Recuerde que el campo stringData es “write-only” (solo escritura). Se usa para
      crear/actualizar el Secret en texto plano, pero al consultarlo (kubectl get secret -o yaml),
      solo se verá el campo data codificado.



Bloque IV - Punto 3                           101 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Actualización en caliente: Si preguntan cómo actualizar la configuración de una aplicación
      sin reiniciar el Pod, la respuesta es usar ConfigMaps montados como Volúmenes (y que la
      aplicación soporte la recarga de archivos). Las variables de entorno nunca se actualizan en
      caliente.
    • Tmpfs: Los Secrets montados como volumen se escriben en memoria RAM (tmpfs), nunca
      en el disco duro del nodo, para evitar que queden rastros forenses.
    • ConfigMap vs Secret:
         – Si son datos de configuración general (URL de base de datos, nivel de log): ConfigMap.
         – Si son credenciales, certificados o claves: Secret.

2.4.4. Namespaces

Los Namespaces (espacios de nombres) son un mecanismo fundamental de Kubernetes para
dividir un único clúster físico en múltiples clústeres virtuales. Proporcionan un ámbito para los
nombres de los recursos, garantizando que los nombres de los objetos (como Pods o Servicios)
sean únicos dentro de un namespace, aunque no necesariamente a través de todo el clúster.

2.4.4.1. Definición y función lógica

Los namespaces actúan como fronteras lógicas de organización y seguridad. Son esenciales en
entornos con muchos usuarios distribuidos en múltiples equipos o proyectos, permitiendo la
multitenencia (multitenancy) ligera.
Sus funciones principales son:
  1. Scope (Ámbito): Evitan colisiones de nombres. Por ejemplo, dos equipos pueden tener un
     despliegue llamado mi-app siempre que estén en namespaces diferentes.
  2. Organización: Permiten separar entornos (desarrollo, pruebas, producción) dentro de la
     misma infraestructura física.
  3. Control de Acceso: Sirven como límite para aplicar políticas de autorización (RBAC),
     definiendo quién puede acceder o modificar recursos en esa partición específica.

2.4.4.2. Namespaces predeterminados

Al iniciar un clúster de Kubernetes, se crean automáticamente varios namespaces iniciales:
    • default: Es el namespace predeterminado para los objetos que no especifican uno.
    • kube-system: Reservado para los objetos creados por el sistema Kubernetes (como el DNS,
      el proxy o los controladores). Evita que los usuarios modifiquen o borren accidentalmente
      componentes críticos del sistema.
    • kube-public: Es un namespace especial que es legible por todos los usuarios (incluso los
      no autenticados). Se usa para recursos que deben ser visibles en todo el clúster, como
      información de descubrimiento.

2.4.4.3. Alcance de los recursos y direccionamiento DNS

Es crucial distinguir qué recursos pertenecen a un namespace y cuáles son globales al clúster.
Clasificación de recursos por alcance:




Bloque IV - Punto 3                         102 de 164                            January 31, 2026
                        Correo electrónico. Contenedores y microservicios



Tipo de Recurso                  Alcance                           Ejemplos

Namespaced                       Pertenecen a un namespace         Pods, Services, Deployments,
                                 específico.                       ReplicaSets, Secrets,
                                                                   ConfigMaps, PVCs.
Cluster-scoped                   Globales, no pertenecen a         Nodes, PersistentVolumes
                                 ningún namespace.                 (PV), Namespaces,
                                                                   ClusterRoles.


Direccionamiento DNS: Los Servicios dentro de un namespace obtienen una entrada DNS
específica. El formato del FQDN (Fully Qualified Domain Name) incluye el nombre del namespace,
lo que permite la comunicación cruzada si se conoce la dirección completa:
Wait for it... <nombre-servicio>.<nombre-namespace>.svc.cluster.local.


2.4.4.4. Aislamiento y Cuotas

Aunque los namespaces proporcionan aislamiento lógico, este no es total por defecto:
  1. Aislamiento de Recursos (ResourceQuotas): Los administradores pueden definir objetos
     ResourceQuota asociados a un namespace. Esto permite limitar el consumo agregado de
     recursos (CPU, memoria, almacenamiento) y el conteo de objetos (número de Pods, Servicios)
     dentro de ese namespace. Esto evita que un inquilino acapare todos los recursos del clúster
     físico (“noisy neighbor problem”).
  2. Aislamiento de Red (Network Policies): Importante: Por defecto, los namespaces no aíslan
     el tráfico de red. Un Pod en el namespace desarrollo puede enviar tráfico a un Pod en
     producción si conoce su IP. Para restringir la comunicación entre namespaces, es obligatorio
     implementar NetworkPolicies.
  3. Control de Acceso (RBAC): Mediante Role y RoleBinding, se pueden limitar las acciones de
     un usuario o cuenta de servicio a un namespace específico, sin otorgarle permisos en otros.

2.4.4.5. Probables Focos de Examen

En el examen de TAI, es frecuente que se evalúen los límites del aislamiento que proporcionan los
namespaces.
    • Falta de aislamiento de red por defecto: Es una pregunta trampa clásica. Crear un
      namespace no impide que los Pods de otros namespaces se comuniquen con él. Se requiere
      explícitamente una NetworkPolicy para denegar el tráfico entre namespaces.
    • Recursos que NO tienen namespace: Hay que memorizar que los Nodos y los Volúmenes
      Persistentes (PV) son recursos globales del clúster y no pertenecen a ningún namespace (a
      diferencia de los PVC que sí son namespaced).
    • Resolución DNS entre namespaces: Se puede preguntar cómo un servicio en el namespace A
      contacta a un servicio en el namespace B. La respuesta implica usar el nombre DNS completo
      (FQDN): servicio.namespaceB.svc.cluster.local.
    • ResourceQuota: Es el objeto utilizado para limitar la cantidad de CPU/RAM o número de
      Pods que se pueden crear dentro de un namespace específico.
    • Namespace kube-system: Identificarlo como el lugar donde residen los componentes críticos
      del plano de control y add-ons del sistema.

Bloque IV - Punto 3                        103 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.4.5. Ingress y balanceo de carga

La gestión del tráfico externo (“norte-sur”) hacia el clúster es uno de los aspectos más críticos
en la orquestación de contenedores. Mientras que los objetos Service (ClusterIP, NodePort)
resuelven la conectividad básica, Ingress surge como la solución estándar para gestionar el acceso
HTTP/HTTPS a nivel de aplicación (Capa 7), ofreciendo capacidades avanzadas de enrutamiento y
seguridad que no poseen los balanceadores de carga tradicionales de Capa 4.

2.4.5.1. Concepto y distinción de capas (L4 vs L7)

Es fundamental distinguir entre los mecanismos de exposición basándose en el modelo OSI:
  1. Balanceo de Carga L4 (Service type LoadBalancer):
        • Opera en la capa de transporte (TCP/UDP).
        • No inspecciona el contenido del paquete; simplemente reenvía tráfico basándose en
          direcciones IP y puertos.
        • Es ineficiente en costes y gestión si se requiere exponer múltiples servicios, ya que
          generalmente provisiona un balanceador de carga físico o de nube (con su propia IP
          pública) por cada servicio expuesto.
  2. Balanceo de Carga L7 (Ingress):
        • Opera en la capa de aplicación (HTTP/HTTPS).
        • Actúa como un proxy inverso inteligente que inspecciona las peticiones HTTP.
        • Permite la consolidación: un único balanceador de carga (y una única IP pública) puede
          enrutar tráfico a múltiples servicios internos basándose en el nombre de dominio (Host)
          o la ruta (Path).

2.4.5.2. El recurso Ingress

El Ingress es un objeto de la API de Kubernetes que define un conjunto de reglas de enrutamiento
para gestionar el acceso externo a los servicios del clúster.
Sus funciones principales incluyen:
    • Enrutamiento basado en contenido: Redirige el tráfico a diferentes servicios basándose
      en el host (ej. api.midominio.com vs web.midominio.com) o en el path de la URL (ej. /app1 vs
      /app2).
    • Terminación SSL/TLS: Desacopla la seguridad de la aplicación. El Ingress maneja los
      certificados y el descifrado del tráfico HTTPS, enviando tráfico descifrado (o re-encriptado)
      a los Pods, liberando recursos en la aplicación.
    • Visibilidad y seguridad: Proporciona un punto centralizado para aplicar autenticación,
      protección WAF (Web Application Firewall) y monitorización de tráfico.
Ejemplo de estructura de un Ingress: Un manifiesto típico define reglas donde se especifica el
host, el path y el backend (nombre del servicio y puerto) al que se debe dirigir el tráfico.


2.4.5.3. Ingress Controller

Un punto crítico de arquitectura es que el recurso Ingress por sí solo es una mera definición
de configuración; no hace nada sin un componente que lo implemente. Este componente es el
Ingress Controller.
    • Funcionamiento: El Ingress Controller es un demonio (pod) que se ejecuta en el clúster,
      vigila el servidor API en busca de nuevos recursos Ingress o cambios en los existentes, y


Bloque IV - Punto 3                         104 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      reconfigura automáticamente un balanceador de carga software (como NGINX o HAProxy)
      para cumplir con esas reglas.
    • Implementaciones: Kubernetes no incluye un controlador por defecto. Existen múltiples
      opciones de código abierto y comerciales, siendo NGINX Ingress Controller la más extendida,
      seguida de otras como Traefik, HAProxy o Contour.
    • Integración en Nube: En entornos cloud (AWS, GKE, Azure), el Ingress Controller puede
      actuar como un adaptador que provisiona y configura los balanceadores de carga nativos de
      la nube (ej. ALB en AWS).

2.4.5.4. Gateway API (Evolución)

La Gateway API es una evolución moderna del estándar Ingress diseñada para superar sus
limitaciones. Mientras que Ingress se centra en HTTP, la Gateway API modela el tráfico de manera
más genérica (L4 y L7), permitiendo enrutamiento basado en cabeceras HTTP, métodos y otros
atributos avanzados, proporcionando una API más expresiva y orientada a roles.

2.4.5.5. Probables Focos de Examen

En el contexto de oposiciones para TAI, las preguntas sobre este apartado suelen centrarse en la
arquitectura y las diferencias funcionales:
  1. Diferencia Ingress vs. LoadBalancer:
        • Pregunta tipo: “¿Qué objeto permite exponer múltiples servicios HTTP bajo una única
          dirección IP pública usando rutas diferentes?”
        • Respuesta: Ingress. El tipo LoadBalancer asigna una IP por servicio (relación 1:1),
          mientras que Ingress permite relación 1:N (fan-out).
  2. Necesidad del Controlador:
        • Concepto clave: Crear un recurso Ingress sin tener instalado un Ingress Controller no
          tendrá ningún efecto. El recurso quedará pendiente y no se enrutará tráfico. Es una
          “trampa” habitual en preguntas prácticas.
  3. Terminación TLS:
        • Se suele preguntar dónde se configura el certificado SSL para exponer un servicio
          HTTPS. La respuesta estándar es en el recurso Ingress (usando un Secret de tipo
          kubernetes.io/tls), permitiendo la terminación TLS en el borde del clúster.
  4. Backend por defecto:
        • Si una petición no coincide con ninguna regla definida en el Ingress, el tráfico se envía
          a un default backend (generalmente una página 404), que debe estar definido o el
          controlador proporcionará uno genérico.
  5. Ámbito de red:
        • Ingress gestiona tráfico Norte-Sur (entra y sale del clúster). No se utiliza para tráfico
          Este-Oeste (comunicación entre servicios dentro del clúster), para lo cual se usan los
          objetos Service o un Service Mesh.

2.4.6. Docker Swarm

Docker Swarm (o más precisamente, el “modo Swarm”) es la herramienta de orquestación nativa
integrada directamente en el motor de Docker. Permite gestionar un grupo de hosts de Docker
como si fueran un único sistema virtual o clúster, facilitando la automatización del despliegue, el
escalado y la gestión de aplicaciones en contenedores a través de múltiples máquinas.
A diferencia de otras soluciones que requieren instalación externa, Swarm está integrado en el


Bloque IV - Punto 3                         105 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


binario estándar de docker desde la versión 1.12, ofreciendo una experiencia de uso simplificada
(“batteries included”).

2.4.6.1. Arquitectura y roles del nodo

La arquitectura de Swarm se basa en un clúster de nodos físicos o virtuales que ejecutan el motor
de Docker. Existen dos roles jerárquicos fundamentales para los nodos dentro del clúster:
  1. Nodos Manager (Gestores):
       • Son responsables de las actividades de orquestación y mantenimiento del estado del
         clúster.
       • Utilizan el algoritmo de consenso Raft para mantener un estado consistente y tolerante
         a fallos. Se recomienda un número impar de managers para garantizar el quórum.
       • Gestionan la planificación (scheduling) de tareas, asignando contenedores a los nodos
         trabajadores disponibles.
       • Proporcionan la API HTTP para la gestión del clúster.
  2. Nodos Worker (Trabajadores):
       • Su función principal es recibir y ejecutar las tareas (contenedores) asignadas por los
         managers.
       • Un nodo Manager es, por defecto, también un Worker, aunque puede configurarse para
         no ejecutar tareas.
       • Los nodos se pueden promocionar (de Worker a Manager) o degradar dinámicamente.
Tabla de comandos de gestión de clúster


Comando                          Acción                             Contexto

docker swarm init                Inicializa un nuevo clúster y      Creación
                                 convierte el nodo actual en
                                 Manager.
docker swarm join                Une un nodo existente a un         Unión
                                 clúster como Worker o
                                 Manager (requiere token).
docker node ls                   Lista los nodos del clúster y su   Monitorización
                                 estado.
docker node promote/demote       Cambia el rol de un nodo entre     Gestión
                                 Manager y Worker.


2.4.6.2. Conceptos operativos: Servicios, Tareas y Stacks

Para gestionar la carga de trabajo, Swarm introduce abstracciones específicas sobre los
contenedores tradicionales:
  1. Servicio (Service): Es la unidad principal de despliegue en Swarm. Define el estado deseado
     de una aplicación (imagen a usar, puertos, redes y número de réplicas). El orquestador se
     asegura de que el estado actual del clúster coincida con este estado deseado (reconciliación).
          • Comando: docker service create.



Bloque IV - Punto 3                         106 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  2. Tarea (Task): Es la unidad atómica de planificación. Una tarea corresponde a un contenedor
     específico desplegado en un nodo y los metadatos asociados a su ejecución. Los usuarios
     gestionan servicios, mientras que Swarm gestiona tareas.
  3. Stack (Pila): Es un grupo de servicios interrelacionados que comparten dependencias, redes
     y volúmenes. Se definen mediante un fichero docker-compose.yml (versión 3 o superior) y
     se despliegan de forma atómica.
          • Comando: docker stack deploy.

2.4.6.3. Redes Overlay y “Routing Mesh”

Swarm implementa modelos de red avanzados para permitir la comunicación transparente entre
contenedores distribuidos en diferentes hosts físicos:
  1. Red Overlay (Superpuesta): Crea una red virtual distribuida sobre los múltiples hosts
     del clúster. Utiliza tecnología VXLAN para encapsular el tráfico, permitiendo que los
     contenedores en diferentes nodos se comuniquen de forma segura (opcionalmente cifrada)
     como si estuvieran en la misma red local.
  2. Malla de Enrutamiento (Routing Mesh): Es un mecanismo de balanceo de carga para el
     tráfico entrante (Ingress).
          • Permite exponer un puerto de servicio al exterior.
          • Swarm expone ese puerto en todos los nodos del clúster, independientemente de si el
            nodo está ejecutando una réplica de ese servicio o no.
          • Cualquier petición recibida en el puerto publicado de cualquier nodo es enrutada
            automáticamente mediante IPVS a un contenedor activo del servicio correspondiente,
            balanceando la carga.

2.4.6.4. Probables Focos de Examen

En las oposiciones para TAI, las preguntas sobre Docker Swarm suelen contrastar su arquitectura
con la de un simple contenedor o con Kubernetes.
    • Diferencia Swarm vs. Swarm Mode: Es fundamental saber que el “Swarm Mode” actual está
      integrado en el Docker Engine y no requiere instalación adicional, a diferencia del producto
      “Docker Swarm” antiguo (standalone) que está deprecado.
    • Algoritmo de Consenso: Se suele preguntar qué algoritmo utilizan los nodos Manager para
      mantener el estado del clúster. La respuesta es Raft.
    • Routing Mesh: Un concepto muy preguntado es la capacidad de acceder a un servicio a
      través de la IP de un nodo que no está ejecutando el contenedor. Esto es posible gracias al
      Routing Mesh (red ingress).
    • Definición de Stack: Los Stacks en Swarm se definen utilizando archivos en formato Docker
      Compose (YAML), no con manifiestos propietarios exclusivos.
    • Token de unión: Para unir un nodo al clúster (docker swarm join), es necesario un token
      criptográfico que determina si el nodo se une como worker o manager. Este token se genera
      en el Manager.

2.5. Seguridad en contenedores
Este último apartado aborda uno de los aspectos más críticos y a menudo descuidados en la
adopción de contenedores: la seguridad. A diferencia de las máquinas virtuales, que ofrecen un


Bloque IV - Punto 3                         107 de 164                             January 31, 2026
                          Correo electrónico. Contenedores y microservicios


aislamiento robusto por hardware, los contenedores comparten el núcleo del sistema operativo
anfitrión. Esto implica que una vulnerabilidad en un solo contenedor mal configurado podría
comprometer todo el nodo y, por extensión, afectar a otros servicios vecinos.
La seguridad en este entorno no es un producto que se instala al final, sino un proceso continuo
que debe integrarse en cada fase del ciclo de vida de la aplicación, un enfoque conocido
como DevSecOps. El administrador debe cambiar su mentalidad de defensa perimetral
(firewall tradicional) a una defensa en profundidad y granular, ya que en una arquitectura de
microservicios el tráfico “este-oeste” (entre contenedores) es tan importante como el tráfico
“norte-sur” (entrada/salida).
Para estructurar la defensa, la industria utiliza el modelo de las “4 C de la Seguridad Cloud Native”.
Si una capa externa es vulnerable, las capas internas quedan expuestas.




                               Figure 5: 4 C de la Seguridad Cloud Native

El temario de esta sección se desarrolla cubriendo estas capas mediante estrategias específicas de
prevención y control:


Punto del Temario                 Fase de Acción                       Objetivo de Seguridad

2.5.1. Buenas Prácticas           Diseño y Ejecución                   Minimizar la superficie de
                                                                       ataque (ej. usar imágenes
                                                                       ligeras distroless, no ejecutar
                                                                       como root, sistemas de
                                                                       ficheros de solo lectura).
2.5.2. Escaneo de                 Construcción (Build)                 Detectar CVEs (Common
Vulnerabilidades                                                       Vulnerabilities and Exposures)
                                                                       en las librerías y dependencias
                                                                       de la imagen antes de que
                                                                       llegue a producción.




Bloque IV - Punto 3                           108 de 164                                January 31, 2026
                          Correo electrónico. Contenedores y microservicios



Punto del Temario                 Fase de Acción                     Objetivo de Seguridad

2.5.3. Políticas de Red           Ejecución (Runtime)               Microsegmentación.
                                                                    Implementar un modelo de
                                                                    “Zero Trust” donde ningún
                                                                    contenedor puede hablar con
                                                                    otro salvo que esté
                                                                    explícitamente autorizado.
2.5.4. Control de Acceso          Gestión                            RBAC (Role-Based Access
                                                                     Control). Limitar quién puede
                                                                     crear, borrar o ver recursos en
                                                                     el clúster (principio de
                                                                     mínimo privilegio).


El objetivo final es garantizar la inmutabilidad de la infraestructura: en lugar de parchear un
contenedor en ejecución (lo cual es una mala práctica), se corrige la imagen base, se reconstruye y
se despliega una nueva versión, asegurando que el código en producción sea siempre idéntico al
auditado.

2.5.1. Buenas prácticas de seguridad

La seguridad en entornos de contenedores requiere un cambio de paradigma respecto a la
seguridad tradicional de servidores. Debido a la naturaleza efímera, dinámica y compartida de
los contenedores, se debe adoptar una estrategia de defensa en profundidad y un modelo de
confianza cero (Zero Trust).
El modelo de seguridad nativo de la nube se suele estructurar en cuatro capas, conocido como el
modelo de las 4C: Cloud (Nube), Cluster (Clúster), Container (Contenedor) y Code (Código).

2.5.1.1. Seguridad a nivel de Host y Sistema Operativo

El host es la base crítica; si el kernel del host se ve comprometido, todos los contenedores que se
ejecutan sobre él están en riesgo debido al kernel compartido.
  1. Uso de Sistemas Operativos Específicos para Contenedores: Se recomienda utilizar sistemas
     operativos minimalistas diseñados explícitamente para ejecutar contenedores (ej. CoreOS,
     Alpine, Bottlerocket). Estos sistemas tienen una superficie de ataque reducida, deshabilitan
     servicios innecesarios y a menudo configuran el sistema de archivos como de solo lectura.
  2. Aislamiento y Agrupación por Sensibilidad: Aunque los contenedores proporcionan
     aislamiento lógico, no es tan robusto como el de las máquinas virtuales. Una buena práctica
     es agrupar los contenedores en nodos según su nivel de sensibilidad o propósito (ej. no
     mezclar contenedores de bases de datos financieras con servidores web públicos en el
     mismo host). Esto limita el “radio de explosión” (blast radius) si un atacante logra escapar
     del contenedor.
  3. Endurecimiento del Kernel: Mantener el kernel actualizado es crítico para mitigar
     vulnerabilidades de escape. Se deben aplicar configuraciones de endurecimiento
     (hardening) como limitar el acceso a llamadas al sistema peligrosas.



Bloque IV - Punto 3                          109 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.5.1.2. Seguridad en la Cadena de Suministro de Imágenes

La seguridad debe aplicarse antes de que el contenedor llegue a ejecutarse, siguiendo el principio
de Shift Left (integrar la seguridad en fases tempranas del desarrollo).
  1. Uso de Imágenes Mínimas y de Confianza: Utilizar imágenes base mínimas (como distroless
     o Alpine) reduce drásticamente la superficie de ataque y la cantidad de vulnerabilidades
     potenciales (CVEs). Se debe evitar el uso de imágenes de fuentes no verificadas o registros
     públicos sin un escaneo previo.
  2. Etiquetas Inmutables (No usar :latest): En producción, se debe evitar la etiqueta
     latest porque es mutable y ambigua. Se deben usar etiquetas específicas de versión o,
     preferiblemente, el digest (hash SHA256) de la imagen para garantizar que se despliega
     exactamente el código auditado.
  3. Firma de Imágenes: Implementar la firma digital de imágenes (p. ej., con Docker Content
     Trust o Notary) y configurar el entorno para que solo permita ejecutar imágenes firmadas
     por una autoridad de confianza.

2.5.1.3. Seguridad en Tiempo de Ejecución (Runtime)

Una vez que el contenedor está en ejecución, se deben restringir sus privilegios para minimizar el
daño en caso de compromiso.
Tabla de controles de seguridad en tiempo de ejecución

                                 Descripción y Práctica
Control                          Recomendada                        Referencia

Usuario no root                  Configurar el contenedor para      „
                                 que ejecute procesos con un
                                 UID numérico alto (no
                                 root/UID 0). Usar la directiva
                                 USER en Dockerfile o
                                 runAsNonRoot: true en
                                 Kubernetes.
Sistema de archivos de solo      Montar el sistema de archivos „
lectura                          raíz del contenedor como
                                 read-only
                                 (readOnlyRootFilesystem:
                                 true). Esto previene que un
                                 atacante instale herramientas,
                                 modifique configuraciones o
                                 persista malware.
Eliminación de Capabilities      El runtime de Docker otorga        „
                                 por defecto capacidades de
                                 Linux innecesarias. Se
                                 recomienda eliminar todas
                                 (DROP ALL) y añadir solo las
                                 estrictamente necesarias (lista
                                 blanca).


Bloque IV - Punto 3                         110 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios



                                  Descripción y Práctica
Control                           Recomendada                       Referencia

Prohibir escalada de              Configurar                        ,
privilegios                       allowPrivilegeEscalation:
                                  false para evitar que un
                                  proceso hijo gane más
                                  permisos que su padre (impide
                                  el uso de binarios setuid).
Perfiles de Seguridad             Aplicar perfiles de AppArmor o    „
(MAC/Seccomp)                     SELinux (Mandatory Access
                                  Control) y filtros Seccomp para
                                  restringir las llamadas al
                                  sistema (syscalls) permitidas.


2.5.1.4. Gestión de Secretos

Nunca se deben incrustar secretos (contraseñas, API keys, certificados) en las imágenes de
contenedor ni en variables de entorno en texto plano, ya que son fácilmente accesibles.
    • Utilizar mecanismos nativos de gestión de secretos (Kubernetes Secrets, Docker Swarm
      Secrets) que inyectan los datos en memoria (tmpfs) o como volúmenes montados, y cifran
      los datos en reposo.
    • Para entornos avanzados, integrar gestores de secretos externos (como HashiCorp Vault).

2.5.1.5. Probables Focos de Examen

En el examen de TAI, las preguntas sobre seguridad suelen centrarse en la configuración del
contenedor y la distinción entre medidas de infraestructura y de aplicación.
    • El peligro de root: Es la pregunta de seguridad más frecuente. Por defecto, el usuario root
      dentro del contenedor es el mismo root del host (a menos que se usen User Namespaces). Por
      tanto, la práctica número uno es evitar ejecutar contenedores como root.
    • Contenedores Privilegiados (--privileged): Activar este modo es extremadamente
      peligroso y equivale a dar acceso casi total al host, deshabilitando aislamientos de seguridad.
      El examen suele plantear escenarios donde esto es un error grave de configuración.
    • Principio de Inmutabilidad: Los contenedores no se parchean en vivo. Si se detecta una
      vulnerabilidad, se reconstruye la imagen y se reemplaza el contenedor. No se entra por SSH
      para hacer apt-get update.
    • Gestión de Capabilities: Se puede preguntar cómo permitir que un contenedor use un puerto
      bajo (ej. 80) sin ser root. La respuesta técnica es asignar la capability NET_BIND_SERVICE en
      lugar de ejecutar como root.
    • Superficie de ataque: El uso de imágenes base grandes (como ubuntu completa) aumenta la
      superficie de ataque frente a imágenes mínimas (como alpine o distroless).

2.5.2. Escaneo de vulnerabilidades

El escaneo de vulnerabilidades en el contexto de contenedores es un proceso automatizado
crítico diseñado para identificar debilidades de seguridad conocidas dentro de las imágenes de
contenedor y sus dependencias. Dada la naturaleza estática e inmutable de las imágenes,

Bloque IV - Punto 3                          111 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


los componentes dentro de ellas pueden quedar obsoletos rápidamente, acumulando
vulnerabilidades críticas (CVEs) tras su creación.

2.5.2.1. Alcance y objetos de análisis

A diferencia del escaneo tradicional de servidores, las herramientas de escaneo de contenedores
deben comprender la estructura de capas del sistema de archivos y el enfoque inmutable de la
infraestructura. El análisis debe cubrir múltiples vectores de riesgo:
  1. Vulnerabilidades de Software (CVEs): Identificación de paquetes del sistema operativo base
     y dependencias de la aplicación (librerías, frameworks) que tienen vulnerabilidades públicas
     conocidas y registradas en bases de datos como NVD (National Vulnerability Database).
  2. Defectos de Configuración: Detección de malas prácticas en la definición de la imagen,
     como la ejecución de servicios como usuario root, la exposición innecesaria de puertos o la
     inclusión de herramientas de administración remota (SSH).
  3. Secretos Embebidos: Búsqueda de credenciales en texto plano, tokens de API, claves SSH
     o certificados que hayan sido copiados inadvertidamente dentro de las capas de la imagen
     durante la construcción.
  4. Malware: Detección de archivos maliciosos que pudieran haber sido introducidos,
     intencionalmente o no, a través de imágenes base de terceros o repositorios no confiables.

2.5.2.2. Integración en el ciclo de vida (Shift Left)

Para que el escaneo sea efectivo, debe implementarse en todas las fases del ciclo de vida del
contenedor, siguiendo la estrategia de “Shift Left” (mover la seguridad hacia la izquierda, es decir,
etapas tempranas del desarrollo).
Tabla de etapas de escaneo y acciones recomendadas


Etapa                             Objetivo                          Acción de Seguridad

Construcción (Build/CI)           Detectar fallos antes de que la   Escaneo integrado en el
                                  imagen se publique.               pipeline de CI/CD. Bloquear la
                                                                    construcción (“break the
                                                                    build”) si se detectan
                                                                    vulnerabilidades que superen
                                                                    un umbral de gravedad (ej.
                                                                    CVSS > 7).
Registro (Registry)               Identificar vulnerabilidades      Monitoreo continuo de las
                                  en imágenes almacenadas           imágenes en reposo. Una
                                  (Stale Images).                   imagen segura hoy puede ser
                                                                    vulnerable mañana al
                                                                    descubrirse nuevos CVEs. Se
                                                                    recomienda purgar imágenes
                                                                    antiguas o inseguras.




Bloque IV - Punto 3                          112 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios



Etapa                           Objetivo                           Acción de Seguridad

Despliegue (Admission)          Evitar que imágenes inseguras      Uso de Controladores de
                                lleguen al clúster.                Admisión (Admission
                                                                   Controllers) para rechazar
                                                                   despliegues de imágenes que
                                                                   no hayan sido escaneadas o no
                                                                   cumplan las políticas de
                                                                   seguridad.
Ejecución (Runtime)             Detectar desviaciones y            Monitoreo continuo de los
                                nuevas amenazas.                   contenedores activos y
                                                                   re-escaneo periódico, ya que el
                                                                   estado de vulnerabilidad
                                                                   puede cambiar tras el
                                                                   despliegue.


2.5.2.3. Herramientas y estándares

El mercado ofrece diversas herramientas que se integran con los registros y orquestadores para
automatizar esta tarea. Es fundamental distinguir entre herramientas de escaneo de imágenes y
herramientas de auditoría de configuración del clúster.
    • Escáneres de Imágenes y Vulnerabilidades:
        – Trivy (Aqua Security): Herramienta popular que escanea vulnerabilidades en paquetes
          de OS, dependencias de aplicaciones, secretos y configuraciones.
        – Clair: Analizador estático de vulnerabilidades para contenedores de aplicaciones.
        – Anchore / Grype: Herramientas para análisis profundo de imágenes y generación de
          SBOM (Software Bill of Materials).
    • Auditoría de Cumplimiento y Configuración:
        – kube-bench: Ejecuta comprobaciones para verificar si el clúster de Kubernetes cumple
          con las CIS Benchmarks (Center for Internet Security).
        – OpenSCAP / Compliance Operator: Evalúan el cumplimiento de perfiles de seguridad
          estandarizados (como PCI-DSS o NIST) y pueden ofrecer rutas de remediación.

2.5.2.4. Probables Focos de Examen

En las preguntas de examen para TAI, es vital comprender la diferencia entre escanear una
imagen estática y monitorear un contenedor en ejecución, así como la gestión de las imágenes
almacenadas.
    • El problema de las imágenes “Stale” (Rancias): Una pregunta frecuente aborda por qué
      es necesario escanear imágenes que llevan meses almacenadas en el registro sin cambios.
      La respuesta es que las vulnerabilidades se descubren con el tiempo; una imagen que era
      segura al momento de crearse puede volverse insegura simplemente por el paso del tiempo
      y la publicación de nuevos CVEs.
    • Falsos Negativos en escáneres tradicionales: Los escáneres de vulnerabilidades
      tradicionales diseñados para servidores físicos a menudo fallan con contenedores
      porque asumen que el host es duradero y tiene agentes instalados. En contenedores, se
      requieren herramientas que entiendan el formato de capas y la inmutabilidad.


Bloque IV - Punto 3                        113 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


    • Política de “Break the Build”: Se suele preguntar cuál es la mejor práctica cuando un escáner
      detecta una vulnerabilidad crítica en el pipeline de CI/CD. La respuesta correcta es detener
      el proceso de construcción inmediatamente e impedir que la imagen se suba al registro o se
      despliegue.
    • CIS Benchmarks: Es probable que se pregunte qué estándar se utiliza habitualmente para
      endurecer (“harden”) la configuración de Kubernetes y Docker. La referencia principal son
      los CIS Benchmarks.
    • Diferencia Trivy vs. Kube-bench:
         – Si la pregunta se refiere a buscar “CVEs en librerías” o “secretos en la imagen”, la
           herramienta es tipo Trivy/Clair.
         – Si la pregunta se refiere a verificar si “el API Server tiene configurado el flag --secure-
           port”, la herramienta es kube-bench.


2.5.3. Políticas de red

Las Políticas de Red (Network Policies) son el mecanismo nativo de Kubernetes para controlar el
flujo de tráfico en las capas 3 (IP) y 4 (TCP/UDP) del modelo OSI entre los Pods, así como entre los
Pods y el exterior del clúster.
Por diseño, Kubernetes sigue un modelo de “red plana” altamente permisivo: por defecto, todos
los Pods pueden comunicarse con todos los Pods dentro del clúster, independientemente del
espacio de nombres (namespace) en el que residan. Para restringir este comportamiento y aplicar
el principio de mínimo privilegio, se utilizan los objetos NetworkPolicy.

2.5.3.1. Arquitectura y requisitos de implementación

La API de NetworkPolicy es solo una especificación declarativa. Kubernetes por sí mismo no hace
cumplir estas reglas; la ejecución depende del plugin de red (CNI) que se esté utilizando en el
clúster.
    • Dependencia del CNI: Para que las políticas tengan efecto, el clúster debe usar un proveedor
      de red compatible, como Calico, Cilium, Weave Net o Kube-router. Plugins simples como
      Flannel (en su configuración básica) no soportan políticas de red, por lo que crearlas no
      tendría ningún efecto.
    • Modelo Aditivo (Allow-list): Las políticas de red funcionan como una lista blanca. Si un
      Pod no es seleccionado por ninguna política, está “no aislado” y acepta todo el tráfico. En
      el momento en que una política selecciona un Pod, este queda “aislado” y rechaza todo el
      tráfico que no esté explícitamente permitido por las reglas de la política.

2.5.3.2. Estructura del objeto NetworkPolicy

Una política de red se define mediante cuatro campos principales en su especificación (spec):
  1. podSelector: Determina a qué Pods se aplica la política (el “destino” de la regla). Si se deja
     vacío ({}), selecciona todos los Pods del namespace.
  2. policyTypes: Lista que indica si la política aplica a tráfico de entrada (Ingress), de salida
     (Egress) o ambos. Si se omite, se asume Ingress por defecto.
  3. ingress: Define las reglas para el tráfico entrante permitido hacia los Pods seleccionados
     (lista de orígenes permitidos: from).
  4. egress: Define las reglas para el tráfico saliente permitido desde los Pods seleccionados (lista
     de destinos permitidos: to).


Bloque IV - Punto 3                           114 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2.5.3.3. Selectores de tráfico: from y to

Para definir quién puede comunicarse con quién, se utilizan tres tipos de selectores que pueden
combinarse:
    • podSelector: Permite el tráfico desde/hacia Pods específicos dentro del mismo namespace,
      basándose en etiquetas (labels).
    • namespaceSelector: Permite el tráfico desde/hacia todos los Pods que residen en namespaces
      específicos (seleccionados por etiquetas del namespace).
    • ipBlock: Permite el tráfico desde/hacia rangos de direcciones IP (CIDR), útil para controlar el
      tráfico externo al clúster (p. ej., bloquear salida a internet excepto a una IP corporativa).
Ejemplo de estructura de aislamiento:
kind: NetworkPolicy
spec:
  podSelector:
    matchLabels:
      role: db       # Aplica a los pods de base de datos
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend # Solo permite tráfico desde el frontend
    ports:
    - port: 5432       # Solo al puerto de la DB


2.5.3.4. Estrategia de “Denegación por defecto” (Default Deny)

La práctica de seguridad más recomendada (“Best Practice”) es implementar una política de
“Denegación por defecto” (Default Deny) en cada namespace. Esto cambia el comportamiento
del namespace de “permitir todo” a “denegar todo”, obligando a los administradores a autorizar
explícitamente cualquier flujo de comunicación necesario.
Una política Default Deny típica selecciona todos los pods pero no define ninguna regla de entrada
permitida:
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}       # Selecciona TODOS los pods del namespace
  policyTypes:
  - Ingress             # Aplica a tráfico entrante


2.5.3.5. Probables Focos de Examen

En el examen de TAI, las preguntas sobre políticas de red suelen centrarse en su comportamiento
por defecto y limitaciones.
    • Comportamiento sin políticas: Es fundamental recordar que, en ausencia de NetworkPolicies,
      no hay aislamiento: cualquier pod puede hablar con cualquier otro, incluso entre distintos
      namespaces.




Bloque IV - Punto 3                          115 de 164                              January 31, 2026
                           Correo electrónico. Contenedores y microservicios


    • Efecto del podSelector: {}: Si una pregunta muestra una política con podSelector: {} y
      una lista de reglas ingress: [] (vacía) o no definida, la respuesta correcta es que bloquea
      todo el tráfico entrante para todos los pods del namespace.
    • Limitación del CNI: Una pregunta “trampa” habitual plantea un escenario donde se aplica
      una política correcta pero el tráfico no se bloquea. La causa suele ser que el clúster usa un
      plugin CNI que no soporta NetworkPolicies (como versiones básicas de Flannel).
    • Aislamiento de Namespaces: Los namespaces por sí solos no aíslan el tráfico de red. Para
      aislar un namespace de otro, es obligatorio crear una NetworkPolicy que restrinja el tráfico de
      entrada.
    • Sintaxis de combinación (AND vs OR):
         – Si se usan múltiples elementos en la lista from (con guiones -), actúa como un OR lógico
           (se permite tráfico de A O de B).
         – Si se usan múltiples selectores dentro de un mismo elemento (sin guiones separados),
           actúa como un AND lógico (el origen debe cumplir la condición A Y la condición B, por
           ejemplo, un pod específico en un namespace específico).

2.5.4. Control de acceso

El control de acceso en entornos de orquestación, específicamente en Kubernetes, es el mecanismo
crítico que protege la API del clúster, garantizando que solo los usuarios y procesos autorizados
puedan visualizar o modificar el estado del sistema. Cada solicitud que llega al servidor API
(kube-apiserver) debe atravesar secuencialmente tres etapas de seguridad: Autenticación,
Autorización y Control de Admisión.

2.5.4.1. Autenticación (Authentication - AuthN)

La autenticación es el proceso de verificar la identidad del sujeto que realiza la solicitud (“¿Quién
eres?”). Kubernetes distingue dos tipos de usuarios:
  1. Cuentas de Servicio (Service Accounts): Son recursos gestionados por la propia API de
     Kubernetes (Kind: ServiceAccount). Están diseñadas para procesos y aplicaciones que
     se ejecutan dentro de los Pods. Se asignan a un namespace específico y se autentican
     automáticamente mediante tokens montados en el contenedor.
  2. Usuarios Normales (Users): Son humanos o sistemas externos. Kubernetes no tiene un
     objeto nativo para representar cuentas de usuario (no existe Kind: User). La gestión de
     estos usuarios se delega a servicios externos (certificados X.509, OpenID Connect, LDAP,
     proveedores cloud).

2.5.4.2. Autorización (Authorization - AuthZ) y RBAC

Una vez autenticado el usuario, la autorización determina si tiene permiso para realizar la acción
solicitada sobre el recurso indicado (“¿Qué puedes hacer?”). El modelo estándar y más utilizado es
el Control de Acceso Basado en Roles (RBAC).
El modelo RBAC en Kubernetes se construye mediante cuatro objetos fundamentales que
relacionan Sujetos (Usuarios, Grupos, ServiceAccounts) con Reglas (Verbos sobre Recursos).
Tabla de objetos RBAC




Bloque IV - Punto 3                           116 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Objeto                            Alcance (Scope)                   Descripción Técnica

Role                              Namespaced                        Conjunto de reglas que definen
                                                                    permisos dentro de un espacio
                                                                    de nombres. Solo puede
                                                                    otorgar acceso a recursos en
                                                                    ese mismo namespace (ej. leer
                                                                    Pods en dev).
ClusterRole                       Cluster-wide                      Conjunto de reglas aplicables a
                                                                    todo el clúster. Se usa para: 1.
                                                                    Recursos que no tienen
                                                                    namespace (ej. Nodes,
                                                                    PersistentVolumes). 2.
                                                                    Permisos sobre recursos con
                                                                    namespace pero aplicados en
                                                                    todos los namespaces. 3.
                                                                    Definir roles comunes para ser
                                                                    reutilizados.
RoleBinding                       Namespaced                        Vincula un Role (o un
                                                                    ClusterRole) a un Sujeto
                                                                    dentro de un namespace
                                                                    específico. Otorga los
                                                                    permisos definidos en el rol
                                                                    únicamente en ese namespace.
ClusterRoleBinding                Cluster-wide                      Vincula un ClusterRole a un
                                                                    Sujeto a nivel de clúster.
                                                                    Otorga los permisos definidos
                                                                    en el rol en todos los
                                                                    namespaces del clúster y sobre
                                                                    recursos globales.


Estructura de una Regla RBAC: Las reglas se definen mediante la combinación de tres elementos:
    • APIGroups: El grupo de la API al que pertenece el recurso (ej. "" para core, apps para
      Deployments).
    • Resources: El objeto sobre el que se actúa (ej. pods, secrets, services).
    • Verbs: La acción específica permitida. Los verbos estándar incluyen get, list, watch (lectura),
      create, update, patch, delete y deletecollection (escritura).


2.5.4.3. Principio de Menor Privilegio y Cuentas Predeterminadas

La seguridad efectiva depende de aplicar el principio de menor privilegio, evitando el uso de
comodines (*) en las reglas.
    • Service Accounts por defecto: Cada namespace tiene una cuenta default que se monta
      automáticamente en los Pods si no se especifica otra. Históricamente, esto podía implicar
      riesgos si se le asignaban permisos excesivos, por lo que se recomienda desactivar el montaje



Bloque IV - Punto 3                          117 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


      automático del token (automountServiceAccountToken: false) si la aplicación no necesita
      hablar con la API.
    • ClusterRoles predeterminados: Kubernetes incluye roles integrados como view (solo
      lectura), edit (lectura/escritura sin cambios de roles), admin (control total del namespace) y
      cluster-admin (superusuario).


2.5.4.4. Probables Focos de Examen

En el examen de TAI, las preguntas sobre control de acceso suelen centrarse en la distinción de
alcances y la mecánica de RBAC.
    • Diferencia entre Role y ClusterRole:
        – Si la pregunta se refiere a dar permisos sobre Nodos (Nodes), la respuesta correcta debe
          implicar un ClusterRole, ya que los nodos no pertenecen a un namespace.
        – Si se pide dar permisos “en todos los namespaces”, se requiere un ClusterRoleBinding
          (o un RoleBinding en cada namespace, que es menos eficiente).
    • Vinculación Cruzada (ClusterRole en RoleBinding):
        – Es posible (y muy común) usar un ClusterRole dentro de un RoleBinding. Esto permite
          reutilizar una definición de permisos común (ej. view) pero otorgarla solo dentro de un
          namespace específico. Esta es una pregunta técnica frecuente.
    • Verbos list vs. watch:
        – get recupera un objeto específico por nombre.
        – list recupera una colección de objetos.
        – watch permite recibir actualizaciones en tiempo real (streaming) de los cambios. Los
          controladores y operadores dependen críticamente del verbo watch.
    • Grupo system:masters:
        – Los usuarios pertenecientes al grupo especial system:masters tienen acceso de
          superusuario completo al clúster y omiten la comprobación de reglas RBAC. Es una
          “puerta trasera” administrativa que no se puede restringir mediante reglas normales.
    • Gestión de Usuarios: Recuerde que no se pueden crear usuarios (User) con kubectl create
      user porque no son recursos de Kubernetes. Se gestionan externamente (certificados o
      proveedores de identidad).




Bloque IV - Punto 3                          118 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



3. Administración de microservicios

3.1. Arquitectura de microservicios
Esta sección marca la transición final del temario, donde la infraestructura (servidores
y contenedores) se pone al servicio de la lógica de negocio. Entender la arquitectura de
microservicios es vital para el administrador moderno, ya que esta dicta cómo se deben
configurar, escalar y monitorizar los recursos subyacentes.




                                  Figure 6: Microservicios vs. SOA

La arquitectura de microservicios es un estilo de diseño de software que estructura una aplicación
como una colección de servicios pequeños, autónomos y débilmente acoplados. A diferencia
del enfoque tradicional o monolítico, donde toda la lógica de la aplicación (interfaz, gestión de
usuarios, facturación, inventario) reside en un único ejecutable y comparte una misma base de
datos, los microservicios dividen estas funciones en procesos independientes. Cada servicio se
enfoca en una única responsabilidad comercial, posee su propio ciclo de vida y se comunica con
los demás a través de interfaces ligeras y estandarizadas, generalmente APIs HTTP/REST o colas
de mensajes.
Este cambio de paradigma transforma radicalmente el rol de la administración de sistemas. Ya
no se gestiona un “servidor grande” para una “aplicación grande”; ahora se orquesta una red
distribuida de cientos de servicios pequeños que pueden estar escritos en diferentes lenguajes de
programación y utilizar distintas tecnologías de almacenamiento de datos. Para visualizar este
contraste fundamental, la siguiente tabla resume las diferencias operativas entre ambos modelos:

                                                                     Arquitectura de
Característica                   Arquitectura Monolítica             Microservicios

Despliegue                       “Todo o nada”: un cambio            Independiente: se puede
                                 pequeño requiere redesplegar        actualizar un servicio sin
                                 toda la aplicación.                 detener el resto del sistema.


Bloque IV - Punto 3                         119 de 164                                 January 31, 2026
                         Correo electrónico. Contenedores y microservicios



                                                                    Arquitectura de
Característica                   Arquitectura Monolítica            Microservicios

Escalabilidad                    Vertical (servidores más           Horizontal y granular: se
                                 potentes) o replicación            escala solo el servicio que
                                 completa del monolito.             tiene alta demanda.
Acoplamiento                     Alto: los componentes son          Bajo (Weakly coupled): el fallo
                                 interdependientes; un error        de un servicio no debería
                                 puede tirar todo el sistema.       colapsar la aplicación entera.
Complejidad                      Complejidad interna en el          Complejidad en la red y la
                                 código; infraestructura            orquestación; código más
                                 simple.                            simple por servicio.
Gestión de Datos                 Base de datos centralizada y       Base de datos por servicio
                                 compartida.                        (Descentralizada).


Si bien los microservicios ofrecen ventajas innegables como la agilidad en el desarrollo y la
resiliencia ante fallos, también introducen nuevos desafíos. La complejidad no desaparece, sino
que se desplaza del código a la infraestructura y la red. El administrador debe enfrentarse ahora
a problemas de latencia de red, consistencia de datos distribuida y la necesidad imperiosa de
automatización, ya que gestionar manualmente este ecosistema es inviable.

3.1.1. Conceptos y principios

La arquitectura de microservicios se define como un estilo arquitectónico que estructura una
aplicación como una colección de servicios pequeños, autónomos y acoplados de forma flexible,
donde cada unidad implementa una capacidad de negocio específica.

3.1.1.1. Definición formal y origen

El término fue formalizado por James Lewis y Martin Fowler en 2014, quienes describieron este
estilo como un enfoque para desarrollar una aplicación única como un conjunto de servicios
pequeños, cada uno ejecutándose en su propio proceso y comunicándose mediante mecanismos
ligeros, a menudo una API de recursos HTTP.
Estos servicios presentan las siguientes características base:
    • Se construyen alrededor de las capacidades de negocio.
    • Son desplegables de forma independiente mediante maquinaria de despliegue totalmente
      automatizada.
    • Existe un mínimo de gestión centralizada de estos servicios.
    • Pueden escribirse en diferentes lenguajes de programación y utilizar diferentes tecnologías
      de almacenamiento de datos.
Históricamente, los microservicios surgieron como reacción a las limitaciones de las arquitecturas
monolíticas y como una evolución de las mejores prácticas de la Arquitectura Orientada a Servicios
(SOA). A diferencia de la SOA tradicional, que a menudo dependía de protocolos complejos (SOAP)
y orquestación centralizada (ESB), los microservicios favorecen la coreografía y protocolos ligeros
(REST).



Bloque IV - Punto 3                         120 de 164                                January 31, 2026
                          Correo electrónico. Contenedores y microservicios


3.1.1.2. Las 9 características de Martin Fowler

Martin Fowler y James Lewis identificaron nueve características fundamentales que definen
este estilo arquitectónico. Estas características son esenciales para diferenciar un diseño de
microservicios puro de otros enfoques distribuidos.
1. Componentización vía servicios El software se compone de servicios independientemente
desplegables en lugar de librerías enlazadas. Esto permite que un cambio en un servicio no
requiera el redespliegue de toda la aplicación, facilitando la sustitución de componentes
(“componentization”).
2. Organización en torno a capacidades de negocio A diferencia de los equipos organizados por
capas técnicas (UI, BBDD, Lógica), los microservicios se estructuran en torno a capacidades de
negocio (Business Capabilities). Esto promueve equipos multifuncionales (“cross-functional
teams”) responsables de todo el ciclo de vida del servicio, alineándose con la Ley de Conway.
3. Productos, no proyectos El equipo de desarrollo posee el producto durante todo su ciclo de vida
(“you build it, you run it”). Se evita el modelo de entregar el software a un equipo de operaciones
separado para que lo mantenga. El objetivo es establecer una relación continua con el software
para mejorar sus capacidades de negocio.
4. “Smart endpoints and dumb pipes” Los microservicios evitan el uso de middleware complejo o
inteligente (como los Enterprise Service Bus - ESB de SOA) que contienen lógica de negocio. En
su lugar, la lógica reside en los propios servicios (“endpoints inteligentes”) y la comunicación se
realiza a través de mecanismos simples (“tuberías tontas”), típicamente HTTP/REST o mensajería
asíncrona ligera (RabbitMQ, ZeroMQ).
   Estilo SOA (ESB)                Estilo Microservicios
+---------------------+          +---------------------+
|   Lógica Compleja   |          |    Tubería Tonta     |
| (Enrutado, Transf.) |          |    (HTTP / AMQP)     |
+----------+----------+          +----------+----------+
           |                                 |
    +------+------+                   +------+------+
    | Servicio A |                    | Servicio A | (Lógica aquí)
    +-------------+                   +-------------+

5. Gobierno descentralizado Se rechaza la estandarización rígida sobre una única plataforma
tecnológica. Cada equipo puede elegir las herramientas y lenguajes más adecuados para su
problema específico (Políglota). El principio es “construirlo y ejecutarlo” (Build it, Run it), lo
que otorga autonomía pero también responsabilidad sobre las decisiones técnicas.
6. Gestión de datos descentralizada Mientras que los monolitos prefieren una única base de
datos lógica para toda la aplicación, los microservicios prefieren que cada servicio gestione su
propia base de datos (Database-per-Service). Esto asegura el desacoplamiento, aunque introduce
desafíos de consistencia eventual.
7. Automatización de la infraestructura Dado el gran número de procesos independientes, la
automatización es obligatoria. Se utilizan prácticas de Integración Continua (CI) y Entrega
Continua (CD) para reducir la carga operativa y permitir despliegues frecuentes y fiables.
8. Diseño para el fallo (Design for failure) Se asume que los servicios pueden fallar en cualquier
momento. Las aplicaciones deben diseñarse para tolerar la caída de servicios dependientes
sin detenerse por completo. Se implementan patrones como Circuit Breaker para gestionar
la resiliencia y evitar fallos en cascada.



Bloque IV - Punto 3                          121 de 164                             January 31, 2026
                        Correo electrónico. Contenedores y microservicios


9. Diseño evolutivo La descomposición en servicios permite que la aplicación evolucione
gradualmente. Se pueden reemplazar partes del sistema sin afectar al resto, facilitando la
adaptación a cambios tecnológicos o de negocio. Esto es crucial para evitar la obsolescencia
tecnológica.

3.1.1.3. Principios de Sam Newman

Sam Newman, en su obra Building Microservices, condensa y complementa estos conceptos en
siete principios clave:

Principio                                        Descripción

Modelado en torno al negocio                     El dominio de negocio debe dictar la estructura
                                                 del código y los límites de los servicios
                                                 (Bounded Contexts).
Cultura de automatización                        Automatizar todo lo posible (pruebas,
                                                 despliegue, infraestructura) para gestionar la
                                                 complejidad de múltiples servicios.
Ocultar detalles de implementación               Los servicios deben tratarse como cajas negras;
                                                 las bases de datos internas nunca deben
                                                 exponerse directamente.
Descentralizar todo                              Evitar cuellos de botella arquitectónicos y
                                                 organizativos; delegar la toma de decisiones a
                                                 los equipos.
Despliegue independiente                         Un cambio en un servicio no debe requerir la
                                                 coordinación con otros servicios para su
                                                 despliegue.
Aislar el fallo                                  Si un servicio falla, no debe provocar la caída de
                                                 todo el sistema (resiliencia y bulkheads).
Altamente observable                             Implementar monitoreo semántico, logs
                                                 agregados y trazabilidad distribuida para
                                                 entender el estado del sistema.


3.1.1.4. Probables focos de examen

Basado en la literatura técnica y patrones de preguntas frecuentes, los siguientes puntos son
críticos para el examen:
  1. Diferencia clave con SOA: El tribunal suele preguntar por la diferencia en la comunicación.
     Recuerde: SOA tiende a usar ESB (Enterprise Service Bus) con lógica de orquestación
     centralizada (“Smart pipes”), mientras que Microservicios usa protocolos ligeros
     (HTTP/REST) y lógica en los extremos (“Smart endpoints, dumb pipes”).
  2. Gestión de Datos: El patrón Database-per-Service es fundamental. Una pregunta típica es
     si los microservicios comparten base de datos. La respuesta normativa es NO; comparten
     datos vía API, no vía tablas compartidas, para garantizar el desacoplamiento.
  3. Teorema CAP y Consistencia: Al descentralizar datos, se pierde la consistencia inmediata
     (ACID) entre servicios. Los microservicios suelen optar por Consistencia Eventual (BASE).

Bloque IV - Punto 3                        122 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


  4. Concepto de “Two-pizza team”: Relacionado con la organización y la Ley de Conway. Un
     equipo debe ser lo suficientemente pequeño como para ser alimentado con dos pizzas,
     favoreciendo la agilidad y comunicación.
  5. Patrón Strangler Fig: Es el método estándar para migrar de monolito a microservicios,
     reemplazando gradualmente funcionalidades sin reescribir todo el sistema de una vez.

3.1.2. Ventajas e inconvenientes

La arquitectura de microservicios no es una “bala de plata”; su adopción implica un intercambio
de complejidades (trade-offs). Mientras que reduce la complejidad a nivel de servicio individual,
incrementa significativamente la complejidad a nivel de sistema global debido a su naturaleza
distribuida.

3.1.2.1. Ventajas principales

La literatura técnica y la experiencia de la industria identifican varios beneficios clave que motivan
la migración desde arquitecturas monolíticas.
1. Escalabilidad independiente y eficiente A diferencia de un monolito, donde escalar una
funcionalidad requiere replicar toda la aplicación, los microservicios permiten escalar únicamente
los componentes que experimentan mayor carga.
    • Optimización de recursos: Permite asignar hardware específico según la necesidad del
      servicio (ej. instancias con alta CPU para procesamiento de imágenes y alta memoria para
      bases de datos en memoria).
    • Elasticidad: Facilita el auto-escalado dinámico en entornos cloud.
2. Agilidad y despliegue independiente Es considerado uno de los mayores beneficios. Un cambio
en un servicio puede ser desplegado sin necesidad de coordinar el despliegue de todo el sistema.
    • Time-to-market: Reduce los ciclos de entrega, permitiendo actualizaciones más frecuentes
      y rápidas.
    • Ciclos de release: Los equipos pueden liberar nuevas funcionalidades a su propio ritmo sin
      verse bloqueados por otros equipos.
3. Aislamiento de fallos (Resiliencia) En un monolito, un error (como una fuga de memoria)
puede tumbar todo el proceso del servidor. En microservicios, si un servicio falla, el impacto
puede ser aislado, permitiendo que el resto de la aplicación continúe funcionando (degradación
elegante).
    • Patrones de contención: Se utilizan patrones como Circuit Breaker o Bulkheads para evitar
      fallos en cascada.
4. Heterogeneidad tecnológica (Persistencia Políglota) Permite adoptar nuevas tecnologías más
rápidamente y usar la herramienta adecuada para cada trabajo (“the right tool for the job”).
    • Sin “Vendor Lock-in”: No es obligatorio estandarizar una única plataforma o lenguaje para
      toda la empresa.
    • Optimización de datos: Cada servicio puede usar el tipo de base de datos que mejor se
      adapte a sus necesidades (ej. Neo4j para grafos, Elasticsearch para búsquedas, RDBMS para
      transaccionalidad).
5. Alineación organizacional Favorece la estructura de equipos pequeños y autónomos (como la
regla de las “dos pizzas” de Amazon), alineándose con la Ley de Conway. Los equipos se organizan
en torno a capacidades de negocio, no a capas técnicas.

Bloque IV - Punto 3                           123 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


6. Reemplazabilidad Dado que los servicios son pequeños, el coste de reescribir uno por completo
es bajo. Esto mitiga el riesgo de obsolescencia tecnológica y facilita la refactorización.

3.1.2.2. Inconvenientes y desafíos

La adopción de microservicios introduce una complejidad inherente a los sistemas distribuidos
que debe ser gestionada.
1. Complejidad de sistemas distribuidos La comunicación entre procesos pasa de ser una llamada
en memoria a una llamada remota (RPC/HTTP), introduciendo latencia y modos de fallo que no
existen en los monolitos.
    • Latencia de red: El aumento de llamadas remotas puede degradar el rendimiento si no se
      gestiona la “charla” (chattiness) entre servicios.
    • Fallos parciales: El sistema debe diseñarse para tolerar que los servicios remotos no estén
      disponibles o sean lentos.
2. Consistencia de datos y transacciones Al aplicar el patrón Database-per-Service, se pierde la
capacidad de realizar transacciones ACID que abarquen múltiples entidades de negocio.
    • Consistencia Eventual: Se debe gestionar la consistencia eventual (modelo BASE), lo cual es
      más complejo de implementar y depurar que las transacciones fuertes.
    • Gestión de estado: Requiere implementar patrones complejos como Sagas o Event Sourcing
      para mantener la coherencia entre servicios.
3. Complejidad operativa (DevOps) Gestionar decenas o cientos de servicios requiere un alto
grado de automatización. El despliegue manual es inviable.
    • Infraestructura: Requiere inversión en orquestadores (Kubernetes), registros de servicios y
      balanceadores de carga.
    • Monitorización: La trazabilidad se vuelve difícil; es necesario implementar Distributed
      Tracing (ej. Jaeger, Zipkin) y agregación de logs para seguir una petición a través de múltiples
      servicios.
4. Sobrecarga de pruebas (Testing) Las pruebas end-to-end son mucho más difíciles de configurar
y lentas de ejecutar debido a la necesidad de levantar múltiples servicios y sus dependencias.
    • Contratos de interfaz: Un cambio en la API de un servicio puede romper a otros
      consumidores si no se gestiona estrictamente el versionado o se usan Consumer-Driven
      Contracts.
5. Coste inicial y curva de aprendizaje El “Microservice Premium” indica que esta arquitectura
añade un coste base en complejidad y recursos que solo se amortiza cuando el sistema alcanza
una cierta escala. Para equipos pequeños o dominios simples, el monolito suele ser más eficiente.

3.1.2.3. Tabla resumen comparativa

                                                                     Arquitectura de
Característica                    Arquitectura Monolítica            Microservicios

Despliegue                        Un solo artefacto; “todo o         Independiente por servicio.
                                  nada”. Lento y arriesgado.         Rápido y frecuente.




Bloque IV - Punto 3                           124 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios



                                                                    Arquitectura de
Característica                   Arquitectura Monolítica            Microservicios

Escalado                         Se escala toda la aplicación       Escalado granular de
                                 (ineficiente).                     componentes específicos.
Base de Datos                    Centralizada y compartida          Descentralizada
                                 (ACID fácil).                      (Database-per-service).
                                                                    Consistencia eventual.
Resiliencia                       Un error puede tumbar todo el     Aislamiento de fallos. El
                                  sistema (Punto único de fallo).   sistema se degrada
                                                                    parcialmente.
Complejidad                      Baja al inicio, alta al crecer     Alta desde el inicio (Sistemas
                                 (Acoplamiento).                    distribuidos).
Tecnología                        Stack único (Lock-in). Difícil    Políglota. Fácil adopción de
                                  de actualizar.                    nuevas tecnologías.


3.1.2.4. Probables focos de examen

  1. Concepto de “Microservice Premium”: Es muy probable que se pregunte sobre la idoneidad
     de usar microservicios en proyectos pequeños. La respuesta correcta suele orientarse a que
     NO se recomiendan para startups o equipos pequeños debido a la complejidad operativa
     inicial (“Premium”) que supera los beneficios.
  2. Complejidad de las Pruebas: Se suele preguntar qué tipo de pruebas se vuelven más
     complejas en microservicios. La respuesta es las pruebas de integración y end-to-end (E2E),
     debido a la naturaleza distribuida.
  3. Transacciones Distribuidas: Preguntas sobre cómo manejar transacciones que afectan a
     varios servicios. La respuesta clave es evitar transacciones distribuidas clásicas (2PC) y optar
     por Consistencia Eventual y patrones como Saga.
  4. Falsas ventajas: Un error común (“distractor” en test) es afirmar que los microservicios son
     “más fáciles de desarrollar” o “más simples”. Aunque el código de un servicio es simple, la
     complejidad del sistema global aumenta. No eliminan la complejidad, la mueven a la red y
     a la operación.
  5. Relación con la Latencia: Pregunta típica sobre rendimiento. Los microservicios
     suelen introducir mayor latencia de red en comparación con un monolito debido a la
     serialización/deserialización y saltos de red.

3.1.3. Diferencias con arquitectura monolítica

La distinción fundamental entre una arquitectura monolítica y una de microservicios radica
en el acoplamiento y la granularidad de despliegue. Mientras que el monolito agrupa todas las
funcionalidades en una única unidad lógica y ejecutable, los microservicios descomponen el
sistema en servicios autónomos distribuidos que se comunican a través de la red.

3.1.3.1. Comparativa estructural y de despliegue

1. Unidad de despliegue y Ciclo de vida



Bloque IV - Punto 3                          125 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


    • Monolito: La aplicación se empaqueta como un único artefacto (por ejemplo, un archivo
      WAR en Java). Cualquier cambio, por pequeño que sea (como corregir una línea de código),
      requiere recompilar, probar y redesplegar toda la aplicación. Esto fomenta despliegues poco
      frecuentes y de alto riesgo (“Big Bang deployment”).
    • Microservicios: Cada servicio es una unidad desplegable independientemente. Un equipo
      puede actualizar un servicio sin detener ni afectar al resto del sistema. Esto habilita la
      Entrega Continua (CD) y despliegues frecuentes con menor riesgo.
2. Escalabilidad y uso de recursos
    • Monolito: El escalado es unidimensional (normalmente vertical o clonación horizontal).
      Si un módulo específico consume muchos recursos (ej. procesamiento de imágenes), se
      debe replicar toda la aplicación en múltiples servidores, desperdiciando memoria y CPU en
      módulos que no lo necesitan.
    • Microservicios: Permite un escalado granular y eficiente. Se pueden asignar más recursos o
      instancias únicamente al servicio que sufre la carga, optimizando costes e infraestructura
      (ej. usar instancias de GPU solo para el servicio de imágenes).
3. Resiliencia y Aislamiento de fallos
    • Monolito: Presenta un Punto Único de Fallo (SPOF) a nivel de proceso. Un error grave, como
      una fuga de memoria en un módulo secundario, puede consumir todos los recursos del
      servidor y tumbar la aplicación completa.
    • Microservicios: Los fallos pueden aislarse (patrón Bulkhead). Si un servicio falla, el resto del
      sistema puede seguir funcionando, degradando la funcionalidad parcialmente en lugar de
      detenerse por completo.
      MONOLITO                          MICROSERVICIOS
+---------------------+             +-------+    +-------+
| [UI] [Negocio]      |             | Svc A |    | Svc B |
| [Datos] [Log]       |             +-------+    +-------+
+---------------------+                 |            |
          |                             v            v
    +-----------+                    +-----+      +-----+
    | DB Única |                     | DB A|      | DB B|
    +-----------+                    +-----+      +-----+


3.1.3.2. Gestión de datos y Tecnológica

1. Gestión de Datos (El cambio más crítico)
    • Monolito: Utiliza una base de datos centralizada y compartida. Esto facilita la gestión
      de transacciones ACID (atomicidad, consistencia, aislamiento, durabilidad) y la integridad
      referencial mediante claves foráneas, pero genera un alto acoplamiento entre módulos a
      nivel de datos.
    • Microservicios: Aplica el principio de Database-per-Service (Base de datos por servicio).
      Cada servicio gestiona su propio almacenamiento y ningún otro servicio puede acceder
      a él directamente, solo a través de API. Esto garantiza el desacoplamiento, pero introduce
      la complejidad de la consistencia eventual y la imposibilidad de usar transacciones ACID
      distribuidas fácilmente.
2. Heterogeneidad Tecnológica (Políglota)
    • Monolito: Obliga a un stack tecnológico único (“Vendor Lock-in”). Si la aplicación está
      en Java, todos los módulos deben escribirse en Java, dificultando la adopción de nuevas


Bloque IV - Punto 3                           126 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


      tecnologías o el uso de la herramienta más adecuada para un problema específico.
    • Microservicios: Permite la programación políglota. Cada equipo puede elegir el lenguaje,
      framework o base de datos que mejor se adapte a su servicio (ej. Node.js para I/O, Python
      para IA, Java para core bancario).

3.1.3.3. Tabla comparativa resumen

La siguiente tabla sintetiza las diferencias clave para efectos de memorización rápida:

                                                                   Arquitectura de
Característica                   Arquitectura Monolítica           Microservicios

Despliegue                       Unitario, lento, arriesgado       Independiente por servicio,
                                 (todo o nada).                    rápido y frecuente.
Base de Datos                    Centralizada, compartida,         Descentralizada (DB privada),
                                 transacciones ACID simples.       consistencia eventual.
Escalabilidad                    Ineficiente (se escala todo el    Granular y eficiente (se escala
                                 bloque).                          solo lo necesario).
Complejidad                      Baja al inicio, alta al crecer    Alta desde el inicio
                                 (código espagueti).               (complejidad operativa y de
                                                                   red).
Comunicación                     Llamadas en memoria               Llamadas de red (latencia,
                                 (rápidas y fiables).              fallos parciales).
Tecnología                       Stack único y rígido.             Stack políglota y flexible.
Equipos                          Silos funcionales (UI, Backend, Equipos multifuncionales
                                 DBA).                           (“Two-pizza teams”).


3.1.3.4. Probables focos de examen

Basado en la literatura técnica y patrones de preguntas frecuentes en oposiciones, estos son los
puntos críticos:
  1. Complejidad Operativa vs. Complejidad de Código: El examen puede plantear que
     los microservicios eliminan la complejidad. Falso. Los microservicios no eliminan la
     complejidad, la desplazan del código interno a la infraestructura y la red (complejidad
     operativa).
  2. Consistencia de Datos: Es muy probable una pregunta sobre transacciones. En monolitos
     son ACID; en microservicios, debido a la base de datos distribuida, se suele trabajar con
     Consistencia Eventual (BASE) y patrones como Sagas, ya que las transacciones distribuidas
     (2PC) se desaconsejan.
  3. Patrón de Base de Datos Compartida: Se puede preguntar si compartir base de datos es
     una buena práctica en microservicios. La respuesta normativa es NO, ya que rompe el
     desacoplamiento y la independencia de despliegue (se considera un anti-patrón excepto en
     migraciones transitorias).
  4. Rendimiento y Latencia: A diferencia del monolito donde la comunicación es en
     memoria (nanosegundos), los microservicios introducen latencia de red y la necesidad de
     serialización/deserialización, lo que puede degradar el rendimiento si no se gestiona bien.

Bloque IV - Punto 3                          127 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  5. Cuándo NO usar microservicios: El concepto de “Microservice Premium” indica que para
     aplicaciones simples o startups pequeñas, la sobrecarga operativa de los microservicios no
     compensa, y un monolito bien modularizado es preferible.

3.2. Diseño de microservicios
Esta sección se adentra en la ingeniería de la solución. Una vez decidido que se utilizará una
arquitectura de microservicios, el reto no es la programación del código, sino definir cómo se
dividen las responsabilidades y cómo fluye la información entre las partes. Un mal diseño en
esta etapa puede dar lugar a lo que se conoce peyorativamente como un “monolito distribuido”:
un sistema que tiene toda la complejidad de red de los microservicios y toda la rigidez de un
monolito.
El diseño de microservicios se basa en dos principios rectores: alta cohesión (cada servicio hace
una sola cosa y la hace bien) y bajo acoplamiento (los servicios saben lo menos posible unos de
otros). El administrador de sistemas debe entender que la aplicación ya no es un ejecutable único,
sino una red de servicios independientes que colaboran. Por tanto, el diseño debe resolver tres
problemas fundamentales: cómo definir los límites de cada servicio (descomposición), cómo
exponerlos al mundo exterior de forma segura y cómo gestionar el tráfico interno entre ellos.
Para estructurar estas soluciones, se utilizan patrones de diseño arquitectónico que estandarizan
la comunicación. Mientras que en un monolito las funciones se llaman entre sí en memoria,
aquí se comunican a través de la red, lo que introduce latencia y posibles fallos que deben ser
gestionados por la infraestructura.
A continuación, se presenta una tabla que resume los componentes críticos de diseño que
gestionan este tráfico:

Componente                       Tipo de Tráfico                    Función Principal

API Gateway                      Norte-Sur (Cliente Sistema)        Punto de entrada único.
                                                                    Gestiona autenticación,
                                                                    enrutamiento y rate-limiting
                                                                    para los clientes externos.
Service Mesh                     Este-Oeste (Servicio Servicio)     Capa de infraestructura
                                                                    dedicada a gestionar la
                                                                    comunicación interna,
                                                                    reintentos, cifrado (mTLS) y
                                                                    observabilidad.
Message Broker                   Asíncrono (Eventos)                Desacopla servicios
                                                                    permitiendo que se
                                                                    comuniquen sin estar activos
                                                                    simultáneamente (ej.
                                                                    RabbitMQ, Kafka).


Para visualizar cómo se integran estas piezas, el siguiente diagrama muestra la diferencia entre el
acceso externo (gestionado por el Gateway) y la comunicación interna:
El diseño correcto implica que el API Gateway oculte la complejidad interna al cliente (el usuario
no necesita saber que existen 10 microservicios detrás), mientras que el Service Mesh (o las

Bloque IV - Punto 3                         128 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios




                                  Figure 7: Diseño de microservicios


librerías de cliente) asegura que si el “Servicio C” falla, el “Servicio B” sepa cómo reintentar la
conexión o fallar elegantemente sin colgar todo el sistema.

3.2.1. Descomposición de aplicaciones

La descomposición es el proceso crítico de dividir una aplicación monolítica (o diseñar una nueva)
en un conjunto de servicios pequeños, autónomos y acoplados flexiblemente. Este proceso es uno
de los desafíos más complejos en la arquitectura de microservicios, ya que una división incorrecta
puede resultar en un “monolito distribuido”, heredando las desventajas de ambos modelos sin
sus beneficios.

3.2.1.1. Estrategias de descomposición y diseño de límites

Para identificar los límites correctos de los servicios, la literatura y la práctica industrial
recomiendan evitar la descomposición basada en capas técnicas (presentación, lógica, datos) y
optar por enfoques centrados en el negocio.
1. Diseño Guiado por el Dominio (Domain-Driven Design - DDD) Es el enfoque metodológico
predominante para definir los límites de los microservicios.
    • Bounded Context (Contexto Acotado): Define el límite dentro del cual un modelo de dominio
      específico se aplica y tiene un significado claro. Los microservicios deben alinearse con estos
      contextos acotados.
    • Agregados (Aggregates): En DDD, un agregado es un conjunto de objetos de dominio que
      pueden tratarse como una sola unidad. Los agregados son a menudo buenos candidatos
      para ser la unidad base de un microservicio.
    • Lenguaje Ubicuo: Utilizar un vocabulario común entre expertos del dominio y
      desarrolladores para definir claramente los términos dentro de cada contexto, evitando
      ambigüedades (ej. el término “Cliente” puede significar cosas distintas en “Ventas” y en
      “Envíos”).
2. Descomposición por capacidades de negocio Los servicios se definen en función de lo que hace
el negocio para generar valor (ej. Gestión de Pedidos, Gestión de Inventario, Facturación). Esta
estructura fomenta equipos multifuncionales responsables de todo el ciclo de vida del servicio.

Bloque IV - Punto 3                          129 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3. Enfoque basado en flujo de datos (Dataflow-Driven) Propone utilizar Diagramas de Flujo
de Datos (DFD) purificados para identificar operaciones y datos. Se agrupan operaciones
que producen el mismo tipo de datos de salida para formar candidatos a microservicios,
proporcionando un método más objetivo y semi-automatizable que el juicio puramente experto.

3.2.1.2. Patrones de migración (De Monolito a Microservicios)

La migración debe ser incremental para reducir riesgos, evitando la reescritura total (“Big Bang”)
que suele conducir al fracaso.
1. Patrón Strangler Fig (Higo Estrangulador) Es el patrón estándar para migrar sistemas
heredados.   Consiste en crear nuevas funcionalidades como microservicios y extraer
gradualmente piezas del monolito.
    • Mecanismo: Se utiliza un proxy o enrutador para interceptar las llamadas. El tráfico se
      redirige gradualmente a los nuevos servicios a medida que se reemplazan las funciones del
      monolito.
    • Resultado: Con el tiempo, el nuevo sistema “estrangula” al monolito hasta que este puede
      ser eliminado o queda reducido a un tamaño manejable.
2. Branch by Abstraction (Rama por Abstracción) Útil cuando la funcionalidad a extraer está
profundamente integrada en el código del monolito.
    • Proceso: Se crea una capa de abstracción (interfaz) sobre el código existente. Luego, se crea
      una nueva implementación que llama al microservicio remoto. Finalmente, se cambia el
      “interruptor” para usar la nueva implementación.
3. Parallel Run (Ejecución en Paralelo) El monolito y el nuevo microservicio se ejecutan
simultáneamente procesando las mismas peticiones. Se comparan los resultados para asegurar la
paridad y la corrección antes de desconectar el sistema antiguo.

3.2.1.3. Granularidad y tamaño del servicio

No existe una métrica universal (como líneas de código) para determinar el tamaño “correcto” de
un microservicio. Sin embargo, existen heurísticas clave:
    • Principio de Responsabilidad Única: El servicio debe hacer una sola cosa y hacerla bien.
    • Regla de las “Dos Pizzas”: Un equipo lo suficientemente pequeño como para ser alimentado
      con dos pizzas debe ser capaz de poseer y operar el servicio completo. Esto asegura que la
      complejidad cognitiva sea manejable por el equipo.
    • Independencia de despliegue: Si para desplegar un cambio en el servicio A se requiere
      desplegar simultáneamente el servicio B, entonces no están correctamente descompuestos;
      probablemente deberían estar juntos o refactorizarse para reducir el acoplamiento.

3.2.1.4. Probables focos de examen

Los siguientes conceptos son recurrentes en la literatura técnica y susceptibles de preguntas tipo
test o desarrollo:
  1. Definición de Bounded Context: Es fundamental asociar este concepto de DDD con la
     delimitación de fronteras de los microservicios. Pregunta típica: “¿Qué concepto de DDD se
     utiliza principalmente para definir los límites de un microservicio?” Respuesta: Bounded
     Context (Contexto Acotado).


Bloque IV - Punto 3                         130 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  2. Patrón Strangler Fig: Identificarlo como la estrategia recomendada para migraciones
     incrementales. Se suele contraponer al patrón “Big Bang” (reescritura total), el cual se
     desaconseja por su alto riesgo.
  3. Criterio de Descomposición: Recordar que la descomposición debe basarse en capacidades
     de negocio o subdominios, y NO en capas técnicas (UI, BBDD, Lógica).
  4. Monolito Distribuido: Entender este anti-patrón. Ocurre cuando se separan los servicios
     físicamente pero permanecen fuertemente acoplados (ej. comparten base de datos o
     requieren despliegues coordinados), obteniendo la complejidad de los sistemas distribuidos
     sin sus beneficios.
  5. Database per Service: En la descomposición, cada microservicio debe gestionar su propia
     base de datos. Compartir esquemas de base de datos entre servicios viola la independencia y
     el desacoplamiento.

3.2.2. Comunicación entre microservicios

En una arquitectura monolítica, los componentes se invocan entre sí mediante llamadas a
funciones o métodos a nivel de lenguaje dentro del mismo espacio de memoria. En contraste,
una aplicación basada en microservicios es un sistema distribuido que se ejecuta en múltiples
procesos o máquinas. Por consiguiente, los servicios deben interactuar utilizando mecanismos
de Comunicación entre Procesos (IPC - Inter-Process Communication) a través de la red.
El diseño de la comunicación es crítico, ya que la latencia de red, la serialización de datos y la
complejidad de los sistemas distribuidos impactan directamente en el rendimiento y la fiabilidad
de la aplicación global.

3.2.2.1. Estilos de interacción

Antes de seleccionar un protocolo específico, es fundamental clasificar los modos de interacción
entre servicios. La literatura técnica, especialmente las guías de arquitectura de NGINX y
Microsoft, categoriza estas interacciones en dos dimensiones: cardinalidad y sincronía.
1. Dimensiones de la interacción
    • Uno a uno vs. Uno a muchos: Dependiendo de si la solicitud es procesada por una sola
      instancia de servicio o por múltiples instancias.
    • Síncrono vs. Asíncrono: Define si el cliente bloquea su ejecución esperando una respuesta o
      continúa su operación.
2. Matriz de estilos de comunicación La combinación de estas dimensiones genera los patrones
de comunicación estándar:

Estilo                            Síncrono                          Asíncrono

Uno a Uno                         Solicitud/Respuesta               Notificación (One-way
                                  (Request/Response)                request) Solicitud/Respuesta
                                                                    Asíncrona
Uno a Muchos                      —                                 Publicar/Suscribir
                                                                    (Publish/Subscribe)
                                                                    Publicar/Respuestas
                                                                    asíncronas



Bloque IV - Punto 3                          131 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.2.2.2. Comunicación Síncrona (Request/Response)

En este patrón, el cliente realiza una solicitud y espera una respuesta oportuna. Si el servicio es
bloqueante (thread-based), el hilo del cliente se detiene hasta recibir la respuesta.
1. HTTP/REST (Representational State Transfer) Es el mecanismo más utilizado debido a su
ubicuidad y facilidad de uso. Utiliza el protocolo HTTP (generalmente HTTP/1.1) y verbos estándar
(GET, POST, PUT, DELETE) para manipular recursos.
    • Formato de datos: Típicamente JSON (texto), aunque puede usar XML.
    • Ventajas: Fácil de implementar, amigable con firewalls, no requiere intermediarios (brokers).
    • Desventajas: Introduce acoplamiento temporal (ambos servicios deben estar activos), mayor
      latencia por el “handshake” TCP en cada petición (en HTTP/1.1), y verbosidad del texto
      (JSON).
2. gRPC (Remote Procedure Call) Es un marco de alto rendimiento desarrollado por Google.
Utiliza HTTP/2 como transporte y Protocol Buffers (Protobuf ) como lenguaje de definición de
interfaz (IDL) y formato de serialización binaria.
    • Ventajas: Es más eficiente que REST (menor tamaño de payload y multiplexación), soporta
      streaming bidireccional y tipado fuerte.
    • Uso recomendado: Comunicación interna entre microservicios (East-West traffic) donde la
      latencia es crítica.

3.2.2.3. Comunicación Asíncrona (Mensajería)

En este modelo, el cliente envía un mensaje sin esperar una respuesta inmediata. El mensaje se
delega generalmente a un intermediario o broker.
1. Colas de Mensajes y Publicación/Suscripción Se utilizan Message Brokers (como RabbitMQ,
Apache Kafka o ActiveMQ) para desacoplar el emisor del receptor.
    • Colas (Point-to-Point): Un mensaje es procesado por un solo consumidor. Útil para distribuir
      carga de trabajo.
    • Pub/Sub (Publish/Subscribe): Un mensaje (evento) es entregado a todos los suscriptores
      interesados. Es la base de las arquitecturas dirigidas por eventos (EDA).
2. Ventajas del modelo asíncrono
    • Desacoplamiento temporal: El consumidor no necesita estar en línea cuando se envía el
      mensaje.
    • Aislamiento de fallos: Si el consumidor falla, los mensajes se encolan y se procesan al
      recuperarse.
    • Nivelación de carga (Load Leveling): Actúa como un amortiguador (buffer) ante picos de
      tráfico.
3. Desafíos
    • Complejidad operativa: Requiere mantener infraestructura adicional (el Broker).
    • Consistencia Eventual: No se garantiza la consistencia inmediata de los datos, lo que
      complica la lógica de negocio.




Bloque IV - Punto 3                         132 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.2.2.4. Formatos de Serialización

La elección del formato de los datos intercambiados afecta el rendimiento y la evolución del
servicio:
    • Texto (JSON/XML): Legibles por humanos y autodescriptivos. Son el estándar en APIs
      públicas y REST. Su desventaja es el tamaño y el costo de procesamiento (parseo).
    • Binario (Avro, Protocol Buffers, Thrift): Más compactos y rápidos de procesar. Requieren
      un esquema o IDL (Interface Definition Language) para deserializar los datos. Son preferibles
      para tráfico interno de alto volumen.

3.2.2.5. Gestión de fallos y resiliencia en la comunicación

Dado que la red no es fiable, los microservicios deben diseñarse para tolerar fallos parciales.
1. Patrón Circuit Breaker (Disyuntor) Evita que una aplicación intente realizar una operación
que es probable que falle. Si un servicio detecta fallos repetidos (ej. timeouts) al llamar a otro,
“abre el circuito” y devuelve un error inmediato o una respuesta por defecto sin realizar la llamada
de red, evitando el agotamiento de recursos y fallos en cascada.
2. Retries (Reintentos) con Backoff Exponencial Para fallos transitorios (ej. una caída
momentánea de red), se puede reintentar la operación. Sin embargo, reintentar agresivamente
puede tumbar el servicio destino (“thundering herd”), por lo que se debe usar un tiempo de espera
creciente entre intentos.

3.2.2.6. Probables focos de examen

Basado en la literatura técnica y los patrones de preguntas en oposiciones de informática, los
siguientes puntos son críticos:
  1. Diferencia crítica entre Síncrono y Asíncrono: Es fundamental entender que la
     comunicación síncrona (REST/gRPC) introduce acoplamiento temporal (ambos servicios
     deben estar activos), mientras que la asíncrona (Broker) lo elimina.
  2. Protocolos y Capas:
         • REST usa típicamente HTTP/1.1 y JSON.
         • gRPC usa obligatoriamente HTTP/2 y Protocol Buffers (binario). Pregunta típica:
           “¿Qué ventaja ofrece gRPC sobre REST?” Respuesta: Menor latencia, multiplexación y
           serialización binaria eficiente.
  3. Idempotencia: En sistemas de mensajería, un mensaje puede entregarse más de una vez
     (at-least-once delivery). Los servicios deben diseñarse para ser idempotentes, es decir, que
     procesar el mismo mensaje múltiples veces tenga el mismo efecto que procesarlo una sola
     vez.
  4. Service Discovery: Dado que las instancias de microservicios tienen direcciones IP
     dinámicas (especialmente en contenedores), se requiere un mecanismo de Service
     Discovery para que los clientes localicen las instancias de servicio disponibles.
  5. Patrón Circuit Breaker: Identificar su función principal: prevenir fallos en cascada y evitar
     el agotamiento de recursos esperando a un servicio que no responde.

3.2.3. API Gateway

El patrón API Gateway (Pasarela de API) es un componente fundamental en la arquitectura de
microservicios que actúa como un punto de entrada único para todos los clientes (aplicaciones


Bloque IV - Punto 3                          133 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


móviles, web, IoT). Funciona como un intermediario que acepta solicitudes de clientes externos y
las enruta a los microservicios apropiados dentro del sistema.
Este patrón es análogo al patrón de diseño de software Fachada (Facade), ya que encapsula la
arquitectura interna del sistema y proporciona una API adaptada a cada cliente, desacoplando así
a los consumidores de la complejidad del backend.

3.2.3.1. Funciones y Responsabilidades (Gateway Offloading)

El API Gateway no se limita a ser un simple proxy inverso; su valor radica en la capacidad de
consolidar funciones transversales (cross-cutting concerns) que, de otro modo, tendrían que
implementarse redundantemente en cada microservicio. Este patrón se conoce como Gateway
Offloading.
Las responsabilidades principales incluyen:
  1. Enrutamiento (Routing): Actúa como un proxy inverso de capa 7, dirigiendo las peticiones
     entrantes al servicio o instancia correcta. Permite a los clientes acceder a través de un único
     dominio sin conocer la topología interna.
  2. Seguridad y Autenticación: Centraliza la validación de tokens (ej. JWT, OAuth 2.0) y claves
     de API. Actúa como primera línea de defensa, reduciendo la superficie de ataque al no exponer
     directamente los microservicios a la red pública.
  3. Terminación SSL/TLS: Gestiona el descifrado de HTTPS en el borde, aliviando a los
     microservicios de la carga computacional del cifrado y simplificando la gestión de
     certificados.
  4. Gestión de Tráfico (Rate Limiting y Throttling): Controla el número de solicitudes
     permitidas por cliente o servicio para evitar abusos o ataques de denegación de servicio
     (DoS), protegiendo la estabilidad del backend.
  5. Traducción de Protocolos: Permite exponer APIs REST/HTTP amigables para la web hacia el
     exterior, mientras se comunica internamente con los microservicios mediante protocolos
     más eficientes pero menos compatibles con navegadores, como gRPC, AMQP o Thrift.
   Cliente Externo        API Gateway              Microservicios
   +-------------+     +----------------+       +-------------------+
   | Móvil/Web | ----> | Autenticación | ----> | Servicio A (REST) |
   +-------------+     | Rate Limiting |        +-------------------+
                       | Enrutamiento |
                       | Traducción     | ----> +-------------------+
                       +----------------+       | Servicio B (gRPC) |
                                                +-------------------+


3.2.3.2. Agregación y Composición de API

Uno de los problemas críticos que resuelve el API Gateway es la “charlatanería” (Chattiness).
En arquitecturas distribuidas, una sola operación de usuario (como cargar la página de detalles
de un producto) puede requerir datos de múltiples servicios (inventario, precios, reseñas,
recomendaciones).
Si el cliente llamara directamente a cada servicio, sufriría de alta latencia y consumo de ancho
de banda debido a múltiples viajes de red (Round Trips). El API Gateway implementa el patrón
Gateway Aggregation: recibe una única solicitud del cliente, invoca múltiples microservicios en
paralelo y combina los resultados en una única respuesta JSON optimizada.




Bloque IV - Punto 3                         134 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Comunicación Directa (Sin Gateway)                 Comunicación con API Gateway

El cliente conoce múltiples endpoints.             El cliente conoce un solo endpoint.
Múltiples llamadas a través de red pública         Una llamada pública, múltiples internas
(Lento).                                           (Rápido).
Lógica de orquestación en el cliente (Complejo).   Lógica de orquestación en el servidor.
Alto acoplamiento entre cliente y backend.         Bajo acoplamiento.


3.2.3.3. Patrón Backend for Frontend (BFF)

Una evolución del API Gateway es el patrón Backend for Frontend (BFF). En lugar de tener un
único gateway monolítico para todos los clientes, se crean gateways específicos adaptados a las
necesidades de cada tipo de cliente.
    • Problema: Un cliente de escritorio puede necesitar una gran cantidad de detalles y tolerar
      imágenes grandes, mientras que un cliente móvil necesita una carga útil (payload) mínima
      para ahorrar batería y datos.
    • Solución BFF: Se despliega un gateway específico para móviles y otro para web. Cada uno
      expone una API optimizada para su interfaz de usuario correspondiente, evitando el enfoque
      de “talla única”.

3.2.3.4. Desventajas y Riesgos

Aunque esencial, el API Gateway introduce riesgos arquitectónicos que deben gestionarse:
  1. Punto Único de Fallo (SPOF): Si el Gateway cae, toda la aplicación se vuelve inaccesible para
     el exterior. Es obligatorio desplegarlo en alta disponibilidad (múltiples réplicas).
  2. Cuello de Botella (Bottleneck): Al centralizar todo el tráfico, si no escala adecuadamente,
     puede degradar el rendimiento global del sistema.
  3. Riesgo de Lógica de Negocio: Existe la tentación de incluir lógica de negocio en el Gateway.
     Esto es un anti-patrón; el Gateway debe limitarse a enrutamiento y preocupaciones
     transversales. La lógica debe permanecer en los microservicios.

3.2.3.5. Probables focos de examen

Basado en la documentación técnica y patrones de diseño, los siguientes puntos son críticos para
la preparación:
  1. Diferencia Norte-Sur vs. Este-Oeste: El API Gateway gestiona principalmente el tráfico
     Norte-Sur (cliente externo hacia la red interna), mientras que el Service Mesh gestiona el
     tráfico Este-Oeste (entre microservicios).
  2. Funciones de Seguridad: Se suele preguntar qué funciones de seguridad descarga el Gateway.
     Las respuestas clave son: Terminación SSL/TLS, Autenticación (OAuth2/JWT) y Rate
     Limiting/Throttling.
  3. Solución a la “Chattiness”: Identificar que la Agregación de API es la técnica utilizada para
     reducir el número de llamadas y la latencia en redes WAN/Móviles.
  4. Definición de BFF: Entender que el patrón Backend for Frontend implica crear gateways
     separados para diferentes interfaces de usuario (Móvil vs. Web) para optimizar la experiencia
     de usuario.

Bloque IV - Punto 3                          135 de 164                            January 31, 2026
                        Correo electrónico. Contenedores y microservicios


  5. Patrón Offloading: Reconocer el concepto de “Gateway Offloading” como la centralización
     de tareas transversales (logging, certificados, caché) para simplificar el código de los
     microservicios individuales.

3.2.4. Service Mesh

El Service Mesh (o Malla de Servicios) se define como una capa de infraestructura dedicada para
gestionar la comunicación servicio a servicio dentro de una arquitectura de microservicios. Su
objetivo principal es abstraer la complejidad de la red de la lógica de negocio de la aplicación,
proporcionando funcionalidades críticas como seguridad, observabilidad y gestión de tráfico de
forma transparente y uniforme sin requerir cambios en el código de los servicios individuales.

3.2.4.1. Arquitectura: Plano de Datos y Plano de Control

La arquitectura de un Service Mesh se divide conceptualmente en dos componentes
fundamentales que operan en conjunto:
  1. Plano de Datos (Data Plane):
        • Constituido por un conjunto de proxies ligeros desplegados junto a cada instancia de
          microservicio.
        • Intercepta y gestiona todo el tráfico de red entrante y saliente (inbound/outbound) de
          los servicios.
        • Es responsable de ejecutar tareas como el balanceo de carga, la comprobación de salud
          (health checking), la autenticación y la recopilación de telemetría.
  2. Plano de Control (Control Plane):
        • Es la capa de gestión centralizada que configura y coordina el comportamiento del plano
          de datos.
        • Proporciona una API para que los operadores definan políticas de seguridad, reglas de
          enrutamiento y gestión de certificados.
        • No toca los paquetes de datos directamente; su función es enviar la configuración
          necesaria a los proxies del plano de datos.

3.2.4.2. El Patrón Sidecar

La implementación estándar del Service Mesh (específicamente la arquitectura SM-AR3 descrita
por el NIST) se basa en el Patrón Sidecar.
En este modelo, el proxy del Service Mesh se despliega en un contenedor o proceso separado
pero dentro del mismo pod (en Kubernetes) o host que el microservicio. Esto permite que el
proxy comparta el mismo ciclo de vida y recursos de red que la aplicación, actuando como un
intermediario transparente.
      POD / HOST
+-------------------------+
| +-------------------+ |
| |    Microservicio   | |    <--- Lógica de Negocio
| +--------+----------+ |
|           | (localhost) |
| +--------v----------+ |
| |    Proxy Sidecar   | |    <--- Lógica de Red (Service Mesh)
| | (Envoy/Linkerd) | |
| +--------+----------+ |
+-----------|-------------+


Bloque IV - Punto 3                        136 de 164                             January 31, 2026
                        Correo electrónico. Contenedores y microservicios


            |
      Red (Tráfico mTLS)
            |
+-----------|-------------+
| +--------v----------+ |
| |    Proxy Sidecar   | |
| +--------+----------+ |
|           |             |
| +--------v----------+ |
| |    Microservicio   | |
| +-------------------+ |
+-------------------------+

Este desacoplamiento permite a los desarrolladores centrarse únicamente en la lógica de negocio,
delegando las preocupaciones de red (reintentos, cifrado, descubrimiento) al sidecar.

3.2.4.3. Capacidades y Funcionalidades Principales

El Service Mesh aborda los desafíos inherentes a los sistemas distribuidos proporcionando cuatro
pilares funcionales:
  1. Gestión de Tráfico y Resiliencia:
       • Balanceo de carga inteligente: Realiza balanceo en capa 7 (L7), permitiendo decisiones
         basadas en latencia o tasas de error, más allá del simple Round Robin de capa 4.
       • Patrones de estabilidad: Implementa automáticamente Circuit Breakers, reintentos
         (retries) y tiempos de espera (timeouts) para evitar fallos en cascada.
       • Despliegues avanzados: Facilita estrategias como Canary Deployments o Blue-Green
         mediante el enrutamiento ponderado de tráfico (traffic splitting).
  2. Seguridad (Zero Trust):
       • mTLS (Mutual TLS): Cifra automáticamente el tráfico entre microservicios y gestiona la
         identidad de los servicios mediante certificados, asegurando que tanto el cliente como
         el servidor se autentiquen mutuamente.
       • Gestión de certificados: El plano de control automatiza la rotación y gestión de claves y
         certificados.
  3. Observabilidad:
       • Proporciona visibilidad uniforme sin instrumentar el código de la aplicación.
       • Genera métricas (latencia, tráfico, errores), logs de acceso y trazas distribuidas
         (Distributed Tracing) de todas las interacciones entre servicios.
  4. Descubrimiento de Servicios:
       • Mantiene un registro actualizado de las instancias de servicios disponibles, gestionando
         la naturaleza efímera de los contenedores.

3.2.4.4. Diferencia con API Gateway

Aunque ambos componentes gestionan tráfico, su ámbito de actuación es distinto y suelen ser
complementarios en una arquitectura robusta:




Bloque IV - Punto 3                         137 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Característica                   API Gateway                        Service Mesh

Tipo de Tráfico                  Norte-Sur: Entrada desde           Este-Oeste: Comunicación
                                 clientes externos (móviles,        interna entre microservicios
                                 web) hacia el clúster.             dentro del clúster.
Rol Principal                     Exponer APIs, monetización,       Fiabilidad de la red interna,
                                  seguridad perimetral,             mTLS entre servicios,
                                  agregación de respuestas.         observabilidad profunda.
Ubicación                         Borde (Edge) de la red.           Ubicuo (presente en cada
                                                                    microservicio mediante
                                                                    sidecar).
Gestión                           Centralizada.                     Descentralizada (Plano de
                                                                    datos distribuido).


3.2.4.5. Implementaciones y Herramientas

Las soluciones de Service Mesh más destacadas en la industria incluyen:
    • Istio: Una de las implementaciones más populares y completas. Utiliza Envoy como
      proxy de sidecar y ofrece un potente plano de control para gestionar tráfico, seguridad y
      observabilidad.
    • Linkerd: Se centra en la simplicidad y el rendimiento (ultraligero). Fue uno de los pioneros
      en el concepto de Service Mesh.
    • Consul Connect: Extensión de HashiCorp Consul que añade capacidades de Service Mesh.
    • AWS App Mesh: Servicio gestionado de AWS basado en Envoy.

3.2.4.6. Probables focos de examen

Basado en la documentación técnica y tendencias de exámenes, los siguientes puntos son críticos:
  1. Patrón Sidecar: Es muy probable que se pregunte cuál es el patrón de despliegue
     característico de un Service Mesh. La respuesta es el patrón Sidecar, donde un proxy se
     ejecuta junto al contenedor de la aplicación.
  2. Diferencia Norte-Sur vs. Este-Oeste: Pregunta clásica para distinguir entre API Gateway y
     Service Mesh. El Service Mesh se especializa en tráfico Este-Oeste (inter-servicio), mientras
     que el API Gateway maneja el Norte-Sur (cliente-servidor).
  3. Desacoplamiento: Entender que el Service Mesh desacopla la lógica de red/infraestructura
     de la lógica de negocio, permitiendo a los desarrolladores escribir servicios en cualquier
     lenguaje sin preocuparse por implementar librerías de comunicación complejas.
  4. Seguridad mTLS: Se suele preguntar cómo el Service Mesh mejora la seguridad interna.
     La clave es la implementación automática de mTLS (Mutual TLS), que cifra y autentica la
     comunicación entre servicios sin cambios en el código.
  5. Planos de Arquitectura: Distinguir entre el Plano de Datos (proxies que tocan los paquetes)
     y el Plano de Control (políticas y configuración).

3.3. Despliegue de microservicios
Esta sección aborda la fase crítica donde el código se transforma en un servicio vivo y accesible
para los usuarios. En una arquitectura monolítica, el despliegue solía ser un evento de alto riesgo,

Bloque IV - Punto 3                          138 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


programado infrecuentemente (mensual o trimestralmente) y que a menudo implicaba paradas
de servicio (“ventanas de mantenimiento”). En el mundo de los microservicios, esta filosofía es
insostenible: el objetivo es realizar despliegues frecuentes, granulares y sin tiempo de inactividad.
El despliegue de microservicios no consiste simplemente en copiar archivos a un servidor; se
trata de gestionar un flujo continuo de cambios. Dado que una aplicación puede estar compuesta
por decenas de servicios, y cada uno puede ser actualizado por un equipo diferente en cualquier
momento, la coordinación manual es imposible. El administrador de sistemas debe implementar y
mantener tuberías de automatización (CI/CD) que validen, empaqueten y distribuyan el software
de forma autónoma.
Sin embargo, la velocidad no debe comprometer la estabilidad. Por ello, el despliegue moderno
se apoya en estrategias avanzadas que permiten probar nuevas versiones en producción con un
riesgo controlado, coexistiendo temporalmente con las versiones antiguas. Esto exige una gestión
estricta del versionado semántico, asegurando que una actualización en el “Servicio de Pagos” no
rompa la compatibilidad con el “Servicio de Pedidos”.
A continuación, se describen las estrategias de despliegue más comunes que permiten esta
actualización sin interrupciones, comparando sus riesgos y requisitos de recursos:

                                                                              Coste de
Estrategia               Descripción                 Ventaja Principal        Infraestructura

Recreate                 Apagar la versión A y       Simpleza técnica.        Bajo (pero implica
                         encender la B.              Estado limpio.           caída del servicio).
Rolling Update           Reemplazo progresivo        Sin caída de servicio    Medio (requiere
                         (ej. 1 a 1) de instancias   (Zero Downtime).         capacidad extra
                         viejas por nuevas.                                   temporal).
Blue-Green               Despliegue de la            Cambio instantáneo y     Alto (requiere
                         versión nueva (Green)       rollback inmediato si    duplicar recursos).
                         en paralelo a la vieja      falla.
                         (Blue).
Canary                   Enviar solo un %            Minimiza el impacto      Medio/Alto
                         pequeño de tráfico a la     de errores en usuarios   (complejidad en
                         nueva versión para          reales.                  balanceadores).
                         probar.


Para visualizar cómo se orquesta este proceso, es fundamental entender el concepto de Pipeline
CI/CD, que actúa como la cadena de montaje de la fábrica de software. El siguiente diagrama
ilustra el flujo desde que un desarrollador guarda un cambio hasta que llega a producción mediante
una estrategia Canary:
El éxito del despliegue en microservicios radica en la reversibilidad: la capacidad del sistema para
detectar automáticamente si la nueva versión (v2.0) está generando errores y volver a la versión
estable anterior (v1.0) sin intervención humana, protegiendo así la experiencia del usuario final.

3.3.1. Estrategias de despliegue

El despliegue de microservicios exige una transición desde la gestión manual de servidores hacia
una infraestructura automatizada e inmutable. Dada la naturaleza distribuida y la frecuencia de

Bloque IV - Punto 3                           139 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios




                                     Figure 8: Estrategia Canary


cambios, las estrategias de despliegue deben garantizar la continuidad del negocio, minimizar el
tiempo de inactividad (downtime) y permitir recuperaciones rápidas (rollbacks) ante errores.
A continuación, se detallan las estrategias estándar en la industria, soportadas por plataformas
de orquestación como Kubernetes y servicios en la nube como AWS.

3.3.1.1. Rolling Update (Actualización Rodante)

Es la estrategia por defecto en plataformas como Kubernetes. Consiste en reemplazar las
instancias de la versión antigua por la nueva de forma incremental y escalonada, asegurando que
siempre haya un número mínimo de instancias disponibles para atender el tráfico.
    • Funcionamiento:
        1. Se lanza un pequeño lote de instancias con la nueva versión (v2).
        2. Una vez que estas instancias pasan las pruebas de salud (readiness probes), se detiene un
           número equivalente de instancias de la versión antigua (v1).
        3. El proceso se repite hasta que todas las instancias son v2.
    • Ventajas:
         – Sin tiempo de inactividad: El servicio mantiene la capacidad de respuesta durante todo
           el proceso.
         – Coste eficiente: No requiere duplicar la infraestructura, solo necesita un pequeño
           excedente de recursos para las nuevas instancias durante la transición (surge).
    • Inconvenientes:
         – Coexistencia de versiones: Durante el despliegue, las versiones v1 y v2 se ejecutan
           simultáneamente y atienden tráfico. La aplicación debe soportar compatibilidad hacia
           atrás (ej. cambios en esquemas de base de datos).
         – Rollback lento: Si se detecta un error, deshacer el cambio requiere repetir el proceso
           inverso, lo que lleva tiempo.

3.3.1.2. Blue-Green Deployment (Despliegue Azul-Verde)

Esta estrategia implica mantener dos entornos de producción idénticos y aislados: uno activo
(“Blue”, con la versión actual) y otro inactivo (“Green”, donde se despliega la nueva versión).
    • Funcionamiento:
       1. El tráfico de producción se dirige al entorno Blue (v1).
       2. Se despliega y testea la nueva versión (v2) en el entorno Green.
       3. Una vez validado, se cambia el enrutador o balanceador de carga para redirigir todo el
          tráfico del entorno Blue al Green instantáneamente.
       4. El entorno Blue queda inactivo, disponible para un rollback inmediato si fuera necesario.
       [Router/DNS]                 [Router/DNS]
            |                            |


Bloque IV - Punto 3                          140 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


    +------+------+                +------+------+
    |             |                |             |
 [Blue]        [Green]          [Blue]        [Green]
 (Activo)      (Idle)           (Idle)        (Activo)
   v1            v2               v1            v2

    • Ventajas:
        – Rollback instantáneo: Si la nueva versión falla, basta con revertir el enrutador al
          entorno anterior.
        – Aislamiento y Pruebas: Permite probar la nueva versión en un entorno idéntico a
          producción antes de recibir tráfico real.
        – Cero tiempo de inactividad: El corte de tráfico es atómico.
    • Inconvenientes:
        – Alto coste: Requiere duplicar la infraestructura (doble de recursos de cómputo)
          mientras ambos entornos coexisten.
        – Gestión de estado: Es complejo si hay bases de datos compartidas o transacciones largas
          pendientes durante el cambio.

3.3.1.3. Canary Release (Lanzamiento Canario)

El despliegue Canario reduce el riesgo al introducir la nueva versión a un pequeño subconjunto
de usuarios antes de un despliegue completo. El nombre proviene de la práctica minera de usar
canarios para detectar gases tóxicos.
    • Funcionamiento:
        1. Se despliega la nueva versión (v2) junto a la antigua (v1).
        2. Se configura el enrutador para enviar un porcentaje pequeño del tráfico (ej. 5% o 10%)
           a la v2, mientras el resto sigue en v1.
        3. Se monitorizan métricas críticas (latencia, errores). Si son estables, se incrementa
           gradualmente el tráfico hacia v2 hasta llegar al 100%.
        4. Si se detectan fallos, se revierte el tráfico inmediatamente, afectando solo a una fracción
           de usuarios.
    • Ventajas:
         – Mínimo impacto de fallos: Solo un pequeño porcentaje de usuarios experimenta errores
           si la versión es defectuosa.
         – Testing en producción: Permite validar el comportamiento con tráfico real (funcional
           y no funcional).
    • Inconvenientes:
         – Lentitud: El despliegue completo tarda más tiempo debido a las fases incrementales de
           validación.
         – Complejidad de enrutamiento: Requiere un balanceador de carga inteligente o un
           Service Mesh (como Istio) para dividir el tráfico de forma granular.

3.3.1.4. Otras estrategias: Recreate y A/B Testing

Estrategia Recreate (Recreación) Es la estrategia más simple pero disruptiva. Consiste en detener
todas las instancias de la versión antigua y luego arrancar las nuevas.
    • Pros: Garantiza que no haya mezcla de versiones; el estado es limpio.
    • Contras: Genera tiempo de inactividad (downtime) durante el proceso de reinicio. Solo es
      aceptable en entornos de desarrollo o sistemas no críticos.



Bloque IV - Punto 3                           141 de 164                              January 31, 2026
                             Correo electrónico. Contenedores y microservicios


A/B Testing A menudo confundida con Canary, su objetivo es diferente. Mientras Canary busca
estabilidad técnica, el A/B Testing busca evaluar la efectividad del negocio o la experiencia de
usuario (UX). Se dirige el tráfico a diferentes versiones basándose en atributos del usuario (cookies,
geolocalización, tipo de dispositivo) para comparar métricas de conversión o comportamiento.

3.3.1.5. Tabla comparativa resumen

La siguiente tabla sintetiza las características clave para el examen:

                      Tiempo de             Coste de             Velocidad de      Riesgo de
Estrategia            Inactividad           Infraestructura      Rollback          Despliegue

Recreate              Alto (Downtime)       Bajo (1x)            Lento             Alto
Rolling Update        Cero                  Bajo (1x + surge)    Lento/Medio       Medio
Blue-Green            Cero                  Alto (2x)            Inmediato         Bajo
Canary                Cero                  Bajo/Medio           Rápido            Muy Bajo


3.3.1.6. Probables focos de examen

  1. Diferencia Blue-Green vs. Canary: Es la pregunta más frecuente.
        • Blue-Green: El cambio de tráfico es “todo o nada” (switch instantáneo). Prioriza el
          rollback rápido. Requiere doble infraestructura.
        • Canary: El cambio es gradual/incremental (ej. 10% -> 50% -> 100%). Prioriza la
          minimización del impacto del error (“Blast radius”).
  2. Coste de Infraestructura: Se suele preguntar qué estrategia es más costosa en términos
     de recursos. La respuesta es Blue-Green, debido a la necesidad de mantener dos entornos
     completos simultáneamente.
  3. Rolling Update y Kubernetes: Identificar que es la estrategia nativa/por defecto en
     Kubernetes (objeto Deployment). Su principal característica es que actualiza los pods
     uno a uno (o en lotes) sin detener el servicio, pero implica que coexisten dos versiones
     temporalmente.
  4. Concepto de “Feature Toggles”: A veces se presentan como alternativa a las ramas de código.
     Permiten desplegar código en producción pero mantener la funcionalidad desactivada hasta
     que se decida “encenderla” (desacoplando despliegue de lanzamiento).
  5. Gestión de Base de Datos en Blue-Green: Un punto avanzado es cómo manejar la base de
     datos. La recomendación general es desacoplar los cambios de esquema de los cambios
     de código, haciendo que la base de datos sea compatible con ambas versiones (backward
     compatibility) antes de realizar el despliegue Blue-Green.

3.3.2. CI/CD para microservicios

La implementación de Integración Continua (CI) y Entrega/Despliegue Continuo (CD) es un
requisito fundamental para el éxito de una arquitectura de microservicios. Sin un proceso de CI/CD
robusto y automatizado, no es posible alcanzar la agilidad que esta arquitectura promete, ya que la
gestión manual de docenas o cientos de servicios independientes resulta inviable operativamente.




Bloque IV - Punto 3                             142 de 164                            January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.3.2.1. Principios de CI/CD en sistemas distribuidos

A diferencia de las aplicaciones monolíticas, donde existe un único pipeline de construcción, los
microservicios requieren un enfoque descentralizado.
  1. Pipeline independiente por servicio: Cada microservicio debe tener su propio repositorio
     de código y su propio pipeline de CI/CD. Esto garantiza la independencia de despliegue,
     permitiendo que un equipo libere una actualización de un servicio (ej. Servicio A) sin tener
     que coordinarse con los equipos de otros servicios ni esperar a una “ventana de lanzamiento”
     global.
  2. Automatización obligatoria: Debido a la complejidad operativa, todo el ciclo de vida debe
     estar automatizado. Esto incluye la compilación, las pruebas, la creación de imágenes de
     contenedores y el despliegue en los orquestadores (como Kubernetes).
  3. Inmutabilidad de los artefactos: El resultado del proceso de CI debe ser un artefacto
     inmutable (típicamente una imagen de contenedor Docker). Esta imagen se construye
     una sola vez y se promociona a través de los diferentes entornos (desarrollo, pre-producción,
     producción), inyectando la configuración específica de cada entorno en tiempo de ejecución,
     pero sin modificar el binario.

3.3.2.2. Etapas del Pipeline de Integración Continua (CI)

El objetivo de la fase de CI es asegurar que el código nuevo se integra correctamente y cumple con
los estándares de calidad antes de generar un artefacto desplegable.


Etapa                            Descripción Técnica                Herramientas Comunes

Commit / Checkout                El desarrollador sube cambios      Git, GitHub, GitLab
                                 al repositorio. El servidor de
                                 CI detecta el cambio y
                                 descarga el código.
Build & Unit Test                Se compila el código y se          Maven, Gradle, npm
                                 ejecutan pruebas unitarias. Se
                                 busca retroalimentación
                                 rápida (“Fail fast”).
Análisis Estático                Revisión automática de             SonarQube, Snyk
                                 calidad de código (linting) y
                                 escaneo de seguridad (SAST)
                                 para detectar vulnerabilidades
                                 en dependencias.
Construcción de Imagen           Se empaqueta la aplicación en Docker Build, Buildpacks
                                 un contenedor (ej. Docker). Es
                                 crucial versionar la imagen (ej.
                                 usando el SHA del commit o
                                 SemVer) para trazabilidad.




Bloque IV - Punto 3                         143 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Etapa                             Descripción Técnica               Herramientas Comunes

Registro de Artefacto             La imagen generada se sube a      Amazon ECR, Azure ACR,
                                  un Container Registry. Este       Docker Hub
                                  actúa como la fuente de
                                  verdad para los despliegues.


3.3.2.3. Estrategias de Entrega y Despliegue (CD)

La fase de CD toma el artefacto generado en CI y lo despliega en los entornos de destino. Aquí se
distingue entre Entrega Continua (requiere aprobación manual para producción) y Despliegue
Continuo (totalmente automático si pasan los tests).
1. Actualización de Orquestadores El despliegue implica actualizar la definición del servicio
en el orquestador (ej. actualizar el Deployment de Kubernetes para usar la nueva etiqueta de la
imagen). Esto desencadena estrategias de actualización como Rolling Update para evitar tiempos
de inactividad.
2. Enfoque GitOps GitOps es el modelo operativo estándar moderno para gestionar despliegues
en Kubernetes.
    • Concepto: El estado deseado de la infraestructura y las aplicaciones se define declarativamente
      en un repositorio Git.
    • Mecanismo: Un agente de software (como Argo CD o Flux) que se ejecuta dentro del clúster
      monitoriza el repositorio. Si detecta una diferencia entre el estado deseado (Git) y el estado
      real (Clúster), sincroniza automáticamente los cambios.
    • Ventaja: Proporciona auditoría, control de versiones y capacidad de reversión (rollback)
      inmediata mediante comandos de Git (git revert).

3.3.2.4. Pruebas en el Pipeline: El reto de los microservicios

Las pruebas de integración tradicionales (End-to-End) son frágiles y lentas en microservicios. Se
promueve una estrategia de prueba diferente:
    • Pruebas de Contrato (Contract Testing): Es la técnica recomendada para asegurar que
      los microservicios pueden comunicarse entre sí sin romper la compatibilidad. Los
      consumidores definen un “contrato” (expectativas de solicitud/respuesta) y el proveedor
      verifica en su pipeline si cumple con ese contrato. Herramientas como Pact son estándar.
    • Pruebas de Componente: Aíslan el microservicio simulando (mocking) sus dependencias
      externas para probar su lógica interna de forma rápida.

3.3.2.5. Probables focos de examen

  1. Diferencia CI/CD: El tribunal puede pedir distinguir entre Continuous Delivery (el software
     está listo para desplegar, pero requiere aprobación humana) y Continuous Deployment (el
     despliegue a producción es automático).
  2. GitOps: Es muy probable una pregunta sobre este concepto. Claves: Git como única fuente
     de verdad, uso de declaraciones (YAML), y herramientas como Argo CD que sincronizan el
     estado.
  3. Independencia del Pipeline: Pregunta sobre si todos los microservicios deben compartir
     un mismo pipeline de construcción. La respuesta normativa es NO; cada microservicio

Bloque IV - Punto 3                          144 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


     debe tener su propio ciclo de vida y pipeline independiente para evitar el acoplamiento de
     despliegue (“lock-step release”).
  4. Artefactos Inmutables: El concepto de “construir una vez, desplegar en muchos lugares”
     (Build once, deploy many). Se debe generar una única imagen Docker en la fase de Build y
     usarla en QA, Staging y Producción, variando solo la configuración inyectada (variables de
     entorno).
  5. Contract Testing: Identificar las Pruebas de Contrato (Consumer-Driven Contracts) como
     la solución al problema de verificar la integración entre servicios sin levantar todo el sistema
     (evitando la fragilidad de los tests End-to-End).

3.3.3. Versionado y actualizaciones

En un sistema distribuido, los servicios evolucionan a diferentes velocidades. A diferencia de un
monolito, donde el código se compila y despliega conjuntamente, en microservicios no es viable
forzar a todos los clientes (otros microservicios o frontales) a actualizarse simultáneamente cada
vez que se modifica una interfaz. Por ello, el versionado es una disciplina crítica para gestionar el
riesgo y garantizar la compatibilidad.

3.3.3.1. Estrategias de Versionado Semántico (SemVer)

El estándar de facto para numerar versiones en microservicios es Semantic Versioning (SemVer).
Este esquema utiliza un formato de tres números: MAJOR.MINOR.PATCH (X.Y.Z).


Componente                        Incremento                        Significado e Impacto

MAJOR (X)                         Cambio incompatible               Breaking Change. La API ha
                                                                    cambiado de forma que rompe
                                                                    a los clientes existentes (ej.
                                                                    eliminar un campo obligatorio
                                                                    o renombrar un endpoint).
MINOR (Y)                         Cambio compatible                 Backward Compatible. Se
                                                                    añade funcionalidad nueva (ej.
                                                                    un nuevo endpoint o campo
                                                                    opcional) sin romper lo
                                                                    existente.
PATCH (Z)                         Corrección de errores             Backward Compatible.
                                                                    Correcciones internas de bugs
                                                                    que no afectan a la interfaz
                                                                    pública.


3.3.3.2. Mecanismos de implementación del versionado de API

Existen cuatro estrategias técnicas principales para exponer la versión de un servicio a sus
consumidores. La elección afecta a la caché, al enrutamiento y a la experiencia del desarrollador.
1. Versionado por URI (URI Versioning) La versión se incluye explícitamente en la ruta del
recurso. Es el método más común y fácil de implementar.
    • Ejemplo: GET /v1/clientes/123


Bloque IV - Punto 3                          145 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Ventajas: Explícito, fácil de probar en navegador, el cliente sabe exactamente qué obtiene.
    • Desventajas: “Contamina” la URI, puede llevar a duplicación de código en los controladores.
2. Versionado por Cabeceras (Header Versioning) Se utiliza una cabecera HTTP personalizada
para indicar la versión deseada.
    • Ejemplo: GET /clientes/123 con Header X-API-Version: 1
    • Ventajas: Mantiene las URIs limpias y semánticas.
    • Desventajas: Más difícil de probar manualmente (requiere herramientas como Postman o
      curl), complica el cacheo (requiere configurar la cabecera Vary).
3. Negociación de Contenido (Media Type Versioning) Se utiliza la cabecera estándar Accept
especificando la versión en el tipo MIME.
    • Ejemplo: Accept: application/vnd.miempresa.v1+json
    • Ventajas: Es la forma más “pura” según los principios REST (HATEOAS). Permite versionar
      la representación del recurso, no solo la API.
    • Desventajas: Alta complejidad de implementación y prueba.
4. Versionado por Parámetros de Consulta (Query Parameter) La versión se pasa como un
argumento en la query string.
    • Ejemplo: GET /clientes/123?version=1
    • Uso: Común en APIs públicas (como Amazon o Google) para facilitar el acceso rápido.

3.3.3.3. Gestión de la compatibilidad: Backward vs. Forward

El objetivo del versionado es evitar la ruptura de contratos. Para ello se aplican principios de
diseño defensivo:
  1. Compatibilidad hacia atrás (Backward Compatibility): Un cambio es compatible hacia
     atrás si los clientes construidos para la versión N pueden funcionar correctamente con la
     versión N+1 del servicio.
        • Técnica: Cambios aditivos. Añadir campos nuevos como opcionales, nunca eliminar o
          renombrar campos obligatorios en una versión MINOR.
  2. Ley de Postel (Principio de Robustez): “Sé conservador en lo que haces, sé liberal en lo que
     aceptas de los demás”.
        • Aplicación: Los microservicios deben ignorar los campos desconocidos en las
          respuestas JSON que consumen. Esto permite que el proveedor añada nuevos datos
          (Forward Compatibility) sin que el consumidor falle al deserializarlos.

3.3.3.4. Patrones de transición y despliegue

Cuando un cambio es inevitablemente rupturista (Breaking Change), se deben utilizar patrones
para gestionar la transición sin tiempo de inactividad.
1. Patrón Expand and Contract (Parallel Change) Es el método estándar para realizar cambios
estructurales (en base de datos o API) sin romper el sistema.
    • Fase 1 (Expand): Se añade la nueva funcionalidad/campo manteniendo la antigua. El
      servicio soporta ambas versiones simultáneamente.
    • Fase 2 (Migrate): Se actualizan gradualmente todos los clientes para usar la nueva versión.
    • Fase 3 (Contract): Una vez que el tráfico a la versión antigua es cero, se elimina el código y
      los campos antiguos.


Bloque IV - Punto 3                          146 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


2. Coexistencia de Endpoints Un mismo microservicio expone múltiples versiones de su API
simultáneamente en el mismo despliegue.
    • Mecanismo: El código tiene controladores para /v1/recurso y /v2/recurso.
    • Uso: Permite a los clientes migrar a su propio ritmo. Es preferible a desplegar servicios
      separados para evitar la complejidad operativa de mantener múltiples binarios en
      producción.

3.3.3.5. Probables focos de examen

  1. Definición de Breaking Change: Se suele preguntar qué tipo de cambio obliga a incrementar
     la versión MAJOR en SemVer. La respuesta clave es: eliminar un recurso, renombrar un
     campo obligatorio o cambiar el tipo de dato de un campo existente. Añadir un campo
     opcional es un cambio MINOR (no rompe).
  2. Ley de Postel: Es muy probable una pregunta sobre el principio de robustez en sistemas
     distribuidos. La respuesta correcta se refiere a ignorar los datos desconocidos en la recepción
     para tolerar la evolución de los servicios productores.
  3. Diferencias URI vs Header: Pregunta de comparación. El versionado por URI es más fácil
     de cachear y probar; el versionado por Header mantiene las URIs limpias pero complica la
     infraestructura de caché (Vary header).
  4. Patrón Expand and Contract: Identificar este patrón como la solución para realizar
     refactorizaciones o migraciones de base de datos sin tiempo de inactividad (zero-
     downtime) en entornos de microservicios.
  5. Consumer-Driven Contracts (CDC): Se puede preguntar cómo detectar automáticamente
     si un cambio de versión rompe a los clientes. La respuesta es el uso de Contract Testing (ej.
     Pact) en el pipeline de CI/CD para validar que la nueva versión cumple las expectativas de los
     consumidores antes de desplegar.

3.4. Monitorización y observabilidad
Esta sección aborda uno de los mayores desafíos en la administración de sistemas distribuidos: la
visibilidad. En un monolito, si algo fallaba, el administrador simplemente consultaba el archivo
de log en /var/log. En una arquitectura de microservicios con cientos de contenedores efímeros
que nacen y mueren dinámicamente, los métodos tradicionales son inútiles. Si un usuario reporta
lentitud, el problema podría estar en la red, en la base de datos de un servicio secundario o en una
fuga de memoria en un contenedor que ya ni siquiera existe.
Es fundamental distinguir entre monitorización (¿el sistema está sano?) y observabilidad (¿por
qué el sistema se comporta de esa manera?). La observabilidad es una propiedad del sistema que
permite inferir su estado interno basándose en los datos que genera externamente. Para lograr
esto, el administrador debe implementar una infraestructura que recolecte, agregue y visualice
datos en tiempo real, basándose en los “Tres Pilares de la Observabilidad”.
Sin estas herramientas, el sistema es una “caja negra”. A continuación, se detalla la función de
cada pilar y las herramientas estándar de la industria que se estudiarán:




Bloque IV - Punto 3                          147 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



                         Pregunta que
Pilar                    responde                   Naturaleza del Dato      Herramienta Típica

Logs (Registros)         “¿Qué ha pasado            Eventos discretos,       ELK Stack
                         exactamente?”              texto no estructurado    (Elasticsearch,
                                                    o JSON.                  Logstash, Kibana),
                                                                             Fluentd.
Métricas                 “¿Cuál es la tendencia     Datos numéricos       Prometheus
                         del sistema?”              agregables (CPU, RAM, (Recolección) y
                                                    Requests/seg).        Grafana
                                                                          (Visualización).
Trazas (Tracing)         “¿Dónde ha ocurrido el     Contexto de una          Jaeger, Zipkin
                         retraso?”                  petición a través de     (Integrado a menudo
                                                    múltiples servicios.     con Service Mesh).


Para que estos pilares sean útiles, se requiere una arquitectura de recolección centralizada. Un
error común es guardar los logs dentro del contenedor; si el contenedor muere, la “caja negra” del
avión se pierde con él. Por ello, se utilizan agentes (sidecars o daemons) que envían los datos a un
almacén central seguro.
El siguiente diagrama muestra cómo fluyen estos datos desde la aplicación hasta el administrador:




                                       Figure 9: Flujo de datos

La trazabilidad distribuida (3.4.3) merece una mención especial: permite asignar un “ID de
correlación” único a cada petición del usuario. Este ID viaja con la petición a través de todos los
microservicios, permitiendo al administrador reconstruir la historia completa de una transacción
(waterfall graph) y detectar cuellos de botella exactos, algo imposible de ver solo con logs o
métricas aisladas.

3.4.1. Logging centralizado

En una arquitectura de microservicios, el registro de eventos (logging) constituye la base de la
evidencia forense y la depuración operativa. A diferencia de los sistemas monolíticos, donde los
registros suelen escribirse en un único archivo en el disco local del servidor, los microservicios
son sistemas distribuidos que generan volúmenes masivos de datos desde múltiples instancias
efímeras. Por ello, es imperativo recolectar, procesar e indexar estos registros en un sistema
centralizado para tener una visión holística del sistema.




Bloque IV - Punto 3                          148 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.4.1.1. Principios de Logging en Sistemas Distribuidos (The 12-Factor App)

La metodología 12-Factor App establece el estándar de facto para el manejo de logs en aplicaciones
nativas de la nube.
  1. Logs como flujos de eventos (Event Streams): Los logs no deben tratarse como archivos
     estáticos, sino como una corriente continua de eventos ordenados cronológicamente. La
     aplicación no debe preocuparse por el enrutamiento o el almacenamiento de su flujo de
     salida.
  2. Salida estándar (stdout/stderr): Cada proceso en ejecución debe escribir su flujo de eventos,
     sin almacenamiento en búfer, directamente en la salida estándar (stdout) y en la salida de
     error estándar (stderr).
          • Desacoplamiento: Esto permite delegar la captura, agregación y almacenamiento a
            la infraestructura de ejecución (como Kubernetes o un agente de logging) en lugar de
            gestionarlo dentro del código de la aplicación.
  3. Efimeridad y Persistencia: Dado que los contenedores son efímeros (pueden reiniciarse
     o moverse entre nodos), escribir logs en el sistema de archivos local del contenedor es un
     anti-patrón que conlleva pérdida de datos. Los logs deben enviarse a un almacenamiento
     persistente centralizado fuera del ciclo de vida del contenedor.

3.4.1.2. Arquitectura de agregación: ELK y EFK Stack

Para gestionar la dispersión de logs, se implementa una arquitectura de tubería (pipeline) que
consta de tres etapas: recolección, almacenamiento/indexado y visualización.
1. Recolección y Envío (Shippers/Collectors) Son agentes encargados de capturar los logs de
stdout, enriquecerlos con metadatos (como el nombre del pod, namespace o ID del contenedor) y
enviarlos al almacén central.
    • Logstash: Herramienta tradicional del stack ELK. Potente para transformar datos, pero
      consume muchos recursos.
    • Fluentd / Fluent Bit: Estándar en entornos Kubernetes (Stack EFK). Fluent Bit es preferido
      por ser más ligero y eficiente en consumo de CPU/Memoria que Fluentd y Logstash.
    • Patrón Sidecar para Logging: Si una aplicación heredada solo sabe escribir en archivos y
      no en stdout, se despliega un contenedor secundario (sidecar) en el mismo pod que lee el
      archivo mediante el comando tail y lo redirige a su propia salida estándar, o ejecuta un
      agente de logging dedicado.
2. Almacenamiento e Indexación
    • Elasticsearch: Es el motor de búsqueda y análisis distribuido más utilizado. Almacena los
      logs como documentos JSON indexados, permitiendo búsquedas de texto completo a gran
      velocidad sobre millones de registros.
3. Visualización
    • Kibana: Es la interfaz gráfica que opera sobre Elasticsearch. Permite a los operadores crear
      paneles (dashboards), realizar búsquedas forenses, filtrar por campos y visualizar volúmenes
      de errores en tiempo real.
Tabla comparativa de Stacks Comunes:




Bloque IV - Punto 3                         149 de 164                             January 31, 2026
                          Correo electrónico. Contenedores y microservicios



                          Stack ELK                 Stack EFK
Componente                (Tradicional)             (Moderno/K8s)             Función

Recolección               Logstash (Pesado,         Fluentd / Fluent Bit      Captura y envío de
                          Java)                     (Ligero)                  logs.
Almacenamiento            Elasticsearch             Elasticsearch             Indexación y
                                                                              búsqueda.
Visualización             Kibana                    Kibana                    Interfaz de usuario.


3.4.1.3. Logs Estructurados y Correlación

Para que el logging centralizado sea efectivo y automatizable, los logs deben dejar de ser texto
plano no estructurado.
  1. Logging Estructurado (JSON): Se recomienda encarecidamente utilizar formatos
     estructurados como JSON. Esto permite que los sistemas de análisis indexen campos
     específicos (ej. user_id, status_code, latency) en lugar de tratar todo el log como una sola
     cadena de texto, facilitando el filtrado y la creación de métricas.
  2. Correlation ID (ID de Correlación): Es el mecanismo crítico para rastrear una solicitud a
     través de múltiples microservicios.
          • Funcionamiento: Cuando una petición entra al sistema (vía API Gateway), se le asigna
            un ID único (GUID). Este ID se propaga en las cabeceras HTTP a todos los servicios
            posteriores.
          • Registro: Cada microservicio debe incluir este Correlation ID en cada línea de log que
            genere. Esto permite que, al buscar dicho ID en Kibana, se reconstruya la historia
            completa de la transacción a través de todo el sistema distribuido.

3.4.1.4. Probables focos de examen

Basado en la literatura técnica y patrones de preguntas de oposición, los siguientes puntos son
críticos:
  1. Anti-patrón de escritura local: Pregunta clásica sobre dónde debe escribir logs un
     microservicio. La respuesta correcta es siempre a la salida estándar (stdout/console),
     nunca a un archivo local persistente dentro del contenedor, debido a la naturaleza efímera
     de los mismos.
  2. Componentes del Stack ELK: Es muy probable que se pida identificar la función de cada
     componente.
        • Elasticsearch: Base de datos/Motor de búsqueda.
        • Logstash: Recolector/Procesador.
        • Kibana: Visualizador/Dashboard.
  3. Diferencia Fluentd vs Logstash: En contextos de Kubernetes y Cloud Native, se suele
     preguntar por Fluentd o Fluent Bit como la alternativa más eficiente y estándar para la
     recolección de logs frente a Logstash.
  4. Importancia del Correlation ID: Se planteará un escenario de error en una cadena de
     microservicios y se preguntará cómo rastrear el problema. La respuesta clave es el uso de
     Correlation IDs inyectados en las cabeceras y registrados en los logs.



Bloque IV - Punto 3                           150 de 164                              January 31, 2026
                        Correo electrónico. Contenedores y microservicios


  5. Logging Estructurado: Identificar JSON como el formato preferido para permitir el análisis
     automatizado y la indexación por campos, en contraposición al texto plano.
  6. Seguridad y Logs: Un foco importante es la anonimización. Los logs NO deben contener
     información sensible (PII, contraseñas, tokens). Se debe aplicar enmascaramiento (masking)
     antes de almacenarlos para cumplir con normativas (GDPR/ENS).

3.4.2. Métricas y alertas

Las métricas constituyen uno de los tres pilares de la observabilidad (junto con los logs y las
trazas). Se definen como representaciones numéricas de datos medidos a lo largo del tiempo
(series temporales), que permiten observar el comportamiento del sistema en tiempo real y
analizar tendencias históricas.
A diferencia de los logs, que registran eventos discretos y detallados, las métricas son datos
agregados y comprimibles, lo que las hace extremadamente eficientes para el almacenamiento y
el procesamiento a largo plazo, siendo la herramienta principal para la detección inmediata de
problemas mediante alertas.

3.4.2.1. Tipos de métricas y niveles de monitorización

En una arquitectura de microservicios, es necesario capturar métricas en múltiples capas para
entender la salud completa del sistema. La literatura técnica clasifica estas métricas en cuatro
niveles fundamentales:
1. Métricas de Infraestructura (Node-level) Miden el consumo de recursos físicos o virtuales del
host. Son esenciales para detectar la saturación del hardware.
    • Ejemplos: Uso de CPU, consumo de memoria, E/S de disco, ancho de banda de red.
    • Herramientas: Node Exporter (en ecosistema Prometheus) o agentes de sistema.
2. Métricas de Contenedor y Orquestación Dado que los servicios corren en contenedores, se
deben recolectar estadísticas a este nivel, ya que un nodo puede estar sano pero un contenedor
específico puede estar siendo limitado (throttled) por límites de recursos (CPU limits/requests).
    • Ejemplos: Uso de CPU por pod, memoria del contenedor, reinicios de pods, estado de los
      despliegues.
    • Herramienta clave: cAdvisor (Container Advisor) en Kubernetes, que expone estadísticas
      de uso de recursos de cada contenedor.
3. Métricas de Aplicación (Service-level) Son específicas del comportamiento del microservicio
y su lógica. Son críticas para entender la experiencia del usuario.
    • Ejemplos: Latencia de respuesta HTTP, tasa de errores (códigos 4xx/5xx), número de
      peticiones por segundo (throughput), tamaño de las colas de mensajes.
    • Estándares de la industria:
        – Método RED: Rate (Tasa de peticiones), Errors (Errores), Duration (Latencia). Enfocado
           a microservicios.
        – Las 4 Señales Doradas (Google SRE): Latencia, Tráfico, Errores y Saturación.
4. Métricas de Negocio Miden el rendimiento de la organización en tiempo real, correlacionando
la salud técnica con el impacto operativo.
    • Ejemplos: Número de pedidos por minuto, ingresos generados, usuarios activos, carritos
      abandonados.


Bloque IV - Punto 3                        151 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.4.2.2. Arquitectura de recolección: Pull vs. Push

La estrategia de recolección de métricas es una decisión arquitectónica clave. Existen dos modelos
predominantes en las herramientas de monitorización:


Modelo                    Descripción              Herramienta Típica        Ventajas/Desventajas

Pull (Scraping)           El sistema de            Prometheus„               Ventaja: El servicio
                          monitorización                                     no necesita conocer al
                          solicita                                           servidor de
                          periódicamente las                                 monitorización
                          métricas al servicio a                             (desacoplamiento).
                          través de un endpoint                              Control centralizado
                          HTTP (ej. /metrics).                               de la frecuencia de
                                                                             lectura. Desventaja:
                                                                             Requiere
                                                                             descubrimiento de
                                                                             servicios para saber
                                                                             qué IPs “scrapear”.
Push                      El servicio envía        Graphite, InfluxDB,       Ventaja: Útil para
                          activamente las          CloudWatch,               trabajos efímeros
                          métricas al sistema de                             (batch jobs) que no
                          monitorización.                                    viven lo suficiente
                                                                             para ser scrapeados.
                                                                             Desventaja: Mayor
                                                                             acoplamiento; riesgo
                                                                             de inundar al servidor
                                                                             de monitorización
                                                                             con tráfico (DDoS
                                                                             accidental).


El estándar de facto en arquitecturas modernas de microservicios y Kubernetes es el modelo Pull
implementado por Prometheus.

3.4.2.3. Estrategias de Alertado

El objetivo de las alertas es notificar a los operadores humanos cuando el sistema se encuentra
en un estado que requiere intervención inmediata. Un diseño deficiente de alertas conduce a la
“fatiga de alertas” (alert fatigue), donde los operadores ignoran avisos críticos debido al exceso de
falsos positivos.
Principios para un alertado eficaz:
  1. Alertar sobre síntomas, no causas: Las alertas deben dispararse cuando el usuario se ve
     afectado (ej. “Alta latencia en Checkout” o “Tasa de errores elevada”), no solo por causas
     técnicas internas (ej. “CPU alta”). La CPU alta es útil para el diagnóstico, pero si el servicio
     sigue respondiendo rápido, no requiere despertar a un ingeniero a las 3 AM.
  2. Definición de Umbrales (SLI/SLO):



Bloque IV - Punto 3                          152 de 164                               January 31, 2026
                           Correo electrónico. Contenedores y microservicios


          • SLI (Service Level Indicator): La métrica que mide el nivel de servicio (ej. latencia
            actual).
          • SLO (Service Level Objective): El objetivo de disponibilidad (ej. el 99% de las peticiones
            deben responderse en < 200ms).
          • Las alertas deben configurarse cuando se quema el “presupuesto de error” o se viola el
            SLO.
  3. Gestión de Alertas (Alertmanager):           Herramientas como Alertmanager (parte del
     ecosistema Prometheus) permiten:
          • Agrupación (Grouping): Convertir 100 alertas de “servicio caído” (una por instancia)
            en una única notificación.
          • Inhibición (Inhibition): Si el cluster entero está caído, silenciar las alertas de los
            servicios individuales para evitar ruido.
          • Silenciamiento (Silencing): Pausar alertas durante ventanas de mantenimiento
            conocidas.

3.4.2.4. Probables focos de examen

Basado en la literatura técnica y la prevalencia de ciertas tecnologías en los temarios de
administración pública, estos son los puntos críticos:
  1. Prometheus y el modelo Pull: Es muy probable una pregunta sobre cómo obtiene datos
     Prometheus. La respuesta correcta es mediante un modelo Pull (Scraping), donde el servidor
     consulta periódicamente a los microservicios.
  2. Diferencia entre Métricas y Logs: Se suele pedir distinguir su uso. Las métricas son para
     detectar problemas y ver tendencias (baratas, agregadas); los logs son para diagnosticar la
     causa raíz y hacer análisis forense (detallados, caros).
  3. Método RED: Identificar las siglas de este estándar de monitorización de microservicios:
     Rate (Tasa), Errors (Errores), Duration (Duración/Latencia).
  4. Concepto de “Alert Fatigue”: Pregunta relacionada con la gestión de operaciones. Se refiere a
     la desensibilización de los administradores ante un exceso de alertas no accionables o falsos
     positivos.
  5. cAdvisor: Identificar a cAdvisor como el componente (generalmente integrado en el
     Kubelet de Kubernetes) encargado de recolectar métricas de uso de recursos (CPU, Memoria)
     directamente de los contenedores.
  6. Cardinalidad: Un problema técnico frecuente en métricas. Se refiere al número de
     combinaciones únicas de etiquetas (tags) en una métrica. Una cardinalidad excesiva (ej.
     incluir el ID de usuario o IP en una etiqueta de métrica) puede desbordar la base de datos de
     series temporales.

3.4.3. Trazabilidad distribuida

La trazabilidad distribuida (Distributed Tracing) es el mecanismo que permite rastrear y visualizar
el flujo de una solicitud (request) a medida que atraviesa los múltiples microservicios que
componen una aplicación distribuida.
En un sistema monolítico, la depuración se realiza siguiendo la pila de llamadas (stack trace) en
un único proceso. En una arquitectura de microservicios, una sola operación de usuario puede
desencadenar una cadena de llamadas a través de decenas de servicios en diferentes servidores,
lo que hace inútiles las herramientas de depuración tradicionales. La trazabilidad distribuida



Bloque IV - Punto 3                           153 de 164                               January 31, 2026
                          Correo electrónico. Contenedores y microservicios


reconstruye esta historia completa, permitiendo identificar cuellos de botella de rendimiento y la
causa raíz de los fallos.

3.4.3.1. Conceptos fundamentales: Trace y Span

La arquitectura de trazabilidad se basa en dos abstracciones principales que modelan la interacción
entre servicios:
  1. Trace (Traza): Representa el recorrido completo de una solicitud desde el inicio hasta el
     final a través del sistema distribuido. Es una colección de spans que comparten un mismo
     identificador de traza, organizados como un gráfico acíclico dirigido (DAG).
  2. Span (Tramo): Es la unidad básica de trabajo. Representa una operación individual dentro
     de un servicio (ej. una consulta a base de datos o una llamada HTTP). Cada span contiene:
        • Nombre de la operación.
        • Hora de inicio y finalización (duración/latencia).
        • Metadatos (etiquetas o tags) y registros de errores.
        • Referencias al span padre (Parent Span ID), lo que permite reconstruir la jerarquía de
          llamadas.

3.4.3.2. Propagación de Contexto y Correlation ID

Para vincular los eventos generados en distintos servidores, es imprescindible propagar el
contexto de la traza junto con la solicitud de red.
    • Correlation ID (ID de Correlación): Es un identificador único (GUID) que se genera cuando
      la solicitud entra por primera vez al sistema (generalmente en el API Gateway o Ingress).
    • Mecanismo de Propagación: Este ID debe inyectarse en las cabeceras HTTP (o metadatos
      gRPC/Kafka) de cada llamada saliente hacia los servicios dependientes. Si un solo servicio
      en la cadena rompe esta propagación (no reenvía las cabeceras), la traza se corta y se pierde
      la visibilidad completa.
    • Integración con Logs: Las mejores prácticas dictan que el Correlation ID debe escribirse
      también en cada línea de log generada por la aplicación. Esto permite cruzar la información
      de las trazas (rendimiento) con los logs (detalles del error) en herramientas como Kibana.

3.4.3.3. Muestreo (Sampling)

Generar y almacenar trazas para el 100% del tráfico en sistemas de alta carga puede generar una
sobrecarga (overhead) significativa en rendimiento y costes de almacenamiento. Para mitigar
esto, se utilizan estrategias de muestreo:
    • Muestreo Probabilístico: Se registra solo un porcentaje fijo de las solicitudes (ej. 0.1% o 1%).
    • Muestreo Adaptativo: Herramientas como Jaeger ajustan dinámicamente la tasa de
      muestreo basándose en el tráfico para garantizar que se capturan suficientes datos de trazas
      inusuales o erróneas sin saturar el sistema.

3.4.3.4. Herramientas y Estándares

El ecosistema de trazabilidad se ha estandarizado significativamente en los últimos años:
    • OpenTelemetry (OTel): Es el estándar actual de la industria (sucesor de OpenTracing y
      OpenCensus). Proporciona un conjunto unificado de SDKs y APIs para instrumentar, generar
      y recolectar métricas, logs y trazas de forma agnóstica al proveedor.


Bloque IV - Punto 3                           154 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Jaeger: Sistema de trazabilidad distribuida de código abierto (creado por Uber). Es
      ampliamente utilizado para visualizar grafos de llamadas y analizar latencias en
      arquitecturas de microservicios.
    • Zipkin: Otro sistema pionero en la trazabilidad distribuida, enfocado en ayudar a recopilar
      datos de tiempo para solucionar problemas de latencia.

3.4.3.5. Probables focos de examen

  1. Diferencia Trazabilidad vs. Logging: El examen puede pedir distinguir su utilidad. Los
     logs registran eventos discretos y aislados (el “qué” detallado), mientras que la trazabilidad
     registra el flujo y la relación entre servicios (el “dónde” y “cuánto tiempo”).
  2. Función del Correlation ID: Es fundamental identificar que el Correlation ID es el
     mecanismo técnico que permite reconstruir la historia de una transacción a través de
     múltiples hilos y servidores. Sin él, los logs son silos de información inconexa.
  3. Concepto de Span: Definición técnica de Span como la unidad atómica de una traza que
     contiene tiempos de inicio/fin y referencias al padre.
  4. Sampling como solución de rendimiento: Ante una pregunta sobre cómo evitar que
     la monitorización degrade el rendimiento del sistema, la respuesta correcta es la
     implementación de Muestreo (Sampling) o Muestreo Adaptativo.
  5. Relación con Service Mesh: Se puede preguntar cómo un Service Mesh facilita la trazabilidad.
     La respuesta es que proxies como Envoy pueden generar y propagar automáticamente las
     cabeceras de trazabilidad para el tráfico de red, aunque la aplicación a menudo debe colaborar
     reenviándolas.

3.4.4. Herramientas: Prometheus, Grafana, ELK Stack

El ecosistema de observabilidad en microservicios se ha estandarizado en torno a un conjunto
de herramientas de código abierto que abordan las tres dimensiones principales: métricas,
visualización y logs. La combinación más frecuente en la industria se conoce a menudo como la
“Pila Moderna de Monitorización” (Modern Monitoring Stack), compuesta por Prometheus para
métricas y alertas, el Stack ELK (o EFK) para logs, y Grafana como capa de visualización unificada.

3.4.4.1. Prometheus (Monitorización de Métricas)

Prometheus es un sistema de monitorización y alerta de código abierto, diseñado específicamente
para la fiabilidad en entornos dinámicos como Kubernetes. Se ha convertido en el estándar de
facto para la monitorización de métricas en arquitecturas de microservicios y nativas de la nube.
Arquitectura y Funcionamiento Prometheus se distingue por su modelo de datos y su mecanismo
de recolección:
  1. Modelo de datos: Almacena todos los datos como series temporales (time-series). Cada serie
     se identifica de forma única por un nombre de métrica y un conjunto de pares clave-valor
     llamados etiquetas (labels). Este modelo multidimensional permite realizar consultas y
     agregaciones flexibles.
  2. Modelo Pull (Scraping): A diferencia de los sistemas tradicionales que esperan que los
     agentes envíen datos (push), el servidor de Prometheus solicita (pulls) o “raspa” (scrapes)
     métricas periódicamente de los endpoints HTTP (típicamente /metrics) expuestos por los
     servicios monitorizados.
  3. Almacenamiento: Utiliza una base de datos de series temporales (TSDB) local en disco,
     optimizada para un alto rendimiento de escritura y consulta.


Bloque IV - Punto 3                         155 de 164                              January 31, 2026
                          Correo electrónico. Contenedores y microservicios


Componentes Principales
    • Servidor Prometheus: El núcleo que recolecta y almacena métricas.
    • Exportadores (Exporters): Son librerías o procesos que exponen métricas de sistemas de
      terceros (Linux, MySQL, HAProxy) en formato Prometheus. Por ejemplo, el Node Exporter se
      usa para métricas de hardware y sistema operativo.
    • Alertmanager: Componente independiente que gestiona las alertas enviadas por el servidor
      Prometheus. Se encarga de la deduplicación, agrupación y enrutamiento de notificaciones a
      receptores como correo electrónico, Slack o PagerDuty.
    • PromQL: Es el Lenguaje de Consulta de Prometheus. Permite filtrar, agregar y analizar datos
      en tiempo real (ej. calcular tasas de error o percentiles) para generar gráficos o definir reglas
      de alerta.

3.4.4.2. Grafana (Visualización y Análisis)

Grafana es una plataforma de análisis y visualización de código abierto que permite consultar,
visualizar, alertar y explorar métricas, logs y trazas, independientemente de dónde estén
almacenados.
Características Clave
  1. Agnóstico al origen de datos: Grafana no almacena los datos, sino que se conecta a múltiples
     fuentes de datos (Data Sources) como Prometheus, Elasticsearch, InfluxDB o bases de datos
     SQL.
  2. Paneles de Control (Dashboards): Permite crear tableros interactivos y personalizables
     con una amplia variedad de visualizaciones (gráficos de series temporales, mapas de calor,
     histogramas, medidores).
  3. Unificación (Single Pane of Glass): Su principal fortaleza en microservicios es la capacidad
     de combinar datos de diferentes fuentes (ej. métricas de Prometheus y logs de Elasticsearch)
     en un mismo panel para correlacionar eventos.

3.4.4.3. ELK Stack y EFK Stack (Gestión de Logs)

El ELK Stack es la solución más extendida para la búsqueda y análisis de logs centralizados. Está
compuesto por tres proyectos de código abierto: Elasticsearch, Logstash y Kibana. En entornos
de microservicios y Kubernetes, a menudo evoluciona hacia el EFK Stack, sustituyendo Logstash
por Fluentd o Fluent Bit.
Componentes
  1. Elasticsearch (Almacenamiento y Búsqueda): Es un motor de búsqueda y análisis
     distribuido basado en Lucene. Actúa como el almacén central donde se indexan los logs
     como documentos JSON, permitiendo búsquedas de texto completo extremadamente
     rápidas sobre grandes volúmenes de datos.
  2. Logstash / Fluentd (Ingesta y Procesamiento):
        • Logstash: Es la herramienta tradicional de procesamiento de datos del lado del
          servidor (ETL). Ingiere datos de múltiples fuentes, los transforma (parseo, filtrado,
          anonimización) y los envía a Elasticsearch. Es potente pero consume muchos recursos.
        • Fluentd / Fluent Bit: Alternativas más ligeras y eficientes, preferidas en entornos de
          contenedores (Kubernetes) para recolectar logs y enviarlos a Elasticsearch. Fluent Bit
          es especialmente ligero.




Bloque IV - Punto 3                           156 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  3. Kibana (Visualización): Es la interfaz de usuario para Elasticsearch. Permite a los operadores
     buscar y visualizar logs, crear gráficos de barras o circulares y mapas, y realizar análisis
     forenses de incidencias.
Flujo de Trabajo Típico Un microservicio escribe logs en stdout. Un agente (Logstash/Fluentd)
recoge estos logs, los procesa (extrae campos como timestamp, service_name, error_code) y los
envía a Elasticsearch. El operador utiliza Kibana para buscar un Correlation ID específico y ver
todos los logs asociados a una transacción distribuida.

3.4.4.4. Probables focos de examen

  1. Modelo Pull de Prometheus: Es muy probable que se pregunte por la diferencia fundamental
     en la recolección de datos. Prometheus utiliza un modelo Pull (el servidor contacta al
     microservicio), mientras que sistemas tradicionales o herramientas como InfluxDB suelen
     usar un modelo Push (el agente envía datos al servidor).
  2. Componentes del Stack ELK: Identificar la función exacta de cada sigla:
        • Elasticsearch: Base de datos / Motor de búsqueda.
        • Logstash: Procesamiento y tubería de datos (Ingesta).
        • Kibana: Visualización e Interfaz de usuario.
  3. PromQL: Reconocer PromQL como el lenguaje de consulta específico utilizado por
     Prometheus para agregar y analizar métricas de series temporales.
  4. Uso de Exportadores: Entender que para monitorizar sistemas que no exponen métricas
     nativas de Prometheus (como el kernel de Linux o una base de datos legacy), se utiliza un
     Exporter (patrón Adapter).
  5. Diferencia Grafana vs. Kibana:
        • Grafana se especializa en métricas y series temporales (visualización de rendimiento,
          CPU, memoria) y soporta múltiples datasources.
        • Kibana se especializa en logs y búsqueda de texto (análisis forense, causa raíz) y está
          estrechamente acoplado a Elasticsearch.

3.5. Gestión de configuración y secretos
Esta última sección cierra el temario abordando un principio fundamental de la metodología
Cloud Native (específicamente el factor III de la “12-Factor App”): la estricta separación entre el
código y la configuración. En la administración moderna, una imagen de contenedor debe ser
inmutable; es decir, el mismo artefacto binario generado en desarrollo debe ser el que llegue a
producción.
Si la imagen del contenedor no cambia entre entornos (Desarrollo, Preproducción, Producción),
la única forma de que la aplicación sepa a qué base de datos conectarse o qué nivel de logging
utilizar es inyectando esa información desde el exterior en tiempo de ejecución. El administrador
de sistemas es el responsable de gestionar estos “diccionarios de configuración” y asegurar que
lleguen al contenedor correcto.
Sin embargo, no toda la configuración es igual. Debemos distinguir claramente entre datos
inocuos (URLs, colores, timeouts) y datos sensibles (contraseñas, claves API, certificados). Tratar
una contraseña como una simple variable de entorno o, peor aún, incluirla en el repositorio de
código (hardcoding), es una vulnerabilidad crítica de seguridad.
A continuación, se comparan los mecanismos que se estudiarán para gestionar estos datos según
su sensibilidad:



Bloque IV - Punto 3                         157 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios



Mecanismo                Uso Recomendado           Nivel de Seguridad        Ejemplo de Dato

Variables de Entorno     Configuración básica      Bajo (visible en          LOG_LEVEL=DEBUG,
                         no sensible.              inspectores de            APP_COLOR=BLUE
                                                   procesos).
ConfigMaps /             Ficheros de               Medio (desacoplado        nginx.conf,
Ficheros                 configuración             pero texto plano).        settings.json
                         complejos.
Gestores de Secretos     Credenciales críticas y   Alto (Cifrado en          DB_PASSWORD,
(Vault)                  certificados.             reposo y tránsito).       AWS_SECRET_KEY



Para el punto 3.5.3. Vault, es crucial entender que herramientas como HashiCorp Vault no
solo almacenan contraseñas cifradas, sino que permiten la gestión dinámica de secretos. Esto
significa que la aplicación solicita una credencial temporal para acceder a la base de datos, y Vault
la genera “al vuelo” y la revoca después, reduciendo la ventana de oportunidad de un ataque.
El siguiente diagrama ilustra cómo se ensambla una aplicación moderna en el momento del
despliegue, combinando tres fuentes distintas de verdad:




                                 Figure 10: Ensamblaje en despliegue

El dominio de esta gestión permite al administrador rotar contraseñas sin detener el servicio,
auditar quién accedió a qué secreto y garantizar que los desarrolladores nunca necesiten conocer
las credenciales de producción, estableciendo una verdadera separación de roles.

3.5.1. Configuración externalizada

La gestión de la configuración es uno de los pilares fundamentales para lograr la portabilidad
y escalabilidad en arquitecturas de microservicios. En este modelo, la configuración se define
como todo aquello que puede variar entre despliegues (entornos de desarrollo, preproducción,
producción), como credenciales de base de datos, URLs de servicios externos o credenciales de
backend, mientras que el código permanece invariable.




Bloque IV - Punto 3                          158 de 164                               January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.5.1.1. El principio de los 12 Factores (Factor III: Config)

La metodología The Twelve-Factor App establece como regla de oro la estricta separación entre
configuración y código.
    • Definición: La configuración debe almacenarse en el entorno, no en el repositorio de código
      fuente.
    • Anti-patrón: Guardar constantes de configuración en el código (hardcoding) o tener archivos
      de configuración (como config.dev.properties o config.prod.properties) confirmados en
      el control de versiones es una mala práctica, ya que vincula el código a un entorno específico
      y aumenta el riesgo de filtrar credenciales.
    • Prueba de fuego: Una aplicación está correctamente factorizada si el código fuente puede
      hacerse público (open source) en cualquier momento sin comprometer ninguna credencial
      ni revelar detalles específicos del entorno de despliegue.

3.5.1.2. Estrategias de implementación técnica

Existen tres mecanismos principales para externalizar la configuración en sistemas distribuidos,
ordenados de menor a mayor complejidad operativa:
1. Variables de Entorno (Environment Variables) Es el mecanismo estándar recomendado por
los 12 Factores por ser universal y agnóstico al lenguaje o sistema operativo.
    • Funcionamiento: Los valores se inyectan en el proceso en tiempo de ejecución. En
      Java/Spring Boot, por ejemplo, se pueden leer mediante System.getenv() o la anotación
      @Value.
    • Ventajas: Simplicidad, soporte nativo en todas las plataformas cloud (AWS, Azure, Heroku)
      y contenedores (Docker).
    • Limitaciones: Dificultad para manejar configuraciones jerárquicas complejas o tipos de
      datos estructurados; riesgo de exposición en logs si no se gestionan con cuidado.
2. Archivos de Configuración Inyectados (Volúmenes) Común en entornos orquestados como
Kubernetes. La configuración se almacena en objetos del clúster (ConfigMaps) y se “monta” dentro
del contenedor como un archivo físico (ej. application.properties) en tiempo de ejecución.
    • Ventaja: Permite gestionar archivos complejos sin reconstruir la imagen del contenedor.
      Desacopla el ciclo de vida de la configuración del ciclo de vida de la aplicación.
3. Servidor de Configuración Centralizada (Centralized Configuration Server) Para sistemas
con decenas o cientos de microservicios, gestionar variables de entorno dispersas se vuelve
inmanejable. Se utiliza un servicio dedicado que actúa como “fuente de verdad” única.
    • Mecanismo: Al arrancar, el microservicio consulta al servidor de configuración (vía API
      REST) para obtener sus propiedades antes de iniciar su lógica de negocio.
    • Backing con Git: Herramientas como Spring Cloud Config permiten usar un repositorio
      Git como backend para almacenar los archivos de configuración. Esto habilita GitOps:
      versionado, auditoría y trazabilidad de los cambios en la configuración (quién cambió qué y
      cuándo).

3.5.1.3. Inmutabilidad de los artefactos (Build, Release, Run)

La externalización es un requisito previo para lograr artefactos inmutables. El objetivo es
“construir una vez, desplegar en muchos lugares” (Build once, deploy many).



Bloque IV - Punto 3                          159 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Proceso:
        1. Build: Se compila el código y se empaqueta en una imagen Docker. Esta imagen es
            idéntica para todos los entornos.
        2. Release: Se toma la imagen del paso anterior y se combina con la configuración
            específica del entorno de destino (Dev, Test, Prod).
        3. Run: Se ejecuta la aplicación en el entorno.
    • Si la configuración estuviera dentro del código, se requeriría una nueva compilación (Build)
      para cambiar de entorno, violando la inmutabilidad y aumentando el riesgo de diferencias
      entre lo probado y lo desplegado.

3.5.1.4. Herramientas destacadas


Herramienta                      Descripción                         Uso Típico

Spring Cloud Config              Servidor centralizado que           Ecosistemas Java/Spring.
                                 sirve configuraciones desde
                                 Git, SVN o Vault. Soporta
                                 refresco en caliente (“hot
                                 reload”) sin reiniciar servicios.
Kubernetes ConfigMap             Recurso nativo de K8s para          Orquestación de
                                 almacenar datos no                  contenedores.
                                 confidenciales en pares
                                 clave-valor. Se pueden
                                 consumir como variables de
                                 entorno o volúmenes.
Consul (HashiCorp)               Almacén de clave-valor              Arquitecturas agnósticas.
                                 distribuido que también
                                 ofrece descubrimiento de
                                 servicios. Permite cambios de
                                 configuración dinámicos.
AWS Systems Manager              Servicio gestionado para            Entornos nativos de AWS.
Parameter Store                  almacenar datos de
                                 configuración y secretos
                                 jerárquicos.


3.5.1.5. Probables focos de examen

  1. Principio “Build Once, Deploy Many”: El tribunal suele preguntar por qué es necesario
     externalizar la configuración. La respuesta clave es: para permitir que el mismo artefacto
     binario (imagen) se despliegue en múltiples entornos sin recompilación, garantizando la
     consistencia.
  2. ConfigMaps vs. Secrets: Distinguir su uso en Kubernetes. Los ConfigMaps son para datos
     no confidenciales (URLs, parámetros de UI), mientras que los Secrets (que se verán en 3.5.3)
     son para datos sensibles, aunque ambos se inyectan de forma similar.
  3. Factor III de 12-Factor App: Identificar que el tercer factor (“Config”) exige explícitamente
     guardar la configuración en el entorno (variables de entorno), no en el código.



Bloque IV - Punto 3                         160 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


  4. Spring Cloud Config y Git: Reconocer que esta herramienta permite versionar la
     configuración utilizando Git como backend, facilitando la auditoría y el rollback de cambios
     de configuración.
  5. Diferencia Configuración vs. Datos: Entender que la configuración no incluye los datos de
     la base de datos (usuarios, pedidos), sino los parámetros para conectar a esa base de datos o
     credenciales de servicios externos.

3.5.2. Gestión de variables de entorno

La gestión de variables de entorno se ha establecido como el mecanismo estándar “de facto” para
la inyección de configuración en aplicaciones nativas de la nube y arquitecturas de microservicios.
Este enfoque responde directamente al tercer principio de la metodología Twelve-Factor App,
que estipula que la configuración (todo lo que varía entre despliegues) debe almacenarse en el
entorno y no en el código fuente.

3.5.2.1. Definición y Propósito

Las variables de entorno son pares clave-valor dinámicos que el sistema operativo pone a
disposición de los procesos en ejecución. En el contexto de microservicios, actúan como un
mecanismo de desacoplamiento que permite que un mismo artefacto de construcción (imagen
de contenedor inmutable) se comporte de manera diferente según el entorno (Desarrollo, QA,
Producción) en el que se despliegue, simplemente modificando los valores inyectados al arrancar
el contenedor.
Su uso principal abarca la definición de parámetros no confidenciales pero variables, tales como:
    • Niveles de registro (logging levels).
    • URLs de servicios dependientes o bases de datos.
    • Interruptores de funcionalidad (Feature Toggles).
    • Puertos de escucha del servicio.

3.5.2.2. Implementación en Contenedores y Orquestadores

La adopción universal de este mecanismo se debe a su soporte nativo en todos los sistemas
operativos y lenguajes de programación modernos.
1. En Docker Las variables pueden definirse en tiempo de construcción dentro del Dockerfile
mediante la instrucción ENV, o inyectarse en tiempo de ejecución mediante el flag -e en el comando
docker run. Esto permite sobrescribir los valores predeterminados sin reconstruir la imagen.

2. En Kubernetes (Patrón EnvVar Configuration) Kubernetes permite definir variables de entorno
directamente en la especificación del Pod o Deployment. Existen dos métodos principales para
poblar estas variables:
    • Definición literal: Se especifica el valor directamente en el manifiesto YAML (value:
      "producción").
    • Delegación (Indirección): El valor se obtiene referenciando objetos externos como
      ConfigMaps (configMapKeyRef) o Secrets (secretKeyRef). Esto permite gestionar la
      configuración de forma independiente al ciclo de vida del Pod.
Adicionalmente, Kubernetes permite la composición de variables dependientes, donde el valor de
una variable puede hacer referencia a otra previamente definida (ej. $(IP):$(PORT)), resolviéndose
en el momento del arranque del contenedor.


Bloque IV - Punto 3                         161 de 164                             January 31, 2026
                         Correo electrónico. Contenedores y microservicios


3.5.2.3. Limitaciones y Desafíos

A pesar de su simplicidad y ubicuidad, el uso exclusivo de variables de entorno presenta
desventajas significativas en sistemas complejos a gran escala:
  1. Falta de Estructura Jerárquica: Las variables de entorno son cadenas de texto planas.
     No soportan nativamente estructuras de datos complejas o jerárquicas (como objetos
     JSON o YAML anidados), lo que obliga a utilizar convenciones de nombrado prolijas (ej.
     SPRING_DATASOURCE_Hikari_connectionTimeout).
  2. Inmutabilidad en Tiempo de Ejecución: Una variable de entorno solo puede establecerse
     antes de que el proceso inicie. Una vez que la aplicación está en ejecución, no es posible
     cambiar el valor de una variable de entorno sin reiniciar el proceso o el contenedor. Aunque
     esto favorece la inmutabilidad, impide la reconfiguración “en caliente” (hot-reload).
  3. Riesgos de Seguridad: Aunque son mejores que el código hardcodeado, las variables de
     entorno no son inherentemente seguras. Pueden filtrarse accidentalmente en registros
     de errores (logs), volcados de memoria o ser inspeccionadas a través de comandos del
     sistema operativo (ps eww o docker inspect), exponiendo secretos si no se gestionan
     adecuadamente.

3.5.2.4. Probables focos de examen

Basado en la literatura técnica y la metodología de 12 factores, los siguientes puntos son críticos
para el examen:
  1. El Tercer Factor (Config): Pregunta clásica sobre la metodología Twelve-Factor App. Debe
     identificar que la recomendación explícita es almacenar la configuración en el entorno
     (variables de entorno), no en archivos de propiedades dentro del repositorio.
  2. Diferencia entre ConfigMap y Variable de Entorno: Es posible que se pida distinguir los
     conceptos en Kubernetes. Los ConfigMaps son el recurso de almacenamiento (el “dónde”
     se guarda la configuración), mientras que las variables de entorno son el mecanismo de
     consumo (el “cómo” la aplicación lee esa configuración).
  3. Seguridad y Secretos: Un error común es considerar las variables de entorno como un
     almacenamiento seguro. El examen puede plantear si es seguro pasar contraseñas en texto
     plano como variables de entorno. La respuesta técnica correcta es que NO es la práctica
     recomendada para datos altamente sensibles debido al riesgo de exposición en logs o
     inspección de procesos; se deben usar gestores de secretos (Vault, Kubernetes Secrets)
     inyectados preferiblemente como volúmenes o variables cifradas.
  4. Reinicio obligatorio: Entender que un cambio en una variable de entorno requiere
     el reinicio (o redepliegue) del microservicio para que surta efecto, a diferencia de los
     volúmenes montados que pueden actualizarse en tiempo real.

3.5.3. Vault y gestión de secretos

En un entorno de microservicios, la proliferación de servicios aumenta exponencialmente el
número de credenciales (contraseñas de base de datos, claves de API, certificados TLS) necesarias
para la operación. La gestión tradicional mediante archivos de configuración o variables de
entorno dispersas presenta graves riesgos de seguridad, conocidos como “dispersión de secretos”
(secret sprawl).
HashiCorp Vault se ha establecido como la herramienta estándar en la industria para centralizar,
asegurar y controlar el acceso a estos secretos. Su filosofía se basa en no confiar en ninguna red



Bloque IV - Punto 3                         162 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


interna y autenticar explícitamente cada solicitud mediante identidad, no solo por ubicación de
red.

3.5.3.1. Arquitectura y principios de funcionamiento

Vault actúa como un intermediario de confianza (trusted broker) entre los clientes (microservicios,
usuarios) y los sistemas sensibles (bases de datos, nubes públicas).
1. Almacenamiento Cifrado y Barrera de Seguridad Vault no almacena los datos en texto plano.
Todos los datos se cifran antes de escribirse en el almacenamiento persistente (backend), que
puede ser Raft (integrado), Consul, o almacenamiento en la nube (S3, GCS).
    • Cifrado en reposo: Si un atacante roba el disco duro donde reside la data de Vault, solo
      obtendrá datos cifrados inútiles sin la clave maestra de cifrado.
2. Sellado y Desellado (Shamir’s Secret Sharing) Al iniciarse, Vault se encuentra en estado sellado
(sealed). No conoce su propia clave maestra de cifrado; esta se encuentra cifrada por una “clave de
desellado”. Para reconstruir esta clave y abrir la bóveda, Vault utiliza el algoritmo de Shamir’s
Secret Sharing (Esquema de Shamir). La clave se divide en N partes (shares) y se requiere un
umbral mínimo T (por defecto 3 de 5) para reconstruirla. Esto evita que un solo administrador
tenga el control total (“Two-man rule”).
3. Autenticación y Autorización (Identity-based) Vault desacopla la autenticación de la
autorización:
    • Métodos de Autenticación (Auth Methods): Verifican quién es el cliente. Soportan humanos
      (LDAP, Userpass) y máquinas (AppRole, Kubernetes, AWS IAM).
    • Políticas (Policies): Una vez autenticado, Vault emite un Token. Las capacidades de
      ese token (lectura, escritura) están definidas por políticas escritas en lenguaje HCL
      (HashiCorp Configuration Language) que autorizan el acceso a rutas específicas (path
      "secret/data/app" { capabilities = ["read"] }).


3.5.3.2. Secretos Dinámicos (Dynamic Secrets)

Esta es la funcionalidad más distintiva y potente de Vault frente a gestores de secretos
tradicionales o variables de entorno.
Concepto: En lugar de almacenar una contraseña estática de larga duración (ej. admin/1234),
Vault genera credenciales efímeras y únicas en el momento en que un microservicio las solicita
(“Just-in-Time credentials”).
Flujo de trabajo:
  1. El microservicio se autentica ante Vault.
  2. Solicita acceso a la base de datos (ej. PostgreSQL).
  3. Vault se conecta a la base de datos, crea un usuario temporal (ej. v-token-readonly-xyz) con
     permisos restringidos.
  4. Vault devuelve las credenciales al microservicio.
  5. Arrendamiento (Lease) y Revocación: Las credenciales tienen un Tiempo de Vida (TTL)
     asociado. Cuando el TTL expira, Vault revoca (borra) automáticamente el usuario en la base
     de datos.
Ventajas clave:
    • Si una credencial es robada, su vida útil es mínima.


Bloque IV - Punto 3                         163 de 164                              January 31, 2026
                         Correo electrónico. Contenedores y microservicios


    • Permite rastrear qué instancia específica de servicio realizó qué acción (atribución única).
    • Elimina la necesidad de rotación manual de contraseñas.

3.5.3.3. Cifrado como Servicio (Transit Engine)

El motor de secretos de tránsito (Transit Secrets Engine) permite a Vault actuar como una utilidad
criptográfica (“Encryption as a Service”).
    • Funcionamiento: Los microservicios envían datos sensibles (ej. número de tarjeta de crédito)
      a Vault a través de su API. Vault cifra los datos y devuelve el texto cifrado (ciphertext). El
      microservicio almacena este texto cifrado en su propia base de datos.
    • Beneficio: El microservicio nunca gestiona las claves de cifrado, y Vault nunca almacena
      los datos del negocio. Esto simplifica el cumplimiento normativo (PCI-DSS), ya que la
      criptografía está centralizada y auditada.

3.5.3.4. Probables focos de examen

Basado en la documentación técnica y patrones de seguridad en sistemas distribuidos, estos son
los puntos críticos:
  1. Secretos Dinámicos vs. Estáticos: Pregunta fundamental. Los secretos estáticos se
     almacenan y rotan manualmente; los dinámicos se generan bajo demanda, son únicos por
     cliente y se revocan automáticamente tras su TTL.
  2. Algoritmo de Shamir: Identificar que el mecanismo de seguridad para el inicio (“desellado”)
     de Vault es la Compartición de Secretos de Shamir (Shamir’s Secret Sharing), que divide la
     clave maestra en fragmentos distribuidos entre varios operadores.
  3. Concepto de “Lease” (Arrendamiento): Entender que todos los secretos dinámicos en Vault
     tienen un contrato de arrendamiento asociado con un TTL. Si no se renueva, el secreto se
     revoca.
  4. Diferencia AppRole vs. Userpass:
        • Userpass: Para humanos (usuario/contraseña).
        • AppRole: Método estándar para máquinas/microservicios, diseñado para la
          automatización sin intervención humana.
  5. Anti-patrón de almacenamiento: Vault NO debe usarse para almacenar grandes volúmenes
     de datos generales, sino para credenciales y claves. Para cifrar datos de aplicación, se usa el
     Transit Engine sin que Vault guarde los datos (solo gestiona las claves).




Bloque IV - Punto 3                          164 de 164                              January 31, 2026
