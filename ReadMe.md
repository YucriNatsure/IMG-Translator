## IMG-Translator

# IMG-Translatorとは？
IMG-Translator(以下当アプリ)は、画像から文字を認識し、その文字を翻訳するものです

また画像を入れなくてもテキストを入力さえすれば翻訳はできるので、翻訳機としても活躍いたします

# 必要なもの
当アプリを使うにあたり、必要なものがあります

### 1: DeepLのトークン

これはDeepL翻訳を使いたい人はご自身のDeepLアカウントを作成して、そこからトークンを入手してください(無料版で大丈夫です)

入手したらダウンロードした中にある「path.json」にご自身のトークンを入力してください

### 2: tesseract 

めっちゃ重要です。これないと起動できません()

Windowsをお使いの方は https://github.com/UB-Mannheim/tesseract/wiki にアクセスして64か32bitをインストールしてください(64bit版を推奨します)

またインストールの際、インストールするものを選ぶ項目がありますが、すべてにチェックを入れてください

### 3: Python3.6以上の環境

開発者のPythonのバージョンは3.9.5 64bitです

### 4: DeepLのライブラリ

こちらはコンソールで以下の文を入れてインストールができます
```
pip install --upgrade deepl
```

### 5: Google trans

こちらも先ほど同様にコンソールにいれてインストールができます
```
pip3 install googletrans
```

### 6: Pillow

4,5同様にコンソールで
```
pip install Pillow
```

