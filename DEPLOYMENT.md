# 🚀 充電站營收分析系統 - 部署指南

本指南將協助您將充電站營收分析系統部署到各種平台。

## 📋 部署前準備

### 1. GitHub Repository 設定

1. **創建 GitHub Repository**
```bash
# 在 GitHub 上創建新的 repository
# 然後在本地初始化
git init
git add .
git commit -m "Initial commit: 充電站營收分析系統"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

2. **驗證檔案結構**
確保您的 repository 包含以下檔案：
```
充電站營收分析系統/
├── streamlit_app.py          # 主應用程式
├── data_processor.py         # 數據處理模組
├── main.py                  # 基礎版應用程式
├── requirements.txt         # Python 依賴
├── README.md               # 專案說明
├── .gitignore              # Git 忽略檔案
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # Docker Compose 配置
├── Procfile               # Heroku 配置
├── setup.sh               # Heroku 設定腳本
├── vercel.json            # Vercel 配置
├── .streamlit/
│   └── config.toml        # Streamlit 配置
└── .github/
    └── workflows/
        └── deploy.yml     # GitHub Actions 工作流程
```

## 🌐 部署選項

### 選項 1: Streamlit Cloud (推薦) ⭐

**優點**: 免費、簡單、專為 Streamlit 設計
**適用**: 個人專案、小型團隊

**步驟**:

1. **訪問 Streamlit Cloud**
   - 前往 https://share.streamlit.io/
   - 使用 GitHub 帳號登入

2. **部署應用程式**
   - 點擊 "New app"
   - 選擇您的 GitHub repository
   - 主檔案設定為: `streamlit_app.py`
   - 點擊 "Deploy"

3. **設定環境**
   - Streamlit Cloud 會自動讀取 `requirements.txt`
   - 配置會從 `.streamlit/config.toml` 載入

4. **訪問應用程式**
   - 部署完成後，您將獲得一個 URL
   - 格式: `https://YOUR_USERNAME-YOUR_REPOSITORY-streamlit-app-HASH.streamlit.app/`

**自動更新**: 每次推送到 main 分支都會自動重新部署

### 選項 2: Heroku

**優點**: 功能豐富、擴展性好
**成本**: 免費額度有限，付費方案從 $7/月起

**步驟**:

1. **安裝 Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# 下載並安裝 Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli

# Ubuntu/Debian
sudo snap install --classic heroku
```

2. **登入 Heroku**
```bash
heroku login
```

3. **創建 Heroku 應用程式**
```bash
heroku create your-charging-station-app
```

4. **設定 buildpack**
```bash
heroku buildpacks:set heroku/python
```

5. **部署**
```bash
git push heroku main
```

6. **開啟應用程式**
```bash
heroku open
```

### 選項 3: Docker 部署

**優點**: 環境一致性、可移植性高
**適用**: 企業部署、自建伺服器

**本地測試**:
```bash
# 建立 Docker image
docker build -t charging-station-analytics .

# 運行容器
docker run -p 8501:8501 charging-station-analytics

# 或使用 Docker Compose
docker-compose up
```

**雲端部署** (AWS ECS, Google Cloud Run, Azure Container Instances):
```bash
# 標記 image
docker tag charging-station-analytics:latest your-registry/charging-station-analytics:latest

# 推送到 registry
docker push your-registry/charging-station-analytics:latest
```

### 選項 4: 自建伺服器

**適用**: 完全控制、企業內部使用

**Ubuntu/Debian 伺服器設定**:
```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝 Python 和 pip
sudo apt install python3 python3-pip python3-venv -y

# 克隆專案
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

# 創建虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 使用 screen 或 tmux 在背景運行
sudo apt install screen -y
screen -S streamlit
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# 按 Ctrl+A, D 來分離 screen session
```

**設定反向代理 (Nginx)**:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 選項 5: Vercel (實驗性)

**注意**: Vercel 主要針對靜態網站，Streamlit 支援有限

```bash
# 安裝 Vercel CLI
npm install -g vercel

# 部署
vercel

# 按照提示完成設定
```

## 🔧 部署後設定

### 環境變數設定

在各平台設定以下環境變數（如需要）:

```env
# Streamlit 設定
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ENABLECORS=false
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 自定義設定
APP_TITLE=充電站營收分析系統
MAX_UPLOAD_SIZE=50
DEBUG=false
```

### 域名設定

**Streamlit Cloud**: 
- 可使用自定義域名（付費功能）
- 設定 CNAME 記錄指向 Streamlit 提供的 URL

**Heroku**:
```bash
heroku domains:add your-domain.com
# 設定 DNS CNAME 記錄
```

**自建伺服器**:
- 設定 A 記錄指向伺服器 IP
- 配置 SSL 證書（推薦使用 Let's Encrypt）

### 監控和日誌

**Streamlit Cloud**: 內建日誌查看功能

**Heroku**:
```bash
heroku logs --tail
heroku logs --source app
```

**Docker**:
```bash
docker logs -f container_name
```

## 🚨 疑難排解

### 常見問題

**1. 記憶體不足**
- 增加 Heroku dyno 規格
- 優化數據處理邏輯
- 使用數據分頁功能

**2. 載入時間過長**
- 啟用 Streamlit 快取
- 優化圖表渲染
- 預處理數據

**3. 檔案上傳限制**
- 調整 `maxUploadSize` 設定
- 實作檔案壓縮功能
- 使用雲端儲存

**4. 依賴安裝失敗**
- 檢查 `requirements.txt` 格式
- 固定套件版本
- 使用輕量化替代品

### 效能優化

**1. 快取設定**
```python
@st.cache_data
def load_data():
    # 數據載入邏輯
    pass
```

**2. 延遲載入**
```python
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

**3. 圖表優化**
- 限制數據點數量
- 使用採樣技術
- 實作分頁功能

## 🔐 安全考量

### 數據安全
- 避免在程式碼中硬編碼敏感資訊
- 使用環境變數儲存設定
- 實作用戶驗證（如需要）

### 存取控制
```python
# 簡單的密碼保護範例
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("密碼", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("密碼", type="password", on_change=password_entered, key="password")
        st.error("密碼錯誤")
        return False
    else:
        return True

if check_password():
    # 顯示主要應用程式內容
    pass
```

## 📊 監控和分析

### 使用情況追蹤
- Google Analytics 整合
- 自定義事件追蹤
- 用戶行為分析

### 錯誤監控
- Sentry 整合
- 日誌聚合
- 警報設定

## 🎯 最佳實踐

1. **版本控制**: 使用語義化版本號
2. **文檔**: 保持 README 和部署文檔更新
3. **測試**: 在部署前運行自動化測試
4. **備份**: 定期備份重要數據和配置
5. **更新**: 定期更新依賴套件

---

## 📞 技術支援

如果在部署過程中遇到問題：

1. 檢查對應平台的官方文檔
2. 查看應用程式日誌
3. 驗證所有配置檔案
4. 測試本地環境是否正常運作

**常用除錯命令**:
```bash
# 檢查 Python 版本
python --version

# 檢查已安裝套件
pip list

# 測試 Streamlit 應用程式
streamlit run streamlit_app.py --server.runOnSave true

# 檢查端口使用狀況
netstat -tulpn | grep :8501
```

祝您部署順利！🚀
