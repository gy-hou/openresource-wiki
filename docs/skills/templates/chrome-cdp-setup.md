---
tags:
  - skill
  - Chrome
  - CDP
  - 自动化
  - 浏览器
---

# Chrome CDP 双实例调试架构

> 🛠️ Chrome 146+ 远程调试的完整解决方案，支持 Claude Code / Codex / OpenClaw

| 属性 | 信息 |
|------|------|
| 类型 | 浏览器自动化 |
| 适用工具 | Claude Code, Codex, OpenClaw |
| 平台 | macOS |
| 版本 | 2.0.0 |
| 依赖 | Chrome 146+ |

## 问题背景

Chrome 146 引入了一条硬安全规则：

> 当 `--user-data-dir` 指向默认 Chrome 目录时，`--remote-debugging-port` 会被拒绝。

这意味着你**不能**直接在日常 Chrome 上启用 CDP 调试。尝试会触发：

- 反复弹出 "Allow remote debugging?" 对话框
- `selected page has been closed` 错误
- `existing-session attach timed out` 错误

## 解决方案：双 Chrome 实例

| 实例 | 用途 | 数据目录 | 调试端口 |
|------|------|----------|----------|
| 日常 Chrome | 正常浏览 | 系统默认 | 无 |
| 自动化 Chrome | CDP 调试 | `~/.chrome-cdp/automation` | 19222 |

两个实例使用不同的 `user-data-dir`，可以同时运行。Cookie 从日常 Chrome 同步到自动化实例，macOS 的 Keychain 加密机制保证跨目录复制后 Cookie 仍可解密。

## 核心功能

- **一键启动** — `start-chrome-cdp.sh` 自动同步 Cookie + 启动调试 Chrome（幂等）
- **Cookie 同步** — 自动从日常 Chrome 复制登录态到自动化实例
- **Profile 隔离** — 自动化目录仅保留 Default profile，避免污染
- **多工具兼容** — 附带 Claude Code / Codex / OpenClaw 三套配置示例
- **完整排障指南** — 覆盖 Chrome 146 所有常见 CDP 坑点

## 安装

=== "Claude Code"

    ```bash
    # 方式 1：直接复制
    mkdir -p ~/.claude/skills
    cp -r chrome-cdp-setup ~/.claude/skills/

    # 方式 2：在 CLAUDE.md 中引用
    echo "Browser CDP: http://127.0.0.1:19222" >> CLAUDE.md
    ```

=== "OpenClaw"

    ```bash
    cp -r chrome-cdp-setup ~/.openclaw/workspace/skills/
    ```

=== "Codex"

    ```bash
    mkdir -p ~/.codex/skills
    cp -r chrome-cdp-setup ~/.codex/skills/
    ```

## 使用方法

```bash
# 1. 启动自动化 Chrome（自动同步 Cookie）
bash ~/.chrome-cdp/scripts/start-chrome-cdp.sh

# 2. AI 工具连接 CDP 端口
curl -s http://127.0.0.1:19222/json/version

# 3. 完成后关闭
bash ~/.chrome-cdp/scripts/stop-chrome-cdp.sh
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CDP_PORT` | `19222` | CDP 调试端口 |
| `CDP_DATADIR` | `~/.chrome-cdp/automation` | 自动化 Chrome 数据目录 |
| `CHROME_PROFILE` | 自动检测 | 源 Chrome Profile 名称 |

## 关键经验

1. Chrome 146+ **禁止在默认数据目录上开启远程调试** — 这是安全硬限制
2. **永远不要复制 `Local State`** — 会引入幽灵 Profile
3. **永远不要用 `existing-session` 传输** — 会反复触发授权弹窗
4. macOS 上 Cookie 加密密钥是 **per-app** 的，跨目录复制可正常解密
5. 启动第二个 Chrome 必须用 `open -na`，`open -a` 只会激活已有实例

!!! tip "最佳实践"
    - 每次开始自动化前先运行 `start-chrome-cdp.sh`（幂等，已运行则跳过）
    - Cookie 过期后重新运行 `sync-chrome-profile.sh` 刷新登录态
    - 操作完 tab 务必关闭，避免累积导致 `selected page has been closed`

!!! warning "注意"
    此 Skill 目前仅支持 macOS。Windows/Linux 的 Chrome 数据目录和加密机制不同，需要适配。

---

[:material-github: 查看完整 Skill 源码](https://github.com/gy-hou/openresource-wiki){ .md-button }
