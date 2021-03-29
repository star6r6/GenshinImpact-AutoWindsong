#GenshinImpact-AutoWindsong

# 配置环境
安装python后，打开命令行，输入下面命令并回车

pip install pyautogui
# 使用方式
使用管理员权限打开命令行，输入下面命令（文件所在路径请``自行更改）并回车，然后切到原神并打开琴键保持，可以切回命令行再使用Ctrl+C中断

python D:\AutoWindsong\Qianbenying.py
# 乐谱翻译指南
前面加L = Low 代表低音

前面加H = High 代表高音

什么都不加代表中音

'L6 3' 为一个低音6(La)音符，时值为3拍（不填默认为1拍，如'L6'）

['L2 4', '4 4'] 中括号内的为同时演奏多个音符，前面标识同时按下低音2(Re)和中音4(Fa)，时值为4拍

各个音符间用英文逗号分隔