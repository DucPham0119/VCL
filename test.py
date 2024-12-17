import numpy as np

# Tạo một mảng ngẫu nhiên để minh họa
arr = np.array([95,46,25,87,37, 28, 31, 21, 69, 47, 53, 48, 43, 97, 46, 74, 19, 32, 98, 54, 34,  9, 23, 63, 73,
                47, 30, 75, 39, 98, 77, 36, 84, 67, 21, 81, 10, 33, 96, 70, 44, 51, 82, 55, 10, 68, 59, 35,
                74, 84])
print(arr)

# Lấy chỉ số của các phần tử theo thứ tự giảm dần
sorted_indices = np.argsort(arr)[::-1]

# Chọn 10 phần tử đầu tiên
top_10_indices = sorted_indices[:10]
print(top_10_indices)

# In ra giá trị và vị trí của 10 phần tử lớn nhất
for i, index in enumerate(top_10_indices, 1):
    print(f"Phần tử lớn nhất thứ {i}: Giá trị = {arr[index]}, Vị trí = {index}")
