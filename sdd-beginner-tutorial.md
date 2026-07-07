# 新手實戰：用 Claude Code + OpenSpec 做 SDD 開發（個人版）

這份教學用**一條時間軸**帶你走完整個流程：從裝工具開始，到把程式部署上線。每一步都標清楚是**必做**還是**選用**，選用的還會說明「什麼時機才需要」。

對象是**單人開發者**，主工具是 **Claude Code + OpenSpec**，需要時再加 **Docker** 部署、**Superpowers** 紀律規範。

> 作業系統指令一律合併在一起，前面用 `#` 備註是哪個系統，挑你的照做即可。

---

## 開始前：先搞懂這三樣東西的分工

| 工具 | 角色 | 一句話 | 必要性 |
|------|------|--------|--------|
| **Claude Code** | 執行者 | 真正動手寫程式的 AI | 必備 |
| **OpenSpec** | 規格管理 | 把「要做什麼／為什麼」留成版控文件 | 必備 |
| **Docker** | 部署打包 | 把環境打包，換機器/上線都一致 | 要部署才用 |
| **Superpowers** | 紀律規範 | 逼 AI 先想清楚、先寫測試、先驗證再說完成 | 選用 |

核心觀念一句話：**在開始之前，先定義什麼叫「完成」。** 這樣 AI 說「做好了」時，你才有標準驗收。

整條時間軸長這樣（右側標示在「全域」還是「專案內」下指令）：

```
STEP 0  裝工具         ← 必做      🌐 全域（在哪個資料夾都行）
STEP 1  決定隔離策略    ← 必做      🌐 全域（裝 uv 本身）
STEP 2  起專案 + 初始化 ← 必做      📁 從這裡開始 cd 進專案
STEP 3  填 config.yaml ← 必做      📁 專案內
STEP 4  探索想法        ← 選用      📁 專案內
STEP 5  建立變更提案    ← 必做      📁 專案內
STEP 6  實作           ← 必做      📁 專案內
STEP 7  驗證           ← 必做      📁 專案內
STEP 8  歸檔 + 推 GitHub ← 必做     📁 專案內
STEP 9  部署           ← 選用      📁 專案內
進階    Superpowers     ← 選用      📁 專案內
```

> **🌐 全域 vs 📁 專案內——新手最容易搞混的地方。** STEP 0 和 STEP 1 都是「裝工具／設定身分」，在哪個資料夾跑都行，一台電腦做一次就好。**到 STEP 2 才第一次 `cd` 進專案資料夾**，從那之後的所有指令（`uv add`、`openspec`、`git`、`/opsx:` 等）都必須在專案資料夾裡跑。心法：**裝東西＝全域；對專案做事＝先 `cd` 進去。**

OpenSpec 官方的兩條路徑（STEP 5～8 對應的就是預設路徑）：

```
預設快速路徑（core profile）：
  /opsx:propose ──► /opsx:apply ──► /opsx:archive

擴充路徑（需先開啟，見 0-6）：
  /opsx:new ──► /opsx:ff 或 /opsx:continue ──► /opsx:apply ──► /opsx:verify ──► /opsx:archive
```

---

# STEP 0：裝工具〔必做〕🌐 全域

> 這一整步都是「裝給整台電腦用」，在哪個資料夾跑都行，一台電腦做一次即可。

## 0-1. Node.js〔必做〕

OpenSpec 是 npm 套件，需要 Node.js。建議裝 **LTS 版**（最穩定）。**OpenSpec 需要 Node.js 20.19.0 以上**，裝 LTS 一定夠。

