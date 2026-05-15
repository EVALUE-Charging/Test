import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# 頁面設定
st.set_page_config(
    page_title="充電站拓點評估系統",
    page_icon="⚡",
    layout="wide"
)

# ==================== 深色模式檢測和主題配色定義 ====================
def get_dark_mode_detection_css():
    """添加深色模式檢測的 CSS"""
    return """
    <script>
    // 檢測深色模式
    function detectDarkMode() {
        const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const streamlitElement = document.querySelector('.stApp');
        if (isDarkMode) {
            streamlitElement.classList.add('dark-mode');
        } else {
            streamlitElement.classList.add('light-mode');
        }
        
        // 監聽深色模式變化
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                streamlitElement.classList.toggle('dark-mode', e.matches);
                streamlitElement.classList.toggle('light-mode', !e.matches);
            });
        }
    }
    
    // 頁面載入時執行檢測
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', detectDarkMode);
    } else {
        detectDarkMode();
    }
    </script>
    """

THEMES = {
    "經典藍": {
        "primary": "#1E90FF",
        "secondary": "#20B2AA",
        "success": "#32CD32",
        "warning": "#FFA500",
        "danger": "#FF4500",
        "accent1": "#87CEEB",
        "accent2": "#20B2AA",
        "color": "#1E90FF",
        "name": "經典藍"
    },
    "商務灰": {
        "primary": "#2C3E50",
        "secondary": "#34495E",
        "success": "#27AE60",
        "warning": "#F39C12",
        "danger": "#E74C3C",
        "accent1": "#95A5A6",
        "accent2": "#7F8C8D",
        "color": "#2C3E50",
        "name": "商務灰"
    },
    "科技紫": {
        "primary": "#9370DB",
        "secondary": "#8A2BE2",
        "success": "#00CED1",
        "warning": "#FFD700",
        "danger": "#DC143C",
        "accent1": "#DDA0DD",
        "accent2": "#BA55D3",
        "color": "#9370DB",
        "name": "科技紫"
    },
    "自然綠": {
        "primary": "#2ECC71",
        "secondary": "#16A085",
        "success": "#27AE60",
        "warning": "#F39C12",
        "danger": "#E74C3C",
        "accent1": "#1ABC9C",
        "accent2": "#3498DB",
        "color": "#2ECC71",
        "name": "自然綠"
    },
    "活力橙": {
        "primary": "#FF6B35",
        "secondary": "#F7931E",
        "success": "#4ECDC4",
        "warning": "#FFE66D",
        "danger": "#C0392B",
        "accent1": "#FFA07A",
        "accent2": "#FF8C42",
        "color": "#FF6B35",
        "name": "活力橙"
    },
    "甜美粉": {
        "primary": "#FFB6C1",
        "secondary": "#FF69B4",
        "success": "#32CD32",
        "warning": "#FFA500",
        "danger": "#FF1493",
        "accent1": "#FFC0CB",
        "accent2": "#FF69B4",
        "color": "#FFB6C1",
        "name": "甜美粉"
    }
}

