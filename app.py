import streamlit as st
from PIL import Image
import pandas as pd

# 設定頁面配置 - 針對手機優化
st.set_page_config(
    page_title="2025 EVALUE Day 嘉年華",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"  # 收起側邊欄
)

# 自定義CSS樣式 - 嘉年華主題（手機優化）
css_styles = """
<style>
    /* 隱藏側邊欄 */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* 強制覆蓋深色模式，保持一致的亮色風格 */
    .stApp {
        background: linear-gradient(180deg, #fef9f3 0%, #fdf4e8 100%) !important;
        color: #2c2c2c !important;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.7) !important;
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        color: #2c2c2c !important;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* 嘉年華漸層背景 - 固定白色文字 */
    .main-header {
        background: linear-gradient(135deg, #E85D75 0%, #F3722C 25%, #FDB143 50%, #43AA8B 75%, #277DA1 100%) !important;
        padding: 2rem 1rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: gradient-shift 5s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main-header h1 {
        font-size: 1.8rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1rem !important;
        color: white !important;
        margin: 0.3rem 0;
    }
    
    /* 區塊標題樣式 */
    .section-header {
        background: linear-gradient(90deg, rgba(67, 170, 139, 0.1), rgba(39, 125, 161, 0.1));
        padding: 1rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #43AA8B;
    }
    
    .section-header h2 {
        color: #277DA1 !important;
        margin: 0;
        font-size: 1.5rem;
    }
    
    /* 活動卡片 - 固定亮色風格 */
    .activity-card {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #F3722C;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: #2c2c2c !important;
    }
    
    .activity-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    
    /* 攤位卡片特殊樣式 */
    .booth-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,252,248,0.95)) !important;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .booth-card::before {
        content: '';
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: -1;
        margin: -2px;
        border-radius: inherit;
        background: linear-gradient(45deg, #E85D75, #F3722C, #FDB143, #43AA8B);
    }
    
    .booth-number {
        display: inline-block;
        background: linear-gradient(45deg, #E85D75, #F3722C);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    
    /* 時程表樣式 */
    .schedule-item {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #43AA8B;
        transition: all 0.3s ease;
    }
    
    .schedule-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .time-badge {
        background: linear-gradient(45deg, #43AA8B, #277DA1);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        display: inline-block;
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }
    
    /* 快速導覽卡片 */
    .nav-card {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 1.5rem 1rem;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        cursor: pointer;
        height: 100%;
    }
    
    .nav-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .nav-card h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
    }
    
    .nav-card h4 {
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .nav-card p {
        margin: 0;
        font-size: 0.85rem;
        color: #666 !important;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(232, 93, 117, 0.9), rgba(243, 114, 44, 0.9)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(232, 93, 117, 0.3) !important;
    }
    
    /* 高亮框 */
    .highlight-box {
        background: linear-gradient(45deg, rgba(253, 177, 67, 0.9), rgba(243, 114, 44, 0.9)) !important;
        color: white !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(253, 177, 67, 0.2);
    }
    
    .highlight-box h3,
    .highlight-box h4,
    .highlight-box p {
        color: white !important;
    }
    
    /* 資訊框 */
    .info-box {
        background: rgba(67, 170, 139, 0.1) !important;
        border-left: 3px solid #43AA8B !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #2c2c2c !important;
    }
    
    /* 表格樣式 */
    .dataframe {
        border: 2px solid rgba(253, 177, 67, 0.6) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    .dataframe th {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid rgba(253, 177, 67, 0.3) !important;
        padding: 8px !important;
        background: rgba(255, 255, 255, 0.8) !important;
        color: #2c2c2c !important;
    }
    
    /* Tabs 樣式優化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: transparent;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9));
        color: white;
    }
    
    /* 成功/錯誤訊息樣式 */
    .stSuccess {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stError {
        background: linear-gradient(45deg, rgba(232, 93, 117, 0.9), rgba(243, 114, 44, 0.9)) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stInfo {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.7), rgba(39, 125, 161, 0.7)) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* 裝飾性元素 */
    .decoration {
        text-align: center;
        font-size: 2rem;
        opacity: 0.3;
        margin: 1rem 0;
    }
    
    /* 分隔線樣式 */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(67, 170, 139, 0.3), transparent);
    }
    
    /* 響應式設計 - 手機優化 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .main-header {
            padding: 1.5rem 0.8rem;
            margin-bottom: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .main-header p {
            font-size: 0.9rem !important;
        }
        
        .section-header h2 {
            font-size: 1.3rem;
        }
        
        .booth-card,
        .activity-card,
        .schedule-item {
            margin-bottom: 0.8rem;
            padding: 0.8rem;
        }
        
        .nav-card {
            padding: 1rem;
            margin-bottom: 0.8rem;
        }
        
        .nav-card h1 {
            font-size: 1.5rem;
        }
        
        .nav-card h4 {
            font-size: 1rem;
        }
        
        /* 調整表格字體大小 */
        .dataframe th,
        .dataframe td {
            font-size: 0.85rem !important;
            padding: 6px !important;
        }
        
        /* 調整按鈕大小 */
        .stButton > button {
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }
        
        /* 優化 Tabs 在手機上的顯示 */
        .stTabs [data-baseweb="tab"] {
            padding: 6px 10px;
            font-size: 0.85rem;
        }
    }
    
    /* 平滑捲動 */
    html {
        scroll-behavior: smooth;
    }
    
    /* 固定頂部導航按鈕 */
    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(45deg, #43AA8B, #277DA1);
        color: white;
        padding: 10px 15px;
        border-radius: 50%;
        cursor: pointer;
        z-index: 999;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .back-to-top:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)


# ==================== 一頁式網站主要內容 ====================

# Logo 和主標題區域
try:
    # 嘗試載入 logo
    logo = Image.open("logo.png")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(logo, width=150, use_container_width=False)
except:
    pass

# 主標題
header_html = """
<div class="main-header">
    <h1>🎪 2025 EVALUE Day 嘉年華 🎪</h1>
    <p><strong>歡樂充電・綠能同行</strong></p>
    <p>📅 11月29日(六) 10:00-17:00</p>
    <p>📍 苗栗西湖渡假村 幸福廣場</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==================== 快速導覽區 ====================
