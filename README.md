# アルル制作所｜完成見学会マーケティング 完全版

住宅写真から、暮らしの物語が伝わるタイトル、SNS・LINE・Web文章、画像、チラシ、予約フォロー、動画準備、完成見学会LPまでを一貫制作する配布版です。

`SKILL.md` だけではなく、媒体別仕様、文章トーン、写真判定、法令確認、Canva引き渡し、検査スクリプト、テンプレートを含むスキル一式を収録しています。

全機能は [skills/openhouse-marketing-master/FEATURES.md](skills/openhouse-marketing-master/FEATURES.md) をご覧ください。

## インストール

Windows PowerShellで次を実行してください。

```powershell
irm https://raw.githubusercontent.com/aruru737/aruru-openhouse-skill/main/install.ps1 | iex
```

インストールされるSkillは1個です。ただし、動作に必要な `references/`、`scripts/`、`templates/`、`tests/` もすべて一緒にインストールされます。

```text
~/.agents/skills/openhouse-marketing-master/
```

Codex再起動後、住宅写真を添付して

```text
完成見学会の資料を作って
```

と入力してください。

## 主な機能

- 写真から5方向のタイトル・キャッチコピー・基本ストーリーを作成
- Instagram、LINE、Web、Googleビジネスプロフィール向け文章
- Instagram 4:5、LINE 1:1、Stories 9:16、カルーセル画像
- A4縦チラシ、依頼時のA4横チラシ、A3ポスター
- 予約フォーム、予約案内、来場前リマインド、来場後フォロー
- SNS動画台本、絵コンテ、撮影カット案
- レスポンシブ対応の完成見学会LP
- Canvaで編集可能なページ・レイヤーへの引き渡し
- 法令・許諾・媒体間整合の検査
- 完成物の一括ZIP化

## 配布ZIP

[openhouse-marketing-master-full.zip](dist/openhouse-marketing-master-full.zip)

ZIPを展開し、フォルダ内の `install.ps1` を実行してもインストールできます。既存版は日時付きでバックアップし、会社固有の `company-profile.yaml` は通常そのまま引き継ぎます。

© アルル制作所
