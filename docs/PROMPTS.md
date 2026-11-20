# Prompts — Analizador de Archivos

Todos los prompts del proyecto, en el orden en que se usan.

## Paso 2 · Pedir la base (estructura de Brockman, versión completa)

```
## Objetivo
Quiero construir "Analizador de Archivos", una app web simple para analizar varios archivos en VirusTotal sin tener que subirlos de a uno desde la página.

Funciones mínimas (solo estas, nada más por ahora):
1. Recibir varios archivos a la vez, arrastrándolos o con un selector. Cada archivo aparece como una tarjeta y entra a una cola en orden. Rechazar los de más de 32 MB sin gastar peticiones.
2. Mandarlos a la API v3 de VirusTotal en cola: primero calcular el SHA-256 local y buscar con GET /files/{hash}. Si devuelve 404, subir con POST /files y consultar GET /analyses/{id} hasta que el estado sea "completed".
3. Mostrar el informe de cada archivo: cuántos motores lo detectan, cuáles y con qué nombre, y un enlace a https://www.virustotal.com/gui/file/{hash}.

## Formato de respuesta
- Dos archivos: un HTML (interfaz y lógica, con CSS y JS vanilla en el mismo archivo) y proxy.py (Python, solo librería estándar), que sirve el HTML y reenvía /api/v3/... a VirusTotal.
- Código comentado de forma sencilla, en español, para que lo pueda estudiar.
- Nada que no sea necesario: sin frameworks, sin librerías externas, sin estilos de más.
- Al final, explicame en pocos pasos cómo lo ejecuto en Windows 11 y una lista de lo que tuviste que suponer.

## Advertencias
- No simules nada: nada de Math.random(), estados falsos de "API conectada" ni cuotas inventadas. Todo dato que se muestre tiene que venir de la API.
- La API pública permite 4 peticiones por minuto y 500 por día. Todas las llamadas (buscar, subir y consultar) tienen que pasar por una sola función que espere al menos 15,5 segundos entre una y otra. Si llega un 429, esperar 60 segundos y reintentar, como máximo 3 veces.
- Si la key es inválida (401), no hay conexión con el proxy o se agotó la cuota, frenar la cola y marcar el resto como cancelado.
- El navegador bloquea por CORS las llamadas directas a VirusTotal; por eso existe proxy.py. No me digas que lo llame directo desde el HTML.
- El proxy escucha solo en 127.0.0.1.
- No inventes endpoints ni campos de la API. Usá data.attributes.last_analysis_stats y last_analysis_results para un archivo conocido, y data.attributes.status, stats y results para un análisis. Si no estás seguro de algo, decímelo en vez de adivinar.
- Los nombres de archivo se muestran con textContent, nunca con innerHTML (para evitar inyección de HTML).
- La API key la pega el usuario en un campo y se guarda en localStorage; no la escribas en el código.

## Contexto
Es un proyecto personal para el curso de desarrollo de apps con IA de Puerta 18. Lo voy a usar yo y algún amigo, cada uno con su propia API key gratuita. Desarrollo en Windows 11. La app es una sola pantalla así:

┌────────────────────────────────────────────────┐
│ Analizador de Archivos                         │
├────────────────────────────────────────────────┤
│ [ API key de VirusTotal  •••••••• ]  12/500 hoy│
├────────────────────────────────────────────────┤
│ ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐ │
│   Arrastrá tus archivos acá o hacé clic        │
│   Máx. 32 MB · No subas archivos privados      │
│ └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘ │
├────────────────────────────────────────────────┤
│ factura.pdf                          0.30 MB   │
│ ✔ Limpio: 0 detecciones de 65 motores (verde)  │
│ Ver informe completo                           │
├────────────────────────────────────────────────┤
│ instalador.exe                      12.40 MB   │
│ ⚠ 3 malicioso / 1 sospechoso de 70   (rojo)    │
│ Kaspersky: Trojan.X · ESET: Gen.Y              │
├────────────────────────────────────────────────┤
│ fotos.zip                            8.10 MB   │
│ Analizando… (consulta 2)            (ámbar)    │
├────────────────────────────────────────────────┤
│ notas.txt                            0.01 MB   │
│ En cola                             (ámbar)    │
└────────────────────────────────────────────────┘
```

## Paso 2 · Pedir la base (plantilla del curso: solo la pantalla)

```
Objetivo:
Quiero hacer una app llamada Analizador de Archivos para no tener que subir los archivos de a uno a la página de VirusTotal y esperar cada resultado.
Más adelante va a tener 3 funciones: recibir varios archivos a la vez, mandarlos en cola a la API de VirusTotal y mostrar el informe de cada archivo.
Por ahora hacé solo la base: la pantalla principal con su estructura y su estilo,
sin que las funciones anden todavía.

Formato de respuesta:
Un solo archivo HTML con el CSS y el JavaScript adentro.
Después de cada cambio, respondé siempre así:
Qué cambié: (en una línea)
Dónde está en el código: (HTML, CSS o JavaScript)
Cómo lo pruebo: (qué tengo que tocar o mirar)

Advertencias:
No agregues funciones que no te pedí.
No uses librerías ni links a imágenes que no existan.
Si algo de lo que pido no está claro, preguntame antes de decidirlo por tu cuenta.

Contexto:
Es para mí y algún amigo; la vamos a usar en la computadora cuando tengamos que revisar varios archivos juntos.
Estoy aprendiendo HTML, CSS y JavaScript, así que prefiero código simple que pueda leer.
La pantalla es una sola columna centrada, con estilo oscuro en gris y negro:
- Arriba: el título "Analizador de Archivos" y debajo un campo para pegar la API key de VirusTotal, con un contador a la derecha que dice "0 / 500 hoy".
- En el medio: una zona con borde punteado que dice "Arrastrá tus archivos acá o hacé clic", y abajo en letra chica "Máx. 32 MB · No subas archivos privados".
- Abajo: la lista de archivos, una tarjeta por archivo con el nombre y el tamaño a la izquierda y el estado debajo. Para ver cómo queda, poné 3 tarjetas de ejemplo: una "En cola" en ámbar, una "✔ Limpio: 0 detecciones de 65 motores" en verde y una "⚠ 3 malicioso / 1 sospechoso de 70 motores" en rojo.
```

