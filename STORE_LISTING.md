# Edge 商店填写清单（v1.0.0）

> 复制到 Partner Center 对应字段。所有功能描述必须与商店包实际行为一致。

## Extension name

```
团务助手 - 团员信息管理
```

## Short description

```
智慧团建团务辅助：名单导出、验证码记录、评议批量设置与团员信息录入预检。
```

## Manifest description（实际文案在 `_locales/zh_CN/messages.json`，硬上限 132 字符）

`manifest.json` 使用占位符：

```
"description": "__MSG_extensionDescription__"
```

`_locales/zh_CN/messages.json` 中的实际文案：

```
团务助手：智慧团建团务辅助，支持名单读取与 CSV 导出、重置验证码记录、评议批量设置、团员信息录入预检；数据本地处理，批量任务确认后提交。
```

> 实际 70 字符。不要直接写长文案到 manifest，也不要超过 132 字符。

## Store listing Description（Partner Center 长描述，250–10000 字符）

> 下面这段填在 Partner Center → Store listings → Details for 中文（简体）→ **Description**，不是 manifest 的 `description` 字段。

```
团务助手是一款面向共青团基层团务工作人员的第三方辅助工具，用于在智慧团建平台（zhtj.youth.cn）上提升日常团务处理效率。主要功能：团员名单读取与 CSV 导出，便于数据核对与归档；密码重置验证码的本地记录与导出；教育评议等级批量设置辅助；团员信息批量填写辅助与录入前数据预检。所有功能由使用者在工具面板中主动启动，仅处理使用者本人有权访问的团务数据，不改变正式审批流程。批量任务需要使用者确认后才开始，确认后工具会自动填写表单字段并执行提交（批量录入点击页面「提交」按钮，评议选择等次后由页面即时保存），操作前请务必核对目标人员与字段内容。姓名、手机号、验证码等敏感数据仅在本机浏览器内处理和导出，不上传至开发者服务器。本工具与智慧团建官方平台无授权或隶属关系。使用者须遵守平台规范与个人信息保护相关法律法规。
```

## Store listing 语言

包已声明 `default_locale: "zh_CN"` 并提供 `_locales/zh_CN/messages.json`，重新上传后 Store listings 应出现 **中文（简体）** 行。

如果仍显示 **英语（美国）不完整**：

1. 确认上传的是包含 `_locales/zh_CN/messages.json` 的新 zip；
2. 等中文（简体）行出现后，点英语（美国）行的 **Remove**，只保留中文；
3. 不要为了消除“不完整”去填英文描述——那等于声明支持英文，反而引入本地化问题。

## Single purpose

```
为团务工作人员提供智慧团建平台团务数据的本地读取、核对与批量录入辅助，减少重复性手工操作。
```

## 权限理由

| 权限 | 理由 |
|---|---|
| `storage` | 仅在本地保存名单变更快照（姓名 + 手机号）、面板设置与更新时间，用于变更识别和恢复，不上传服务器。 |
| `https://zhtj.youth.cn/*` | 内容脚本只在该平台页面运行，需要读取页面表格与调用同源字典接口，必需。 |

商店版不申请任何其他 host 权限，也不发起外部网络请求。

## 远程代码

选 **No**。包内没有 `eval`、`new Function`、动态脚本注入或远程脚本加载。

## 数据用途勾选

- 个人身份信息（姓名）
- 电话号码（手机号）
- 身份验证信息（密码重置验证码）
- 网页内容（平台表格）

不勾选位置、财务、健康信息。

## 隐私政策 URL

```
https://jasper100-dev.github.io/CYLAA--Communist-Youth-League-Affairs-Assistant/docs/edge/
```

## Notes for certification

```
本扩展依赖智慧团建平台（zhtj.youth.cn）的真实账号与团务数据。涉及团员个人信息，出于个人信息保护要求无法提供公开测试账号与真实测试数据。

商店版（v1.0.0）说明：
1. 仅申请 storage 与 https://zhtj.youth.cn/*，不包含外部更新检查，不请求任何第三方地址；
2. 访问 https://zhtj.youth.cn 即可验证扩展加载与面板显示；
3. 批量录入/评议必须先由使用者在面板中点击确认，确认后才会逐人填写并提交；评议选择等次后由平台即时保存；
4. 姓名、手机号、验证码仅在本机处理和导出，不发送至开发者或第三方服务器；
5. 完整功能需由具有平台权限的团务工作人员在真实业务场景中测试。

审核如需进一步说明，请通过商店支持渠道联系。
```

## 素材

| 文件 | 规格 | 状态 |
|---|---|---|
| `icons/icon128.png` | 128×128，1:1 | 已在包内 |
| `store-assets/logo-300.png` | 300×300，1:1 | 已生成 |
| `store-assets/small-promotional-tile-440x280.png` | 440×280 | 已生成 |
| `store-assets/large-promotional-tile-1400x560.png` | 1400×560 | 已生成 |
| `store-assets/screenshots/01-roster.png` | 1280×800 | 已生成：名单 |
| `store-assets/screenshots/02-evaluation.png` | 1280×800 | 已生成：评议 |
| `store-assets/screenshots/03-member-info.png` | 1280×800 | 已生成：信息 |
| `store-assets/screenshots/04-import.png` | 1280×800 | 已生成：录入 |
| `store-assets/screenshots/05-codes.png` | 1280×800 | 已生成：取码 |
| `store-assets/screenshots/06-settings.png` | 1280×800 | 已生成：设置 |

截图已用 v1.0.0 真实界面制作，姓名、手机号尾号等已打码；共 6 张，顺序：名单 → 评议 → 信息 → 录入 → 取码 → 设置。面板底部文案与 v1.0.0 一致（“批量任务需确认后自动提交 · 请核对”）。

## 上架前检查

1. 发布包 `dist/CYLAA-edge-1.0.0.zip` 已生成，manifest 在 zip 根目录。
2. 权限仅 `storage` + `https://zhtj.youth.cn/*`，只加载 `content.js`。
3. 包内无 `update.js`、`version.json`、第三方更新地址。
4. 隐私页 URL 可访问，内容与商店版行为一致。
5. 商店描述、面板文案、隐私页三处关于“确认后自动提交”的表述一致。
6. 6 张截图已放入 `store-assets/screenshots/`，均为 1280×800，敏感信息已打码。
7. `manifest.json` 的 `description` 已压到 70 字符（≤132），长描述填在 Store listing 的 Description 字段。
