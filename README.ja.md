# KiCadハーネス設計SaaS - バックエンド

[![CI](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/<OWNER>/<REPO>/graph/badge.svg?token=<TOKEN>)](https://codecov.io/gh/<OWNER>/<REPO>)

このリポジトリは、KiCadハーネス設計SaaSアプリケーションのバックエンドを含みます。これはFastAPIベースのサービスであり、JSONデータからKiCadの回路図ファイル（`.kicad_sch`）をプログラムで生成し、`kicad-cli`を使用してDXFやBOMファイルなどの製造用ファイルを出力する責任を担います。

このSaaSアプリケーションは、主に2つのAPIエンドポイント群を提供します。

1.  **ハーネス設計とエクスポートAPI:** ハーネス設計プロジェクトを作成し、製造用ファイル（DXF、BOMなど）をエクスポートするためのエンドポイント群です (`/api/v1/projects`)。
2.  **KiCad HTTPライブラリAPI:** KiCad 8/9の「HTTPライブラリ」機能と互換性のあるエンドポイント群です。これにより、KiCadユーザーはSaaS上で集中管理されたコンポーネントライブラリにアクセスできます (`/api/v1/kicad_library`)。

このREADMEでは、主に初期セットアップについて説明しています。詳細なAPIの利用方法については、自動生成されるAPIドキュメントを参照してください。

## APIドキュメント

アプリケーションの実行後、APIドキュメントはFastAPIによって自動的に生成され、以下のURLで利用可能です。

-   **Swagger UI:** [`/docs`](http://127.0.0.1:8000/docs)
-   **ReDoc:** [`/redoc`](http://127.0.0.1:8000/redoc)

## プロジェクト構造

このプロジェクトは、関心事を分離するためにクリーンアーキテクチャに従っています。

-   `/app`: メインアプリケーションコード
    -   `/api`: FastAPIのエンドポイントとルーター
    -   `/core`: 設定管理
    -   `/db`: データベースセッションとベースモデルの定義
    -   `/models`: SQLAlchemyのORMモデル
    -   `/schemas`: データバリデーション用のPydanticスキーマ
    -   `/services`: `KiCadEngineService`を含むコアビジネスロジック
-   `/tests`: Pytestのテストスイート
-   `/alembic`: Alembicのデータベースマイグレーションスクリプト

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
