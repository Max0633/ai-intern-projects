# AI智能问答助手

基于LangChain和OpenAI API构建的智能问答系统，支持多轮对话和知识检索(RAG)。

## 功能特点

- 🤖 **智能问答**: 基于大语言模型的自然语言理解
- 📚 **知识检索**: 支持上传文档，基于文档内容回答问题
- 💬 **多轮对话**: 支持上下文记忆的连续对话
- 🔍 **RAG技术**: 检索增强生成，提高回答准确性
- 🎯 **流式输出**: 实时显示AI回答

## 技术栈

- **后端**: Python 3.10+
- **AI框架**: LangChain
- **大模型**: OpenAI GPT-3.5/GPT-4
- **向量数据库**: ChromaDB
- **前端界面**: Streamlit
- **文档处理**: LangChain Document Loaders

## 项目结构

`
ai-qa-assistant/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖
├── README.md          # 项目文档
├── data/              # 示例文档目录
├── docs/              # 详细文档
├── utils/             # 工具函数
│   ├── __init__.py
│   ├── document_loader.py  # 文档加载器
│   └── vector_store.py     # 向量数据库管理
└── tests/             # 测试文件
`

## 安装步骤

### 1. 克隆项目
`ash
git clone https://github.com/your-username/ai-qa-assistant.git
cd ai-qa-assistant
`

### 2. 创建虚拟环境
`ash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
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
streamlit run app.py
`

## 使用方法

1. 启动应用后，在侧边栏输入OpenAI API密钥
2. 上传文档（支持.txt和.md格式）
3. 点击"处理文档"按钮
4. 在主界面输入问题，AI会基于文档内容回答

## 核心概念

### RAG (检索增强生成)
RAG是一种结合检索和生成的技术：
1. **检索**: 从知识库中找到相关文档片段
2. **增强**: 将检索到的信息作为上下文
3. **生成**: 基于上下文生成准确回答

### 向量数据库
使用ChromaDB存储文档的向量嵌入，支持语义搜索，快速找到相关文档。

## 示例对话

`
用户: 什么是机器学习？
AI: 机器学习是人工智能的一个分支，它使计算机系统能够从数据中学习并改进...
（基于上传的文档内容回答）
`

## 扩展功能

- [ ] 支持更多文档格式(PDF, Word)
- [ ] 添加对话历史持久化
- [ ] 支持多用户会话
- [ ] 添加知识库管理界面
- [ ] 集成更多大模型(本地模型)

## 学习收获

通过这个项目，我掌握了：
- LangChain框架的核心概念和使用方法
- RAG技术的实现原理
- 向量数据库的基本操作
- 大语言模型API的调用方式
- Streamlit快速开发Web应用

## 联系方式

- **GitHub**: [your-username]
- **邮箱**: your-email@example.com

---
*最后更新: 2026-07-02*
