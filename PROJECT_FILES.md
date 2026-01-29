# 充電站營收分析系統 - 專案檔案清單

## 📁 核心應用程式檔案
- `streamlit_app.py`      - 主應用程式（進階版，支援檔案上傳）
- `main.py`               - 基礎版應用程式（含示範數據）
- `data_processor.py`     - 數據處理核心模組

## 📋 配置檔案
- `requirements.txt`      - Python 相依套件清單
- `.streamlit/config.toml` - Streamlit 應用配置

## 📚 說明文件
- `README.md`             - 專案主要說明文件
- `DEPLOYMENT.md`         - 詳細部署指南
- `PROJECT_FILES.md`      - 此檔案清單

## 🚀 部署相關檔案
- `deploy_to_github.sh`   - GitHub 自動部署腳本
- `start.sh`              - 本地啟動腳本
- `Dockerfile`            - Docker 容器化配置
- `docker-compose.yml`    - Docker Compose 配置
- `Procfile`              - Heroku 部署配置
- `setup.sh`              - Heroku 設定腳本
- `vercel.json`           - Vercel 部署配置

## 🔧 開發工具
- `.gitignore`            - Git 忽略檔案設定
- `test_system.py`        - 系統功能測試腳本
- `.github/workflows/deploy.yml` - GitHub Actions CI/CD

## 📊 檔案用途說明

### 應用程式檔案
| 檔案 | 用途 | 何時使用 |
|------|------|----------|
| `streamlit_app.py` | 完整功能的主應用程式 | 生產環境、支援檔案上傳 |
| `main.py` | 簡化版應用程式 | 展示用途、含示範數據 |
| `data_processor.py` | 數據處理邏輯 | 被主程式呼叫 |

### 部署選項對應檔案
| 平台 | 所需檔案 | 說明 |
|------|----------|------|
| Streamlit Cloud | `streamlit_app.py`, `requirements.txt`, `.streamlit/config.toml` | 推薦選項，免費且簡單 |
| Heroku | `Procfile`, `setup.sh`, `requirements.txt` | 功能豐富，適合擴展 |
| Docker | `Dockerfile`, `docker-compose.yml` | 容器化部署，環境一致 |
| Vercel | `vercel.json`, `requirements.txt` | 實驗性支援 |

### 腳本使用指南
| 腳本 | 功能 | 執行方式 |
|------|------|----------|
| `deploy_to_github.sh` | 自動化 GitHub 部署流程 | `./deploy_to_github.sh` |
| `start.sh` | 本地開發環境啟動 | `./start.sh` |
| `test_system.py` | 系統功能測試 | `python test_system.py` |

## 🏗️ 專案架構

```
充電站營收分析系統/
├── 核心程式/
│   ├── streamlit_app.py
│   ├── main.py
│   └── data_processor.py
├── 配置檔案/
│   ├── requirements.txt
│   └── .streamlit/config.toml
├── 部署配置/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Procfile
│   ├── setup.sh
│   └── vercel.json
├── 自動化腳本/
│   ├── deploy_to_github.sh
│   ├── start.sh
│   └── test_system.py
├── CI/CD/
│   └── .github/workflows/deploy.yml
└── 文件/
    ├── README.md
    ├── DEPLOYMENT.md
    └── PROJECT_FILES.md
```

## 📝 檔案大小概覽
- 總檔案數量: ~15 個
- 主程式檔案: ~3 個 (約 50KB)
- 配置檔案: ~8 個 (約 10KB)
- 說明文件: ~4 個 (約 30KB)

## 🎯 使用建議

### 開發階段
1. 使用 `main.py` 進行功能測試
2. 執行 `python test_system.py` 驗證系統
3. 使用 `./start.sh` 啟動本地開發環境

### 部署階段
1. 執行 `./deploy_to_github.sh` 快速部署
2. 選擇合適的部署平台
3. 參考 `DEPLOYMENT.md` 獲取詳細指引

### 生產環境
1. 使用 `streamlit_app.py` 作為主程式
2. 根據需求調整 `.streamlit/config.toml`
3. 定期運行 `test_system.py` 進行健康檢查
