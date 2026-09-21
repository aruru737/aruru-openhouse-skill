---
name: openhouse-orchestrator
description: >
  住宅写真から完成見学会のタイトル・キャッチコピー候補を作り、番号選択で
  Instagram画像、LINE画像、A4縦チラシ、A4横チラシを順番に制作し、必要に応じて関連販促物も作る統合ワークフロー。
  ユーザーが「完成見学会の資料を作って」などと依頼したときに使う。
---

# 完成見学会マーケティング統合Skill

住宅写真を受け取り、ユーザーが番号を選ぶだけで完成見学会の販促物を作れるよう進行する。

## 最優先ルール
- 一度に質問する内容は原則1つ。
- 可能な限り番号選択で進める。
- 写真から分からない情報を創作しない。
- 選択済みのタイトル、キャッチコピー、説明文は後続制作で共通利用する。
- 同一住宅の制作物は、写真・色・余白・書体の方向性を統一する。
- 住宅そのものの形、窓、外壁、屋根、庭などを別物に改変しない。
- 画像制作機能が使える場合は実際に制作する。使えない場合は、完成版に近い制作仕様、掲載テキスト、レイアウト、制作プロンプトを返し、作成済みと偽らない。

## 起動
住宅写真とともに、以下に近い依頼を受けたとき起動する。
- 完成見学会の資料を作って
- この家の完成見学会資料を作成して
- 見学会用の販促物を作って

写真は1枚でも開始可。推奨3〜10枚。

## STEP 1：写真確認
`openhouse-photo-selector` の方針で各媒体に向く写真を内部選定する。分析内容は表示しない。

## STEP 2：タイトル・キャッチコピー候補
`openhouse-naming` の方針で10案を作る。各案に title / catchcopy / description を内部保持する。

ユーザーには必ず次の形式で提示する。

完成見学会のタイトル・キャッチコピーは、どれにしますか？
番号で答えてください。

1. タイトル
   キャッチコピー

2. タイトル
   キャッチコピー

…

10. タイトル
    キャッチコピー

11. 変更する

説明文は選択後の制作に利用するため内部保持し、求められた場合のみ表示する。

## STEP 3：変更
11が選ばれたら次だけを聞く。

どんな方向に変更したいですか？
「もっと上質に」「もっと家族の暮らしを感じるように」「庭を中心に」など、希望をそのまま入力してください。

回答を反映して10案を再生成し、再び1〜10＋11を表示する。

## STEP 4：コピー確定
1〜10が選ばれたら、その案の title / catchcopy / description を確定状態として保持する。

内部状態：
- SELECTED_TITLE
- SELECTED_CATCHCOPY
- SELECTED_DESCRIPTION
- CREATED_INSTAGRAM = false
- CREATED_LINE = false
- CREATED_FLYER_PORTRAIT = false
- CREATED_FLYER_LANDSCAPE = false

## STEP 5：基本制作物メニュー
最初は必ず以下を表示する。

次はどれを作りますか？
番号で答えてください。

1. Instagram投稿用の画像（4:5）
2. LINE配信用の画像（1:1）
3. チラシ縦タイプ（A4縦）
4. チラシ横タイプ（A4横）
5. 終了する

## STEP 6：制作
選択された制作物に対応するSkillを使用する。
- Instagram → openhouse-instagram-image
- LINE → openhouse-line-image
- A4縦 → openhouse-flyer-portrait
- A4横 → openhouse-flyer-landscape

開催情報が必要で未入力の場合は `openhouse-event-info` に従う。先にデザインできる場合は質問で止めず、差し替え欄として確保する。
完成前に `openhouse-final-check` で確認する。

## STEP 7：制作後のメニュー更新
1つ完成するたびに、その制作物を候補から削除する。残りだけを並べ、表示番号は必ず1から振り直す。最後に「終了する」を置く。
表示番号と内部制作物IDを混同しない。

例：Instagram制作済み

次はどれを作りますか？
番号で答えてください。

1. LINE配信用の画像（1:1）
2. チラシ縦タイプ（A4縦）
3. チラシ横タイプ（A4横）
4. 終了する

## STEP 8：基本4制作物が全部完成
4種類すべて完成したら、次を表示する。

基本の完成見学会資料がすべて完成しました。
関連する販促物も作りますか？
番号で答えてください。

1. Instagram投稿本文
2. LINE配信メッセージ
3. Web・ホームページ告知文
4. Instagramストーリーズ画像（9:16）
5. Instagramリール構成（15〜30秒）
6. Googleビジネスプロフィール告知文
7. A3完成見学会ポスター
8. 来場予約フォーム・予約案内文
9. 来場前リマインドメッセージ
10. 見学後のお礼・フォローメッセージ
11. 終了する

対応Skill：
- 1 → openhouse-instagram-caption
- 2 → openhouse-line-message
- 3 → openhouse-web-announcement
- 4 → openhouse-story-image
- 5 → openhouse-reel-script
- 6 → openhouse-google-business-post
- 7 → openhouse-poster-a3
- 8 → openhouse-reservation-copy
- 9 → openhouse-reminder-message
- 10 → openhouse-followup-message

1つ作るたびにその項目を候補から削除し、残りだけを1から振り直す。最後に「終了する」を置く。

## 終了
「終了する」が選択されたら簡潔に終了する。不要な追加営業や長いまとめをしない。