## Paso 3 · Agregar las funciones (de a una, en orden)

### Función 1

```
Agregá la función 1: cuando arrastro uno o varios archivos a la zona punteada, o hago clic y los elijo, cada archivo aparece como una tarjeta en la lista con su nombre, su tamaño y el estado "En cola" en ámbar. Si un archivo pesa más de 32 MB, su tarjeta dice "✖ Supera 32 MB" en rojo. Si el campo de la API key está vacío, aparece el aviso "Primero pegá tu API key" y no se agrega nada. Sacá las 3 tarjetas de ejemplo.
No cambies nada más del código.
```

### Función 2

```
Agregá la función 2: cuando hay archivos "En cola", se mandan de a uno a la API v3 de VirusTotal. Primero se calcula el SHA-256 y se busca con GET /files/{hash}; si da 404, se sube con POST /files y se consulta GET /analyses/{id} hasta que el estado sea "completed". La tarjeta va mostrando cada paso ("Buscando informe…", "Subiendo…", "Analizando… (consulta N)"). Todas las peticiones pasan por una sola función que espera 15,5 segundos entre una y otra, y el contador "N / 500 hoy" sube con cada petición. Si llega un 429, espera 60 segundos y reintenta, como máximo 3 veces. Si la key es inválida o no hay conexión, la tarjeta muestra el error en rojo y el resto queda "Cancelado". No muestres el resultado todavía: cuando termina, la tarjeta solo dice "Listo".
Como el navegador bloquea las llamadas directas a VirusTotal (CORS), creá también un proxy.py con la librería estándar de Python que sirva el HTML en http://localhost:8000 y reenvíe /api/v3/... a https://www.virustotal.com/api/v3/..., escuchando solo en 127.0.0.1.
No cambies nada más del código.
```

### Función 3

```
Agregá la función 3: cuando un archivo termina de analizarse, en lugar de "Listo" su tarjeta muestra "✔ Limpio: 0 detecciones de N motores" en verde, o "⚠ X malicioso / Y sospechoso de N motores" en rojo con la lista de motores que lo detectaron y el nombre que le dan. Debajo va un enlace "Ver informe completo" a https://www.virustotal.com/gui/file/{hash}. Usá last_analysis_stats y last_analysis_results si el archivo ya existía, o stats y results si se analizó recién. Los nombres de archivo y de motores se muestran con textContent, no con innerHTML.
No cambies nada más del código.
```

### Extra

```
Agregá el extra: cuando se vacía la cola, suena un pitido corto y aparece una notificación del sistema que dice "Cola terminada: N archivo(s)". El permiso para las notificaciones se pide la primera vez que agrego un archivo.
No cambies nada más del código.
```

## Paso 4 · Guardar datos con localStorage

### API key y contador (si la IA no los guardó antes)

```
Quiero que mi app guarde la API key y el contador de peticiones del día (que se reinicie a las 21:00 hora argentina, cuando VirusTotal renueva la cuota) para que no se borre al recargar. Usá localStorage. No cambies nada más del código y explicame en 3 líneas qué agregaste.
```

### Historial de informes (ya hecho)

```
Quiero que mi app guarde los informes de los archivos ya analizados (nombre, tamaño, resultado con sus detecciones y el enlace a VirusTotal) para que no se borre al recargar. Usá localStorage. Al abrir la página, mostrá esos informes en la lista como tarjetas terminadas, y agregá un botón "Borrar historial" que los elimine. No cambies nada más del código y explicame en 3 líneas qué agregaste.
```

## Paso 5 · Mejoras

### Cancelar un archivo (ya hecho)

```
Agregá un botón "Cancelar" en cada tarjeta: cuando lo toco en un archivo que espera en la cola, sale de la cola sin gastar peticiones y su tarjeta dice "Cancelado"; cuando lo toco en un archivo que se está analizando, se corta la petición en curso (con AbortController) y no se hacen las que faltan. El botón desaparece cuando el archivo termina, da error o se cancela.
No cambies nada más del código.
```

### Saltear archivos repetidos (siguiente idea)

```
Agregá esto: cuando agrego a la cola un archivo con el mismo SHA-256 que otro que ya está en la cola o ya se analizó en esta sesión, no se consulta de nuevo y su tarjeta muestra el mismo informe con la aclaración "(repetido)".
No cambies nada más del código.
```
