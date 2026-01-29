#!/bin/bash

echo "⚡ 充電站監控面板 - 簡化版啟動"
echo ""

# 安裝基本套件
echo "📦 安裝必要套件..."
pip3 install streamlit pandas numpy openpyxl --quiet

if [ $? -eq 0 ]; then
    echo "✅ 套件安裝完成"
else
    echo "❌ 套件安裝失敗"
    echo "請手動執行: pip install streamlit pandas numpy openpyxl"
    exit 1
fi

echo ""
echo "🚀 啟動應用程式..."
echo "🌐 瀏覽器將開啟: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止"
echo ""

# 啟動最簡版應用程式
streamlit run charging_dashboard_minimal.py --server.port 8501
