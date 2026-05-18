# Spring 声明式事务 @Transactional 完整详解（面试+开发必备）

## 前言

Spring 声明式事务是日常开发中**最常用、最核心、最容易踩坑**的技术点，尤其在秒杀、订单、转账等**高并发 + 数据一致性**业务中至关重要。

本文基于**官方标准原理**，覆盖：核心原理、代理机制、事务失效场景、AOP 关联、本类调用坑、锁与事务顺序，帮你彻底吃透，可作为长期查阅手册。

---

## 一、什么是 Spring 声明式事务

### 1. 定义

Spring 声明式事务是 **Spring AOP 基于动态代理实现的事务管理机制**。

开发者只需要添加 `@Transactional` 注解，即可自动实现：

- 开启事务

- 提交事务

- 异常回滚事务

- 事务传播、隔离级别控制

无需手动编写 `connection.setAutoCommit(false)` 等原生代码，实现业务与事务解耦。

### 2. 核心优点

- 无侵入：业务代码与事务代码完全分离，不改动核心业务逻辑

- 简洁易用：一个注解即可完成事务配置，降低开发成本

- 统一管理：事务的开启、提交、回滚由 Spring 统一控制，便于维护和扩展

---

## 二、Spring 声明式事务 底层实现原理（最重要）

### 1. 核心：基于 AOP + 动态代理

Spring 事务 **不是魔法**，它的本质是：

### **AOP 切面 = 事务增强逻辑**

### **动态代理 = 承载事务功能的对象**

#### 执行流程（核心必记）：

1. Spring 启动时，扫描所有带有 `@Transactional` 注解的类/方法

2. 为带有注解的目标类，生成 **动态代理对象（Proxy）**

3. 代理对象在**目标方法执行前后，自动织入事务逻辑**（开启、提交、回滚）

#### 直观流程示意：

```java
// 代理对象调用方法的完整流程
代理对象.method() {
    1. 开启事务（connection.setAutoCommit(false)）;
    2. try {
        目标对象.method(); // 执行开发者编写的业务逻辑
        3. 提交事务（connection.commit()）;
       } catch (Exception e) {
        4. 回滚事务（connection.rollback()）;
       }
}
```

#### 关键补充（贴合核心坑点）

很多开发者会踩一个核心误区：在本类中直接调用带有 `@Transactional` 注解的方法，误以为事务会生效，实则不然。`@Transactional` 注解的本质是 Spring AOP 定义的一个事务切面标识，其事务增强逻辑（开启、提交、回滚）需要通过 Spring 生成的代理对象调用才能触发；若在本类中直接通过 `this` 调用注解方法，不会经过代理对象，也就不会触发切面的事务增强，此时事务注解相当于无效。

需要特别说明的是，原句“事务注解的本质是一个切面类”表述不够严谨：准确来说，`@Transactional` 是一个**切面标识注解**，Spring 会通过该注解识别需要织入事务切面的方法，真正的事务切面逻辑由 Spring 内部的 `TransactionInterceptor`（事务拦截器）实现，而非注解本身是切面类。但原句核心逻辑（“代理对象调用才生效，本类直接调用不经过切面”）完全正确，是日常开发中最常见的事务失效场景。

### 2. 两种代理策略（Spring 自动选择）

- **JDK 动态代理**：当目标类实现了接口时，Spring 会使用 JDK 动态代理生成代理对象（基于接口代理），代理对象实现目标类的所有接口，并重写接口中的方法，织入事务逻辑。

- **CGLIB 代理**：当目标类没有实现接口时，Spring 会使用 CGLIB 代理（基于子类继承），生成目标类的子类作为代理对象，重写目标类的方法，织入事务逻辑。

补充：Spring Boot 2.x 版本后，默认开启 CGLIB 代理，即使目标类实现了接口，也会优先使用 CGLIB 代理（可通过配置修改）。

### 3. 最重要结论（刻在脑子里）

### **Spring 声明式事务，只有通过【代理对象】调用才生效！**

