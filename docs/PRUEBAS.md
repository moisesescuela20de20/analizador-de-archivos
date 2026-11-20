# Cómo probar el Analizador de Archivos

Una tabla por función: qué hacer y qué tiene que pasar. Conviene correrlas después de cada cambio, con 2 o 3 archivos chicos, para no gastar cuota.

Para probar en tu PC: `python proxy.py` y abrir `http://localhost:8000`. Para probar la versión publicada: el link de GitHub Pages.

## Función 1 — Recibir varios archivos a la vez

**Anda si:** todos los archivos aparecen, los de más de 32 MB se rechazan sin gastar peticiones y no arranca nada sin API key.

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| 1.1 | Arrastro 3 archivos chicos juntos a la zona punteada. | Aparecen 3 tarjetas; la primera avanza y las otras dicen `En cola`. |
| 1.2 | Hago clic en la zona y elijo 2 archivos con el selector. | Aparecen 2 tarjetas nuevas, debajo de las anteriores. |
| 1.3 | Agrego un archivo de más de 32 MB. | Su tarjeta dice `✖ Supera 32 MB` y el contador `N / 500 hoy` no sube. |
| 1.4 | Borro la API key y agrego un archivo. | Sale el aviso "Primero pegá tu API key" y no se agrega nada. |
| 1.5 | Agrego archivos mientras la cola sigue trabajando. | Se suman al final y la cola los procesa sin empezar otra en paralelo. |

## Función 2 — Mandarlos a la API de VirusTotal

**Anda si:** los archivos nuevos se suben, los conocidos no, nunca hay dos peticiones a menos de 15 segundos y los errores graves frenan la cola.

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| 2.1 | Creo un `.txt` con un texto que nadie más tenga (mi nombre, la fecha y la hora) y lo agrego. | Pasa por `Subiendo…` y `Analizando… (consulta N)`. El enlace del resultado dice "análisis nuevo". |
| 2.2 | Vuelvo a agregar el mismo `.txt` de la prueba 2.1. | No pasa por `Subiendo…`: el enlace dice "informe existente". |
| 2.3 | Abro F12 → pestaña **Red** y agrego 3 archivos. | Entre una petición a `/api/v3` y la siguiente pasan 15 segundos o más. |
| 2.4 | Pego una API key inventada y agrego 2 archivos. | El primero dice `✖ API key inválida` y el segundo `Cancelado`. |
| 2.5 | Cierro la ventana de `proxy.py` y agrego un archivo. | Dice `✖ No hay conexión con proxy.py` y la cola se frena. |
| 2.6 | Abro `index.html` con doble clic, sin el proxy. | Arriba aparece el aviso rojo que explica que hay que usar `http://localhost:8000`. |
| 2.7 | Miro el contador después de las pruebas. | Subió una vez por cada petición, no una vez por archivo. |

## Función 3 — Mostrar el informe

**Anda si:** los números coinciden con la web de VirusTotal y un archivo detectado se distingue a simple vista de uno limpio.

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| 3.1 | Agrego un archivo común y conocido (por ejemplo, un PDF descargado de un sitio oficial). | En verde: `✔ Limpio: 0 detecciones de N motores`. |
| 3.2 | Agrego el archivo de prueba EICAR, descargado de eicar.org. Es inofensivo y existe para probar antivirus; Windows Defender puede borrarlo apenas lo bajo, así que conviene una carpeta excluida o Linux. | En rojo: `⚠ N malicioso…` y debajo la lista de antivirus con el nombre que le dan. |
| 3.3 | Hago clic en "Ver informe completo". | Se abre la página de VirusTotal con la misma huella SHA-256. |
| 3.4 | Comparo los números de la tarjeta con los de esa página. | Coinciden (puede haber una diferencia mínima si VirusTotal lo reanalizó después). |
| 3.5 | Agrego un archivo con símbolos en el nombre, como `<b>hola</b>.txt`. | El nombre se ve tal cual, como texto, sin negritas. |

## Extra — Aviso al terminar

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| E.1 | Agrego un archivo por primera vez. | El navegador pregunta si permito notificaciones; acepto. |
| E.2 | Agrego 2 archivos y me paso a otra pestaña. | Al terminar suena un pitido y aparece "Cola terminada: 2 archivo(s)". |
| E.3 | Dejo la pestaña en segundo plano y controlo el tiempo. | Puede tardar más (Chrome frena los temporizadores), pero nunca va más rápido de lo permitido. |

## Historial — Guardar los informes al recargar

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| H.1 | Analizo 2 archivos y recargo la página (F5). | Las 2 tarjetas siguen, con su resultado y su enlace. |
| H.2 | Cierro el navegador, lo abro de nuevo y entro a la app. | Siguen los informes y la API key. |
| H.3 | Recargo mientras hay archivos en cola. | Los informes terminados siguen; los de la cola desaparecen y hay que agregarlos de nuevo. |
| H.4 | Toco "Borrar historial" y recargo. | La lista queda vacía. |

## Mejora — Cancelar un archivo

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| C.1 | Agrego 3 archivos y cancelo el último mientras dice `En cola`. | Dice `Cancelado`, desaparece su botón y el contador no sube por él. |
| C.2 | Cancelo un archivo mientras dice `Analizando…`. | Dice `Cancelado` y la cola sigue con el siguiente. |
| C.3 | Con F12 → **Red** abierto, repito C.2. | Después de cancelar no aparecen más peticiones de ese archivo. |
| C.4 | Espero a que un archivo termine. | Su botón `Cancelar` desaparece. |

## Calidad — Listo para publicar

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| Q.1 | Abro F12 → **Consola** y analizo un archivo conocido y uno nuevo. | No aparece nada en rojo. |
| Q.2 | Abro la app sin explicarle a nadie qué es. | El título y la línea de abajo dicen para qué sirve. |
| Q.3 | Busco mi API key en `index.html`, `proxy.py` y `worker/worker.js`. | No aparece: la key solo se pega en la página. |

## Versión publicada (GitHub Pages + Cloudflare)

| # | Qué hago | Qué tiene que pasar |
|---|---|---|
| P.1 | Abro el link del Worker solo, sin nada al final. | Dice `No encontrado` (es normal: el puente no tiene pantalla). |
| P.2 | Abro el link del Worker con `/api/v3/files/x` al final. | Aparece un texto con `"error"`: el puente habló con VirusTotal. |
| P.3 | Abro el link de GitHub Pages en la PC, pego la API key y analizo un archivo. | Funciona igual que en `localhost`. |
| P.4 | Repito P.3 en el celular, tocando la zona punteada para elegir el archivo. | Funciona y la pantalla entra sin cortarse. |
