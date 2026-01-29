#!/bin/bash

echo "🚀 充電站營收分析系統 - GitHub 部署助手"
echo "============================================="

# 檢查是否在 git repository 中
if [ ! -d ".git" ]; then
    echo "📁 初始化 Git repository..."
    git init
    echo "✅ Git repository 已初始化"
fi

# 檢查是否有 remote origin
if ! git remote get-url origin &> /dev/null; then
    echo ""
    echo "🔗 設定 GitHub remote URL"
    echo "請輸入您的 GitHub repository URL (例如: https://github.com/username/repository.git):"
    read -r repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote URL 已設定: $repo_url"
    else
        echo "❌ 未提供 repository URL，請手動設定"
        exit 1
    fi
fi

# 檢查是否有未追蹤的檔案
echo ""
echo "📋 檢查專案檔案..."

required_files=(
    "streamlit_app.py"
    "data_processor.py" 
    "requirements.txt"
    "README.md"
    ".gitignore"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ 缺少必要檔案:"
    printf '   - %s\n' "${missing_files[@]}"
    echo "請確保所有必要檔案都存在後再次執行此腳本"
    exit 1
fi

echo "✅ 所有必要檔案都存在"

# 添加所有檔案到 git
echo ""
echo "📦 添加檔案到 Git..."
git add .

# 檢查是否有需要提交的變更
if git diff --cached --quiet; then
    echo "ℹ️  沒有需要提交的變更"
else
    echo "💾 提交變更..."
    
    # 獲取提交訊息
    echo "請輸入提交訊息 (或按 Enter 使用預設訊息):"
    read -r commit_message
    
    if [ -z "$commit_message" ]; then
        commit_message="部署充電站營收分析系統 - $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    git commit -m "$commit_message"
    echo "✅ 變更已提交: $commit_message"
fi

# 確保在 main 分支
current_branch=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "main" ] && [ "$current_branch" != "master" ]; then
    echo ""
    echo "🔄 切換到 main 分支..."
    if git show-ref --verify --quiet refs/heads/main; then
        git checkout main
    elif git show-ref --verify --quiet refs/heads/master; then
        git checkout master
    else
        git checkout -b main
    fi
fi

# 推送到 GitHub
echo ""
echo "⬆️  推送到 GitHub..."
current_branch=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD)

if git push -u origin "$current_branch"; then
    echo "✅ 成功推送到 GitHub"
else
    echo "❌ 推送失敗，請檢查網路連接和 GitHub 認證"
    exit 1
fi

# 顯示部署選項
echo ""
echo "🎉 專案已成功上傳到 GitHub！"
echo ""
echo "📋 接下來的部署選項:"
echo ""
echo "1️⃣  Streamlit Cloud (推薦 - 免費且簡單)"
echo "   📍 前往: https://share.streamlit.io/"
echo "   🔗 使用 GitHub 帳號登入"
echo "   ✨ 選擇您的 repository 並設定主檔案為: streamlit_app.py"
echo ""
echo "2️⃣  Heroku (功能豐富)"
echo "   📍 前往: https://dashboard.heroku.com/"
echo "   🛠️  創建新 app 並連接 GitHub repository"
echo "   ⚙️  啟用自動部署"
echo ""
echo "3️⃣  Docker 部署"
echo "   🐳 執行: docker build -t charging-station-analytics ."
echo "   🚀 執行: docker run -p 8501:8501 charging-station-analytics"
echo ""
echo "4️⃣  自建伺服器"
echo "   📖 查看 DEPLOYMENT.md 獲取詳細指南"
echo ""

# 顯示 repository 資訊
repo_url=$(git remote get-url origin)
echo "🔗 您的 GitHub Repository: $repo_url"
echo ""

# 檢查是否要開啟 GitHub
echo "是否要在瀏覽器中開啟 GitHub repository? (y/N):"
read -r open_github

if [[ $open_github =~ ^[Yy]$ ]]; then
    # 轉換 git URL 為 web URL
    web_url=$(echo "$repo_url" | sed 's/\.git$//' | sed 's/git@github\.com:/https:\/\/github.com\//')
    
    if command -v xdg-open &> /dev/null; then
        xdg-open "$web_url"
    elif command -v open &> /dev/null; then
        open "$web_url"
    elif command -v start &> /dev/null; then
        start "$web_url"
    else
        echo "請手動開啟: $web_url"
    fi
fi

echo ""
echo "📚 更多部署資訊請參考:"
echo "   - README.md (專案說明)"
echo "   - DEPLOYMENT.md (詳細部署指南)"
echo ""
echo "🎊 祝您部署順利！"