st.markdown('<div class="decoration">🎈 🎪 🎯 🎨 🎭 🎪 🎈</div>', unsafe_allow_html=True)

# 快速導覽按鈕
st.markdown("## 🚀 快速導覽")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    st.markdown("""
    <div class="nav-card">
        <h1>🎪</h1>
        <h4 style="color: #E85D75;">攤位資訊</h4>
        <p>精彩攤位</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="nav-card">
        <h1>📅</h1>
        <h4 style="color: #F3722C;">活動時程</h4>
        <p>時間表</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div class="nav-card">
        <h1>🎁</h1>
        <h4 style="color: #43AA8B;">抽獎查詢</h4>
        <p>得獎公布</p>
    </div>
    """, unsafe_allow_html=True)

with nav_col4:
    st.markdown("""
    <div class="nav-card">
        <h1>📍</h1>
        <h4 style="color: #277DA1;">交通資訊</h4>
        <p>如何抵達</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== 活動介紹 ====================
st.markdown('<div class="section-header"><h2>🎊 活動介紹</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    intro_card = """
    <div class="activity-card">
        <h3 style="color: #E85D75; margin-bottom: 0.8rem;">歡迎來到 EVALUE Day！</h3>
        <p>一年一度的 EVALUE Day 嘉年華即將盛大舉行！今年我們準備了更豐富的園遊會攤位、精彩的舞台表演，以及超值的抽獎活動。</p>
        <br>
        <p><strong>🎯 活動亮點：</strong></p>
        <ul style="margin-top: 0.5rem;">
            <li>30+ 精彩攤位遊戲</li>
            <li>豐富美食饗宴</li>
            <li>專業舞台表演</li>
            <li>超值抽獎活動</li>
            <li>親子互動專區</li>
        </ul>
    </div>
    """
    st.markdown(intro_card, unsafe_allow_html=True)

with col2:
    try:
        event_image = Image.open("event_banner.png")
        st.image(event_image, caption="2025 EVALUE Day 嘉年華", use_container_width=True)
    except:
        info_card = """
        <div class="highlight-box">
            <h3>📌 活動資訊</h3>
            <p>📅 <strong>日期：</strong>2025年11月29日 (六)</p>
            <p>⏰ <strong>時間：</strong>10:00 - 17:00</p>
            <p>📍 <strong>地點：</strong>苗栗西湖渡假村</p>
            <p>🎫 <strong>參加資格：</strong>EVALUE 會員</p>
            <p>💰 <strong>費用：</strong>免費入場</p>
        </div>
        """
        st.markdown(info_card, unsafe_allow_html=True)

# 最新消息
with st.container():
    st.markdown("### 📢 最新消息")
    st.info("🔔 【11/15】攤位配置圖已公布，請查看下方攤位資訊")
    st.info("🔔 【11/10】第一波抽獎名單已公布！請至抽獎查詢區查看")
    st.info("🔔 【11/05】活動當天提供免費接駁車，詳見交通資訊")

st.markdown("---")

# ==================== 攤位資訊 ====================
st.markdown('<div class="section-header"><h2>🎪 攤位資訊</h2></div>', unsafe_allow_html=True)

# 攤位分類
tab1, tab2, tab3, tab4 = st.tabs(["🎮 遊戲攤位", "🍔 美食攤位", "🛍️ 文創市集", "💡 綠能展示"])

with tab1:
    st.markdown("### 🎮 遊戲攤位")
    game_col1, game_col2 = st.columns(2)
    
    with game_col1:
        booth_html = """
        <div class="booth-card">
            <span class="booth-number">攤位 A01</span>
            <h4 style="color: #E85D75; margin: 0.5rem 0;">套圈圈大挑戰</h4>
            <p style="margin: 0.3rem 0;">經典遊戲，豐富獎品！</p>
            <p style="color: #666; font-size: 0.85rem;">💰 遊戲券 x2</p>
        </div>
        
        <div class="booth-card">
            <span class="booth-number">攤位 A03</span>
            <h4 style="color: #E85D75; margin: 0.5rem 0;">彈珠檯</h4>
            <p style="margin: 0.3rem 0;">懷舊彈珠檯</p>
            <p style="color: #666; font-size: 0.85rem;">💰 遊戲券 x1</p>
        </div>
        """
        st.markdown(booth_html, unsafe_allow_html=True)
    
    with game_col2:
        booth_html = """
        <div class="booth-card">
            <span class="booth-number">攤位 A02</span>
            <h4 style="color: #E85D75; margin: 0.5rem 0;">夾娃娃機</h4>
            <p style="margin: 0.3rem 0;">超可愛娃娃</p>
            <p style="color: #666; font-size: 0.85rem;">💰 遊戲券 x3</p>
        </div>
        
        <div class="booth-card">
            <span class="booth-number">攤位 A04</span>
            <h4 style="color: #E85D75; margin: 0.5rem 0;">釣水球</h4>
            <p style="margin: 0.3rem 0;">親子同樂首選</p>
            <p style="color: #666; font-size: 0.85rem;">💰 遊戲券 x1</p>
        </div>
        """
        st.markdown(booth_html, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🍔 美食攤位")
    food_col1, food_col2 = st.columns(2)
    
    with food_col1:
        st.markdown("""
        <div class="booth-card">
            <span class="booth-number">攤位 B01</span>
            <h4 style="color: #F3722C;">台式小吃</h4>
            <p>蚵仔煎、臭豆腐、滷肉飯</p>
        </div>
        """, unsafe_allow_html=True)
    
    with food_col2:
        st.markdown("""
        <div class="booth-card">
            <span class="booth-number">攤位 B02</span>
            <h4 style="color: #F3722C;">飲料吧</h4>
            <p>珍珠奶茶、果汁、咖啡</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="booth-card">
        <span class="booth-number">攤位 C01-C10</span>
        <h4 style="color: #43AA8B;">手作文創區</h4>
        <p>10個優質文創品牌，手工皮件、陶藝、飾品等</p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="booth-card">
        <span class="booth-number">攤位 D01</span>
        <h4 style="color: #277DA1;">EVALUE 充電體驗區</h4>
        <p>最新充電技術展示，完成體驗送好禮</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== 活動時程 ====================
st.markdown('<div class="section-header"><h2>📅 活動時程表</h2></div>', unsafe_allow_html=True)

# 時程表
col1, col2 = st.columns([1, 1])

with col1:
    schedule_html = """
    <div class="schedule-item">
        <span class="time-badge">09:00 - 10:00</span>
        <h4 style="color: #E85D75;">報到時間</h4>
        <p>領取活動手冊、遊戲券</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">10:00 - 10:30</span>
        <h4 style="color: #E85D75;">開幕典禮</h4>
        <p>主持人開場、長官致詞</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">10:30 - 11:30</span>
        <h4 style="color: #F3722C;">魔術表演</h4>
        <p>國際級魔術師演出</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">11:30 - 12:30</span>
        <h4 style="color: #FDB143;">午餐時間</h4>
        <p>自由活動、享用美食</p>
    </div>
    """
    st.markdown(schedule_html, unsafe_allow_html=True)

with col2:
    schedule_html2 = """
    <div class="schedule-item">
        <span class="time-badge">12:30 - 13:00</span>
        <h4 style="color: #43AA8B;">第一波抽獎</h4>
        <p>iPhone 15、充電金回饋</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">13:00 - 14:00</span>
        <h4 style="color: #277DA1;">親子互動</h4>
        <p>大地遊戲、團康活動</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">15:00 - 15:30</span>
        <h4 style="color: #F3722C;">第二波抽獎</h4>
        <p>家電好禮、優惠券</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">16:30 - 17:00</span>
        <h4 style="color: #277DA1;">壓軸大抽獎</h4>
        <p>特斯拉充電一年份</p>
    </div>
    """
    st.markdown(schedule_html2, unsafe_allow_html=True)

st.markdown("---")

# ==================== 抽獎查詢 ====================
st.markdown('<div class="section-header"><h2>🎁 抽獎名單查詢</h2></div>', unsafe_allow_html=True)

# 抽獎批次選擇
lottery_batch = st.selectbox(
    "選擇抽獎批次",
    ["第一波抽獎 (12:30)", "第二波抽獎 (15:00)", "壓軸大抽獎 (16:30)"],
    key="lottery_select"
)

# 載入得獎名單
@st.cache_data
def load_lottery_data(batch):
    """載入抽獎名單資料"""
    try:
        if "第一波" in batch:
            df = pd.read_csv("lottery_round1.csv")
        elif "第二波" in batch:
            df = pd.read_csv("lottery_round2.csv")
        else:
            df = pd.read_csv("lottery_final.csv")
        return df
    except FileNotFoundError:
        # 建立示例資料
        sample_data = {
            "抽獎編號": ["A0001", "B0234", "C0567", "D0890", "E1234"],
            "獎項": ["iPhone 15 Pro", "充電金5000元", "充電金3000元", "充電金1000元", "精美禮品"],
            "姓名": ["王○明", "李○華", "張○文", "陳○美", "林○志"],
            "電話": ["0912****678", "0922****456", "0933****789", "0955****123", "0988****456"]
        }
        return pd.DataFrame(sample_data)

# 搜尋功能
col1, col2 = st.columns([3, 1])
with col1:
    search_number = st.text_input(
        "🔍 搜尋抽獎編號",
        placeholder="請輸入您的抽獎編號 (例：A0001)",
        key="search_input"
    )
with col2:
    search_button = st.button("查詢", type="primary", use_container_width=True, key="search_btn")

# 載入並顯示資料
df = load_lottery_data(lottery_batch)

if search_button and search_number:
    result = df[df["抽獎編號"] == search_number.upper()]
    if not result.empty:
        st.success(f"🎉 恭喜！您中獎了！")
        st.markdown(f"""
        <div class="highlight-box">
            <h3>中獎資訊</h3>
            <p><strong>抽獎編號：</strong>{result.iloc[0]['抽獎編號']}</p>
            <p><strong>獎項：</strong>{result.iloc[0]['獎項']}</p>
            <p><strong>姓名：</strong>{result.iloc[0]['姓名']}</p>
            <p><strong>領獎地點：</strong>服務台</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("😢 很抱歉，此編號未中獎或輸入錯誤")

# 顯示完整名單
with st.expander(f"📋 查看 {lottery_batch} 完整得獎名單"):
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# 領獎須知
st.markdown("""
<div class="info-box">
    <strong>📌 領獎須知：</strong>
    <ul style="margin-top: 0.5rem;">
        <li>請攜帶抽獎券存根及身分證件至服務台領獎</li>
        <li>領獎時間：活動當日 10:00 - 17:00</li>
        <li>逾時未領取視同放棄得獎資格</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================== 交通資訊 ====================
st.markdown('<div class="section-header"><h2>📍 交通資訊</h2></div>', unsafe_allow_html=True)

# 地址資訊
location_card = """
<div class="highlight-box">
    <h3>🏛️ 活動地點</h3>
    <p><strong>苗栗西湖渡假村 幸福廣場</strong></p>
    <p>地址：苗栗縣三義鄉西湖村西湖11號</p>
    <p>GPS：24.423046, 120.744301</p>
</div>
"""
st.markdown(location_card, unsafe_allow_html=True)

# 交通方式
st.markdown("### 🚗 交通方式")
tab1, tab2, tab3, tab4 = st.tabs(["🚗 自行開車", "🚌 接駁專車", "🚄 大眾運輸", "🅿️ 停車資訊"])

with tab1:
    drive_info = """
    <div class="activity-card">
        <h4 style="color: #E85D75;">國道一號（中山高）</h4>
        <p><strong>南下：</strong>三義交流道下 → 右轉台13線 → 前往西湖渡假村</p>
        <p><strong>北上：</strong>三義交流道下 → 左轉台13線 → 前往西湖渡假村</p>
        <p style="margin-top: 0.8rem;"><strong>車程時間：</strong></p>
        <ul style="margin-top: 0.3rem;">
            <li>台北出發：約2小時</li>
            <li>台中出發：約40分鐘</li>
            <li>高雄出發：約2.5小時</li>
        </ul>
    </div>
    """
    st.markdown(drive_info, unsafe_allow_html=True)

with tab2:
    shuttle_info = """
    <div class="activity-card">
        <h4 style="color: #F3722C;">免費接駁專車</h4>
        <p><strong>接駁點1：三義火車站</strong></p>
        <ul>
            <li>去程：08:30、09:00、09:30</li>
            <li>回程：16:30、17:00、17:30</li>
        </ul>
        <p style="margin-top: 0.8rem;"><strong>接駁點2：苗栗高鐵站</strong></p>
        <ul>
            <li>去程：08:45、09:15</li>
            <li>回程：16:45、17:15</li>
        </ul>
        <p style="color: #E85D75; margin-top: 0.8rem;">⚠️ 請事先預約，額滿為止</p>
    </div>
    """
    st.markdown(shuttle_info, unsafe_allow_html=True)

with tab3:
    public_info = """
    <div class="activity-card">
        <h4 style="color: #43AA8B;">大眾運輸</h4>
        <p><strong>🚂 火車</strong></p>
        <p>搭乘台鐵至「三義站」，轉乘接駁車（約10分鐘）</p>
        <p style="margin-top: 0.8rem;"><strong>🚄 高鐵</strong></p>
        <p>搭乘高鐵至「苗栗站」，轉乘接駁車（約20分鐘）</p>
        <p style="margin-top: 0.8rem;"><strong>🚌 客運</strong></p>
        <p>搭乘客運至苗栗轉運站，轉乘計程車前往</p>
    </div>
    """
    st.markdown(public_info, unsafe_allow_html=True)

with tab4:
    parking_info = """
    <div class="activity-card">
        <h4 style="color: #277DA1;">停車資訊</h4>
        <p><strong>會場停車場</strong></p>
        <ul>
            <li>提供 500 個免費停車位</li>
            <li>設有電動車充電專區（20個充電車位）</li>
        </ul>
        <p style="margin-top: 0.8rem;"><strong>臨時停車場</strong></p>
        <ul>
            <li>距離會場步行5分鐘</li>
            <li>提供 200 個備用停車位</li>
        </ul>
        <p style="color: #E85D75; margin-top: 0.8rem;">💡 建議提早抵達或搭乘大眾運輸</p>
    </div>
    """
    st.markdown(parking_info, unsafe_allow_html=True)

# 聯絡資訊
st.markdown("---")
st.markdown("### 📞 聯絡我們")

contact_col1, contact_col2 = st.columns(2)

with contact_col1:
    contact_info = """
    <div class="activity-card">
        <h4 style="color: #E85D75;">活動諮詢</h4>
        <p>📧 event@evalue.com.tw</p>
        <p>☎️ 0800-000-000</p>
        <p>週一至週五 09:00-18:00</p>
    </div>
    """
    st.markdown(contact_info, unsafe_allow_html=True)

with contact_col2:
    emergency_info = """
    <div class="activity-card">
        <h4 style="color: #F3722C;">活動當日緊急聯絡</h4>
        <p>📱 0912-345-678（總召）</p>
        <p>📱 0923-456-789（交通組）</p>
        <p>活動當日 08:00-18:00</p>
    </div>
    """
    st.markdown(emergency_info, unsafe_allow_html=True)


# ==================== 頁尾 ====================
st.markdown("---")
st.markdown('<div class="decoration">🎈 🎪 🎯 🎨 🎭 🎪 🎈</div>', unsafe_allow_html=True)

footer_html = """
<div style="text-align: center; padding: 2rem 1rem; color: #666;">
    <p>© 2025 EVALUE 充電嘉年華 | 綠能永續・共創未來 🌱</p>
    <p style="font-size: 0.9rem;">主辦單位：EVALUE 華城電能</p>
    <p style="font-size: 0.85rem; margin-top: 1rem;">
        📧 event@evalue.com.tw | ☎️ 0800-000-000
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

# 返回頂部按鈕（使用JavaScript）
back_to_top = """
<script>
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("backToTop").style.display = "block";
    } else {
        document.getElementById("backToTop").style.display = "none";
    }
}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
</script>

<button onclick="topFunction()" id="backToTop" class="back-to-top" title="返回頂部" style="display: none;">
    ↑
</button>
"""
st.markdown(back_to_top, unsafe_allow_html=True)
