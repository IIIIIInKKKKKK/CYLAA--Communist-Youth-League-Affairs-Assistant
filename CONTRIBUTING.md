# 贡献指南

感谢你关注并支持「团务助手 · 智慧团建」。

## 1. 分支模型

项目按发布通道拆成两个长期分支，文件互不混用：

| 分支 | 内容 | 版本 |
|---|---|---|
| `main` | GitHub 发布版：`content.js` + `update.js` + `manifest.json` + `docs/` | 0.3.x |
| `edge` | Microsoft Edge 商店版：仅 `content.js` + `manifest.json` + `docs/` + 商店素材 | 1.0.x |

- 功能/修复从目标分支拉 `feat/<主题>` 或 `fix/<主题>`，PR 合回目标分支。
- 不要直接把 `edge` 合进 `main`，也不要把 `main` 合进 `edge`；两边运行时文件按需分别修改。
- `main` 的 `docs/edge/` 只作为 Edge 商店隐私政策的公开托管地址，不属于 GitHub 版运行时代码。

## 2. 反馈问题

请通过 GitHub Issues 提交，并说明：

- 软件版本、浏览器名称及版本、操作系统。
- 问题发生的功能模块。
- 复现步骤、预期结果与实际结果。
- 必要的错误截图（请遮挡真实姓名、手机号、验证码等）。

请勿提交真实团员个人信息、账号密码或访问令牌。

## 3. 提交代码

1. 保持目标分支现有文件结构，不把另一版本的运行文件带进来。
2. 避免无关修改。
3. 不提交 `dist/`、真实团员数据、账号密码、令牌。
4. 行为变化同步更新 `CHANGELOG.md`，并保证面板文案、商店/README 描述、隐私页三处一致。

## 4. Pull Request

PR 请说明修改目的、影响范围（GitHub 版 / Edge 版）、验证方式和已知问题。

合并前至少确认：

- `main`：`node --check content.js update.js`，`manifest.json` 的 `content_scripts` 包含两个脚本，权限仅 `storage` + `zhtj`。
- `edge`：`node --check content.js`，`manifest.json` 版本 1.0.0、权限仅 `storage` + `zhtj`、只加载 `content.js`，包内没有外部更新引用。
- 本地能打出根目录含 `manifest.json` 的 zip。

## 5. 发布

- GitHub 版：在 `main` 推送 `v0.3.x` tag，`.github/workflows/release.yml` 自动打包并创建 Release。
- Edge 版：在 `edge` 推送 `edge-v1.0.x` tag 作为记录，手动打包并上传 Microsoft Edge 加载项商店。

## 6. 行为规范

参与项目讨论和协作时，请保持友善、尊重和理性。

不允许利用项目实施未经授权的数据访问、隐私泄露或其他违法违规行为。

## 7. 许可证

提交贡献即表示你同意相关贡献按照项目现有开源许可证进行管理。
