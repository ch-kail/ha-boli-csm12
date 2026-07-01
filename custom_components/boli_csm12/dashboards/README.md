## 📊 Prebuilt Dashboard Setup

This repository includes a fully designed energy monitoring dashboard with modern UI, covering all electrical parameters and trend analysis. You can import it via the raw configuration editor.

### Prerequisites
- The **Boli CSM12 Energy Meter** integration is installed and all sensors are working properly.
- **Mushroom Cards** is installed via HACS (Frontend category).
  > If not installed: HACS → Frontend → Search `Mushroom` → Install → Reload frontend.

### Import Steps (Raw Configuration Editor)
1. **Create a new blank dashboard**
   Go to your Home Assistant Overview page:
   - Click the ⋮ menu in the top right → **Edit Dashboard**
   - Click the ⋮ menu again → **New Dashboard**
   - Enter a title (e.g. `Energy Monitor`) and save.

2. **Open raw configuration editor**
   While in edit mode of the new dashboard:
   - Click the ⋮ menu in the top right → Select **Raw configuration editor**

3. **Paste the dashboard YAML**
   - Press `Ctrl+A` / `Cmd+A` to select all default content, then delete it completely.
   - Open [`dashboards/smart-meter-dashboard.yaml`](dashboards/smart-meter-dashboard.yaml) from this repository, copy all content.
   - Paste the full YAML into the editor.

4. **Replace entity prefix (required)**
   Use the editor's find-and-replace function to replace the placeholder `energy_meter` with your actual device entity prefix.
   - How to find the prefix: Go to **Developer Tools → States**, search for your meter entities. For `sensor.xxx_voltage`, `xxx` is the prefix.
   - Example: If your entity is `sensor.ke_ting_slave_21_voltage`, replace `energy_meter` with `ke_ting_slave_21`.

5. **Save and apply**
   Click **Save** in the top right. The page will refresh automatically and the dashboard will take effect.

### Multi-Meter Usage
- This is a single-meter template. For multiple meters, repeat the steps above to create separate dashboard pages.
- Replace the entity prefix in each dashboard with the corresponding slave address prefix.

### FAQ
- **Cards show red error**: Make sure Mushroom Cards is installed and you have reloaded the frontend.
- **Entities show "unavailable"**: Verify the entity prefix is correct and the device is online.
- **Statistics graph is empty**: Daily statistics require at least 24 hours of historical data.

---

## 📊 预置仪表盘导入指南

本仓库提供一套完整设计的电能表监控仪表盘，采用现代UI风格，覆盖全电量参数与趋势分析，可通过原始配置编辑器快速导入使用。

### 前置条件
- 已安装 **Boli CSM12 电能表** 集成，且所有传感器正常上报数据。
- 已通过 HACS 安装前端依赖 **Mushroom Cards**（前端分类）。
  > 未安装请前往：HACS → 前端 → 搜索 `Mushroom` → 安装 → 重载前端。

### 导入步骤（原始配置编辑器方式）
1. **新建空白仪表盘**
   进入 Home Assistant 概览页面：
   - 点击右上角 ⋮ 菜单 → **编辑仪表盘**
   - 再次点击右上角 ⋮ 菜单 → **新建仪表盘**
   - 输入标题（例如「电能监控」）并保存。

2. **打开原始配置编辑器**
   在新仪表盘的编辑状态下：
   - 点击右上角 ⋮ 菜单 → 选择 **原始配置编辑器**。

3. **粘贴仪表盘配置**
   - 按 `Ctrl+A` / `Cmd+A` 全选编辑器内默认内容并全部删除。
   - 打开本仓库内的 [`dashboards/smart-meter-dashboard.yaml`](dashboards/smart-meter-dashboard.yaml) 文件，复制全部内容。
   - 将完整 YAML 内容粘贴到编辑器中。

4. **替换实体前缀（必填）**
   使用编辑器的查找替换功能，将配置中的占位符 `energy_meter` 全局替换为你的设备实体前缀。
   - 前缀查看方式：进入 **开发者工具 → 状态**，搜索电能表实体，例如 `sensor.xxx_voltage`，则 `xxx` 即为设备前缀。
   - 示例：若实体为 `sensor.ke_ting_slave_21_voltage`，则将 `energy_meter` 替换为 `ke_ting_slave_21`。

5. **保存生效**
   点击右上角 **保存**，页面自动刷新后仪表盘即可正常显示。

### 多设备扩展
- 本模板为单设备模板，若有多台电能表，可重复上述步骤，新建多个仪表盘页面。
- 每个仪表盘分别替换为对应从站地址的实体前缀即可。

### 常见问题
- **卡片显示红色错误**：请确认 Mushroom Cards 已正确安装，并已重载前端。
- **实体显示不可用**：请检查实体前缀替换是否正确，设备是否在线。
- **统计图表无数据**：日统计数据需要设备运行至少24小时后才会生成。
