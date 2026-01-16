# PLT Backend - 專案說明文檔

> 此文件為 AI 編碼助手提供專案上下文和開發指南。

## 專案概述

PLT (Platform) 是一個多模組 Maven 專案，基於 Spring Boot 3.x 構建的後端服務系統，主要提供**資金管理**、**用戶管理**、**遊戲服務**、**代理系統**等核心業務功能。

## 技術棧

- **語言**: Java 17+
- **框架**: Spring Boot 3.x
- **構建工具**: Maven
- **數據庫**: PostgreSQL
- **ORM**: MyBatis Plus
- **緩存**: Redis (Redisson)
- **消息隊列**: RabbitMQ
- **數據庫遷移**: Flyway
- **監控**: Micrometer + Prometheus + OpenTelemetry
- **代碼生成**: Lombok, MapStruct

## 模組結構

```
plt/
├── pay/                       # 支付服務（獨立）
├── plt-fund/                  # 資金核心服務
├── plt-fund-aggregation/      # 資金聚合服務
├── plt-user/                  # 用戶核心服務
├── plt-user-aggregation/      # 用戶聚合服務
├── plt-account/               # 賬戶服務
├── plt-activity/              # 活動服務
├── plt-activity-aggregation/  # 活動聚合服務
├── plt-basics/                # 基礎服務
├── plt-game/                  # 遊戲核心服務
├── plt-game-aggregation/      # 遊戲聚合服務
├── plt-gateway/               # API 網關
├── plt-message/               # 消息服務
├── plt-messageagg/            # 消息聚合服務
├── plt-proxy/                 # 代理核心服務
├── plt-proxy-aggregation/     # 代理聚合服務
├── plt-proxy-gateway/         # 代理網關
├── plt-report/                # 報表核心服務
├── plt-reportagg/             # 報表聚合服務
├── plt-risk/                  # 風險控制服務
├── wallet-service/            # 錢包服務
├── wallet-aggregation/        # 錢包聚合服務
├── third-party-callback/      # 第三方回調服務
├── xxl-job/                   # 定時任務核心
├── xxl-job-admin/             # 定時任務管理
├── xxl-op-executor/           # 定時任務執行器
└── doc/                       # 設計文檔
```

## 常用命令

### 編譯專案
```bash
# 編譯全部模組（跳過測試）
mvn clean compile -DskipTests

# 編譯單一模組
mvn clean compile -DskipTests -pl plt-fund

# 打包專案
mvn clean package -DskipTests
```

### 運行服務
```bash
# 使用本地配置運行
mvn spring-boot:run -pl <module-name> -Dspring-boot.run.profiles=local
```

## 代碼規範

### 包結構
```
com.galaxy/
├── controller/v1/    # REST API 控制器
├── domain/           # 領域服務接口
│   └── impl/         # 領域服務實現
├── service/          # 業務服務
│   └── impl/         # 業務服務實現
├── storage/rdbms/
│   ├── entity/       # 數據庫實體
│   └── mapper/       # MyBatis Mapper
├── model/
│   ├── dto/          # 數據傳輸對象
│   └── vo/           # 視圖對象
└── enumeration/      # 枚舉類型
```

### 命名慣例

| 類型 | 後綴 | 範例 |
|------|------|------|
| 實體 | Entity | `WithdrawEntity` |
| DTO | Dto | `AuditPassWithdrawOrderDto` |
| VO | Vo | `WithdrawExceptionVo` |
| 領域服務 | DomainService | `WithdrawActionManageDomainService` |
| 領域服務實現 | DomainServiceImpl | `WithdrawActionManageDomainServiceImpl` |
| Mapper 接口 | Mapper | `WithdrawMapper` |
| Controller | Controller | `WithdrawActionManageController` |

### 註解使用

- **Lombok**: `@Data`, `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`
- **驗證**: `@NotNull`, `@NotBlank`, `@Size`, `@Pattern`
- **API 文檔**: 使用 Javadoc 註釋
- **廢棄標記**: `@Deprecated` 配合 Javadoc `@deprecated` 說明

## 當前進行中的工作

### 提現管理系統精簡 (Withdrawal Management Simplification)

**目標**: 移除「提款分配」和「異常提款處理」流程，實現「直通車」模式。

**狀態變更**:
- 手工出款: `1 → 2 → 3 → 4` 改為 `1 → 3 → 4`
- 三方出款: `1 → 2 → 3 → 7` 改為 `1 → 3 → 7`

**廢棄策略**: 使用 `@Deprecated` 標記，不刪除代碼。

詳見: [doc/task.md](doc/task.md), [doc/action-plan.md](doc/action-plan.md)

## 重要文件位置

| 功能 | 主要文件路徑 |
|------|-------------|
| 提現狀態枚舉 | `plt-fund/src/main/java/com/galaxy/enumeration/withdraw/WithdrawStatus.java` |
| 提現實體 | `plt-fund/src/main/java/com/galaxy/storage/rdbms/entity/WithdrawEntity.java` |
| 提現子單實體 | `plt-fund/src/main/java/com/galaxy/storage/rdbms/entity/WithdrawSubEntity.java` |
| 提現操作服務 | `plt-fund/src/main/java/com/galaxy/domain/impl/WithdrawActionManageDomainServiceImpl.java` |
| 提現控制器 | `plt-fund/src/main/java/com/galaxy/controller/v1/WithdrawActionManageController.java` |

## 注意事項

1. **多模組同步**: 部分類存在於多個模組中（如 `WithdrawStatus`），修改時需同步更新
2. **狀態機**: 提現流程涉及複雜的狀態機，修改狀態轉換時需謹慎
3. **廢棄標記**: 遵循專案的廢棄策略，使用 `@Deprecated` 而非刪除代碼
4. **數據庫字段**: 對應數據庫字段使用 `COMMENT ON COLUMN ... IS 'DEPRECATED: ...'` 標記
