# 远端（服务器）AI 起步指南

这份文件用于指导“服务器 VS Code 中的 AI”如何快速对齐上下文与拉取最新代码。

步骤

1. 打开仓库根目录，阅读 docs/AI_CONTEXT.md 顶部“最新小结”。
2. 在终端执行：scripts/sync/pull-shared-branch.sh（默认拉取 shared/win-sync 分支）。
3. 若未安装脚本执行权限：chmod +x scripts/sync/pull-shared-branch.sh。
4. 若当前目录不是 git 仓库：请先 git clone 相同的 GitHub 仓库到该路径。

额外说明

- 若需要回传变更给本地，请在服务器侧提交并 push 到 shared/win-sync；本地使用 push-shared-branch.ps1 继续迭代。
- 若仅临时传输文件，可以使用 scripts/sync/scp-sync.ps1，但推荐优先使用 Git 分支方式保持历史与合并能力。
