# -*- coding: utf-8 -*-
"""
充電站損益分析監控面板 - 穩定版
作者: Claude Assistant
版本: v1.1.0
"""

# 套件導入和錯誤處理
try:
    import streamlit as st
    import pandas as pd
    import numpy as np
    from datetime import datetime
    import io
    
    # 嘗試導入 plotly，如果失敗則使用 matplotlib
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        PLOTLY_AVAILABLE = True
    except ImportError:
        import matplotlib.pyplot as plt
        import seaborn as sns
        PLOTLY_AVAILABLE = False
        st.warning("⚠️ Plotly 未安裝，使用 Matplotlib 作為替代方案")
        
except ImportError as e:
    st.error(f"""
    ❌ 錯誤：缺少必要的套件 - {e}
    
    請執行以下指令安裝所需套件：
    ```
    pip install streamlit pandas numpy matplotlib seaborn openpyxl
    ```
    
    如需完整功能，請額外安裝：
    ```
    pip install plotly
    ```
    """)
    st.stop()

# 設定頁面配置
st.set_page_config(
    page_title="充電站損益分析面板",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂CSS樣式（簡化版）
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .profit-positive { border-left: 4px solid #4caf50; }
    .profit-negative { border-left: 4px solid #f44336; }
    .profit-neutral { border-left: 4px solid #ff9800; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """載入範例數據"""
    try:
        data = {
            '月份': ['2025/12'] * 9,
            '負責人': ['Anita'] * 9,
            '站ID': ['BZ01', 'BZ00', 'EV01', 'SP02', 'SP03', 'SP04', 'SP05', 'SP07', 'SP09'],
            '經營類型': ['關站(2025.12)', '關站(2025.12)', '自營', '自營', '自營', '自營', '自營', '自營', '自營'],
            '站點規格': ['純DC站', '純DC站', '純AC站', '純AC站', '純AC站', '純AC站', '純AC站', '純AC站', '純AC站'],
            'POI': ['車廠', '車廠', '高球場', '科學園區', '科學園區', '科學園區', '科學園區', '科學園區', '科學園區'],
            '啟用日期': ['2020/04/18', '2020/05/07', '2020/06/18', '2020/07/21', '2020/07/21', '2020/07/22', '2020/07/23', '2020/07/24', '2020/07/27'],
            '名稱': ['賓航賓士_新北中和', '台隆賓士_台北濱江', '高雄鳳頂高爾夫練習場', '新竹科學園區_研發四路', 
                    '新竹科學園區_篤行會館', '新竹科學園區_弘道樓', '苗栗竹南科學園區_轉運站', '苗栗銅鑼科學園區', '桃園龍潭科學園區'],
            '充電槍數': [2, 2, 1, 2, 2, 2, 2, 2, 2],
            '全站功率': [120, 120, 7, 18, 18, 18, 18, 18, 18],
            '總充電度數': [1155.404, 736.404, 354.126, 1809.834, 1981.056, 1972.36, 621.94, 28.408, 1189.852],
            'AC度數': [0, 0, 354.126, 1809.834, 1981.056, 1972.36, 621.94, 28.408, 1189.852],
            'DC度數': [1155.404, 736.404, 0, 0, 0, 0, 0, 0, 0],
            '總充電次數': [35, 23, 22, 108, 99, 120, 41, 4, 62],
            '成功充電次數': [35, 22, 21, 107, 98, 112, 38, 4, 62],
            '失敗充電次數': [0, 1, 1, 1, 1, 8, 3, 0, 0],
            '認列收入': [0, 0, 2587, 10408, 13194, 13917, 4383, 209, 8613],
            '認列成本': [3329, 3329, 4567, 25520, 26167, 27976, 19227, 14718, 14932],
            '共同分攤': [3178, 3178, 3178, 3178, 3178, 3178, 3178, 3178, 3178],
            '電費分潤成本': [0, 0, 0, 19429, 19854, 21547, 12784, 8405, 8405],
            '設備攤提': [0, 0, 1238, 2762, 2984, 3100, 3114, 2984, 3198],
            '租金': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            '監視系統費': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            '保險費': [151, 151, 151, 151, 151, 151, 151, 151, 151],
            '派工費用': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            '領料/設備': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            '其他成本': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            '標案成本': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            '稼動率': [0.564516129, 0.35483871, 0.677419355, 1.725806452, 1.580645161, 1.806451613, 0.612903226, 0.064516129, 1],
            '周轉率': [0.016176691, 0.010310316, 0.08499568, 0.168928651, 0.184910394, 0.184098716, 0.058051449, 0.002651583, 0.111059961],
            '失敗率': [0, 0.043478261, 0.045454545, 0.009259259, 0.01010101, 0.066666667, 0.073170732, 0, 0],
            '損益': [-3329, -3329, -1980, -15112, -12973, -14059, -14844, -14509, -6319],
            '損益率': [float('inf'), float('inf'), -0.765365288, -1.451960031, -0.983249962, -1.010203348, -3.386721424, -69.42105263, -0.733658423]
        }
        
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"載入範例數據時發生錯誤: {e}")
        return None

def safe_process_uploaded_file(uploaded_file):
    """安全地處理上傳的Excel文件"""
    try:
        if uploaded_file is None:
            return None
            
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("請上傳 .xlsx 或 .csv 格式的文件")
            return None
        
        # 檢查必要欄位
        required_columns = ['月份', '負責人', '站ID', '名稱', '認列收入', '認列成本', '損益']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"文件缺少必要欄位: {', '.join(missing_columns)}")
            st.info("必要欄位包括：月份, 負責人, 站ID, 名稱, 認列收入, 認列成本, 損益")
            return None
            
        return df
    except Exception as e:
        st.error(f"讀取文件時發生錯誤: {str(e)}")
        return None

def create_simple_bar_chart(data, x_col, y_col, title):
    """創建簡單的柱狀圖（兼容版本）"""
    if PLOTLY_AVAILABLE:
        fig = px.bar(data, x=x_col, y=y_col, title=title)
        return fig
    else:
        # 使用 matplotlib 作為後備方案
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(data[y_col], data[x_col])
        ax.set_title(title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        plt.xticks(rotation=45)
        return fig

def main():
    """主要應用程式邏輯"""
    try:
        # 主標題
        st.markdown("""
            <div class="main-header">
                <h1>⚡ 充電站損益分析監控面板</h1>
                <p>智能化站點營運監控與成本分析系統</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 文件上傳區域
        st.sidebar.header("📁 數據載入")
        uploaded_file = st.sidebar.file_uploader(
            "上傳損益資料檔案",
            type=['xlsx', 'csv'],
            help="請上傳包含充電站損益數據的 Excel 或 CSV 文件"
        )
        
        # 載入數據
        if uploaded_file is not None:
            df = safe_process_uploaded_file(uploaded_file)
            if df is None:
                st.stop()
        else:
            st.sidebar.info("使用範例數據進行展示")
            df = load_sample_data()
            if df is None:
                st.error("無法載入範例數據")
                st.stop()
        
        # 側邊欄篩選器
        st.sidebar.header("🔍 篩選條件")
        
        # 負責人篩選
        managers = ['全部'] + sorted(df['負責人'].unique().tolist())
        selected_manager = st.sidebar.selectbox("選擇負責人", managers)
        
        # 月份篩選
        months = ['全部'] + sorted(df['月份'].unique().tolist())
        selected_month = st.sidebar.selectbox("選擇月份", months)
        
        # 經營類型篩選
        operation_types = ['全部'] + sorted(df['經營類型'].unique().tolist())
        selected_operation = st.sidebar.selectbox("經營類型", operation_types)
        
        # 應用篩選條件
        filtered_df = df.copy()
        if selected_manager != '全部':
            filtered_df = filtered_df[filtered_df['負責人'] == selected_manager]
        if selected_month != '全部':
            filtered_df = filtered_df[filtered_df['月份'] == selected_month]
        if selected_operation != '全部':
            filtered_df = filtered_df[filtered_df['經營類型'] == selected_operation]
        
        if len(filtered_df) == 0:
            st.warning("沒有符合篩選條件的數據")
            return
        
        # 主要指標卡片
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = filtered_df['認列收入'].sum()
        total_cost = filtered_df['認列成本'].sum()
        total_profit = filtered_df['損益'].sum()
        station_count = len(filtered_df)
        
        with col1:
            st.metric("💰 總營收", f"NT$ {total_revenue:,.0f}")
        
        with col2:
            st.metric("💸 總成本", f"NT$ {total_cost:,.0f}")
        
        with col3:
            profit_delta = "📈" if total_profit > 0 else "📉"
            st.metric("📊 總損益", f"NT$ {total_profit:,.0f}", delta=profit_delta)
        
        with col4:
            st.metric("🏢 站點數量", f"{station_count} 站")
        
        # 主要內容區域
        tab1, tab2, tab3 = st.tabs(["📊 總覽分析", "🏢 站點詳情", "📋 數據檢視"])
        
        with tab1:
            st.subheader("各站點損益對比")
            
            # 損益排序
            profit_df = filtered_df.sort_values('損益', ascending=True)
            
            if PLOTLY_AVAILABLE:
                fig = px.bar(
                    profit_df,
                    x='損益',
                    y='名稱',
                    orientation='h',
                    title="各站點損益對比",
                    color='損益',
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # matplotlib 版本
                fig, ax = plt.subplots(figsize=(12, 8))
                colors = ['red' if x < 0 else 'green' for x in profit_df['損益']]
                ax.barh(profit_df['名稱'], profit_df['損益'], color=colors)
                ax.set_title("各站點損益對比")
                ax.set_xlabel("損益 (NT$)")
                plt.tight_layout()
                st.pyplot(fig)
            
            # 經營類型統計
            st.subheader("經營類型統計")
            operation_summary = filtered_df.groupby('經營類型').agg({
                '損益': 'sum',
                '站ID': 'count',
                '認列收入': 'sum'
            }).reset_index()
            operation_summary.columns = ['經營類型', '總損益', '站點數', '總營收']
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(operation_summary, hide_index=True)
            
            with col2:
                for _, row in operation_summary.iterrows():
                    profit_icon = "🔴" if row['總損益'] < 0 else "🟢"
                    st.markdown(f"""
                        **{row['經營類型']}** {profit_icon}  
                        - 站點數: {row['站點數']}  
                        - 總營收: NT$ {row['總營收']:,.0f}  
                        - 總損益: NT$ {row['總損益']:,.0f}
                    """)
        
        with tab2:
            st.subheader("🏢 站點詳細資訊")
            
            # 站點選擇
            station_options = filtered_df['名稱'].tolist()
            selected_stations = st.multiselect(
                "選擇要檢視的站點（最多選擇5個）",
                station_options,
                default=station_options[:min(3, len(station_options))]
            )
            
            if selected_stations:
                for station_name in selected_stations[:5]:  # 限制最多顯示5個
                    station_data = filtered_df[filtered_df['名稱'] == station_name]
                    if len(station_data) > 0:
                        row = station_data.iloc[0]
                        
                        with st.expander(f"📍 {station_name}", expanded=len(selected_stations) <= 2):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("**基本資訊**")
                                st.write(f"🆔 站點ID: {row['站ID']}")
                                st.write(f"👤 負責人: {row['負責人']}")
                                st.write(f"📅 啟用日期: {row['啟用日期']}")
                                st.write(f"🏷️ 經營類型: {row['經營類型']}")
                                st.write(f"⚡ 站點規格: {row['站點規格']}")
                                st.write(f"📍 POI類型: {row['POI']}")
                            
                            with col2:
                                st.markdown("**營運數據**")
                                st.write(f"🔌 充電槍數: {row['充電槍數']}")
                                st.write(f"⚡ 全站功率: {row['全站功率']} kW")
                                st.write(f"📊 總充電度數: {row['總充電度數']:.1f} kWh")
                                st.write(f"✅ 成功充電: {row['成功充電次數']} 次")
                                st.write(f"❌ 失敗充電: {row['失敗充電次數']} 次")
                                st.write(f"📈 稼動率: {row['稼動率']:.2%}")
                            
                            with col3:
                                st.markdown("**財務績效**")
                                st.write(f"💰 認列收入: NT$ {row['認列收入']:,.0f}")
                                st.write(f"💸 認列成本: NT$ {row['認列成本']:,.0f}")
                                profit_color = "🟢" if row['損益'] > 0 else "🔴"
                                st.write(f"{profit_color} 損益: NT$ {row['損益']:,.0f}")
                                if not np.isinf(row['損益率']):
                                    st.write(f"📉 損益率: {row['損益率']:.2%}")
                                st.write(f"🔄 周轉率: {row['周轉率']:.2%}")
                                st.write(f"⚠️ 失敗率: {row['失敗率']:.2%}")
            else:
                st.info("請選擇要檢視的站點")
        
        with tab3:
            st.subheader("📋 完整數據檢視")
            
            # 顯示篩選後的數據
            st.write(f"目前顯示 {len(filtered_df)} 筆記錄")
            st.dataframe(filtered_df, use_container_width=True, height=400)
            
            # 匯出功能
            if st.button("📥 準備下載 CSV 檔案"):
                csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="⬇️ 下載 CSV 檔案",
                    data=csv,
                    file_name=f"充電站損益分析_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        # 版本資訊
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
            **📝 版本資訊**  
            版本: v1.1.0  
            更新: 2026/01/29  
            開發: Claude Assistant
        """)
        
    except Exception as e:
        st.error(f"應用程式執行時發生錯誤: {str(e)}")
        st.markdown("請嘗試重新載入頁面或檢查數據格式")

if __name__ == "__main__":
    main()
