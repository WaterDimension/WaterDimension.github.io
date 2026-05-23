这是一份**超级实用、你以后写项目直接照搬的 AOP 指南**，专门解决：
**不知道什么时候用 AOP、不知道怎么写、不知道和业务怎么关联** 的问题。

我会用**最简单、最实战、最贴近你现在写的秒杀项目**来讲。

# 一、先记住一句话：
## **AOP = 与业务无关，但很多方法都要做的重复逻辑，抽出来统一做！**
只要你发现：
> 好多方法都要写一样的代码：日志、权限、校验、统计、事务、埋点…
> 那就是 **AOP 的场景**！

✔ 登录校验、Token 刷新 → 适合用 拦截器（Interceptor）
✔ 细粒度权限、角色控制、方法级控制 → 适合用 AOP
✔ 日志、限流、操作记录、监控 → 只能用 AOP

# 二、企业最常用 4 大 AOP 场景
我每个都给你：
**适用场景 → 为什么用AOP → 代码模板 → 怎么关联业务**

---

# 1）AOP 统一日志（最常用）
## 场景
所有接口都要打印：
- 请求参数
- 返回结果
- 方法执行时间
- 异常信息

## 为什么用 AOP？
每个接口写一遍日志会死人，重复代码爆炸。

## AOP 代码（直接复制可用）
```java
@Aspect
@Component
@Slf4j
public class LogAspect {

    // 切点：所有 controller 方法
    @Pointcut("execution(* com.hmdp.controller..*.*(..))")
    public void logPointcut() {}

    // 环绕通知：执行前后都能控制
    @Around("logPointcut()")
    public Object logAround(ProceedingJoinPoint joinPoint) throws Throwable {
        // 1. 方法执行前
        long start = System.currentTimeMillis();
        log.info("请求开始：{}，参数：{}", joinPoint.getSignature(), joinPoint.getArgs());

        // 2. 执行目标方法
        Object result = joinPoint.proceed();

        // 3. 方法执行后
        long time = System.currentTimeMillis() - start;
        log.info("请求结束：{}，耗时：{}ms，结果：{}", joinPoint.getSignature(), time, result);
        return result;
    }
}
```

## 你怎么关联业务？
你写任何 Controller 方法，**完全不用加任何东西**，AOP 自动帮你打日志。

---

# 2）AOP 统一权限校验
## 场景
- 只有管理员能访问某些接口
- 只有登录用户才能下单
- 接口必须带 token

## 为什么用 AOP？
不然每个方法都要写：
```java
if (!isAdmin()) return 403;
```

## AOP 代码（自定义注解 + AOP 最标准写法）
### ① 先自定义注解
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequireLogin {
}
```
ElementType.METHOD = 只能贴在方法上
ElementType.TYPE = 只能贴在类上
ElementType.FIELD = 只能贴在成员变量上
### ② AOP 切面
```java
@Aspect
@Component
@Slf4j
public class AuthAspect {

  // 切点：找到所有加了 @RequireLogin 的方法
  @Pointcut("@annotation(com.hmdp.annotation.RequireLogin)")
  public void authPointcut() {}

  // 环绕通知：方法执行前后拦截
  @Around("authPointcut()")
  public Object checkLogin(ProceedingJoinPoint joinPoint) throws Throwable {
      // 1. 检查是否登录
      UserDTO user = UserHolder.getUser();
      if (user == null) {
          throw new RuntimeException("请先登录");
      }
      // 2. 已登录 → 放行，执行原来的方法
      return joinPoint.proceed();
  }
}
```
当然，**权限校验**拦截器也能做，不过**AOP细粒度更高**能针**对接口做拦截**，而且操作空间也更高。

```c
public class LoginInterceptor implements HandlerInterceptor {
    //不是bean对象
    private StringRedisTemplate stringRedisTemplate;

    //利用有参构造
    public LoginInterceptor(StringRedisTemplate stringRedisTemplate) {
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        //1.判断是否需要拦截（Threadlocal中有用户）
        if (UserHolder.getUser() == null) {
            //设置状态码
            response.setStatus(401);
            //拦截
            return false;
        }
        //有用户，放行
        return true;
    }
```

### ③ 业务使用
```java
@PostMapping("/seckill/{id}")
@RequireLogin  // ✅ 只加一个注解，AOP 自动校验
public Result seckill(@PathVariable Long id) {
    // 你的业务代码
}
```

## 你看！业务代码完全干净！

---

# 3）AOP 统计接口耗时（监控）
## 场景
- 统计哪些接口慢
- 性能分析
- 接入监控平台

## AOP 代码
```java
@Aspect
@Component
@Slf4j
public class TimeAspect {

    @Pointcut("execution(* com.hmdp.controller..*.*(..))")
    public void timePointcut() {}

