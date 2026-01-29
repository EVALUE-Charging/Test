#!/bin/bash

# 充電站損益分析監控面板啟動腳本

echo "⚡ 啟動充電站損益分析監控面板..."
echo "🔧 開發者: Claude Assistant"
echo "📅 版本: v1.0.0"
echo ""

# 檢查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python 版本: $python_version"

# 檢查是否安裝了所需的套件
echo "📦 檢查並安裝相依套件..."
pip3 install -r requirements_charging.txt --quiet

# 檢查安裝結果
if [ $? -eq 0 ]; then
    echo "✅ 套件安裝完成"
else
    echo "❌ 套件安裝失敗，請檢查 requirements_charging.txt"
    exit 1
fi

echo ""
echo "🚀 啟動 Streamlit 應用程式..."
echo "🌐 瀏覽器將自動開啟: http://localhost:8501"
echo "📊 請準備好你的損益資料.xlsx檔案進行上傳分析"
echo "⏹️  按 Ctrl+C 停止服務"
echo ""
echo "🔍 主要功能："
echo "   • 負責人別損益分析"
echo "   • 站點詳細營運數據"
echo "   • 成本結構拆解分析"
echo "   • 營收趨勢視覺化"
echo "   • 效率指標排行榜"
echo ""

# 啟動 Streamlit 應用程式
streamlit run charging_station_dashboard.py \
    --server.port 8501 \
    --server.headless false \
    --theme.base light \
    --theme.primaryColor "#667eea" \
    --theme.backgroundColor "#ffffff" \
    --theme.secondaryBackgroundColor "#f8f9ff"
