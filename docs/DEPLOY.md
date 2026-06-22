# 部署指南：上线到 Streamlit Community Cloud

把这个 demo 部署成一个公开链接（`https://你的名字-xxx.streamlit.app`），
**放进简历比 GitHub 链接威力大得多**——招聘官点进去 30 秒就能自己输入指令试。
免费、无需服务器。全程约 10 分钟。

---

## 前置：把代码推上 GitHub（公开仓库）

```bash
cd 项目目录
git init
git add .
git commit -m "多语种车载意图路由器"
# 在 github.com 新建一个 public 仓库后：
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

> ⚠️ **关键安全检查**：推送前确认 `.gitignore` 已生效，`git status` 里**不能出现** `.streamlit/secrets.toml` 或 `.env`。
> 公开仓库一旦提交 API key，会在几分钟内被爬虫扫到盗刷。本项目已配好 `.gitignore` 挡住这些文件。

---

## 第 1 步：登录 Streamlit Cloud

1. 打开 https://share.streamlit.io
2. 用你的 GitHub 账号登录（授权它读取你的仓库）

## 第 2 步：创建 App

1. 点 **New app** → **Deploy a public app from GitHub**
2. 选择：
   - Repository：你刚推上去的仓库
   - Branch：`main`
   - Main file path：`app.py`
3. 先**不要**点 Deploy，先去配密钥（下一步）

## 第 3 步：配置 LLM 密钥（Secrets）

点 **Advanced settings** → **Secrets**，粘贴下面内容并填上真实值
（格式见仓库里的 `.streamlit/secrets.toml.example`）：

```toml
LLM_API_KEY = "你的真实key"
LLM_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
LLM_MODEL = "qwen-plus"
```

> - 用**通义千问**：base_url 如上，model 填 `qwen-plus` / `qwen-turbo`
> - 用 **DeepSeek**：base_url 填 `https://api.deepseek.com`，model 填 `deepseek-chat`
> - 用 **OpenAI**：删掉 `LLM_BASE_URL` 这行，model 填 `gpt-4o-mini`
> - **不配也能部署**：会以规则引擎运行，但混说效果一般，建议至少配一个便宜的 model

## 第 4 步：部署

点 **Deploy**，等 2-3 分钟（首次要装依赖）。完成后得到一个公开 URL。

---

## 上线后自查清单

- [ ] 打开 URL，侧边栏显示「LLM 已启用」（说明 secrets 读到了）
- [ ] 实时路由输入"把 air conditioning 调到 20 度"，能正确命中 `climate.set_temperature`
- [ ] 质量看板点「跑评测集」，整体准确率明显高于规则引擎基线(84.5%),且三语种均衡
- [ ] 把这个 URL 加到简历项目那一行，和 GitHub 链接并列

---

## 成本与防滥用提示

- 公开链接任何人都能用，会消耗你的 LLM 额度。建议：
  - 用便宜的 model（千问 turbo / deepseek-chat，单次调用成本极低）
  - 在 LLM 厂商后台设**消费上限**，避免被刷爆
- 评测集只有 27 条，跑一次评测的调用量可控，不必担心。

---

## 备选：录一段 GIF 放 README

如果不想长期挂一个消耗额度的公开服务，也可以本地跑起来录一段操作 GIF
（输入混说指令 → 命中功能 → 跑评测看板），放到 README 顶部。
macOS 用 `Cmd+Shift+5` 录屏，再用在线工具转 GIF 即可。静态截图已经有了，GIF 是加分项。
