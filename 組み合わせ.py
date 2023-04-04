import numpy as np

arr = [3, 2, 4, 5, 4, 2]
arr = sorted(arr)
arr = np.array(arr)

print(arr)
print(np.sum(arr))


# 計10になるリストを2個作る
# max_elmを最初に指定する
max_elem = arr[-1]      # 最後のやつ
print(max_elem)

