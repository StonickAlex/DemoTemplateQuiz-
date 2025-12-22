#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация полного JSON квиза на основе docx_full_text.txt
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
    """Парсит docx_full_text.txt и создает структуру вопросов"""
    with open('docx_full_text.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    questions = {}
    current_question = None
    current_answers = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('Множественный выбор') or line.startswith('Во всех ответах'):
            i += 1
            continue
        
        # Находим вопрос
        question_match = re.match(r'Вопрос\s+(\d+(?:\.\d+[a-z]?)+)\.\s*(.+)', line)
        if question_match:
            # Сохраняем предыдущий вопрос
            if current_question:
                questions[current_question['id']] = {
                    'id': current_question['id'],
                    'text': clean_text(current_question['text']),
                    'answers': current_answers
                }
            
            # Начинаем новый вопрос
            q_id = question_match.group(1)
            q_text = question_match.group(2)
            current_question = {'id': q_id, 'text': q_text}
            current_answers = []
            i += 1
            continue
        
        # Находим ответы
        if line == 'Ответы:':
            i += 1
            continue
        
        answer_match = re.match(r'(\d+(?:\.\d+[a-z]?)+)\.\s*(.+?)\s*→\s*(\S+)', line)
        if answer_match:
            ans_id = answer_match.group(1)
            ans_text = answer_match.group(2).strip()
            next_q = answer_match.group(3).strip()
            
            # Определяем баллы (пока 0, потом добавим)
            points = 0
            
            current_answers.append({
                'id': ans_id,
                'text': ans_text,
                'points': points,
                'nextQuestion': next_q
            })
            i += 1
            continue
        
        i += 1
    
    # Сохраняем последний вопрос
    if current_question:
        questions[current_question['id']] = {
            'id': current_question['id'],
            'text': clean_text(current_question['text']),
            'answers': current_answers
        }
    
    return questions

def add_scoring(questions):
    """Добавляет систему баллов к вопросам"""
    # Это будет сделано вручную после проверки структуры
    # Пока оставляем все баллы = 0
    return questions

def create_results():
    """Создает структуру results"""
    return {
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

def main():
    print("Парсинг docx_full_text.txt...")
    questions = parse_docx_text()
    
    print(f"Найдено вопросов: {len(questions)}")
    
    # Добавляем баллы
    questions = add_scoring(questions)
    
    # Создаем полную структуру
    quiz_data = {
        "title": "Диагностика связи с родом",
        "startQuestion": "1",
        "questions": questions,
        "results": create_results()
    }
    
    # Сохраняем
    with open('quiz_alex_full.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=4)
    
    print("✅ Создан quiz_alex_full.json")
    print(f"Всего вопросов: {len(questions)}")

if __name__ == '__main__':
    main()

