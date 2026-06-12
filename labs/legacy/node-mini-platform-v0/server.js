const http = require('http');

const appName = 'Cloud Native Korea Lab Mini Platform';
const version = '0.1.0';
const port = process.env.PORT || 3000;

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8'
  });
  res.end(JSON.stringify(data, null, 2));
}

function sendHtml(res, statusCode, html) {
  res.writeHead(statusCode, {
    'Content-Type': 'text/html; charset=utf-8'
  });
  res.end(html);
}

const server = http.createServer((req, res) => {
  const { method, url } = req;

  console.log(`${new Date().toISOString()} ${method} ${url}`);

  if (method === 'GET' && url === '/') {
    return sendHtml(res, 200, `
      <!doctype html>
      <html lang="ko">
        <head>
          <meta charset="utf-8" />
          <title>${appName}</title>
        </head>
        <body>
          <h1>${appName}</h1>
          <p>Mini Platform v${version} is running.</p>
          <ul>
            <li><a href="/health">/health</a></li>
            <li><a href="/version">/version</a></li>
          </ul>
        </body>
      </html>
    `);
  }

  if (method === 'GET' && url === '/health') {
    return sendJson(res, 200, {
      status: 'ok',
      service: appName,
      uptime: process.uptime(),
      timestamp: new Date().toISOString()
    });
  }

  if (method === 'GET' && url === '/version') {
    return sendJson(res, 200, {
      service: appName,
      version,
      environment: process.env.NODE_ENV || 'local'
    });
  }

  return sendJson(res, 404, {
    error: 'Not Found',
    message: `Cannot ${method} ${url}`
  });
});

server.listen(port, () => {
  console.log(`${appName} v${version} is running on http://localhost:${port}`);
});