直接调用目标对象（this 关键字）**事务完全失效！**（这是最经典、最容易踩的坑）

---

## 三、@Transactional 执行流程（标准流程）

```java
1. 客户端调用目标方法 → 实际进入代理对象
2. 代理对象开启事务（设置事务属性、获取数据库连接、关闭自动提交）
3. 代理对象调用目标对象的真实方法（执行业务逻辑：如扣库存、创建订单）
4. 若业务逻辑无异常 → 代理对象提交事务（释放连接）
5. 若业务逻辑抛出异常 → 代理对象回滚事务（释放连接）
6. 事务执行完毕，返回结果给客户端
```

---

## 四、Spring 事务生效的 4 个必要条件（缺一不可）

只有同时满足以下 4 个条件，@Transactional 注解才会生效，否则事务失效：

1. **方法必须是 public 修饰**：Spring 事务代理只对 public 方法进行增强，private、protected、default 修饰的方法，事务不生效。原因是 Spring AOP 底层依赖 JDK 动态代理或 CGLIB 代理，private 方法无法被重写，无法织入事务逻辑。

2. **目标类必须被 Spring 管理**：目标类必须添加 @Service、@Component 等注解，被 Spring 容器扫描并实例化，否则无法生成代理对象，事务也无法生效。若手动 new 一个目标类对象，调用其注解方法，事务必然失效。

3. **必须通过代理对象调用**：如前文所述，`@Transactional` 基于 AOP 切面实现，只有通过 Spring 生成的代理对象调用注解方法，才能触发切面的事务增强；本类内部 `this` 直接调用，不会经过代理，事务失效。

4. **异常需被 Spring 捕获**：默认情况下，Spring 只对 `RuntimeException` 和 `Error` 类型的异常进行事务回滚，若异常被手动 catch 且未重新抛出，事务不会回滚；若需对所有异常回滚，需配置 `rollbackFor = Exception.class`。

---

## 五、最经典坑：本类内部调用（this调用）事务失效

### 1. 失效代码示例（日常开发高频错误）

```java
@Service
public class OrderService {

    // 无事务注解的方法
    public void createOrder(Long voucherId) {
        // this 是当前 OrderService 的真实对象，不是代理对象
        this.doCreateOrder(voucherId); // 本类直接调用，事务失效
    }

    // 有事务注解的方法
    @Transactional
    public void doCreateOrder(Long voucherId) {
        // 扣库存
        seckillService.update().setSql("stock = stock - 1").eq("voucher_id", voucherId).update();
        // 创建订单
        VoucherOrder order = new VoucherOrder();
        order.setVoucherId(voucherId);
        orderService.save(order);
    }
}
```

### 结果：**事务失效！** 若扣库存成功但创建订单失败，库存不会回滚，导致数据不一致。

### 失效原因

- `createOrder()` 内部调用 `doCreateOrder()` 时，使用的是 `this` 关键字，`this` 指向的是 OrderService 的**真实对象**，而非 Spring 生成的代理对象。

- 真实对象没有被 AOP 织入事务增强逻辑，调用其注解方法时，不会开启、提交或回滚事务，事务注解完全无效。

### 2. 解决方案：获取代理对象调用（秒杀业务常用）

#### 步骤 1：开启代理对象暴露

在 Spring 配置类或 Service 类上添加 `@EnableAspectJAutoProxy(exposeProxy = true)`，作用是将 Spring 生成的代理对象暴露到 AopContext 中，便于手动获取。

```java
@EnableAspectJAutoProxy(exposeProxy = true) // 开启代理暴露
@Service
public class OrderService {
    // 业务方法...
}
```

#### 步骤 2：手动获取代理对象，调用事务方法

