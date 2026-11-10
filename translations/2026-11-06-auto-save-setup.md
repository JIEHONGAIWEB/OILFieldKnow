# Auto-save setup for doc-translator

## Original (中文)
已设置自动保存。改动在 .claude/agents/doc-translator.md,并新建了 translations/ 文件夹。
- 保存位置:每次翻译完,助手自动写入 translations/。
- 文件名:YYYY-MM-DD-简短主题.md,例如 2026-11-06-well-report.md。
- 文件内容:中文原文、英文译文、关键信息清单。
- 重名处理:同名文件已存在时加 -2,不会覆盖旧文件。
- 回复提示:保存后会在回复末尾告诉你文件路径。
我没有实际跑过这个助手。配置改完后,你可能要重开会话才会生效。

## Translation
Auto-save has been set up. The change is in .claude/agents/doc-translator.md, and a new translations/ folder was created.
- Save location: after each translation, the assistant automatically writes to translations/.
- File name: YYYY-MM-DD-short-topic.md, e.g. 2026-11-06-well-report.md.
- File content: the Chinese original, the English translation, and a key-information list.
- Duplicate handling: if a file with the same name exists, "-2" is appended; the old file is never overwritten.
- Reply notice: after saving, the file path is given at the end of the reply.
I have not actually run this assistant. After the configuration change, you may need to restart the session for it to take effect.

## Key Information
- **Topic:** Enabling auto-save for the doc-translator assistant
- **Key terms:** 自动保存 → auto-save; 重名 → duplicate file name; 关键信息清单 → key-information list
- **Files / Paths:** .claude/agents/doc-translator.md; translations/
- **Figures / Metrics:** naming pattern YYYY-MM-DD-short-topic.md; suffix "-2" on duplicates
- **Action items:** Restart the session so the new agent configuration takes effect