```
# Windows（內建 winget）
winget install OpenJS.NodeJS.LTS

# macOS（Homebrew，沒裝先裝 Homebrew）
brew install node

# Linux（Ubuntu / Debian，用 NodeSource 取得較新版本）
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

> macOS 若還沒裝 Homebrew：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

**驗證（任何系統都一樣）：**

```
node --version
npm --version
```

兩行都印出版本號（例如 `v22.x.x`）就成功。

## 0-2. nvm 管理 Node 版本〔選用〕

**什麼時機需要：** 你會同時開發多個專案、或不同專案要不同 Node 版本時。第一次學可以先跳過。

⚠️ **macOS/Linux 和 Windows 是兩個不同專案，方式不同。**

**macOS / Linux（nvm）：**

```
# 安裝（版本號可到 nvm GitHub 看最新）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```

裝完**關掉終端機再重開**（或 `source ~/.bashrc` / `source ~/.zshrc`），然後：

```
nvm --version
nvm install --lts        # 裝最新 LTS
nvm use --lts            # 切換到它
nvm alias default 'lts/*' # 設為預設（注意是 lts/* 別名，不能用 --lts）
```

**Windows（nvm-windows，另一個專案）：**

```
winget install CoreyButler.NVMforWindows
```

> 若之前用別的方式裝過 Node，建議先移除再用 nvm-windows，避免打架。裝完**重開一個新終端機**。

```
nvm version
nvm install lts
nvm use 20.11.0          # Windows 建議寫完整版本號
nvm list
```

## 0-3. Git〔必做〕

SDD 流程裡規格和程式碼都要進版控才有意義（保留歷史、可回溯、可回退）。

```
# 先確認有沒有裝
git --version

# 沒有的話：
# Windows
winget install Git.Git
# macOS
brew install git
# Ubuntu / Debian
sudo apt-get install git
```

**第一次用 Git，設定身分（會記在每次提交裡）：**

```
git config --global user.name "你的名字"
git config --global user.email "你的Email"
```

**確認有沒有寫入：**

```
git config --global user.name     # 各印出你剛設的值
git config --global user.email
# 或一次看全部全域設定：
git config --global --list
```

有印出值就是寫進去了；空白代表還沒設或打錯。打錯的話再跑一次同樣的 `git config --global ...` 直接覆蓋即可，不用先刪。

## 0-4. Claude Code〔必做〕

確認在終端機輸入 `claude` 能進入。還沒裝的話先把這步弄定。

## 0-5. OpenSpec〔必做〕

```
npm install -g @fission-ai/openspec@latest
openspec --version
```

> **指令版本說明（重要）**：本教學用最新的 `opsx:` 系列指令。OpenSpec 預設的 `core` profile 已含 `propose`、`explore`、`apply`、`archive`（外加 `sync`，通常自動觸發），新手用這些就夠。若要用到擴充指令（`new`、`continue`、`ff`、`verify`、`bulk-archive`、`onboard`），要先開啟，見下方 0-6。舊的 `/openspec:proposal` 系列仍可用但已是 legacy，不建議新專案再用。

## 0-6. 開啟擴充指令〔選用〕

**什麼時機需要：** 你想要更細的控制（逐份產生文件、實作後驗證等）。新手第一次可以先跳過，只用核心指令。

```
openspec config profile     # 🌐 全域：選 workflows（擴充工作流），設一次全電腦生效
openspec update             # 📁 專案內：要 cd 進「每個」專案各跑一次，才會套用到該專案
```

> ⚠️ **兩段式，新手常只做一半：** `openspec config profile` 是全域設定，但設完一定要進每個專案 `cd` 進去跑 `openspec update`，那個專案才會出現擴充指令。只跑前半段會以為沒生效。（不過這步是 STEP 2 之後才會用到，這裡先知道即可。）

開啟後會多出這些指令：`/opsx:new`（只建骨架）、`/opsx:continue`（逐份產生下一個文件）、`/opsx:ff`（一次產生全部規劃文件）、`/opsx:verify`（驗證實作是否符合規格）、`/opsx:bulk-archive`（一次歸檔多個變更）、`/opsx:onboard`（互動教學）。

---

# STEP 1：決定隔離策略〔必做：做個決定〕🌐 全域（裝 uv）

