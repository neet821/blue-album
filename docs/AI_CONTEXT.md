# AI 项目上下文与对齐说明

目的：让“服务器 VS Code 中的 AI”与“本地 VS Code 中的 AI/你”共享相同的代码与上下文。将此文件视为跨会话的“单一事实来源”。

你需要做什么

- 始终把重要结论、已做改动、小结和下一步写在本文件顶部的“最新小结”。
- 提交并推送到同一分支；在服务器窗口里拉取相同分支。本文件即是远端 AI 的快速对齐入口。

最新小结（请随做随更）

- 更新时间：2025-10-23
- 本地环境：Windows + VS Code + PowerShell；仓库 remote: origin (GitHub: neet821/blue-album)
- 同步策略：使用同一 Git 分支（默认 shared/win-sync），服务器侧拉取此分支
- 最近操作：
  1. 建立跨设备 AI 对齐机制（本文件 + 同步脚本）
  2. 清理根目录 89 个零字节空文件（测试脚本、临时文档、空 .bat/.py/.md）
  3. 生成清理报告：docs/零字节文件清理说明.md
- 约定：服务器 VS Code 打开的是同一个仓库路径；若未克隆请先执行 git clone

分支与同步约定

- 分支：shared/win-sync（建议固定，用于“本地⇄服务器”快速对齐）
- 同步顺序：本地提交→推送到 origin→服务器拉取同分支。
- 冲突处理：若服务器存在未提交改动，请先提交/暂存于服务器，再拉取。

服务器侧需要的前置

- 服务器路径必须是本仓库的一个 git clone，且 origin 指向同一 GitHub 仓库。
- 服务器已安装 git 和 ssh；VS Code 通过 Remote SSH 打开该路径。

常见问题

- 服务器 AI 看不到改动：确认分支一致，且服务器已 git pull；本文件是否同步更新。
- 服务器路径不是 git 仓库：先在目标路径 git clone 本仓库，再切换到同步分支。

附：最小操作流程（本地）

1) 编辑/更新本文件“最新小结”。
2) 提交并推送到 shared/win-sync 分支。
3) 在服务器 VS Code 终端：git fetch origin && git checkout -B shared/win-sync origin/shared/win-sync && git pull --ff-only
