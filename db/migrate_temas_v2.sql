-- ============================================================
-- Migración: estructura antigua (8+6+10+9) → nueva (9+5+9+10)
-- Preserva temas con estado_ingesta = 'completo'
-- ============================================================

BEGIN TRANSACTION;

-- 1. Borrar temas pendientes (los completos se preservan)
DELETE FROM temas WHERE estado_ingesta = 'pendiente';

-- 2. Borrar temas que ya no existen en la nueva estructura
--    (solo si no tienen datos: preguntas, flashcards, cuadros, srs)
DELETE FROM temas
WHERE id NOT IN (
    'tema-01-la-constitucion-espanola-de-1978',
    'tema-02-la-corona-las-cortes-generales',
    'tema-03-el-gobierno-y-la-administracion-el-poder-judicial',
    'tema-04-la-organizacion-territorial-del-estado-la-union-europea',
    'tema-05-el-estatuto-basico-del-empleado-publico',
    'tema-06-la-ley-39-2015-del-procedimiento-administrativo-comun',
    'tema-07-la-ley-40-2015-de-regimen-juridico-del-sector-publico',
    'tema-08-la-ley-19-2013-de-transparencia-y-buen-gobierno',
    'tema-09-proteccion-de-datos-igualdad-discapacidad-violencia-de-genero',
    'tema-10-hardware-y-software-sistemas-operativos',
    'tema-11-redes-de-area-local-internet',
    'tema-12-seguridad-informatica',
    'tema-13-ofimatica-herramientas-de-productividad',
    'tema-14-administracion-electronica-servicios-digitales',
    'tema-15-modelado-de-datos-diseno-de-bases-de-datos',
    'tema-16-bases-de-datos-relacionales-sql',
    'tema-17-bases-de-datos-nosql-big-data',
    'tema-18-metodologias-de-desarrollo-ciclo-de-vida-del-software',
    'tema-19-lenguajes-de-programacion-java-y-net',
    'tema-20-desarrollo-web-html-css-javascript',
    'tema-21-servicios-web-apis-rest-microservicios',
    'tema-22-pruebas-de-software-calidad-y-accesibilidad',
    'tema-23-seguridad-en-aplicaciones-owasp',
    'tema-24-redes-de-comunicaciones-modelo-osi-y-tcp-ip',
    'tema-25-direccionamiento-ip-subnetting',
    'tema-26-protocolos-de-aplicacion-dns-dhcp-http',
    'tema-27-sistemas-operativos-linux',
    'tema-28-sistemas-operativos-windows-server-active-directory',
    'tema-29-virtualizacion-y-contenedores-docker-y-kubernetes',
    'tema-30-almacenamiento-raid-backup',
    'tema-31-centros-de-procesamiento-de-datos-cpd',
    'tema-32-cloud-computing',
    'tema-33-seguridad-en-redes-ens-ccn-cert'
);

COMMIT;
