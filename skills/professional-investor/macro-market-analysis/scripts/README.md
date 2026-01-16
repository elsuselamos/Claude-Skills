# Scripts 使用說明

## fetch_macro_data.py

### 功能說明
自動從 FRED API 獲取美國總體經濟指標，包括：
- GDP 成長率
- 通膨指標（CPI, PPI, PCE）
- 利率與殖利率曲線
- 就業數據
- PMI 指數
- 消費與零售數據
- 住房市場指標
- 工業生產指標

### 前置需求

#### 1. 安裝 Python 套件
```bash
pip install requests pandas python-dotenv
