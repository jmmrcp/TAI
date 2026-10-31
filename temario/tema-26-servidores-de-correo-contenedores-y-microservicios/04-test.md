# Test — Tema 26: Servidores de correo. Contenedores y microservicios

20 preguntas. Marca la opción correcta (a–d).

## 1. ¿Qué modelo de entrega caracteriza al correo electrónico frente a la mensajería instantánea?
   a) c) Difusión por multicast
   b) b) Almacenamiento y reenvío (store-and-forward)
   c) d) Streaming de datos
   d) a) Entrega en tiempo real directa entre emisor y receptor

## 2. ¿Cuál es el puerto estándar utilizado por el MSA (Mail Submission Agent)?
   a) d) 993
   b) c) 587
   c) a) 25
   d) b) 110

## 3. Según el texto, ¿qué afirmación sobre el MUA es correcta?
   a) b) El MUA solo entrega el mensaje al primer servidor de la cadena (MSA/MTA)
   b) d) El MUA consulta los registros MX del dominio destinatario
   c) c) El MUA es el responsable de depositar el mensaje en el buzón
   d) a) El MUA envía el correo a través de Internet hasta el destino final

## 4. ¿Qué agente es el responsable de depositar el mensaje en el buzón local del usuario?
   a) b) MSA
   b) c) MDA
   c) a) MTA
   d) d) MAA

## 5. Según RFC 5322, ¿cuál es el límite máximo obligatorio (MUST) de caracteres por línea, excluyendo el CRLF?
   a) b) 998 caracteres
   b) c) 1000 caracteres
   c) d) 512 caracteres
   d) a) 78 caracteres

## 6. ¿Qué campos son estrictamente obligatorios en una cabecera RFC 5322 para la validez mínima?
   a) b) Date y From (y Sender bajo condiciones específicas)
   b) d) Message-ID y From
   c) c) To y Date
   d) a) From y Subject

## 7. ¿En qué caso debe incluirse el campo Sender en una cabecera RFC 5322?
   a) c) Cuando el mensaje tiene más de un destinatario
   b) b) Solo si es diferente del From o si el From contiene múltiples direcciones
   c) a) Siempre que exista el campo From
   d) d) Cuando se responde a un mensaje (prefijo Re:)

## 8. Si un dominio tiene varios registros MX, ¿a cuál intentará contactar primero el MTA emisor?
   a) b) Al de menor valor numérico
   b) d) Al que tenga mayor TTL
   c) a) Al de mayor valor numérico
   d) c) Al primero listado en el DNS

## 9. ¿Cómo se realiza el plegado (folding) de un campo de cabecera largo en RFC 5322?
   a) a) Insertando un CRLF seguido de un espacio en blanco (WSP)
   b) c) Truncando la línea a 78 caracteres
   c) b) Insertando dos CRLF consecutivos
   d) d) Codificando el contenido en Base64

## 10. ¿Qué extensiones se utilizan para transmitir imágenes o audio en un mensaje de correo, dado que RFC 5322 solo admite US-ASCII?
   a) c) POP3 e IMAP
   b) d) DNS y MX
   c) a) SMTP y LMTP
   d) b) MIME (RFC 2045, 2046, 2049)

## 11. ¿Cuál es el puerto estándar para la sumisión de correo (submission) desde un cliente (MUA) al servidor (MSA)?
   a) c) 587
   b) b) 110
   c) d) 143
   d) a) 25

## 12. En una sesión SMTP, el servidor responde con código 450. ¿Qué debe hacer el cliente?
   a) d) Reenviar el mismo comando DATA sin cambios
   b) c) Enviar el comando RSET y cerrar la conexión
   c) b) Reintentar más tarde, ya que se trata de un error temporal
   d) a) Abortar definitivamente la transacción (hard bounce)

## 13. ¿Cuáles son los puertos estándar de POP3 y POP3S (SSL implícito)?
   a) d) 110 y 993
   b) b) 143 y 993
   c) a) 110 y 995
   d) c) 25 y 465

## 14. En POP3, ¿en qué estado se produce la eliminación física de los mensajes marcados con DELE?
   a) c) Estado de Actualización
   b) d) Al enviar RETR
   c) b) Estado de Transacción
   d) a) Estado de Autorización

## 15. ¿Cuáles son los puertos estándar de IMAP e IMAPS (SSL implícito)?
   a) a) 110 y 995
   b) b) 143 y 993
   c) d) 143 y 995
   d) c) 25 y 587

## 16. En IMAP, ¿qué flag indica que un mensaje ha sido leído?
   a) d) \Recent
   b) a) \Answered
   c) c) \Seen
   d) b) \Flagged

## 17. ¿Qué protocolo permite gestionar carpetas (buzones) jerárquicos directamente en el servidor de correo?
   a) b) SMTP
   b) d) Ninguno de los anteriores
   c) c) IMAP
   d) a) POP3

## 18. ¿Con qué secuencia de comandos finaliza el envío del contenido del mensaje en una transacción SMTP?
   a) b) Enviando una línea que contiene únicamente un punto (<CRLF>.<CRLF>)
   b) d) Enviando NOOP
   c) a) Enviando QUIT
   d) c) Enviando RSET

