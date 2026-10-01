# 泡泡玛特盲盒概率计算 / POP MART POP NOW Plugins

截图算概率，给出最佳盲盒选择。

Calculate box probabilities from screenshots and find the best blind-box selection.

开发者 / Developer: **5noopya**

| 版本 / Variant | 当前版本 / Version | 使用方式 / Interaction |
| --- | --- | --- |
| Chat版 / Chat | 0.2.13 | 无远程 MCP 依赖；通过对话收集偏好，宿主支持时使用本地交互表单 / No remote MCP dependency; conversational preferences and local forms where supported |
| Codex版 / Codex | 0.3.5 | 远程 MCP 选择表单；内置本地计算脚本作为备用 / Remote MCP preference form with a bundled local solver fallback |

## 使用说明 / How to use

### Chat版 / Chat variant

Popmart官网的POP NOW功能，线上抽盲盒，把一个完整组合的每个盲盒都Shake for hints得到排除选项，点击Box status, 截图并发给plugin. 若截图中没有涵盖所有盲盒，需要再截图页面下方的所有盲盒名称列表。plugin会自动计算每个盲盒编号对应每种款式的概率，并询问喜欢的款式，不想要的款式，和购买数量，给出最佳组合。

Use POP NOW on the official POP MART website to open blind boxes online. For every box in a complete set, use "Shake for hints" to reveal excluded styles. Click "Box status", take a screenshot, and send it to the plugin. If the screenshot does not cover all the blind boxes, also send a screenshot of the full list of blind-box style names at the bottom of the page. The plugin automatically calculates the probability of each style for every box number, then asks which styles you like, which styles you do not want, and how many boxes you want to buy, and recommends the best combination.

### Codex版 / Codex variant

Popmart官网的POP NOW功能，线上抽盲盒，把一个完整组合的每个盲盒都Shake for hints得到排除选项，点击Box status, 截图并发给plugin. 若截图中没有涵盖所有盲盒，需要再截图页面下方的所有盲盒名称列表。plugin会自动计算每个盲盒编号对应每种款式的概率，并让你选择喜欢的款式，不想要的款式，和购买数量，给出最佳组合。

Use POP NOW on the official POP MART website to open blind boxes online. For every box in a complete set, use "Shake for hints" to reveal excluded styles. Click "Box status", take a screenshot, and send it to the plugin. If the screenshot does not cover all the blind boxes, also send a screenshot of the full list of blind-box style names at the bottom of the page. The plugin automatically calculates the probability of each style for every box number, then lets you select the styles you like, the styles you do not want, and how many boxes you want to buy, and recommends the best combination.

默认直接输出中文结果，同一回复附上“如需英文，请回复「English」。”；回复 English 可切换后续输出语言。只上传截图即可启动，也可以明确要求只计算概率、只选择偏好，或按不要款的风险排序。

Results default to Chinese with a short inline notice. Reply English to switch subsequent responses. A screenshot alone starts the workflow; you can also request probabilities only, preferences only, or unwanted-style risk rankings.

## 安装 / Installation

### Codex 桌面端：Add marketplace（无需 CLI）

1. 打开 **Plugins → Add marketplace**。
2. 输入本仓库链接：
   ```text
   https://github.com/5noopya/pop-mart-pop-now-plugins
   ```
3. 确认添加，在该来源下选择 **泡泡玛特盲盒概率计算**（Codex版）或 **泡泡玛特盲盒概率计算（Chat版）**，点击安装。
4. 按提示完成需要的连接授权，开启新对话，选用已安装插件并上传截图。

Open **Plugins → Add marketplace** in Codex desktop, enter the repository URL above, add the source, and install the variant you want. Complete any connection prompts, then start a new chat with the plugin and upload your screenshot. No terminal commands are needed. Menu labels and availability can vary by client version.

### 完整 ZIP：Upload plugin archive

在 [最新 Release](https://github.com/5noopya/pop-mart-pop-now-plugins/releases/latest) 的 **Assets** 中下载以下完整安装文件：

- **Chat版**：`pop-mart-pop-now-chat-0.2.13.zip`
- **Codex版**：`pop-mart-pop-now-codex-0.3.5.zip`

在提供此入口的网页版或桌面客户端打开 **Plugins → Add → Upload plugin archive**，上传对应 ZIP，再按页面提示安装/启用。网页版建议选择 Chat版。上传的是每位用户自己的插件副本；客户端是否支持运行其中的脚本或表单仍取决于宿主环境。不要使用 GitHub 自动生成的 **Source code (zip)** 作为单个插件归档，它包含整个仓库和两个插件。

Download the complete Chat or Codex ZIP from the **Assets** section of the [latest release](https://github.com/5noopya/pop-mart-pop-now-plugins/releases/latest). In web or desktop clients that expose **Plugins → Add → Upload plugin archive**, upload the corresponding ZIP and follow the prompts. Prefer the Chat variant on the web. This imports a personal copy; script execution and form rendering still depend on the host. The GitHub-generated **Source code (zip)** contains the whole repository and is not a single-plugin archive.

## 运行条件 / Runtime requirements

- 精确计算脚本需要支持执行 Python 3.8+ 的环境，仅使用标准库。没有可用计算环境时，插件不能保证完成大规模精确计算。
- Chat版没有远程 MCP 配置，但交互 HTML 表单需要宿主支持；若不支持按钮，可文字提交喜欢款、不要款和购买数量。
- Codex版连接现有远程 MCP 服务。发布准备时，未登录的连接检查返回 401，需完成宿主提示的授权；其他账号的远程表单尚未验证。若服务无法连接，保留偏好并使用内置计算脚本和文字交互。
- 安装归档不等于部署服务器。工作区通过 GitHub 导入带 `mcp.json` 或 `.mcp.json` 的版本时，按当前官方规则会标记为仅桌面端。
- 概率基于整组常规款各一件、满足所有排除线索的排列等可能这一模型；未知隐藏款机制不计入，不保证抽中。截图和偏好仅用于分析，本插件不会代替你购买。

The exact bundled solver requires a Python 3.8+ execution environment and uses only the standard library. The Chat variant has no remote MCP configuration; HTML buttons require host support, otherwise submit preferences in text. The Codex variant uses an existing remote MCP service: an unauthenticated release-preparation check returned 401, and other users' authorized forms have not been verified. Complete the host's authorization prompts; when unavailable, use the bundled solver and text preferences. Installing an archive does not deploy the server. GitHub workspace imports containing MCP configuration are currently desktop-only. Probabilities assume one of each regular style with equally likely valid whole-set arrangements; unknown secret-style mechanisms are excluded. The plugin does not make purchases.

## 仓库内容 / Repository contents

```text
.agents/plugins/marketplace.json
plugins/
  pop-mart-blind-box-v027/  # Chat版 / Chat
  pop-mart-blind-box/       # Codex版 / Codex
README.md
LICENSE
```

## 许可 / License

[MIT](LICENSE). 此项目为独立工具，与 POP MART 无官方关联。 / This is an independent tool, not affiliated with POP MART.