```java
@Service
public class OrderService {

    public void createOrder(Long voucherId) {
        // 获取当前类的 Spring 代理对象
        OrderService proxy = (OrderService) AopContext.currentProxy();
        // 用代理对象调用事务方法 → 事务生效
        proxy.doCreateOrder(voucherId);
    }

    @Transactional
    public void doCreateOrder(Long voucherId) {
        // 扣库存、创建订单（事务生效）
        seckillService.update().setSql("stock = stock - 1").eq("voucher_id", voucherId).update();
        VoucherOrder order = new VoucherOrder();
        order.setVoucherId(voucherId);
        orderService.save(order);
    }
}
```

### 补充说明

若不开启 `exposeProxy = true`，调用 `AopContext.currentProxy()` 会抛出 `IllegalStateException` 异常，提示“Cannot find current proxy: Set 'exposeProxy' property on Advised to 'true' to make it available.”。

---

## 六、AOP 与事务到底是什么关系？

### 一句话总结：

### **AOP 是机制，事务是 AOP 的一种具体增强功能**

#### 核心关系图（必记）：

#### 关键关联点

- 没有 AOP，就没有 Spring 声明式事务：Spring 事务的实现完全依赖 AOP 的动态代理和切面织入能力，若禁用 AOP，@Transactional 注解会完全失效。

- 代理对象是 AOP 与事务的桥梁：代理对象承载了 AOP 织入的事务逻辑，是事务生效的核心载体。

- @Transactional 是 AOP 切面的“标识”：Spring 通过该注解识别需要织入事务切面的方法，无需开发者手动编写切面逻辑。

---

## 七、@Transactional 常用配置（开发必备）

@Transactional 注解支持多种配置参数，可根据业务需求灵活调整，核心配置如下：

```java
@Transactional(
    rollbackFor = Exception.class,      // 所有异常都回滚（推荐配置）
    propagation = Propagation.REQUIRED, // 事务传播级别（默认）
    isolation = Isolation.READ_COMMITTED, // 事务隔离级别（默认）
    timeout = 3, // 事务超时时间（单位：秒），超过时间自动回滚
    readOnly = false // 是否为只读事务，查询操作可设为true，提升性能
)
```

### 1. 事务传播机制（常用，面试高频）

事务传播机制定义了“当一个事务方法调用另一个事务方法时，事务如何传递”，核心常用的 4 种：

- **Propagation.REQUIRED（默认）**：如果当前存在事务，就加入当前事务；如果当前没有事务，就新建一个事务。（最常用，如订单创建时，扣库存和创建订单共用一个事务）

- **Propagation.REQUIRES_NEW**：无论当前是否存在事务，都新建一个独立的事务，原事务暂停，新事务执行完毕后，原事务继续执行。（如日志记录，无论订单事务是否成功，日志都必须保存）

- **Propagation.NESTED**：嵌套事务，在当前事务内部新建一个子事务，子事务回滚不影响父事务，但父事务回滚会带动子事务回滚。（如订单创建时，先扣库存，再创建订单，库存扣减失败则订单不创建，订单创建失败可回滚库存）

- **Propagation.SUPPORTS**：支持当前事务，如果当前存在事务，就加入事务；如果当前没有事务，就以非事务方式执行。（很少用，适合查询操作）

### 2. 事务隔离级别（解决并发问题）

事务隔离级别用于解决并发场景下的脏读、不可重复读、幻读问题，MySQL 默认隔离级别是 READ_COMMITTED，Spring 事务默认也是该级别：

- **READ_UNCOMMITTED**：最低隔离级别，允许读取未提交的数据，会出现脏读、不可重复读、幻读。（不推荐使用）

- **READ_COMMITTED（开发常用）**：允许读取已提交的数据，可避免脏读，会出现不可重复读、幻读。（MySQL 默认，Spring 默认）

- **REPEATABLE_READ**：可重复读，保证同一事务内多次读取同一数据结果一致，可避免脏读、不可重复读，会出现幻读。（InnoDB 引擎通过 MVCC 机制避免幻读）

- **SERIALIZABLE**：最高隔离级别，串行执行所有事务，可避免所有并发问题，但性能极差，适合并发量极低的场景。（不推荐使用）

### 3. 其他常用配置

