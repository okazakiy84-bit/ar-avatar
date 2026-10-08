# AR アバター（印刷物マーカー方式）

印刷したカードの QR コードを読み込むと Web ページが開き、カメラをカードに向けると
カードの上に 3D アバターが浮かび上がります。アプリのインストールは不要です。

- 使用ライブラリ: [MindAR](https://github.com/hiukim/mind-ar-js) 1.2.5 + [A-Frame](https://aframe.io/) 1.5.0（CDN から読み込み）
- 対応: iPhone の Safari / Android の Chrome（カメラの許可が必要）

## ファイル構成

| パス | 内容 |
|---|---|
| `index.html` | AR ページ本体 |
| `targets/card.png` | 印刷用カード（この画像がマーカー） |
| `targets/card.mind` | `card.png` から作った MindAR の学習データ |
| `targets/qr.png` | QR コード単体 |
| `models/Astronaut.glb` | 仮のアバター（Google model-viewer リポジトリのサンプル。動作確認用） |
| `tools/make_card.py` | カードと QR コードを作るスクリプト |

## 公開手順（GitHub Pages）

1. GitHub のリポジトリで **Settings → Pages** を開く
2. Source を **Deploy from a branch**、Branch を **main**、フォルダを **/ (root)** にして保存
3. 数分後に `https://okazakiy84-bit.github.io/ar-avatar/` で公開される
4. `targets/card.png` を印刷し（はがき〜A5 程度推奨）、スマホで QR を読み込む

URL が違う場合は `python tools/make_card.py <公開URL>` でカードを作り直し、
下記の手順で `card.mind` も作り直してください（カードの絵柄が変わると認識できなくなるため）。

## カスタマイズ

- **アバターを変える**: `models/` に `.glb` を置き、`index.html` の `<a-asset-item src>` を変更。
  VRoid Studio の VRM は Blender（VRM アドオン）などで `.glb` に書き出せます。
  大きさは `animation__appear` の `to:` の値で調整（カードの横幅 = 1）。
- **マーカー画像を変える**: 好きな画像を MindAR の
  [Image Target Compiler](https://hiukim.github.io/mind-ar-js-doc/tools/compile) に入れて `.mind` を作り、
  `targets/card.mind` を置き換えます。絵柄が細かく、繰り返し模様の少ない画像ほど認識が安定します。
