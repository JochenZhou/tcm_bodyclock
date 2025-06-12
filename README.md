# Home Assistant - 中医十二时辰养生表 (TCM Body Clock)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

这是一个为 Home Assistant 设计的中医养生表自定义组件，其灵感和部分代码实现得益于 AI 的辅助。它基于中医十二时辰养生理论，可以实时显示当前时辰、经络当令、养生要点、推荐及禁忌事项，帮助您顺应自然节律，科学调理身心。

---

## ✨ 功能特性

- **实时时辰显示**：根据当前时间，自动更新对应的中医时辰（如“子时”、“丑时”等）。
- **经络当令信息**：展示每个时辰所对应的主要经络（如“胆经当令”、“肝经当令”）。
- **个性化养生建议**：
    - **养生要点**：提供当前时辰的核心养生原则。
    - **推荐事项**：给出适合在该时辰进行的活动建议。
    - **注意事项**：提醒需要避免的行为，防止损害健康。
- **强大的自动化联动**：可作为触发器或条件，轻松创建个性化的健康提醒，例如定时喝水、起身活动或准备休息。

---

## ⚙️ 安装与配置

### 1. 安装

推荐使用 HACS (Home Assistant Community Store) 进行安装。

1.  进入 **HACS** > **集成** 页面。
2.  点击右上角的三个点，选择 **自定义存储库**。
3.  在弹出的对话框中：
    -   **存储库**: 粘贴 `JochenZhou/tcm_bodyclock`
    -   **类别**: 选择 `集成`
4.  点击 **添加**。
5.  在 HACS 集成页面中找到 "中医养生表"，点击 **安装**，并按照提示完成。
6.  **重启 Home Assistant**。

**手动安装**
1.  将 `tcm_bodyclock` 文件夹（位于 `custom_components` 目录下） 复制到您 Home Assistant 的 `<config>/custom_components/` 目录中。
2.  **重启 Home Assistant**。

### 2. 配置

此集成通过 Home Assistant 界面进行配置，无需编辑 `configuration.yaml` 文件。

1.  导航至 **设置** > **设备与服务** > **集成**。
2.  点击右下角的 **+ 添加集成**。
3.  搜索 **"中医养生表"** 并选择它。
4.  点击 **提交** 即可完成添加。

---

## 💡 使用指南

### 实体信息

安装配置完成后，系统会创建一个名为 `sensor.zhong_yi_yang_sheng_biao` 的传感器实体。
-   **状态 (State)**: 当前时辰的名称，例如 `未时`。
-   **属性 (Attributes)**:
    -   `经络值班`: 当前时辰的当令经络。
    -   `养生重点`: 当前时辰的核心养生建议。
    -   `推荐事项`: 建议进行的活动。
    -   `注意事项`: 应避免的行为。

> **注意**: 如果您修改了实体名称，请在下面的卡片和自动化代码中同步更新实体ID。

### 前端卡片示例

您可以在 Lovelace Dashboard 中使用以下卡片来美观地展示养生信息。

#### 简洁实体卡片

```yaml
type: entities
entities:
  - entity: sensor.zhong_yi_yang_sheng_biao
    name: 当前养生时辰
    icon: mdi:clock-outline
    secondary_info:
      attribute: 养生重点