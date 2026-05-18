// shared site logic: theme + nav + small utilities

const STORAGE_KEY = "wd-theme";

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  const btn = document.querySelector(".theme-btn");
  if (btn) btn.textContent = theme === "dark" ? "☀" : "☾";
}

function initTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved || (prefersDark ? "dark" : "light"));
}

function toggleTheme() {
  const cur = document.documentElement.getAttribute("data-theme");
  const next = cur === "dark" ? "light" : "dark";
  localStorage.setItem(STORAGE_KEY, next);
  applyTheme(next);
}

function buildHeader(active) {
  const links = [
    { href: "index.html", label: "首页", key: "home" },
    { href: "projects.html", label: "项目", key: "projects" },
    { href: "notes.html", label: "笔记", key: "notes" },
    { href: "about.html", label: "关于", key: "about" },
  ];
  const html = `
    <div class="container">
      <nav class="nav">
        <a class="brand" href="index.html"><span class="dot"></span>frank · WaterDimension</a>
        <div class="nav-links">
          ${links.map(l => `<a href="${l.href}" class="${l.key === active ? "active" : ""}">${l.label}</a>`).join("")}
          <button class="theme-btn" aria-label="切换主题" onclick="toggleTheme()">☾</button>
        </div>
      </nav>
    </div>`;
  const header = document.querySelector(".site-header");
  if (header) header.innerHTML = html;
}

function buildFooter() {
  const html = `
    <div class="container">
      © ${new Date().getFullYear()} frank · 由静态页面驱动 · <a href="https://github.com/WaterDimension" target="_blank" rel="noopener">GitHub</a>
    </div>`;
  const footer = document.querySelector(".site-footer");
  if (footer) footer.innerHTML = html;
}

async function loadJSON(path) {
  const res = await fetch(path, { cache: "no-cache" });
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );
}

const LANG_COLORS = {
  Java: "#b07219",
  Python: "#3572A5",
  HTML: "#e34c26",
  JavaScript: "#f1e05a",
  "C++": "#f34b7d",
  TypeScript: "#3178c6",
  Go: "#00ADD8",
  Vue: "#41b883",
};

function langDot(lang) {
  return `<span class="dot" style="background:${LANG_COLORS[lang] || "#999"}"></span>`;
}

function relativeDate(iso) {
  if (!iso) return "";
  const then = new Date(iso).getTime();
  const diff = (Date.now() - then) / 1000;
  if (diff < 60) return "刚刚";
  if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} 小时前`;
  if (diff < 86400 * 30) return `${Math.floor(diff / 86400)} 天前`;
  if (diff < 86400 * 365) return `${Math.floor(diff / 86400 / 30)} 个月前`;
  return `${Math.floor(diff / 86400 / 365)} 年前`;
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  const active = document.body.dataset.page || "home";
  buildHeader(active);
  buildFooter();
});
