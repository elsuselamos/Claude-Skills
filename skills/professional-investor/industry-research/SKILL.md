---
name: industry-research
description: 產業研究與輪動策略,整合全球頂尖投行報告,識別景氣循環中的產業機會,判斷產業競爭格局與長期趨勢,可獨立執行或承接總體經濟分析為個股選擇提供方向指引
version: 2.2.0
author: Evan
license: Proprietary
tags:
  - industry-analysis
  - sector-rotation
  - investment-themes
  - supply-demand-analysis
  - competitive-landscape
  - megatrends
  - institutional-research
---

# 產業研究與輪動 (Industry Research & Rotation)

## 概述

本模組專注於產業層面的深度研究,整合全球頂尖投行與研究機構的產業報告,搭配現有整體政策與經濟狀況,識別景氣循環中的產業機會,判斷產業競爭格局與長期趨勢,為個股選擇提供方向指引[file:1]。

**模組特性:**
- ✅ 可獨立執行產業分析
- ✅ 可承接總體經濟分析結果
- ✅ 動態追蹤最新市場趨勢
- ✅ 支援漸進式對話深入探討

### 核心理念

**選對產業比選對個股更重要**

- 產業順風時,平庸的公司也能有好表現(產業 Beta 效應)
- 產業逆風時,再優秀的公司也難有超額報酬
- 在對的時間佈局對的產業,事半功倍
- 結構性成長優於週期性反彈:長期趨勢的力量遠大於短期波動

**機構投資人的智慧**

本模組整合全球頂尖投行與研究機構的集體智慧,動態追蹤最新市場共識[file:2]。詳細機構追蹤方法請參考:
- `references/institutional/institutional-reports-tracking.md` - 機構報告追蹤方法
- `references/institutional/13f-holdings-analysis.md` - 對沖基金持倉分析

### 核心能力

1. **機構報告整合能力** - 追蹤 13F 文件與頂尖投行產業報告
2. **產業生命週期定位** - 判斷產業處於導入期/成長期/成熟期/衰退期
3. **供需分析與景氣追蹤** - 識別供需拐點與產業週期轉折
4. **競爭格局評估** - 市場集中度與龍頭企業護城河分析
5. **技術變革影響研判** - 破壞性創新與技術成熟度評估
6. **產業鏈上下游分析** - 價值鏈拆解與關鍵瓶頸識別
7. **產業輪動時機判斷** - 基於經濟週期與主題投資的動態配置

---

## 適用場景

### 應使用本模組的情境

**產業趨勢研判:**
- 「現在該佈局哪些產業?」
- 「半導體 / AI / 電動車 / 核電產業現在處於什麼階段?」
- 「哪些產業有結構性成長機會?」

**產業比較與選擇:**
- 「金融股 / 科技股 / 傳產股哪個比較好?」
- 「為什麼投行推薦國防股?邏輯是什麼?」
- 「AI 產業鏈中,哪個環節最有投資價值?」

**供需與競爭分析:**
- 「產業供需如何?庫存健康嗎?」
- 「這個產業的競爭格局如何?誰是龍頭?」
- 「產業定價權在誰手上?」

**投資組合配置:**
- 「產業輪動策略怎麼做?」
- 「各產業該配置多少權重?」
- 「什麼時候該從科技股輪動到金融股?」

### 觸發關鍵詞

**產業名稱:** 半導體、AI、電動車、核電、國防、金融、醫療、能源、消費

**產業相關:** 產業趨勢、產業週期、產業輪動、供需、競爭格局、產業鏈

**投資主題:** AI 算力、數據中心、軍備、核電、去美元化、肥胖藥、GLP-1

### 不適用情境

- 單一公司深度分析 → 使用 `equity-fundamental-analysis`
- 總體經濟環境評估 → 使用 `macro-market-analysis`
- 技術線型與進場時機 → 使用 `technical-analysis`

---

## 執行流程

### Step 1: 總體經濟環境評估(動態載入)

**檢查是否有先前的總經分析結果:**

