           RESUMEN ADMINISTRACIÓN DE
 SERVIDORES DE CORREO ELECTRÓNICO
  Administración de servidores de correo electrónico y sus
  protocolos .................................................................................... 1
     Protocolos de correo electrónico (SMTP, POP3, IMAP4).......... 1
     Puertos de correo electrónico ................................................... 2
     Seguridad y Protección del correo ............................................ 3
     Administración y Almacenamiento ............................................ 4
  Administración de contenedores y microservicios ........................ 4
     Arquitecturas de microservicios ................................................ 4
     Administración de contenedores (Docker y otros) .................... 5
     Orquestación con Kubernetes (K8s) ......................................... 6



 Administración de servidores de correo electrónico y sus
                        protocolos
Protocolos de correo electrónico (SMTP, POP3, IMAP4)
  • SMTP (Simple Mail Transfer Protocol): "Se usa desde el
    ordenador del usuario de origen al servidor de correo
    electrónico en el origen, así como desde el servidor de origen
    al servidor de destino". Es el protocolo empleado "para
    gestionar el correo saliente".
       o Lista de comandos mínima para receptores: "EHLO,
          HELO, MAIL, RCPT, DATA, RSET, NOOP, QUIT, VRFY".
       o Orden para indicar destinatario: "rcpt to".
       o Códigos SMTP Clave:
             ▪ 250: Acción de correo completada con éxito (OK).
             ▪ 421: Servicio no disponible, el canal de transmisión
                se cerrará.
             ▪ 550: Acción no realizada: el buzón no existe o no
                está disponible.
             ▪ 554: Transacción fallida (error genérico).
  • POP3 (Post Office Protocol v3): Protocolo de acceso al
    correo. Permite que el usuario "descargue sus mensajes a su

                                                                                    Página | 1
      cliente, de modo que ya no siguen en el buzón central sino
      simplemente en el de su cliente local".
          o Comando POP3: "STAT".
  •   IMAP (Internet Message Access Protocol): Protocolo de
      acceso al correo. "Sus mensajes permanecen en el buzón
      central aunque desde el cliente puede borrarlos, moverlos o
      responderlos". "Permite visualizar los correos directamente en
      el servidor sin descargarlos".
  •   X.400: "Estándar inicialmente para el intercambio de mensajes
      entre hosts TCP/IP".
  •   Exchange ActiveSync: "Protocolo de sincronización, basado
      en HTTP y XML, que permite que dispositivos móviles
      obtengan acceso a la información de una organización (emails,
      calendario, etc.) alojada en servidor/es Microsoft Exchange".
  •   MUA (Mail User Agent): El cliente de correo (Outlook,
      Thunderbird).
  •   MTA (Mail Transfer Agent): El servidor que envía/recibe
      (Postfix, Sendmail). Usa SMTP.
  •   MDA (Mail Delivery Agent): El que deposita el correo en el
      buzón del usuario para que POP/IMAP lo recojan.




Puertos de correo electrónico
Tabla de puertos de correo (Estándar e IANA):
Protocolo Puerto Estándar Puerto Seguro (TLS/SSL)
SMTP      25              465

                                                         Página | 2
POP3        110                995
IMAP        143                993


  • QUICK Mail Transfer Protocol (qmtp): Utiliza el puerto 209.
Enfoque CPS: El tribunal suele preguntar por la diferencia operativa
entre POP3 (borra del servidor) e IMAP (mantiene en servidor). Es
una "pregunta trampa" clásica incluir Outlook como protocolo,
cuando es un cliente. También se debe memorizar que SMTP se usa
tanto para el envío cliente-servidor como servidor-servidor.


Seguridad y Protección del correo
  • SPF (Sender Policy Framework): "Protocolo que protege
    contra la falsificación de direcciones en el envío de correo
    electrónico identificando los servidores de correo SMTP
    autorizados para el transporte de los mensajes a través de los
    registros de nombres de dominio (DNS)".
  • DKIM (DomainKeys Identified Mail): Añade una firma digital
    a las cabeceras para verificar que el mensaje no ha sido
    alterado.
  • DMARC: Es la política que dice qué hacer si SPF o DKIM fallan
    (ej. rechazar el correo o mandarlo a SPAM).




  • S/MIME: "Protocolo usado para el envío de correos
    electrónicos seguros".
  • PGP (Pretty Good Privacy): "Sistema de cifrado asimétrico"
    para asegurar la confidencialidad en infraestructuras de correo.
  • Sophos / IronPort: Soluciones para la "protección de sistemas
    de correo electrónico".
  • Antispam: Filtro para calificar mensajes como Spam a partir de
    un determinado umbral.

                                                         Página | 3
  • STARTTLS: Importante mencionar que es el comando para
    convertir una conexión insegura en segura en el mismo puerto.
  • Open Relay (Relay Abierto): Servidor de correo que permite
    el envío de mensajes desde cualquier origen a cualquier
    destino sin autenticación. Es una vulnerabilidad crítica que
    facilita el spam.
  • RBL (Real-time Blackhole List): Listas de direcciones IP en
    tiempo real conocidas por enviar spam que los servidores
    consultan para bloquear tráfico.


Administración y Almacenamiento
  • Servidores habituales: Postfix (común en distribuciones
    Linux), Microsoft Exchange Server.
  • Ubicación recomendada: Según el CCN-CERT, el servidor de
    correo corporativo debe estar "ubicado en una zona
    desmilitarizada (DMZ)".
  • Formatos de buzón:
       o mbox: "Formato que guarda correo electrónico en un
          único fichero".
       o maildir: Formato que guarda cada mensaje en un fichero
          separado.
  • Configuración Postfix: necesidad de editar el fichero
    /etc/postfix/main.cf para cambiar el mensaje HELO del
    servidor.
  • DAG (Database Availability Group): En Microsoft Exchange
    2013, los posibles estados de una base de datos son activa y
    pasiva.


      Administración de contenedores y microservicios
