import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io

# 設定頁面配置
st.set_page_config(
    page_title="充電站損益分析面板",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂CSS樣式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .cost-breakdown {
        background: linear-gradient(45deg, #f8f9ff, #e8f0fe);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e3f2fd;
    }
    
    .station-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .station-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .profit-positive { border-left: 4px solid #4caf50; }
    .profit-negative { border-left: 4px solid #f44336; }
    .profit-neutral { border-left: 4px solid #ff9800; }
    
    .stSelectbox > div > div {
        background-color: #f8f9ff;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """載入範例數據"""
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
        '損益率': [np.inf, np.inf, -0.765365288, -1.451960031, -0.983249962, -1.010203348, -3.386721424, -69.42105263, -0.733658423]
    }
    
    return pd.DataFrame(data)

def process_uploaded_file(uploaded_file):
    """處理上傳的Excel文件"""
    try:
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
            return None
            
        return df
    except Exception as e:
        st.error(f"讀取文件時發生錯誤: {str(e)}")
        return None

def create_cost_breakdown_chart(station_data):
    """創建成本結構圖表"""
    cost_columns = ['共同分攤', '電費分潤成本', '設備攤提', '租金', '監視系統費', '保險費', '派工費用', '領料/設備', '其他成本', '標案成本']
    
    costs = []
    labels = []
    
    for col in cost_columns:
        if col in station_data.columns:
            value = station_data[col].iloc[0] if len(station_data) > 0 else 0
            if value > 0:
                costs.append(value)
                labels.append(col)
    
    if not costs:
        return None
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=costs,
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>金額: %{value:,.0f}<br>占比: %{percent}<extra></extra>',
            marker=dict(colors=px.colors.qualitative.Set3)
        )
    ])
    
    fig.update_layout(
        title=f"成本結構分析 - {station_data['名稱'].iloc[0]}",
        font=dict(size=12),
        height=400
    )
    
    return fig

def main():
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
        df = process_uploaded_file(uploaded_file)
        if df is None:
            return
    else:
        st.sidebar.info("使用範例數據進行展示")
        df = load_sample_data()
    
    # 側邊欄篩選器
    st.sidebar.header("🔍 篩選條件")
    
    # 負責人篩選
    managers = sorted(df['負責人'].unique())
    selected_manager = st.sidebar.selectbox("選擇負責人", ['全部'] + managers)
    
    # 月份篩選
    months = sorted(df['月份'].unique())
    selected_month = st.sidebar.selectbox("選擇月份", ['全部'] + months)
    
    # 經營類型篩選
    operation_types = sorted(df['經營類型'].unique())
    selected_operation = st.sidebar.selectbox("經營類型", ['全部'] + operation_types)
    
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
        st.markdown(f"""
            <div class="metric-card">
                <h3>💰 總營收</h3>
                <h2>NT$ {total_revenue:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h3>💸 總成本</h3>
                <h2>NT$ {total_cost:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        profit_class = "profit-positive" if total_profit > 0 else "profit-negative"
        st.markdown(f"""
            <div class="metric-card {profit_class}">
                <h3>📊 總損益</h3>
                <h2>NT$ {total_profit:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <h3>🏢 站點數量</h3>
                <h2>{station_count} 站</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # 主要內容區域
    tab1, tab2, tab3, tab4 = st.tabs(["📊 總覽分析", "🏢 站點詳情", "💹 營收趨勢", "🔧 成本分析"])
    
    with tab1:
        # 損益分布圖表
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 各站損益對比
            fig_profit = px.bar(
                filtered_df.sort_values('損益'),
                x='損益',
                y='名稱',
                orientation='h',
                color='損益',
                color_continuous_scale=['red', 'yellow', 'green'],
                title="各站點損益對比",
                labels={'損益': '損益 (NT$)', '名稱': '站點名稱'}
            )
            fig_profit.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_profit, use_container_width=True)
        
        with col2:
            # 經營類型分布
            operation_summary = filtered_df.groupby('經營類型').agg({
                '損益': 'sum',
                '站ID': 'count'
            }).reset_index()
            operation_summary.columns = ['經營類型', '總損益', '站點數']
            
            fig_pie = px.pie(
                operation_summary,
                values='站點數',
                names='經營類型',
                title="經營類型分布"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("### 📈 經營類型績效")
            for _, row in operation_summary.iterrows():
                profit_icon = "🔴" if row['總損益'] < 0 else "🟢"
                st.markdown(f"""
                    **{row['經營類型']}** {profit_icon}  
                    站點數: {row['站點數']}  
                    總損益: NT$ {row['總損益']:,.0f}
                """)
    
    with tab2:
        st.markdown("### 🏢 站點詳細資訊")
        
        # 站點選擇
        station_options = filtered_df['名稱'].tolist()
        selected_stations = st.multiselect(
            "選擇要檢視的站點",
            station_options,
            default=station_options[:3] if len(station_options) >= 3 else station_options
        )
        
        if selected_stations:
            for station_name in selected_stations:
                station_data = filtered_df[filtered_df['名稱'] == station_name]
                if len(station_data) > 0:
                    row = station_data.iloc[0]
                    
                    profit_class = "profit-positive" if row['損益'] > 0 else ("profit-negative" if row['損益'] < 0 else "profit-neutral")
                    
                    with st.expander(f"📍 {station_name}", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                                **基本資訊**  
                                🆔 站點ID: {row['站ID']}  
                                👤 負責人: {row['負責人']}  
                                📅 啟用日期: {row['啟用日期']}  
                                🏷️ 經營類型: {row['經營類型']}  
                                ⚡ 站點規格: {row['站點規格']}  
                                📍 POI類型: {row['POI']}
                            """)
                        
                        with col2:
                            st.markdown(f"""
                                **營運數據**  
                                🔌 充電槍數: {row['充電槍數']}  
                                ⚡ 全站功率: {row['全站功率']} kW  
                                📊 總充電度數: {row['總充電度數']:.1f} kWh  
                                ✅ 成功充電: {row['成功充電次數']} 次  
                                ❌ 失敗充電: {row['失敗充電次數']} 次  
                                📈 稼動率: {row['稼動率']:.2%}
                            """)
                        
                        with col3:
                            profit_color = "green" if row['損益'] > 0 else "red"
                            st.markdown(f"""
                                **財務績效**  
                                💰 認列收入: NT$ {row['認列收入']:,.0f}  
                                💸 認列成本: NT$ {row['認列成本']:,.0f}  
                                <span style="color: {profit_color}; font-weight: bold;">📊 損益: NT$ {row['損益']:,.0f}</span>  
                                📉 損益率: {row['損益率']:.2%}  
                                🔄 周轉率: {row['周轉率']:.2%}  
                                ⚠️ 失敗率: {row['失敗率']:.2%}
                            """, unsafe_allow_html=True)
                        
                        # 成本結構圖表
                        cost_chart = create_cost_breakdown_chart(station_data)
                        if cost_chart:
                            st.plotly_chart(cost_chart, use_container_width=True)
    
    with tab3:
        st.markdown("### 💹 營收趨勢分析")
        
        if len(filtered_df) > 1:
            # 營收 vs 成本散點圖
            fig_scatter = px.scatter(
                filtered_df,
                x='認列收入',
                y='認列成本',
                size='總充電度數',
                color='損益',
                hover_name='名稱',
                title="營收 vs 成本關係圖",
                labels={'認列收入': '營收 (NT$)', '認列成本': '成本 (NT$)'},
                color_continuous_scale=['red', 'yellow', 'green']
            )
            
            # 添加損益平衡線
            max_value = max(filtered_df['認列收入'].max(), filtered_df['認列成本'].max())
            fig_scatter.add_shape(
                type="line",
                x0=0, y0=0, x1=max_value, y1=max_value,
                line=dict(color="gray", width=2, dash="dash"),
                name="損益平衡線"
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # 效率指標分析
            col1, col2 = st.columns(2)
            
            with col1:
                fig_efficiency = px.bar(
                    filtered_df.nlargest(10, '稼動率'),
                    x='稼動率',
                    y='名稱',
                    orientation='h',
                    title="稼動率排行 (前10名)",
                    labels={'稼動率': '稼動率', '名稱': '站點名稱'}
                )
                st.plotly_chart(fig_efficiency, use_container_width=True)
            
            with col2:
                fig_turnover = px.bar(
                    filtered_df.nlargest(10, '周轉率'),
                    x='周轉率',
                    y='名稱',
                    orientation='h',
                    title="周轉率排行 (前10名)",
                    labels={'周轉率': '周轉率', '名稱': '站點名稱'}
                )
                st.plotly_chart(fig_turnover, use_container_width=True)
        else:
            st.info("需要多個站點的數據才能顯示趨勢分析")
    
    with tab4:
        st.markdown("### 🔧 成本結構分析")
        
        cost_columns = ['共同分攤', '電費分潤成本', '設備攤提', '租金', '監視系統費', '保險費', '派工費用', '領料/設備', '其他成本', '標案成本']
        
        # 計算各成本項目的總計
        cost_summary = {}
        for col in cost_columns:
            if col in filtered_df.columns:
                total = filtered_df[col].sum()
                if total > 0:
                    cost_summary[col] = total
        
        if cost_summary:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # 總成本結構餅圖
                fig_total_cost = go.Figure(data=[
                    go.Pie(
                        labels=list(cost_summary.keys()),
                        values=list(cost_summary.values()),
                        hole=0.4,
                        textinfo='label+percent',
                        hovertemplate='<b>%{label}</b><br>金額: NT$ %{value:,.0f}<br>占比: %{percent}<extra></extra>',
                        marker=dict(colors=px.colors.qualitative.Pastel)
                    )
                ])
                
                fig_total_cost.update_layout(
                    title="整體成本結構分析",
                    font=dict(size=12),
                    height=400
                )
                
                st.plotly_chart(fig_total_cost, use_container_width=True)
            
            with col2:
                # 成本明細表
                st.markdown("#### 💰 成本明細")
                cost_df = pd.DataFrame(list(cost_summary.items()), columns=['成本項目', '總金額'])
                cost_df['占比'] = (cost_df['總金額'] / cost_df['總金額'].sum() * 100).round(1)
                cost_df['總金額'] = cost_df['總金額'].apply(lambda x: f"NT$ {x:,.0f}")
                cost_df['占比'] = cost_df['占比'].apply(lambda x: f"{x}%")
                
                st.dataframe(cost_df, hide_index=True, use_container_width=True)
        
        # 各站成本效率分析
        st.markdown("#### 📊 成本效率排行")
        
        # 計算每度電成本
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['每度電成本'] = filtered_df_copy.apply(
            lambda row: row['認列成本'] / row['總充電度數'] if row['總充電度數'] > 0 else 0, axis=1
        )
        
        # 顯示成本效率最佳和最差的站點
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💚 成本效率最佳 (前5名)**")
            best_efficiency = filtered_df_copy[filtered_df_copy['每度電成本'] > 0].nsmallest(5, '每度電成本')
            for _, row in best_efficiency.iterrows():
                st.markdown(f"📍 **{row['名稱']}**  \n每度電成本: NT$ {row['每度電成本']:.2f}")
        
        with col2:
            st.markdown("**🔴 成本效率待改善 (後5名)**")
            worst_efficiency = filtered_df_copy[filtered_df_copy['每度電成本'] > 0].nlargest(5, '每度電成本')
            for _, row in worst_efficiency.iterrows():
                st.markdown(f"📍 **{row['名稱']}**  \n每度電成本: NT$ {row['每度電成本']:.2f}")
    
    # 資料表格檢視
    st.markdown("---")
    st.markdown("### 📋 完整數據檢視")
    
    if st.checkbox("顯示原始數據"):
        st.dataframe(filtered_df, use_container_width=True)
        
        # 匯出功能
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下載 CSV 檔案",
            data=csv,
            file_name=f"充電站損益分析_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
