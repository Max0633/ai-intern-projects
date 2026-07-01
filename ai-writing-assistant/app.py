# -*- coding: utf-8 -*-
"""
AI写作助手工具 - 主应用文件
支持文章生成、润色、翻译、格式优化
"""

import os
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="AI写作助手",
    page_icon="✍️",
    layout="wide"
)

# 自定义样式
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #ff6b6b;
    text-align: center;
    margin-bottom: 2rem;
}
.tool-card {
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid #ddd;
    margin-bottom: 1rem;
    background-color: #f8f9fa;
}
.active-tool {
    border: 2px solid #ff6b6b;
    background-color: #fff5f5;
}
</style>
""", unsafe_allow_html=True)

# 写作工具定义
WRITING_TOOLS = {
    "article_generator": {
        "name": "📝 文章生成",
        "description": "根据主题和要求生成完整文章",
        "icon": "📝"
    },
    "content_polisher": {
        "name": "✨ 内容润色",
        "description": "优化文章表达，提升可读性",
        "icon": "✨"
    },
    "translator": {
        "name": "🌐 翻译助手",
        "description": "中英文互译，保持原意",
        "icon": "🌐"
    },
    "format_optimizer": {
        "name": "📋 格式优化",
        "description": "优化文章结构和格式",
        "icon": "📋"
    },
    "title_generator": {
        "name": "💡 标题生成",
        "description": "生成吸引人的文章标题",
        "icon": "💡"
    },
    "summary_generator": {
        "name": "📊 摘要生成",
        "description": "生成文章摘要和要点",
        "icon": "📊"
    }
}

def init_session_state():
    """初始化会话状态"""
    if "current_tool" not in st.session_state:
        st.session_state.current_tool = "article_generator"
    if "history" not in st.session_state:
        st.session_state.history = []

def get_openai_client():
    """获取OpenAI客户端"""
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return OpenAI(api_key=api_key)
    return None

def generate_content(prompt, system_message, max_tokens=2000):
    """使用AI生成内容"""
    client = get_openai_client()
    if not client:
        return "请先配置OpenAI API密钥"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"生成失败: {str(e)}"

def article_generator_ui():
    """文章生成界面"""
    st.header("📝 文章生成")
    st.markdown("根据主题和要求，AI将为你生成完整的文章")
    
    with st.form("article_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("文章主题", placeholder="例如：人工智能的未来发展")
            word_count = st.slider("目标字数", 500, 3000, 1000, step=100)
        
        with col2:
            style = st.selectbox("写作风格", [
                "学术论文", "新闻报道", "博客文章", 
                "产品介绍", "技术文档", "创意写作"
            ])
            tone = st.selectbox("语气", [
                "正式", "轻松", "专业", "幽默", "感性"
            ])
        
        requirements = st.text_area(
            "特殊要求",
            placeholder="例如：需要包含具体案例、数据支持等"
        )
        
        submitted = st.form_submit_button("生成文章", type="primary")
        
        if submitted and topic:
            system_message = f"""你是一个专业的写作助手。请根据以下要求生成文章：
- 主题: {topic}
- 风格: {style}
- 语气: {tone}
- 字数: 约{word_count}字
- 特殊要求: {requirements if requirements else '无'}

请确保文章结构清晰，内容丰富，逻辑连贯。"""
            
            with st.spinner("正在生成文章..."):
                result = generate_content(topic, system_message, max_tokens=3000)
                st.session_state.history.append({
                    "tool": "文章生成",
                    "input": topic,
                    "output": result,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.markdown(result)

def content_polisher_ui():
    """内容润色界面"""
    st.header("✨ 内容润色")
    st.markdown("优化你的文章表达，提升可读性和专业性")
    
    with st.form("polish_form"):
        original_text = st.text_area(
            "请输入需要润色的内容",
            height=200,
            placeholder="粘贴你的文章内容..."
        )
        
        polish_type = st.multiselect("润色选项", [
            "语法检查", "表达优化", "逻辑调整", 
            "专业术语", "可读性提升"
        ], default=["语法检查", "表达优化"])
        
        submitted = st.form_submit_button("开始润色", type="primary")
        
        if submitted and original_text:
            system_message = f"""你是一个专业的文字润色专家。请对以下内容进行润色：
- 润色重点: {', '.join(polish_type)}
- 保持原意，提升表达质量
- 使文章更加流畅和专业

请输出润色后的内容，并简要说明改进之处。"""
            
            with st.spinner("正在润色内容..."):
                result = generate_content(original_text, system_message)
                st.session_state.history.append({
                    "tool": "内容润色",
                    "input": original_text[:100] + "...",
                    "output": result,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("原文")
                    st.text_area("原文", original_text, height=200, disabled=True)
                with col2:
                    st.subheader("润色后")
                    st.text_area("润色后", result, height=200, disabled=True)

def translator_ui():
    """翻译助手界面"""
    st.header("🌐 翻译助手")
    st.markdown("高质量中英文互译，保持原意和风格")
    
    with st.form("translate_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox("源语言", ["中文", "英文"])
        
        with col2:
            target_lang = st.selectbox("目标语言", ["英文", "中文"])
        
        source_text = st.text_area(
            "请输入需要翻译的内容",
            height=150,
            placeholder="粘贴你的文本..."
        )
        
        submitted = st.form_submit_button("开始翻译", type="primary")
        
        if submitted and source_text:
            system_message = f"""你是一个专业的翻译专家。请将以下{source_lang}翻译成{target_lang}：
- 保持原文意思和风格
- 使用自然流畅的表达
- 注意专业术语的准确翻译

