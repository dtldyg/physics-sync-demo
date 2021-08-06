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

## TODO
0. 扩展ecs，整理那些硬取comp的系统，尝试改为关闭comp

## 预测和插值
|-      |主控（预测）|主控（内插）|主控（无）|副本（内插）|副本（航位）|副本（物理-内插）|副本（物理-外插）|副本（物理-碰撞）|副本（无）|
|----   |----      |----      |----    |----      |----     |----          |----          |----          |----    |
|外插值  |-         |-         |-       |-         |√         |√            |√             |√             |-       |
|内插值  |-         |√         |-       |√         |√         |-            |√             |√             |-       |
|物理   |√          |-        |-        |-        |-         |-             |-             |√             |-       |
|回滚   |√          |-        |-        |-        |-         |-             |-             |-             |-       |
|渲染插值|√          |√        |-        |√        |√         |√             |√             |√             |-       |

## 很重要但不做的
- 状态指令冲突

## 计划
客户端:pygame * n - 服务器:python
1. 单机：球，摩擦力，质量，力，wasd控制 【完成】
2. 多样化控制，GUI 【完成】
3. 客户端操作上传服务器，物理模拟移交服务器，服务器下发状态 【完成】
4. 客户端物理预测，预测失败回滚重放 【完成】
5. 客机接入，内插值 【完成】
6. 完善服务器物理模拟 【完成】
7. 服务端输入缓冲，客户端可变帧率 【完成】
8. 外插值+物理混合+副本状态缓冲 【物理混合】

## 备忘
1. 协议浮点精度问题
2. 客户端时间缩胀时的客/服时钟同步

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
  - system_reset 系统_重置触发标志
  - system_package_dispatch 系统_消息分发
  - system_entity_manager 系统_实体管理
  - system_recv_state 系统_接收状态
  - system_game_event 系统_游戏事件
  - system_control 系统_控制
  - system_sync_cmd 系统_同步指令
  - system_extrapolation 系统_外插
  - system_interpolation 系统_内插
  - system_physics 系统_物理
  - system_simulate_blend 系统_模拟混合
  - system_rollback 系统_回滚
  - system_render_logic 系统_渲染逻辑
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

### 副本位置修正相关
- extrapolation: server -> target（20fps）（根据最后一个服务器的'过时'位置，推算主控时间下的位置）
  - 外插值 | 物理混合&AOI内：target > server
  - 其他：target = server
  - tips：碰撞发生后，target的推算是错误且大偏差的
- interpolation: real + target -> real（60fps）（平滑网络离散状态，本质是real追赶target）
  - 无：real = target
  - 其他：real < target
  - tips：物理混合期间，不工作，平滑工作交给物理+混合系统
- physics: real -> real（对当前位置的驱动、碰撞检测、修正。注意，永远从当前位置开始，这才符合'看见的真实'）
  - 物理混合 & 碰撞|混合中：real > real
  - 其他：real = real
- simulate: real + target -> real（将物理修正的位置，和外推的位置，）
  - 物理混合 & 混合中：real > real
  - 其他：real = real
  - tips：整个副本运动分两种：物理和追随，都是基于当前位置进行推进的，而且不处于碰撞或混合时，物理等于只走个碰撞检测过场
  - tips：混合时，先根据当前位置物理模拟，然后等于有个外力（target）再对它进行修正
  - tips：混合时间：系数1的时间要大于等于（外插时间+状态间隔）：这么多时间之后，server端碰撞之后的状态一定会到来，之后逐渐衰减
- render: real -> render（120fps）（平滑逻辑离散状态）
  - 无：render = real
  - 其他：render < real
