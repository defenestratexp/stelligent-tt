'use strict';

// Sample app for module 15. It has no dependencies: only Node.js built-ins.
//
// Environment variables (all optional):
//   PORT         port to listen on (default 8080)
//   BG_COLOR     page background: a CSS color name or #hex value (default white)
//   APP_VERSION  shown on the page so you can see a rolling update happen
//
// Endpoints:
//   GET /         HTML page showing the color, version and the Pod's hostname
//   GET /healthz  plain "ok", for readiness and liveness probes

const http = require('node:http');
const os = require('node:os');

const PORT = Number.parseInt(process.env.PORT || '8080', 10);
const APP_VERSION = process.env.APP_VERSION || 'v1';
const HOSTNAME = os.hostname();

// Accept only simple color values, so the variable can't inject HTML or CSS.
const COLOR_PATTERN = /^(#[0-9a-fA-F]{3,8}|[a-zA-Z]{1,30})$/;
const requestedColor = process.env.BG_COLOR || 'white';
const BG_COLOR = COLOR_PATTERN.test(requestedColor) ? requestedColor : 'white';
if (BG_COLOR !== requestedColor) {
  console.warn(`Ignoring BG_COLOR=${JSON.stringify(requestedColor)}; using white`);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function page() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Stelligent-U module 15</title>
  <style>
    body { margin: 0; min-height: 100vh; background: ${BG_COLOR};
           font-family: system-ui, sans-serif; display: grid; place-items: center; }
    main { background: white; padding: 2rem 3rem; border-radius: 0.5rem;
           box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2); }
    dt { font-weight: bold; }
  </style>
</head>
<body>
  <main>
    <h1>Hello from EKS</h1>
    <dl>
      <dt>Version</dt><dd>${escapeHtml(APP_VERSION)}</dd>
      <dt>Background</dt><dd>${escapeHtml(BG_COLOR)}</dd>
      <dt>Served by Pod</dt><dd>${escapeHtml(HOSTNAME)}</dd>
    </dl>
  </main>
</body>
</html>
`;
}

const server = http.createServer((req, res) => {
  const path = new URL(req.url, 'http://localhost').pathname;

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { Allow: 'GET, HEAD' });
    res.end();
    return;
  }

  if (path === '/healthz') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok\n');
    return;
  }

  if (path === '/') {
    res.writeHead(200, {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
    });
    res.end(page());
    console.log(`${new Date().toISOString()} ${req.method} ${path} from ${req.socket.remoteAddress}`);
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('not found\n');
});

server.listen(PORT, () => {
  console.log(`listening on port ${PORT}, version ${APP_VERSION}, color ${BG_COLOR}`);
});

// Kubernetes sends SIGTERM when it stops a Pod (for example during a rolling
// update). Stop accepting new connections and exit once in-flight requests end.
function shutdown(signal) {
  console.log(`${signal} received, shutting down`);
  server.close(() => process.exit(0));
  server.closeIdleConnections();
  // Don't wait forever: the Pod's terminationGracePeriodSeconds defaults to 30.
  setTimeout(() => process.exit(0), 10000).unref();
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
