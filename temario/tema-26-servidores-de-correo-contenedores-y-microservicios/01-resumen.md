# Resumen — Tema 26: Servidores de correo. Contenedores y microservicios

## Elevator pitch (5 líneas)

Tema técnico del Bloque IV que abarca dos grandes áreas: (1) administración de
servidores de correo electrónico (protocolos SMTP/POP3/IMAP, puertos, seguridad
SPF/DKIM/DMARC, almacenamiento mbox/maildir, Postfix/Exchange) y (2)
contenedores y microservicios (Docker, LXC, Kubernetes, arquitecturas de
microservicios, orquestación). El tribunal insiste en puertos seguros, diferencia
operativa POP3 vs IMAP, y objetos básicos de Kubernetes (Pod, Service, etc.).

## Resumen (1 página)

**Correo electrónico.** Modelo asíncrono de almacenamiento y reenvío
(store-and-forward). Protocolos: SMTP (envío, cliente→servidor y
servidor→servidor, comandos EHLO/HELO/MAIL/RCPT/DATA…, códigos 250/421/550/554),
POP3 (descarga al cliente, borra del servidor, comando STAT, puerto 110/995 TLS)
e IMAP (mantiene en servidor, visualización sin descarga, puerto 143/993 TLS).
Agentes: MUA (cliente), MTA (envío/recepción, Postfix/Sendmail), MDA (depósito
en buzón). Formatos de buzón: mbox (un fichero) y maildir (un fichero por
mensaje). Exchange ActiveSync (sync móvil vía HTTP/XML), X.400 (estándar inicial).

**Puertos clave (memorizar):** SMTP 25 / 465 TLS; POP3 110 / 995 TLS; IMAP 143
/ 993 TLS; qmtp 209.

**Seguridad:** SPF (servidores SMTP autorizados vía DNS), DKIM (firma digital de
cabeceras), DMARC (política si fallan SPF/DKIM), S/MIME, PGP, STARTTLS (upgrade
inseguro→seguro en mismo puerto), Open Relay (vulnerabilidad crítica), RBL
(listas negras en tiempo real), antispam. Servidor de correo corporativo en DMZ
(CCN-CERT). DAG en Exchange 2013 (bases activa/pasiva).

**Contenedores.** Docker: creación fácil de contenedores; persistencia preferida
mediante Volúmenes; imágenes de solo lectura compuestas por capas + capa
R/W al ejecutar; Dockerfile con instrucciones; comandos docker ps/info;
redes bridge (por defecto, red virtual interna) y host (comparte pila de red).
CMD (argumentos por defecto, sobrescribibles) vs ENTRYPOINT (ejecutable
principal). LXC (virtualización a nivel de SO), Containerd, Podman. OCI.

**Microservicios.** Funcionalidades por composición de microservicios; estrategias
Coreografía (descentralizada) y Orquestación (centralizada); beneficios:
escalado flexible, CI/CD, resistencia a errores. Patrón Sidecar (contenedor
secundario en mismo Pod, comparte ciclo de vida y red).

**Kubernetes (K8s).** Sistema de gestión de contenedores. Objetos básicos: Pod,
Service, Volume, Namespace. Metadata identifica unívocamente al objeto.
Protocolos de servicio: SCTP, TCP (por defecto), UDP. ETCD (almacenamiento no
volátil de configuración del clúster). Componentes: Kubelet (estado de
ejecución por nodo), API Server (puerta de entrada), Scheduler (asignación de
Pod a nodo), Controller Manager (estado deseado), Kube-proxy (red por nodo).
Servicios: ClusterIP (por defecto, solo interno), NodePort (puerto estático en
cada nodo, acceso externo básico), LoadBalancer (equilibrador externo), Ingress
(acceso externo HTTP/HTTPS con rutas). ConfigMap (config no confidencial en
texto plano) y Secret (datos sensibles, base64). Plataformas: OpenShift.

**Trampas del tribunal:** Outlook no es protocolo (es cliente/MUA); SNMP no es
protocolo de correo (gestión de red); Terraform es IaC, no registro de
contenedores; puertos seguros 465/995/993 no confundir.

## Detallado

### 1. Correo electrónico — protocolos

- **SMTP** (Simple Mail Transfer Protocol): protocolo de envío. Se usa desde el
  cliente al servidor de origen y entre servidores. Gestiona el correo saliente.
  Comandos mínimos para receptores: EHLO, HELO, MAIL, RCPT, DATA, RSET, NOOP,
  QUIT, VRFY. Indicar destinatario: `rcpt to`. Códigos clave: 250 (OK), 421
  (servicio no disponible, canal se cierra), 550 (buzón no existe/no
  disponible), 554 (transacción fallida).
- **POP3** (v3): acceso al correo; descarga mensajes al cliente y los borra del
  buzón central. Comando STAT. Puertos 110 / 995 (TLS).
- **IMAP**: acceso al correo; mensajes permanecen en el buzón central (visualizar
  sin descargar, borrar/mover/responder). Puertos 143 / 993 (TLS).