- **rollbackFor**：指定需要回滚的异常类型，默认只回滚 RuntimeException 和 Error，推荐配置 `rollbackFor = Exception.class`，确保所有异常都能回滚。

- **timeout**：事务超时时间，超过指定时间（单位：秒），Spring 会自动回滚事务，避免事务长时间占用数据库连接。

- **readOnly**：是否为只读事务，查询操作可设为 true，Spring 会优化事务性能，避免不必要的事务操作；增删改操作必须设为 false（默认）。

---

## 八、事务失效 10 大场景（面试必考）

结合前文内容，总结日常开发中最常见的 10 种事务失效场景，帮你快速避坑：

1. **非 public 方法**：private、protected、default 修饰的方法，事务不生效（Spring 只增强 public 方法）。

2. **final/private 方法**：final 方法无法被代理对象重写，AOP 无法织入事务逻辑，事务失效；private 方法同理。

3. **本类内部调用（this 调用）**：最经典场景，this 是真实对象，不经过代理，事务失效。

4. **异常被 catch 吃掉**：异常被手动 catch 且未重新抛出，Spring 无法捕获异常，无法触发回滚，事务失效。

5. **数据库不支持事务**：如 MySQL 的 MyISAM 引擎，不支持事务，即使添加 @Transactional 注解，也不会有事务效果（推荐使用 InnoDB 引擎）。

6. **目标类未被 Spring 管理**：目标类未添加 @Service、@Component 等注解，未被 Spring 扫描为 Bean，无法生成代理对象，事务失效。

7. **事务传播级别配置错误**：如配置为 Propagation.NOT_SUPPORTED（不支持事务），即使添加注解，也会以非事务方式执行。

8. **多线程调用**：一个事务方法调用另一个线程的事务方法，两个方法不在同一个事务中，事务无法共享，会出现事务失效（如异步方法调用）。

9. **类未被代理**：未开启 AOP 代理（未加 @EnableAspectJAutoProxy），或目标类是 final 类（无法被 CGLIB 代理），无法生成代理对象，事务失效。

10. **异常类型不匹配**：默认只回滚 RuntimeException 和 Error，若抛出 checked 异常（如 IOException），未配置 rollbackFor，事务不会回滚。

---

## 九、高并发关键：锁与事务的顺序（秒杀必看）

在秒杀、订单等高并发场景中，锁与事务的顺序直接影响数据一致性，若顺序错误，会导致一人多单、超卖等问题。

### 1. 错误顺序（高频错误，会导致并发安全问题）

```java
@Transactional
public Result createOrder(Long voucherId) {
    Long userId = UserHolder.getUser().getId();
    // 错误：先开启事务，再加锁
    synchronized (userId.toString().intern()) {
        // 一人一单判断
        int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
        if (count > 0) {
            return Result.fail("您已经购买过一次了");
        }
        // 扣库存
        boolean success = seckillService.update().setSql("stock = stock - 1").eq("voucher_id", voucherId).gt("stock", 0).update();
        if (!success) {
            return Result.fail("库存不足！");
        }
        // 创建订单
        VoucherOrder order = new VoucherOrder();
        order.setVoucherId(voucherId);
        order.setUserId(userId);
        orderService.save(order);
        return Result.ok(order.getId());
    }
}
```

### 错误原因

先开启事务，再加锁，执行完业务逻辑后，锁会先释放，而事务可能还未提交（事务提交需要时间）。此时其他线程获取锁后，查询到的是未提交的事务数据（脏读），会导致一人多单、超卖。

### 2. 正确顺序（必须记住，秒杀安全核心）

