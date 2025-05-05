# 操作步骤
0. 1.繁体转简体.py
  ```
  detected_texts_output.txt,这个文件是pic1这个目录的最后结果，
  把它转换成简体
  detected_texts_output_simplified.txt
  ```

0. 2.2.全部文字块.路径.py
  ```
  这是把上面的简体文本，分为图片路径，还有图片中的文字两部分。
  结果放在：extracted_file_path_and_all_text_blocks.txt
  ```

0. 3.sutra-name-list.txt
  ```
  这个是从网页转换过来的“标准”文本。
  ```

0. 4.1.8.阿里三改.py
  ```
  这个是识别到的图片中的文本，和标准文本进行比较。
  比较结果在：comparison_result_with_sliding_window_levels.txt
  ```

0. 5.2.html格式.py
  ```
  这个是把上面的比较结果转换为html格式
  comparison_result_with_sliding_window_levels.html
  ```
# 不足之处
0. 还有封面没有被检测出来。有的封面的文字太模糊，没有被检测到。
0. 匹配的时候，全匹配/窗口匹配，还有模糊匹配为进行。
0. 最好封面都找出来后，再尝试模糊匹配。
0. 所以最好再新开一个目录pic2。封面的检测，可以用封面后面的那个图片来进行。这个是个强的稳定的被检测标志。 
