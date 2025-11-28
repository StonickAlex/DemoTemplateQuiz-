#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для преобразования QuizKatrin_IMPROVED.md в JSON для HTML-квиза
"""

import re
import json
from typing import Dict, List, Any

def parse_points(points_str: str) -> int:
    """Парсит строку с баллами и возвращает число"""
    # Убираем "+" и "балла", "баллов" и т.д.
    points_str = points_str.replace('+', '').strip()
    # Извлекаем число
    match = re.search(r'(\d+)', points_str)
    if match:
        return int(match.group(1))
    return 0

def parse_markdown(content: str) -> Dict[str, Any]:
    """Парсит markdown файл и создает структуру вопросов"""
    questions = {}
    current_question = None
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Ищем заголовок вопроса
        question_match = re.match(r'^### ВОПРОС (.+?): (.+)$', line)
        if question_match:
            question_id = question_match.group(1).strip()
            question_text = question_match.group(2).strip()
            current_question = {
                'id': question_id,
                'text': question_text,
                'answers': []
            }
            questions[question_id] = current_question
            continue
        
        # Ищем ответ
        answer_match = re.match(r'^\*\*Ответ (.+?): (.+?)\*\* \((.+?)\)', line)
        if answer_match and current_question:
            answer_id = answer_match.group(1).strip()
            answer_text = answer_match.group(2).strip()
            points_str = answer_match.group(3).strip()
            points = parse_points(points_str)
            
            # Ищем следующий вопрос в следующей строке
            next_question = None
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('→'):
                    if 'РЕЗУЛЬТАТЫ' in next_line:
                        next_question = 'RESULTS'
                    else:
                        next_match = re.match(r'^→ ВОПРОС (.+?)(?:: (.+))?$', next_line)
                        if next_match:
                            next_question = next_match.group(1).strip()
            
            current_question['answers'].append({
                'id': answer_id,
                'text': answer_text,
                'points': points,
                'nextQuestion': next_question
            })
    
    return questions

def get_results_info() -> Dict[str, Any]:
    """Возвращает информацию о результатах"""
    return {
        'levels': [
            {
                'min': 0,
                'max': 30,
                'title': 'Обычный человек, слабая связь с родом',
                'description': 'Минимальные проявления способностей. Обычная жизнь без особых родовых программ.'
            },
            {
                'min': 31,
                'max': 60,
                'title': 'Чувствительность к энергии рода, начальные способности',
                'description': 'Есть связь с родом, но не критическая. Проявляются начальные способности (интуиция, чувствительность).'
            },
            {
                'min': 61,
                'max': 100,
                'title': 'Сильная связь с родом, развитые способности',
                'description': 'Явная связь с родовой энергией. Развитые способности (вещие сны, дежа-вю, чувствительность к энергии).'
            },
            {
                'min': 101,
                'max': 150,
                'title': 'Очень сильная связь, мощные способности, возможны родовые проклятия',
                'description': 'Очень сильная связь с родом. Мощные способности, которые могут мешать или помогать. Тяжелые родовые программы или проклятия.'
            },
            {
                'min': 151,
                'max': 9999,
                'title': 'Критическая связь с родом, сильные способности и тяжелые родовые программы',
                'description': 'Критическая связь с родом. Очень сильные способности, которые могут быть опасны. Тяжелые родовые проклятия и программы.'
            }
        ]
    }

def main():
    # Читаем markdown файл из корня проекта
    import os
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_file = os.path.join(root_dir, 'QuizKatrin_IMPROVED.md')
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Парсим
    questions = parse_markdown(content)
    
    # Получаем информацию о результатах
    results = get_results_info()
    
    # Создаем финальную структуру
    quiz_data = {
        'title': 'Узнай, какая суперсила передалась тебе по роду',
        'startQuestion': '1',
        'questions': questions,
        'results': results
    }
    
    # Сохраняем в JSON в текущей директории (quiz/)
    import os
    json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz_data.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    
    print(f"Обработано {len(questions)} вопросов")
    print(f"Создан файл: {json_file}")

if __name__ == '__main__':
    main()

