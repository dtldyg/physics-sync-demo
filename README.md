# physics-sync-demo

## 简介
最小物理同步demo，参考自GDC2018火箭联盟分享

## 目标特性
- 状态同步（客户端上传操作，服务器物理模拟）
- 服务器缓冲（延迟会导致帧序与客户端不一致）
- 主控预测（预测失败回滚世界重放）
- 副本内插值+缓冲
- 副本外插值预测：Predict Everything
- 物理模拟混合

## 很重要但不做的
- 状态指令冲突

## 计划
客户端:pygame * n - 服务器:python
1. 单机：球，摩擦力，质量，力，wasd控制 【完成】
2. 多样化控制，GUI 【完成】
3. 客户端操作上传服务器，物理模拟移交服务器，服务器下发状态 【完成】
4. 客户端物理预测，预测失败回滚重放
5. 客机接入，内插值
6. 完善服务器物理模拟（单机验证）
7. 输入缓冲
8. 外插值+物理混合

## 帧率 & 采样率
- 客户端-服务器：相同逻辑帧：更新世界物理状态
- 客户端：渲染帧：插值渲染
- 采样率：客户端逻辑帧采样操作，上传；服务器低频采样状态，下发
- 渲染60：客户端渲染
- 逻辑30：客户端input、采样输入、output、逻辑，服务器input、逻辑
- 状态20：服务器采样状态、output

## 确定性
- c/s保证逻辑帧率一致
- s维护的c中记录帧号，c的帧号和s保持一致，做到任意时刻c/s处于同一帧号
- c的x帧延迟时，s将会用x-1帧输入作为x帧输入并计算，这导致s的x帧状态与c预测的x帧状态不一致，c回滚重放

## 依赖关系
### 客户端
#### 模块依赖
```mermaid
graph TD
     main --> io
     main --> game

     game --> const
     game --> scene
     game --> io
     game --> gui
     game --> window
     game --> event
     game --> entity
     
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

     entity --> ec
     entity --> comp_physics
     entity --> comp_state

     comp_physics --> ec

     comp_state --> ec
     comp_state --> math
```
#### 线程模型
```mermaid
graph TD
     client1.run_conn_recv --> recv_q
     client2.run_conn_recv --> recv_q

     recv_q --> game

     game --> client1.send_q
     game --> client2.send_q

     client1.send_q --> client1.run_conn_send
     client2.send_q --> client2.run_conn_send
```

## 通信消息
### client
#### sync
```json
{
  "p": {
    "x": 1.0,
    "y": 1.0
  },
  "v": {
    "x": 1.0,
    "y": 1.0
  }
}
```
### server
#### sync
```json
{
  "p": {
    "x": 1.0,
    "y": 1.0
  },
  "v": {
    "x": 1.0,
    "y": 1.0
  }
}
```
