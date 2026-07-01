# -*- coding: utf-8 -*-
"""
个人智能笔记管理系统 - 主应用文件
支持AI摘要、语义搜索、自动标签
"""

import os
import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT DEFAULT '',
            summary TEXT DEFAULT '',
            embedding TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# OpenAI客户端
client = None

def get_openai_client():
    global client
    if client is None:
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            client = OpenAI(api_key=api_key)
    return client

def generate_summary(content):
    """使用AI生成笔记摘要"""
    client = get_openai_client()
    if not client:
        return content[:100] + "..." if len(content) > 100 else content
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的摘要助手，请用简洁的语言概括用户提供的内容。"},
                {"role": "user", "content": f"请为以下内容生成一个简短的摘要：\n\n{content[:2000]}"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return content[:100] + "..." if len(content) > 100 else content

def generate_tags(content):
    """自动生成标签"""
    # 简单的关键词提取
    keywords = []
    common_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
    
    words = content.split()
    word_freq = {}
    for word in words:
        if len(word) > 1 and word not in common_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # 取频率最高的5个词作为标签
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:5]]
    
    return ','.join(keywords)

def semantic_search(query, notes):
    """语义搜索笔记"""
    if not notes:
        return []
    
    # 使用TF-IDF进行简单语义搜索
    documents = [note['content'] for note in notes]
    documents.append(query)
    
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        query_vector = tfidf_matrix[-1]
        note_vectors = tfidf_matrix[:-1]
        
        similarities = cosine_similarity(query_vector, note_vectors)[0]
        
        # 按相似度排序
        indexed_similarities = list(enumerate(similarities))
        indexed_similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in indexed_similarities:
            if score > 0.1:  # 相似度阈值
                note = notes[idx].copy()
                note['relevance'] = round(score * 100, 2)
                results.append(note)
        
        return results
    except Exception:
        return notes

@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notes ORDER BY updated_at DESC')
    notes = [dict(row) for row in c.fetchall()]
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/note/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 生成摘要和标签
        summary = generate_summary(content)
        tags = generate_tags(content)
        
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO notes (title, content, tags, summary)
            VALUES (?, ?, ?, ?)
        ''', (title, content, tags, summary))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('note_form.html', note=None)

@app.route('/note/<int:id>')
def view_note(id):
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notes WHERE id = ?', (id,))
    note = dict(c.fetchone())
    conn.close()
    return render_template('note_detail.html', note=note)

@app.route('/note/<int:id>/edit', methods=['GET', 'POST'])
def edit_note(id):
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        summary = generate_summary(content)
        tags = generate_tags(content)
        
        c.execute('''
            UPDATE notes 
            SET title=?, content=?, tags=?, summary=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (title, content, tags, summary, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_note', id=id))
    
    c.execute('SELECT * FROM notes WHERE id = ?', (id,))
    note = dict(c.fetchone())
    conn.close()
    return render_template('note_form.html', note=note)

@app.route('/note/<int:id>/delete', methods=['POST'])
def delete_note(id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    notes = [dict(row) for row in c.fetchall()]
    conn.close()
    
    results = semantic_search(query, notes)
    return render_template('search_results.html', results=results, query=query)

@app.route('/api/notes', methods=['GET'])
def api_notes():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM notes ORDER BY updated_at DESC')
    notes = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(notes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
