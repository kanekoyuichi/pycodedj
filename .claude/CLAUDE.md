# ContextGate — AI 行動指針

## Memory

作業の記録は `.claude/projects/contextgate/.claude/memory/` 配下に保存する。
インデックスは `MEMORY.md`。新しい知見・決定事項・フィードバックが生じたら都度更新する。

## Notes

`.claude/notes/` 配下には気づいたことや記事の下書きなどを自由に置く。コードや仕様とは切り離した作業メモ用ディレクトリ。

## プロジェクト情報の参照先

- 仕様: `.claude/spec.md`
- 実装計画: `.claude/plan.md`

## 実装方針

- シンプル第一。影響するコードを最小限にする
- v0.1 スコープを厳守する。スコープ外の機能を実装しない
- 3ステップ以上のタスクは必ず Plan モードで開始する

## コード規約

- Python >= 3.10 の型ヒントを使用する（`str | None` 形式）
- `dataclass` を使用する。Pydantic は使わない
- コメントは WHY が非自明な場合のみ書く

## テスト方針

- pytestで実施する
- 動作を証明できるまで完了としない

## Codex レビュー

コードを新規作成または修正した場合、実装完了後に必ず Codex レビューを実施する。

手順は `.claude/skills/codex-review.md` を参照。

- `codex review --uncommitted` でレビューを実行する
- レビュー結果をすべてユーザーに提示する
- レビュー結果に対して修正を実行する
- 修正を行った後は、適用後に変更内容を確認し、テストを実行する
- Codexの再レビューを実行する
