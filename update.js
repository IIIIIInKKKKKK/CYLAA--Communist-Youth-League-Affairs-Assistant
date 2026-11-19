/* 团务助手 · 更新检查（仅 GitHub 版加载）
 *
 * Edge 商店构建不会打包本文件，也不会声明对应的 host 权限；
 * 因此商店版对 GitHub / Gitee / CDN 没有任何网络请求。
 *
 * 本文件只负责读取公开的 version.json，把结果交给 content.js 显示；
 * 面板的 DOM 由 content.js 持有，避免两处各自渲染。
 */
(() => {
  'use strict';
  if (window.__ZHTJ_UPDATER_LOADED__) return;
  window.__ZHTJ_UPDATER_LOADED__ = true;

  // 只在顶层页面自动检查，避免每个 iframe 都发请求；手动检查在各 frame 都可用。
  const IS_TOP = window.top === window.self;

  const UPDATE_REPO = 'Jasper100-dev/CYLAA--Communist-Youth-League-Affairs-Assistant';
  const [UPDATE_OWNER, UPDATE_NAME] = UPDATE_REPO.split('/');
  const UPDATE_SOURCES = [
    // GitHub Pages 国内可访问且带 CORS 头，作为首选
    `https://${UPDATE_OWNER}.github.io/${UPDATE_NAME}/version.json`,
    `https://cdn.jsdelivr.net/gh/${UPDATE_REPO}@main/version.json`,
    `https://raw.githubusercontent.com/${UPDATE_REPO}/main/version.json`,
  ];

  const esc = (s) =>
    String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const verNum = (v) => String(v || '').split('.').map((x) => parseInt(x, 10) || 0);
  function isNewer(a, b) {
    const A = verNum(a);
    const B = verNum(b);
    for (let i = 0; i < 3; i++) {
      const x = A[i] || 0;
      const y = B[i] || 0;
      if (x !== y) return x > y;
    }
    return false;
  }

  let current = null;

  function getHost() {
    return window.__CYLAA_HOST__ || null;
  }

  function log(msg) {
    const h = getHost();
    if (h && h.log) h.log(msg);
  }

  async function check(manual) {
    const h = getHost();
    if (!h || !h.hasUpdater) return;
    if (manual) log('正在检查更新…');
    for (const u of UPDATE_SOURCES) {
      try {
        const r = await fetch(u, { cache: 'no-store', signal: AbortSignal.timeout(6000) });
        if (!r.ok) continue;
        const j = await r.json();
        if (!j || !j.version) continue;
        if (isNewer(j.version, h.version)) {
          current = { version: String(j.version), url: String(j.url || ''), notes: String(j.notes || '') };
          h.setUpdate(current);
          log(`发现新版本 v${j.version}${j.notes ? '：' + j.notes : ''}`);
        } else {
          current = null;
          h.setUpdate(null);
          if (manual) log(`已是最新版本 v${h.version}`);
        }
        return;
      } catch (e) {
        /* 换下一个源 */
      }
    }
    if (manual) log('检查更新失败：更新源都访问不到（可稍后再试）');
  }

  function open() {
    if (current && current.url) window.open(current.url, '_blank');
  }

  // 由 content.js 的设置页调用，返回这一段 HTML；没有 update.js 时该插槽不会渲染。
  function settingsHtml() {
    const h = getHost();
    const v = h ? h.version : '0.0.0';
    const upd = current;
    return `
      <div class="tiny">当前版本 v${esc(v)}${upd ? ` · <b style="color:#c8161d">发现新版本 v${esc(upd.version)}</b>` : ''}</div>
      <div class="row">
        <button class="b" data-act="checkupd">检查更新</button>
        ${upd && upd.url ? '<button class="b p" data-act="openupd">去下载</button>' : ''}
      </div>`;
  }

  async function autoCheck() {
    if (typeof chrome === 'undefined' || !chrome.storage || !chrome.storage.local) return;
    try {
      const got = await chrome.storage.local.get('zhtjLastUpdateCheck');
      const last = got && got.zhtjLastUpdateCheck ? got.zhtjLastUpdateCheck.at : 0;
      if (Date.now() - last < 24 * 3600 * 1000) return;
      await chrome.storage.local.set({ zhtjLastUpdateCheck: { at: Date.now() } });
    } catch (e) {
      return;
    }
    check(false);
  }

  async function start() {
    // content.js 先加载并挂好 __CYLAA_HOST__；这里留一点重试余量
    for (let i = 0; i < 50 && !getHost(); i++) await new Promise((r) => setTimeout(r, 100));
    const h = getHost();
    if (!h || !h.hasUpdater) return;
    window.__CYLAA_UPDATER__ = { check, open, settingsHtml };
    window.dispatchEvent(new CustomEvent('cylaa:updater-ready'));
    if (IS_TOP) autoCheck();
  }

  start();
})();
