# ipicls1D
**pic_density**
1次元粒子コード ipicls1d が出力する電子・イオン密度に関するデータをグラフ化するスクリプト．
awk, gnuplot,  platex, dvipdfmx, convert(imagemagick) が必要．  

convertは、homebrew で、brew install imagimagick でインストールできる．


Pathの通ったところに保存し、  
chmod +x pic_density   
で実行許可を与え、計算結果が格納されているディレクトリで実行する．

オプション  -f, -t, -b, -u, -s が設定されていて、  
-f : 横軸の始まりの値を指定  
-t : 横軸の終わりの値を指定  
-b : 縦軸の最小値を指定  
-u : 縦軸の最大値を指定  
-s : 1 ページのグラフの数を 1,2,6 から指定する．デフォルトは 1．  

動画(アニメーション)は、Safari で表示されるので、Mac以外のときは最終行を適切に書き換えること．
