# -*- coding: utf-8 -*-
"""
AI智能问答助手 - 主应用文件
基于LangChain和OpenAI API构建的智能问答系统
支持多轮对话和知识检索(RAG)
"""

import os
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import tempfile
import shutil

# 页面配置
st.set_page_config(
    page_title="AI智能问答助手",
    page_icon="🤖",
    layout="wide"
)

# 自定义样式
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}
.bot-message {
    background-color: #f5f5f5;
    border-left: 4px solid #4caf50;
}
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

def load_documents(uploaded_files):
    """加载上传的文档"""
    documents = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # 根据文件类型选择加载器
            if uploaded_file.name.endswith('.txt'):
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
            elif uploaded_file.name.endswith('.md'):
                loader = TextLoader(file_path, encoding='utf-8')
                documents.extend(loader.load())
    finally:
        shutil.rmtree(temp_dir)
    
    return documents

def create_vectorstore(documents):
    """创建向量数据库"""
    # 文本分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    splits = text_splitter.split_documents(documents)
    
    # 创建向量数据库
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vectorstore

def create_conversation_chain(vectorstore):
    """创建对话链"""
    # 自定义提示模板
    template = """你是一个专业的AI助手，基于提供的上下文信息回答用户问题。
如果上下文中没有相关信息，请说明你无法从提供的文档中找到答案。
请用中文回答，保持回答准确、简洁、有帮助。

上下文信息:
{context}

用户问题: {question}

回答:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # 创建对话链
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
    return chain

def display_chat_history():
    """显示聊天历史"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    """主函数"""
    init_session_state()
    
    # 侧边栏
    with st.sidebar:
        st.header("📁 文档管理")
        
        # API密钥输入
        api_key = st.text_input(
            "OpenAI API密钥:",
            type="password",
            help="请输入你的OpenAI API密钥"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        st.divider()
        
        # 文件上传
        uploaded_files = st.file_uploader(
            "上传文档 (支持.txt, .md):",
            type=["txt", "md"],
            accept_multiple_files=True,
            help="上传文档后，AI将基于这些文档回答问题"
        )
        
        # 处理文档按钮
        if st.button("处理文档", type="primary"):
            if uploaded_files:
                with st.spinner("正在处理文档..."):
                    documents = load_documents(uploaded_files)
                    st.session_state.vectorstore = create_vectorstore(documents)
                    st.session_state.chain = create_conversation_chain(st.session_state.vectorstore)
                    st.success(f"✅ 成功处理 {len(documents)} 个文档")
            else:
                st.warning("⚠️ 请先上传文档")
        
        st.divider()
        
        # 清除对话按钮
        if st.button("🗑️ 清除对话"):
            st.session_state.messages = []
            st.rerun()
        
        # 使用说明
        st.divider()
        st.header("📖 使用说明")
        st.markdown("""
        1. 输入OpenAI API密钥
        2. 上传文档(.txt或.md)
        3. 点击"处理文档"按钮
        4. 在主界面输入问题
        """)
    
    # 主界面
    st.markdown('<h1 class="main-header">🤖 AI智能问答助手</h1>', unsafe_allow_html=True)
    st.markdown("基于LangChain和OpenAI的智能问答系统，支持多轮对话和知识检索")
    
    # 显示聊天历史
    display_chat_history()
    
    # 用户输入
    if prompt := st.chat_input("请输入你的问题..."):
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 生成回答
        if st.session_state.chain:
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    response = st.session_state.chain({"question": prompt})
                    answer = response["answer"]
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.warning("⚠️ 请先上传并处理文档")

if __name__ == "__main__":
    main()