這一步不一定要裝東西，但**一定要先想清楚**，免得之後「換電腦就掛」才回頭補。隔離有不同層級，別一開始就上最重的工具。

> **這裡的 1-2 安裝 uv 是全域動作**（裝工具本身，一次就好，任何資料夾可跑）。但 1-3 的 `uv init`／`uv add`／`uv run`／`uv sync` 是**專案內指令**，要等 STEP 2 `cd` 進專案後才跑——這裡先看懂用法，先別執行。

**照這張表對號入座：**

| 你的情況 | 用什麼 | 時機 |
|----------|--------|------|
| 寫 Python、單人本機 | **uv** | 只要寫 Python 就用 |
| 寫 Node / JS | 不用額外的 | `node_modules` + `package.json` 本身就是隔離 |
| 想跨電腦同步 | uv + 把 `pyproject.toml` / `uv.lock` 進版控 | 通常已足夠 |
| 有資料庫 / 要部署上線 / 多台機器要一致 | **Docker** | 走到 STEP 9 再裝 |

## 1-1. 為什麼用 uv？

寫 Python 的話，**這份教學用 [uv](https://docs.astral.sh/uv/)** 來管理虛擬環境和套件。uv 是用 Rust 寫的，一個工具同時取代 pip（裝套件）、venv（虛擬環境）、pyenv（管 Python 版本），而且快非常多。對新手的好處是：指令少、不用手動 activate、依賴鎖定（`uv.lock`）讓換電腦能精準重現環境。

## 1-2. 安裝 uv

照官方 standalone installer（建議方式）：

```
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows（PowerShell）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> 也可以用套件管理器：macOS `brew install uv`、Windows `winget install --id=astral-sh.uv -e`。

裝完**關掉終端機再重開**，確認：

```
uv --version
```

## 1-3. uv 基本用法（STEP 2 起好專案後會用到）

```
# 在專案目錄初始化（產生 pyproject.toml）
uv init

# 加套件（自動建虛擬環境 .venv、自動更新 pyproject.toml 和 uv.lock）
uv add fastapi "uvicorn[standard]"

# 跑程式（不必手動 activate，uv 會自動用專案的環境）
uv run uvicorn main:app --reload

# 換電腦後，依 lock 檔精準重建環境
uv sync
```

新手只要記住四個：`uv init`（起專案）、`uv add`（加套件）、`uv run`（跑東西）、`uv sync`（重建環境）。**不用再手動 `source venv/bin/activate`**，uv 全自動。

**結論給個人開發者：** 用 uv 開發、把 `pyproject.toml` 和 `uv.lock` 進版控，就解決約八成「換電腦」問題。**Docker 留到 STEP 9 要部署時再上**，不要為了「以後可能用到」第一天就扛它的複雜度。

---

# STEP 2：起專案並初始化 OpenSpec〔必做〕📁 從這裡 cd 進專案

> **這是分水嶺。** 前面 STEP 0、1 都是全域裝工具；**從這一步的 `cd` 開始，你就「進到專案資料夾裡」了，之後每一步（含 STEP 1 教過的 `uv init`／`uv add`／`uv run`）都在這個資料夾內跑。** 開新終端機回來繼續做時，記得第一件事就是 `cd` 回專案。

```
# 全新專案：先建資料夾
mkdir my-app
cd my-app                 # ← 進專案，分水嶺就在這裡
git init

# 既有專案：直接進專案根目錄
cd my-existing-project    # ← 一樣，先 cd 進去

# 進到專案後才做：初始化
openspec init
uv init                   # Python 專案：產生 pyproject.toml（Node 專案改 npm init）
```

`openspec init` 會問用哪個 AI 工具，選 **Claude Code**，它會自動產生對應 slash 指令並建立：

```
├── .claude/           # Claude Code 的 skills 與 opsx 指令（依所選工具產生）
└── openspec
    ├── config.yaml     # 專案設定：技術棧、慣例、規則都寫在這（STEP 3 要填）
    ├── specs/          # 系統現狀規格（真相來源；全新專案一開始是空的）
    └── changes/        # 變更提案
        └── archive/    # 已完成的變更
```

> **注意（OpenSpec 1.4 起）**：專案脈絡放在 **`config.yaml`** 的 `context` 欄位，**不再有獨立的 `project.md`**。舊教學或舊版本可能寫 `project.md`，1.4 之後已改成 config.yaml，別被搞混。

**接著建立 `.gitignore`**（避免把不該進版控的東西提交）：

```
# .gitignore
node_modules/
.venv/
.env
__pycache__/
*.pyc
```

---

# STEP 3：填寫 config.yaml〔必做，最常被跳過〕

把專案的技術棧、慣例、限制寫進 `openspec/config.yaml` 的 `context` 欄位，AI 產生規格和程式碼時就會參考它。打開 Claude Code，貼這句：

```
請讀 openspec/config.yaml，幫我把專案的技術棧、開發慣例和重要限制填進 context 欄位（必要時補 rules）。先問我幾個問題確認細節再填。
```

AI 會反問你問題（語言、框架、命名慣例、測試框架等）。**認真回答**——填得越具體，AI 越不會亂猜。填好後 `config.yaml` 大致長這樣（官方格式）：

```yaml
schema: spec-driven
context: |
  Tech stack: Python (FastAPI), PostgreSQL
  Testing: pytest
  慣例：RESTful API、命名用 snake_case
  限制：對外 API 要維持向後相容
rules:
  proposal:
    - 明確定義 in-scope 與 out-of-scope
  tasks:
    - 包含 lint/build/測試的驗證步驟
```

> **找不到 `config.yaml`？** OpenSpec 1.4 起專案脈絡放在這個檔，沒有 `project.md`。若 `openspec init` 沒產生 config.yaml，可手動建一個，最少寫 `schema: spec-driven` 和 `context:` 兩段即可。
>
> 既有專案的好處：AI 可以直接讀你現有程式碼推斷慣例。但仍要親自確認，特別是「只有你知道」的隱性限制。

---

# STEP 4：探索想法〔選用〕

**什麼時機需要：** 你連「問題到底是什麼／要做哪些功能」都還不確定的時候。心裡已經清楚要做什麼就**直接跳 STEP 5**。

```
/opsx:explore 我想做一個記帳 App，但還沒想清楚核心功能
```

explore 很隨性，跟著有趣的線索走、用文字圖表幫你思考，**最後可能什麼檔案都不產出**，目的純粹是讓你和 AI 對問題有共識。聊到方向清楚後，AI 會提示你接 `/opsx:propose` 正式開一個變更。

> 既有專案特別建議先 explore，讓 AI 摸清相關程式碼脈絡，幫你回答提案裡最關鍵的問題：**這次變更會影響哪些現有部分？**
> ```
> /opsx:explore 我想在訂單模組加折扣碼，先幫我看現在訂單流程怎麼運作
> ```

---

# STEP 5：建立變更提案〔必做〕

這一步分兩種情況，差別在「規格怎麼寫」。

## 5-A. 全新專案

用核心指令 `propose` 一步產生所有規劃文件：

```
/opsx:propose 使用者註冊與登入功能
```

AI 會在 `openspec/changes/` 建立資料夾，含：

- `proposal.md` — 為什麼做、做什麼、影響範圍（Why / What / Impact）
- `specs/` — 這次新增的規格
- `design.md` — 技術設計
- `tasks.md` — 實作待辦（checkbox 格式）

建立過程 AI 會不斷問你確認規格。**這正是價值**——逼你在寫程式前想清楚「登入失敗怎麼辦」「密碼有什麼限制」這些細節。

> **想逐份審查文件？** 開啟擴充指令（0-6）後，可改用 `/opsx:new` 建骨架，再用 `/opsx:continue` 一份一份產生，或 `/opsx:ff` 一次全產生。新手用 `propose` 就好。

## 5-B. 既有專案

```
/opsx:propose 訂單加入折扣碼功能
```

既有專案的 `specs/` 用 **Delta 格式**——只描述「跟現狀相比改了什麼」，用 `## ADDED`、`## MODIFIED`、`## REMOVED` 標記。官方 Scenario 用 **GIVEN / WHEN / THEN**（可再加 AND）：

```
# Delta for Checkout

## ADDED Requirements

### Requirement: Discount Code
The system SHALL allow users to enter a discount code at checkout.

#### Scenario: Valid code
- GIVEN a user at the checkout page
- WHEN the user enters a valid, non-expired discount code
- THEN the discount is applied
- AND the total is recalculated
```

**歸檔時 Delta 怎麼併進主 specs（官方行為）：** ADDED → 附加到主 spec；MODIFIED → 取代既有版本；REMOVED → 從主 spec 刪除。變更資料夾接著移到 `openspec/changes/archive/`。

> ⚠️ **MODIFIED 要貼完整內容**（含所有 Scenario）。因為歸檔時是「整段取代」既有需求，只寫差異會讓原本沒寫到的 Scenario 消失。

## 5-C. 驗證提案格式（兩種都做）

```
openspec validate add-discount-code --strict
```

（名稱用 `openspec list` 查。）驗證會檢查每個需求有沒有對應 Scenario、有沒有用 `SHALL`/`MUST`。**現在抓出格式問題，比歸檔時才發現合併失敗輕鬆得多。**

其他好用的檢視指令：`openspec show <name>`（看單一變更細節）、`openspec view`（互動式儀表板，總覽所有進行中的變更）。

---

# STEP 6：實作〔必做〕

```
/opsx:apply add-discount-code
```

AI 讀 `proposal.md` 和 `tasks.md`，照清單一個個做，完成一項把 `- [ ]` 改 `- [x]`，進度看得到。

**紀律提醒：** AI 想做規格沒寫的東西，直接提醒它：

```
這不在提案範圍內，請專注在 tasks.md 列出的項目
```

實作中發現規格有問題？歸檔前都能改。改 `proposal.md`／`tasks.md`／`specs/`，重跑一次 `openspec validate`，再繼續。

---

# STEP 7：驗證〔必做，最常被偷懶〕

AI 很愛說「完成了」，但測試沒過、邊界沒處理它也會輕描淡寫帶過。**接受「完成」前一定要看到證據：**

- 說測試通過 → 要有測試輸出顯示 0 失敗
- 說 build 成功 → 要有 exit code 0
- 說 bug 修好 → 要重新測原症狀確認不再出現

直接要求：

```
在說完成之前，請實際跑一次測試，把完整輸出貼給我看
```

> **有開擴充指令（0-6）的話**，可用 `/opsx:verify` 讓 AI 自動比對「實作有沒有符合規格」，從完整性、正確性、一致性三個面向檢查，並把問題分成 CRITICAL／WARNING／SUGGESTION 回報。歸檔前跑一次，能抓出實作偏離規格的地方。

---

# STEP 8：歸檔 + 進版控 + 推 GitHub〔必做〕

## 8-1. 歸檔

所有任務完成、測試通過後：

```
/opsx:archive add-discount-code
```

歸檔做兩件事：把變更資料夾移到 `changes/archive/`（加日期前綴，如 `2026-01-15-add-discount-code/`），並把規格差異合併回 `specs/`。這樣 `specs/` 永遠是「系統現在該長什麼樣」，`archive/` 保留每次變更歷史。

## 8-2. 進版控

```
git add .
git commit -m "Add discount code feature"
```

**整個 `openspec/` 都要進版控。** 給新手的 Git 習慣：

- **一功能一提交**，commit 訊息寫清楚。
- **提交前 `git status` / `git diff` 看一眼**，別誤把密鑰或暫存檔帶上。
- **想退回上一個能動的版本**：`git log` 找好的版本、`git checkout` 退回去。這就是版控搭配 SDD 的好處——**有規格知道目標、有版控可隨時回退**。

## 8-3. 推上 GitHub〔強烈建議〕

**什麼時機：** 想要異地備份、跨電腦同步、或未來找人協作。第一次設定：

**1. 在 GitHub 建空 repo**：[github.com](https://github.com) → `+` → New repository → 填名稱 → **不要**勾 README/.gitignore/license（本機已有檔案，勾了會衝突）→ Create。

**2. 連遠端並推送：**

```
git remote add origin https://github.com/你的帳號/my-app.git
git branch -M main                # 確認主分支叫 main
git push -u origin main           # 首次推送，-u 記住對應，之後只需 git push
```

> 首次 push 要登入，GitHub 不接受帳密，要用 **Personal Access Token**（Settings → Developer settings → Personal access tokens，被問密碼時貼 token），或裝 [GitHub CLI](https://cli.github.com/) 跑 `gh auth login` 一次設定好。

**之後日常：**

```
git add .
git commit -m "說明"
git push
```

**換電腦接著做：**

```
git clone https://github.com/你的帳號/my-app.git
cd my-app
uv sync          # Python：依 uv.lock 精準重建環境（或 Node 專案：npm install）
```

依賴鎖定檔（`uv.lock`／`package-lock.json`）和 `openspec/` 都進版控，**新電腦 clone 下來就能精準重現規格、程式碼和依賴**。

**🔒 安全紅線：**

- **密鑰/密碼/token 絕不推上去**（尤其公開 repo），`.env`、憑證一定要 `.gitignore`。
- **不小心推了密鑰**：光刪檔沒用（歷史還在）——**立刻去該服務作廢那把密鑰、換新的**。
- push 前養成 `git status` 習慣。

---

# STEP 9：部署 / 環境一致〔選用：Docker〕

**什麼時機需要：** 落在「**有資料庫、要部署上線、或多台機器/伺服器要環境一致**」這格時。範例用 **FastAPI（Python）+ PostgreSQL**。

先裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)（Windows/macOS）或 Docker Engine（Linux），確認：

```
docker --version
docker compose version
```

分兩步：**先只 Docker 化 App，再加資料庫**。建議先跑通第一步。

## 9-1. 只把 App 裝進容器

專案結構（用 uv 的話，依賴記在 `pyproject.toml` + `uv.lock`）：

```
my-app/
├── main.py
├── pyproject.toml      # uv init / uv add 自動產生
├── uv.lock             # uv 自動產生的鎖定檔
├── Dockerfile          # 建立這個
└── .dockerignore       # 和這個
```

`main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok"}
```

依賴用 uv 加入（不必手寫 requirements.txt）：

```
uv add fastapi "uvicorn[standard]"
```

`Dockerfile`（用官方 uv 映像，逐行註解）：

```dockerfile
# 基底映像：官方 uv 映像（已內建 uv 和 Python）
FROM ghcr.io/astral-sh/uv:python3.12-slim

# 容器內工作目錄
WORKDIR /app

# 先只複製依賴檔並安裝（單獨一層，之後改 code 不會重裝套件，build 更快）
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# 再複製其餘程式碼
COPY . .

# 對外開放的埠
EXPOSE 8000

# 啟動指令（用 uv run 跑，自動用專案環境）
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`.dockerignore`：

```
.venv/
__pycache__/
*.pyc
.env
.git/
```

建置並執行：

```
docker build -t my-app .          # -t 命名，最後的 . 是 build 位置
docker run -p 8000:8000 my-app    # 容器 8000 對應本機 8000
```

到 `http://localhost:8000` 看到 `{"status":"ok"}` 就成功。**這個映像可搬到任何裝了 Docker 的機器跑，環境完全一致**。

## 9-2. 加上 PostgreSQL（docker compose）

根目錄建 `compose.yaml`：

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      # host 用服務名 "db"，不是 localhost
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data   # 資料持久化，容器刪了也不丟

volumes:
  pgdata:
```

新手三個關鍵觀念：

- **服務名就是主機名**：App 連資料庫 host 是 `db`（compose 服務名），不是 `localhost`。
- **連線資訊用環境變數**：程式裡 `os.environ["DATABASE_URL"]` 讀。**密碼正式環境別寫死**，改用 `.env`（記得 gitignore）。
- **volume 保住資料**：沒設 volume，容器一刪資料就沒。

操作：

```
docker compose up -d --build     # 建置並背景啟動
docker compose logs -f           # 看 log
docker compose down              # 全部停掉
docker compose down -v           # 連資料一起清（會刪 volume，慎用）
```

## 9-3. Docker 怎麼接回前面流程

把 `Dockerfile`、`compose.yaml`、`.dockerignore` **都進版控**。換電腦或上伺服器時 `git clone` + `docker compose up`，整個環境（App + 資料庫 + 版本）原樣重現。

> **和 uv 衝突嗎？** 不衝突，層級不同。常見分工：**本機日常用 uv（快、輕、IDE 整合好），驗證部署/上線才用 Docker**。新手建議 uv 開發、Docker 負責部署，職責清楚。

---

# 進階：加 Superpowers〔選用〕

**什麼時機需要：** 前面流程已能穩定開發；若你發現 AI 還是常「沒想清楚就動工」「說修好其實沒好」，再引入 [Superpowers](https://github.com/obra/superpowers)，用一套 Skills 幫 AI 建立紀律。

不必全套（全套很耗 token），先挑這兩個最有感的：

1. **verification-before-completion** — 強制「沒驗證不准說完成」，直接解決 STEP 7 的痛點。
2. **systematic-debugging** — 除錯拆成「根因 → 模式 → 假說 → 實作」四階段，並規定**修三次還沒好就停下來質疑架構**，避免鬼打牆。

## 三個探索/規劃工具怎麼分？

| 工具 | 用在 | 一句話 |
|------|------|--------|
| `opsx:explore`（STEP 4） | 還不確定問題是什麼 | 「我想聊聊，看看能發現什麼」 |
| Superpowers `brainstorming` | 有想法但還沒成形 | 「我有個想法，幫我變成具體設計」 |
| Claude Code **Plan Mode** | 已經知道要做什麼 | 「我知道要做什麼，幫我規劃步驟」 |

可串接（explore → brainstorming → Plan Mode），但**不必每次走完三段**：需求清楚直接 Plan Mode，模糊就從 brainstorming 起手。每個小功能都走三段反而是另一種過度設計。

---

# 番外：什麼時候「不用」走完整流程？

判斷標準一句話：**這次改動會不會讓系統行為跟 `specs/` 裡定義的不一樣？** 會 → 開提案（回 STEP 5）。不會 → 直接改：

- **修 bug**（是讓程式符合規格，不是改規格）
- 修錯字、調格式、改註解
- 更新依賴（非破壞性）
- 調設定（不影響行為規格）
- 補現有行為的測試

---

# 附錄：OpenSpec 指令速查（最新版）

## 核心指令（預設 `core` profile 就有，新手實際只需這四個）

> `core` profile 其實還含 `sync`（把 delta specs 併回主 specs），但 `archive` 通常會自動處理，少有手動呼叫的需求，所以日常記住下面四個即可。

| 指令 | 用途 | 對應 STEP |
|------|------|-----------|
| `/opsx:propose` | 一步建立變更並產生所有規劃文件 | STEP 5 |
| `/opsx:explore` | 投入變更前先釐清想法（不產文件） | STEP 4 |
| `/opsx:apply` | 實作變更裡的任務 | STEP 6 |
| `/opsx:archive` | 歸檔已完成的變更（會提示是否 sync） | STEP 8 |

最短路徑：`explore`（選用）→ `propose` → `apply` → `archive`。

## 擴充指令（要先 `openspec config profile` + `openspec update` 開啟）

| 指令 | 用途 |
|------|------|
| `/opsx:new` | 只建立變更骨架 |
| `/opsx:continue` | 依相依順序逐份產生下一個文件 |
| `/opsx:ff` | fast-forward，一次產生全部規劃文件 |
| `/opsx:verify` | 驗證實作是否符合規格（完整性/正確性/一致性） |
| `/opsx:sync` | 把 delta specs 併回主 specs（archive 通常會自動處理） |
| `/opsx:bulk-archive` | 一次歸檔多個變更 |
| `/opsx:onboard` | 用你真實的程式碼帶你走一遍完整流程的互動教學 |

## 常用 CLI（在終端機跑，非 slash 指令）

| 指令 | 用途 |
|------|------|
| `openspec init` | 初始化專案（可加 `--tools claude,cursor` 指定 AI 工具，或 `--tools all`） |
| `openspec update` | 升級 CLI 後刷新 AI 指令、套用 profile 設定 |
| `openspec list` | 列出進行中的變更 |
| `openspec show <name>` | 看單一變更的細節 |
| `openspec validate <name> --strict` | 驗證提案格式 |
| `openspec view` | 互動式儀表板，總覽所有變更 |
| `openspec config profile` | 選擇要啟用的 workflows（擴充指令） |

> **不同 AI 工具語法略有差異**：Claude Code 用 `/opsx:propose` 這種冒號寫法；Cursor／Windsurf／Copilot 用連字號 `/opsx-propose`。功能一樣。
>
> **想偷懶學最快**：裝完直接在 Claude Code 裡跑 `/opsx:onboard`，它會用你自己的專案帶你把整個流程走一遍，比讀文件更快上手。

---

# 新手常見地雷

1. **跳過 config.yaml（STEP 3）** → AI 沒脈絡，產出風格亂七八糟。
2. **既有專案想一次補完所有規格** → 不切實際。漸進式導入，用到哪補到哪。
3. **小事也開提案** → 修 bug、改錯字不用走流程，否則「修一顆螺絲寫十幾頁報告」。
4. **AI 說完成就相信（STEP 7）** → 一定要它跑驗證、貼輸出。要證據不要感覺。
5. **MODIFIED 只寫差異（STEP 5-B）** → 必須貼完整內容，否則歸檔後原內容消失。
6. **忘記把 openspec/ 進版控** → 歷史紀錄和規格錨定全失效。
7. **把 node_modules / .venv / .env 提交進版控** → 倉庫肥大、可能外洩密鑰。一開始就設好 `.gitignore`。
8. **把密鑰推上 GitHub（尤其公開 repo）** → 等於對全世界公開。先 gitignore；真推了要立刻作廢換新，光刪檔沒用。
9. **Python 不用隔離環境（STEP 1）** → 不同專案套件互相污染，遲早出現版本衝突的怪 bug。用 uv 就自動有隔離（`.venv`）。
10. **太早扛 Docker** → 單人本機學習階段複雜度大於收益。先 uv + lock 檔進版控，要部署（STEP 9）再上。
11. **追求全自動（Spec-as-source）** → 目前不可行：LLM 非確定性，同規格每次生出的程式碼結構都不同。務實做法是人在迴路裡，AI 出初版、你審查調整。

---

# 一句話總結

> 不追求 AI 全自動，也不憑感覺亂寫，而是在兩者之間抓人機協作的節奏：**你負責定義「要做什麼」和「什麼叫完成」，AI 負責做出來，你負責驗收。**

下次 AI 再說「完成了」，記得反問：「完成了什麼？」 :)
