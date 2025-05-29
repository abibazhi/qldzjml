# 操作过程
0. (qldzj3) jm@X2024:~/dev/qldzjocr/pic1$ python 1.h.all.3.5.通过.豆包.断点续传.py
  ```
  这个命令会遍历所有qldzj图片
  然后输出所有潜在的封面图片
  保存到black_background_results.txt这个文件中。 
  ```
0. (qldzj3) jm@X2024:~/dev/qldzjocr/pic1$ python 1.i.9.3.阿里.输出图片.存子目录.辅助检测.py^C
  ```
  这个命令会检查black_background_results.txt中的图片
  把不是封面的进一步筛选掉。
  结果在selected_images这个目录中。
  ```
0. (qldzj3) jm@X2024:~/dev/qldzjocr/pic1$ python 3.1.2.检测封面文字.改为黑白.文件排序.py
  ```
  这个命令把封面中的文字都解析出来。
  至此，pic1就是从图片中找封面，就结束了。
  ```

0. 最后输出是detected_texts_output.txt
