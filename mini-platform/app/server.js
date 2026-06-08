const express = require('express');

const app = express();
const port = process.env.PORT || 3000;
const version = process.env.APP_VERSION || 'v0.1.0';

app.get('/', (req, res) => {
  res.json({
    service: 'Cloud Native Korea Lab Mini Platform',
    status: 'running',
    version,
    message: 'Welcome to Cloud Native Korea Lab Mini Platform.'
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'ok'
  });
});

app.get('/version', (req, res) => {
  res.json({
    version
  });
});

app.listen(port, () => {
  console.log(`Cloud Native Korea Lab Mini Platform is running on port ${port}`);
});
