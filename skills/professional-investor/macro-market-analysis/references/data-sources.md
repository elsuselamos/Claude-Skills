---
title: 總體經濟數據來源
version: 1.0.0
last_updated: 2026-01-02
---

# 總體經濟數據來源 (Economic Data Sources)

## 使用指引

當需要獲取最新總體經濟數據時，請使用 `search_web` 或 `get_full_page_content` 工具直接訪問以下網站。

---

## 🇺🇸 美國經濟數據

### 1. FRED (Federal Reserve Economic Data) - 最權威來源
**網站：** https://fred.stlouisfed.org/

**主要指標直達連結：**

#### GDP 與經濟成長
- **實質 GDP 成長率**: https://fred.stlouisfed.org/series/A191RL1Q225SBEA
- **實質 GDP**: https://fred.stlouisfed.org/series/GDPC1

#### 通膨指標
- **CPI (消費者物價指數)**: https://fred.stlouisfed.org/series/CPIAUCSL
- **核心 CPI (排除食品與能源)**: https://fred.stlouisfed.org/series/CPILFESL
- **PPI (生產者物價指數)**: https://fred.stlouisfed.org/series/PPIACO
- **PCE (個人消費支出物價)**: https://fred.stlouisfed.org/series/PCEPI
- **核心 PCE (Fed 首選)**: https://fred.stlouisfed.org/series/PCEPILFE

#### 利率與殖利率
- **聯邦基金利率**: https://fred.stlouisfed.org/series/FEDFUNDS
- **10 年期公債殖利率**: https://fred.stlouisfed.org/series/DGS10
- **2 年期公債殖利率**: https://fred.stlouisfed.org/series/DGS2
- **30 年期房貸利率**: https://fred.stlouisfed.org/series/MORTGAGE30US

#### 就業數據
- **失業率**: https://fred.stlouisfed.org/series/UNRATE
- **非農就業人數**: https://fred.stlouisfed.org/series/PAYEMS
- **初領失業救濟金人數**: https://fred.stlouisfed.org/series/ICSA
- **平均時薪**: https://fred.stlouisfed.org/series/CES0500000003
- **勞動參與率**: https://fred.stlouisfed.org/series/CIVPART

#### 消費與零售
- **零售銷售 (排除汽車)**: https://fred.stlouisfed.org/series/RSXFS
- **個人消費支出**: https://fred.stlouisfed.org/series/PCE

#### 工業生產
- **工業生產指數**: https://fred.stlouisfed.org/series/INDPRO
- **產能利用率**: https://fred.stlouisfed.org/series/TCU

#### 住房市場
- **新屋開工**: https://fred.stlouisfed.org/series/HOUST
- **營建許可**: https://fred.stlouisfed.org/series/PERMIT
- **Case-Shiller 房價指數**: https://fred.stlouisfed.org/series/CSUSHPISA

**使用方法：**
使用 get_full_page_content 工具訪問上述連結，提取最新數值、日期、以及圖表數據。
FRED 頁面結構清晰，易於解析。

---

### 2. Trading Economics - 全球數據整合平台
**網站：** https://tradingeconomics.com/

**主要功能：**
- 全球經濟數據日曆
- 即時指標更新
- 跨國比較

**常用頁面：**
- **美國經濟數據總覽**: https://tradingeconomics.com/united-states/indicators
- **經濟日曆 (未來數據發布時間)**: https://tradingeconomics.com/calendar
- **CPI 數據**: https://tradingeconomics.com/united-states/inflation-cpi
- **GDP 數據**: https://tradingeconomics.com/united-states/gdp-growth
- **失業率**: https://tradingeconomics.com/united-states/unemployment-rate

**使用方法：**
適合快速查看最新值與趨勢圖，也可查詢其他國家數據。

---

### 3. BLS (Bureau of Labor Statistics) - 就業數據官方來源
**網站：** https://www.bls.gov/

**主要報告：**
- **月度就業報告 (Employment Situation)**: https://www.bls.gov/news.release/empsit.nr0.htm
  - 包含非農就業、失業率、薪資數據
- **CPI 報告**: https://www.bls.gov/news.release/cpi.nr0.htm
- **PPI 報告**: https://www.bls.gov/news.release/ppi.nr0.htm

**使用時機：**
數據發布當天（通常每月第一個週五），可直接爬取新聞稿獲得最新數據與 BLS 官方解讀。

---

### 4. Fed 官方網站
**網站：** https://www.federalreserve.gov/