```

IF 對話歷史中存在總經分析結果:
→ 讀取並引用以下資訊:
- 經濟週期階段(復甦期/擴張期/高峰期/衰退期)
- 市場風險偏好(Risk-On / Risk-Off)
- 央行政策立場與利率環境
- 建議股票部位比例
→ 在回應中說明:「根據先前的總經分析...」

ELSE (無先前總經分析):
→ 自行搜索當前總體經濟狀況:
- 搜索關鍵詞:「2026 經濟展望」「美國/中國/全球 經濟現況」
- 搜索關鍵詞:「美聯儲/ECB/央行 最新政策」
- 搜索關鍵詞:「2026 GDP/通膨/利率 預測」
→ 快速總結當前經濟環境(2-3 段)
→ 在回應中說明:「根據最新經濟數據搜索...」

```

**根據經濟環境初步篩選產業方向:**

詳細產業輪動策略與經濟週期對應表請參考:
- `references/frameworks/sector-rotation-by-cycle.md`

**輸出格式(簡潔版):**
```


## 當前經濟環境概況

[來源說明:先前分析結果 OR 最新搜索結果]

- **經濟週期:** [復甦期/擴張期/高峰期/衰退期]
- **央行政策:** [寬鬆/中性/緊縮]
- **風險偏好:** [Risk-On / Risk-Off]
- **優先產業方向:** [根據週期推薦的產業類別]

```

---

### Step 2: 機構報告整合與共識追蹤

**動態搜索最新機構觀點:**

```

搜索策略:

1. 頂級投行最新報告(近 1-3 個月):
    - 「J.P. Morgan 2026 產業展望」
    - 「Goldman Sachs [目標產業] 報告」
    - 「Morgan Stanley 產業配置建議」
    - 「BlackRock 2026 投資主題」
2. 13F 持倉變化(最新季度):
    - 「Bridgewater / Berkshire 最新持倉」
    - 「對沖基金 [目標產業] 持倉變化」
3. 產業專家觀點:
    - 「McKinsey / BCG / Gartner [目標產業] 趨勢」
```

**機構共識評分系統:**
```

一致看多(5 分):≥80% 機構推薦超配
偏多(4 分):60-79% 機構推薦超配
中性(3 分):40-59% 機構推薦超配
偏空(2 分):20-39% 機構推薦超配
一致看空(1 分):<20% 機構推薦超配

```

**詳細方法參考:**
- `references/institutional/institutional-reports-tracking.md`
- `references/institutional/13f-holdings-analysis.md`
- `references/institutional/consensus-scoring-system.md`

**輸出格式(簡潔版):**
```


## 機構共識追蹤

### 頂級投行觀點

- **J.P. Morgan:** [核心觀點] (來源連結)
- **Goldman Sachs:** [核心觀點] (來源連結)
- **BlackRock:** [核心觀點] (來源連結)


### 機構共識評分

[目標產業]: ⭐⭐⭐⭐ (4.2/5.0) - 偏多共識

### 關鍵發現

[3-5 個重點摘要]

```

---

### Step 3: 產業深度分析(七步驟框架)

針對目標產業執行標準化分析:

1. **產業鏈拆解** - 上中下游價值鏈與利潤分配
2. **供需關係分析** - 需求驅動、產能利用率、庫存週期
3. **競爭格局分析** - 市場集中度(HHI)、龍頭企業護城河
4. **技術與政策驅動** - 破壞性創新、政府補貼與法規支持
5. **產業估值水準** - 本益比歷史分位數、相對估值
6. **領先與落後指標** - 設定預警指標與觸發條件
7. **泡沫風險評估** - 估值、情緒、基本面、機構面檢查清單

**詳細框架參考:**
- `references/frameworks/seven-step-industry-analysis.md`
- `references/frameworks/supply-demand-framework.md`
- `references/frameworks/competitive-landscape-framework.md`
- `references/frameworks/bubble-risk-assessment.md`

**輸出格式(漸進式對話):**
```


## [目標產業]深度分析

### 產業鏈結構

[簡要說明上中下游,標註關鍵環節]

### 供需狀況

- **需求驅動:** [主要成長動能]
- **供給狀況:** [產能利用率/庫存水位]
- **供需評分:** [1-10 分]


### 競爭格局

- **市場集中度:** [高/中/低]
- **龍頭企業:** [列出前 3-5 名]
- **進入障礙:** [高/中/低]


### 技術與政策

- **技術趨勢:** [關鍵技術變革]
- **政策支持:** [政府補貼/法規影響]


### 估值與風險

- **估值水準:** [相對歷史/同業的位置]
- **泡沫風險:** [低/中/高]

***
💡 **想深入了解某個部分嗎?**
您可以進一步詢問:

- 「產業鏈中哪個環節利潤最高?」
- 「主要競爭對手有哪些?優劣勢分析?」
- 「有哪些領先指標可以追蹤?」

```