请输出翻译结果。"""
            
            with st.spinner("正在翻译..."):
                result = generate_content(source_text, system_message)
                st.session_state.history.append({
                    "tool": "翻译助手",
                    "input": f"{source_lang} -> {target_lang}",
                    "output": result,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.markdown(result)

def format_optimizer_ui():
    """格式优化界面"""
    st.header("📋 格式优化")
    st.markdown("优化文章结构，提升可读性")
    
    with st.form("format_form"):
        content = st.text_area(
            "请输入需要优化格式的内容",
            height=200
        )
        
        format_options = st.multiselect("优化选项", [
            "添加标题层级", "段落分隔", "列表格式化",
            "重点突出", "添加引用"
        ], default=["段落分隔", "重点突出"])
        
        submitted = st.form_submit_button("优化格式", type="primary")
        
        if submitted and content:
            system_message = f"""你是一个格式优化专家。请对以下内容进行格式优化：
- 优化选项: {', '.join(format_options)}
- 使用Markdown格式
- 使结构清晰，易于阅读

请输出优化后的内容。"""
            
            with st.spinner("正在优化格式..."):
                result = generate_content(content, system_message)
                st.session_state.history.append({
                    "tool": "格式优化",
                    "input": content[:100] + "...",
                    "output": result,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.markdown(result)

def title_generator_ui():
    """标题生成界面"""
    st.header("💡 标题生成")
    st.markdown("为你的文章生成吸引人的标题")
    
    with st.form("title_form"):
        content_preview = st.text_area(
            "请输入文章内容预览",
            height=100,
            placeholder="简要描述文章内容..."
        )
        
        title_count = st.slider("生成标题数量", 3, 10, 5)
        title_style = st.selectbox("标题风格", [
            "专业正式", "吸引眼球", "疑问式", 
            "数字列表式", "创意新颖"
        ])
        
        submitted = st.form_submit_button("生成标题", type="primary")
        
        if submitted and content_preview:
            system_message = f"""你是一个标题创作专家。请根据文章内容生成{title_count}个标题：
- 风格: {title_style}
- 要求: 吸引人、准确、简洁

请列出生成的标题，并简要说明每个标题的特点。"""
            
            with st.spinner("正在生成标题..."):
                result = generate_content(content_preview, system_message)
                st.session_state.history.append({
                    "tool": "标题生成",
                    "input": content_preview[:100],
                    "output": result,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.markdown(result)

def summary_generator_ui():
    """摘要生成界面"""
    st.header("📊 摘要生成")
    st.markdown("快速生成文章摘要和要点")
    
    with st.form("summary_form"):
        article_content = st.text_area(
            "请输入文章内容",
            height=200
        )
        
        summary_length = st.selectbox("摘要长度", [
            "一句话摘要", "简短摘要(100字)", 
            "标准摘要(200字)", "详细摘要(300字)"
        ])
        
        include_keywords = st.checkbox("包含关键词提取", value=True)
        
        submitted = st.form_submit_button("生成摘要", type="primary")
        
        if submitted and article_content:
            system_message = f"""你是一个摘要生成专家。请为以下文章生成摘要：
- 长度: {summary_length}
- 是否提取关键词: {'是' if include_keywords else '否'}

请输出摘要内容。"""
            
            with st.spinner("正在生成摘要..."):
                result = generate_content(article_content, system_message)
                st.session_state.history.append({
                    "tool": "摘要生成",
                    "input": article_content[:100] + "...",
                    "output": result,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.markdown(result)

def show_history():
    """显示使用历史"""
    st.header("📚 使用历史")
    
    if not st.session_state.history:
        st.info("暂无使用记录")
        return
    
    for i, record in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{record['tool']} - {record['time']}"):
            st.write(f"**输入**: {record['input']}")
            st.markdown(f"**输出**:\n{record['output']}")

def main():
    """主函数"""
    init_session_state()
    
    # 侧边栏
    with st.sidebar:
        st.header("🔧 写作工具")
        
        # API密钥
        api_key = st.text_input(
            "OpenAI API密钥:",
            type="password"
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        st.divider()
        
        # 工具选择
        for tool_key, tool_info in WRITING_TOOLS.items():
            if st.button(
                f"{tool_info['icon']} {tool_info['name']}", 
                key=tool_key,
                use_container_width=True
            ):
                st.session_state.current_tool = tool_key
        
        st.divider()
        
        # 使用统计
        st.header("📊 使用统计")
        st.write(f"总使用次数: {len(st.session_state.history)}")
        
        if st.button("查看历史"):
            st.session_state.show_history = True
    
    # 主界面
    st.markdown('<h1 class="main-header">✍️ AI写作助手</h1>', unsafe_allow_html=True)
    
    # 工具说明
    tool_info = WRITING_TOOLS.get(st.session_state.current_tool, {})
    st.markdown(f"### {tool_info.get('name', '')} - {tool_info.get('description', '')}")
    
    # 显示对应工具界面
    tool_ui_map = {
        "article_generator": article_generator_ui,
        "content_polisher": content_polisher_ui,
        "translator": translator_ui,
        "format_optimizer": format_optimizer_ui,
        "title_generator": title_generator_ui,
        "summary_generator": summary_generator_ui
    }
    
    if st.session_state.current_tool in tool_ui_map:
        tool_ui_map[st.session_state.current_tool]()
    
    # 显示历史
    if hasattr(st.session_state, 'show_history') and st.session_state.show_history:
        show_history()

if __name__ == "__main__":
    main()