def get_theme_css(theme):
    """根據選擇的主題生成對應的 CSS，支援深色模式"""
    colors = THEMES[theme]
    
    return f"""
{get_dark_mode_detection_css()}

<style>
    /* 全局樣式 - 根據模式調整 */
    .stApp {{
        transition: background-color 0.3s ease, color 0.3s ease;
    }}
    
    /* 淺色模式 */
    .stApp.light-mode {{
        background-color: #F5F5F5;
        color: #333333;
    }}
    
    /* 深色模式 */
    .stApp.dark-mode {{
        background-color: #1E1E1E;
        color: #E0E0E0;
    }}
    
    /* 主標題樣式 - 適配深色模式 */
    .stApp h1 {{
        color: {colors['primary']} !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }}
    
    .stApp.dark-mode h1 {{
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }}
    
    .stApp h2, .stApp h3 {{
        font-weight: 600 !important;
        transition: color 0.3s ease;
    }}
    
    .stApp.light-mode h2, 
    .stApp.light-mode h3 {{
        color: #333333 !important;
    }}
    
    .stApp.dark-mode h2, 
    .stApp.dark-mode h3 {{
        color: #E0E0E0 !important;
    }}
    
    /* 側邊欄樣式 */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {colors['primary']} 0%, {colors['secondary']} 100%);
    }}
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stTickBarMin"],
    [data-testid="stSidebar"] [data-testid="stTickBarMax"] {{
        color: white !important;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.3);
    }}
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
        font-weight: 600 !important;
    }}
    
    /* 指標卡片 - 適配深色模式 */
    [data-testid="stMetric"] {{
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid {colors['primary']};
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .stApp.light-mode [data-testid="stMetric"] {{
        background: white;
    }}
    
    .stApp.dark-mode [data-testid="stMetric"] {{
        background: #2D2D2D;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: color 0.3s ease;
    }}
    
    .stApp.light-mode [data-testid="stMetricLabel"] {{
        color: #888888 !important;
    }}
    
    .stApp.dark-mode [data-testid="stMetricLabel"] {{
        color: #B0B0B0 !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {colors['primary']} !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}
    
    /* 按鈕樣式 */
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 144, 255, 0.4);
    }}
    
    .stApp.dark-mode .stButton > button {{
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}
    
    /* 分頁樣式 - 適配深色模式 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        padding: 0.5rem;
        border-radius: 10px;
        transition: background-color 0.3s ease;
    }}
    
    .stApp.light-mode .stTabs [data-baseweb="tab-list"] {{
        background-color: white;
    }}
    
    .stApp.dark-mode .stTabs [data-baseweb="tab-list"] {{
        background-color: #2D2D2D;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .stApp.light-mode .stTabs [data-baseweb="tab"] {{
        background-color: #F5F5F5;
        color: #333333;
    }}
    
    .stApp.dark-mode .stTabs [data-baseweb="tab"] {{
        background-color: #404040;
        color: #E0E0E0;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%) !important;
        color: white !important;
    }}
    
    /* 自定義指標卡片 - 適配深色模式 */
    .metric-card, .metric-card-success, .metric-card-warning, .metric-card-danger {{
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .stApp.light-mode .metric-card,
    .stApp.light-mode .metric-card-success,
    .stApp.light-mode .metric-card-warning,
    .stApp.light-mode .metric-card-danger {{
        background: white;
    }}
    
    .stApp.dark-mode .metric-card,
    .stApp.dark-mode .metric-card-success,
    .stApp.dark-mode .metric-card-warning,
    .stApp.dark-mode .metric-card-danger {{
        background: #2D2D2D;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    }}
    
    .metric-card {{
        border-top: 4px solid {colors['primary']};
    }}
    
    .metric-card-success {{
        border-top: 4px solid {colors['success']};
    }}
    
    .metric-card-warning {{
        border-top: 4px solid {colors['warning']};
    }}
    
    .metric-card-danger {{
        border-top: 4px solid {colors['danger']};
    }}
    
    .big-metric {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }}
    
    .metric-label {{
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
        transition: color 0.3s ease;
    }}
    
    .stApp.light-mode .metric-label {{
        color: #888888;
    }}
    
    .stApp.dark-mode .metric-label {{
        color: #B0B0B0;
    }}
    
    /* 警告框 - 適配深色模式 */
    .stAlert {{
        border-radius: 10px;
        border-left: 4px solid {colors['primary']};
        transition: background-color 0.3s ease;
    }}
    
    .stApp.dark-mode .stAlert {{
        background-color: #2D2D2D !important;
        color: #E0E0E0 !important;
    }}
    
    /* 展開器 - 適配深色模式 */
    .streamlit-expanderHeader {{
        border-radius: 8px;
        font-weight: 600;
        transition: background-color 0.3s ease, color 0.3s ease;
    }}
    
    .stApp.light-mode .streamlit-expanderHeader {{
        background-color: white;
        color: #333333;
    }}
    
    .stApp.dark-mode .streamlit-expanderHeader {{
        background-color: #2D2D2D;
        color: #E0E0E0;
    }}
    
    /* 輸入框 - 適配深色模式 */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        border-radius: 8px;
        border: 2px solid #E0E0E0;
        transition: all 0.3s ease;
    }}
    
    .stApp.light-mode .stTextInput > div > div > input,
    .stApp.light-mode .stNumberInput > div > div > input {{
        background-color: white;
        color: #333333;
    }}
    
    .stApp.dark-mode .stTextInput > div > div > input,
    .stApp.dark-mode .stNumberInput > div > div > input {{
        background-color: #2D2D2D !important;
        color: #E0E0E0 !important;
        border-color: #404040 !important;
    }}
    
    .stApp.light-mode .stSelectbox > div > div {{
        background-color: white;
    }}
    
    .stApp.dark-mode .stSelectbox > div > div {{
        background-color: #2D2D2D;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {colors['primary']} !important;
        box-shadow: 0 0 0 2px rgba(30, 144, 255, 0.2) !important;
    }}
    
    /* 選擇框標籤 - 適配深色模式 */
    .stSelectbox > label,
    .stTextInput > label,
    .stNumberInput > label {{
        transition: color 0.3s ease;
    }}
    
    .stApp.light-mode .stSelectbox > label,
    .stApp.light-mode .stTextInput > label,
    .stApp.light-mode .stNumberInput > label {{
        color: #333333 !important;
    }}
    
    .stApp.dark-mode .stSelectbox > label,
    .stApp.dark-mode .stTextInput > label,
    .stApp.dark-mode .stNumberInput > label {{
        color: #E0E0E0 !important;
    }}
    
    /* 滑桿 - 適配深色模式 */
    .stSlider > div > div > div > div {{
        background-color: {colors['primary']} !important;
    }}
    
    /* 登出按鈕 */
    .logout-button > button {{
        background: linear-gradient(135deg, {colors['danger']} 0%, {colors['warning']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }}
    
    /* Radio 按鈕 - 適配深色模式 */
    .stRadio > div > label > div > p {{
        transition: color 0.3s ease;
    }}
    
    .stApp.light-mode .stRadio > div > label > div > p {{
        color: #333333 !important;
    }}
    
    .stApp.dark-mode .stRadio > div > label > div > p {{
        color: #E0E0E0 !important;
    }}
    
    /* 數據框 - 適配深色模式 */
    .stApp.dark-mode .stDataFrame {{
        background-color: #2D2D2D;
    }}
    
    .stApp.dark-mode .stDataFrame [data-testid="stTable"] {{
        background-color: #2D2D2D;
    }}
    
    /* 成功/資訊/警告/錯誤訊息 - 適配深色模式 */
    .stApp.dark-mode .stSuccess,
    .stApp.dark-mode .stInfo,
    .stApp.dark-mode .stWarning,
    .stApp.dark-mode .stError {{
        background-color: #2D2D2D !important;
        color: #E0E0E0 !important;
    }}
    
    /* Caption 文字 - 適配深色模式 */
    .stApp.dark-mode .stCaption {{
        color: #B0B0B0 !important;
    }}
    
    /* 展開器內容 - 適配深色模式 */
    .stApp.dark-mode .streamlit-expanderContent {{
        background-color: #1E1E1E !important;
        border-color: #404040 !important;
    }}
    
    /* 滑桿標籤和數值 - 適配深色模式 */
    .stApp.dark-mode .stSlider > label {{
        color: #E0E0E0 !important;
    }}
    
    .stApp.dark-mode [data-testid="stTickBarMin"],
    .stApp.dark-mode [data-testid="stTickBarMax"] {{
        color: #B0B0B0 !important;
    }}
    
    /* 主題選擇器下拉選單 - 適配深色模式 */
    .stApp.dark-mode .stSelectbox [data-baseweb="select"] {{
        background-color: #2D2D2D !important;
        color: #E0E0E0 !important;
        border-color: #404040 !important;
    }}
    
    /* 數字輸入框按鈕 - 適配深色模式 */
    .stApp.dark-mode .stNumberInput > div > div > button {{
        background-color: #404040 !important;
        color: #E0E0E0 !important;
        border-color: #404040 !important;
    }}
</style>
"""