---

### Step 4: 核心投資趨勢評估(動態更新)

**實時搜索與分析當前熱門趨勢:**

```

搜索策略:

1. 當前熱門投資主題(近 1 個月):
    - 「2026 投資主題」「investment themes 2026」
    - 「2026 megatrends」「emerging sectors 2026」
2. 產業熱度與資金流向:
    - 「[年份] ETF 資金流向」
    - 「institutional investors [產業] allocation」
3. 政策與地緣政治驅動:
    - 「美國/中國/歐盟 產業政策 2026」
    - 「geopolitical impact [產業]」
4. 技術突破與創新:
    - 「breakthrough technology 2026」
    - 「disruptive innovation [產業]」
```

**趨勢評估框架:**
```

對每個識別出的趨勢進行評分:

1. 機構共識度 (0-5 分):頂級投行推薦程度
2. 政策支持度 (0-5 分):政府補貼與法規力度
3. 技術成熟度 (0-5 分):商業化進展
4. 市場規模潛力 (0-5 分):TAM 與成長性
5. 時間週期 (短期/中期/長期):趨勢持續性

總分 ≥ 18 分 → 核心趨勢 (⭐⭐⭐⭐⭐)
總分 15-17 分 → 重要趨勢 (⭐⭐⭐⭐)
總分 12-14 分 → 關注趨勢 (⭐⭐⭐)
總分 < 12 分 → 觀察趨勢 (⭐⭐)

```

**詳細分析參考:**
- `references/themes/trend-evaluation-framework.md` - 趨勢評估方法論
- `references/themes/policy-tracking.md` - 政策追蹤指南
- `references/themes/technology-maturity-assessment.md` - 技術成熟度評估

**輸出格式(動態生成):**
```


## 當前核心投資趨勢 (基於最新搜索)

### 🔥 核心趨勢 (⭐⭐⭐⭐⭐)

1. **[趨勢名稱]**
    - 驅動因素: [關鍵動能]
    - 機構共識: [X/5] | 政策支持: [X/5] | 技術成熟: [X/5]
    - 受益產業: [列出 2-3 個]
    - 投資時間軸: [短期/中期/長期]
2. **[趨勢名稱]**
...

### ⚡ 重要趨勢 (⭐⭐⭐⭐)

[同上格式]

### 👀 新興趨勢 (⭐⭐⭐)

[處於早期階段但潛力大的趨勢]

***
📊 **數據來源:** [列出主要參考來源與時間]
💡 **想深入某個趨勢?** 可以問:「詳細分析 [趨勢名稱]」

```

---

### Step 5: 產業輪動策略制定

**輪動時機判斷(滿足任一即啟動):**
- 經濟週期階段轉換
- 央行政策立場轉向
- 產業供需關係逆轉
- 機構共識評分變化 ≥1.0 分
- 關鍵領先指標連續 2 個月轉向

**動態配置建議(基於當前環境):**
```

基於 Step 1(經濟環境) + Step 2(機構共識) + Step 4(趨勢評估)
→ 生成當前時點的產業配置建議

```

**詳細策略參考:**
- `references/frameworks/sector-rotation-by-cycle.md`
- `references/frameworks/rotation-decision-checklist.md`

**輸出格式(簡潔版):**
```


## 產業配置建議 (基於 [日期] 環境)

| 產業 | 配置權重 | 配置邏輯 | 風險提示 |
| :-- | :-- | :-- | :-- |
| [產業A] | 25-30% | [核心理由] | [主要風險] |
| [產業B] | 15-20% | [核心理由] | [主要風險] |
| ... | ... | ... | ... |

### 輪動訊號追蹤

- ✅ [已觸發的訊號]
- ⏳ [接近觸發的訊號]

***
💡 **配置原則:**

- 單一產業上限 30%
- 前三大合計 60-70%
- 保留 10-15% 現金彈性

```

---

### Step 6: 分析結果輸出(對話串漸進式呈現)

