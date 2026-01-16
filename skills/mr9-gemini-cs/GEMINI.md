# Galaxy CS Backend Project Context

## Project Overview

This is a **Java Spring Boot Microservices** project, serving as the backend for a platform likely involved in gaming, funds management (deposits/withdrawals), and user activities. The project is structured as a mono-repo containing multiple services.

**Key Technologies:**
- **Framework:** Spring Boot, Spring Cloud (OpenFeign)
- **Database:** PostgreSQL (managed by Flyway)
- **ORM:** MyBatis Plus
- **Caching/Locking:** Redis (Redisson)
- **Messaging:** RabbitMQ
- **Job Scheduling:** XXL-JOB
- **Observability:** Micrometer, OpenTelemetry (OTLP), Prometheus

## Directory Structure & Modules

The project is divided into domain-specific modules and aggregation layers:

- **Core Domains:**
  - `cs-user`: User management (profiles, security).
  - `cs-fund`: Financial transactions (withdrawals, deposits, bank cards).
  - `cs-game`: Game integration and management.
  - `cs-activity`: User activities and events.
  - `cs-message`: Notification and messaging services.
  - `cs-risk`: Risk control and analysis.
  - `cs-basics`: Infrastructure or common logic (likely).
  - `cs-proxy`: Proxy/Agent related functionality.
  - `cs-gateway`: API Gateway (routing, initial auth).

- **Aggregation Layers (BFF/Orchestrators):**
  - `cs-user-aggregation`
  - `cs-fund-aggregation`
  - `cs-game-aggregation`
  - `cs-activityagg` (Activity Aggregation)
  - `cs-message-aggregation`

## Architecture Patterns

1.  **Request Flow:**
    `Client` -> `cs-gateway` -> `*-aggregation` Service -> `Domain` Service.

2.  **Inter-Service Communication:**
    - **Synchronous:** Feign Clients (e.g., `userFeignClient`).
    - **Asynchronous:** RabbitMQ (e.g., bank card review workflows).

3.  **Data Consistency:**
    - Uses **Domain Services** for core business logic.
    - **Redis Distributed Locks** (`redisUtil.doWithRedisLock`) are heavily used for concurrency control (e.g., preventing duplicate bank card bindings).
    - **Strategy Pattern** is used for handling multi-currency logic (e.g., `BindCardStrategyService` with implementations for CNY, THB, etc.).

## Key Workflows

Detailed documentation exists for specific complex workflows in the root directory:
- `bind_bank_workflow.md`: Analysis of the bank card binding process (User -> Fund -> PLT Service).
- `bind_exchange_workflow.md`, `bind_usdt_workflow.md`: Likely similar flows for other asset types.

## Development Conventions

- **Build System:** Maven. Each module typically contains a `mvnw` wrapper.
- **DTO/VO Mapping:** Uses `MapStruct` (look for `Converter` classes).
- **Code Style:** Lombok is used to reduce boilerplate (`@Data`, `@Builder`).
- **Validation:** Standard `javax.validation` / Hibernate Validator annotations.
- **Configuration:** Profiles are used (e.g., `otlp`).
- **Error Handling:** Custom exceptions (e.g., `BusinessException`) with error codes.

## Common Commands

**Build a specific module:**
```bash
cd cs-user
./mvnw clean install
```

**Run a module:**
```bash
cd cs-user
./mvnw spring-boot:run
```

**Database Migrations:**
Flyway is configured. Migrations likely run on application startup or via Maven plugin.
