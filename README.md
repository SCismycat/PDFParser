# PDF解析器
## 代码说明
针对pdf数据进行解析，其中对pdf中的文字部分进行提取，对表格部分通过一定的规则识别表头，表头和内容拼接成文本格式，以空格进行分割；

## 使用方法
有两种使用方法，第一种使用Docker镜像，需要系统安装了Docker;第二种，假设已有了Python环境，可以通过直接执行代码或者通过脚本运行的方式进行使用。
### 方法1：使用Docker镜像
事先准备：
```
镜像已构建完成，需要安装Docker才能使用。
安装Docker，本Docker镜像是在windows上打的，如果存在不适配情况(例如需要在linux下使用)，可以自己打镜像。
1. 切换到Dockerfile所在的目录
2. 执行docker build -t pdfparser:v1.0 .
完成后，使用docker imgaes查看即可。
```
1. 加载镜像  
`docker load -i pdf-parser.tar`
2. 查看镜像  
`docker images `
如果出现pdf-parser:v1.5为正常；
3. 执行命令进行pdf解析  
`docker run -it -v E:/MyProject/data/:/work/data/ -v E:/MyProject/parser:/work/parser --rm pdfparser:v1.5 /work/data/ /work/parser/ all`
```
参数说明：
-v：第一个-v挂载的是待解析目录；第二个-v 加载的是解析完成后的输出目录；
--rm：后面跟的参数分别是pdfparser:v1.5(镜像名称)、/work/data/(刚刚挂载到镜像内数据目录)、/work/parser/(刚刚挂载到镜像内数据输出目录)、all(是全量处理还是增量处理，一般就是all)
```
```
4. 数据格式：
如：E:\MyProject\data是放数据的目录，E:\MyProject\data\a和E:\MyProject\data\b是放pdf的文件夹；  
则指定E:\MyProject\data，程序自动解析下面的子文件夹以及子文件夹下的pdf文件；
E:/MyProject/parser是解析后目录，所有解析后的excel全部放在该文件夹下。
```

### 方法2：基于已有的Python环境直接运行代码
事先准备：
```
安装Python环境，然后
pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
0. 直接使用代码；（不是很推荐）  
代码结构说明如下：  
src  
    -- main.py：主函数，代码直接run需要修改注释的函数；  
    -- PDFParser.py: 解析函数，对PDF进行解析；  
utils  
    -- CombineExcel.py: 合并所有的Excel，合并到一个大的CSV文件；（Excel有行数限制，因此转CSV）  

**参数说明：**  
+ origin_path: 待解析PDF路径，为文件夹路径，程序自动寻找后缀为.pdf的文档；（假设：/pdf/1、/pdf/2、/pdf/3三个目录下有若干）PDF文档，则origin_path=/pdf/）

+ writer_path: excel写出路径；(假设想把文件放在/data/下，则填/data/就行，程序会把一个子目录下的所有pdf解析成excel)

+ deal_mode: 处理模式；参数有“all”和“increment”；all表示全量，increment表示当解析终止或失败后，增量对未处理pdf进行进一步处理；  

2. 通过命令行执行；(比较推荐)
```
1. 假设origin_path,writer_path分别位于：E:/datas/和 E:/parsed/;
2. 打开cmd命令行，切换到 PDFParser/src/文件夹；
    2.1 直接执行 python main.py E:/datas/ E:/parsed/ all，（解释：main.py后面跟的参数分别是源路径，写出路径，和处理模式）
    2.2 等待程序处理完成即可
```
