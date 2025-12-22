#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Правильная генерация JSON квиза на основе docx_full_text.txt
"""

import json
import re

def clean_text(text):
    """Убирает 'Переходим на X' и 'Переходим ->X' из текста"""
    text = re.sub(r'\s*Переходим\s+на\s+\d+\s*', '', text)
    text = re.sub(r'\s*Переходим\s*->\s*\d+\s*', '', text)
    text = re.sub(r'\s*->\s*\d+\s*$', '', text)
    return text.strip()

def parse_docx_text():
    """Парсит docx_full_text.txt и создает правильную структуру вопросов"""
    with open('docx_full_text.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = {}
    
    # Паттерн для поиска вопросов
    # "Вопрос 1. Текст" или "Вопрос 2.2a. Текст"
    question_pattern = r'Вопрос\s+(\d+(?:\.\d+[a-z]?)*)\.\s*([^\n]+)'
    
    # Находим все вопросы
    question_matches = list(re.finditer(question_pattern, content))
    
    for i, match in enumerate(question_matches):
        q_id = match.group(1)
        q_text = match.group(2).strip()
        
        # Находим начало следующего вопроса или конца файла
        start_pos = match.end()
        if i + 1 < len(question_matches):
            end_pos = question_matches[i + 1].start()
        else:
            end_pos = len(content)
        
        question_block = content[start_pos:end_pos]
        
        # Парсим ответы из блока
        answers = []
        answer_pattern = r'(\d+(?:\.\d+[a-z]?)+)\.\s*([^\n→]+?)\s*→\s*(\S+)'
        
        for ans_match in re.finditer(answer_pattern, question_block):
            ans_id = ans_match.group(1)
            ans_text = ans_match.group(2).strip()
            next_q = ans_match.group(3).strip()
            
            # Проверяем, что это ответ для текущего вопроса
            if ans_id.startswith(q_id + '.'):
                answers.append({
                    'id': ans_id,
                    'text': ans_text,
                    'points': 0,  # Будет добавлено позже
                    'nextQuestion': next_q
                })
        
        if q_text and (answers or q_id == '1'):  # Вопрос 1 может не иметь ответов в блоке
            questions[q_id] = {
                'id': q_id,
                'text': clean_text(q_text),
                'answers': answers
            }
    
    # Специальная обработка вопроса 1 (дата рождения)
    if '1' in questions and not questions['1']['answers']:
        questions['1']['answers'] = [{
            'id': '1.1',
            'text': 'Дата рождения указана',
            'points': 0,
            'nextQuestion': '2'
        }]
    
    return questions

def main():
    print("Парсинг docx_full_text.txt...")
    questions = parse_docx_text()
    
    print(f"Найдено вопросов: {len(questions)}")
    
    # Выводим список всех вопросов для проверки
    main_q = sorted([q for q in questions.keys() if re.match(r'^\d+$', q)], key=int)
    print(f"Основные вопросы: {main_q}")
    
    # Создаем полную структуру
    quiz_data = {
        "title": "Диагностика связи с родом",
        "startQuestion": "1",
        "questions": questions,
        "results": {
            "levels": [
                {
                    "min": 0,
                    "max": 50,
                    "title": "Минимальная связь с родом",
                    "description": "Слабая связь с родовой энергией. Минимальные проявления способностей."
                },
                {
                    "min": 51,
                    "max": 100,
                    "title": "Умеренная связь с родом",
                    "description": "Есть связь с родом. Проявляются некоторые способности (интуиция, чувствительность)."
                },
                {
                    "min": 101,
                    "max": 150,
                    "title": "Сильная связь с родом",
                    "description": "Явная связь с родовой энергией. Развитые способности (вещие сны, дежа-вю, чувствительность к энергии)."
                },
                {
                    "min": 151,
                    "max": 200,
                    "title": "Очень сильная связь, возможны родовые программы",
                    "description": "Очень сильная связь с родом. Мощные способности, которые могут мешать или помогать. Тяжелые родовые программы."
                },
                {
                    "min": 201,
                    "max": 9999,
                    "title": "Критическая связь, родовые проклятия",
                    "description": "Критическая связь с родом. Очень мощные способности, но и тяжелые родовые проклятия и программы, требующие работы."
                }
            ]
        }
    }
    
    # Сохраняем
    with open('quiz_alex_correct.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=4)
    
    print("✅ Создан quiz_alex_correct.json")
    
    # Проверяем несколько вопросов
    print("\nПроверка структуры:")
    for q_id in ['1', '2', '3', '4']:
        if q_id in questions:
            q = questions[q_id]
            print(f"  {q_id}: {q['text'][:60]}... ({len(q['answers'])} ответов)")

if __name__ == '__main__':
    main()

