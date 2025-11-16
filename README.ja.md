# KiCadハーネス設計SaaS - バックエンド

[![CI](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/<OWNER>/<REPO>/graph/badge.svg?token=<TOKEN>)](https://codecov.io/gh/<OWNER>/<REPO>)

このリポジトリは、KiCadハーネス設計SaaSアプリケーションのバックエンドを含みます。これはFastAPIベースのサービスであり、JSONデータからKiCadの回路図ファイル（`.kicad_sch`）をプログラムで生成し、`kicad-cli`を使用してDXFやBOMファイルなどの製造用ファイルを出力する責任を担います。

この初期実装は、中核となるワークフローを検証するための技術スパイク（サイクル0）として機能します。

## APIドキュメント

アプリケーションの実行後、APIドキュメントはFastAPIによって自動的に生成され、以下のURLで利用可能です。

-   **Swagger UI:** [`/docs`](http://127.0.0.1:8000/docs)
-   **ReDoc:** [`/redoc`](http://127.0.0.1:8000/redoc)

## ハーネスAPI

このサービスの中核は、ハーネスデータの「単一の信頼できる情報源（Single Source of Truth）」を確立するハーネスAPIです。

-   `POST /api/v1/harnesses/`: 詳細なJSONオブジェクトから新しいハーネス定義を作成します。
-   `PUT /api/v1/harnesses/{harness_id}`: 既存のハーネス定義を提供されたJSONオブジェクトで上書き更新します。
-   `GET /api/v1/harnesses/{harness_id}/bom`: 指定されたハーネスの部品表（BOM）を返します。
-   `GET /api/v1/harnesses/{harness_id}/cutlist`: ハーネスのワイヤーカットリストを返します。
-   `GET /api/v1/harnesses/{harness_id}/fromto`: ハーネスの結線リスト（From-Toリスト）を返します。
-   `GET /api/v1/components`: フロントエンドのコンポーネントライブラリ用に、利用可能なコンポーネント（コネクタ、電線）のリストを返します。

## プロジェクト構造

このプロジェクトは、関心事を分離するためにクリーンアーキテクチャに従っています。

-   `/app`: メインアプリケーションコード
    -   `/api`: FastAPIのエンドポイントとルーター
    -   `/core`: 設定管理
    -   `/db`: データベースセッションとベースモデルの定義
    -   `/models`: SQLAlchemyのORMモデル
    -   `/schemas`: データバリデーション用のPydanticスキーマ
    -   `/services`: `KiCadEngineService`を含むコアビジネスロジック
-   `/tests`: バックエンド用のPytestテストスイート
-   `/alembic`: Alembicのデータベースマイグレーションスクリプト
-   `/frontend`: インタラクティブなハーネスエディタのためのReactベースのフロントエンドアプリケーション

## フロントエンドアプリケーション

このプロジェクトには、`/frontend`ディレクトリに配置された、React、TypeScript、Viteで構築されたフロントエンドアプリケーションが含まれています。これにより、ハーネス設計を作成・修正するためのインタラクティブなWebベースのエディタが提供されます。

### フロントエンドの実行方法

フロントエンドの開発サーバーを実行するには：

1.  **フロントエンドディレクトリに移動します:**
    ```bash
    cd frontend
    ```

2.  **依存関係をインストールします:**
    ```bash
    npm install
    ```

3.  **Vite開発サーバーを起動します:**
    ```bash
    npm run dev
    ```

フロントエンドアプリケーションは`http://localhost:5173`（または次に利用可能なポート）で利用可能になります。APIリクエストは、`http://127.0.0.1:8000`で実行されているバックエンドサーバーにプロキシされるように設定されています。

## セットアップ方法

### 前提条件

-   Python 3.10以上
-   KiCad 7.x以降（`kicad-cli`がシステムのPATHに含まれていること）
-   `uv`（または`pip`と`venv`）

### インストールとセットアップ

1.  **リポジトリをクローンします:**

    ```bash
    git clone <repository-url>
    cd kicad-harness-saas
    ```

2.  **仮想環境を作成し、依存関係をインストールします:**

    `uv`を使用する場合:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

    `venv`と`pip`を使用する場合:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **（任意）環境変数:**

    アプリケーションは設定に`.env`ファイルを使用します。デフォルトの`DATABASE_URL`が提供されていますが、`.env`ファイルを作成して設定を上書きすることができます。

    ```
    DATABASE_URL="sqlite:///./your_database_name.db"
    ```

### アプリケーションの実行

開発サーバーを実行するには：

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

APIは`http://127.0.0.1:8000`で利用可能になります。

### テストの実行

テストスイートを実行するには：

```bash
source .venv/bin/activate
pytest
```

テストには`kicad-cli`と`kicad-sch-api`のモックが含まれており、KiCadを完全にインストールしていなくても実行できます。
