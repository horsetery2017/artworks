# 陈国军 · 作品选集

由《陈国军部分作品.pdf》整理的静态个人作品网站：8 件作品、9 张图片。支持手机与电脑、作品大图、键盘左右切换、Esc 关闭、《向量空间》双视角与原 PDF 下载。

## 本地查看

直接双击 `index.html`，默认打开英文页；点击顶部“中文”进入 `zh.html`，点击“EN”返回英文页。两页各自独立显示完整的作品、简介和对应语言的弹窗。无需安装软件或启动服务器。全部图片、脚本与字体回退均可离线使用。请保留文件之间的相对位置。

## 上传到 GitHub Pages

1. 本地仓库对应 `https://github.com/horsetery2017/artworks`，网站文件已放在仓库根目录。
2. 将文件提交并推送到远程仓库的 `main` 分支。保留整个 `assets` 文件夹和 `.nojekyll`。
3. 打开仓库 **Settings → Pages**，在 **Build and deployment** 中选择 **Deploy from a branch**，分支选择 **main**、目录选择 **/(root)**，保存。
4. 等待 GitHub 部署完成后，访问 `https://horsetery2017.github.io/artworks/`。部署状态以仓库 Pages 页面显示为准。

也可放入任意项目仓库的根目录，通过对应的项目 Pages 地址访问；网站使用相对路径，无需改代码。本次交付仅生成本地网站，尚未向 GitHub 上传或发布。

## 编辑

- `works.json`：作品名称、年代、艺术家原文说明、英文译文、图片与图录页码。修改后运行 `python tools/build_page.py`，同时生成英文 `index.html` 与中文 `zh.html`。所有说明和年代直接呈现在页面中，不需要打开弹窗；《向量空间》的两个视角也同时显示。
- `artist.json`：艺术家提供的中文个人简介及英文译文。修改后同样运行 `python tools/build_page.py`。
- `style.css`：颜色、字体、布局与手机样式。
- `app.js`：大图浏览与双视角交互。
- `assets/images`：WebP 网页预览和较大尺寸图片；保持原图比例，按 PDF 中的方向显示。
- `assets/chen-guojun-selected-works.pdf`：所提供 PDF 的完整副本。
- `tools/prepare_assets.py`：重新提取图片的可选脚本，需要 PyMuPDF、Pillow，以及网站上一级目录中的原始 PDF；日常修改文字不需要运行。

作品与图片的对应关系已经确认。《向量空间》两幅图片采用中性的“展陈视角 01 / 02”命名。作品说明、年代和个人简介均由艺术家提供，英文为译文。院校英文名称参考学校官网：https://www.gzarts.edu.cn/En/About_GAFA/Introduction.htm 和 https://www.joongbu.ac.kr/eng/ 。未补写尺寸或联系方式。PDF 中只有静态图像，本版本展示这些静态图像。

上传部署需要 `index.html`、`zh.html`、`style.css`、`app.js`、`favicon.svg`、`.nojekyll` 和整个 `assets` 文件夹。其余文件用于后续编辑，不影响网站运行。网站根地址默认显示英文，中文地址为 `https://horsetery2017.github.io/artworks/zh.html`；语言选择无需 JavaScript，也不依赖浏览器语言或缓存设置。
