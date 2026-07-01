# 智能日程管理助手

基于Flask和OpenAI的智能日程管理应用，支持AI建议、冲突检测、优先级管理。

## 功能特点

- 📅 **日程管理**: 创建、编辑、删除日程事件
- 🤖 **AI建议**: 智能分析日程，提供优化建议
- ⚠️ **冲突检测**: 自动检测时间冲突
- 🎯 **优先级管理**: 支持1-5级优先级设置
- 📊 **分类管理**: 支持事件分类
- ✅ **完成状态**: 标记事件完成状态

## 技术栈

- **后端**: Python, Flask
- **数据库**: SQLite
- **AI**: OpenAI API
- **前端**: HTML, CSS, JavaScript

## 项目结构

`
smart-scheduler/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖
├── README.md          # 项目文档
├── templates/         # HTML模板
│   ├── base.html     # 基础模板
│   ├── index.html    # 首页(日程视图)
│   ├── event_form.html # 事件表单
│   └── event_detail.html # 事件详情
├── static/            # 静态文件
│   └── css/
│       └── style.css  # 样式文件
└── utils/             # 工具函数
    └── helpers.py     # 辅助函数
`

## 安装步骤

### 1. 克隆项目
`ash
git clone https://github.com/your-username/smart-scheduler.git
cd smart-scheduler
`

### 2. 创建虚拟环境
`ash
python -m venv venv
venv\Scripts\activate  # Windows
`

### 3. 安装依赖
`ash
pip install -r requirements.txt
`

### 4. 配置API密钥
创建 .env 文件：
`
OPENAI_API_KEY=your_openai_api_key_here
`

### 5. 运行应用
`ash
python app.py
`

访问 http://localhost:5001

## 使用方法

1. **添加事件**: 点击"新建事件"，填写详细信息
2. **查看日程**: 首页显示今日和本周日程
3. **获取建议**: 点击"AI建议"获取优化建议
4. **管理事件**: 编辑、删除、标记完成

## 核心功能详解

### 冲突检测
系统会自动检测新事件与现有事件的时间冲突，避免安排重叠。

### AI日程优化
基于现有日程，AI会分析并提供：
- 时间安排建议
- 优先级调整建议
- 优化点识别
- 注意事项提醒

### 优先级系统
- 1级: 最高优先级（紧急重要）
- 2级: 高优先级（重要不紧急）
- 3级: 中优先级（一般）
- 4级: 低优先级（不重要）
- 5级: 最低优先级

## 示例

### 创建事件
`
标题: 项目会议
时间: 2024-01-15 14:00 - 15:30
优先级: 2级
分类: 工作
`

### AI建议示例
`
建议:
1. 上午安排创意性工作，下午安排会议
2. 预留15分钟缓冲时间
3. 重要会议前避免安排高强度工作
`

## 扩展功能

- [ ] 集成Google Calendar
- [ ] 添加提醒功能
- [ ] 支持重复事件
- [ ] 多用户支持
- [ ] 移动端适配

## 学习收获

通过这个项目，我掌握了：
- Flask Web应用开发
- SQLite数据库操作
- 时间处理和冲突检测算法
- OpenAI API调用
- 日程管理业务逻辑

## 联系方式

- **GitHub**: [your-username]
- **邮箱**: your-email@example.com

---
*最后更新: 2026-07-02*
