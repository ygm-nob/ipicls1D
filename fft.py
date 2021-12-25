#!/usr/local/bin/python3
# coding: utf-8

############################################################################################
#  【fft.py】
#    fft を行う python3 プログラム
#      スペース区切りの時系列データファイルを指定し、
#      フーリエ変換(FFT)されたパワースペクトルと位相のファイルを出力する．
#
#  ・インストール方法
#      fft.py を PATH の通ったところにセーブし、
#        > chmod +x fft.py
#      で、実行許可を与える．
#      実行時に、いくつかのパッケージのインストールを要求されたら、
#       > pip3 install numpy
#      で、インストールすること．numpy や argparse は普通インストールされていない．
#
#  ・使い方
#       > fft.py -h
#      で、簡単な使い方の help が表示される
#
#    使っている parse については、以下のURLを参考にする
#               https://www.sejuku.net/blog/23647#argparse-3
#
# 【!!!注意!!!】
# グラフの作成には、外部コマンドの gnuplot を使っているので、 gnuplot の install が必要
#
############################################################################################

import numpy as np
import argparse
from argparse import RawTextHelpFormatter
import os.path
import subprocess

# パーサーを作る．ここでは全体の設定をする
parser = argparse.ArgumentParser(
            prog='fft.py',                       # プログラム名
            usage='fft.py [-h] [-g --gnuplot, -n --norm, -c --csv, -c --silent] data_file', # プログラムの利用方法
            description="2 列のデータ(デフォルトは space 区切り)の高速フーリエ変換(FFT)プログラム\nデータの # で始まる行は無視されます．\nグラフを表示するためには gnuplot がインストールされている必要があります．\n以下は引数です．" ,                                  # 引数のヘルプの前に表示
            epilog='end',                          # 引数のヘルプの後で表示
            add_help=True,                         # -h/–help オプションの設定
            formatter_class=RawTextHelpFormatter   # help の文の改行をするため
)


# option の設定．
parser.add_argument('-g', '--gnuplot', help='gnuplotで作成したグラフ(pdf)を表示', action='store_true') # gnuplot option
parser.add_argument('-c', '--csv', help='csv file を指定(デフォルトは space 区切り)', action='store_true') # csv option
parser.add_argument('-s', '--silent', help='-g オプションを指定しているとき、グラフ(pdf)の画面表示をしない(epsは保存されます)', action='store_true') # option 引数
parser.add_argument('-n', '--norm', help='最大値で規格化(epsは保存されます)', action='store_true') # normalization option
parser.add_argument('data_file', help='データファイル(必須)')    # 必須の引数を追加(- や -- 以外で始まる引数)

# 引数を解析する(お決まりの記述)
args = parser.parse_args()

# file 名を分割(拡張子を除いた部分を basename とする)
basename, ext = os.path.splitext(args.data_file)   # 位置引数の data_file のファイル名の拡張子を除いた部分の取得

# 出力するファイル名
fft_data_file = basename + '_fft.dat'          # fft のデータファイル名
phase_data_file = basename + '_phase.dat'      # fft の位相データファイル名
fft_data_eps  = basename + '_fft.eps'          # fft グラフのファイル名(eps)
gp_file       = basename + '_fft.gp'           # gnuplot のスクリプト

#data = np.loadtxt(args.data_file)  # 入力のファイル．2列のデータ(時間、振幅)

# ファイルの読み込み
# ファイルの冒頭の# はコメント行とする．
# 1 列目と 2列目だけを読み込む．
if args.csv:                # -c または --csv で csv file を指定しているとき
    # loadtxt の usecols は、読み込む列を指定．ここでは 1 列目と 2 列目を指定している．
    data = np.loadtxt(args.data_file, delimiter=',', comments="#", usecols=(0,1))  # 入力のファイル．2列のデータ(時間、振幅)
else:                       # -c または --csv で csv file を指定していないとき(つまり、デフォルトの space 区切りの場合)
    data = np.loadtxt(args.data_file, comments="#", usecols=(0,1))

time = data[:,0]                                # 入力ファイルの1列目を抽出
signal = data[:,1]                              # 入力ファイルの2列目を抽出

samplingPeriod = time[1] - time[0]              # サンプリング時間
samplingFreq = 1/samplingPeriod                 # サンプリング周波数

# FFT Y-axis
sp =  np.fft.fft(signal)                        # ここで入力信号を FFT している
N = len(sp)                                     # fft のデータ数
y = np.abs(sp)                                  # spectrum 絶対値 (もう少し長い変数名にすればよかった．)
max_intensity =max(y)                           # fft 強度の最大値．データを規格化する時に使う． see args.norm

# データを規格化するか．-n or --norm 指定のときは、最大値で割る
if args.norm:
    y=y/max_intensity


# FFT Phase
p = np.angle(sp)                                # 位相 (もう少し長い変数名にすればよかった．)

# FFT X-axis                                    # fft したときの各周波数(もう少し長い変数名にすればよかった．)
x = np.fft.fftfreq(N, samplingPeriod)


final = np.c_[x, y]                             # x 軸と y 軸のデータの結合
np.savetxt(fft_data_file, final)                # xy 2列の FFT のデータの保存

phase =np.c_[x, p]                              # x 軸と 位相の値の データの結合
np.savetxt(phase_data_file, phase)              # xy 2列の FFT位相のデータの保存

# option --gnuplot (-g) の有無での分岐
if args.gnuplot:
#   gnuplot を実行するとき:
    gp_script =" set term postscript eps color enhanced font  ',24'\n set output '"+fft_data_eps+"'\n set xrange [0:]\n set xlabel 'Frequency'\n plot '"+fft_data_file+"' w l"

    # gnuplot のscript の保存 (ファイル名は basename + _fft.gp )
    f =open (gp_file, 'w')
    f.write(gp_script)
    f.close()

    cmd1 = 'gnuplot '+gp_file                  # gnuplotの実行コマンド
    cmd2 = 'open '+fft_data_eps                # pdf の表示

    # サブプロセス
    subprocess.call(cmd1.split())              # gnuplot gp_file.gp の実行

# option --silent (-s) の有無での分岐    --silent があると、pdf の表示をしない．
    if args.silent:
            print("")
            print('FFT(パワースペクトル)のデータを '+fft_data_file+' というファイル名で保存しました．(space 区切り)')
            print('FFT(パワースペクトル) のグラフを '+fft_data_eps+' というファイル名で保存しました．')
            print("")
            quit()
    else:
        subprocess.call(cmd2.split())  # cmd2="pdf の表示"
        print("")
        print('FFT(パワースペクトル)データを '+fft_data_file+' というファイル名で保存しました．(space 区切り)')
        print('FFT(パワースペクトル)のグラフを '+fft_data_eps+' というファイル名で保存しました．')
        print("")
        quit()
else:
# gnuplotを実行しないとき(fftのファイルは作成する):
    print("")
    print('FFT(パワースペクトル)データを '+fft_data_file+'というファイル名で保存しました．(space 区切り)')
    print('FFT(位相)データを '+phase_data_file+'というファイル名で保存しました．(space 区切り)')
    print("データをグラフ化したい場合は、gnuplot をお使いください．")
    print("--------------------------------------------------------")
    print("> gnuplot")
    print("> plot '"+fft_data_file+"' w l   パワースペクトル")
    print("> plot '"+phase_data_file+"' w l   位相")
    print("でグラフ化できます．")
    print("--------------------------------------------------------")
    print("または、-g (--gnuplot) オプションをつけて fft.py を実行するとグラフが表示されます．")
    print("")
    quit()
