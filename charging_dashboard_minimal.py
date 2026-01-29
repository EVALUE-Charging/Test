import streamlit as st
import pandas as pd
import numpy as np

# 頁面配置
st.set_page_config(
    page_title="充電站損益分析",
    page_icon="⚡",
    layout="wide"
)

# 標題
st.title("⚡ 充電站損益分析監控面板")
st.markdown("---")

# 建立範例資料的函數
@st.cache_data
def create_sample_data():
    data = {
        '月份': ['2025/12'] * 9,
        '負責人': ['Anita'] * 9,
        '站ID': ['BZ01', 'BZ00', 'EV01', 'SP02', 'SP03', 'SP04', 'SP05', 'SP07', 'SP09'],
        '名稱': [
            '賓航賓士_新北中和', '台隆賓士_台北濱江', '高雄鳳頂高爾夫練習場',
            '新竹科學園區_研發四路', '新竹科學園區_篤行會館', '新竹科學園區_弘道樓',
            '苗栗竹南科學園區_轉運站', '苗栗銅鑼科學園區', '桃園龍潭科學園區'
        ],
        '經營類型': ['關站(2025.12)', '關站(2025.12)', '自營', '自營', '自營', '自營', '自營', '自營', '自營'],
        '認列收入': [0, 0, 2587, 10408, 13194, 13917, 4383, 209, 8613],
        '認列成本': [3329, 3329, 4567, 25520, 26167, 27976, 19227, 14718, 14932],
        '損益': [-3329, -3329, -1980, -15112, -12973, -14059, -14844, -14509, -6319],
        '充電槍數': [2, 2, 1, 2, 2, 2, 2, 2, 2],
        '總充電度數': [1155.4, 736.4, 354.1, 1809.8, 1981.1, 1972.4, 621.9, 28.4, 1189.9]
    }
    return pd.DataFrame(data)

# 處理檔案上傳
def process_file(file):
    try:
        if file.name.endswith('.xlsx'):
            return pd.read_excel(file)
        elif file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            st.error("請上傳 .xlsx 或 .csv 檔案")
            return None
    except Exception as e:
        st.error(f"檔案讀取錯誤: {e}")
        return None

# 側邊欄
st.sidebar.header("📁 資料載入")
uploaded_file = st.sidebar.file_uploader("上傳損益資料檔案", type=['xlsx', 'csv'])

# 載入資料
if uploaded_file:
    df = process_file(uploaded_file)
    if df is None:
        st.stop()
else:
    st.sidebar.info("使用範例資料")
    df = create_sample_data()

# 檢查必要欄位
required_cols = ['負責人', '站ID', '名稱', '認列收入', '認列成本', '損益']
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"缺少必要欄位: {', '.join(missing_cols)}")
    st.stop()

# 篩選器
st.sidebar.header("🔍 篩選條件")
managers = ['全部'] + sorted(df['負責人'].unique().tolist())
selected_manager = st.sidebar.selectbox("負責人", managers)

if selected_manager != '全部':
    df = df[df['負責人'] == selected_manager]

# 主要指標
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df['認列收入'].sum()
    st.metric("💰 總營收", f"NT$ {total_revenue:,.0f}")

with col2:
    total_cost = df['認列成本'].sum()
    st.metric("💸 總成本", f"NT$ {total_cost:,.0f}")

with col3:
    total_profit = df['損益'].sum()
    st.metric("📊 總損益", f"NT$ {total_profit:,.0f}")

with col4:
    station_count = len(df)
    st.metric("🏢 站點數", f"{station_count} 站")

# 分頁
tab1, tab2, tab3 = st.tabs(["📊 總覽", "🏢 站點詳情", "📋 資料檢視"])

with tab1:
    st.subheader("各站點損益情況")
    
    # 損益圖表（使用簡單的條狀圖）
    chart_data = df.sort_values('損益')[['名稱', '損益']].set_index('名稱')
    st.bar_chart(chart_data)
    
    # 統計摘要
    st.subheader("統計摘要")
    col1, col2 = st.columns(2)
    
    with col1:
        profitable_stations = len(df[df['損益'] > 0])
        loss_stations = len(df[df['損益'] < 0])
        st.write(f"🟢 獲利站點: {profitable_stations} 站")
        st.write(f"🔴 虧損站點: {loss_stations} 站")
    
    with col2:
        if '經營類型' in df.columns:
            operation_summary = df.groupby('經營類型')['損益'].sum()
            st.write("**經營類型損益:**")
            for op_type, profit in operation_summary.items():
                icon = "🟢" if profit > 0 else "🔴"
                st.write(f"{icon} {op_type}: NT$ {profit:,.0f}")

with tab2:
    st.subheader("站點詳細資訊")
    
    # 站點選擇
    stations = df['名稱'].tolist()
    selected_stations = st.multiselect("選擇要檢視的站點", stations, default=stations[:3])
    
    for station in selected_stations:
        station_data = df[df['名稱'] == station].iloc[0]
        
        with st.expander(f"📍 {station}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**基本資訊**")
                st.write(f"🆔 站點ID: {station_data['站ID']}")
                st.write(f"👤 負責人: {station_data['負責人']}")
                if '經營類型' in df.columns:
                    st.write(f"🏷️ 經營類型: {station_data['經營類型']}")
            
            with col2:
                st.write("**營運數據**")
                if '充電槍數' in df.columns:
                    st.write(f"🔌 充電槍數: {station_data['充電槍數']}")
                if '總充電度數' in df.columns:
                    st.write(f"⚡ 充電度數: {station_data['總充電度數']:.1f} kWh")
            
            with col3:
                st.write("**財務資訊**")
                st.write(f"💰 收入: NT$ {station_data['認列收入']:,.0f}")
                st.write(f"💸 成本: NT$ {station_data['認列成本']:,.0f}")
                profit_color = "🟢" if station_data['損益'] > 0 else "🔴"
                st.write(f"{profit_color} 損益: NT$ {station_data['損益']:,.0f}")

with tab3:
    st.subheader("完整資料檢視")
    st.dataframe(df, use_container_width=True)
    
    # 下載功能
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 下載 CSV",
        data=csv,
        file_name="charging_station_data.csv",
        mime="text/csv"
    )

# 頁尾資訊
st.markdown("---")
st.markdown("**💡 使用說明:** 可上傳包含站點損益資料的 Excel 或 CSV 檔案進行分析")
st.markdown("**📊 版本:** v1.2.0 - 簡化穩定版")