**重要資源：**
- **FOMC 會議聲明**: https://www.federalreserve.gov/newsevents/pressreleases.htm
- **FOMC 會議紀要 (Minutes)**: 會議後 3 週發布
- **Fed 官員演講**: https://www.federalreserve.gov/newsevents/speeches.htm
- **經濟預測 (Summary of Economic Projections)**: 包含 Dot Plot

**使用方法：**
當需要解讀 Fed 政策時，使用 search_web 搜尋最新 FOMC 聲明或官員發言。


---

### 5. CME FedWatch Tool - Fed 利率預期
**網站：** https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html

**功能：**
- 市場對 Fed 未來利率決策的定價
- 升息/降息機率預測

**使用方法：**
使用 get_full_page_content 提取當前市場對下次 FOMC 會議的利率預期機率。


---

## 🌏 其他主要經濟體數據

### 中國
- **國家統計局**: http://www.stats.gov.cn/english/
- **Trading Economics 中國**: https://tradingeconomics.com/china/indicators

### 歐盟
- **Eurostat**: https://ec.europa.eu/eurostat
- **ECB (歐洲央行)**: https://www.ecb.europa.eu/

### 台灣
- **中華民國統計資訊網**: https://www.stat.gov.tw/
- **中央銀行**: https://www.cbc.gov.tw/
- **主計總處**: https://www.dgbas.gov.tw/

---

## 📊 市場情緒與技術指標

### 1. CNN Fear & Greed Index
**網站：** https://edition.cnn.com/markets/fear-and-greed

**用途：** 衡量市場情緒（0-100，恐懼到貪婪）

### 2. CBOE VIX Index
**網站：** https://www.cboe.com/tradable_products/vix/

**用途：** 波動率指數，市場恐慌程度

### 3. Put/Call Ratio
**數據源：** CBOE 或各大財經網站
**用途：** 選擇權市場情緒

---

## 📈 產業數據

### 半導體產業
- **SEMI (國際半導體產業協會)**: https://www.semi.org/en
  - B/B Ratio (Book-to-Bill Ratio)
- **TSMC 法說會資料**: https://investor.tsmc.com/chinese

### AI 產業
- **NVIDIA 財報**: https://investor.nvidia.com/
- **雲端 CapEx 數據**: 各大科技公司財報

### 能源產業
- **EIA (美國能源資訊局)**: https://www.eia.gov/
  - 原油庫存、產量

### 黃金
- **World Gold Council**: https://www.gold.org/
- **Gold Price (即時金價)**: https://www.gold.org/goldhub/data/gold-prices

---

## 🔍 使用範例

### 範例 1：獲取最新 CPI 數據

**步驟：**
1. 使用 `get_full_page_content` 訪問 https://fred.stlouisfed.org/series/CPIAUCSL
2. 提取頁面中的最新值、日期、YoY 變化
3. 使用 `search_web` 搜尋 "latest CPI report BLS" 獲取 BLS 官方解讀
4. 結合 `references/economic-indicators.md` 中的解讀框架進行分析

### 範例 2：判斷 Fed 政策立場

**步驟：**
1. 使用 `search_web` 搜尋 "latest FOMC statement"
2. 使用 `get_full_page_content` 訪問 Fed 官網最新聲明
3. 使用 CME FedWatch Tool 查看市場預期
4. 結合 `references/fed-policy-framework.md` 解讀政策方向

### 範例 3：評估殖利率曲線

**步驟：**
1. 訪問 https://fred.stlouisfed.org/series/DGS10 (10Y)
2. 訪問 https://fred.stlouisfed.org/series/DGS2 (2Y)
3. 計算利差 (10Y - 2Y)
4. 使用 `references/economic-indicators.md` 解讀倒掛意義

---

## ⚠️ 注意事項

### 數據發布時間
- **非農就業報告**: 每月第一個週五（美東時間 08:30）
- **CPI 報告**: 每月中旬
- **FOMC 會議**: 每年 8 次（約每 6 週）
- **GDP 報告**: 每季度末後約 1 個月

### 數據修正
許多經濟數據會有「初值 → 修正值 → 終值」，需關注後續修正。

### 網站變動
如網頁結構變動導致無法提取數據，請：
1. 使用 `search_web` 搜尋最新數據
2. 改用 Trading Economics 等替代來源
3. 通知 Skill 維護者更新連結

---

## 🔄 更新頻率建議

- **每日必查**: Fed Funds Rate, VIX, 殖利率曲線
- **每週必查**: 初領失業救濟金人數
- **每月必查**: CPI, 非農就業, 零售銷售
- **每季必查**: GDP 成長率

---

**最後更新：** 2026-01-02
