#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

# Читаем наш квиз из JSON
with open('quiz_data.json', 'r', encoding='utf-8') as f:
    our_quiz = json.load(f)

# Читаем docx (конвертированный в txt)
with open('quiz_full_formatted_temp.txt', 'r', encoding='utf-8') as f:
    docx_lines = f.readlines()

# Парсим docx файл
docx_questions = {}
current_q = None
current_q_text = None
current_answers = []
in_answers = False

for line in docx_lines:
    line = line.strip()
    if not line:
        continue
    
    # Находим вопрос
    q_match = re.match(r'Вопрос\s+([\d\.a]+)\.\s+(.+)', line)
    if q_match:
        if current_q:
            docx_questions[current_q] = {'text': current_q_text, 'answers': current_answers}
        current_q = q_match.group(1)
        current_q_text = q_match.group(2)
        current_answers = []
        in_answers = False
        continue
    
    # Находим начало ответов
    if line == 'Ответы:':
        in_answers = True
        continue
    
    # Находим ответ
    if in_answers and current_q:
        ans_match = re.match(r'[\d\.a]+\.\s+(.+?)\s+→\s+(.+)', line)
        if ans_match:
            ans_text = ans_match.group(1).strip()
            next_q = ans_match.group(2).strip()
            current_answers.append({'text': ans_text, 'nextQuestion': next_q})

if current_q:
    docx_questions[current_q] = {'text': current_q_text, 'answers': current_answers}

# Сравниваем
our_q_ids = set(our_quiz['questions'].keys())
docx_q_ids = set(docx_questions.keys())

print('=' * 80)
print('ДЕТАЛЬНОЕ СРАВНЕНИЕ: quiz_full_formatted.docx vs quiz_data.json')
print('=' * 80)

print(f'\n📊 ОБЩАЯ СТАТИСТИКА:')
print(f'  • Вопросов в quiz_data.json: {len(our_q_ids)}')
print(f'  • Вопросов в docx файле: {len(docx_q_ids)}')
print(f'  • Общих вопросов: {len(our_q_ids & docx_q_ids)}')

# Вопросы, которых нет в docx
missing_in_docx = sorted(our_q_ids - docx_q_ids)
if missing_in_docx:
    print(f'\n❌ ВОПРОСЫ, КОТОРЫХ НЕТ В DOCX ({len(missing_in_docx)}):')
    for q_id in missing_in_docx:
        our_q = our_quiz['questions'][q_id]
        print(f'  • {q_id}: {our_q["text"]}')
        print(f'    Ответов: {len(our_q["answers"])}')

# Вопросы, которых нет у нас
extra_in_docx = sorted(docx_q_ids - our_q_ids)
if extra_in_docx:
    print(f'\n⚠️ ВОПРОСЫ, КОТОРЫХ НЕТ В quiz_data.json ({len(extra_in_docx)}):')
    for q_id in extra_in_docx:
        print(f'  • {q_id}: {docx_questions[q_id]["text"]}')

# Сравниваем общие вопросы
common_q_ids = sorted(our_q_ids & docx_q_ids, key=lambda x: (len(x.split('.')), x))
text_differences = []
answer_count_differences = []
answer_text_differences = []
next_q_differences = []

