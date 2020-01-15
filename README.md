## 概要
作成したプログラムを上げます。  
- Hurwitzテスト
- Kharitonov  
のプログラムです。  
Hurwitzについては[サイト](https://hurwitz-test.site)で実装しています。

# Install

コマンドライン上で(windowsだったら Windows key + R -> cmd と入力)以下のコマンドを入力
```
pip install git+https://github.com/KMDMNAK/Hurwitz-Test.git
```

Pythonコマンドラインで以下を実行


``` python:main.py

from hurwitz.hurwitzTest import HurwitzStabililtyTestForRealPolymonials

coefficients = [2,3,4,5,6,7]
H = HurwitzStabililtyTestForRealPolymonials(coefficients)
result = H.execute() # true or false

```
