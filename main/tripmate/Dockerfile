# Node の公式イメージを使用
FROM node:18-alpine

# 作業ディレクトリ作成
WORKDIR /app

# package.json と package-lock.json をコピーして依存関係をインストール
COPY package*.json ./
RUN npm install

# プロジェクトのソースコードをすべてコピー
COPY . .

# ポートを 3200 番で使用
EXPOSE 3200
ENV PORT=3200

# 開発サーバーを起動
CMD ["npm", "start"]
