# PromptGate ブランチ運用ルール

## 基本

- `main` は公開可能な安定状態に保つ。
- コード、テスト、README、docs、CI、`pyproject.toml` を変更する時は、作業ブランチを作る。
- 1ブランチ1目的にする。無関係な修正を混ぜない。
- `.claude/notes/`、`.claude/rules/`、`.claude/specs/` の小さなメモ更新だけなら `main` で作業してよい。

## ブランチ名

形式は `type/short-name` とする。英小文字、数字、ハイフンを使う。

- `feature/...`: 機能追加
- `fix/...`: バグ修正、検出精度の修正
- `docs/...`: README、docs、仕様更新
- `chore/...`: CI、開発環境、メタデータ更新
- `release/vX.Y.Z`: リリース準備
- `experiment/...`: 試作・検証

例:

- `feature/classifier-threshold`
- `fix/xml-wrapper-detection`
- `docs/versioning-rules`
- `release/v0.4.2`

## 作業開始時

作業前に現在のブランチと差分を確認する。

```bash
git branch --show-current
git status --short
```

未コミット差分がある場合は、ユーザーの作業を上書きしない。関係する差分は内容を確認し、無関係な差分は触らない。