# ==================== 登入驗證功能 ====================
def check_login():
    """檢查登入狀態"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in

def login_page():
    """登入頁面 - 適配深色模式"""
    st.markdown(f"""
    {get_dark_mode_detection_css()}
    <style>
        .stApp {{
            background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
            transition: all 0.3s ease;
        }}
        
        .stApp.dark-mode {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        }}
        
        .login-container {{
            max-width: 450px;
            margin: 80px auto;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stApp.light-mode .login-container {{
            background: white;
        }}
        
        .stApp.dark-mode .login-container {{
            background: #2D2D2D;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        
        .login-title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            transition: color 0.3s ease;
        }}
        
        .stApp.light-mode .login-title {{
            color: #2C3E50;
        }}
        
        .stApp.dark-mode .login-title {{
            color: #E0E0E0;
        }}
        
        .login-subtitle {{
            text-align: center;
            font-size: 1rem;
            margin-bottom: 2rem;
            transition: color 0.3s ease;
        }}
        
        .stApp.light-mode .login-subtitle {{
            color: #7F8C8D;
        }}
        
        .stApp.dark-mode .login-subtitle {{
            color: #B0B0B0;
        }}
        
        .login-icon {{
            text-align: center;
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        
        /* 登入頁面輸入框樣式優化 */
        .stTextInput > div > div > input {{
            border: 2px solid #E0E0E0 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }}
        
        .stApp.light-mode .stTextInput > div > div > input {{
            background-color: #F8F9FA !important;
            color: #2C3E50 !important;
        }}
        
        .stApp.dark-mode .stTextInput > div > div > input {{
            background-color: #404040 !important;
            color: #E0E0E0 !important;
            border-color: #555555 !important;
        }}
        
        .stTextInput > div > div > input::placeholder {{
            transition: color 0.3s ease;
        }}
        
        .stApp.light-mode .stTextInput > div > div > input::placeholder {{
            color: #95A5A6 !important;
        }}
        
        .stApp.dark-mode .stTextInput > div > div > input::placeholder {{
            color: #888888 !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: #3498DB !important;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2) !important;
        }}
        
        /* 登入頁面標籤文字 */
        .stTextInput > label {{
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            transition: color 0.3s ease;
        }}
        
        .stApp.light-mode .stTextInput > label {{
            color: #2C3E50 !important;
        }}
        
        .stApp.dark-mode .stTextInput > label {{
            color: #E0E0E0 !important;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-icon">⚡</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: white; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">充電站拓點評估系統</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #BDC3C7; font-size: 1rem; margin-bottom: 2.5rem;">Electric Vehicle Charging Analysis Platform</p>', unsafe_allow_html=True)
        
        # 帳號標籤 - 白色文字
        st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem; font-size: 1rem;">帳號</p>', unsafe_allow_html=True)
        username = st.text_input("帳號", placeholder="請輸入帳號", label_visibility="collapsed", key="username_input")
        
        # 密碼標籤 - 白色文字
        st.markdown('<p style="color: white; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1.2rem; font-size: 1rem;">密碼</p>', unsafe_allow_html=True)
        password = st.text_input("密碼", type="password", placeholder="請輸入密碼", label_visibility="collapsed", key="password_input")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1, 1])
        with col_b:
            login_button = st.button("🔐 登入", use_container_width=True, type="primary", key="login_button")
        
        if login_button:
            if username == "EVALUE" and password == "EVALUE2025":
                st.session_state.logged_in = True
                st.success("✅ 登入成功！")
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤")

def logout():
    """登出功能"""
    st.session_state.logged_in = False
    st.rerun()

# ==================== 主程式 ====================

if not check_login():
    login_page()
    st.stop()

# 初始化主題
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "商務灰"

# 自定義 CSS - 根據選擇的主題
st.markdown(get_theme_css(st.session_state.current_theme), unsafe_allow_html=True)

# 載入資料函數
@st.cache_data
def load_station_data():
    try:
        for encoding in ['utf-8', 'utf-8-sig', 'big5', 'gbk', 'cp950']:
            try:
                df = pd.read_csv('data/stations.csv', encoding=encoding)
                break
            except (FileNotFoundError, UnicodeDecodeError):
                continue
        else:
            st.error("❌ 找不到充電站資料檔案")
            return pd.DataFrame()
        
        column_mapping = {
            '站ID': 'station_id', '名稱': 'name', '經度': 'longitude', '緯度': 'latitude',
            '充電槍數': 'charger_count', '啟用日期': 'installation_date', '負責人': 'manager',
            '站點規格': 'station_type', 'AC槍數量': 'ac_count', 'DC槍數量': 'dc_count',
            '槍頭規格': 'connector_type', '區域屬性': 'area_type', '站點屬性': 'location_type',
            '縣市': 'city', '標案性質': 'project_type'
        }
        
        df = df.rename(columns=column_mapping)
        required_columns = ['station_id', 'name', 'latitude', 'longitude', 'charger_count']
        if not all(col in df.columns for col in required_columns):
            return pd.DataFrame()
        
        if 'address' not in df.columns:
            if 'area_type' in df.columns and 'location_type' in df.columns:
                df['address'] = df['area_type'].fillna('').astype(str) + ' - ' + df['location_type'].fillna('').astype(str)
            else:
                df['address'] = df['name']
        
        df = df.dropna(subset=['latitude', 'longitude'])
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude'])
        
        for col in ['charger_count', 'ac_count', 'dc_count']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"❌ 讀取資料時發生錯誤: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_usage_data():
    try:
        for encoding in ['utf-8', 'utf-8-sig', 'big5', 'gbk', 'cp950']:
            try:
                df = pd.read_csv('data/usedata.csv', encoding=encoding)
                break
            except (FileNotFoundError, UnicodeDecodeError):
                continue
        else:
            return pd.DataFrame()
        df['Avg_Degree_Per_Day'] = pd.to_numeric(df['Avg_Degree_Per_Day'], errors='coerce')
        return df
    except:
        return pd.DataFrame()

@st.cache_data
def calculate_utilization_rate(_stations_df, _usage_df, ac_capacity=7, dc_capacity=30):
    if _usage_df.empty or _stations_df.empty:
        return pd.DataFrame()
    
    merged = _usage_df.merge(
        _stations_df[['station_id', 'ac_count', 'dc_count', 'installation_date']], 
        left_on='Station', right_on='station_id', how='left'
    )
    
    if 'installation_date' in merged.columns:
        merged['installation_date'] = pd.to_datetime(
            merged['installation_date'], format='mixed', dayfirst=False, errors='coerce'
        )
    
    def calc_rate(row):
        if pd.isna(row['Avg_Degree_Per_Day']):
            return None
        
        try:
            year = int(row['Quarter'].split('-')[0])
            quarter_num = int(row['Quarter'].split('-Q')[1])
            quarter_start_month = (quarter_num - 1) * 3 + 1
            quarter_start = pd.Timestamp(year=year, month=quarter_start_month, day=1)
            
            if quarter_num == 4:
                quarter_end = pd.Timestamp(year=year, month=12, day=31)
            else:
                next_quarter_start = pd.Timestamp(year=year, month=quarter_start_month + 3, day=1)
                quarter_end = next_quarter_start - pd.Timedelta(days=1)
            
            quarter_days = (quarter_end - quarter_start).days + 1
            actual_days = quarter_days
            
            if pd.notna(row.get('installation_date')):
                install_date = pd.Timestamp(row['installation_date'])
                if quarter_start <= install_date <= quarter_end:
                    actual_days = (quarter_end - install_date).days + 1
        except:
            quarter_days = 91
            actual_days = 91
        
        adjusted_avg = (row['Avg_Degree_Per_Day'] * quarter_days) / actual_days
        
        if row['ChargerType'] == 'AC':
            return adjusted_avg / (row['ac_count'] * ac_capacity) if row['ac_count'] > 0 else None
        elif row['ChargerType'] == 'DC':
            return adjusted_avg / (row['dc_count'] * dc_capacity) if row['dc_count'] > 0 else None
        return None
    
    merged['utilization_rate'] = merged.apply(calc_rate, axis=1)
    return merged

@st.cache_data
def calculate_quarterly_utilization(_utilization_df, station_ids, ac_capacity, dc_capacity):
    """計算季度稼動率，加入參數作為快取鍵"""
    if _utilization_df.empty or not station_ids:
        return pd.DataFrame()
    
    filtered = _utilization_df[_utilization_df['Station'].isin(station_ids)].copy()
    if filtered.empty:
        return pd.DataFrame()
    
    quarterly = filtered.groupby(['Quarter', 'ChargerType'])['utilization_rate'].mean().reset_index()
    quarterly = quarterly.sort_values('Quarter')
    pivot_table = quarterly.pivot(index='Quarter', columns='ChargerType', values='utilization_rate').reset_index()
    pivot_table.columns.name = None
    
    pivot_table['Year'] = pivot_table['Quarter'].str[:4]
    
    agg_dict = {}
    if 'AC' in pivot_table.columns:
        agg_dict['AC'] = 'mean'
    if 'DC' in pivot_table.columns:
        agg_dict['DC'] = 'mean'
    
    if agg_dict:
        yearly_avg = pivot_table.groupby('Year').agg(agg_dict).reset_index()
        
        if 'AC' in yearly_avg.columns:
            yearly_avg['AC年成長率'] = yearly_avg['AC'].pct_change() * 100
        if 'DC' in yearly_avg.columns:
            yearly_avg['DC年成長率'] = yearly_avg['DC'].pct_change() * 100
        
        merge_cols = ['Year']
        if 'AC年成長率' in yearly_avg.columns:
            merge_cols.append('AC年成長率')
        if 'DC年成長率' in yearly_avg.columns:
            merge_cols.append('DC年成長率')
        
        pivot_table = pivot_table.merge(
            yearly_avg[merge_cols],
            on='Year',
            how='left'
        )
    
    pivot_table = pivot_table.drop('Year', axis=1)
    
    if 'AC' in pivot_table.columns:
        pivot_table['AC'] = pivot_table['AC'].round(2)
    
    if 'DC' in pivot_table.columns:
        pivot_table['DC'] = pivot_table['DC'].round(2)
    
    return pivot_table

@st.cache_data
def find_nearby_stations(target_lat, target_lon, _stations_df, radius_km=5):
    if _stations_df.empty:
        return pd.DataFrame()
    
    from numpy import radians, cos, sin, arcsin, sqrt
    
    lat1 = radians(target_lat)
    lon1 = radians(target_lon)
    lat2 = radians(_stations_df['latitude'].values)
    lon2 = radians(_stations_df['longitude'].values)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * arcsin(sqrt(a))
    distances = 6371 * c
    
    result = _stations_df.copy()
    result['distance_km'] = distances
    nearby = result[result['distance_km'] <= radius_km].sort_values('distance_km')
    return nearby

def create_map(center_lat, center_lon, _nearby_stations, target_address, radius_km):
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='OpenStreetMap')
    
    folium.Marker(
        [center_lat, center_lon],
        popup=f"<b>評估地點</b><br>{target_address}",
        tooltip="評估地點",
        icon=folium.Icon(color='red', icon='star')
    ).add_to(m)
    
    for idx, station in _nearby_stations.iterrows():
        popup_parts = [f"<b>{station['name']}</b>", f"站點ID: {station['station_id']}"]
        
        if 'ac_count' in station and 'dc_count' in station:
            ac_num = int(station['ac_count']) if pd.notna(station['ac_count']) else 0
            dc_num = int(station['dc_count']) if pd.notna(station['dc_count']) else 0
            popup_parts.append(f"AC槍數: {ac_num}")
            popup_parts.append(f"DC槍數: {dc_num}")
        else:
            popup_parts.append(f"充電槍數: {int(station['charger_count'])}")
        
        popup_parts.append(f"距離: {station['distance_km']:.2f} km")
        
        if 'area_type' in station and pd.notna(station['area_type']):
            popup_parts.append(f"區域: {station['area_type']}")
        if 'location_type' in station and pd.notna(station['location_type']):
            popup_parts.append(f"類型: {station['location_type']}")
        if 'city' in station and pd.notna(station['city']):
            popup_parts.append(f"縣市: {station['city']}")
        if 'project_type' in station and pd.notna(station['project_type']):
            popup_parts.append(f"標案性質: {station['project_type']}")
        
        popup_html = f"<div style='width:200px'>{'<br>'.join(popup_parts)}</div>"
        
        folium.Marker(
            [station['latitude'], station['longitude']],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=station['name'],
            icon=folium.Icon(color='blue', icon='charging-station', prefix='fa')
        ).add_to(m)
    
    folium.Circle(
        radius=radius_km * 1000, location=[center_lat, center_lon],
        color='#1E90FF', fill=True, fillOpacity=0.15
    ).add_to(m)
    
    return m

def render_utilization_gauge(value, label, color):
    """渲染稼動率儀表板"""
    if value >= 0.7:
        bar_color = "#32CD32"
        card_class = "metric-card-success"
    elif value >= 0.4:
        bar_color = "#FFA500"
        card_class = "metric-card-warning"
    else:
        bar_color = "#FF4500"
        card_class = "metric-card-danger"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div class="metric-label">{label}</div>
        <div class="big-metric" style="color: {bar_color};">{value:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # 標題列
    header_col1, header_col2, header_col3 = st.columns([4, 1, 1])
    with header_col1:
        st.title("⚡ 充電站拓點評估系統")
        st.markdown("**Electric Vehicle Charging Station Analysis Platform**")
    with header_col2:
        # 主題選擇器
        theme_choice = st.selectbox(
            "主題",
            options=list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state.current_theme),
            key="theme_selector",
            label_visibility="collapsed"
        )
        
        if theme_choice != st.session_state.current_theme:
            st.session_state.current_theme = theme_choice
            st.rerun()
    
    with header_col3:
        # 登出按鈕
        if st.button("🚪 登出", key="logout_btn", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    # 載入資料（在分頁選擇之前）
    stations_df = load_station_data()
    usage_df = load_usage_data()
    
    if stations_df.empty:
        st.warning("無充電站資料")
        return
    
    # 初始化充電度數參數
    if 'ac_capacity' not in st.session_state:
        st.session_state.ac_capacity = 7
    if 'dc_capacity' not in st.session_state:
        st.session_state.dc_capacity = 30
    
    utilization_df = pd.DataFrame()
    if not usage_df.empty:
        utilization_df = calculate_utilization_rate(
            stations_df, 
            usage_df, 
            st.session_state.ac_capacity,
            st.session_state.dc_capacity
        )
    
    # 初始化當前分頁狀態
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "拓點評估"
    
    # 使用 radio 按鈕來追蹤當前分頁
    tab_selection = st.radio(
        "選擇功能",
        ["📍 拓點評估", "📊 平均稼動率"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # 根據選擇更新 session_state
    if "拓點評估" in tab_selection:
        st.session_state.current_tab = "拓點評估"
    else:
        st.session_state.current_tab = "平均稼動率"
    
    # 初始化側邊欄變數
    manual_lat = 25.057138899151003
    manual_lon = 121.6144309671576
    search_radius = 5.0
    ac_capacity = st.session_state.ac_capacity
    dc_capacity = st.session_state.dc_capacity
    selected_area = '全部'
    selected_location = '全部'
    selected_city = '全部'
    selected_project = '全部'
    search_button = False
    
    # 側邊欄內容 - 只在拓點評估時顯示
    if st.session_state.current_tab == "拓點評估":
        with st.sidebar:
            st.header("🔍 設定評估條件")
            st.info("💡 從 Google Maps 右鍵複製座標")
            
            col1, col2 = st.columns(2)
            with col1:
                manual_lat = st.number_input("緯度", min_value=21.0, max_value=26.0, value=25.057138899151003, format="%.4f")
            with col2:
                manual_lon = st.number_input("經度", min_value=120.0, max_value=122.5, value=121.6144309671576, format="%.4f")
            
            search_radius = st.slider("搜尋半徑 (km)", min_value=0.1, max_value=10.0, value=5.0, step=0.1)
            
            st.markdown("---")
            st.markdown("### 🎯 每次充電度數參數設定")
            
            param_col1, param_col2 = st.columns(2)
            with param_col1:
                ac_capacity = st.number_input(
                    "AC 槍每次最大電量 (度/次)",
                    min_value=1,
                    max_value=99,
                    value=st.session_state.ac_capacity,
                    step=1,
                    help="AC 充電槍每次充電的最大電量，用於計算稼動率",
                    key="ac_cap_sidebar"
                )
            with param_col2:
                dc_capacity = st.number_input(
                    "DC 槍每次最大電量 (度/次)",
                    min_value=1,
                    max_value=99,
                    value=st.session_state.dc_capacity,
                    step=1,
                    help="DC 充電槍每次充電的最大電量，用於計算稼動率",
                    key="dc_cap_sidebar"
                )
            
            st.markdown("---")
            st.markdown("### 🎯 進階篩選條件")
            
            # 現有的區域屬性和站點屬性
            if 'area_type' in stations_df.columns:
                area_types = ['全部'] + sorted(stations_df['area_type'].dropna().unique().tolist())
                selected_area = st.selectbox("區域屬性", options=area_types)
            else:
                selected_area = '全部'
            
            if 'location_type' in stations_df.columns:
                location_types = ['全部'] + sorted(stations_df['location_type'].dropna().unique().tolist())
                selected_location = st.selectbox("站點屬性", options=location_types)
            else:
                selected_location = '全部'
            
            # 新增縣市篩選
            if 'city' in stations_df.columns:
                cities = ['全部'] + sorted(stations_df['city'].dropna().unique().tolist())
                selected_city = st.selectbox("縣市", options=cities)
            else:
                selected_city = '全部'
            
            # 新增標案性質篩選
            if 'project_type' in stations_df.columns:
                project_types = ['全部'] + sorted(stations_df['project_type'].dropna().unique().tolist())
                selected_project = st.selectbox("標案性質", options=project_types)
            else:
                selected_project = '全部'
            
            st.markdown("---")
            search_button = st.button("🔍 開始評估", type="primary", use_container_width=True)
    else:
        # 平均稼動率分頁 - 側邊欄顯示簡單訊息
        with st.sidebar:
            st.info("📊 請在主頁面設定篩選條件")
    
    # ===== 分頁1: 拓點評估 =====
    if st.session_state.current_tab == "拓點評估":
        if search_button:
            if manual_lat is None or manual_lon is None:
                st.warning("⚠️ 請輸入經緯度座標")
            else:
                # 保存充電度數參數到 session_state
                st.session_state.ac_capacity = ac_capacity
                st.session_state.dc_capacity = dc_capacity
                
                # 重新計算稼動率（使用新參數）
                if not usage_df.empty:
                    utilization_df = calculate_utilization_rate(
                        stations_df, 
                        usage_df, 
                        ac_capacity,
                        dc_capacity
                    )
                
                st.session_state.search_executed = True
                st.session_state.search_lat = manual_lat
                st.session_state.search_lon = manual_lon
                st.session_state.search_radius = search_radius
                st.session_state.selected_area = selected_area
                st.session_state.selected_location = selected_location
                st.session_state.selected_city = selected_city
                st.session_state.selected_project = selected_project
        
        if st.session_state.get('search_executed', False):
            lat = st.session_state.search_lat
            lon = st.session_state.search_lon
            search_radius = st.session_state.search_radius
            selected_area = st.session_state.get('selected_area', '全部')
            selected_location = st.session_state.get('selected_location', '全部')
            selected_city = st.session_state.get('selected_city', '全部')
            selected_project = st.session_state.get('selected_project', '全部')
            
            with st.spinner("🔄 正在分析地點..."):
                nearby = find_nearby_stations(lat, lon, stations_df, search_radius)
                
                # 應用篩選條件
                if selected_area != '全部' and 'area_type' in nearby.columns:
                    nearby = nearby[nearby['area_type'] == selected_area]
                if selected_location != '全部' and 'location_type' in nearby.columns:
                    nearby = nearby[nearby['location_type'] == selected_location]
                if selected_city != '全部' and 'city' in nearby.columns:
                    nearby = nearby[nearby['city'] == selected_city]
                if selected_project != '全部' and 'project_type' in nearby.columns:
                    nearby = nearby[nearby['project_type'] == selected_project]
                
                st.session_state.nearby_stations = nearby
            
            st.subheader(f"📊 評估結果")
            st.caption(f"座標：{lat:.4f}, {lon:.4f} | 搜尋半徑：{search_radius} km")
            st.caption(f"⚙️ 計算參數：AC={st.session_state.ac_capacity}度/次 | DC={st.session_state.dc_capacity}度/次")
            
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                total_stations = len(nearby)
                st.metric("附近站點數", total_stations, help="搜尋半徑內的站點數量")
            
            with metric_col2:
                if 'ac_count' in nearby.columns:
                    total_ac = int(nearby['ac_count'].sum()) if len(nearby) > 0 else 0
                    st.metric("AC 槍數", total_ac, delta="慢充", delta_color="off")
            
            with metric_col3:
                if 'dc_count' in nearby.columns:
                    total_dc = int(nearby['dc_count'].sum()) if len(nearby) > 0 else 0
                    st.metric("DC 槍數", total_dc, delta="快充", delta_color="off")
            
            st.markdown("---")
            
            if not utilization_df.empty and len(nearby) > 0:
                st.subheader("📈 區域稼動率表現")
                
                nearby_stations = nearby['station_id'].tolist()
                nearby_util = utilization_df[utilization_df['Station'].isin(nearby_stations)]
                
                if not nearby_util.empty:
                    latest_quarter = nearby_util['Quarter'].max()
                    latest_data = nearby_util[nearby_util['Quarter'] == latest_quarter]
                    
                    gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
                    
                    with gauge_col1:
                        st.markdown(f"**最新季度：{latest_quarter}**")
                    
                    with gauge_col2:
                        ac_util = latest_data[latest_data['ChargerType'] == 'AC']['utilization_rate'].dropna()
                        if len(ac_util) > 0:
                            render_utilization_gauge(ac_util.mean(), "AC 稼動率", "#87CEEB")
                    
                    with gauge_col3:
                        dc_util = latest_data[latest_data['ChargerType'] == 'DC']['utilization_rate'].dropna()
                        if len(dc_util) > 0:
                            render_utilization_gauge(dc_util.mean(), "DC 稼動率", "#20B2AA")
            
            st.markdown("---")
            
            map_col, station_col = st.columns([1, 1])
            
            with map_col:
                st.subheader("🗺️ 地圖視圖")
                target_address = f"座標: ({lat:.4f}, {lon:.4f})"
                map_obj = create_map(lat, lon, nearby, target_address, search_radius)
                folium_static(map_obj, width=600, height=500)
            
            with station_col:
                st.subheader("🔍 單站詳細資訊")
                
                if len(nearby) > 0:
                    station_options = {f"{row['name']} ({row['station_id']})": row['station_id'] 
                                      for _, row in nearby.iterrows()}
                    
                    selected_display = st.selectbox(
                        "選擇站點查看詳情",
                        options=["請選擇站點..."] + list(station_options.keys()),
                        key="single_station"
                    )
                    
                    if selected_display != "請選擇站點...":
                        selected_id = station_options[selected_display]
                        station_info = nearby[nearby['station_id'] == selected_id].iloc[0]
                        
                        st.markdown(f"### {station_info['name']}")
                        
                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.markdown(f"**站點 ID**  \n`{station_info['station_id']}`")
                            st.markdown(f"**距離**  \n🚗 {station_info['distance_km']:.2f} km")
                            if 'city' in station_info and pd.notna(station_info['city']):
                                st.markdown(f"**縣市**  \n🏙️ {station_info['city']}")
                        with info_col2:
                            if 'ac_count' in station_info:
                                st.markdown(f"**AC 槍數**  \n⚡ {int(station_info['ac_count'])}")
                            if 'dc_count' in station_info:
                                st.markdown(f"**DC 槍數**  \n⚡ {int(station_info['dc_count'])}")
                            if 'project_type' in station_info and pd.notna(station_info['project_type']):
                                st.markdown(f"**標案性質**  \n📋 {station_info['project_type']}")
                        
                        if not utilization_df.empty:
                            station_util = utilization_df[utilization_df['Station'] == selected_id]
                            
                            if not station_util.empty:
                                st.markdown("#### 📊 稼動率歷史")
                                
                                quarterly_single = calculate_quarterly_utilization(
                                    utilization_df, 
                                    [selected_id],
                                    st.session_state.ac_capacity,
                                    st.session_state.dc_capacity
                                )
                                
                                if not quarterly_single.empty:
                                    display_df = quarterly_single[['Quarter']].copy()
                                    if 'AC' in quarterly_single.columns:
                                        display_df['AC稼動率'] = quarterly_single['AC']
                                    if 'DC' in quarterly_single.columns:
                                        display_df['DC稼動率'] = quarterly_single['DC']
                                    
                                    st.dataframe(display_df, use_container_width=True, hide_index=True, height=250)
                else:
                    st.info("此範圍內無站點")
            
            if not utilization_df.empty and len(nearby) > 0:
                with st.expander("📈 查看區域歷季趨勢詳細資料"):
                    quarterly_df = calculate_quarterly_utilization(
                        utilization_df, 
                        nearby_stations,
                        st.session_state.ac_capacity,
                        st.session_state.dc_capacity
                    )
                    
                    if not quarterly_df.empty:
                        fig = go.Figure()
                        
                        if 'AC' in quarterly_df.columns:
                            fig.add_trace(go.Scatter(
                                x=quarterly_df['Quarter'],
                                y=quarterly_df['AC'],
                                mode='lines+markers',
                                name='AC稼動率',
                                line=dict(color=THEMES[st.session_state.current_theme]['accent1'], width=3),
                                marker=dict(size=8)
                            ))
                        
                        if 'DC' in quarterly_df.columns:
                            fig.add_trace(go.Scatter(
                                x=quarterly_df['Quarter'],
                                y=quarterly_df['DC'],
                                mode='lines+markers',
                                name='DC稼動率',
                                line=dict(color=THEMES[st.session_state.current_theme]['accent2'], width=3),
                                marker=dict(size=8)
                            ))
                        
                        fig.update_layout(
                            title='區域稼動率季度趨勢',
                            xaxis_title='季度',
                            yaxis_title='稼動率',
                            height=400,
                            hovermode='x unified',
                            plot_bgcolor='white',
                            paper_bgcolor='#F5F5F5'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown("#### 📋 數據表格")
                        
                        display_df = quarterly_df.copy()
                        display_df['Year'] = display_df['Quarter'].str[:4]
                        
                        html_table = '<table style="width:100%; border-collapse: collapse; text-align: center; background: white; border-radius: 8px; overflow: hidden;">'
                        html_table += '<thead><tr style="background: linear-gradient(135deg, ' + THEMES[st.session_state.current_theme]['primary'] + ' 0%, ' + THEMES[st.session_state.current_theme]['secondary'] + ' 100%); color: white; font-weight: bold;">'
                        html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">季度</th>'
                        
                        if 'AC' in display_df.columns:
                            html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">AC稼動率</th>'
                            html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">AC年成長率</th>'
                        if 'DC' in display_df.columns:
                            html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">DC稼動率</th>'
                            html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">DC年成長率</th>'
                        
                        html_table += '</tr></thead><tbody>'
                        
                        year_counts = display_df['Year'].value_counts().sort_index()
                        year_first_occurrence = {}
                        
                        for idx, row in display_df.iterrows():
                            year = row['Year']
                            
                            if year not in year_first_occurrence:
                                year_first_occurrence[year] = True
                                is_first = True
                            else:
                                is_first = False
                            
                            html_table += '<tr style="border: 1px solid #E0E0E0;">'
                            html_table += f'<td style="padding: 10px; border: 1px solid #E0E0E0; color: #333333;">{row["Quarter"]}</td>'
                            
                            if 'AC' in row:
                                ac_value = row['AC']
                                html_table += f'<td style="padding: 10px; border: 1px solid #E0E0E0; color: #333333; font-weight: 600;">{ac_value:.2f}</td>'
                                
                                if is_first and 'AC年成長率' in row:
                                    ac_growth = row['AC年成長率']
                                    rowspan = year_counts[year]
                                    
                                    if pd.notna(ac_growth) and ac_growth != 0:
                                        color = '#32CD32' if ac_growth > 0 else '#FF4500'
                                        growth_text = f"{ac_growth:+.1f}%"
                                    else:
                                        color = '#AAAAAA'
                                        growth_text = '-'
                                    
                                    html_table += f'<td rowspan="{rowspan}" style="padding: 10px; border: 1px solid #E0E0E0; background-color: #F5F5F5; color: {color}; font-weight: bold; vertical-align: middle;">{growth_text}</td>'
                            
                            if 'DC' in row:
                                dc_value = row['DC']
                                html_table += f'<td style="padding: 10px; border: 1px solid #E0E0E0; color: #333333; font-weight: 600;">{dc_value:.2f}</td>'
                                
                                if is_first and 'DC年成長率' in row:
                                    dc_growth = row['DC年成長率']
                                    rowspan = year_counts[year]
                                    
                                    if pd.notna(dc_growth) and dc_growth != 0:
                                        color = '#32CD32' if dc_growth > 0 else '#FF4500'
                                        growth_text = f"{dc_growth:+.1f}%"
                                    else:
                                        color = '#AAAAAA'
                                        growth_text = '-'
                                    
                                    html_table += f'<td rowspan="{rowspan}" style="padding: 10px; border: 1px solid #E0E0E0; background-color: #F5F5F5; color: {color}; font-weight: bold; vertical-align: middle;">{growth_text}</td>'
                            
                            html_table += '</tr>'
                        
                        html_table += '</tbody></table>'
                        st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.info("👈 請在側邊欄設定評估條件並點擊「開始評估」")
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("系統總站點數", len(stations_df))
            with stat_col2:
                st.metric("系統總充電槍數", int(stations_df['charger_count'].sum()))
            with stat_col3:
                if 'ac_count' in stations_df.columns and 'dc_count' in stations_df.columns:
                    total_ac = int(stations_df['ac_count'].sum())
                    total_dc = int(stations_df['dc_count'].sum())
                    st.metric("AC / DC 比例", f"{total_ac} / {total_dc}")
    
    # ===== 分頁2: 平均稼動率 =====
    elif st.session_state.current_tab == "平均稼動率":
        # 先檢查是否需要重新計算稼動率
        if not usage_df.empty:
            utilization_df = calculate_utilization_rate(
                stations_df, 
                usage_df, 
                st.session_state.ac_capacity,
                st.session_state.dc_capacity
            )
        
        if utilization_df.empty:
            st.warning("⚠️ 無稼動率資料")
            return
        
        st.subheader("🎯 每次充電度數參數設定")
        
        param_col1, param_col2, param_col3 = st.columns([2, 2, 1])
        with param_col1:
            ac_capacity_tab2 = st.number_input(
                "AC 槍每次最大電量 (度/次)",
                min_value=1,
                max_value=99,
                value=st.session_state.ac_capacity,
                step=1,
                help="AC 充電槍每次充電的最大電量，用於計算稼動率",
                key="ac_capacity_tab2"
            )
        with param_col2:
            dc_capacity_tab2 = st.number_input(
                "DC 槍每次最大電量 (度/次)",
                min_value=1,
                max_value=99,
                value=st.session_state.dc_capacity,
                step=1,
                help="DC 充電槍每次充電的最大電量，用於計算稼動率",
                key="dc_capacity_tab2"
            )
        with param_col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 更新參數", type="primary", use_container_width=True, key="update_params_tab2"):
                st.session_state.ac_capacity = ac_capacity_tab2
                st.session_state.dc_capacity = dc_capacity_tab2
                st.success("✅ 參數已更新")
                st.rerun()
        
        st.markdown("---")
        
        st.subheader("🎯 通路篩選條件")
        
        filter_row1 = st.columns([2, 2, 2, 2])
        
        with filter_row1[0]:
            if 'area_type' in stations_df.columns:
                area_types_all = ['全部'] + sorted(stations_df['area_type'].dropna().unique().tolist())
                filter_area = st.selectbox("區域屬性", options=area_types_all, key="filter_area")
            else:
                filter_area = '全部'
        
        with filter_row1[1]:
            if 'location_type' in stations_df.columns:
                location_types_all = ['全部'] + sorted(stations_df['location_type'].dropna().unique().tolist())
                filter_location = st.selectbox("站點屬性", options=location_types_all, key="filter_location")
            else:
                filter_location = '全部'
        
        with filter_row1[2]:
            if 'city' in stations_df.columns:
                cities_all = ['全部'] + sorted(stations_df['city'].dropna().unique().tolist())
                filter_city = st.selectbox("縣市", options=cities_all, key="filter_city")
            else:
                filter_city = '全部'
        
        with filter_row1[3]:
            if 'project_type' in stations_df.columns:
                project_types_all = ['全部'] + sorted(stations_df['project_type'].dropna().unique().tolist())
                filter_project = st.selectbox("標案性質", options=project_types_all, key="filter_project")
            else:
                filter_project = '全部'
        
        st.markdown("---")
        
        st.subheader("🎯 單站篩選條件")
        
        station_name_search = st.text_input(
            "🔍 單站搜尋（選填）",
            placeholder="輸入站點名稱關鍵字快速找站...",
            key="station_name_search",
            help="模糊搜尋站點名稱，找到後可在下方選擇單站查看"
        )
        
        if station_name_search and station_name_search.strip():
            st.markdown("---")
            
            search_results = stations_df[
                stations_df['name'].str.contains(station_name_search.strip(), case=False, na=False)
            ]
            
            if len(search_results) > 0:
                st.markdown(f"**找到 {len(search_results)} 個站點**，請選擇要查看的單站：")
                
                station_options = {
                    f"{row['name']} ({row['station_id']})": row['station_id'] 
                    for _, row in search_results.iterrows()
                }
                
                selected_station_display = st.selectbox(
                    "選擇站點",
                    options=["請選擇站點..."] + list(station_options.keys()),
                    key="selected_single_station"
                )
                
                if selected_station_display != "請選擇站點...":
                    selected_station_id = station_options[selected_station_display]
                    filtered_stations = stations_df[stations_df['station_id'] == selected_station_id]
                    st.success(f"✅ 已選擇單站：{selected_station_display}")
                else:
                    filtered_stations = stations_df.copy()
                    
                    # 應用通路篩選條件
                    if filter_area != '全部' and 'area_type' in filtered_stations.columns:
                        filtered_stations = filtered_stations[filtered_stations['area_type'] == filter_area]
                    if filter_location != '全部' and 'location_type' in filtered_stations.columns:
                        filtered_stations = filtered_stations[filtered_stations['location_type'] == filter_location]
                    if filter_city != '全部' and 'city' in filtered_stations.columns:
                        filtered_stations = filtered_stations[filtered_stations['city'] == filter_city]
                    if filter_project != '全部' and 'project_type' in filtered_stations.columns:
                        filtered_stations = filtered_stations[filtered_stations['project_type'] == filter_project]
            else:
                st.warning(f"⚠️ 找不到包含「{station_name_search}」的站點")
                filtered_stations = stations_df.copy()
                
                # 應用通路篩選條件
                if filter_area != '全部' and 'area_type' in filtered_stations.columns:
                    filtered_stations = filtered_stations[filtered_stations['area_type'] == filter_area]
                if filter_location != '全部' and 'location_type' in filtered_stations.columns:
                    filtered_stations = filtered_stations[filtered_stations['location_type'] == filter_location]
                if filter_city != '全部' and 'city' in filtered_stations.columns:
                    filtered_stations = filtered_stations[filtered_stations['city'] == filter_city]
                if filter_project != '全部' and 'project_type' in filtered_stations.columns:
                    filtered_stations = filtered_stations[filtered_stations['project_type'] == filter_project]
        else:
            filtered_stations = stations_df.copy()
            
            # 應用通路篩選條件
            if filter_area != '全部' and 'area_type' in filtered_stations.columns:
                filtered_stations = filtered_stations[filtered_stations['area_type'] == filter_area]
            if filter_location != '全部' and 'location_type' in filtered_stations.columns:
                filtered_stations = filtered_stations[filtered_stations['location_type'] == filter_location]
            if filter_city != '全部' and 'city' in filtered_stations.columns:
                filtered_stations = filtered_stations[filtered_stations['city'] == filter_city]
            if filter_project != '全部' and 'project_type' in filtered_stations.columns:
                filtered_stations = filtered_stations[filtered_stations['project_type'] == filter_project]
        
        filtered_station_ids = filtered_stations['station_id'].tolist()
        
        if len(filtered_station_ids) == 0:
            st.warning("⚠️ 沒有符合篩選條件的站點")
            return
        
        quarterly_data = calculate_quarterly_utilization(
            utilization_df, 
            filtered_station_ids,
            st.session_state.ac_capacity,
            st.session_state.dc_capacity
        )
        
        if quarterly_data.empty:
            st.info("📊 篩選條件下無稼動率資料")
            return
        
        st.markdown("---")
        
        latest_quarter = quarterly_data.iloc[-1]
        
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric("篩選站點數", len(filtered_stations), help="符合篩選條件的站點總數")
        
        with kpi_col2:
            total_chargers = int(filtered_stations['charger_count'].sum())
            st.metric("充電槍總數", total_chargers)
        
        with kpi_col3:
            if 'AC' in latest_quarter:
                ac_growth = latest_quarter.get('AC年成長率', 0)
                growth_text = f"{ac_growth:+.1f}%" if pd.notna(ac_growth) and ac_growth != 0 else None
                st.metric(
                    f"AC稼動率 ({latest_quarter['Quarter']})",
                    f"{latest_quarter['AC']:.2f}",
                    delta=growth_text,
                    help="年度平均成長率"
                )
        
        with kpi_col4:
            if 'DC' in latest_quarter:
                dc_growth = latest_quarter.get('DC年成長率', 0)
                growth_text = f"{dc_growth:+.1f}%" if pd.notna(dc_growth) and dc_growth != 0 else None
                st.metric(
                    f"DC稼動率 ({latest_quarter['Quarter']})",
                    f"{latest_quarter['DC']:.2f}",
                    delta=growth_text,
                    help="年度平均成長率"
                )
        
        st.markdown("---")
        st.caption(f"⚙️ 計算參數：AC={st.session_state.ac_capacity}度/次 | DC={st.session_state.dc_capacity}度/次")
        st.markdown("---")
        
        st.subheader("📊 稼動率趨勢分析")
        
        fig = go.Figure()
        
        if 'AC' in quarterly_data.columns:
            fig.add_trace(go.Scatter(
                x=quarterly_data['Quarter'],
                y=quarterly_data['AC'],
                mode='lines+markers+text',
                name='AC稼動率',
                line=dict(color=THEMES[st.session_state.current_theme]['accent1'], width=3),
                marker=dict(size=10, symbol='circle'),
                text=[f"{val:.2f}" for val in quarterly_data['AC']],
                textposition='top center',
                textfont=dict(size=10, color='#333333'),
                hovertemplate='<b>AC稼動率</b><br>季度: %{x}<br>稼動率: %{y:.2f}<extra></extra>'
            ))
        
        if 'DC' in quarterly_data.columns:
            fig.add_trace(go.Scatter(
                x=quarterly_data['Quarter'],
                y=quarterly_data['DC'],
                mode='lines+markers+text',
                name='DC稼動率',
                line=dict(color=THEMES[st.session_state.current_theme]['accent2'], width=3),
                marker=dict(size=10, symbol='square'),
                text=[f"{val:.2f}" for val in quarterly_data['DC']],
                textposition='bottom center',
                textfont=dict(size=10, color='#333333'),
                hovertemplate='<b>DC稼動率</b><br>季度: %{x}<br>稼動率: %{y:.2f}<extra></extra>'
            ))
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            xaxis=dict(title='季度'),
            yaxis=dict(title='稼動率'),
            plot_bgcolor='white',
            paper_bgcolor='#F5F5F5',
            font=dict(color='#333333')
        )
        
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E0E0E0')
        
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 查看詳細數據表格", expanded=False):
            display_data = quarterly_data.copy()
            display_data['Year'] = display_data['Quarter'].str[:4]
            
            html_table = '<table style="width:100%; border-collapse: collapse; text-align: center; background: white; border-radius: 8px; overflow: hidden;">'
            html_table += '<thead><tr style="background: linear-gradient(135deg, ' + THEMES[st.session_state.current_theme]['primary'] + ' 0%, ' + THEMES[st.session_state.current_theme]['secondary'] + ' 100%); color: white; font-weight: bold;">'
            html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">季度</th>'
            
            if 'AC' in display_data.columns:
                html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">AC稼動率</th>'
                html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">AC年成長率</th>'
            if 'DC' in display_data.columns:
                html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">DC稼動率</th>'
                html_table += '<th style="padding: 12px; border: 1px solid #E0E0E0;">DC年成長率</th>'
            
            html_table += '</tr></thead><tbody>'
            
            year_counts = display_data['Year'].value_counts().sort_index()
            year_first_occurrence = {}
            
            for idx, row in display_data.iterrows():
                year = row['Year']
                
                if year not in year_first_occurrence:
                    year_first_occurrence[year] = True
                    is_first = True
                else:
                    is_first = False
                
                html_table += '<tr style="border: 1px solid #E0E0E0;">'
                html_table += f'<td style="padding: 10px; border: 1px solid #E0E0E0; color: #333333;">{row["Quarter"]}</td>'
                
                if 'AC' in row:
                    ac_value = row['AC']
                    html_table += f'<td style="padding: 10px; border: 1px solid #E0E0E0; color: #333333; font-weight: 600;">{ac_value:.2f}</td>'
                    
                    if is_first and 'AC年成長率' in row:
                        ac_growth = row['AC年成長率']
                        rowspan = year_counts[year]
                        
                        if pd.notna(ac_growth) and ac_growth != 0:
                            color = '#32CD32' if ac_growth > 0 else '#FF4500'
                            growth_text = f"{ac_growth:+.1f}%"
                        else:
                            color = '#AAAAAA'
                            growth_text = '-'
                        
                        html_table += f'<td rowspan="{rowspan}" style="padding: 10px; border: 1px solid #E0E0E0; background-color: #F5F5F5; color: {color}; font-weight: bold; vertical-align: middle;">{growth_text}</td>'
                
                if 'DC' in row:
                    dc_value = row['DC']
                    html_table += f'<td style="padding: 10px; border: 1px solid #E0E0E0; color: #333333; font-weight: 600;">{dc_value:.2f}</td>'
                    
                    if is_first and 'DC年成長率' in row:
                        dc_growth = row['DC年成長率']
                        rowspan = year_counts[year]
                        
                        if pd.notna(dc_growth) and dc_growth != 0:
                            color = '#32CD32' if dc_growth > 0 else '#FF4500'
                            growth_text = f"{dc_growth:+.1f}%"
                        else:
                            color = '#AAAAAA'
                            growth_text = '-'
                        
                        html_table += f'<td rowspan="{rowspan}" style="padding: 10px; border: 1px solid #E0E0E0; background-color: #F5F5F5; color: {color}; font-weight: bold; vertical-align: middle;">{growth_text}</td>'
                
                html_table += '</tr>'
            
            html_table += '</tbody></table>'
            st.markdown(html_table, unsafe_allow_html=True)
            
            st.markdown("---")
            
            download_data = display_data.copy()
            
            if 'AC年成長率' in download_data.columns:
                download_data['AC年成長率'] = download_data['AC年成長率'].apply(
                    lambda x: f"{x:+.1f}%" if pd.notna(x) and x != 0 else "-"
                )
            if 'DC年成長率' in download_data.columns:
                download_data['DC年成長率'] = download_data['DC年成長率'].apply(
                    lambda x: f"{x:+.1f}%" if pd.notna(x) and x != 0 else "-"
                )
            
            rename_map = {
                'Quarter': '季度',
                'AC': 'AC稼動率',
                'DC': 'DC稼動率',
                'Year': '年份'
            }
            download_data = download_data.rename(columns=rename_map)
            
            export_cols = ['季度']
            if 'AC稼動率' in download_data.columns:
                export_cols.append('AC稼動率')
            if 'AC年成長率' in download_data.columns:
                export_cols.append('AC年成長率')
            if 'DC稼動率' in download_data.columns:
                export_cols.append('DC稼動率')
            if 'DC年成長率' in download_data.columns:
                export_cols.append('DC年成長率')
            
            download_data = download_data[export_cols]
            
            # 建立檔案名稱
            filter_parts = []
            if filter_area != '全部':
                filter_parts.append(filter_area)
            if filter_location != '全部':
                filter_parts.append(filter_location)
            if filter_city != '全部':
                filter_parts.append(filter_city)
            if filter_project != '全部':
                filter_parts.append(filter_project)
            
            filename_suffix = '_'.join(filter_parts) if filter_parts else '全部'
            
            csv = download_data.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 下載數據 (CSV)",
                data=csv,
                file_name=f"稼動率分析_{filename_suffix}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