## 19. ¿Qué extensión permite autenticar al cliente ante el servidor SMTP para evitar Open Relays y Email Spoofing?
   a) d) IDLE (RFC 2177)
   b) c) MIME
   c) b) SMTP-AUTH (RFC 4954)
   d) a) STARTTLS (RFC 3207)

## 20. Ante un usuario que necesita acceder al correo desde PC de oficina, portátil y móvil con sincronización de estado, ¿qué protocolo es el adecuado?
   a) a) POP3
   b) b) SMTP
   c) c) IMAP
   d) d) POP3 en modo Keep

---
## Plantilla de respuestas

1. b) b) Almacenamiento y reenvío (store-and-forward)  — El correo electrónico se basa en un modelo de almacenamiento y reenvío, donde los mensajes se depositan en servidores intermedios hasta que el receptor decide acceder a ellos.
2. b) c) 587  — El MSA utiliza SMTP en el puerto estándar 587; históricamente se usaba el 25, pero actualmente el 25 se reserva preferentemente para la comunicación MTA-a-MTA.
3. a) b) El MUA solo entrega el mensaje al primer servidor de la cadena (MSA/MTA)  — El MUA no envía el correo a través de Internet hasta el destino final; solo lo entrega al primer servidor de la cadena (el MSA/MTA).
4. b) c) MDA  — El MDA (Mail Delivery Agent) es el responsable de la entrega final: recibe el mensaje del MTA y lo deposita en el buzón local (Message Store).
5. a) b) 998 caracteres  — Ninguna línea puede exceder los 998 caracteres (excluyendo el CRLF) como límite obligatorio; la recomendación de interoperabilidad es de 78 caracteres.
6. a) b) Date y From (y Sender bajo condiciones específicas)  — Los campos estrictamente obligatorios son Date y From (y Sender bajo condiciones específicas). Subject y Message-ID son recomendados pero no obligatorios.
7. b) b) Solo si es diferente del From o si el From contiene múltiples direcciones  — Sender es obligatorio si el From contiene múltiples direcciones o si el transmisor difiere del autor; si es idéntico al From no debe usarse.
8. a) b) Al de menor valor numérico  — El MTA emisor intentará contactar primero con el registro MX de menor valor numérico, que corresponde a mayor prioridad.
9. a) a) Insertando un CRLF seguido de un espacio en blanco (WSP)  — Los campos de cabecera largos pueden dividirse en múltiples líneas insertando un CRLF seguido de un espacio en blanco (WSP).
10. d) b) MIME (RFC 2045, 2046, 2049)  — Para superar la limitación de texto US-ASCII se utilizan las extensiones MIME (RFC 2045, 2046, 2049), que estructuran los mensajes para ajustarse a la sintaxis del RFC 5322.
11. a) c) 587  — El puerto 587 es el estándar para la sumisión de correo (Submission) desde clientes como Outlook o Thunderbird, requiriendo habitualmente autenticación. El 25 se usa entre MTA, el 110 es POP3 y el 143 es IMAP.
12. c) b) Reintentar más tarde, ya que se trata de un error temporal  — Los códigos 4xx indican error temporal; el cliente debería reintentar más tarde (soft bounce). Es la base del Greylisting. Los 5xx son errores permanentes que no deben reintentarse.
13. c) a) 110 y 995  — POP3 estándar usa el puerto 110 TCP (texto claro/STARTTLS) y POP3S (SSL implícito) usa el 995 TCP. Los pares 143/993 corresponden a IMAP/IMAPS.
14. a) c) Estado de Actualización  — El estado de Actualización se inicia al enviar QUIT; entonces el servidor elimina físicamente todos los mensajes marcados para borrado durante la transacción. En el estado de Transacción solo se marcan para eliminación.
15. b) b) 143 y 993  — IMAP estándar usa el puerto 143 TCP (escalable con STARTTLS) e IMAPS (SSL implícito) usa el 993 TCP. Los pares 110/995 corresponden a POP3/POP3S.
16. c) c) \Seen  — El flag \Seen indica que el mensaje ha sido leído. \Answered indica contestado, \Flagged marcado/urgente y \Recent recién llegado. Los flags se almacenan en el servidor, permitiendo sincronización entre dispositivos.
17. c) c) IMAP  — IMAP permite crear, renombrar y borrar buzones (carpetas) jerárquicos en el servidor. POP3 solo gestiona un único buzón (INBOX); cualquier organización en carpetas es local del cliente.
18. a) b) Enviando una línea que contiene únicamente un punto (<CRLF>.<CRLF>)  — Tras el comando DATA, el cliente indica el fin del mensaje enviando una línea que contiene únicamente un punto (<CRLF>.<CRLF>). QUIT cierra la sesión, RSET aborta la transacción y NOOP mantiene la sesión activa.
19. c) b) SMTP-AUTH (RFC 4954)  — SMTP-AUTH (RFC 4954) utiliza SASL para autenticar al cliente ante el servidor, solucionando la falta de autenticación original de SMTP. STARTTLS cifra la conexión, MIME codifica datos no ASCII e IDLE es extensión de IMAP.
20. c) c) IMAP  — IMAP está diseñado para mantener los mensajes en el servidor y sincronizar estado (leído/no leído, carpetas) entre múltiples dispositivos. POP3 carece de sincronización de estado entre dispositivos.
