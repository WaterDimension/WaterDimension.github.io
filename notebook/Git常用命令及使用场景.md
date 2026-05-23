#  Git常用命令及使用场景

# 一.本地

1.git branch a 创建分支

  git checkout/switch a切换分支

## 2.git switch a; git merge main 先切换到分支，后合并主分支

## 3.git rebase main 让bugfix续在main后面，看起来像由main开发而来。

![img](https://i-blog.csdnimg.cn/direct/2a8f31c262b7456aa2b0d327bcafc475.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

## 4.分支上移动：

想看 HEAD 指向，可以通过 cat .git/HEAD 查看

- 分离head，让head指针从指向main到指向一个提交c1（c1是hash值，能代表）

![img](https://i-blog.csdnimg.cn/direct/2f0797fbf35543778e1c5f2cacec12a5.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/3bb83fd311984abe907e71d877c658be.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

- ###   相对引用

- 使用 ^ 向上移动 1 个提交记录
- 使用 ~<num> 向上移动多个提交记录，如 ~3
- 得先把head分离出来



![img](https://i-blog.csdnimg.cn/direct/93eb2c5402c24f64b4a7757c7b0d9683.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



~<num> 一次后退四步。Git checkout HEAD~4



### Git branch -f main c6 强制移动main(一般不用）



## 5.撤销变更



### 要有两种方法用来撤销变更 —— 一是 git reset，还有就是 git revert





![img](https://i-blog.csdnimg.cn/direct/2cd56426a55e4f7d8763fc4224da75d9.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

虽然在你的本地分支中使用 git reset 很方便，但是这种“改写历史”的方法对大家一起使用的远程分支是无效的哦！





![img](https://i-blog.csdnimg.cn/direct/34d816bdb73b49878338ca416d5603af.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

### git reset HEAD^ 核心含义

git reset HEAD^ 是 Git 中**撤销最近一次提交**的核心命令，通俗说就是：**把当前分支的指针回退到「上一个提交」，同时保留工作区的修改**。





1. ## Cherry-pick

本系列的第一个命令是 git cherry-pick, 命令形式为:

- git cherry-pick <提交1> <提交2> <...>

这是一种非常直接的方式，用来表达你想将一些提交复制到当前所在的位置（HEAD）下面。我个人非常喜欢 cherry-pick，因为它几乎没什么魔法成分，而且很容易理解。



![img](https://i-blog.csdnimg.cn/direct/f8fe7291c0f24e76ad36a197f4ac6c5a.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/487a43c276f542b2bfb368e4b34f375d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



1. ## 交互式变基

**Git 交互式变基**

当你知道你所需要的提交记录（**并且**还知道这些提交记录的哈希值）时, 用 cherry-pick 再好不过了 —— 没有比这更简单的方式了。

但是如果你不清楚你想要的提交记录的哈希值呢? 幸运的是，Git 也有办法应对这种情况！我们可以使用交互式变基来解决这个问题 —— 这是审查你即将变基的一系列提交的最佳方式。



![img](https://i-blog.csdnimg.cn/direct/8f570b45c34b4b07b8424bba1aec3f95.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/5898666eb56140bdac149c9d5baaa10f.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

git rebase -i HEAD~4





1. ## **本地栈式提交**



![img](https://i-blog.csdnimg.cn/direct/f34cc142e84b4b25a59b1e21af41230c.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/297edad77d1a4f62b1bec060ab3dfd33.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/3f1dec64d0ee4c20a4184c4fe8b6b47e.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



git rebase -i HEAD~3/git cherry-pick bugFix

git branch -f master bugFix     //强制移动



1. ## **提交的技巧**



![img](https://i-blog.csdnimg.cn/direct/f6cd94f6c655488196f913f558c6c451.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/5305808fc9a84c0f8308efd9e359d648.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





**我们可以使用** **rebase -i** **对提交记录进行重新排序。只要把我们想要的提交记录挪到最前端，我们就可以很轻松的用** **--**

 

**amend** **修改它，然后把它们重新排成我们想要的顺序。**

![img](https://i-blog.csdnimg.cn/direct/e76561f0132f4cffab61f7f401eba183.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



1. ### **分支很容易被认为改动，但是有了新的提交时，它也会移动。** **有了****tags****固定标记**

![img](https://i-blog.csdnimg.cn/direct/123b52b3ca1f47e392e3465c42f9a375.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

按照目标建立两个标签，然后切换到 v1 上面，要注意你会进到分离 HEAD 的状态 —— 这是因为不能直接在v1 上面做

commit。





1. ## Git describle



![img](https://i-blog.csdnimg.cn/direct/9d1702d3bb164c9482eac830490b73af.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/f16e72e7ba0e4743864a9dd3d72e630f.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/d096aaf45c1c4eab8dea1a4c9b7f5144.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





## **两个****parent****节点：**

![img](https://i-blog.csdnimg.cn/direct/516ebbedf8c24ec798bc5a982185c3a5.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/f9e7ac2ba716438cb397a1d7ffee9a73.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/077c8f7c0cac49e1b1b48cb51f84ddeb.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/27488e2e36cc462d815a4859da0295d0.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

**先向上一个****~1****，** **再向非垂直** **父节点****c5 ^2****，** **最后向上****2 ~2****。**





# **二.远程**

## 1.拷贝远程仓库



![img](https://i-blog.csdnimg.cn/direct/3de62e98e17f4f4bb6987c83bfbff4a5.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





![img](https://i-blog.csdnimg.cn/direct/af5353a902944530b4ff77ee98a1635d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





## 2.远程分支

![img](https://i-blog.csdnimg.cn/direct/425bd1f231614b18a1172b27930a3be4.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/3e8e9756fc8f46278c821b782f7c545c.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/1407dde43a824bedbc041405126d2fe4.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/8f877426731a4a5d85a86fdab198f6b8.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



## 3.Git fetch获取远程的数据



![img](https://i-blog.csdnimg.cn/direct/810a8f4a3f2a40249f64bb9c67e0e454.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/8905097da5ab4a5db91696e989e97da0.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/97059fffec8a4004bbe29e85004e78b1.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

git fetch 完成了仅有的但是很重要的两步:

- 从远程仓库下载本地仓库中缺失的提交记录
- 更新远程分支指针（如 o/main）

### git fetch 实际上将本地仓库中的远程分支更新成了远程仓库相应分支最新的状态。



### fetch不会做的事

![img](https://i-blog.csdnimg.cn/direct/1ddb04157a184b96ba495b56cdb4f3ff.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





## 4.Git pull



![img](https://i-blog.csdnimg.cn/direct/af2bd12b98b1491ab6f682f862abe8d1.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/0132d574b9524c4e9916105d2dc7298b.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/386cd3b74c864f60b7e3c38d4ed41122.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/158c453d5cc54103b8f81d2a40538091.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

- ### ✅ **你的 c2 提交会被完整保留**，不会丢失；

- ### ✅ 远程的新提交 c3 也会被拉到本地，并和你的 c2 合并。



1. ## 模拟团队合作



![img](https://i-blog.csdnimg.cn/direct/aad3ebd30e99420c88170c2607f0f1ef.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/f74dc140143c4d99bae231b34f11c457.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



1. ## Git push



![img](https://i-blog.csdnimg.cn/direct/8e7689958d124582bbcec95c41f70ff3.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/4dfbd15913b74f069e42a29d6abdf50b.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/1d518a4d4ae94ed7b20ad8192cec290d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





1. ## 偏离的工作

![img](https://i-blog.csdnimg.cn/direct/97085438622a4037a799e9bc63dd6c4b.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/f8bd30ef10e0443aafec290537df7af6.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/b7b4a6f1496d49fc87623bf8109312a5.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

那该如何解决这个问题呢？很简单，你需要做的就是使你的工作基于最新的远程分支。

有许多方法做到这一点呢，不过最直接的方法就是通过 rebase 调整你的工作。





![img](https://i-blog.csdnimg.cn/direct/866d296ff3dd4ca9bf490ebfb2f9990d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/bd98959deb924279b99d1f2e247441c3.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/c9b851c4ac04434098dee3439bf44ffc.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/c5ff3b5e83db4a31bd035dc70300f638.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



## Git pull --rebase

![img](https://i-blog.csdnimg.cn/direct/2d8f6ad9c7a741eab2c3609d23368337.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/0682664ae3a748519b8ec2562b5447a8.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑





## 8.远程服务器拒绝（Remote Rejected) = 怎么提PR?



![img](https://i-blog.csdnimg.cn/direct/f47f935ac0f542499facaa781cd4c15a.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/65606361587149e4a17b1b25886476d5.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/141134cf9507424eb6404bbe94ba5144.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

## 思考

### 1. 为什么会被拒绝？

- 你们团队的 **main** **分支是被保护 / 锁定的**，不允许任何人直接 git push 代码上去。
- 必须走 **Pull Request (PR)** 流程：先在自己的分支开发，再提交 PR 给团队 review，通过后才能合并到 main。
- 你现在的操作是：直接在本地 main 上写代码、提交（commit），然后想 git push 到远程 main → 服务器直接拒绝，报这个错。

### 2. 现在的困境

- 你的本地 main 已经有了新提交，但远程 main 不让你直接推。
- 如果不处理，下次你 git pull 拉别人代码并合并时，会和你本地的提交产生冲突，更麻烦。



### 3. 解决办法（一步步来）

假设你本地 main 上有了新提交，现在要把它 “搬” 到新分支，再恢复 main 干净：

#### 步骤 1：基于当前本地 main 新建一个功能分支

\# 新建并切换到 feature 分支（名字随便起，比如 feature/login）
 git checkout -b feature  （main）

这一步的作用：把你在 main 上写的代码，完整 “复制” 到这个新分支里。

#### 步骤 2：把这个新分支推送到远程



git push origin feature 推送到远程仓库origin

现在你的代码安全地存在远程的 feature/your-feature 分支了，可以去平台（GitHub/GitLab/Azure DevOps）提 PR 了。

#### 步骤 3：把本地 main 恢复成和远程一样（清空你的本地提交）



\# 先切回 main 分支
 git checkout main

\# 把本地 main 强制重置到和远程 main 一模一样
 git reset --hard origin/main

这一步会**删除你本地 main 上的所有新提交**，让它和远程 main 完全同步，避免以后冲突。



#### 4. 之后怎么提交代码？

以后永远记住这个流程：

1. 从最新的 main 切出功能分支：git checkout -b feature/xxx
2. 在这个分支上开发、提交
3. 推送到远程：git push origin feature/xxx
4. 去平台提 Pull Request，等 review 通过后合并到 main
5. 永远**不要直接在本地** **main** **上写代码、提交**





## 合并 特性分支



![img](https://i-blog.csdnimg.cn/direct/5a61ae111db045a8839d67d04b706ed4.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/f1f3872b63fa4c86b578e0310e79e96c.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

git pull --rebase 是 git pull 的进阶用法，先拆解基础逻辑：

- 普通 git pull = git fetch（拉取远程最新代码） + git merge（合并到本地分支）
- git pull --rebase = git fetch（拉取远程最新代码） + git rebase（变基到远程最新提交）



### ❌ 避坑提醒

- **不要在公共分支（如 main）用** **git pull --rebase**：公共分支的提交是团队共享的，变基会改写历史，导致其他人代码冲突。
- **变基时的冲突要逐个解决**：如果你的多个提交都和远程代码冲突，Git 会逐个暂停，需要解决一个、git add、git rebase --continue，直到全部解决。
- **变基前确保本地代码已提交**：如果有未提交的修改，先 git commit 或 git stash（暂存），否则变基会失败。



### ✅ 公共分支的正确做法

对 main 这类公共分支，永远用**普通** **git pull****（merge 方式）**：



git checkout main
 **git pull origin main = git fetch + git merge****，不会改写历史**

执行后你的本地历史会变成：

C1 → C2 → C3 → C4 → C6（合并节点）
      ↘ C5 ↗

- 虽然多了一个 “合并提交 C6”，但**保留了所有原始提交的哈希**，团队所有人的历史都是 “可追溯、可对齐” 的，不会出现冲突爆炸。



### 🌰 举个团队协作的反面例子

假设你和同事 **小明** 都基于远程 main 的 C3 提交开发：

初始状态（所有人一致）

远程 origin/main：C1 → C2 → C3

你的本地 main：C1 → C2 → C3

小明的本地 main：C1 → C2 → C3

步骤 1：小明先推了新代码到远程

小明在本地 main 提交 C4，并推送到远程：

远程 origin/main：C1 → C2 → C3 → C4

小明的本地 main：C1 → C2 → C3 → C4

步骤 2：你在本地 main 做了提交 C5（没同步远程）

你的本地 main：C1 → C2 → C3 → C5（此时你的本地落后远程）

步骤 3：你错误地执行 git pull --rebase origin main

这一步会触发两个操作：

1. git fetch：拉取远程最新的 C4，本地 origin/main 变成 C1→C2→C3→C4。
2. git rebase：把你的 C5 从 C3 后面 “剪下来”，贴到 C4 后面，生成**新的提交** **C5'**（哈希和原来的 C5 完全不同）。

此时你的本地 main 历史变成：C1 → C2 → C3 → C4 → C5'

步骤 4：你把改写后的历史推到远程（git push）

远程 origin/main 被你改成：C1 → C2 → C3 → C4 → C5'

步骤 5：小明遭殃了（冲突爆发）

小明此时想同步远程代码，执行 git pull：

- 小明的本地历史是 C1→C2→C3→C4，远程历史是 C1→C2→C3→C4→C5'。
- 但问题是：你的 C5' 是 “改写后的提交”，Git 认为小明的本地历史和远程历史**完全分叉**（因为 C5' 替换了原本可能的合并逻辑）。
- 更糟的是，如果小明也在 C4 后面做了新提交 C6，执行 git pull 会直接出现大量冲突，甚至需要手动对比哈希、合并代码，团队协作直接乱套。







## **合并远程仓库**

![img](https://i-blog.csdnimg.cn/direct/32589e8b5f6e4464bf889edc04180ff3.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑



![img](https://i-blog.csdnimg.cn/direct/a771ba6145184dffb0add5b9cd25aff1.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