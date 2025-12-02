const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Отдаем статические файлы из текущей директории
app.use(express.static(path.join(__dirname)));

// Главная страница - quiz.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'quiz.html'));
});

// Fallback для всех остальных маршрутов
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'quiz.html'));
});

app.listen(PORT, () => {
  console.log(`Сервер запущен на порту ${PORT}`);
  console.log(`Откройте http://localhost:${PORT} в браузере`);
});







