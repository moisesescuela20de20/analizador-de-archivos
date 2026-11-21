# Analizador de Archivos

## Spec

- **Problema:** en la página de VirusTotal hay que subir los archivos de a uno y esperar cada resultado
- **Para quién:** para mí y algún amigo, cuando tengo que revisar varios archivos juntos
- **Funciones mínimas:** recibir varios archivos a la vez, mandarlos en cola a la API de VirusTotal y mostrar el informe de cada uno
- **Extra:** que haga un ruido o mande una notificación al terminar, para dejarla en segundo plano

## Decisiones

### 20/11 · Un HTML más un mini proxy en Python
El navegador no deja que una página llame directo a VirusTotal (CORS). `proxy.py` hace de puente, usa solo la librería estándar de Python y escucha únicamente en mi PC.

### 20/11 · Una Petición cada 15,5 segundos
La API gratuita permite 4 peticiones por minuto y 500 por día. Cuento todas las peticiones (buscar, subir y consultar el estado), no una por archivo.

### 20/11 · Buscar la Huella antes de Subir
Si VirusTotal ya conoce el archivo, uso ese informe. Gasto menos cuota y no comparto archivos sin necesidad.

### 20/11 · Cada uno Pega su Propia API key
La key no va en el código. Así cada amigo tiene sus 500 peticiones por día y no gasta las mías.

### 20/11 · Frenar la cola ante Errores Graves
Si la key es inválida, el proxy está cerrado o se agotó la cuota, cancelo el resto en lugar de seguir gastando peticiones.

### 20/11 · Una sola Lista de Tarjetas
La primera versión tenía dos columnas (en cola y completados). Con una lista donde cada tarjeta cambia de estado alcanza, y queda más simple.

### 20/11 · Dejo la Paleta Oscura Gris y Negra
La elegí en el boceto original. Verde para limpio, rojo para detectado y ámbar para en espera.

### 20/11 · El Extra va Después de la Base
Primero las tres funciones mínimas tienen que pasar las pruebas de la spec; recién después agrego el aviso al terminar (pitido y notificación). Ya está agregado.

### 20/11 · El Proxy Encuentra el HTML aunque tenga otro Nombre
Al descargarlo, el HTML puede quedar con otro nombre (un prefijo o "(1)") y el proxy fallaba con FileNotFoundError. Ahora busca primero `analizador_de_archivos.html`; si no está, usa el primer `.html` de la carpeta, y al arrancar dice cuál está usando. Si no hay ninguno, la página lo explica en vez de dar error.

### 20/11 · Guardo los Informes Terminados
Con localStorage, para que no se borren al recargar la página. Guardo solo los informes, no la cola: el navegador no deja guardar los archivos en sí. Un botón "Borrar historial" los elimina.

### 20/11 · Botón "Cancelar" en cada Archivo
Si el archivo espera en la cola, lo saca y no gasta ninguna petición. Si ya se está analizando, corta la petición en curso y no hace las que faltan. Límite: si lo cancelo justo mientras dice "Subiendo…" y el archivo ya llegó al proxy, VirusTotal lo puede recibir igual; cancelar no "des-sube" nada.

### 20/11 · Consola sin Errores en Rojo
El navegador marcaba en rojo dos cosas que no eran fallas: el pedido de `favicon.ico` y el 404 con el que VirusTotal avisa que no conoce un archivo. Le puse un ícono vacío al HTML, y el proxy ahora manda ese 404 como 200. Los errores reales (key inválida, 429) se siguen viendo.

### 20/11 · Una Línea que Explica para qué Sirve
Debajo del título dice "Analizá varios archivos en VirusTotal de una sola vez", para que se entienda sin explicarlo.

### 20/11 · En el Celular se ve Bien, pero no Funciona Solo
La pantalla se adapta al ancho del celular. Para usarla de verdad hace falta el proxy, que corre en la PC y solo escucha ahí: por seguridad, no la abro a la red.

### 20/11 · Para publicar, el Puente va a Cloudflare Workers
Los servidores gratuitos de páginas solo sirven el HTML, no corren Python. `worker.js` hace lo mismo que `proxy.py`, pero en Cloudflare Workers (gratis: 100.000 peticiones por día, se pega el código en el navegador sin instalar nada). El HTML usa `proxy.py` cuando lo abro en mi PC (localhost) y el Worker cuando está publicado. Así la app anda en el celular.

### 20/11 · Repositorio en GitHub
El HTML pasa a llamarse `index.html` y queda en la raíz del repo, así GitHub Pages lo publica sin configurar nada más. `proxy.py` lo busca con ese nombre; el puente en la nube va en `worker/` y la documentación del proceso en `docs/`.

### 21/11 . Agregar Nuevo Apartado

## Ideas para después

En orden de prioridad (las primeras ahorran cuota o tiempo):

1. Saltear archivos repetidos en la cola (mismo SHA-256): hoy se consultan dos veces.
2. Mostrar el tiempo estimado de la cola (peticiones que faltan × 15 s).
3. Botón "Reintentar" en los archivos que dieron error.
4. Agregar un apartado que indique que clase de virus es o que se puede hacer con ello.
5. Botón "Cancelar todo".
6. Copiar el SHA-256 con un clic.
7. Exportar los informes a CSV para guardarlos o mandarlos.
8. Arrastrar una carpeta entera.
9. Archivos de más de 32 MB (la API lo permite pidiendo antes una dirección especial de subida, que gasta una petición más).
10. Analizar URLs además de archivos.