- **X.400**: estándar inicial para intercambio de mensajes entre hosts TCP/IP.
- **Exchange ActiveSync**: sincronización basada en HTTP y XML para dispositivos
  móviles contra Microsoft Exchange (emails, calendario…).
- **MUA/MTA/MDA**: cliente / servidor de transferencia (usa SMTP) / agente de
  entrega en buzón.
- **qmtp** (Quick Mail Transfer Protocol): puerto 209.

### 2. Puertos (tabla)

| Protocolo | Puerto estándar | Puerto seguro (TLS/SSL) |
|-----------|-----------------|-------------------------|
| SMTP      | 25              | 465                     |
| POP3      | 110             | 995                     |
| IMAP      | 143             | 993                     |

### 3. Seguridad y protección del correo

- **SPF**: identifica servidores SMTP autorizados vía registros DNS.
- **DKIM**: firma digital en cabeceras para verificar integridad.
- **DMARC**: política ante fallo de SPF/DKIM (rechazar o marcar spam).
- **S/MIME**: envío de correo seguro.
- **PGP**: cifrado asimétrico para confidencialidad.
- **STARTTLS**: upgrade de conexión insegura a segura en el mismo puerto.
- **Open Relay**: servidor que reenvía sin autenticación (vulnerabilidad crítica
  de spam).
- **RBL**: listas negras en tiempo real.
- **Antispam**: filtro por umbral.
- Soluciones corporativas: Sophos, IronPort.
- Ubicación del servidor de correo corporativo: DMZ (CCN-CERT).
- **DAG** (Database Availability Group) en Exchange 2013: bases activa/pasiva.

### 4. Administración y almacenamiento

- Servidores habituales: Postfix (Linux), Microsoft Exchange.
- Formatos de buzón: **mbox** (un único fichero) y **maildir** (un fichero por
  mensaje).
- Configuración Postfix: editar `/etc/postfix/main.cf` para cambiar el mensaje
  HELO.
- Exchange ActiveSync (ver arriba).

### 5. Microservicios

- Definición: funcionalidades implementadas mediante composición de
  microservicios.
- Estrategias: **Coreografía** (descentralizada) y **Orquestación** (centralizada).
- Beneficios: escalado flexible, CI/CD, resistencia a errores (degradación sin
  bloquear toda la app), tecnologías heterogéneas (frente a monolitos).
- Patrón **Sidecar**: contenedor secundario junto al principal en el mismo Pod;
  comparte ciclo de vida y red (logs, proxies, seguridad).

### 6. Contenedores (Docker)

- Docker: creación fácil de contenedores para ejecución de aplicaciones.
- Persistencia: mecanismo preferido = **Volúmenes**.
- Imágenes: solo lectura, compuestas por **capas (layers)**; al ejecutar un
  contenedor se añade una fina capa R/W superior.
- Dockerfile: fichero de texto con instrucciones para crear la imagen.
- Comandos: `docker ps` (lista contenedores en ejecución), `docker info`
  (info del sistema Docker).
- Redes: **bridge** (por defecto, red virtual interna) y **host** (comparte pila
  de red con el host).
- CMD vs ENTRYPOINT: CMD proporciona argumentos por defecto sobrescribibles;
  ENTRYPOINT es el ejecutable principal que siempre se ejecuta.
- LXC (Linux Containers): virtualización a nivel de SO para Linux.
- Otras: Containerd, Podman. OCI (Open Container Initiative).

### 7. Kubernetes (K8s)

- Sistema de gestión de contenedores.
- Objetos básicos: Pod, Service, Volume, Namespace.
- **Metadata**: campo donde se incluyen los valores que identifican unívocamente
  al objeto.
- Protocolos para servicios: SCTP, TCP (por defecto), UDP.
- **ETCD**: almacenamiento no volátil donde se guarda toda la configuración del
  clúster.
- Componentes: Kubelet (estado de ejecución por nodo), API Server (puerta de
  entrada), Scheduler (asignación de Pod a nodo), Controller Manager (estado
  deseado), Kube-proxy (red por nodo).
- Servicios: ClusterIP (por defecto, solo interno), NodePort (puerto estático
  en cada nodo, acceso externo básico), LoadBalancer (equilibrador externo en
  cloud), Ingress (acceso externo HTTP/HTTPS con rutas).
- ConfigMap (config no confidencial, texto plano) y Secret (datos sensibles,
  base64).
- Plataformas: OpenShift.

### 8. Notas de enfoque CPS (trampas)

- Puertos seguros: 465 (SMTP), 995 (POP3), 993 (IMAP) — no confundir.
- Outlook es cliente (MUA), no protocolo.
- SNMP es gestión de red, no protocolo de correo.
- Terraform es IaC, no registro de contenedores.
- Metadata identifica unívocamente objetos en K8s; persistencia en Docker =
  Volúmenes.
- Microservicios: Coreografía (descentralizada) y Orquestación (centralizada);
  permiten tecnologías heterogéneas (frente a monolitos).
- En 2024 se incidió en tecnologías heterogéneas vs monolíticos.
file_path">
/root/oposicion/temario/tema-26-servidores-de-correo-contenedores-y-microservicios/01-resumen.md