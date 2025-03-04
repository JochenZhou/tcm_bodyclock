
---

# 中医养生表 - Home Assistant 自定义组件

这是一个借助**deepseek**为 Home Assistant 设计的中医养生表自定义组件。它基于中医十二时辰养生理论，实时显示当前时辰、经络值班、养生重点、推荐事项和注意事项，帮助用户更好地遵循自然规律，调理身体。

---

## 功能特性

- **实时时辰显示**：根据当前时间自动显示对应的中医时辰（如“子时”、“丑时”等）。
- **经络值班**：显示当前时辰对应的经络值班信息（如“胆经值班”、“肝经值班”等）。
- **养生重点**：提供每个时辰的养生重点（如“阳气初生宜安眠”、“藏血排毒黄金期”等）。
- **推荐事项**：列出当前时辰的推荐事项（如“关闭电子设备，准备入睡”、“每小时起身活动”等）。
- **注意事项**：提醒当前时辰的注意事项（如“熬夜加班、刷手机”、“空腹喝咖啡”等）。
- **自动化支持**：支持通过 Home Assistant 自动化实现定时提醒功能。

---

## 安装方法

### 通过 HACS 安装（推荐）
1. 打开 HACS 面板。
2. 点击 **集成**。
3. 点击右下角 **+ 浏览并添加存储库**。
4. 搜索 `tcm_bodyclock` 并添加。
5. 重启 Home Assistant。

### 手动安装
1. 将 `tcm_bodyclock` 文件夹复制到 `custom_components` 目录。
2. 重启 Home Assistant。
3. 进入 **配置 -> 设备与服务 -> 集成**。
4. 点击右下角 **+ 添加集成**。
5. 搜索 **中医养生表** 并添加。

---

## 配置

### 配置示例
在 `configuration.yaml` 中添加以下配置：

```yaml
tcm_bodyclock:
  name: 中医养生表
```

### 配置选项
- **name**（可选）：自定义传感器名称，默认为“中医养生表”。

---

## 使用说明

### 实体属性
添加集成后，会生成一个传感器实体 `sensor.zhong_yi_yang_sheng_biao`，其属性包括：
- **state**：当前时辰（如“子时”、“丑时”等）。
- **attributes**：
  - **经络值班**：当前时辰对应的经络值班信息。
  - **养生重点**：当前时辰的养生重点。
  - **推荐事项**：当前时辰的推荐事项。
  - **注意事项**：当前时辰的注意事项。

### 前端展示
在 Lovelace UI 中，可以使用 **实体卡片** 或 **Markdown 卡片** 展示信息。

#### 实体卡片
```yaml
type: entities
entities:
  - entity: sensor.zhong_yi_yang_sheng_biao
    name: 当前养生时辰
    secondary_info: attribute
    attribute: 养生重点
    icon: mdi:clock-chinese
```

#### Markdown 卡片
```yaml
type: markdown
content: >
  **当前时辰**: {{ states('sensor.zhong_yi_yang_sheng_biao') }}

  **经络值班**: {{ state_attr('sensor.zhong_yi_yang_sheng_biao', '经络值班') }}

  **养生重点**: {{ state_attr('sensor.zhong_yi_yang_sheng_biao', '养生重点') }}

  **推荐事项**: {{ state_attr('sensor.zhong_yi_yang_sheng_biao', '推荐事项') }}

  **注意事项**: {{ state_attr('sensor.zhong_yi_yang_sheng_biao', '注意事项') }}
```

### 自动化示例
以下是一个自动化示例，用于在“未时”提醒喝水：

```yaml
automation:
  - alias: "未时喝水提醒"
    trigger:
      - platform: time
        at: "13:30:00"
    condition:
      - condition: state
        entity_id: sensor.zhong_yi_yang_sheng_biao
        state: "未时"
    action:
      - service: tts.google_translate_say
        data:
          message: "未时小肠经当令，请及时补充200ml温水"
```

---

## 开发与贡献

### 依赖
- Home Assistant 2023.7 或更高版本。

### 代码结构
```
custom_components/
└── tcm_bodyclock/
    ├── __init__.py
    ├── manifest.json
    ├── config_flow.py
    ├── sensor.py
    └── const.py
```

### 贡献指南
欢迎提交 Issue 或 Pull Request！请在提交前确保代码通过测试并符合代码风格规范。

---

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

---

## 致谢

- 感谢中医养生理论的智慧。
- 感谢 Home Assistant 社区的支持。
- 感谢 deepseek的支持。

---


**祝您养生愉快，健康常伴！** 🌿# tcm_bodyclock
