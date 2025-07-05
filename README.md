# TripMate - AI旅行提案アプリケーション

## プロジェクト概要

TripMateは、AIを活用した旅行提案アプリケーションです。ユーザーの好みや予算に基づいて、最適な旅行先とルートを提案します。

## 技術スタック

### フロントエンド (React)
- **React 18.2.0** - ユーザーインターフェース構築
- **TypeScript 4.8.4** - 型安全性の確保
- **React Router DOM 6.28.1** - ルーティング管理
- **React Scripts 5.0.1** - 開発環境とビルドツール

### バックエンド (Reflex)
- **Reflex 0.7.8** - Pythonベースのフルスタックフレームワーク
- **FastAPI** - APIサーバー
- **Uvicorn** - ASGIサーバー
- **Folium** - 地図表示機能
- **BeautifulSoup4** - Webスクレイピング
- **Requests** - HTTP通信

## プロジェクト構造

```
TripMate/
├── main/tripmate/          # Reactフロントエンド
│   ├── src/
│   │   ├── components/     # Reactコンポーネント
│   │   ├── pages/         # ページコンポーネント
│   │   └── App.tsx        # メインアプリケーション
│   └── package.json       # Node.js依存関係
├── ginmate/               # Reflexバックエンド
│   ├── app/
│   │   ├── components/    # Reflexコンポーネント
│   │   └── pages/        # ページ定義
│   ├── main.py           # メインアプリケーション
│   └── requirements.txt  # Python依存関係
└── README.md
```

## 起動方法

### 1. 依存関係のインストール

#### Reactフロントエンド
```bash
cd main/tripmate
npm install
```

#### Reflexバックエンド
```bash
cd ginmate
pip install -r requirements.txt
```

### 2. アプリケーションの起動

#### Reactフロントエンド
```bash
cd main/tripmate
npm start
```
- アクセス: http://localhost:3000

#### Reflexバックエンド
```bash
cd ginmate
python -m reflex run --env dev
```
- アクセス: http://localhost:3001

## 主な機能

### フロントエンド機能
- ユーザー登録・ログイン
- 旅行先選択
- ルート表示
- レスポンシブデザイン

### バックエンド機能
- AI旅行提案
- ルート生成
- 地図表示（Folium/Leaflet）
- リアルタイム通信
- 旅行ルートの可視化

## 開発環境

- **OS**: macOS 25.0.0
- **Node.js**: v24.2.0
- **Python**: 3.11.8
- **パッケージマネージャー**: npm, pip

## トラブルシューティング

### ポートが使用中の場合
```bash
# ポート3000を解放
lsof -ti:3000 | xargs kill -9

# ポート3001を解放
lsof -ti:3001 | xargs kill -9
```

### Reactアプリケーションが起動しない場合
```bash
cd main/tripmate
rm -rf node_modules package-lock.json
npm install
npm start
```

### Reflexアプリケーションが起動しない場合
```bash
cd ginmate
pip install --upgrade reflex
python -m reflex run
```

## デプロイ方法

### Vercelへのデプロイ

1. **GitHubにプッシュ**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Vercelでデプロイ**
- [Vercel](https://vercel.com)にアクセス
- GitHubリポジトリをインポート
- 自動的にデプロイが開始されます

### 環境変数の設定

Vercelのダッシュボードで以下の環境変数を設定：

- `ENV`: `prod`
- `FRONTEND_PORT`: `3000`
- `BACKEND_PORT`: `8000`
- `API_URL`: デプロイ後のAPI URL

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 