```java
public Result createOrder(Long voucherId) {
    Long userId = UserHolder.getUser().getId();
    // 正确：先加锁，再开启事务（通过代理调用事务方法）
    synchronized (userId.toString().intern()) {
        // 获取代理对象，调用事务方法
        OrderService proxy = (OrderService) AopContext.currentProxy();
        return proxy.doCreateOrder(voucherId);
    }
}

// 事务方法单独抽取，由代理对象调用
@Transactional
public Result doCreateOrder(Long voucherId) {
    Long userId = UserHolder.getUser().getId();
    // 一人一单判断
    int count = query().eq("user_id", userId).eq("voucher_id", voucherId).count();
    if (count > 0) {
        return Result.fail("您已经购买过一次了");
    }
    // 扣库存（乐观锁防止超卖）
    boolean success = seckillService.update().setSql("stock = stock - 1").eq("voucher_id", voucherId).gt("stock", 0).update();
    if (!success) {
        return Result.fail("库存不足！");
    }
    // 创建订单
    VoucherOrder order = new VoucherOrder();
    order.setVoucherId(voucherId);
    order.setUserId(userId);
    orderService.save(order);
    return Result.ok(order.getId());
}
```

### 正确逻辑顺序（刻在脑子里）

### 核心优势

锁包住整个事务，保证事务提交完成后再释放锁，避免其他线程读取未提交的脏数据，确保高并发场景下的数据一致性（一人一单、不超卖）。

---

## 十、终极总结（最强记忆版）

1. **核心原理**：Spring 声明式事务 = AOP + 动态代理，@Transactional 是 AOP 切面标识，代理对象织入事务逻辑。

2. **生效关键**：只有通过代理对象调用，事务才生效；this 调用（真实对象）事务失效。

3. **本类调用解决方案**：开启 @EnableAspectJAutoProxy(exposeProxy = true)，通过 AopContext.currentProxy() 获取代理对象。

4. **生效三要素**：public 方法 + Spring 管理的 Bean + 代理对象调用。

5. **高并发顺序**：锁 → 代理调用 → 事务 → 业务 → 提交事务 → 释放锁。

6. **避坑重点**：避免 10 大事务失效场景，尤其注意本类调用、异常被 catch、非 public 方法。

---

## 十一、Spring 事务面试题 20 道（含标准答案）

### 基础题（必背）

1. **问题**：Spring 声明式事务的核心原理是什么？
   **答案**：基于 AOP 动态代理实现，通过 @Transactional 注解标识需要织入事务逻辑的方法，Spring 生成代理对象，在目标方法前后自动织入开启、提交、回滚事务的逻辑。

2. **问题**：@Transactional 注解作用在类上和方法上有什么区别？
   **答案**：作用在类上，该类中所有 public 方法都会生效；作用在方法上，只有该方法生效，方法上的配置会覆盖类上的配置。

3. **问题**：Spring 事务的两种代理方式是什么？区别是什么？
   **答案**：JDK 动态代理（基于接口，代理对象实现接口）和 CGLIB 代理（基于子类，生成目标类的子类）；区别：JDK 代理要求目标类实现接口，CGLIB 代理无要求，但目标类不能是 final 类。

4. **问题**：Spring 事务生效的必要条件有哪些？
   **答案**：4 个：方法是 public 修饰、目标类被 Spring 管理、通过代理对象调用、异常被 Spring 捕获。

5. **问题**：@Transactional 注解默认回滚哪些异常？
   **答案**：默认只回滚 RuntimeException（运行时异常）和 Error（错误），checked 异常（如 IOException）不会回滚。

### 进阶题（面试高频）

1. **问题**：本类内部调用事务方法，为什么事务会失效？如何解决？
   **答案**：原因：本类调用使用 this 关键字，指向真实对象，不经过代理对象，AOP 无法织入事务逻辑；解决方案：开启 @EnableAspectJAutoProxy(exposeProxy = true)，通过 AopContext.currentProxy() 获取代理对象，用代理对象调用事务方法。

2. **问题**：事务传播机制中，REQUIRED 和 REQUIRES_NEW 的区别是什么？
   **答案**：REQUIRED：有事务则加入，无则新建，共用一个事务；REQUIRES_NEW：无论是否有事务，都新建独立事务，原事务暂停，新事务执行完毕后原事务继续。

