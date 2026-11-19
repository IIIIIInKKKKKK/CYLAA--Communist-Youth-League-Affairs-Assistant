## 变更说明

<!-- 这个 PR 做了什么，为什么需要 -->

## 影响范围

- [ ] GitHub 发布版（`manifest.json` / `update.js` / `docs/`）
- [ ] Edge 商店版（`edge/` / `docs/edge/` / `build/manifest.edge.json`）
- [ ] 两者都影响
- [ ] 仅文档、构建或 CI

## 验证

- [ ] 本地运行 `python build/build.py --target all` 通过
- [ ] Edge 包不包含 `update.js` / `version.json`，也没有外部更新地址
- [ ] 版本线正确：Edge 改 `edge/VERSION`，GitHub 改 `manifest.json`
- [ ] 面板文案、商店描述、隐私页三处行为描述一致
- [ ] 未提交 `dist/`、真实团员数据、账号密码或令牌
- [ ] 涉及界面/行为变化时已更新 `CHANGELOG.md`

## 发布说明

<!-- 是否需要打 tag、更新 version.json、提交 Edge 商店审核 -->
