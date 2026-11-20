// Puente en la nube para el Analizador de Archivos (Cloudflare Workers).
// Hace lo mismo que proxy.py, pero publicado en internet: así la app anda desde cualquier lado.
// El navegador no puede llamar directo a VirusTotal (CORS); este puente sí, y le agrega
// al navegador el permiso (cabeceras CORS) para leer la respuesta.

const VIRUSTOTAL = 'https://www.virustotal.com';

// Permiso para que la página publicada pueda leer las respuestas del puente
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'x-apikey, content-type',
};

export default {
  async fetch(request) {
    const url = new URL(request.url);

    // El navegador pregunta antes si puede mandar la cabecera x-apikey: le decimos que sí
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });

    // Solo reenvía lo que usa la app (buscar, subir y consultar análisis)
    if (!/^\/api\/v3\/(files|analyses)(\/|$)/.test(url.pathname)) {
      return new Response('No encontrado', { status: 404, headers: CORS });
    }

    const cabeceras = { 'x-apikey': request.headers.get('x-apikey') || '', accept: 'application/json' };
    if (request.headers.get('content-type')) cabeceras['content-type'] = request.headers.get('content-type');

    const respuesta = await fetch(VIRUSTOTAL + url.pathname, {
      method: request.method,
      headers: cabeceras,
      // El archivo se lee entero (máx. 32 MB) para que el pedido salga con su tamaño exacto
      body: request.method === 'POST' ? await request.arrayBuffer() : undefined,
    });

    // "Archivo no encontrado" es normal (VirusTotal no lo conoce): igual que proxy.py, lo mandamos
    // como 200 para que la consola del navegador no lo pinte en rojo.
    let codigo = respuesta.status;
    if (codigo === 404 && request.method === 'GET' && url.pathname.startsWith('/api/v3/files/')) codigo = 200;

    return new Response(respuesta.body, {
      status: codigo,
      headers: { ...CORS, 'content-type': respuesta.headers.get('content-type') || 'application/json' },
    });
  },
};
