# Galaxy CS 後端專案說明

## 專案概述

這是一個 **Java Spring Boot 微服務** 專案，作為平台的後端系統，主要涉及遊戲、資金管理（存款/提款）和用戶活動等功能。專案採用 mono-repo 結構，包含多個服務模組。

**核心技術棧：**
- **框架：** Spring Boot、Spring Cloud (OpenFeign)
- **資料庫：** PostgreSQL（使用 Flyway 管理遷移）
- **ORM：** MyBatis Plus
- **快取/分散式鎖：** Redis (Redisson)
- **訊息佇列：** RabbitMQ
- **任務排程：** XXL-JOB
- **可觀測性：** Micrometer、OpenTelemetry (OTLP)、Prometheus

## 目錄結構與模組

專案分為領域服務模組和聚合層模組：

- **核心領域模組：**
  - `cs-user`：用戶管理（個人資料、安全性）
  - `cs-fund`：資金交易（提款、存款、銀行卡）
  - `cs-game`：遊戲整合與管理
  - `cs-activity`：用戶活動與事件
  - `cs-message`：通知與訊息服務
  - `cs-risk`：風控與分析
  - `cs-basics`：基礎設施或共用邏輯
  - `cs-proxy`：代理/經銷商相關功能
  - `cs-gateway`：API 閘道（路由、初步認證）

- **聚合層模組（BFF/編排器）：**
  - `cs-user-aggregation`
  - `cs-fund-aggregation`
  - `cs-game-aggregation`
  - `cs-activityagg`（活動聚合）
  - `cs-message-aggregation`

## 架構模式

1. **請求流程：**
   `客戶端` -> `cs-gateway` -> `*-aggregation` 服務 -> `領域` 服務

2. **服務間通訊：**
   - **同步：** Feign Clients（例如 `userFeignClient`）
   - **非同步：** RabbitMQ（例如銀行卡審核流程）

3. **資料一致性：**
   - 使用 **領域服務** 處理核心業務邏輯
   - 大量使用 **Redis 分散式鎖**（`redisUtil.doWithRedisLock`）進行併發控制（例如防止重複綁定銀行卡）
   - 使用 **策略模式** 處理多幣種邏輯（例如 `BindCardStrategyService`，包含 CNY、THB 等實作）

## 關鍵工作流程

根目錄下有詳細的工作流程文檔：
- `bind_bank_workflow.md`：銀行卡綁定流程分析（User -> Fund -> PLT Service）
- `bind_exchange_workflow.md`、`bind_usdt_workflow.md`：其他資產類型的類似流程

## 開發規範

- **建置系統：** Maven，每個模組通常包含 `mvnw` 包裝器
- **DTO/VO 映射：** 使用 `MapStruct`（尋找 `Converter` 類別）
- **程式碼風格：** 使用 Lombok 減少樣板程式碼（`@Data`、`@Builder`）
- **驗證：** 使用標準 `javax.validation` / Hibernate Validator 註解
- **設定檔：** 使用 profiles（例如 `otlp`）
- **錯誤處理：** 使用自訂例外（例如 `BusinessException`）和錯誤碼

## 常用指令

**建置特定模組：**
```bash
cd cs-user
./mvnw clean install
```

**執行模組：**
```bash
cd cs-user
./mvnw spring-boot:run
```

**資料庫遷移：**
已設定 Flyway，遷移腳本會在應用程式啟動時或透過 Maven 外掛執行。

## 編碼指南

- 使用中文進行溝通和文檔撰寫
- 使用 `@Deprecated` 標記廢棄的功能，而不是直接刪除程式碼
- 資料庫欄位廢棄時使用 `COMMENT ON COLUMN ... IS 'DEPRECATED - ...'` 而非 `DROP COLUMN`
- 遵循現有的程式碼風格和架構模式
