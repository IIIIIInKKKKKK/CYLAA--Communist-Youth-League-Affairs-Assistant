## 变更说明

<!-- 这个 PR 改了什么，为什么需要 -->

## 影响范围

- [ ] GitHub 发布版（`content.js` / `update.js` / `manifest.json` / `docs/`）
- [ ] 仅文档、CI 或发布配置

## 检查清单

- [ ] `node --check content.js` 与 `node --check update.js` 通过
- [ ] `manifest.json` 的 `content_scripts` 包含 `content.js` + `update.js`，权限仅 `storage` + `https://zhtj.youth.cn/*`
- [ ] 没有把 `edge` 分支的商店文件（`store-assets/`、Edge 版 `manifest.json`）合入本分支
- [ ] 版本号变更时同步更新 `version.json`
- [ ] 面板文案、README、隐私页三处行为描述一致
- [ ] 未提交 `dist/`、真实团员数据、账号密码或令牌
- [ ] 行为变化已更新 `CHANGELOG.md`

## 发布说明

<!-- 是否需要打 v* tag、更新 version.json -->