**輸出原則:**
- ✅ 在對話串中直接呈現核心結果(3-5 個段落)
- ✅ 使用結構化格式(表格/列表/評分)
- ✅ 提供互動式引導,讓使用者深入詢問
- ❌ 不預設生成完整多頁報告

**標準輸出結構(精簡版):**
```markdown
# [目標產業/主題] 產業研究分析

## 📊 執行摘要
- **產業評級:** [買進/持有/觀望/減碼] 
- **機構共識:** ⭐⭐⭐⭐ (4.2/5.0)
- **產業景氣:** [1-10 分]
- **配置建議:** [超配/標配/低配]
- **投資時間軸:** [短期/中期/長期]

## 🎯 核心發現
[3-5 個最重要的結論,每個 1-2 句話]

## 💼 機構觀點摘要
[頂級投行核心觀點,2-3 段]

## 📈 產業基本面
[供需/競爭格局/估值 關鍵數據,使用表格呈現]

## ⚠️ 風險提示
[主要風險因素,3-5 點]

## 🎬 下一步建議
[具體可執行的操作建議]

***
## 💬 想進一步了解?

您可以繼續詢問:
- 「這個產業的具體公司推薦?」→ 觸發第三階段個股分析
- 「產業鏈上下游詳細拆解?」→ 深入產業鏈分析
- 「與 [其他產業] 比較?」→ 多產業比較分析  
- 「生成完整 PDF 報告」→ 觸發完整報告模板
```

**完整報告範本(僅在明確要求時使用):**

- `references/templates/industry-report-template.md` - 15-20 頁深度報告
- `references/templates/sector-comparison-template.md` - 多產業比較報告
- `references/templates/quick-insight-template.md` - 2-3 頁快速洞察

---

## 參考資料體系

### 核心框架文檔(必讀)

**分析方法論:**

- `references/frameworks/seven-step-industry-analysis.md`
- `references/frameworks/sector-rotation-by-cycle.md`
- `references/frameworks/supply-demand-framework.md`
- `references/frameworks/competitive-landscape-framework.md`

**機構追蹤:**

- `references/institutional/institutional-reports-tracking.md`
- `references/institutional/13f-holdings-analysis.md`
- `references/institutional/consensus-scoring-system.md`

**趨勢評估:**

- `references/themes/trend-evaluation-framework.md`
- `references/themes/policy-tracking.md`
- `references/themes/technology-maturity-assessment.md`

**數據來源:**

- `references/data-sources/industry-data-sources.md`
- `references/data-sources/leading-indicators.md`

**實用範本:**

- `references/templates/industry-report-template.md`
- `references/templates/quick-insight-template.md`
- `references/templates/rotation-decision-checklist.md`


### 外部資源(精選)

**頂級投行研究:**

- [J.P. Morgan Markets](https://www.jpmorgan.com/insights/research)
- [Goldman Sachs Research](https://www.goldmansachs.com/insights/pages/top-of-mind.html)
- [Morgan Stanley Research](https://www.morganstanley.com/ideas)
- [BlackRock Investment Institute](https://www.blackrock.com/corporate/insights/blackrock-investment-institute)

**完整資源清單:** `references/data-sources/external-resources.md`

---

## 常見問題

**Q1: 沒有先前的總經分析,模組能獨立運作嗎?**
可以。模組會自動搜索最新經濟數據與環境評估,快速建立背景脈絡[file:1]。

**Q2: 如何判斷產業處於生命週期的哪個階段?**
使用三指標:營收成長率、市場滲透率、競爭格局。詳見 `references/frameworks/seven-step-industry-analysis.md`

**Q3: 如何確保趨勢分析的時效性?**
每次執行時動態搜索最新 1-3 個月的機構報告與市場數據,避免使用過時資訊。

**Q4: 產業輪動的最佳時機?**
領先市場 1-2 個月最佳,使用輪動訊號確認檢查表(至少滿足 3 項條件)。詳見 `references/frameworks/rotation-decision-checklist.md`

**Q5: 如何避免產業配置過度集中?**
使用「331 配置原則」:單一產業上限 30%、前三大合計 60-70%、其他分散 30-40%[file:1]。

**Q6: 如果需要完整報告怎麼辦?**
在對話中明確要求:「生成完整產業研究報告」,系統會使用標準範本產出 15-20 頁深度分析。
