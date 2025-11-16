# E2Eテスト デバッグの道のり

このドキュメントは、Playwrightを使用したE2Eテストのセットアップ中に発生した一連の問題と、その解決プロセスを記録したものです。

## 初期問題：テスト実行の失敗

当初、`npm run test:e2e` を実行すると、以下の2つの主要なエラーによりテストが失敗していました。

1.  **Viteのビルドエラー:** `Multiple exports with the same name "default"`
2.  **Playwrightの環境エラー:** `Executable doesn't exist`

### 解決策

- **重複エクスポートの修正:** `frontend/src/stores/useHarnessStore.ts` ファイルにあった重複した `export default` 文を削除しました。
- **Playwrightブラウザのインストール:** `frontend` ディレクトリで `npx playwright install` を実行し、テストに必要なブラウザをダウンロードしました。

---

## 第2の問題：アプリケーションの起動クラッシュ

上記の問題を解決した後も、テストは依然として失敗しました。

**現象:**
- `await expect(page.getByTestId('sidebar')).toBeVisible()` の段階でタイムアウトする。
- これは、Playwrightがページ（`http://localhost:5173`）にアクセスした際に、アプリケーションがクラッシュし、何も描画されていない（真っ白なページ）ことを示唆していました。

### 原因特定までの長い道のり

アプリケーションがクラッシュする根本原因を特定するために、以下の仮説を立て、検証と修正を繰り返しました。

1.  **`reactflow`のフック使用法の問題（仮説）:**
    - `useReactFlow` フックの初期化タイミングに問題がある可能性を疑い、`HarnessVisualizer.tsx` コンポーネントをリファクタリングしました。
    - **結果:** 解決せず。

2.  **React 19との互換性問題（仮説）:**
    - `package.json` を調査し、`react: ^19.2.0` が使用されていることを発見。`reactflow@11` との互換性問題を疑いました。
    - **アクション:** Reactのバージョンを18にダウングレードし、`node_modules` と `package-lock.json` を削除してクリーンインストールを実行しました。
    - **結果:** 解決せず。

3.  **バックエンドAPIの不在（仮説）:**
    - `vite.config.ts` のプロキシ設定から、テスト実行時にバックエンドAPIサーバーが起動していないことが問題である可能性を疑いました。
    - **アクション:** Playwrightの `page.route()` を使用して、バックエンドへのAPIリクエストをすべてモックし、テストを自己完結させました。
    - **結果:** 解決せず。

### 真の原因：TypeScriptの型インポートエラー

最終的に、ユーザーがブラウザの開発者ツールで確認したコンソールエラーが、問題解決の鍵となりました。

**エラー:** `Uncaught SyntaxError: The requested module ... does not provide an export named 'HarnessData'`

**根本原因:**
TypeScriptの `interface` は「型」であり、JavaScriptにコンパイルされると消去されます。しかし、複数のファイルで `interface` を「値」であるかのようにインポートしていました。これがモジュール解決エラーを引き起こし、アプリケーション全体のクラッシュにつながっていました。

**修正:**
以下の3つのファイルで、`HarnessData` や `LibraryComponent` といった型のインポートを、`import type` を使用した型のみのインポートに修正しました。

- `frontend/src/services/api.ts`
- `frontend/src/components/Sidebar.tsx`
- `frontend/src/stores/useHarnessStore.ts`

**修正例:**
```typescript
// 修正前
import { HarnessData } from '../utils/dataTransformer';

// 修正後
import type { HarnessData } from '../utils/dataTransformer';
```

---

## 第3の問題：ドラッグ＆ドロップの失敗

アプリケーションのクラッシュが解決されると、テストは先に進みましたが、新たな問題が発生しました。

**現象:**
- 最初のコンポーネントをドラッグ＆ドロップした後、テストが停止または失敗する。

**原因と解決策:**

1.  **ノードが表示されない:**
    - **原因:** `onDrop` イベントハンドラ内でのドロップ座標の計算ロジックが不安定でした。
    - **アクション:** `getBoundingClientRect` を使った手動計算をやめ、`screenToFlowPosition` に `event.clientX/Y` を直接渡すシンプルな方式に修正しました。

2.  **それでもノードが表示されない（最終修正）:**
    - **原因:** `useReactFlow` フックの代わりに、より堅牢な `onLoad` コールバックと `useState` を使用してReact Flowのインスタンスを取得する必要がありました。`useReactFlow`フックでは、`onDrop` の時点でインスタンスが完全には利用可能になっていない可能性がありました。
    - **アクション:** `HarnessVisualizer.tsx` をリファクタリングし、`<ReactFlow>` コンポーネントの `onLoad` プロパティでインスタンスを取得し、それを `useState` で管理する方式に変更しました。

この一連のデバッグプロセスを経て、E2Eテストは最終的に安定して動作するようになりました。
