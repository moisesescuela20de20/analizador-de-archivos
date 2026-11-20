# Cómo publicar el Analizador de Archivos

La app tiene dos partes y las dos tienen que estar en internet:

1. **El puente** (`worker/worker.js`): habla con VirusTotal. Va a Cloudflare Workers, que es gratis.
2. **La página** (`index.html`): va a GitHub Pages o adonde publique el curso.

Primero el puente, porque la página necesita su link.

## 1. Publicar el puente en Cloudflare (unos 5 minutos)

Los nombres de los botones pueden cambiar un poco con el tiempo.

1. Entrá a **dash.cloudflare.com** y creá una cuenta gratis.
2. En el menú, entrá a **Workers & Pages** (puede aparecer dentro de **Compute**) → **Create** → **Create Worker** (empezando por "Hello World").
3. Ponele de nombre `analizador-puente` y tocá **Deploy**.
4. Tocá **Edit code**, borrá todo, pegá el contenido de `worker/worker.js` y tocá **Deploy** otra vez.
5. Copiá el link del Worker. Tiene esta forma: `https://analizador-puente.TU-USUARIO.workers.dev`
6. **Probá que anda:** abrí ese link agregándole `/api/v3/files/x` al final. Tiene que aparecer un texto con `"error"`. Es normal, porque no mandaste API key, y significa que el puente responde.

## 2. Conectar la página con el puente

1. Abrí `index.html` con un editor de texto.
2. Buscá esta línea:
   ```
   const PUENTE_PUBLICADO = 'https://TU-WORKER.workers.dev';
   ```
3. Reemplazá el link por el de tu Worker, **sin barra al final**, y guardá.
4. Subí el cambio al repo:
   ```
   git add index.html
   git commit -m "Conectar con el puente de Cloudflare"
   git push
   ```

En tu PC sigue usando `proxy.py` (cuando la abrís en `localhost`); el Worker se usa solo cuando está publicada. El link del Worker no es secreto: puede quedar en el repo público.

## 3. Publicar la página con GitHub Pages

1. En tu repo de GitHub, entrá a **Settings** → **Pages**.
2. En **Source** elegí **Deploy from a branch**, rama `main`, carpeta `/ (root)`, y tocá **Save**.
3. Esperá uno o dos minutos y recargá: arriba aparece el link, con esta forma: `https://TU-USUARIO.github.io/analizador-de-archivos/`

Si el curso publica de otra forma, subí solo `index.html`: `proxy.py`, `worker/` y `docs/` no hacen falta en el servidor.

## 4. Probar en el celular

1. Abrí el link en el celular.
2. Pegá tu API key (en el celular se guarda aparte de la de tu PC).
3. Tocá la zona punteada, elegí un archivo chico y esperá el resultado.
4. Si dice "No hay conexión con el puente", revisá el link del Worker del paso 2.

## Para tener en cuenta

- **Gratis y sin sorpresas:** el plan gratuito de Cloudflare permite 100.000 peticiones por día. Si se pasa, el Worker deja de responder hasta el día siguiente; no cobra nada.
- **Cada uno usa su propia API key:** el puente no guarda ninguna, solo la pasa a VirusTotal.
- **Si falla al publicar,** presentás desde tu compu con `proxy.py` y lo subís después.
