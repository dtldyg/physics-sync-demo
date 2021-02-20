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
4. 客户端物理预测，预测失败回滚重放 【完成】
5. 客机接入，内插值
6. 完善服务器物理模拟（单机验证）
7. 输入缓冲，消息剔除
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

## ECS
### client
- world
  - entity_game 实体_游戏
  - entity_player_master 实体_主机玩家
  - entity_player_replica 实体_副本玩家
  - component_package 组件_消息
  - component_surface 组件_渲染面
  - component_gui 组件_界面
  - component_info 组件_全局信息
  - component_input 组件_输入
  - component_record 组件_回滚记录
  - component_package 组件_消息
  - component_control 组件_控制
  - component_physics 组件_物理
  - component_frame 组件_帧
  - component_transform 组件_移动
  - component_render 组件_渲染
  - system_package_dispatch 系统_消息分发
  - system_entity_manager 系统_实体管理
  - system_recv_state 系统_接收状态
  - system_game_event 系统_游戏事件
  - system_control 系统_控制
  - system_sync_cmd 系统_同步指令
  - system_physics 系统_物理
  - system_render_logic 系统_渲染逻辑
  - system_rollback 系统_回滚
  - system_render 系统_渲染

### server
- world
  - entity_game 实体_游戏
  - entity_player 实体_玩家
  - component_connection 组件_连接
  - component_package 组件_消息
  - component_physics 组件_操控
  - component_frame 组件_帧
  - component_transform 组件_移动
  - system_package_dispatch 系统_消息分发
  - system_entity_manager 系统_实体管理
  - system_recv_cmd 系统_接收指令
  - system_physics 系统_物理
  - system_sync_state 系统_同步状态
