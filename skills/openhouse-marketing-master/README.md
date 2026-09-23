# openhouse-marketing-master の運用メモ

スキルが対応するセット、単品制作、文章・画像・Canva・品質検査・インストール機能は、[FEATURES.md](FEATURES.md) にまとめています。

このパソコンでは、このフォルダを**正本**として育てる。

| | 場所 |
|---|---|
| 正本（編集はここ） | `C:\Users\<user>\.agents\skills\openhouse-marketing-master\` — Codexが読む |
| 控え（自動コピー） | `C:\999_git_kei\claude-code\.claude\skills\openhouse-marketing-master\` — Claude Codeが読む |

## 直したら同期する

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\999_git_kei\claude-code\main\scripts\sync_openhouse_skill.ps1"
```

控え側を直しても、次の同期で消える。直すのは常にこのフォルダ。

## Gitから配布・インストールする

このフォルダの `install.ps1` は、`SKILL.md` だけでなく `references/`、`scripts/`、
`templates/`、`tests/` を含むスキル一式をインストールする。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.claude\skills\openhouse-marketing-master\install.ps1"
```

既存版がある場合は、同じ階層へ日時付きバックアップを作ってから入れ替える。
既存の `references/company-profile.yaml` は会社固有情報を守るため通常は引き継ぐ。
Git配布版のひな型へ戻す場合だけ、次を使う。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.claude\skills\openhouse-marketing-master\install.ps1" -ReplaceCompanyProfile
```

別の場所へ試験インストールするときは `-TargetRoot` でスキル格納フォルダを指定できる。
インストール後はCodexを再起動する。

## 中身

| ファイル | 役目 |
|---|---|
| `SKILL.md` | 流れ・番号メニュー・最優先ルール |
| `install.ps1` | Git配布版をバックアップ付きでインストール |
| `references/legal-housing.md` | 住宅・不動産の表示のルール（文章を書く前に読む） |
| `scripts/lint_output.py` | 原稿の検査。FAILが残る原稿は出さない |
| `references/company-profile.yaml` | 会社固有の承認済み表現・根拠・トーン |
| `references/photo-observation-rules.md` | 写真の観察と推測を分離する基準 |
| `references/channels/` | 媒体別の文字量・レイアウト・導線 |
| `scripts/validate_input.py` | 案件情報と許諾・特典条件の入力検査 |
| `scripts/check_cross_channel_consistency.py` | 複数媒体の基本情報の一致検査 |
| `tests/test_validators.py` | 検査スクリプトの基本テスト |

検査の使い方:

```
python scripts/lint_output.py <原稿ファイル> --event <開催情報のJSON>
```
