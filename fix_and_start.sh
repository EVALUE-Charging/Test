#!/bin/bash

# 充電站監控面板 - 一鍵修復和啟動腳本 v1.1
# 自動檢測和修復常見問題

echo "⚡ 充電站損益分析監控面板 - 自動修復工具"
echo "🔧 版本: v1.1.0"
echo "📅 更新: 2026-01-29"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查 Python 版本
echo "🔍 檢查系統環境..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo -e "${GREEN}✅ Python 版本: $python_version (符合需求)${NC}"
else
    echo -e "${RED}❌ Python 版本: $python_version (需要 $required_version 或更高)${NC}"
    echo -e "${YELLOW}請更新 Python 版本${NC}"
    exit 1
fi

# 檢查檔案是否存在
echo "📁 檢查必要檔案..."
files=("charging_station_dashboard_stable.py" "requirements_charging.txt")
missing_files=()

for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo -e "${RED}❌ 缺少檔案: ${missing_files[*]}${NC}"
    exit 1
else
    echo -e "${GREEN}✅ 所有必要檔案存在${NC}"
fi

# 檢查並安裝套件
echo "📦 檢查和安裝 Python 套件..."

# 檢查套件是否已安裝
check_package() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# 核心套件列表
core_packages=("streamlit" "pandas" "numpy")
optional_packages=("plotly" "openpyxl")

echo "🔧 安裝核心套件（必須）..."
for package in "${core_packages[@]}"; do
    if check_package "$package"; then
        echo -e "${GREEN}✅ $package 已安裝${NC}"
    else
        echo -e "${YELLOW}📥 安裝 $package...${NC}"
        pip3 install "$package" --quiet
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ $package 安裝成功${NC}"
        else
            echo -e "${RED}❌ $package 安裝失敗${NC}"
        fi
    fi
done

echo "🎨 安裝可選套件（增強功能）..."
for package in "${optional_packages[@]}"; do
    if check_package "$package"; then
        echo -e "${GREEN}✅ $package 已安裝${NC}"
    else
        echo -e "${YELLOW}📥 安裝 $package...${NC}"
        pip3 install "$package" --quiet
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ $package 安裝成功${NC}"
        else
            echo -e "${YELLOW}⚠️ $package 安裝失敗（功能會受限但仍可運行）${NC}"
        fi
    fi
done

# 最終檢查
echo ""
echo "🧪 進行最終檢查..."
python3 -c "
try:
    import streamlit
    import pandas
    import numpy
    print('✅ 核心套件檢查通過')
    
    try:
        import plotly
        print('✅ Plotly 可用 - 完整功能模式')
    except ImportError:
        print('⚠️ Plotly 不可用 - 基礎功能模式')
        
    print('🎯 系統準備就緒！')
except ImportError as e:
    print(f'❌ 套件檢查失敗: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 系統檢查失敗，請檢查錯誤訊息${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🚀 啟動充電站損益分析監控面板...${NC}"
echo -e "${BLUE}🌐 瀏覽器將自動開啟: http://localhost:8501${NC}"
echo -e "${BLUE}📊 請準備好你的損益資料.xlsx檔案進行分析${NC}"
echo -e "${BLUE}⏹️  按 Ctrl+C 停止服務${NC}"
echo ""
echo "💡 功能特色："
echo "   • 負責人別損益分析"
echo "   • 站點營運數據監控"
echo "   • 成本結構詳細拆解"
echo "   • 視覺化趨勢分析"
echo "   • 智能異常檢測"
echo ""
echo "🔧 如遇問題請參考 troubleshooting_guide.md"
echo ""

# 啟動應用程式（使用穩定版）
streamlit run charging_station_dashboard_stable.py \
    --server.port 8501 \
    --server.headless false \
    --theme.base light \
    --theme.primaryColor "#4CAF50" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f8f9ff" \
    2>/dev/null

# 如果穩定版失敗，嘗試最簡版本
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ 穩定版啟動失敗，嘗試基礎模式...${NC}"
    python3 -c "
import streamlit as st
st.set_page_config(page_title='充電站監控面板', page_icon='⚡')
st.title('⚡ 充電站損益分析監控面板')
st.error('啟動時遇到問題，請檢查以下項目：')
st.markdown('''
1. 確保已安裝所有必要套件
2. 檢查 Python 版本 (需要 3.7+)
3. 重新運行安裝腳本
4. 查看 troubleshooting_guide.md 獲取更多幫助
''')
st.info('請聯繫技術支援獲得協助')
" > minimal_app.py
    streamlit run minimal_app.py --server.port 8501
fi
