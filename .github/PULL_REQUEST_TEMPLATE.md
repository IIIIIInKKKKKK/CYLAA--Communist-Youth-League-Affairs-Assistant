## 变更说明

<!-- 这个 PR 改了什么，为什么需要 -->

## 检查清单

- [ ] `node --check content.js` 通过
- [ ] `manifest.json` 版本为 `1.0.0`，权限仅 `storage` + `https://zhtj.youth.cn/*`
- [ ] `content_scripts` 只加载 `content.js`
- [ ] 包内没有 `update.js`、`version.json`、GitHub/Gitee/CDN 等外部引用
- [ ] 面板文案、商店描述、`docs/index.html` 三处行为描述一致
- [ ] 未提交 `dist/`、真实团员数据、账号密码或令牌
- [ ] 行为变化已更新 `CHANGELOG.md`

## 商店影响

<!-- 是否需要重新打包、提交审核、更新截图 -->
