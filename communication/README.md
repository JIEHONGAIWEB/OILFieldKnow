# 沟通交流话术

本文件夹用于存放沟通交流的常用话语。

## 建议分类
- meeting.md:会议用语
- email.md:邮件模板
- feedback.md:反馈、催办话术

## 如何调用 doc-translator 代理

doc-translator 是一个子代理,用于把中文文档/描述翻译成英文,并提取关键信息清单。翻译结果会保存到 `translations/` 目录(如 `translations/2026-11-06-greeting.md`)。

### 方式一:斜杠命令(最简单)
在 Claude Code 对话框中输入要翻译的文字,再加上 `/doc-translator`:

```
帮助我翻译这段话 你好 很高兴能认识你 /doc-translator
```

### 方式二:自然语言指定代理
直接告诉 Claude 使用该代理:

```
请使用 doc-translator 代理翻译下面的内容,并提取要点清单:
<粘贴中文内容>
```

### 方式三:翻译文件
给出文件路径,代理会读取文件后翻译:

```
请用 doc-translator 代理翻译 communication/meeting.md,并提取关键信息
```

### 输出内容
- **Translation**:英文译文
- **Key Information**:主题、关键术语对照、人物/日期/数字/待办事项(文本中没有的项会省略)
- **Saved to**:译文保存路径

### 适用场景
- 需要把中文文档、描述翻译成英文
- 需要从中文文本中提取要点列表

> 提示:代理在后台运行,完成后会自动返回结果,无需手动轮询。

## 如何调用 doc-sync 代理

doc-sync 是文档同步助手,按路由规则把文档归类并同步到对应文件夹(如会议话术 → `communication/`,翻译稿 → `translations/`,Bug 记录 → `bug-knowledge/`),并更新目标目录的 README 索引。路由表见 `.claude/agents/doc-sync.md`,可直接编辑。

```
请使用 doc-sync 代理把 xxx.md 同步到对应文件夹
请使用 doc-sync 代理整理并归档下面这段内容:<粘贴内容>
```

- 默认复制,不删除源文件;要移动请明确说"移动"。
- 目标已有同名且内容不同的文件时会先询问,不会覆盖。
- 无法判定类型时会列出候选目录让你确认。
