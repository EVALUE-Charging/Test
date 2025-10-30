import streamlit as st
from PIL import Image

# 設定頁面配置
st.set_page_config(
    page_title="2025 EVALUE Day 嘉年華",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義CSS樣式 - 嘉年華主題
css_styles = """
<style>
    /* 強制覆蓋深色模式，保持一致的亮色風格 */
    .stApp {
        background: linear-gradient(180deg, #fef9f3 0%, #fdf4e8 100%) !important;
        color: #2c2c2c !important;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.7) !important;
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        color: #2c2c2c !important;
    }
    
    /* 嘉年華漸層背景 - 固定白色文字 */
    .main-header {
        background: linear-gradient(135deg, #E85D75 0%, #F3722C 25%, #FDB143 50%, #43AA8B 75%, #277DA1 100%) !important;
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: gradient-shift 5s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main-header h1,
    .main-header p,
    .main-header small {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 活動卡片 - 固定亮色風格 */
    .activity-card {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border-left: 6px solid #F3722C;
        border-top: 2px solid #FDB143;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(10px);
        color: #2c2c2c !important;
    }
    
    .activity-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* 攤位卡片特殊樣式 */
    .booth-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,252,248,0.95)) !important;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
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
    
    .booth-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .booth-number {
        display: inline-block;
        background: linear-gradient(45deg, #E85D75, #F3722C);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    /* 時程表樣式 */
    .schedule-item {
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #43AA8B;
        transition: all 0.3s ease;
    }
    
    .schedule-item:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .time-badge {
        background: linear-gradient(45deg, #43AA8B, #277DA1);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin-bottom: 0.5rem;
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
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(232, 93, 117, 0.9), rgba(243, 114, 44, 0.9)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(232, 93, 117, 0.3) !important;
    }
    
    /* 側邊欄樣式 */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(253,250,246,0.95)) !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(253,250,246,0.95)) !important;
    }
    
    /* 導覽連結樣式 */
    .nav-link {
        display: block;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        background: rgba(255,255,255,0.8);
        border-radius: 10px;
        text-decoration: none;
        color: #2c2c2c;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;
    }
    
    .nav-link:hover {
        background: linear-gradient(90deg, rgba(67, 170, 139, 0.1), rgba(39, 125, 161, 0.1));
        border-left-color: #43AA8B;
        transform: translateX(5px);
    }
    
    /* 標題動畫 */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* 高亮框 */
    .highlight-box {
        background: linear-gradient(45deg, rgba(253, 177, 67, 0.9), rgba(243, 114, 44, 0.9)) !important;
        color: white !important;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(253, 177, 67, 0.2);
    }
    
    /* 資訊框 */
    .info-box {
        background: rgba(67, 170, 139, 0.1) !important;
        border-left: 4px solid #43AA8B !important;
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
        padding: 12px !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid rgba(253, 177, 67, 0.3) !important;
        padding: 10px !important;
        background: rgba(255, 255, 255, 0.8) !important;
        color: #2c2c2c !important;
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
        position: fixed;
        pointer-events: none;
        opacity: 0.1;
        z-index: 0;
    }
    
    .balloon {
        font-size: 3rem;
        animation: float 4s ease-in-out infinite;
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .booth-card,
        .activity-card,
        .schedule-item {
            margin-bottom: 1rem;
        }
    }
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# 側邊欄導覽
st.sidebar.markdown("## 🎪 導覽選單")
st.sidebar.markdown("---")

# 導覽選項
page = st.sidebar.radio(
    "選擇頁面",
    ["🏠 首頁", "🎪 攤位資訊", "📅 活動時程", "🎁 抽獎名單", "📍 交通資訊"],
    label_visibility="collapsed"
)

# Logo 處理
try:
    logo = Image.open("logo.png")
    st.sidebar.image(logo, use_container_width=True)
except:
    st.sidebar.markdown("### EVALUE")
    st.sidebar.markdown("##### 充電嘉年華")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 聯絡資訊")
st.sidebar.markdown("📧 service@evalue.com.tw")
st.sidebar.markdown("☎️ 0800-000-000")

# 主要內容區域
if page == "🏠 首頁":
    # 主標題
    header_html = """
    <div class="main-header">
        <h1 class="floating">🎪 2025 EVALUE Day 嘉年華 🎪</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">歡樂充電・綠能同行</p>
        <p style="font-size: 1rem; opacity: 0.9; margin-top: 0.5rem;">11月29日(六) 10:00-17:00 | 苗栗西湖渡假村 幸福廣場</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # 活動介紹
    col1, col2 = st.columns([1, 1])
    
    with col1:
        intro_card = """
        <div class="activity-card">
            <h3 style="color: #E85D75; margin-bottom: 1rem;">🎊 活動介紹</h3>
            <p>一年一度的 EVALUE Day 嘉年華即將盛大舉行！</p>
            <p>今年我們準備了更豐富的園遊會攤位、精彩的舞台表演，以及超值的抽獎活動。</p>
            <p>誠摯邀請所有 EVALUE 會員攜家帶眷，一同共襄盛舉！</p>
            <br>
            <p><strong>🎯 活動亮點：</strong></p>
            <ul>
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
            # 活動資訊卡片
            info_card = """
            <div class="highlight-box">
                <h3 style="color: white; margin-bottom: 1rem;">📌 活動資訊</h3>
                <p>📅 <strong>日期：</strong>2025年11月29日 (星期六)</p>
                <p>⏰ <strong>時間：</strong>10:00 - 17:00</p>
                <p>📍 <strong>地點：</strong>苗栗西湖渡假村 幸福廣場</p>
                <p>🎫 <strong>參加資格：</strong>EVALUE 會員及親友</p>
                <p>💰 <strong>費用：</strong>免費入場</p>
            </div>
            """
            st.markdown(info_card, unsafe_allow_html=True)
    
    # 快速導覽
    st.markdown("---")
    st.markdown("## 🚀 快速導覽")
    
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
    
    with nav_col1:
        st.markdown("""
        <div class="activity-card" style="text-align: center; cursor: pointer;">
            <h1 style="margin: 0;">🎪</h1>
            <h4 style="color: #E85D75;">攤位資訊</h4>
            <p style="font-size: 0.9rem; color: #666;">探索精彩攤位</p>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col2:
        st.markdown("""
        <div class="activity-card" style="text-align: center; cursor: pointer;">
            <h1 style="margin: 0;">📅</h1>
            <h4 style="color: #F3722C;">活動時程</h4>
            <p style="font-size: 0.9rem; color: #666;">查看時間表</p>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col3:
        st.markdown("""
        <div class="activity-card" style="text-align: center; cursor: pointer;">
            <h1 style="margin: 0;">🎁</h1>
            <h4 style="color: #43AA8B;">抽獎名單</h4>
            <p style="font-size: 0.9rem; color: #666;">得獎公布</p>
        </div>
        """, unsafe_allow_html=True)
    
    with nav_col4:
        st.markdown("""
        <div class="activity-card" style="text-align: center; cursor: pointer;">
            <h1 style="margin: 0;">📍</h1>
            <h4 style="color: #277DA1;">交通資訊</h4>
            <p style="font-size: 0.9rem; color: #666;">如何抵達</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 最新消息
    st.markdown("---")
    st.markdown("## 📢 最新消息")
    
    news_container = st.container()
    with news_container:
        st.info("🔔 【11/15】攤位配置圖已公布，請至「攤位資訊」查看")
        st.info("🔔 【11/10】第一波抽獎名單已公布！請至「抽獎名單」查看")
        st.info("🔔 【11/05】活動當天提供免費接駁車，詳見「交通資訊」")

elif page == "🎪 攤位資訊":
    st.markdown("""
    <div class="main-header">
        <h1>🎪 攤位資訊</h1>
        <p>精彩攤位等你來探索！</p>
    </div>
    """, unsafe_allow_html=True)
    
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
                <p>經典遊戲，豐富獎品等你拿！</p>
                <p style="color: #666; font-size: 0.9rem;">💰 遊戲券 x2</p>
            </div>
            
            <div class="booth-card">
                <span class="booth-number">攤位 A03</span>
                <h4 style="color: #E85D75; margin: 0.5rem 0;">彈珠檯</h4>
                <p>懷舊彈珠檯，重溫童年記憶</p>
                <p style="color: #666; font-size: 0.9rem;">💰 遊戲券 x1</p>
            </div>
            
            <div class="booth-card">
                <span class="booth-number">攤位 A05</span>
                <h4 style="color: #E85D75; margin: 0.5rem 0;">射飛鏢</h4>
                <p>考驗你的準度，射中靶心贏大獎</p>
                <p style="color: #666; font-size: 0.9rem;">💰 遊戲券 x2</p>
            </div>
            """
            st.markdown(booth_html, unsafe_allow_html=True)
        
        with game_col2:
            booth_html = """
            <div class="booth-card">
                <span class="booth-number">攤位 A02</span>
                <h4 style="color: #E85D75; margin: 0.5rem 0;">夾娃娃機</h4>
                <p>超可愛娃娃，保證正版授權</p>
                <p style="color: #666; font-size: 0.9rem;">💰 遊戲券 x3</p>
            </div>
            
            <div class="booth-card">
                <span class="booth-number">攤位 A04</span>
                <h4 style="color: #E85D75; margin: 0.5rem 0;">釣水球</h4>
                <p>親子同樂首選，人人有獎</p>
                <p style="color: #666; font-size: 0.9rem;">💰 遊戲券 x1</p>
            </div>
            
            <div class="booth-card">
                <span class="booth-number">攤位 A06</span>
                <h4 style="color: #E85D75; margin: 0.5rem 0;">VR 體驗區</h4>
                <p>最新 VR 遊戲，身歷其境的刺激體驗</p>
                <p style="color: #666; font-size: 0.9rem;">💰 免費體驗</p>
            </div>
            """
            st.markdown(booth_html, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🍔 美食攤位")
        
        food_col1, food_col2 = st.columns(2)
        
        with food_col1:
            booth_html = """
            <div class="booth-card">
                <span class="booth-number">攤位 B01</span>
                <h4 style="color: #F3722C; margin: 0.5rem 0;">台式小吃</h4>
                <p>蚵仔煎、臭豆腐、滷肉飯</p>
                <p style="color: #666; font-size: 0.9rem;">💰 餐券可用</p>
            </div>
            
            <div class="booth-card">
                <span class="booth-number">攤位 B03</span>
                <h4 style="color: #F3722C; margin: 0.5rem 0;">日式料理</h4>
                <p>壽司、拉麵、天婦羅</p>
                <p style="color: #666; font-size: 0.9rem;">💰 餐券可用</p>
            </div>
            """
            st.markdown(booth_html, unsafe_allow_html=True)
        
        with food_col2:
            booth_html = """
            <div class="booth-card">
                <span class="booth-number">攤位 B02</span>
                <h4 style="color: #F3722C; margin: 0.5rem 0;">飲料吧</h4>
                <p>珍珠奶茶、果汁、咖啡</p>
                <p style="color: #666; font-size: 0.9rem;">💰 餐券可用</p>
            </div>
            
            <div class="booth-card">
                <span class="booth-number">攤位 B04</span>
                <h4 style="color: #F3722C; margin: 0.5rem 0;">甜點站</h4>
                <p>雞蛋糕、棉花糖、冰淇淋</p>
                <p style="color: #666; font-size: 0.9rem;">💰 餐券可用</p>
            </div>
            """
            st.markdown(booth_html, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🛍️ 文創市集")
        st.markdown("""
        <div class="booth-card">
            <span class="booth-number">攤位 C01-C10</span>
            <h4 style="color: #43AA8B; margin: 0.5rem 0;">手作文創區</h4>
            <p>集結10個優質文創品牌，包括手工皮件、陶藝、飾品、香氛等</p>
            <p style="color: #666; font-size: 0.9rem;">💰 現金/行動支付</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 💡 綠能展示")
        st.markdown("""
        <div class="booth-card">
            <span class="booth-number">攤位 D01</span>
            <h4 style="color: #277DA1; margin: 0.5rem 0;">EVALUE 充電體驗區</h4>
            <p>最新充電技術展示，專業人員解說</p>
            <p>現場體驗充電，完成問卷送好禮</p>
            <p style="color: #666; font-size: 0.9rem;">💰 免費參觀</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 攤位地圖
    st.markdown("---")
    st.markdown("### 📍 攤位配置圖")
    
    map_info = """
    <div class="info-box">
        <strong>攤位配置說明：</strong>
        <ul style="margin-top: 0.5rem;">
            <li>A區：遊戲攤位（幸福廣場左側）</li>
            <li>B區：美食攤位（幸福廣場右側）</li>
            <li>C區：文創市集（幸福廣場後方）</li>
            <li>D區：綠能展示（幸福廣場入口）</li>
        </ul>
    </div>
    """
    st.markdown(map_info, unsafe_allow_html=True)

elif page == "📅 活動時程":
    st.markdown("""
    <div class="main-header">
        <h1>📅 活動時程表</h1>
        <p>精彩活動不間斷！</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 時程表
    st.markdown("### 🎭 舞台區活動")
    
    schedule_html = """
    <div class="schedule-item">
        <span class="time-badge">09:00 - 10:00</span>
        <h4 style="color: #E85D75; margin: 0.5rem 0;">報到時間</h4>
        <p>領取活動手冊、遊戲券、餐券</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">10:00 - 10:30</span>
        <h4 style="color: #E85D75; margin: 0.5rem 0;">開幕典禮</h4>
        <p>主持人開場、長官致詞、活動說明</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">10:30 - 11:30</span>
        <h4 style="color: #F3722C; margin: 0.5rem 0;">魔術表演</h4>
        <p>國際級魔術師精彩演出</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">11:30 - 12:30</span>
        <h4 style="color: #FDB143; margin: 0.5rem 0;">午餐時間</h4>
        <p>自由活動、享用美食</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">12:30 - 13:00</span>
        <h4 style="color: #43AA8B; margin: 0.5rem 0;">第一波抽獎</h4>
        <p>iPhone 15、充電金回饋等大獎</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">13:00 - 14:00</span>
        <h4 style="color: #277DA1; margin: 0.5rem 0;">親子互動遊戲</h4>
        <p>大地遊戲、團康活動</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">14:00 - 15:00</span>
        <h4 style="color: #E85D75; margin: 0.5rem 0;">樂團表演</h4>
        <p>Live Band 現場演唱</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">15:00 - 15:30</span>
        <h4 style="color: #F3722C; margin: 0.5rem 0;">第二波抽獎</h4>
        <p>家電好禮、充電優惠券</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">15:30 - 16:30</span>
        <h4 style="color: #43AA8B; margin: 0.5rem 0;">舞蹈表演</h4>
        <p>街舞、熱舞社團演出</p>
    </div>
    
    <div class="schedule-item">
        <span class="time-badge">16:30 - 17:00</span>
        <h4 style="color: #277DA1; margin: 0.5rem 0;">壓軸大抽獎 & 閉幕</h4>
        <p>特斯拉充電一年份、旅遊券等超級大獎</p>
    </div>
    """
    st.markdown(schedule_html, unsafe_allow_html=True)
    
    # 注意事項
    st.markdown("---")
    st.markdown("### ⚠️ 注意事項")
    
    notice_box = """
    <div class="info-box">
        <ul>
            <li>請於活動開始前完成報到，領取相關物品</li>
            <li>抽獎券請妥善保管，遺失恕不補發</li>
            <li>中獎者需在現場領獎，未到場視同放棄</li>
            <li>活動時程可能因現場狀況調整</li>
            <li>請遵守現場工作人員指示</li>
        </ul>
    </div>
    """
    st.markdown(notice_box, unsafe_allow_html=True)

elif page == "🎁 抽獎名單":
    st.markdown("""
    <div class="main-header">
        <h1>🎁 抽獎名單公布</h1>
        <p>恭喜所有得獎者！</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 抽獎批次選擇
    lottery_batch = st.selectbox(
        "選擇抽獎批次",
        ["第一波抽獎 (12:30)", "第二波抽獎 (15:00)", "壓軸大抽獎 (16:30)"]
    )
    
    # 載入得獎名單
    import pandas as pd
    
    @st.cache_data
    def load_lottery_data(batch):
        """載入抽獎名單資料"""
        try:
            # 根據批次載入不同的CSV檔案
            if "第一波" in batch:
                df = pd.read_csv("lottery_round1.csv")
            elif "第二波" in batch:
                df = pd.read_csv("lottery_round2.csv")
            else:
                df = pd.read_csv("lottery_final.csv")
            return df
        except FileNotFoundError:
            # 如果找不到檔案，建立示例資料
            sample_data = {
                "抽獎編號": ["A0001", "B0234", "C0567", "D0890", "E1234"],
                "獎項": ["iPhone 15 Pro", "充電金5000元", "充電金3000元", "充電金1000元", "精美禮品"],
                "姓名": ["王○明", "李○華", "張○文", "陳○美", "林○志"],
                "電話": ["0912****678", "0922****456", "0933****789", "0955****123", "0988****456"]
            }
            return pd.DataFrame(sample_data)
        except Exception as e:
            st.error(f"載入資料時發生錯誤: {str(e)}")
            return pd.DataFrame()
    
    # 搜尋功能
    col1, col2 = st.columns([3, 1])
    with col1:
        search_number = st.text_input(
            "🔍 搜尋抽獎編號",
            placeholder="請輸入您的抽獎編號 (例：A0001)"
        )
    with col2:
        search_button = st.button("查詢", type="primary", use_container_width=True)
    
    # 載入並顯示資料
    df = load_lottery_data(lottery_batch)
    
    if search_button and search_number:
        # 搜尋特定編號
        result = df[df["抽獎編號"] == search_number.upper()]
        if not result.empty:
            st.success(f"🎉 恭喜！您中獎了！")
            st.markdown(f"""
            <div class="highlight-box">
                <h3 style="color: white;">中獎資訊</h3>
                <p><strong>抽獎編號：</strong>{result.iloc[0]['抽獎編號']}</p>
                <p><strong>獎項：</strong>{result.iloc[0]['獎項']}</p>
                <p><strong>姓名：</strong>{result.iloc[0]['姓名']}</p>
                <p><strong>領獎地點：</strong>服務台</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("😢 很抱歉，此編號未中獎或輸入錯誤")
    
    # 顯示完整名單
    st.markdown("---")
    st.markdown(f"### 📋 {lottery_batch} - 完整得獎名單")
    
    if not df.empty:
        # 設定表格樣式
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "抽獎編號": st.column_config.TextColumn(
                    "抽獎編號",
                    width="medium",
                ),
                "獎項": st.column_config.TextColumn(
                    "獎項",
                    width="large",
                ),
                "姓名": st.column_config.TextColumn(
                    "姓名",
                    width="medium",
                ),
                "電話": st.column_config.TextColumn(
                    "電話",
                    width="medium",
                ),
            }
        )
        
        # 統計資訊
        st.markdown("---")
        st.markdown("### 📊 獎項統計")
        
        prize_stats = df["獎項"].value_counts()
        
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1:
            st.metric("總得獎人數", len(df))
        with stats_col2:
            st.metric("獎項種類", len(prize_stats))
        with stats_col3:
            if "iPhone" in df["獎項"].values[0]:
                st.metric("頭獎", "iPhone 15 Pro")
            else:
                st.metric("最大獎", df["獎項"].values[0])
    else:
        st.info("📢 得獎名單尚未公布，請稍後再查看")
    
    # 領獎須知
    st.markdown("---")
    st.markdown("### 📌 領獎須知")
    
    claim_info = """
    <div class="info-box">
        <strong>領獎注意事項：</strong>
        <ul style="margin-top: 0.5rem;">
            <li>請攜帶<strong>抽獎券存根</strong>及<strong>身分證件</strong>至服務台領獎</li>
            <li>領獎時間：活動當日 10:00 - 17:00</li>
            <li>逾時未領取視同放棄得獎資格</li>
            <li>獎品不得要求更換或折換現金</li>
            <li>如有爭議，主辦單位保留最終解釋權</li>
        </ul>
    </div>
    """
    st.markdown(claim_info, unsafe_allow_html=True)

elif page == "📍 交通資訊":
    st.markdown("""
    <div class="main-header">
        <h1>📍 交通資訊</h1>
        <p>如何抵達會場</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 地址資訊
    location_card = """
    <div class="highlight-box">
        <h3 style="color: white;">🏛️ 活動地點</h3>
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
            <h4 style="color: #E85D75;">國道一號（中山高速公路）</h4>
            <ol>
                <li>南下：三義交流道下 → 右轉台13線 → 沿指標前往西湖渡假村</li>
                <li>北上：三義交流道下 → 左轉台13線 → 沿指標前往西湖渡假村</li>
            </ol>
            <p style="margin-top: 1rem;"><strong>車程時間：</strong></p>
            <ul>
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
            <h4 style="color: #F3722C;">🚌 免費接駁專車</h4>
            <p>活動當日提供免費接駁服務</p>
            <hr style="margin: 1rem 0; opacity: 0.3;">
            
            <p><strong>接駁點1：三義火車站</strong></p>
            <ul>
                <li>去程：08:30、09:00、09:30</li>
                <li>回程：16:30、17:00、17:30</li>
            </ul>
            
            <p style="margin-top: 1rem;"><strong>接駁點2：苗栗高鐵站</strong></p>
            <ul>
                <li>去程：08:45、09:15</li>
                <li>回程：16:45、17:15</li>
            </ul>
            
            <p style="margin-top: 1rem; color: #E85D75;">
                ⚠️ 請事先預約接駁車，額滿為止
            </p>
        </div>
        """
        st.markdown(shuttle_info, unsafe_allow_html=True)
    
    with tab3:
        public_info = """
        <div class="activity-card">
            <h4 style="color: #43AA8B;">🚄 大眾運輸</h4>
            
            <p><strong>火車</strong></p>
            <ul>
                <li>搭乘台鐵至「三義站」下車</li>
                <li>轉乘接駁專車或計程車（約10分鐘）</li>
            </ul>
            
            <p style="margin-top: 1rem;"><strong>高鐵</strong></p>
            <ul>
                <li>搭乘高鐵至「苗栗站」下車</li>
                <li>轉乘接駁專車或計程車（約20分鐘）</li>
            </ul>
            
            <p style="margin-top: 1rem;"><strong>客運</strong></p>
            <ul>
                <li>國光客運、統聯客運等至苗栗轉運站</li>
                <li>轉乘計程車前往會場</li>
            </ul>
        </div>
        """
        st.markdown(public_info, unsafe_allow_html=True)
    
    with tab4:
        parking_info = """
        <div class="activity-card">
            <h4 style="color: #277DA1;">🅿️ 停車資訊</h4>
            
            <p><strong>會場停車場</strong></p>
            <ul>
                <li>提供 500 個免費停車位</li>
                <li>先到先停，額滿為止</li>
                <li>設有電動車充電專區（20個充電車位）</li>
            </ul>
            
            <p style="margin-top: 1rem;"><strong>臨時停車場</strong></p>
            <ul>
                <li>距離會場步行5分鐘</li>
                <li>提供 200 個備用停車位</li>
                <li>有接駁車往返會場</li>
            </ul>
            
            <p style="margin-top: 1rem; color: #E85D75;">
                💡 建議提早抵達或搭乘大眾運輸工具
            </p>
        </div>
        """
        st.markdown(parking_info, unsafe_allow_html=True)
    
    # 地圖
    st.markdown("---")
    st.markdown("### 🗺️ 會場地圖")
    
    # 這裡可以嵌入Google地圖或其他地圖服務
    map_placeholder = """
    <div class="info-box" style="text-align: center; padding: 2rem;">
        <p>🗺️ 互動式地圖</p>
        <p style="color: #666; font-size: 0.9rem;">
            <a href="https://goo.gl/maps/..." target="_blank">在 Google 地圖上查看</a>
        </p>
    </div>
    """
    st.markdown(map_placeholder, unsafe_allow_html=True)
    
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
            <p>服務時間：週一至週五 09:00-18:00</p>
        </div>
        """
        st.markdown(contact_info, unsafe_allow_html=True)
    
    with contact_col2:
        emergency_info = """
        <div class="activity-card">
            <h4 style="color: #F3722C;">活動當日緊急聯絡</h4>
            <p>📱 0912-345-678（活動總召）</p>
            <p>📱 0923-456-789（交通組）</p>
            <p>服務時間：活動當日 08:00-18:00</p>
        </div>
        """
        st.markdown(emergency_info, unsafe_allow_html=True)

# 頁尾
st.markdown("---")
footer_html = """
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>© 2025 EVALUE 充電嘉年華 | 綠能永續・共創未來 🌱</p>
    <p style="font-size: 0.9rem;">主辦單位：EVALUE 華城電能</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)