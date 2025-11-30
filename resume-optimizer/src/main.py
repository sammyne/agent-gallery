import streamlit as st
import os
from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex

from dotenv import load_dotenv
import tempfile
import shutil
import base64
# from PyPDF2 import PdfReader

import model

# 加载环境变量
load_dotenv()


def run_rag_completion(
    documents,
    query_text: str,
    job_title: str,
    job_description: str,
    embedding_model: str,
    generative_model: str,
) -> str:
    """Run RAG completion using Nebius models for resume optimization."""
    llm = model.must_new_openai_like(generative_model)
    embed_model = model.must_new_openai_like_embedding(embedding_model)

    Settings.llm = llm
    Settings.embed_model = embed_model

    # Step 1: Analyze the resume
    analysis_prompt = f"""
    详细分析这份简历。重点关注：
    1. 关键技能和专业能力
    2. 工作经验和成就
    3. 教育背景和认证
    4. 重要项目或成就
    5. 职业发展轨迹和空缺期
    
    请以要点形式提供简洁的分析。
    """

    index = VectorStoreIndex.from_documents(documents)
    resume_analysis = index.as_query_engine(similarity_top_k=5).query(
        analysis_prompt
    )

    # Step 2: Generate optimization suggestions
    optimization_prompt = f"""
    基于简历分析和职位要求，提供具体、可操作的改进建议。
    
    简历分析：
    {resume_analysis}
    
    职位名称：{job_title}
    职位描述：{job_description}
    
    优化请求：{query_text}
    
    请严格按照以下格式提供直接、结构化的回应：

    ## 主要发现
    • [2-3个要点，突出主要匹配度和差距]

    ## 具体改进
    • [3-5个要点，提供具体建议]
    • 每个要点应以强有力的动作动词开头
    • 尽可能包含具体示例

    ## 行动项目
    • [2-3个具体的、立即可以执行的步骤]
    • 每个项目应清晰明确且可实施

    保持所有要点简洁且可操作。不要包含任何思考过程或分析。
    """

    optimization_suggestions = index.as_query_engine(similarity_top_k=5).query(
        optimization_prompt
    )

    return str(optimization_suggestions)


def display_pdf_preview(pdf_file):
    """Display PDF preview in the sidebar."""
    try:
        st.sidebar.subheader("Resume Preview")
        base64_pdf = base64.b64encode(pdf_file.getvalue()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
        st.sidebar.markdown(pdf_display, unsafe_allow_html=True)
        return True
    except Exception as e:
        st.sidebar.error(f"Error previewing PDF: {str(e)}")
        return False


def main():
    st.set_page_config(page_title="Resume Optimizer", layout="wide")

    # Initialize session states
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "docs_loaded" not in st.session_state:
        st.session_state.docs_loaded = False
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = None
    if "current_pdf" not in st.session_state:
        st.session_state.current_pdf = None

    # Header
    st.title("📝 简历优化器")
    # st.caption("Powered by Nebius AI")

    # Sidebar for configuration
    with st.sidebar:
        # st.image("./Nebius.png", width=150)

        # Model selection
        generative_model = st.selectbox(
            "大模型", ["qwen3-max","qwen3-max-2025-09-23", "deepseek-v3.2-exp"], index=0
        )

        # 向量化模型选择
        embedding_model = st.selectbox(
            "文本向量模型", ["text-embedding-v4", "text-embedding-v2"], index=0
        )

        st.divider()

        st.subheader("上传简历")
        uploaded_file = st.file_uploader(
            "选择你的简历（PDF）", type="pdf", accept_multiple_files=False
        )

        # PDF 上传和处理
        if uploaded_file is not None:
            if uploaded_file != st.session_state.current_pdf:
                st.session_state.current_pdf = uploaded_file
                try:
                    # if not os.getenv("NEBIUS_API_KEY"):
                    #     st.error("Missing Nebius API key")
                    #     st.stop()

                    # 创建存储 PDF 的临时目录
                    if st.session_state.temp_dir:
                        shutil.rmtree(st.session_state.temp_dir)
                    st.session_state.temp_dir = tempfile.mkdtemp()

                    # 将上传的 pdf 保存到临时目录
                    file_path = os.path.join(
                        st.session_state.temp_dir, uploaded_file.name
                    )
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    with st.spinner("简历加载中 ..."):
                        documents = SimpleDirectoryReader(
                            st.session_state.temp_dir
                        ).load_data()
                        st.session_state.docs_loaded = True
                        st.session_state.documents = documents
                        st.success("✓ 简历加载成功")
                        display_pdf_preview(uploaded_file)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("职位信息")
        job_title = st.text_input("职位名称")
        job_description = st.text_area("职位描述", height=200)

        st.subheader("优化选项")
        optimization_type = st.selectbox(
            "选择优化类型",
            [
                # ATS 全称申请人跟踪系统（Applicant Tracking System）在筛选简历时重点关注的技能、经验或资格等核心词汇。
                "ATS关键词优化器",
                "经验部分增强",
                "技能层次创建器",
                "专业摘要撰写器",
                "教育优化",
                "技术技能展示",
                "职业空档期润色",
            ],
        )

        if st.button("优化简历"):
            if not st.session_state.docs_loaded:
                st.error("请先上传你的简历")
                st.stop()
            if not job_title or not job_description:
                st.error("请提供职位名称和职位描述")
                st.stop()

            # 优化类型对应的生成优化提示词
            prompts = {
                "ATS关键词优化器": "识别并优化ATS关键词。重点关注职位描述中的精确匹配和语义变体。",
                "经验部分增强": "增强经验部分以符合职位要求。重点关注可量化的成就。",
                "技能层次创建": "根据职位要求组织技能。识别差距和发展机会。",
                "专业摘要撰写": "创建针对性的专业摘要，突出相关经验和技能。",
                "教育优化": "优化教育部分，强调与该职位相关的资格。",
                "技术技能展示": "根据职位要求组织技术技能。突出关键能力。",
                "职业空档期润色": "专业地处理职业空档期。关注成长和相关经验。",
            }

            with st.spinner("分析简历并生成建议中..."):
                try:
                    response = run_rag_completion(
                        st.session_state.documents,
                        prompts[optimization_type],
                        job_title,
                        job_description,
                        embedding_model,
                        generative_model,
                    )
                    # Remove think tags from response
                    response = response.replace("<think>", "").replace("</think>", "")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

            st.divider()

    with col2:
        st.subheader("优化结果")
        for message in st.session_state.messages:
            st.markdown(message["content"])


if __name__ == "__main__":
    main()
