以下將介紹各資料的資訊 <br>
time_result.py --> 將四個時間類別(DATE、TIME、SET、DURATION)進行標準化，並產生processed_data.csv <br>
time_info.py --> 將answer.txt的四個時間類別特別拉出來，並放到extracted_data.csv裡面 <br>
comparison.py --> 將官方提供的(answer.txt)時間類別答案，與利用rule-based所產生的答案進行比較，不一樣的答案會輸出到mismatched_data.csv裡 <br>
<br>
answer.txt --> 官方提供的標準化後的答案 <br>
extracted_data.csv --> 裡面資料包含PHI(DATE、TIME、SET、DURATION)、原始文檔、官方提供的標準化答案 <br>
processed_data.csv --> 執行time_result.py後，會產生這個檔案，裡面結合extracted.csv及執行time_result.py標準化後的時間 <br>
mismatched_data.csv --> 利用processed_data.csv，比較官方提供的(answer.txt)時間類別答案，與利用rule-based所產生的答案，不一樣的答案可以在這看到