for q_id in common_q_ids:
    our_q = our_quiz['questions'][q_id]
    docx_q = docx_questions[q_id]
    
    # Текст вопроса
    if our_q['text'] != docx_q['text']:
        text_differences.append({
            'id': q_id,
            'our': our_q['text'],
            'docx': docx_q['text']
        })
    
    # Количество ответов
    if len(our_q['answers']) != len(docx_q['answers']):
        answer_count_differences.append({
            'id': q_id,
            'our_count': len(our_q['answers']),
            'docx_count': len(docx_q['answers']),
            'our_ans': [a['text'] for a in our_q['answers']],
            'docx_ans': [a['text'] for a in docx_q['answers']]
        })
    
    # Сравниваем ответы
    our_ans_dict = {ans['text']: ans for ans in our_q['answers']}
    docx_ans_dict = {ans['text']: ans for ans in docx_q['answers']}
    
    # Ответы, которые есть у нас, но нет в docx
    for ans_text, our_ans in our_ans_dict.items():
        if ans_text not in docx_ans_dict:
            # Ищем похожий
            found_similar = False
            for docx_ans_text in docx_ans_dict.keys():
                # Нормализуем для сравнения
                our_norm = ans_text.lower().replace(' ', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                docx_norm = docx_ans_text.lower().replace(' ', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                if our_norm == docx_norm or (len(our_norm) > 15 and our_norm[:15] in docx_norm) or (len(docx_norm) > 15 and docx_norm[:15] in our_norm):
                    found_similar = True
                    # Проверяем nextQuestion
                    if our_ans['nextQuestion'] != docx_ans_dict[docx_ans_text]['nextQuestion']:
                        next_q_differences.append({
                            'id': q_id,
                            'answer': ans_text[:50],
                            'our_next': our_ans['nextQuestion'],
                            'docx_next': docx_ans_dict[docx_ans_text]['nextQuestion']
                        })
                    break
            if not found_similar:
                answer_text_differences.append({
                    'id': q_id,
                    'type': 'missing_in_docx',
                    'text': ans_text
                })
    
    # Ответы, которые есть в docx, но нет у нас
    for ans_text, docx_ans in docx_ans_dict.items():
        if ans_text not in our_ans_dict:
            found_similar = False
            for our_ans_text in our_ans_dict.keys():
                our_norm = ans_text.lower().replace(' ', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                docx_norm = our_ans_text.lower().replace(' ', '').replace(',', '').replace('.', '').replace('(', '').replace(')', '')
                if our_norm == docx_norm or (len(our_norm) > 15 and our_norm[:15] in docx_norm) or (len(docx_norm) > 15 and docx_norm[:15] in our_norm):
                    found_similar = True
                    break
            if not found_similar:
                answer_text_differences.append({
                    'id': q_id,
                    'type': 'missing_in_our',
                    'text': ans_text
                })

# Выводим результаты
if text_differences:
    print(f'\n📝 РАЗЛИЧИЯ В ТЕКСТАХ ВОПРОСОВ ({len(text_differences)}):')
    for diff in text_differences[:15]:  # Показываем первые 15
        print(f'\n  {diff["id"]}:')
        print(f'    Наш:    {diff["our"]}')
        print(f'    Docx:   {diff["docx"]}')
    if len(text_differences) > 15:
        print(f'\n  ... и еще {len(text_differences) - 15} различий')

if answer_count_differences:
    print(f'\n📊 РАЗНОЕ КОЛИЧЕСТВО ОТВЕТОВ ({len(answer_count_differences)}):')
    for diff in answer_count_differences:
        print(f'\n  {diff["id"]}: у нас {diff["our_count"]}, в docx {diff["docx_count"]}')
        print(f'    Наши ответы: {diff["our_ans"]}')
        print(f'    Docx ответы: {diff["docx_ans"]}')

if answer_text_differences:
    missing_in_docx_ans = [d for d in answer_text_differences if d['type'] == 'missing_in_docx']
    missing_in_our_ans = [d for d in answer_text_differences if d['type'] == 'missing_in_our']
    
    if missing_in_docx_ans:
        print(f'\n❌ ОТВЕТЫ, КОТОРЫХ НЕТ В DOCX ({len(missing_in_docx_ans)}):')
        for diff in missing_in_docx_ans[:15]:
            print(f'  • {diff["id"]}: "{diff["text"][:70]}..."')
        if len(missing_in_docx_ans) > 15:
            print(f'  ... и еще {len(missing_in_docx_ans) - 15}')
    
    if missing_in_our_ans:
        print(f'\n⚠️ ОТВЕТЫ, КОТОРЫХ НЕТ В quiz_data.json ({len(missing_in_our_ans)}):')
        for diff in missing_in_our_ans[:15]:
            print(f'  • {diff["id"]}: "{diff["text"][:70]}..."')
        if len(missing_in_our_ans) > 15:
            print(f'  ... и еще {len(missing_in_our_ans) - 15}')

if next_q_differences:
    print(f'\n🔀 РАЗНЫЕ СЛЕДУЮЩИЕ ВОПРОСЫ ({len(next_q_differences)}):')
    for diff in next_q_differences[:10]:
        print(f'  • {diff["id"]}: ответ "{diff["answer"]}..."')
        print(f'    Наш: {diff["our_next"]}, Docx: {diff["docx_next"]}')
    if len(next_q_differences) > 10:
        print(f'  ... и еще {len(next_q_differences) - 10}')

print(f'\n' + '=' * 80)
print('ИТОГ:')
if missing_in_docx or text_differences or answer_count_differences or answer_text_differences:
    print('⚠️ Квизы РАЗЛИЧАЮТСЯ')
    print(f'  • Отсутствуют в docx: {len(missing_in_docx)} вопросов')
    print(f'  • Разные тексты: {len(text_differences)} вопросов')
    print(f'  • Разное количество ответов: {len(answer_count_differences)} вопросов')
    print(f'  • Разные ответы: {len(answer_text_differences)} случаев')
    if next_q_differences:
        print(f'  • Разные переходы: {len(next_q_differences)} случаев')
else:
    print('✅ Квизы ИДЕНТИЧНЫ')
print('=' * 80)



