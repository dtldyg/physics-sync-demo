# physics-sync-demo

## 简介
最小物理同步demo，参考自GDC2017看门狗2分享

# 目标特性
- 状态同步（服务端碰撞）
- 主控预测
- 副本内插值平滑
- 副本状态缓冲
- 副本外插值预测
- 物理模拟混合

# 很重要但不做的
- 状态指令冲突

## 计划
客户端:pygame * 2 - 服务器:python/go？
1. 单机：PlayerEntity:圆，摩擦力，质量，wasd四个方向力 【完成】
2. 服务器实现，实现一个主控非预测状态同步模型 【完成】
3. 多样化控制，GUI 【完成】
4. 服务端碰撞检测，主控预测-回滚
5. 2P接入，外插值预测，内插值平滑
6. 物理同步

## 依赖关系

### 客户端

#### 模块依赖
```mermaid
graph TD
     main --> io
     main --> game

     game --> const
     game --> io
     game --> gui
     game --> window
     game --> event
     game --> entity
     game --> scene
     
     gui --> const
     gui --> switch
     gui --> window

     entity --> const
     entity --> ec
     entity --> comp_control
     entity --> comp_physics
     entity --> comp_state
     entity --> comp_render

     comp_control --> const
     comp_control --> math
     comp_control --> switch
     comp_control --> ec
     comp_control --> window
     comp_control --> event

     comp_physics --> const
     comp_physics --> math
     comp_physics --> ec

     comp_state --> const
     comp_state --> math
     comp_state --> ec
     comp_state --> io

     comp_render --> const
     comp_render --> math
     comp_render --> switch
     comp_render --> ec
     comp_render --> window
```
#### 组件依赖
```mermaid
graph TD
     comp_control --> comp_physics
     comp_control --> comp_state
     comp_control --> comp_render

     comp_physics --> comp_state

     comp_render --> comp_state
```

### 服务端

#### 模块依赖
```mermaid
graph TD
     main --> io
     main --> game

     game --> const
     game --> math
     game --> entity

     entity --> comp_physics
     entity --> comp_state

     comp_physics --> math
```
