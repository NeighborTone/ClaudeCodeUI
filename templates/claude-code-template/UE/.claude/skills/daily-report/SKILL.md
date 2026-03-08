---
name: daily-report
description: Generate daily report from today's VCS commits
allowed-tools: Bash(git:*)
---

# Daily Report

## Usage
```
/daily-report
```

## Workflow

1. 今日のコミット履歴を取得する:

```bash
git log --oneline --since="today 00:00" --format="%h %s"
```

2. 今日の日付のコミットだけを抽出し、作業内容を把握する

3. 以下のフォーマットで日報を出力する

## Format

```
### 今回の作業内容

- 作業1
- 作業2
- 作業3

---

### 課題

- 課題があれば記載

---

### 次回の予定

- 予定1
- 予定2

---

### その他

- 補足があれば記載
```

## Rules

- 簡潔に書く（1項目1行）
- ドキュメントの引用・パスは付けない
- チェックポイント番号（CP X-Y）やPhase番号は付けない
- 技術用語は使ってよいが、内部管理番号は不要
- 課題・次回の予定・その他は、該当なしなら「- なし」と書く