3. **问题**：为什么 final 方法的事务会失效？
   **答案**：Spring 事务依赖代理对象重写目标方法，织入事务逻辑；final 方法无法被重写，代理对象无法织入事务逻辑，导致事务失效。

4. **问题**：异常被 catch 后，事务为什么不回滚？
   **答案**：Spring 事务回滚的前提是捕获到异常，若异常被手动 catch 且未重新抛出，Spring 无法捕获异常，无法触发回滚机制。

5. **问题**：readOnly = true 有什么作用？什么时候使用？
   **答案**：作用：标记事务为只读事务，Spring 会优化事务性能，避免不必要的事务操作（如禁止增删改）；使用场景：纯查询操作，无增删改逻辑。

### 高阶题（秒杀/高并发场景）

1. **问题**：高并发场景下，锁与事务的顺序为什么不能颠倒？
   **答案**：若先开启事务再加锁，锁会先释放，事务可能未提交，其他线程获取锁后会读取未提交的脏数据，导致一人多单、超卖；正确顺序是先加锁，再开启事务，确保事务提交后再释放锁。

2. **问题**：分布式场景下，Spring 本地事务为什么会失效？如何解决？
   **答案**：失效原因：分布式场景下，多个服务不在同一个数据库，本地事务无法跨服务生效；解决方案：使用分布式事务（如 Seata、TCC）。

3. **问题**：如何避免高并发场景下的事务超时？
   **答案**：1. 合理设置 timeout 参数，避免事务长时间占用连接；2. 优化业务逻辑，减少事务执行时间；3. 拆分大事务为小事务，降低执行耗时。

4. **问题**：Spring 事务隔离级别中，READ_COMMITTED 能解决什么问题？不能解决什么问题？
   **答案**：能解决脏读，不能解决不可重复读和幻读；MySQL InnoDB 引擎通过 MVCC 机制可避免幻读。

5. **问题**：多线程调用事务方法，事务为什么会失效？
   **答案**：多线程调用时，每个线程有独立的事务上下文，两个线程的事务无法共享，一个线程的事务提交/回滚不会影响另一个线程，导致事务失效。

### 拓展题（深度面试）

1. **问题**：Spring 事务的传播机制中，NESTED 和 REQUIRES_NEW 的区别是什么？
   **答案**：NESTED 是嵌套事务，子事务依赖父事务，父事务回滚子事务也回滚，子事务回滚不影响父事务；REQUIRES_NEW 是独立事务，与父事务无关，父事务回滚不影响新事务。

2. **问题**：如何手动控制 Spring 事务（编程式事务）？
   **答案**：通过 TransactionTemplate 或 PlatformTransactionManager 手动控制，如：使用 TransactionTemplate 的 execute 方法，在回调中执行业务逻辑，无需注解。

3. **问题**：Spring Boot 中，@Transactional 注解为什么不需要手动开启 AOP 代理？
   **答案**：Spring Boot 自动配置中，默认开启 AOP 代理（AutoConfiguration 中已集成 @EnableAspectJAutoProxy 相关配置），无需手动开启。

4. **问题**：MyISAM 引擎为什么不支持事务？
   **答案**：MyISAM 引擎是面向查询的引擎，不支持事务、行锁，设计初衷是追求查询性能，不具备事务的 ACID 特性；InnoDB 引擎支持事务和行锁，适合业务场景。

5. **问题**：如何排查 Spring 事务失效问题？
   **答案**：1. 检查方法是否为 public；2. 检查目标类是否被 Spring 管理；3. 检查是否通过代理对象调用；4. 检查异常是否被 catch 或类型是否匹配；5. 检查数据库引擎是否支持事务；6. 检查事务配置（传播级别、rollbackFor 等）是否正确。

---

## 适合人群

- Java 开发工程师（日常开发查阅）

- 面试备战者（重点掌握原理、失效场景、面试题）

- 秒杀/订单/支付业务开发者（重点掌握锁与事务顺序）

- 想彻底弄懂 Spring 事务原理的开发者

**本文永久保存，遇到事务问题随时查阅！**


