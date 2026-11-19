# Edge 商店发布线

本目录只维护 Microsoft Edge 加载项商店版。它与 GitHub 发布版是两条独立的发布线：版本号各自递增，产物互不引用，互不影响。

## 版本

- 商店版版本号写在 [`VERSION`](VERSION)，当前为 `1.0.0`。
- GitHub 版版本号在根目录 `manifest.json`，当前为 `0.3.6`。
- 两条线不要求同号；商店版更新时只递增 `VERSION`。

## 构建

```bash
python build/build.py --target edge
```

产物：`dist/CYLAA-edge-<version>.zip`。

构建脚本会强制检查，任何一项不过都不会出包：

- `manifest.json` 位于 zip 根目录；
- `permissions` 仅为 `["storage"]`，`host_permissions` 仅为 `https://zhtj.youth.cn/*`；
- 不包含 `update.js`、`version.json`；
- 包内不出现 `github`、`jsdelivr`、`gitee`、`releases`、`version.json` 等字样；
- 图标尺寸 16/32/48/128 与 manifest 一致；
- JS 通过 `node --check`。

## 与 GitHub 版的隔离规则

1. 商店包不包含 `update.js`，`content.js` 内的 `HAS_UPDATER` 被构建脚本改为 `false`，设置页不显示“检查更新”。
2. 商店包只保留 `storage` 与 `zhtj`；GitHub 版同样已移除更新源 host 权限，更新检查改走公开 CORS 接口（GitHub Pages 优先）。
3. 商店版隐私政策见 [`docs/edge/index.html`](../docs/edge/index.html)，只描述同源请求，不提第三方更新源。
4. 商店 listing 不链接代码仓库：Website 留空或使用独立法务页，Support 填邮箱/商店支持方式。
5. 商店版被拒或下架时，只改本目录与 Edge 构建，不触碰 GitHub 版。
6. GitHub 的 `version.json` 只服务于 GitHub 发布线，不要把商店版的 `1.0.0` 写进去，否则 GitHub 用户会被提示去下载一个不存在的版本。

## 商店 listing 要点

| 项目 | 内容 |
|---|---|
| Extension name | 取自 manifest：`团务助手 - 团员信息管理` |
| Short description | 取自 manifest：`智慧团建团务辅助：名单导出、验证码记录、评议批量设置与团员信息录入预检。` |
| Description | 取自 manifest（≥250 字符）；已写明批量任务需确认后自动提交 |
| Logo | `icons/icon128.png`（≥128×128，1:1） |
| Privacy policy URL | `https://jasper100-dev.github.io/CYLAA--Communist-Youth-League-Affairs-Assistant/docs/edge/` |
| Website / Support | 不填代码仓库；Support 用邮箱或商店支持方式 |

## 仍需人工完成

1. **截图**：现有截图来自旧版界面，必须用商店版重新截取（1280×800 或 640×480，最多 6 张）。
2. **商店素材**：logo 300×300（必填）、小宣传图 440×280、大宣传图 1400×560（可选）。
3. **隐私页托管**：当前隐私页仍放在代码仓库的 GitHub Pages 上。若希望彻底解耦，可把它迁到独立仓库或独立域名，然后只改 Partner Center 里的 URL；商店包本身不需要改动。
4. **Partner Center**：注册 Edge 开发者账号（免费、个人 MSA）、上传 zip、填写 Privacy 与 Store listings、写 Notes for certification。
5. **审核备注**：说明批量任务需用户确认、验证码记录仅本地、无法提供真实测试账号及原因。

## 已知风险（与构建无关）

- 批量录入/评议的“确认后自动逐人提交”仍可能被审核归入自动化操纵平台，需在描述与备注中如实说明由使用者主动确认并承担核对责任。
- “密码重置验证码记录”涉及非用户的身份验证信息，属于审核高风险功能；如被质疑，可只在 Edge 构建中关闭该功能，GitHub 版不受影响。
