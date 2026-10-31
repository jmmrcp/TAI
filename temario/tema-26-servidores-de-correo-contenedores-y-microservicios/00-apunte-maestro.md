# Apunte maestro — Tema 26: Servidores de correo. Contenedores y microservicios

> Generado a partir de `00-texto-normalizado-2.md` (resumen CPS) y `02-conceptos-clave.json`.
> Las anotaciones `[VERIFICAR]` marcan datos no contrastados con fuente oficial (BOE/manual).

## 1. Correo electrónico — protocolos

### SMTP
- Protocolo de envío. Se usa desde el cliente al servidor de origen y entre servidores.
- Gestiona el correo saliente.
- Comandos mínimos para receptores: EHLO, HELO, MAIL, RCPT, DATA, RSET, NOOP, QUIT, VRFY.
- Indicar destinatario: `rcpt to`.
- Códigos clave: 250 (OK), 421 (servicio no disponible), 550 (buzón no existe/no disponible), 554 (transacción fallida).

### POP3
- Protocolo de acceso al correo. Descarga mensajes al cliente y los borra del buzón central.
- Comando: STAT. Puertos 110 / 995 (TLS).

### IMAP
- Protocolo de acceso al correo. Mensajes permanecen en el buzón central; visualización sin descarga.
- Puertos 143 / 993 (TLS).

### X.400
- Estándar inicial para intercambio de mensajes entre hosts TCP/IP.

### Exchange ActiveSync
- Sincronización basada en HTTP y XML para dispositivos móviles contra Microsoft Exchange.

### Agentes
- MUA (Mail User Agent): cliente de correo (Outlook, Thunderbird). No es protocolo.
- MTA (Mail Transfer Agent): servidor que envía/recibe; usa SMTP (Postfix, Sendmail).
- MDA (Mail Delivery Agent): deposita el correo en el buzón del usuario.

### qmtp
- Quick Mail Transfer Protocol: puerto 209.

## 2. Puertos

| Protocolo | Puerto estándar | Puerto seguro (TLS/SSL) |
|-----------|-----------------|-------------------------|
| SMTP      | 25              | 465                     |
| POP3      | 110             | 995                     |
| IMAP      | 143             | 993                     |

## 3. Seguridad y protección del correo

- SPF: servidores SMTP autorizados vía DNS.
- DKIM: firma digital en cabeceras.
- DMARC: política ante fallo de SPF/DKIM.
- S/MIME: envío de correo seguro.
- PGP: cifrado asimétrico.
- STARTTLS: upgrade inseguro→seguro en mismo puerto.
- Open Relay: vulnerabilidad crítica (reenvío sin autenticación).
- RBL: listas negras en tiempo real.
- Antispam: filtro por umbral.
- Soluciones corporativas: Sophos, IronPort.
- Servidor de correo corporativo en DMZ (CCN-CERT).
- DAG (Database Availability Group) en Exchange 2013: bases activa/pasiva.

## 4. Administración y almacenamiento

- Servidores habituales: Postfix (Linux), Microsoft Exchange.
- Formatos de buzón: mbox (un único fichero) y maildir (un fichero por mensaje).
- Configuración Postfix: editar `/etc/postfix/main.cf` para cambiar el mensaje HELO.

## 5. Microservicios

- Funcionalidades por composición de microservicios.
- Estrategias: Coreografía (descentralizada, por eventos) y Orquestación (centralizada, con orquestador).
- Beneficios: escalado flexible, CI/CD, resistencia a errores, tecnologías heterogéneas (frente a monolitos).
- Patrón Sidecar: contenedor secundario junto al principal en el mismo Pod; comparte ciclo de vida y red.

## 6. Contenedores (Docker)

- Creación fácil de contenedores para ejecución de aplicaciones.
- Persistencia preferida: Volúmenes.
- Imágenes: solo lectura, compuestas por capas; al ejecutar se añade capa R/W superior.
- Dockerfile: fichero de texto con instrucciones para crear la imagen.
- Comandos: `docker ps`, `docker info`.
- Redes: bridge (por defecto, red virtual interna) y host (comparte pila de red con el host).
- CMD vs ENTRYPOINT: CMD argumentos por defecto sobrescribibles; ENTRYPOINT ejecutable principal.
- LXC (Linux Containers): virtualización a nivel de SO.
- Otras: Containerd, Podman. OCI (Open Container Initiative).

## 7. Kubernetes (K8s)

- Sistema de gestión de contenedores.
- Objetos básicos: Pod, Service, Volume, Namespace.
- Metadata: identifica unívocamente al objeto.
- Protocolos para servicios: SCTP, TCP (por defecto), UDP.
- ETCD: almacenamiento no volátil de toda la configuración del clúster.
- Componentes: Kubelet, API Server, Scheduler, Controller Manager, Kube-proxy.
- Servicios: ClusterIP (por defecto, solo interno), NodePort, LoadBalancer, Ingress.
- ConfigMap (config no confidencial, texto plano) y Secret (datos sensibles, base64).
- Plataformas: OpenShift.

## 8. Notas de enfoque CPS (trampas del tribunal)

- Puertos seguros: 465 (SMTP), 995 (POP3), 993 (IMAP) — no confundir.
- Outlook es cliente (MUA), no protocolo.
- SNMP es gestión de red, no protocolo de correo.
- Terraform es IaC, no registro de contenedores.
- Metadata identifica unívocamente objetos en K8s; persistencia en Docker = Volúmenes.
- Microservicios: Coreografía (descentralizada) y Orquestación (centralizada); permiten tecnologías heterogéneas.
file_path">
/root/oposicion/temario/tema-26-servidores-de-correo-contenedores-y-microservicios/00-apunte-maestro.md