Arquitecturas de microservicios
  • Definición: "Las funcionalidades se implementan mediante la
    composición de distintos microservicios".
  • Estrategias de composición: Existen dos estrategias para
    gestionar esta composición: Coreografía (descentralizada) y
    orquestación (centralizada).


                                                       Página | 4
  • Beneficios: "Permite un escalado flexible, admite integración y
    entrega continuas (CI/CD), y mejora la resistencia a errores
    permitiendo degradar una funcionalidad sin bloquear toda la
    aplicación".
  • Patrón Sidecar: Consiste en colocar un contenedor
    secundario (sidecar) junto al contenedor principal dentro del
    mismo Pod. Comparten el mismo ciclo de vida y red (útil para
    logs, proxies o seguridad).




Administración de contenedores (Docker y otros)
  • Docker: Método que permite la fácil creación de contenedores
    para la ejecución de aplicaciones.
       o Persistencia de datos: "El mecanismo preferido por los
          contenedores Docker para persistir los datos son los
          Volúmenes".
       o Comandos Docker:
             ▪ docker ps: Lista contenedores en ejecución.
             ▪ docker info: "Muestra la información que tiene todo
                el sistema sobre la instalación de Docker (nº de
                contenedores, imágenes…)".
       o Dockerfile: Menciona que es el fichero de texto con
          instrucciones para crear la imagen.
       o Capas (Layers): Las imágenes Docker son de solo
          lectura y se componen de capas. Al ejecutar un
          contenedor, se añade una fina capa de lectura/escritura
          en la parte superior.


                                                        Página | 5
       o Diferencia CMD vs ENTRYPOINT: (Pregunta clásica)
          CMD Proporciona argumentos por defecto para el
          ENTRYPOINT o un comando inicial que sí puede ser
          sobrescrito por el usuario al hacer docker run.
          ENTRYPOINT Es el comando ejecutable principal que
          siempre se ejecuta al iniciar el contenedor (no se
          sobrescribe fácilmente).
       o Redes en Docker:
             ▪ bridge (por defecto): Crea una red virtual interna
                 para los contenedores.
             ▪ host: El contenedor comparte la pila de red
                 directamente con el host (sin aislamiento de red).
  • LXC (Linux Containers): "Tecnología de virtualización en el
    nivel de sistema operativo para Linux".
  • Otras tecnologías relacionadas: "Containerd y Podman".


Orquestación con Kubernetes (K8s)
  • Kubernetes: Sistema de "gestión de contenedores".
  • Objetos básicos: "Pod, Service, Volume, Namespace".
  • Campo Metadata: "Campo del objeto Kubernetes donde hay
    que incluir los valores que permiten identificar unívocamente al
    objeto".
  • Protocolos para servicios: Kubernetes puede utilizar "SCTP,
    TCP (por defecto) y UDP".
  • ETCD: "Clase de almacenamiento de datos no volátil, donde se
    almacena toda la información relevante a la configuración del
    clúster de Kubernetes".

                                                         Página | 6
• Kubelet: Responsable del estado de ejecución de cada nodo
  (asegura que los contenedores en el nodo estén saludables).
• Plataformas de contenedores: OpenShift.
• API Server: La puerta de entrada a K8s (todo pasa por aquí).
• Scheduler: El que decide en qué nodo se ejecuta cada Pod.
• Controller Manager: El que se encarga de que el estado actual
  coincida con el deseado (ej. si se cae un Pod, levanta otro).
• Kube-proxy: El que gestiona la red en cada nodo.




• ClusterIP (Por defecto): El servicio solo es accesible desde
  dentro del clúster.
• NodePort: Expone el servicio en un puerto estático de cada
  Nodo. Permite acceso externo básico.
• LoadBalancer: Crea un equilibrador de carga externo (típico
  de entornos cloud como AWS/Azure).




                                                     Página | 7
  • Ingress: Objeto que gestiona el acceso externo a los servicios
    del clúster, proporcionando normalmente balanceo de carga
    HTTP/HTTPS y rutas (ej. mi-app.com/login).
  • ConfigMap y Secret:
       o ConfigMap: Almacena datos de configuración no
          confidenciales (en texto plano).
       o Secret: Almacena datos sensibles (contraseñas, tokens)
          cifrados en base64.


Notas de Enfoque CPS
  • Contenedores: CPS suele preguntar por la identificación
    unívoca de objetos en Kubernetes (Respuesta: metadata) y por
    el mecanismo de persistencia en Docker (Respuesta:
    volúmenes). Es frecuente que pongan nombres de
    herramientas de automatización como Terraform para
    confundir con herramientas de registro de contenedores
    (Terraform es IaC, no registro).
  • Correo: El punto crítico son los puertos seguros. Es vital no
    confundir el puerto seguro de SMTP (465) con el de IMAP (993)
    o POP3 (995). También se debe recordar que SNMP NO es un
    protocolo de correo, sino de gestión de red.
  • Microservicios: Memorice las dos estrategias de gestión:
    Coreografía (descentralizada) y Orquestación (centralizada).
    En los exámenes de 2024, se ha incidido en que los
    microservicios permiten el uso de tecnologías heterogéneas, al
    contrario que los diseños monolíticos.




                                                        Página | 8
