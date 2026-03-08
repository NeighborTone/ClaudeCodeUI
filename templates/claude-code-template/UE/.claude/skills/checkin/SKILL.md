---
name: checkin
description: Check in changes to version control, build, and verify
allowed-tools: Bash(git:*), Bash(Build.bat:*), Bash(powershell:*), Read, AskUserQuestion
---

# Version Control Check-in + Build + Verify

## Usage
```
/checkin [message]
```

## Description
VCSへのコミット → ビルド検証を一括実行する。

## Workflow

### Phase 1: Version Control Check-in

#### 1. Check Status
```bash
git status
git diff --stat
```

#### 2. ファイルリストをユーザーに提示 (必須)
`git status` の結果を以下のカテゴリに分類して表示する:
- **変更済み (Modified)**: 既存ファイルの変更
- **新規 (Untracked/Added)**: 新しく追加されたファイル
- **削除 (Deleted)**: 削除されたファイル

**必ず以下を明示的に確認すること:**
- [ ] `.uasset` / `.umap` Blueprint ファイルが含まれているか（UEプロジェクトの場合）
- [ ] `Build.cs` ファイルが含まれているか（UEプロジェクトの場合）
- [ ] Config 設定ファイルの変更が含まれているか
- [ ] セッション中に編集した全ファイルがリストに含まれているか

ユーザーに全ファイルリストを提示し、コミットの確認を求める。

#### 3. Stage & Commit
```bash
# 個別にファイルを追加（git add -A は使わない）
git add "path/to/file1" "path/to/file2"
git commit -m "メッセージ"
```

#### 4. Verify Commit (必須)
```bash
git status
```
- **変更が残っている場合** → ユーザーに報告
- **変更なし** → Phase 2へ進む

### Phase 2: Build Verification (コミット成功後に自動実行)

```bash
{{BUILD_COMMAND}}
```

**ビルド失敗時**: エラーログを報告して停止。

## Commit Message Format
```
[Category] 変更概要

詳細説明（任意）

Co-Authored-By: Claude <co-author>
```

### Categories
- `[Feature]` - 新機能
- `[Fix]` - バグ修正
- `[Refactor]` - リファクタリング
- `[Docs]` - ドキュメント
- `[WIP]` - 作業中
- `[CP X-Y]` - チェックポイント

## Important Notes
- バイナリファイル（.uasset, .umap）は注意してコミット
- Saved/ と Intermediate/ はコミットしない
- `.env`, `secrets/` はコミットしない
- **コミット後は必ず `git status` で漏れを確認する**
- **コミットにはファイルを明示的にステージングする（`git add -A` 禁止）**
