# Translation Examples

## Example 1: Rust Function Documentation

**Original:**
```rust
/// Calculate the nth Fibonacci number using an iterative approach
///
/// # Arguments
///
/// * `n` - A non-negative integer representing the position in the Fibonacci sequence
///
/// # Returns
///
/// Returns the nth Fibonacci number as u64
///
/// # Examples
///
/// ```
/// let result = fibonacci(10);
/// assert_eq!(result, 55);
/// ```
pub fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0;
            let mut b = 1;
            for _ in 2..=n {
                let temp = a + b;
                a = b;
                b = temp;
            }
            b
        }
    }
}
```

**Translation:**
```rust
/// 使用迭代方法计算第 n 个斐波那契数
///
/// # 参数
///
/// * `n` - 表示斐波那契数列位置的非负整数
///
/// # 返回值
///
/// 返回第 n 个斐波那契数，类型为 u64
///
/// # 示例
///
/// ```
/// let result = fibonacci(10);
/// assert_eq!(result, 55);
/// ```
pub fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0;
            let mut b = 1;
            for _ in 2..=n {
                let temp = a + b;
                a = b;
                b = temp;
            }
            b
        }
    }
}
```

## Example 2: AI Prompt Translation

**Original:**
> **Role:** You are a senior Rust Developer and an expert in high-performance computing.
>
> **Task:** Write a Rust function, called `calculate_fibonacci_iterative`, that calculates the $n$-th Fibonacci number using an **iterative approach** (not recursive). The function signature should accept an unsigned $32$-bit integer, `u32`, as input $n$, and return the result as `u64`. Ensure the code is idiomatic Rust and includes proper error handling for potential overflows (though less likely with `u64`). Use the `match` expression for better readability if $n$ is $0$ or $1$.

**Translation:**
> **角色：** 你是一位资深的 Rust 开发者，同时也是高性能计算领域的专家。
>
> **任务：** 编写一个 Rust 函数，名为 `calculate_fibonacci_iterative`，它使用**迭代方法**（非递归）来计算第 $n$ 个斐波那契数。该函数的签名应接受一个无符号 $32$-位整数 (`u32`) 作为输入 $n$，并返回 `u64` 类型的结果。确保代码是地道的 Rust 风格，并包含对潜在**溢出** (overflows) 的适当错误处理（尽管对于 `u64` 来说可能性较低）。如果 $n$ 是 $0$ 或 $1$，请使用 `match` 表达式以提高可读性。

## Example 3: Technical Tutorial

**Original:**
# Understanding Recursion vs Iteration

In programming, recursion and iteration are two fundamental approaches to solve repetitive problems.

## Recursion
Recursion is a technique where a function calls itself directly or indirectly. It's particularly useful for problems that have a natural recursive structure.

**Pros:**
- Elegant and concise code
- Natural fit for certain problems (tree traversal, divide and conquer)
- Easier to understand for mathematical recursive definitions

**Cons:**
- Higher memory usage due to call stack
- Risk of stack overflow for deep recursion
- Generally slower than iteration

## Iteration
Iteration uses loops to repeat a block of code until a condition is met.

**Pros:**
- More memory efficient
- Generally faster execution
- No risk of stack overflow

**Cons:**
- Can be more verbose for certain problems
- May require manual state management

**Translation:**
# 理解递归与迭代

在编程中，递归和迭代是解决重复性问题的两种基本方法。

## 递归
递归是一种函数直接或间接调用自身的技术。对于具有自然递归结构的问题特别有用。

**优点：**
- 代码优雅简洁
- 自然适用于某些问题（树遍历、分治算法）
- 更容易理解数学递归定义

**缺点：**
- 由于调用栈导致更高的内存使用
- 深度递归有栈溢出风险
- 通常比迭代慢

## 迭代
迭代使用循环重复执行代码块，直到满足特定条件。

**优点：**
- 内存效率更高
- 执行速度通常更快
- 没有栈溢出风险

**缺点：**
- 对某些问题可能更冗长
- 可能需要手动状态管理

## Example 4: API Documentation

**Original:**
# User API Documentation

## Create User
Creates a new user account with the provided information.

### Endpoint
`POST /api/users`

### Request Body
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### Response
**201 Created**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "datetime"
}
```

### Error Responses
- `400 Bad Request` - Invalid input data
- `409 Conflict` - Username or email already exists

**Translation:**
# 用户 API 文档

## 创建用户
使用提供的信息创建新用户账户。

### 接口端点
`POST /api/users`

### 请求体
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### 响应
**201 Created**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "datetime"
}
```

### 错误响应
- `400 Bad Request` - 输入数据无效
- `409 Conflict` - 用户名或邮箱已存在