# 🔧 充電站監控面板 - 問題修復指南

## 🚨 常見錯誤解決方案

### 錯誤 1: "ModuleNotFoundError: No module named 'streamlit'"

**問題**：缺少必要的 Python 套件

**解決方案**：
```bash
# 安裝基本套件（必須）
pip install streamlit pandas numpy openpyxl

# 安裝完整功能套件（推薦）
pip install streamlit pandas plotly numpy openpyxl xlsxwriter matplotlib seaborn
```

### 錯誤 2: "Oh no. Error running app."

**可能原因和解決方案**：

#### 原因 1：套件版本衝突
```bash
# 建立虛擬環境（推薦）
python -m venv charging_env
source charging_env/bin/activate  # Linux/Mac
# 或 charging_env\Scripts\activate  # Windows

# 重新安裝套件
pip install -r requirements_charging.txt
```

#### 原因 2：Python 版本不相容
```bash
# 檢查 Python 版本（需要 3.7+）
python --version

# 如果版本太舊，請更新 Python
```

#### 原因 3：文件編碼問題
- 確保所有檔案都使用 UTF-8 編碼
- 避免檔名包含特殊字元

## 🚀 推薦的啟動流程

### 方法 1：使用穩定版本（推薦）
```bash
# 使用修復版本
streamlit run charging_station_dashboard_stable.py
```

### 方法 2：最小安裝
```bash
# 只安裝核心套件
pip install streamlit pandas numpy
streamlit run charging_station_dashboard_stable.py
```

### 方法 3：完整安裝
```bash
# 安裝所有功能套件
pip install streamlit pandas plotly numpy openpyxl xlsxwriter matplotlib seaborn
streamlit run charging_station_dashboard.py
```

## 🔍 除錯步驟

1. **檢查 Python 版本**
   ```bash
   python --version
   # 需要 Python 3.7 或更高版本
   ```

2. **檢查套件安裝**
   ```bash
   python -c "import streamlit; print('Streamlit OK')"
   python -c "import pandas; print('Pandas OK')"
   python -c "import numpy; print('NumPy OK')"
   ```

3. **清理快取**
   ```bash
   # 清理 Streamlit 快取
   streamlit cache clear
   ```

4. **重新安裝套件**
   ```bash
   pip uninstall streamlit pandas plotly numpy
   pip install streamlit pandas plotly numpy
   ```

## 📝 環境需求

### 最低需求
- Python 3.7+
- streamlit >= 1.20.0
- pandas >= 1.3.0
- numpy >= 1.20.0

### 推薦配置
- Python 3.9+
- streamlit >= 1.28.0
- pandas >= 2.0.0
- plotly >= 5.0.0
- numpy >= 1.24.0

## 🆘 如果問題持續存在

1. **檢查錯誤訊息**：複製完整的錯誤訊息
2. **檢查檔案完整性**：確保所有檔案都完整下載
3. **重新開始**：刪除所有檔案重新下載
4. **使用虛擬環境**：建立乾淨的 Python 環境

## 📞 常見問題 FAQ

**Q: 為什麼圖表不顯示？**  
A: 可能缺少 plotly 套件，穩定版會自動切換到 matplotlib

**Q: 資料上傳失敗？**  
A: 檢查 Excel 檔案格式，確保包含必要欄位

**Q: 頁面空白？**  
A: 清除瀏覽器快取，重新載入頁面

**Q: 中文顯示亂碼？**  
A: 確保檔案使用 UTF-8 編碼保存
