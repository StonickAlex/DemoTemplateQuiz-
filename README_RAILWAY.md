# Деплой квиза на Railway

## Быстрый старт

### 1. Подготовка

Убедитесь, что все файлы находятся в папке `quiz`:
- `quiz.html` - основной HTML файл
- `quiz_data.json` - данные квиза
- `server.js` - Node.js сервер
- `package.json` - зависимости

### 2. Деплой на Railway

#### Вариант 1: Через GitHub (рекомендуется)

1. **Создайте репозиторий на GitHub** (если еще нет)
   ```bash
   cd /Users/aleks/Documents/LeoDima
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <ваш-репозиторий>
   git push -u origin main
   ```

2. **Подключите Railway к GitHub:**
   - Зайдите на [railway.app](https://railway.app)
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Выберите ваш репозиторий
   - Railway автоматически определит, что это Node.js проект

3. **Настройте деплой:**
   - Railway автоматически найдет `package.json` в корне репозитория
   - Если `package.json` в папке `quiz`, укажите Root Directory: `quiz`
   - Railway автоматически установит зависимости и запустит `npm start`

#### Вариант 2: Через Railway CLI

1. **Установите Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Войдите в Railway:**
   ```bash
   railway login
   ```

3. **Создайте проект:**
   ```bash
   cd quiz
   railway init
   ```

4. **Деплой:**
   ```bash
   railway up
   ```

### 3. Настройка переменных окружения

Railway автоматически установит `PORT` из переменных окружения. Никаких дополнительных настроек не требуется.

### 4. Проверка

После деплоя Railway предоставит URL вида: `https://your-project-name.railway.app`

Откройте этот URL в браузере - квиз должен работать!

## Структура файлов

```
quiz/
├── quiz.html          # Основной HTML файл
├── quiz_data.json     # Данные квиза
├── server.js          # Express сервер
├── package.json       # Зависимости Node.js
└── README_RAILWAY.md  # Эта инструкция
```

## Обновление данных квиза

Если вы изменили `QuizKatrin_IMPROVED.md` в корне проекта:

1. Обновите JSON:
   ```bash
   cd quiz
   python3 generate_quiz_json.py
   ```

2. Закоммитьте изменения:
   ```bash
   git add quiz_data.json
   git commit -m "Update quiz data"
   git push
   ```

3. Railway автоматически перезапустит приложение

## Локальный запуск

Для тестирования локально:

```bash
cd quiz
npm install
npm start
```

Откройте http://localhost:3000

## Troubleshooting

**Проблема:** Railway не находит `package.json`
- **Решение:** Убедитесь, что Root Directory в настройках Railway установлен на `quiz`

**Проблема:** Квиз не загружается
- **Решение:** Проверьте, что `quiz_data.json` находится в той же папке, что и `quiz.html`

**Проблема:** Ошибка "Cannot find module 'express'"
- **Решение:** Railway должен автоматически установить зависимости. Если нет, проверьте, что `package.json` корректен

