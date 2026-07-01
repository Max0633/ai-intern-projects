# -*- coding: utf-8 -*-
"""
智能日程管理助手 - 主应用文件
支持AI建议、时间优化、冲突检测
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from openai import OpenAI
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('scheduler.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            priority INTEGER DEFAULT 3,
            category TEXT DEFAULT '其他',
            is_completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def check_time_conflict(start1, end1, start2, end2):
    """检查时间冲突"""
    return start1 < end2 and start2 < end1

def get_conflicting_events(events, new_start, new_end):
    """获取冲突的事件"""
    conflicts = []
    for event in events:
        if check_time_conflict(
            new_start, new_end,
            event['start_time'], event['end_time']
        ):
            conflicts.append(event)
    return conflicts

def generate_schedule_suggestion(events):
    """使用AI生成日程建议"""
    client = get_openai_client()
    if not client:
        return "请先配置OpenAI API密钥"
    
    # 准备事件信息
    events_text = ""
    for event in events:
        events_text += f"- {event['title']}: {event['start_time']} 到 {event['end_time']}\n"
    
    prompt = f"""你是一个时间管理专家。请根据以下现有日程，提供优化建议：

现有日程：
{events_text if events_text else '暂无日程安排'}

请提供：
1. 时间安排建议
2. 优先级调整建议
3. 可能的优化点
4. 注意事项"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的时间管理顾问，擅长优化日程安排。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成建议失败: {str(e)}"

def optimize_schedule(events):
    """优化日程安排"""
    # 按优先级和时间排序
    sorted_events = sorted(events, key=lambda x: (x['priority'], x['start_time']))
    
    optimized = []
    current_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for event in sorted_events:
        event_start = datetime.fromisoformat(event['start_time'])
        event_end = datetime.fromisoformat(event['end_time'])
        duration = event_end - event_start
        
        # 如果有冲突，调整时间
        if optimized:
            last_end = datetime.fromisoformat(optimized[-1]['end_time'])
            if event_start < last_end:
                event_start = last_end + timedelta(minutes=15)  # 15分钟间隔
                event_end = event_start + duration
        
        optimized.append({
            **event,
            'start_time': event_start.isoformat(),
            'end_time': event_end.isoformat()
        })
    
    return optimized

@app.route('/')
def index():
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # 获取今天的事件
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('''
        SELECT * FROM events 
        WHERE DATE(start_time) = ? 
        ORDER BY start_time
    ''', (today,))
    today_events = [dict(row) for row in c.fetchall()]
    
    # 获取本周事件
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
    week_end = (datetime.now() + timedelta(days=6-datetime.now().weekday())).strftime('%Y-%m-%d')
    c.execute('''
        SELECT * FROM events 
        WHERE DATE(start_time) BETWEEN ? AND ? 
        ORDER BY start_time
    ''', (week_start, week_end))
    week_events = [dict(row) for row in c.fetchall()]
    
    conn.close()
    
    return render_template('index.html', 
                         today_events=today_events, 
                         week_events=week_events)

@app.route('/event/new', methods=['GET', 'POST'])
def new_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        priority = int(request.form.get('priority', 3))
        category = request.form.get('category', '其他')
        
        # 检查冲突
        conn = sqlite3.connect('scheduler.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM events WHERE DATE(start_time) = ?', 
                 (datetime.fromisoformat(start_time).strftime('%Y-%m-%d'),))
        existing_events = [dict(row) for row in c.fetchall()]
        conn.close()
        
        conflicts = get_conflicting_events(
            existing_events, 
            datetime.fromisoformat(start_time),
            datetime.fromisoformat(end_time)
        )
        
        if conflicts:
            conflict_titles = ', '.join([e['title'] for e in conflicts])
            return render_template('event_form.html', 
                                 event=None, 
                                 error=f"与以下事件冲突: {conflict_titles}")
        
        # 保存事件
        conn = sqlite3.connect('scheduler.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO events (title, description, start_time, end_time, priority, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, start_time, end_time, priority, category))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('event_form.html', event=None)

@app.route('/event/<int:id>')
def view_event(id):
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id = ?', (id,))
    event = dict(c.fetchone())
    conn.close()
    return render_template('event_detail.html', event=event)

@app.route('/event/<int:id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        priority = int(request.form.get('priority', 3))
        category = request.form.get('category', '其他')
        is_completed = 'is_completed' in request.form
        
        c.execute('''
            UPDATE events 
            SET title=?, description=?, start_time=?, end_time=?, 
                priority=?, category=?, is_completed=?
            WHERE id=?
        ''', (title, description, start_time, end_time, priority, category, is_completed, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_event', id=id))
    
    c.execute('SELECT * FROM events WHERE id = ?', (id,))
    event = dict(c.fetchone())
    conn.close()
    return render_template('event_form.html', event=event)

@app.route('/event/<int:id>/delete', methods=['POST'])
def delete_event(id):
    conn = sqlite3.connect('scheduler.db')
    c = conn.cursor()
    c.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/suggestion')
def api_suggestion():
    """获取AI日程建议"""
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM events ORDER BY start_time')
    events = [dict(row) for row in c.fetchall()]
    conn.close()
    
    suggestion = generate_schedule_suggestion(events)
    return jsonify({"suggestion": suggestion})

@app.route('/api/events', methods=['GET'])
def api_events():
    """获取所有事件"""
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM events ORDER BY start_time')
    events = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(events)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
