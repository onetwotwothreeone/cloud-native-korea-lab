const express = require('express');

const app = express();
const port = process.env.PORT || 3000;
const version = process.env.APP_VERSION || 'v0.1.0';

app.use(express.json());

app.get('/', (req, res) => {
  res.json({
    service: 'Cloud Native AI Docs Agent',
    status: 'running',
    version,
    message: 'Welcome to Cloud Native AI Docs Agent.'
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

app.post('/ask', (req, res) => {
  const { question } = req.body;

  if (!question || typeof question !== 'string') {
    return res.status(400).json({
      error: 'question is required',
      message: 'Please send a JSON body like: { "question": "What is Kubernetes?" }'
    });
  }

  res.json({
    question,
    answer: {
      summary: 'Kubernetes is a system that helps run and manage containers automatically.',
      easyExplanation: '쉽게 말하면 Kubernetes는 여러 컨테이너를 관리하는 운영 매니저입니다.',
      keyTerms: [
        {
          term: 'Container',
          meaning: '앱과 실행 환경을 함께 포장한 작은 실행 박스입니다.'
        },
        {
          term: 'Pod',
          meaning: 'Kubernetes에서 컨테이너가 실행되는 가장 작은 단위입니다.'
        },
        {
          term: 'Deployment',
          meaning: 'Pod를 원하는 개수만큼 유지하고 업데이트하는 관리자입니다.'
        },
        {
          term: 'Service',
          meaning: 'Pod에 안정적으로 접근할 수 있게 해주는 네트워크 입구입니다.'
        }
      ],
      practice: {
        title: 'Check Kubernetes resources',
        commands: [
          'kubectl get pods',
          'kubectl get svc',
          'kubectl describe deployment mini-platform'
        ]
      },
      note: 'This is a fixed example response. AI and RAG will be added in a later version.'
    },
    sources: [
      {
        title: 'Kubernetes Official Documentation',
        type: 'official-docs',
        url: 'https://kubernetes.io/docs/'
      }
    ],
    version
  });
});

app.listen(port, () => {
  console.log(`Cloud Native AI Docs Agent is running on port ${port}`);
});
