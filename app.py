"""
爆款视频内容复刻辅助工具 - 任务一：项目骨架与状态管理
=================================================
核心功能：
- Streamlit应用初始化
- 项目管理（创建、选择、删除）
- 会话状态管理
- API Key配置
"""

import streamlit as st
import json
import os
from datetime import datetime

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="爆款视频内容复刻工具",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 样式定制 - 潮酷年轻风 ====================
# 色彩系统：极夜黑 #0A0A0F | 霓虹粉 #FF2E63 | 电光蓝 #08D9D6 | 渐变紫 #7B2CBF
st.markdown("""
<style>
    /* ===== 字体引入 ===== */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    /* ===== 全局变量 ===== */
    :root {
        --bg-primary: #0A0A0F;
        --bg-secondary: #1A1A2E;
        --bg-card: #1A1A2E;
        --accent-pink: #FF2E63;
        --accent-cyan: #08D9D6;
        --accent-purple-start: #7B2CBF;
        --accent-purple-end: #E040FB;
        --text-primary: #EAEAEA;
        --text-secondary: #6C6C6C;
        --success: #00E676;
        --warning: #FFB300;
        --error: #FF5252;
        --border-subtle: rgba(255,255,255,0.08);
    }
    
    /* ===== 全局重置 ===== */
    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(255,46,99,0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(8,217,214,0.08) 0%, transparent 50%);
        color: var(--text-primary);
        font-family: 'Poppins', 'Source Han Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ===== 滚动条美化 ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--bg-secondary);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-cyan);
    }
    
    /* ===== 标题样式 ===== */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Poppins', 'Source Han Sans SC', sans-serif !important;
    }
    
    h1 {
        font-size: 42px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, var(--accent-pink) 0%, var(--accent-purple-end) 50%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    h3 {
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    
    /* ===== 主标题样式 ===== */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF2E63 0%, #E040FB 50%, #08D9D6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        animation: gradientFlow 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ===== 副标题样式 ===== */
    .subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* ===== 卡片样式 ===== */
    .card {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-subtle);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 300ms ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
        border-color: rgba(8,217,214,0.3);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px rgba(8,217,214,0.1);
    }
    
    /* ===== 成功提示样式 ===== */
    .success-box {
        background: rgba(0,230,118,0.1);
        border: 1px solid rgba(0,230,118,0.3);
        border-radius: 8px;
        padding: 1rem;
        color: var(--success);
    }
    
    /* ===== 警告提示样式 ===== */
    .warning-box {
        background: rgba(255,179,0,0.1);
        border: 1px solid rgba(255,179,0,0.3);
        border-radius: 8px;
        padding: 1rem;
        color: var(--warning);
    }
    
    /* ===== 信息提示样式 ===== */
    .info-box {
        background: rgba(64,196,255,0.1);
        border: 1px solid rgba(64,196,255,0.3);
        border-radius: 8px;
        padding: 1rem;
        color: #40C4FF;
    }
    
    /* ===== Streamlit组件美化 ===== */
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: #0F0F14 !important;
        border-right: 1px solid var(--border-subtle);
    }
    
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] .stSelectbox > label,
    [data-testid="stSidebar"] .stTextInput > label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
    }
    
    /* 按钮 */
    .stButton > button {
        background: linear-gradient(90deg, #FF2E63 0%, #FF6B9D 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        letter-spacing: 0.5px;
        transition: all 250ms ease;
        box-shadow: 0 4px 15px rgba(255,46,99,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,46,99,0.4);
        background: linear-gradient(90deg, #FF4D7A 0%, #FF7EAD 100%);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    .stButton > button[kind="secondary"] {
        background: transparent;
        border: 1px solid var(--accent-cyan);
        color: var(--accent-cyan);
        box-shadow: none;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(8,217,214,0.1);
    }
    
    /* 输入框 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #0A0A0F;
        border: 1px solid #2A2A3E;
        border-radius: 8px;
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        transition: all 250ms ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-cyan);
        box-shadow: 0 0 0 3px rgba(8,217,214,0.15), 0 0 20px rgba(8,217,214,0.2);
        outline: none;
    }
    
    /* 选择框 */
    .stSelectbox > div > div > div {
        background: #0A0A0F !important;
        border: 1px solid #2A2A3E !important;
        color: var(--text-primary) !important;
    }
    
    /* 文件上传器 */
    [data-testid="stFileUploader"] {
        background: var(--bg-card);
        border-radius: 16px;
        padding: 2rem;
        border: 2px dashed rgba(8,217,214,0.3);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-cyan);
        background: rgba(8,217,214,0.05);
    }
    
    /* 分割线 */
    hr {
        border-color: var(--border-subtle);
    }
    
    /* 标签/徽章 */
    .stBadge {
        background: rgba(255,46,99,0.15) !important;
        color: var(--accent-pink) !important;
        border-radius: 20px !important;
        padding: 4px 12px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }
    
    /* 进度条 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-pink), var(--accent-purple-end)) !important;
    }
    
    /* 标签页 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        color: var(--text-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--bg-card);
        color: var(--accent-cyan) !important;
        border-bottom: 2px solid var(--accent-cyan);
    }
    
    /* 警告框 */
    .stAlert {
        background: rgba(255,46,99,0.1);
        border: 1px solid rgba(255,46,99,0.3);
        border-radius: 8px;
        color: var(--text-primary);
    }
    
    /* 展开器 */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border-radius: 8px;
        color: var(--text-primary) !important;
    }
    
    /* 多列布局 */
    [data-testid="column"] {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid var(--border-subtle);
    }
    
    /* 表格 */
    .stDataFrame {
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
    }
    
    /* 底部隐藏元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== 动画效果 ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stMarkdown {
        animation: fadeIn 400ms ease forwards;
    }
    
    /* 加载骨架屏效果 */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .stSkeleton {
        background: linear-gradient(90deg, #1A1A2E 25%, #252536 50%, #1A1A2E 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 状态初始化 ====================
def init_session_state():
    """初始化所有会话状态变量"""
    
    # 项目管理
    if 'projects' not in st.session_state:
        st.session_state.projects = {}  # {project_id: {name, created_at, files: []}}
    
    if 'current_project_id' not in st.session_state:
        st.session_state.current_project_id = None
    
    # API配置
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    
    # 转写数据
    if 'transcripts' not in st.session_state:
        st.session_state.transcripts = {}  # {file_id: {name, text, duration, timestamp}}
    
    # 分析结果
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    
    # 脚本数据
    if 'script' not in st.session_state:
        st.session_state.script = None  # 结构化脚本
    
    # 对话历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 素材库
    if 'assets' not in st.session_state:
        st.session_state.assets = {}  # {segment_id: [asset_url, ...]}
    
    # 备注信息
    if 'notes' not in st.session_state:
        st.session_state.notes = {}  # {segment_id: note_text}
    
    # Pexels API
    if 'pexels_api_key' not in st.session_state:
        st.session_state.pexels_api_key = None


def create_project(name: str) -> str:
    """创建新项目"""
    project_id = f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    st.session_state.projects[project_id] = {
        'name': name,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'files': [],
        'transcripts': {},
        'analysis': None,
        'script': None,
        'chat_history': [],
        'assets': {},
        'notes': {}
    }
    
    st.session_state.current_project_id = project_id
    
    # 清空当前工作区数据
    st.session_state.transcripts = {}
    st.session_state.analysis = None
    st.session_state.script = None
    st.session_state.chat_history = []
    st.session_state.assets = {}
    st.session_state.notes = {}
    
    return project_id


def switch_project(project_id: str):
    """切换项目"""
    if project_id in st.session_state.projects:
        st.session_state.current_project_id = project_id
        
        # 加载项目数据到工作区
        project = st.session_state.projects[project_id]
        st.session_state.transcripts = project.get('transcripts', {})
        st.session_state.analysis = project.get('analysis')
        st.session_state.script = project.get('script')
        st.session_state.chat_history = project.get('chat_history', [])
        st.session_state.assets = project.get('assets', {})
        st.session_state.notes = project.get('notes', {})


def delete_project(project_id: str):
    """删除项目"""
    if project_id in st.session_state.projects:
        del st.session_state.projects[project_id]
        
        # 如果删除的是当前项目，切换到None
        if st.session_state.current_project_id == project_id:
            st.session_state.current_project_id = None
            st.session_state.transcripts = {}
            st.session_state.analysis = None
            st.session_state.script = None
            st.session_state.chat_history = []
            st.session_state.assets = {}
            st.session_state.notes = {}


def save_current_project():
    """保存当前项目状态"""
    if st.session_state.current_project_id:
        project_id = st.session_state.current_project_id
        st.session_state.projects[project_id].update({
            'transcripts': st.session_state.transcripts,
            'analysis': st.session_state.analysis,
            'script': st.session_state.script,
            'chat_history': st.session_state.chat_history,
            'assets': st.session_state.assets,
            'notes': st.session_state.notes
        })


# ==================== 侧边栏组件 ====================
def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("📁 项目管理")
        
        # 项目名称输入和创建
        st.subheader("新建项目")
        new_project_name = st.text_input(
            "项目名称",
            placeholder="输入项目名称...",
            key="new_project_name_input"
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("➕ 创建项目", use_container_width=True):
                if new_project_name.strip():
                    create_project(new_project_name.strip())
                    st.success(f"✅ 项目 '{new_project_name}' 创建成功！")
                else:
                    st.warning("请输入项目名称")
        
        st.divider()
        
        # 项目列表
        st.subheader("我的项目")
        
        if not st.session_state.projects:
            st.info("暂无项目，请先创建一个新项目")
        else:
            # 项目选择器
            project_options = ["选择项目..."] + [
                f"{pid}: {info['name']}" 
                for pid, info in st.session_state.projects.items()
            ]
            selected_project = st.selectbox(
                "选择项目",
                options=project_options,
                key="project_selector"
            )
            
            if selected_project != "选择项目...":
                project_id = selected_project.split(":")[0]
                switch_project(project_id)
                
                # 显示当前项目信息
                current_project = st.session_state.projects[project_id]
                st.markdown(f"""
                <div class="card">
                    <strong>📌 当前项目：{current_project['name']}</strong><br>
                    <small>创建时间：{current_project['created_at']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # 删除项目按钮
                if st.button("🗑️ 删除当前项目", use_container_width=True):
                    delete_project(project_id)
                    st.rerun()
        
        st.divider()
        
        # API配置
        st.subheader("⚙️ API配置")
        
        # 用户需要自己输入API密钥（不设默认值，保护用户隐私）
        api_key_input = st.text_input(
            "DMXAPI密钥",
            type="password",
            value="",
            placeholder="请输入您的DMXAPI密钥",
            help="请输入DMXAPI密钥，可在 https://dmxapi.cn 获取"
        )
        
        # 保存API密钥
        if st.button("💾 保存API密钥"):
            if api_key_input.strip():
                st.session_state.api_key = api_key_input.strip()
                st.success("✅ API密钥已保存！")
            else:
                st.warning("请输入API密钥")
        
        # 显示API状态
        if st.session_state.api_key:
            st.markdown('<div class="success-box">✅ API密钥已配置</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ 请配置API密钥</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Pexels API配置
        st.subheader("🖼️ Pexels图片搜索")
        
        # 默认Pexels API密钥（自动生效）
        default_pexels_key = "fdkmekFd4G6Jrc14xbrRTQ5jgDcfanZ8dCBQuCOMcUjrzp2VtxO0RU6G"
        
        # 如果session_state中没有，则使用默认值
        if st.session_state.pexels_api_key is None:
            st.session_state.pexels_api_key = default_pexels_key
        
        # 显示当前状态
        if st.session_state.pexels_api_key:
            st.markdown('<div class="success-box">✅ Pexels API密钥已配置</div>', unsafe_allow_html=True)
        
        pexels_api_key = st.text_input(
            "Pexels API密钥",
            type="password",
            value=st.session_state.pexels_api_key or "fdkmekFd4G6Jrc14xbrRTQ5jgDcfanZ8dCBQuCOMcUjrzp2VtxO0RU6G",
            placeholder="输入Pexels API密钥",
            key="pexels_api_key_input",
            help="用于搜索真实图片，可在 https://www.pexels.com/api/ 获取"
        )
        
        # 保存Pexels API密钥到session_state
        if st.button("💾 保存Pexels密钥"):
            if pexels_api_key:
                import requests
                try:
                    headers = {'Authorization': pexels_api_key}
                    test_response = requests.get('https://api.pexels.com/v1/search?query=test', headers=headers, timeout=5)
                    if test_response.status_code == 200:
                        st.session_state.pexels_api_key = pexels_api_key
                        st.success("✅ Pexels API密钥已保存！")
                    else:
                        st.error("⚠️ Pexels API密钥无效")
                except Exception as e:
                    st.error(f"⚠️ 验证失败: {str(e)}")
            else:
                st.warning("请输入Pexels API密钥")
        
        st.divider()
        
        # 使用说明
        with st.expander("📖 使用说明"):
            st.markdown("""
            **使用流程：**
            1. 创建或选择一个项目
            2. 上传参考视频/音频
            3. 分析爆款公式
            4. 输入新主题生成脚本
            5. 对话式修改脚本
            6. 获取素材推荐
            7. 导出项目
            """)


# ==================== 任务二：多文件上传与音视频转写 ====================

import base64
import io
import requests
import time

# DMXAPI配置
DMXAPI_BASE_URL = "https://www.dmxapi.cn/v1"


def get_dmxclient():
    """获取DMXAPI客户端"""
    if not st.session_state.api_key:
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=st.session_state.api_key,
            base_url=DMXAPI_BASE_URL
        )
        return client
    except Exception as e:
        st.error(f"API客户端初始化失败: {str(e)}")
        return None


def transcribe_audio(file_data: bytes, filename: str, client) -> dict:
    """使用DMXAPI Whisper转写音频（仅支持音频文件）"""
    try:
        import tempfile
        import os
        
        # 获取文件扩展名
        ext = filename.split('.')[-1].lower()
        
        # 检查是否为支持的音频格式
        audio_exts = ['mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg']
        if ext not in audio_exts:
            return {
                'success': False,
                'error': f"不支持的文件格式: {ext}。请上传MP3、WAV、M4A等音频文件。",
                'filename': filename
            }
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
            tmp.write(file_data)
            audio_path = tmp.name
        
        try:
            filename_only = os.path.basename(audio_path)
            
            # MIME类型映射
            mime_types = {
                'mp3': 'audio/mpeg',
                'wav': 'audio/wav',
                'm4a': 'audio/mp4',
                'flac': 'audio/flac',
                'aac': 'audio/aac',
                'ogg': 'audio/ogg'
            }
            mime_type = mime_types.get(ext, 'audio/mpeg')
            
            # 调用Whisper API转写
            url = f"{DMXAPI_BASE_URL}/audio/transcriptions"
            
            # DMXAPI支持的Whisper模型 - 只使用官方whisper-1模型
            model_options = [
                'whisper-1'  # 官方 Whisper 模型
            ]
            
            for model_name in model_options:
                try:
                    with open(audio_path, 'rb') as f:
                        files = {
                            'file': (filename_only, f, mime_type),
                            'model': (None, model_name)
                        }
                        headers = {'Authorization': f'Bearer {st.session_state.api_key}'}
                        response = requests.post(url, files=files, headers=headers, timeout=180)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"转写成功，使用模型: {model_name}")
                        return {'success': True, 'text': result.get('text', ''), 'filename': filename, 'model': model_name}
                    else:
                        # 直接返回错误信息
                        error_msg = response.text if response.text else f"HTTP {response.status_code}"
                        return {'success': False, 'error': f"API错误: {error_msg}", 'filename': filename}
                except Exception as e:
                    return {'success': False, 'error': str(e), 'filename': filename}
            
            return {'success': False, 'error': "转写失败，请检查API密钥是否正确", 'filename': filename}
                
        finally:
            try:
                os.unlink(audio_path)
            except:
                pass
            
    except Exception as e:
        return {'success': False, 'error': str(e), 'filename': filename}


def render_file_uploader():
    """渲染文件上传器"""
    st.subheader("📤 上传参考素材")


def render_file_uploader():
    """渲染文件上传器"""
    st.subheader("📤 上传参考素材")
    
    # 支持的文件类型 - 只支持音频文件，避免ffmpeg依赖
    accepted_types = [
        "audio/mpeg",      # .mp3
        "audio/wav",       # .wav
        "audio/mp4",      # .m4a
        "audio/x-m4a",    # .m4a
    ]
    
    uploaded_files = st.file_uploader(
        "选择音频文件（支持多个文件）",
        type=['mp3', 'wav', 'm4a'],
        accept_multiple_files=True,
        help="支持MP3、WAV、M4A音频格式。视频文件请先用其他工具转换为音频后再上传。"
    )
    
    if uploaded_files:
        st.markdown(f"**已选择 {len(uploaded_files)} 个文件**")
        
        # 显示文件列表
        for i, file in enumerate(uploaded_files):
            file_id = f"file_{i}_{file.name}"
            
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**📄 {file.name}**")
                st.markdown(f"<small>{file.size / 1024:.1f} KB</small>", unsafe_allow_html=True)
            with col2:
                # 检查是否已转写
                if file_id in st.session_state.transcripts:
                    st.success("✅ 已转写")
                else:
                    st.info("⏳ 待转写")
            with col3:
                # 删除文件按钮
                if st.button("🗑️", key=f"del_{file_id}"):
                    if file_id in st.session_state.transcripts:
                        del st.session_state.transcripts[file_id]
                    st.rerun()
        
        st.divider()
        
        # 转写按钮
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**点击下方按钮开始转写所有文件**")
        with col2:
            if st.button("🔄 全部转写", type="primary", use_container_width=True):
                if not st.session_state.api_key:
                    st.error("请先在侧边栏配置API密钥！")
                    return
                
                # 初始化客户端
                client = get_dmxclient()
                if not client:
                    st.error("API客户端初始化失败！")
                    return
                
                # 转写所有文件
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, file in enumerate(uploaded_files):
                    file_id = f"file_{i}_{file.name}"
                    
                    # 检查是否已转写
                    if file_id in st.session_state.transcripts:
                        continue
                    
                    status_text.text(f"正在转写: {file.name}...")
                    
                    # 读取文件内容
                    file_data = file.read()
                    
                    # 转写
                    result = transcribe_audio(file_data, file.name, client)
                    
                    if result['success']:
                        st.session_state.transcripts[file_id] = {
                            'name': result['filename'],
                            'text': result['text'],
                            'size': len(file_data),
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    else:
                        st.error(f"转写失败: {result['error']}")
                    
                    # 更新进度
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.text("转写完成！")
                time.sleep(0.5)
                status_text.empty()
                progress_bar.empty()
                
                st.rerun()
    
    return uploaded_files


def render_transcripts():
    """渲染转写结果"""
    if not st.session_state.transcripts:
        return
    
    st.subheader("📝 转写结果")
    
    # 统计信息
    total_files = len(st.session_state.transcripts)
    total_chars = sum(len(t['text']) for t in st.session_state.transcripts.values())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("文件数", total_files)
    with col2:
        st.metric("总字符数", f"{total_chars:,}")
    with col3:
        avg_chars = total_chars // total_files if total_files > 0 else 0
        st.metric("平均长度", f"{avg_chars:,} 字符")
    
    st.divider()
    
    # 显示每个转写结果
    for file_id, transcript in st.session_state.transcripts.items():
        with st.expander(f"📄 {transcript['name']}", expanded=False):
            st.markdown(f"**上传时间:** {transcript.get('timestamp', '未知')}")
            st.markdown(f"**字符数:** {len(transcript['text'])}")
            
            st.text_area(
                "转写内容",
                value=transcript['text'],
                height=200,
                key=f"transcript_{file_id}"
            )
            
            # 复制按钮
            if st.button(f"📋 复制内容", key=f"copy_{file_id}"):
                st.code(transcript['text'])


# ==================== 主区域组件 ====================
def render_main_area():
    """渲染主区域"""
    st.markdown('<p class="main-title">🎬 爆款视频内容复刻工具</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">上传视频/音频，分析爆款逻辑，生成你的专属脚本</p>', unsafe_allow_html=True)
    
    # 检查是否有选中的项目
    if not st.session_state.current_project_id:
        st.markdown("""
        <div class="info-box">
            <h3>👋 欢迎使用爆款视频内容复刻工具！</h3>
            <p>请按照以下步骤开始：</p>
            <ol>
                <li>在左侧侧边栏创建或选择一个项目</li>
                <li>上传参考视频/音频文件</li>
                <li>让AI分析爆款公式</li>
                <li>输入新主题生成脚本</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示功能介绍
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>📤</h3>
                <h4>上传素材</h4>
<p>支持多个视频/音频文件上传</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>🔍</h3>
                <h4>分析结构</h4>
                <p>提取爆款视频的核心逻辑</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>💬</h3>
                <h4>对话生成</h4>
                <p>像ChatGPT一样多轮修改</p>
            </div>
            """, unsafe_allow_html=True)
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>🎬</h3>
                <h4>素材推荐</h4>
                <p>AI推荐匹配的图片和视频</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>📝</h3>
                <h4>结构化输出</h4>
                <p>生成可直接使用的脚本</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3>📦</h3>
                <h4>导出项目</h4>
                <p>导出完整项目文件</p>
            </div>
            """, unsafe_allow_html=True)
        
        return False
    
    # ========== 有项目时显示主功能区 ==========
    
    # 使用步骤进度条组织功能
    # 定义4个步骤
    steps = [
        "📤 上传与转写",
        "🔍 分析爆款公式", 
        "💬 脚本生成",
        "📝 脚本与素材"
    ]
    
    # 初始化当前步骤
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    
    # 显示步骤进度条
    st.markdown("### 📊 创作进度")
    
    # 自定义步骤进度条样式
    step_labels = """
    <style>
    .step-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 10px;
    }
    .step-item {
        text-align: center;
        flex: 1;
        padding: 10px;
        border-radius: 8px;
    }
    .step-item.active {
        background: #6366f1;
        color: white;
    }
    .step-item.completed {
        background: #10b981;
        color: white;
    }
    .step-item.pending {
        background: #e5e7eb;
        color: #6b7280;
    }
    </style>
    """
    st.markdown(step_labels, unsafe_allow_html=True)
    
    # 渲染步骤指示器
    cols = st.columns(4)
    for i, step in enumerate(steps):
        with cols[i]:
            if i < st.session_state.current_step:
                st.markdown(f"✅ **{step}**")
            elif i == st.session_state.current_step:
                st.markdown(f"🔵 **{step}**")
            else:
                st.markdown(f"⚪ {step}")
    
    st.divider()
    
    # 根据当前步骤渲染对应内容
    if st.session_state.current_step == 0:
        # 步骤1：上传与转写
        render_file_uploader()
        render_transcripts()
        
        # 下一步按钮
        if st.session_state.transcripts:
            if st.button("下一步：分析爆款公式 →", type="primary"):
                st.session_state.current_step = 1
                st.rerun()
    
    elif st.session_state.current_step == 1:
        # 步骤2：分析爆款公式
        render_analysis_section()
        
        # 上下一步按钮
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← 上一步"):
                st.session_state.current_step = 0
                st.rerun()
        with col2:
            if st.session_state.analysis:
                if st.button("下一步：生成脚本 →", type="primary"):
                    st.session_state.current_step = 2
                    st.rerun()
    
    elif st.session_state.current_step == 2:
        # 步骤3：脚本生成
        render_script_generation_section()
        
        # 上下一步按钮
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← 上一步"):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.session_state.script:
                if st.button("下一步：脚本与素材 →", type="primary"):
                    st.session_state.current_step = 3
                    st.rerun()
    
    elif st.session_state.current_step == 3:
        # 步骤4：脚本与素材 - 折叠面板布局
        st.markdown("### 📝 脚本与素材")
        
        # 获取脚本
        script = st.session_state.script
        
        # 检查脚本是否存在
        if not script:
            st.warning("暂无脚本数据，请先在步骤3生成脚本")
            if st.button("← 返回生成脚本", type="primary"):
                st.session_state.current_step = 2
                st.rerun()
            return
        
        # 支持字典和文本两种格式
        if isinstance(script, dict) and 'segments' in script:
            # 字典格式：结构化脚本
            segments = script['segments']
            
            # 脚本基本信息
            if 'title' in script:
                st.markdown(f"**📌 脚本标题：**{script['title']}")
            if 'total_duration' in script:
                st.markdown(f"**⏱️ 总时长：**{script['total_duration']}")
            st.divider()
            
            # 脚本基本信息
            if 'title' in script:
                st.markdown(f"**📌 脚本标题：**{script['title']}")
            if 'total_duration' in script:
                st.markdown(f"**⏱️ 总时长：**{script['total_duration']}")
            st.divider()
            
            # 场景列表 - 使用st.expander提高性能
            st.markdown(f"**📋 场景列表（共{len(segments)}个）**")
            
            # 渲染场景（使用st.expander替代复杂HTML）
            for idx, seg in enumerate(segments):
                # 构建场景摘要
                duration = seg.get('duration', '')
                name = seg.get('name', f'场景{idx+1}')
                keywords = ', '.join(seg.get('keywords', [])[:3]) if seg.get('keywords') else ''
                summary = f"{name} | {duration} | 🏷️ {keywords}"
                
                # 使用expander替代复杂HTML卡片
                with st.expander(summary, expanded=False):
                    # 场景详细信息
                    st.markdown(f"**📹 场景{idx+1}: {name}**")
                    st.markdown(f"⏱️ **时长:** {duration}")
                    
                    if 'voiceover' in seg:
                        st.markdown("🎤 **画外音:**")
                        voiceover_text = seg['voiceover'][:500] + '...' if len(seg.get('voiceover', '')) > 500 else seg.get('voiceover', '')
                        st.text(voiceover_text)
                    
                    if 'visual_description' in seg:
                        st.markdown("🎬 **画面描述:**")
                        visual_text = seg['visual_description'][:500] + '...' if len(seg.get('visual_description', '')) > 500 else seg.get('visual_description', '')
                        st.text(visual_text)
                    
                    if 'keywords' in seg:
                        st.markdown(f"🏷️ **关键词:** {', '.join(seg['keywords'])}")
                    
                    st.divider()
                    
                    # 素材推荐面板
                    st.markdown("**📝 画面描述**")
                    custom_prompt = st.text_area(
                        "输入自定义描述（英文更佳）",
                        value=seg.get('visual_description', ''),
                        placeholder="例如：A beautiful sunset over the ocean...",
                        key=f"custom_prompt_{idx}",
                        height=60
                    )
                    
                    # AI生成和搜索
                    col_gen, col_search = st.columns(2)
                    
                    with col_gen:
                        st.markdown("**🎨 AI生成图片**")
                        gen_count = st.radio("数量", [1, 2], index=1, key=f"gen_count_{idx}", horizontal=True)
                        if st.button(f"🎨 生成{gen_count}张图片", key=f"gen_assets_{idx}", use_container_width=True):
                            if not st.session_state.api_key:
                                st.error("请先配置API密钥")
                            else:
                                client = get_dmxclient()
                                if client:
                                    # 使用用户自定义描述或默认描述
                                    prompt = custom_prompt or seg.get('visual_description', '')
                                    prompt = f"""{prompt}

要求：真实摄影风格，专业布光，8K超高清，电影感构图，主体明确，色彩和谐，无文字无水印"""
                                    
                                    with st.spinner("AI正在生成图片..."):
                                        result = generate_image(prompt, client, count=gen_count)
                                    
                                    if result['success']:
                                        urls = result.get('urls', [])
                                        if urls:
                                            if f"segment_{idx}" not in st.session_state.assets:
                                                st.session_state.assets[f"segment_{idx}"] = []
                                            for url_idx, url in enumerate(urls):
                                                st.session_state.assets[f"segment_{idx}"].append({
                                                    'type': 'ai_generated',
                                                    'url': url,
                                                    'model': 'DALL-E',
                                                    'index': url_idx + 1
                                                })
                                            st.success(f"✅ 生成{len(urls)}张图片！")
                                            st.rerun()
                                    else:
                                        st.error(f"生成失败: {result.get('error', '')}")
                    
                    with col_search:
                        st.markdown("**🔍 关键词搜索**")
                        search_keywords = ', '.join(seg.get('keywords', []))
                        search_input = st.text_input(
                            "搜索关键词",
                            value=search_keywords,
                            key=f"search_kw_{idx}",
                            placeholder="输入关键词搜索图片..."
                        )
                        if st.button("🔍 搜索Pexels", key=f"search_assets_{idx}", use_container_width=True):
                            if search_input.strip():
                                with st.spinner(f"正在搜索: {search_input}..."):
                                    result = search_images(search_input.strip(), per_page=5)
                                
                                if result['success']:
                                    images = result.get('images', [])
                                    if images:
                                        if f"segment_{idx}" not in st.session_state.assets:
                                            st.session_state.assets[f"segment_{idx}"] = []
                                        for img in images:
                                            st.session_state.assets[f"segment_{idx}"].append({
                                                'type': 'search',
                                                'url': img.get('url', ''),
                                                'thumbnail': img.get('thumbnail', ''),
                                                'source': img.get('source', ''),
                                                'photographer': img.get('photographer', ''),
                                                'license': img.get('license', '')
                                            })
                                        st.success(f"✅ 找到{len(images)}张图片！")
                                        st.rerun()
                                else:
                                    st.error(f"搜索失败: {result.get('error', '')}")
                            else:
                                st.warning("请输入搜索关键词")
                        
                        # 3. 已保存的素材
                        if f"segment_{idx}" in st.session_state.assets:
                            assets = st.session_state.assets[f"segment_{idx}"]
                            if assets:
                                st.markdown("**📁 已保存的素材**")
                                cols = st.columns(min(len(assets), 4))
                                for j, asset in enumerate(assets):
                                    with cols[j % 4]:
                                        st.image(asset.get('url', ''), width=120)
                                        asset_type = "🎨 AI" if asset.get('type') == 'ai_generated' else "🔍 搜索"
                                        st.caption(f"{asset_type} #{j+1}")
                        
                        st.markdown("---")
            
            # 批量操作提示
            st.info("💡 点击场景右侧的「素材推荐」按钮展开详细面板")
            
            # 返回按钮
            st.divider()
            if st.button("← 返回上一步"):
                st.session_state.current_step = 2
                st.rerun()
            
        elif isinstance(script, str):
            # 文本格式脚本：简单显示
            st.warning("当前脚本为文本格式，无法进行分段素材编辑")
            st.markdown("### 📝 脚本内容")
            with st.expander("查看脚本内容", expanded=True):
                st.markdown(script)
            
            st.info("💡 提示：建议重新生成结构化脚本以使用素材推荐功能")
            
            # 返回按钮
            st.divider()
            if st.button("← 返回上一步2"):
                st.session_state.current_step = 2
                st.rerun()
        
        else:
            st.warning("脚本格式不支持，请重新生成脚本")
        
        # 上一步按钮（备用）
        if st.button("← 返回上一步3"):
            st.session_state.current_step = 2
            st.rerun()
    
    return True


# ==================== 任务三：爆款公式提取与结构化分析 ====================

import json
from prompts import ANALYSIS_PROMPT, SCRIPT_OUTLINE_PROMPT, SCRIPT_GENERATION_PROMPT, SCRIPT_REVISION_PROMPT


def analyze_script(script_text: str, client) -> dict:
    """分析脚本，提取爆款公式"""
    try:
        # 构建提示词
        prompt = ANALYSIS_PROMPT.format(script=script_text)
        
        # 调用API - 优化：减少max_tokens加快速度
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "你是一位专业的短视频内容分析专家，擅长提取爆款视频的脚本结构和内容逻辑。请严格按照JSON格式输出分析结果。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000  # 优化：从4000减少到2000
        )
        
        # 解析结果
        result_text = response.choices[0].message.content
        
        # 尝试解析JSON
        try:
            # 尝试提取JSON部分
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            result = json.loads(result_text)
            return {'success': True, 'analysis': result}
        except json.JSONDecodeError:
            return {'success': True, 'analysis_text': result_text}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_analysis_section():
    """渲染爆款公式分析区域"""
    st.subheader("🔍 爆款公式分析")
    
    # 检查是否有转写内容
    if not st.session_state.transcripts:
        st.warning("请先上传并转写视频/音频文件")
        return
    
    # 合并所有转写内容
    combined_text = "\n\n".join([
        f"【{t['name']}】\n{t['text']}"
        for t in st.session_state.transcripts.values()
    ])
    
    # 显示合并后的文本预览
    with st.expander("📝 查看合并的转写内容", expanded=False):
        st.text(combined_text[:2000] + "..." if len(combined_text) > 2000 else combined_text)
    
    st.divider()
    
    # 分析按钮
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("点击下方按钮分析爆款公式")
    with col2:
        if st.button("🔍 分析爆款公式", type="primary", use_container_width=True):
            if not st.session_state.api_key:
                st.error("请先在侧边栏配置API密钥！")
                return
            
            client = get_dmxclient()
            if not client:
                st.error("API客户端初始化失败！")
                return
            
            # 执行分析
            with st.spinner("AI正在分析爆款公式..."):
                result = analyze_script(combined_text, client)
            
            if result['success']:
                st.session_state.analysis = result.get('analysis') or result.get('analysis_text')
                st.success("✅ 分析完成！")
                st.rerun()
            else:
                st.error(f"分析失败: {result.get('error', '未知错误')}")
    
    # 显示分析结果
    if st.session_state.analysis:
        st.divider()
        st.markdown("### 📊 分析结果")
        
        analysis = st.session_state.analysis
        
        # 判断是字典还是文本
        if isinstance(analysis, dict):
            # 钩子
            if 'hook' in analysis:
                with st.expander("🪝 钩子（Hook）", expanded=True):
                    hook = analysis['hook']
                    st.markdown(f"**描述:** {hook.get('description', '')}")
                    if hook.get('examples'):
                        st.markdown("**例子:**")
                        for ex in hook['examples']:
                            st.markdown(f"- {ex}")
                    if hook.get('technique'):
                        st.markdown(f"**技巧:** {hook['technique']}")
            
            # 痛点
            if 'pain_point' in analysis:
                with st.expander("😣 痛点（Pain Point）", expanded=True):
                    pain = analysis['pain_point']
                    st.markdown(f"**描述:** {pain.get('description', '')}")
                    if pain.get('target_audience'):
                        st.markdown(f"**目标受众:** {pain['target_audience']}")
                    if pain.get('examples'):
                        st.markdown("**例子:**")
                        for ex in pain['examples']:
                            st.markdown(f"- {ex}")
            
            # 解决方案
            if 'solution' in analysis:
                with st.expander("💡 解决方案", expanded=True):
                    sol = analysis['solution']
                    st.markdown(f"**描述:** {sol.get('description', '')}")
                    if sol.get('key_points'):
                        st.markdown("**关键卖点:**")
                        for pt in sol['key_points']:
                            st.markdown(f"- {pt}")
            
            # 价值主张
            if 'value_proposition' in analysis:
                with st.expander("⭐ 价值主张", expanded=True):
                    val = analysis['value_proposition']
                    st.markdown(f"**描述:** {val.get('description', '')}")
                    if val.get('benefits'):
                        st.markdown("**好处:**")
                        for b in val['benefits']:
                            st.markdown(f"- {b}")
            
            # CTA
            if 'cta' in analysis:
                with st.expander("👉 行动号召", expanded=True):
                    cta = analysis['cta']
                    st.markdown(f"**行动:** {cta.get('action', '')}")
                    if cta.get('timing'):
                        st.markdown(f"**时机:** {cta['timing']}")
            
            # 结构
            if 'structure' in analysis:
                with st.expander("📐 视频结构", expanded=True):
                    struct = analysis['structure']
                    if struct.get('total_duration'):
                        st.markdown(f"**总时长:** {struct['total_duration']}")
                    if struct.get('segments'):
                        st.markdown("**分段:**")
                        for seg in struct['segments']:
                            st.markdown(f"- **{seg.get('name', '')}**: {seg.get('duration', '')} - {seg.get('purpose', '')}")
            
            # 风格
            if 'style' in analysis:
                with st.expander("🎨 风格特点", expanded=True):
                    style = analysis['style']
                    if style.get('tone'):
                        st.markdown(f"**语气:** {style['tone']}")
                    if style.get('pacing'):
                        st.markdown(f"**节奏:** {style['pacing']}")
                    if style.get('keywords'):
                        st.markdown("**关键词:**")
                        cols = st.columns(3)
                        for i, kw in enumerate(style['keywords']):
                            with cols[i % 3]:
                                st.code(kw)
            
            # 病毒元素
            if 'viral_elements' in analysis:
                with st.expander("🔥 病毒传播元素", expanded=False):
                    viral = analysis['viral_elements']
                    if viral.get('emotion_trigger'):
                        st.markdown(f"**情感触发:** {viral['emotion_trigger']}")
                    if viral.get('curiosity_gap'):
                        st.markdown(f"**好奇心缺口:** {viral['curiosity_gap']}")
                    if viral.get('social_proof'):
                        st.markdown(f"**社会认同:** {viral['social_proof']}")
            
            # 复制分析结果按钮
            if st.button("📋 复制分析结果"):
                st.code(json.dumps(analysis, ensure_ascii=False, indent=2))
                st.success("已复制到剪贴板！")
        
        else:
            # 文本格式的结果
            with st.expander("📝 分析详情", expanded=True):
                st.markdown(analysis)
            
            if st.button("📋 复制分析结果"):
                st.code(analysis)
                st.success("已复制到剪贴板！")
        
        # 跳转到脚本生成
        st.divider()
        if st.button("🚀 基于此分析生成脚本", type="primary"):
            # 切换到脚本生成标签页
            st.session_state.active_tab = "💬 脚本生成"
            st.rerun()


# ==================== 任务四：对话式脚本生成与多轮修改 ====================

def generate_outline(analysis: dict, topic: str, extra_info: str, client) -> dict:
    """先生成脚本大纲"""
    try:
        if isinstance(analysis, dict):
            analysis_text = json.dumps(analysis, ensure_ascii=False, indent=2)
        else:
            analysis_text = str(analysis)
        
        prompt = SCRIPT_OUTLINE_PROMPT.format(
            analysis=analysis_text,
            topic=topic,
            extra_info=extra_info or "无"
        )
        
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "你是一位专业的短视频脚本架构师，擅长规划视频内容的叙事结构。请严格按照JSON格式输出脚本大纲。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000  # 优化：减少到1000
        )
        
        result_text = response.choices[0].message.content
        
        try:
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            outline = json.loads(result_text)
            return {'success': True, 'outline': outline}
        except json.JSONDecodeError:
            return {'success': True, 'outline_text': result_text}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def generate_script(analysis: dict, topic: str, extra_info: str, client) -> dict:
    """分步生成新脚本：先大纲，后脚本"""
    try:
        # 步骤1：先生成大纲
        outline_result = generate_outline(analysis, topic, extra_info, client)
        
        if not outline_result['success']:
            return {'success': False, 'error': f"大纲生成失败: {outline_result.get('error')}"}
        
        outline = outline_result.get('outline') or outline_result.get('outline_text')
        outline_text = json.dumps(outline, ensure_ascii=False, indent=2) if isinstance(outline, dict) else str(outline)
        
        # 步骤2：基于大纲生成完整脚本
        prompt = SCRIPT_GENERATION_PROMPT.format(
            outline=outline_text,
            topic=topic,
            extra_info=extra_info or "无"
        )
        
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "你是一位专业的短视频脚本写手，擅长创作能够引发传播的爆款内容。请严格按照JSON格式输出完整脚本。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000  # 恢复为4000避免脚本截断
        )
        
        # 解析结果
        result_text = response.choices[0].message.content
        
        # 尝试解析JSON
        try:
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            script = json.loads(result_text)
            return {'success': True, 'script': script}
        except json.JSONDecodeError:
            return {'success': True, 'script_text': result_text}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def revise_script(script: dict, revision_request: str, chat_history: list, client) -> dict:
    """修改脚本"""
    try:
        # 准备脚本内容
        script_text = json.dumps(script, ensure_ascii=False, indent=2)
        
        # 准备对话历史
        history_text = "\n".join([
            f"用户: {h.get('user', '')}\nAI: {h.get('assistant', '')}"
            for h in chat_history[-5:]  # 只取最近5轮
        ])
        
        # 构建提示词
        prompt = SCRIPT_REVISION_PROMPT.format(
            script=script_text,
            revision_request=revision_request,
            chat_history=history_text or "无"
        )
        
        # 调用API
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "你是一位专业的短视频脚本写手，正在与用户进行多轮对话修改脚本。请严格按照JSON格式输出修改后的脚本。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000  # 优化：从4000减少到2000
        )
        
        # 解析结果
        result_text = response.choices[0].message.content
        
        # 尝试解析JSON
        try:
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            new_script = json.loads(result_text)
            return {'success': True, 'script': new_script}
        except json.JSONDecodeError:
            return {'success': True, 'script_text': result_text}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def render_script_generation_section():
    """渲染脚本生成区域"""
    st.subheader("💬 脚本生成")
    
    # 检查是否有分析结果
    if not st.session_state.analysis:
        st.warning("请先完成「分析爆款公式」步骤")
        return
    
    # 初始化对话历史（如果需要新主题）
    if 'script_generation_started' not in st.session_state:
        st.session_state.script_generation_started = False
    
    # 左侧：对话区域
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💬 对话式修改")
        
        # 输入新主题
        if not st.session_state.script_generation_started:
            st.info("请输入新主题开始生成脚本")
            
            topic = st.text_input(
                "🎯 新主题",
                placeholder="例如：AI工具推荐、健康饮食、职场技巧...",
                key="new_topic_input"
            )
            
            extra_info = st.text_area(
                "📝 额外信息（可选）",
                placeholder="补充更多背景信息，如：目标受众、风格要求、内容重点等",
                key="extra_info_input",
                height=80
            )
            
            if st.button("🚀 开始生成脚本", type="primary", use_container_width=True):
                if not topic:
                    st.warning("请输入新主题")
                    return
                
                if not st.session_state.api_key:
                    st.error("请先在侧边栏配置API密钥！")
                    return
                
                client = get_dmxclient()
                if not client:
                    st.error("API客户端初始化失败！")
                    return
                
                # 生成脚本
                with st.spinner("AI正在生成脚本..."):
                    result = generate_script(
                        st.session_state.analysis,
                        topic,
                        extra_info,
                        client
                    )
                
                if result['success']:
                    script = result.get('script') or result.get('script_text')
                    st.session_state.script = script
                    st.session_state.script_generation_started = True
                    st.session_state.chat_history = []
                    st.success("✅ 脚本生成成功！")
                    st.rerun()
                else:
                    st.error(f"生成失败: {result.get('error', '未知错误')}")
        
        # 对话式修改
        if st.session_state.script_generation_started:
            st.markdown("---")
            st.markdown("**继续修改脚本：**")
            
            # 显示对话历史
            if st.session_state.chat_history:
                for i, msg in enumerate(st.session_state.chat_history):
                    with st.chat_message("user"):
                        st.markdown(msg.get('user', ''))
                    with st.chat_message("assistant"):
                        st.markdown(msg.get('assistant', ''))
            
            # 用户输入 - 使用text_input+button替代chat_input
            st.markdown("**💬 继续修改脚本：**")
            
            revision_request = st.text_input(
                "输入修改要求，如：'把钩子改得更吸引人'、'在第二段加入情感共鸣'...",
                key="revision_input",
                placeholder="输入修改意见..."
            )
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                send_btn = st.button("🚀 发送修改", type="primary", use_container_width=True)
            with col_btn2:
                clear_btn = st.button("🔄 重新开始", use_container_width=True)
            
            # 处理发送按钮
            if send_btn and revision_request and st.session_state.script:
                if not st.session_state.api_key:
                    st.error("请先在侧边栏配置API密钥！")
                    return
                
                client = get_dmxclient()
                if not client:
                    st.error("API客户端初始化失败！")
                    return
                
                # 记录用户消息
                st.session_state.chat_history.append({
                    'user': revision_request,
                    'assistant': ''
                })
                
                # 执行修改
                with st.spinner("AI正在修改脚本..."):
                    result = revise_script(
                        st.session_state.script,
                        revision_request,
                        st.session_state.chat_history,
                        client
                    )
                
                if result['success']:
                    script = result.get('script') or result.get('script_text')
                    st.session_state.script = script
                    # 更新对话历史
                    st.session_state.chat_history[-1]['assistant'] = "脚本已更新，请查看右侧预览"
                    st.rerun()
                else:
                    st.error(f"修改失败: {result.get('error', '未知错误')}")
                    # 移除失败的消息
                    st.session_state.chat_history.pop()
            
            # 处理重新开始按钮
            if clear_btn:
                st.session_state.script_generation_started = False
                st.session_state.script = None
                st.session_state.chat_history = []
                st.rerun()
    
    with col2:
        st.markdown("### 📝 脚本预览")
        
        # 显式检查是否是None
        if st.session_state.script is None:
            st.info("请先生成脚本，脚本将显示在这里")
            return
        
        script = st.session_state.script
        
        # 显示脚本内容 - 易读格式
        st.success("✅ 脚本已生成！")
        
        # 如果是字典格式，转换为易读的文本格式
        if isinstance(script, dict):
            # 提取关键信息显示
            if 'title' in script:
                st.markdown(f"## 📌 {script['title']}")
            
            if 'total_duration' in script:
                st.markdown(f"**⏱️ 总时长:** {script['total_duration']}")
            
            st.divider()
            
            # 显示每个分段
            if 'segments' in script:
                st.markdown("### 📋 脚本内容")
                for i, seg in enumerate(script['segments']):
                    st.markdown(f"**【{i+1}. {seg.get('name', '未命名')}】**")
                    if 'duration' in seg:
                        st.markdown(f"   ⏱️ 时长: {seg['duration']}")
                    if 'voiceover' in seg:
                        st.markdown(f"   🎤 画外音:\n   {seg['voiceover']}")
                    if 'visual_description' in seg:
                        st.markdown(f"   🎬 画面描述:\n   {seg['visual_description']}")
                    if 'keywords' in seg:
                        st.markdown(f"   🏷️ 关键词: {', '.join(seg['keywords'])}")
                    st.markdown("---")
            
            # CTA
            if 'cta' in script:
                st.markdown(f"👉 **行动号召:** {script['cta'].get('action', '')}")
            
            # 元数据
            if 'metadata' in script:
                meta = script['metadata']
                if 'target_audience' in meta:
                    st.markdown(f"👥 **目标受众:** {meta['target_audience']}")
                if 'tone' in meta:
                    st.markdown(f"🎨 **风格:** {meta['tone']}")
        else:
            # 文本格式直接显示
            st.text(script)
            content = str(script) if not isinstance(script, str) else script
            st.code(content, language="json")
        
        # 复制按钮
        import json
        if st.button("📋 复制完整脚本", use_container_width=True):
            if isinstance(script, dict):
                st.code(json.dumps(script, ensure_ascii=False, indent=2))
            else:
                st.code(script)
            st.success("已复制到剪贴板！")
        
        # 转换按钮
        if isinstance(script, dict):
            if st.button("📑 转换为制作表格", type="primary", use_container_width=True):
                st.session_state.show_script_table = True
                st.success("已保存到制作表格！")


# ==================== 任务五：结构化脚本表格与编辑 ====================

def render_script_table_section():
    """渲染结构化脚本表格"""
    st.subheader("📑 脚本制作表格")
    
    # 检查是否有脚本
    if not st.session_state.script:
        st.warning("请先在「脚本生成」标签页生成脚本")
        return
    
    script = st.session_state.script
    
    # 判断脚本格式
    if isinstance(script, dict) and 'segments' in script:
        segments = script['segments']
    else:
        st.error("脚本格式不支持表格编辑，请重新生成脚本")
        return
    
    # 转换为DataFrame格式用于编辑
    import pandas as pd
    
    # 准备数据
    table_data = []
    for i, seg in enumerate(segments):
        table_data.append({
            "序号": i + 1,
            "分段名称": seg.get('name', ''),
            "时长": seg.get('duration', ''),
            "画外音/台词": seg.get('voiceover', ''),
            "画面描述": seg.get('visual_description', ''),
            "关键词": ', '.join(seg.get('keywords', [])),
            "备注": st.session_state.notes.get(i, '')
        })
    
    # 创建可编辑的表格
    st.markdown("**👇 可编辑脚本表格（点击单元格即可编辑）：**")
    
    # 确保table_data是列表
    if not table_data:
        st.warning("暂无脚本数据")
        return
    
    edited_df = st.data_editor(
        table_data,
        num_rows="dynamic",
        use_container_width=True,
        height=400,
        key="script_table_editor"
    )
    
    # 确保edited_df是DataFrame类型
    import pandas as pd
    if not isinstance(edited_df, pd.DataFrame):
        st.warning("表格数据格式错误")
        return
    
    if edited_df.empty:
        st.warning("表格为空")
        return
    
    # 保存修改
    if st.button("💾 保存修改", type="primary"):
        # 更新备注
        for i, row in edited_df.iterrows():
            st.session_state.notes[i] = row.get('备注', '')
        
        # 更新脚本
        for i, row in edited_df.iterrows():
            if i < len(segments):
                segments[i]['name'] = row.get('分段名称', '')
                segments[i]['duration'] = row.get('时长', '')
                segments[i]['voiceover'] = row.get('画外音/台词', '')
                segments[i]['visual_description'] = row.get('画面描述', '')
                segments[i]['keywords'] = [k.strip() for k in row.get('关键词', '').split(',') if k.strip()]
        
        st.session_state.script['segments'] = segments
        st.success("✅ 修改已保存！")
    
    # 统计信息
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("分段数", len(edited_df))
    with col2:
        total_chars = sum(len(str(row.get('画外音/台词', ''))) for _, row in edited_df.iterrows())
        st.metric("总字符数", f"{total_chars:,}")
    with col3:
        # 估算时长
        st.metric("预估时长", "~60秒")


# ==================== 任务六：混合素材搜索与AI生成 ====================

# Pexels API配置（预填用户提供的密钥）
PEXELS_API_KEY = "fdkmekFd4G6Jrc14xbrRTQ5jgDcfanZ8dCBQuCOMcUjrzp2VtxO0RU6G"


def generate_image(prompt: str, client, count: int = 2) -> dict:
    """使用AI模型生成图片 - 优化版
    
    Args:
        prompt: 图片描述
        client: OpenAI客户端
        count: 需要生成的图片数量（默认2张）
        
    Returns:
        dict: {'success': True, 'urls': [...]}
    """
    import concurrent.futures
    
    # 优化提示词 - 更详细、更具体，提高匹配度
    enhanced_prompt = f"""{prompt}

详细要求：
- 真实摄影风格，画面逼真自然
- 专业布光，光影层次分明
- 8K超高清，细节丰富
- 电影感构图，视觉冲击力强
- 无文字、无水印、无logo
- 干净简洁，适合作为视频素材
- 主体明确，色彩和谐"""
    
    # 定义模型列表（按优先级排序）
    # 单图模型需要并发多次请求，支持多图的模型可以一次性请求
    SINGLE_IMAGE_MODELS = ['dall-e-3']  # 只支持n=1的模型
    MULTI_IMAGE_MODELS = ['dall-e-2', 'seedream-3.0']  # 支持n>1的模型
    
    def call_api_with_retry(model: str, prompt: str, n: int = 1, retries: int = 1):
        """调用API，带重试机制（优化：减少重试次数）"""
        for attempt in range(retries):
            try:
                # DALL-E 3 使用 hd 质量更高
                quality = "hd" if model == "dall-e-3" else "standard"
                
                response = client.images.generate(
                    model=model,
                    prompt=prompt,
                    size="1024x1024",
                    quality=quality,
                    n=n
                )
                urls = [img.url for img in response.data]
                return {'success': True, 'urls': urls, 'model': model}
            except Exception as e:
                error_msg = str(e)
                # 检查是否是n值错误
                if 'n_not_within_range' in error_msg or 'invalid value of n' in error_msg:
                    # 这个模型不支持多图
                    if model in SINGLE_IMAGE_MODELS:
                        return {'success': False, 'error': f'{model}仅支持单张生成', 'retry': False}
                    raise
                # 检查是否是渠道不可用
                if '无可用渠道' in error_msg or '503' in error_msg:
                    if attempt < retries - 1:
                        continue
                raise
        return {'success': False, 'error': '重试次数用尽'}
    
    # 策略1：直接使用DALL-E 3（最稳定），并发请求
    try:
        # 并发生成多张图片
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(count, 4)) as executor:
            futures = [
                executor.submit(call_api_with_retry, 'dall-e-3', enhanced_prompt, 1)
                for _ in range(count)
            ]
            
            all_urls = []
            success_count = 0
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result['success']:
                    all_urls.extend(result['urls'])
                    success_count += 1
            
            if all_urls:
                return {'success': True, 'urls': all_urls, 'model': 'dall-e-3'}
    except Exception as e:
        pass
    
    # 所有方案都失败
    return {
        'success': False,
        'error': '图片生成服务暂时不可用，请稍后重试或使用搜索功能获取素材'
    }


def search_images(keywords: str, per_page: int = 5) -> dict:
    """智能搜索图片 - 支持自定义关键词搜索，返回前5条结果"""
    
    # 使用session_state中的Pexels API key
    pexels_key = st.session_state.get('pexels_api_key')
    
    if not pexels_key:
        return {'success': False, 'error': '请在侧边栏配置Pexels API密钥（免费获取：https://www.pexels.com/api/）'}
    
    # 优先使用Pexels API
    if pexels_key:
        try:
            import requests
            
            headers = {
                'Authorization': pexels_key
            }
            
            params = {
                'query': keywords,
                'per_page': per_page,
                'orientation': 'landscape'
            }
            
            response = requests.get(
                'https://api.pexels.com/v1/search',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get('photos', [])
                
                images = []
                for photo in photos[:per_page]:  # 限制返回前5条
                    images.append({
                        'url': photo['src']['large'],
                        'thumbnail': photo['src']['medium'],
                        'photographer': photo.get('photographer', 'Unknown'),
                        'photographer_url': photo.get('photographer_url', ''),
                        'source': 'Pexels',
                        'license': 'Free to use',  # Pexels免费商用许可
                        'alt': photo.get('alt', keywords)
                    })
                
                return {
                    'success': True,
                    'images': images,
                    'total_results': data.get('total_results', 0)
                }
        except Exception as e:
            pass
    
    # 如果没有Pexels API，尝试使用Unsplash API
    UNSPLASH_ACCESS_KEY = None
    if UNSPLASH_ACCESS_KEY:
        try:
            import requests
            
            headers = {
                'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
            }
            
            params = {
                'query': keywords,
                'per_page': per_page,
                'orientation': 'landscape'
            }
            
            response = requests.get(
                'https://api.unsplash.com/search/photos',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                images = []
                for photo in results[:per_page]:  # 限制返回前5条
                    images.append({
                        'url': photo['urls']['regular'],
                        'thumbnail': photo['urls']['thumb'],
                        'photographer': photo.get('user', {}).get('name', 'Unknown'),
                        'photographer_url': photo.get('user', {}).get('links', {}).get('html', ''),
                        'source': 'Unsplash',
                        'license': 'Unsplash License - Free to use',  # Unsplash免费商用许可
                        'alt': photo.get('alt_description', keywords)
                    })
                
                return {
                    'success': True,
                    'images': images,
                    'total_results': data.get('total_results', 0)
                }
        except Exception as e:
            pass
    
    # 如果都没有配置，返回提示信息
    return {
        'success': False,
        'error': '请在侧边栏配置Pexels API密钥（免费获取：https://www.pexels.com/api/）',
        'images': []
    }


def render_assets_section():
    """渲染素材推荐区域 - 支持自定义关键词搜索"""
    st.subheader("🎬 素材推荐")
    
    # 检查是否有脚本
    if not st.session_state.script:
        st.warning("请先生成脚本")
        return
    
    script = st.session_state.script
    
    if isinstance(script, dict) and 'segments' in script:
        segments = script['segments']
    else:
        st.error("脚本格式不支持素材推荐")
        return
    
    st.markdown("**为每个脚本分段推荐/生成素材：**")
    
    # 为每个分段生成/搜索素材
    for i, seg in enumerate(segments):
        with st.expander(f"分段 {i+1}: {seg.get('name', '未命名')}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**画外音：** {seg.get('voiceover', '')[:100]}...")
                st.markdown(f"**画面描述：** {seg.get('visual_description', '')}")
                if seg.get('keywords'):
                    st.markdown(f"**关键词：** {', '.join(seg.get('keywords', []))}")
            
            with col2:
                # 生成图片按钮 - 生成4张图片
                if st.button(f"🎨 AI生成4张图片 (即梦3.0)", key=f"gen_img_{i}", use_container_width=True):
                    if not st.session_state.api_key:
                        st.error("请先配置API密钥")
                        return
                    
                    client = get_dmxclient()
                    if not client:
                        st.error("API客户端初始化失败")
                        return
                    
                    # 构建提示词
                    visual_desc = seg.get('visual_description', '')
                    prompt = f"高质量摄影风格图片：{visual_desc}，专业布光，电影感画面"
                    
                    with st.spinner("AI正在生成4张图片（使用即梦3.0）..."):
                        result = generate_image(prompt, client)
                    
                    if result['success']:
                        urls = result.get('urls', [])
                        
                        # 显示4张图片（2x2网格）
                        st.markdown("**🎨 生成结果（点击选择一张）：**")
                        
                        # 初始化选中状态
                        if f"selected_img_{i}" not in st.session_state:
                            st.session_state[f"selected_img_{i}"] = None
                        
                        cols = st.columns(2)
                        for idx, url in enumerate(urls):
                            with cols[idx % 2]:
                                # 检查是否被选中
                                is_selected = st.session_state[f"selected_img_{i}"] == idx
                                
                                # 显示图片
                                if is_selected:
                                    st.image(url, caption=f"✅ 已选中 #{idx+1}", use_container_width=True)
                                else:
                                    st.image(url, caption=f"图片 #{idx+1}", use_container_width=True)
                                
                                # 选择按钮
                                if st.button(f"选择第{idx+1}张", key=f"select_{i}_{idx}"):
                                    st.session_state[f"selected_img_{i}"] = idx
                                    # 保存选中的图片到素材库
                                    if f"segment_{i}" not in st.session_state.assets:
                                        st.session_state.assets[f"segment_{i}"] = []
                                    st.session_state.assets[f"segment_{i}"].append({
                                        'type': 'ai_generated',
                                        'url': url,
                                        'model': '即梦3.0',
                                        'index': idx + 1
                                    })
                                    st.success(f"已选择第{idx+1}张图片！")
                                    st.rerun()
                        
                        st.info("💡 点击上方按钮选择一张图片保存到素材库")
                    else:
                        st.error(f"生成失败: {result.get('error', '')}")
            
            # 自定义关键词搜索
            st.markdown("---")
            st.markdown("**🔍 自定义搜索：**")
            
            # 默认关键词
            default_keywords = ', '.join(seg.get('keywords', []))
            
            # 关键词输入框
            search_keywords = st.text_input(
                "输入搜索关键词",
                value=default_keywords,
                placeholder="例如：风景、城市、人物、科技",
                key=f"search_keywords_{i}"
            )
            
            # 搜索按钮
            if st.button(f"🔎 执行搜索", key=f"do_search_{i}", use_container_width=True):
                if not search_keywords.strip():
                    st.warning("请输入搜索关键词")
                else:
                    with st.spinner(f"正在搜索：{search_keywords} ..."):
                        result = search_images(search_keywords, per_page=5)  # 限制返回前5条
                    
                    if result['success']:
                        images = result.get('images', [])
                        if images:
                            # 显示搜索结果（带版权信息）
                            st.markdown(f"**📸 搜索结果（前{len(images)}条）：**")
                            
                            for j, img in enumerate(images):
                                with st.container():
                                    col_img, col_info = st.columns([3, 1])
                                    
                                    with col_img:
                                        # 显示缩略图
                                        thumbnail_url = img.get('thumbnail', img.get('url'))
                                        st.image(thumbnail_url, caption=f"结果 {j+1}", use_container_width=True)
                                    
                                    with col_info:
                                        # 显示版权和许可信息
                                        st.markdown("**素材信息：**")
                                        st.markdown(f"📷 **摄影师：** {img.get('photographer', 'Unknown')}")
                                        st.markdown(f"🌐 **来源：** {img.get('source', 'Unknown')}")
                                        st.markdown(f"📜 **许可：** {img.get('license', 'Unknown')}")
                                        
                                        # 保存到素材库按钮
                                        if st.button(f"💾 保存", key=f"save_{i}_{j}", use_container_width=True):
                                            if f"segment_{i}" not in st.session_state.assets:
                                                st.session_state.assets[f"segment_{i}"] = []
                                            st.session_state.assets[f"segment_{i}"].append({
                                                'type': 'search',
                                                'url': img['url'],
                                                'thumbnail': img.get('thumbnail', ''),
                                                'source': img.get('source', ''),
                                                'photographer': img.get('photographer', ''),
                                                'license': img.get('license', ''),
                                                'keywords': search_keywords
                                            })
                                            st.success("已保存到素材库！")
                                    
                                    st.markdown("---")
                            
                            st.success(f"✅ 搜索完成，找到 {len(images)} 张图片")
                        else:
                            st.warning("未找到相关图片，请尝试其他关键词")
                    else:
                        # 显示错误信息
                        error_msg = result.get('error', '未知错误')
                        st.error(f"搜索失败: {error_msg}")
                        if 'Pexels API密钥' in error_msg:
                            st.info("💡 请在侧边栏配置Pexels API密钥（免费获取：https://www.pexels.com/api/）")
            
            st.divider()
            
            # 显示已保存的素材
            if f"segment_{i}" in st.session_state.assets:
                st.markdown("**📁 已保存的素材库：**")
                assets = st.session_state.assets[f"segment_{i}"]
                
                if assets:
                    cols = st.columns(min(len(assets), 3))
                    for j, asset in enumerate(assets):
                        with cols[j % 3]:
                            st.image(asset['url'], width=150)
                            # 显示素材来源和版权信息
                            asset_type = asset.get('type', '素材')
                            source = asset.get('source', '')
                            license_info = asset.get('license', '')
                            if asset_type == 'ai_generated':
                                st.caption(f"🎨 AI生成 #{j+1}")
                            else:
                                st.caption(f"🔍 {source} #{j+1}")
                            if license_info:
                                st.caption(f"📜 {license_info}")
                else:
                    st.info("暂无保存的素材")


# ==================== 任务七：素材标注、导出与项目保存 ====================

def render_export_section():
    """渲染导出区域"""
    st.subheader("📦 导出项目")
    
    # 检查是否有数据
    if not st.session_state.script and not st.session_state.analysis:
        st.warning("没有可导出的数据，请先生成脚本")
        return
    
    # 导出选项
    st.markdown("### 选择导出格式")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 导出CSV
        if st.button("📊 导出CSV", use_container_width=True):
            if st.session_state.script and isinstance(st.session_state.script, dict):
                import pandas as pd
                
                segments = st.session_state.script.get('segments', [])
                table_data = []
                for i, seg in enumerate(segments):
                    table_data.append({
                        "序号": i + 1,
                        "分段名称": seg.get('name', ''),
                        "时长": seg.get('duration', ''),
                        "画外音": seg.get('voiceover', ''),
                        "画面描述": seg.get('visual_description', ''),
                        "关键词": ', '.join(seg.get('keywords', [])),
                        "备注": st.session_state.notes.get(i, '')
                    })
                
                df = pd.DataFrame(table_data)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                
                st.download_button(
                    label="💾 下载CSV",
                    data=csv,
                    file_name="video_script.csv",
                    mime="text/csv"
                )
    
    with col2:
        # 导出JSON
        if st.button("📋 导出JSON", use_container_width=True):
            export_data = {
                'project_name': st.session_state.projects.get(st.session_state.current_project_id, {}).get('name', '未命名'),
                'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'analysis': st.session_state.analysis,
                'script': st.session_state.script,
                'assets': st.session_state.assets,
                'notes': st.session_state.notes
            }
            
            json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
            
            st.download_button(
                label="💾 下载JSON",
                data=json_str,
                file_name="video_project.json",
                mime="application/json"
            )
    
    # 项目概览
    st.divider()
    st.markdown("### 📋 项目概览")
    
    project = st.session_state.projects.get(st.session_state.current_project_id, {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("项目名称", project.get('name', '-'))
    with col2:
        st.metric("已转写文件", len(st.session_state.transcripts))
    with col3:
        if st.session_state.script and isinstance(st.session_state.script, dict):
            segments = st.session_state.script.get('segments', [])
            st.metric("脚本分段", len(segments))
        else:
            st.metric("脚本分段", 0)
    with col4:
        st.metric("素材数量", sum(len(v) for v in st.session_state.assets.values()))
    
    # 预览
    if st.session_state.script:
        with st.expander("📝 脚本预览", expanded=False):
            st.json(st.session_state.script)


# ==================== 主程序 ====================
def main():
    """主函数"""
    # 初始化状态
    init_session_state()
    
    # 渲染侧边栏
    render_sidebar()
    
    # 渲染主区域
    has_project = render_main_area()
    
    # 自动保存项目状态
    if has_project:
        save_current_project()


if __name__ == "__main__":
    main()
