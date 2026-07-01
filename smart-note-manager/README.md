# 个人智能笔记管理系统

基于Flask和OpenAI的智能笔记应用，支持AI摘要生成、语义搜索、自动标签。

## 功能特点

- 📝 **笔记管理**: 创建、编辑、删除、查看笔记
- 🤖 **AI摘要**: 自动生成笔记摘要
- 🔍 **语义搜索**: 基于内容的智能搜索
- 🏷️ **自动标签**: 自动提取关键词作为标签
- 💾 **本地存储**: SQLite数据库存储

## 技术栈

- **后端**: Python, Flask
- **数据库**: SQLite
- **AI**: OpenAI API
- **搜索**: TF-IDF + 余弦相似度
- **前端**: HTML, CSS, JavaScript

## 项目结构

`
smart-note-manager/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖
├── README.md          # 项目文档
├── templates/         # HTML模板
│   ├── base.html     # 基础模板
│   ├── index.html    # 首页
│   ├── note_form.html # 笔记表单
│   ├── note_detail.html # 笔记详情
│   └── search_results.html # 搜索结果
├── static/            # 静态文件
│   └── css/
│       └── style.css  # 样式文件
└── utils/             # 工具函数
    └── helpers.py     # 辅助函数
`

## 安装步骤

### 1. 克隆项目
`ash
git clone https://github.com/your-username/smart-note-manager.git
cd smart-note-manager
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

访问 http://localhost:5000

## 使用方法

1. **创建笔记**: 点击"新建笔记"，输入标题和内容
2. **查看笔记**: 点击笔记标题查看详情
3. **编辑笔记**: 在详情页点击"编辑"按钮
4. **搜索笔记**: 使用搜索框进行语义搜索
5. **删除笔记**: 在详情页点击"删除"按钮

## 核心功能详解

### AI摘要生成
使用OpenAI GPT模型自动生成笔记摘要，帮助快速了解笔记内容。

### 语义搜索
基于TF-IDF和余弦相似度实现语义搜索，即使关键词不完全匹配也能找到相关笔记。

### 自动标签
自动提取笔记中的关键词作为标签，方便分类和管理。

## 示例

`
笔记标题: 机器学习基础
笔记内容: 机器学习是人工智能的一个分支...
AI摘要: 介绍机器学习的基本概念和主要类型
自动标签: 机器学习,人工智能,算法,神经网络,数据
`

## 扩展功能

- [ ] 支持Markdown编辑
- [ ] 添加笔记分类功能
- [ ] 导出笔记为PDF
- [ ] 多用户支持
- [ ] 笔记共享功能

## 学习收获

通过这个项目，我掌握了：
- Flask Web应用开发
- SQLite数据库操作
- OpenAI API调用
- TF-IDF文本向量化
- 余弦相似度计算

## 联系方式

- **GitHub**: [your-username]
- **邮箱**: your-email@example.com

---
*最后更新: 2026-07-02*
