export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/app.js") {
      const asset = await env.ASSETS.fetch(new Request(new URL("/app.js", request.url)));

      const headers = new Headers(asset.headers);
      headers.set("Content-Type", "application/javascript");
      headers.set("Content-Encoding", "br");
      headers.set("Cache-Control", "public, max-age=604800, immutable");
      headers.set("Vary", "Accept-Encoding");
      headers.set("Access-Control-Allow-Origin", "*");
      headers.set("X-Debug-Worker", "yes");

      return new Response(asset.body, {
        status: asset.status,
        statusText: asset.statusText,
        headers,
      });
    }

    return env.ASSETS.fetch(request);
  },
};