    @Around("timePointcut()")
    public Object timeAround(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long time = System.currentTimeMillis() - start;
        log.info("【耗时统计】{} 耗时：{}ms", joinPoint.getSignature().getName(), time);
        return result;
    }
}
```

---

# 4）AOP 全局异常处理（其实是@RestControllerAdvice通知 ，但思想 = AOP）

```java
@RestControllerAdvice
public class WebExceptionAdvice {
    @ExceptionHandler(RuntimeException.class)
    public Result handleRuntimeException(RuntimeException e) {
        log.error(e.getMessage(), e);
        return Result.fail("服务器异常");
    }
}
```

## 思想完全是 AOP：
**对所有方法抛出异常，统一拦截处理！**

---

# 三、你最困惑的点：
## **我怎么知道什么时候该用 AOP？**

我给你一个**万能判断口诀**（背下来，你以后永远不会错）：

### ✔ 出现以下任意一句话 → 立刻用 AOP
1. **好多方法都要做同一件事**
2. **这件事和业务逻辑无关**
3. **我不想在业务代码里写这些乱七八糟的东西**

满足 → **AOP！**

---

# 四、秒杀项目里哪些地方可以用 AOP？（实战对应）

1. **秒杀接口必须登录**
   → **@RequireLogin + AOP**

2. **所有接口统一日志**
   → **LogAspect**

3. **接口耗时统计**
   → **TimeAspect**

4. **全局异常**
   → **WebExceptionAdvice**

5. **接口防刷、限流**
   → **AOP**

6. **操作日志（谁下单了）**
   → **AOP**



---

# 1️⃣ 秒杀接口必须登录 → **@RequireLogin + AOP**
## ① 新建注解
```java
import java.lang.annotation.*;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequireLogin {
}
```

## ② AOP 切面
```java
import com.hmdp.exception.BusinessException;
import com.hmdp.utils.UserHolder;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LoginAspect {

    @Pointcut("@annotation(com.hmdp.annotation.RequireLogin)")
    public void loginPointcut() {}

    @Around("loginPointcut()")
    public Object checkLogin(ProceedingJoinPoint pjp) throws Throwable {
        if (UserHolder.getUser() == null) {
            throw new BusinessException("请先登录");
        }
        return pjp.proceed();
    }
}
```

## ③ 使用（秒杀接口上加）
```java
@PostMapping("/seckill/{id}")
@RequireLogin  // ✅ 加这个即可
public Result seckill(@PathVariable Long id) {
    return voucherOrderService.seckillVoucher(id);
}
```

---

# 2️⃣ 所有接口统一日志 → **LogAspect**
```java
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Slf4j
@Aspect
@Component
public class LogAspect {

    @Pointcut("execution(* com.hmdp.controller..*.*(..))")
    public void logPointcut() {}

    @Around("logPointcut()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        log.info("请求方法：{}", pjp.getSignature());
        log.info("请求参数：{}", pjp.getArgs());
        long start = System.currentTimeMillis();
        Object result = pjp.proceed();
        log.info("返回结果：{}", result);
        log.info("耗时：{}ms", System.currentTimeMillis() - start);
        return result;
    }
}
```

---

# 3️⃣ 接口耗时统计 → **TimeAspect**
```java
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Slf4j
@Aspect
@Component
public class TimeAspect {

    @Pointcut("execution(* com.hmdp.controller..*.*(..))")
    public void timePointcut() {}

    @Around("timePointcut()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object proceed = pjp.proceed();
        long end = System.currentTimeMillis();
        log.info("[接口耗时] {} → {}ms", pjp.getSignature().getName(), end - start);
        return proceed;
    }
}
```

---

# 4️⃣ 全局异常 → **WebExceptionAdvice**
你项目里**已经有了**，我给你标准版：
```java
import com.hmdp.dto.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@Slf4j
@RestControllerAdvice
public class WebExceptionAdvice {

    @ExceptionHandler(RuntimeException.class)
    public Result runtimeException(RuntimeException e) {
        log.error("全局异常：", e);
        return Result.fail(e.getMessage());
    }
}
```

---

# 5️⃣ 接口防刷、限流 → **AOP**
## ① 注解
```java
import java.lang.annotation.*;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RateLimit {
    int limit() default 10;
}
```

## ② AOP
```java
import com.hmdp.exception.BusinessException;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import java.util.concurrent.TimeUnit;

@Aspect
@Component
public class RateLimitAspect {

    private final StringRedisTemplate redisTemplate;

    public RateLimitAspect(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Pointcut("@annotation(com.hmdp.annotation.RateLimit)")
    public void limitPointcut() {}

    @Around("limitPointcut()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        String key = "limit:" + UserHolder.getUser().getId();
        Long count = redisTemplate.opsForValue().increment(key);
        if (count == 1) {
            redisTemplate.expire(key, 1, TimeUnit.MINUTES);
        }
        if (count > 10) {
            throw new BusinessException("请求过于频繁，请稍后再试");
        }
        return pjp.proceed();
    }
}
```

## ③ 使用
```java
@RateLimit(limit = 10)
@PostMapping("/seckill/{id}")
public Result seckill(@PathVariable Long id) { ... }
```

---

# 6️⃣ 操作日志（谁下单了）→ **AOP**
## ① 注解
```java
import java.lang.annotation.*;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface OperateLog {
    String value();
}
```

## ② AOP
```java
import com.hmdp.utils.UserHolder;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Slf4j
@Aspect
@Component
public class OperateLogAspect {

    @Pointcut("@annotation(com.hmdp.annotation.OperateLog)")
    public void logPointcut() {}

    @AfterReturning("logPointcut()")
    public void after(JoinPoint joinPoint) {
        Long userId = UserHolder.getUser().getId();
        String method = joinPoint.getSignature().getName();
        log.info("【操作日志】用户{} 执行了{}", userId, method);
    }
}
```

## ③ 使用
```java
@OperateLog("用户秒杀下单")
@PostMapping("/seckill/{id}")
public Result seckill(...) { ... }
```

---

# 🎯 你现在彻底掌握 AOP 了！
我给你的全部是：
**企业真实用法 + 可直接复制 + 完全匹配你的秒杀项目**

你只要记住一句：
## **凡是重复、通用、非业务逻辑 → 全部 AOP！**

---


# 五、终极总结
## **AOP 就是：把重复、通用、非业务逻辑抽出去统一管理！**
## **业务代码只写业务，其他全部丢给 AOP！**

---

