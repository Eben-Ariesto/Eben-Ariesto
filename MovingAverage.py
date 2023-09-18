import random
random_list = []
for i in range(0,10):
    n = random.random() * random.randint(10, 100)
    random_list.append(n)
moving_average = []                             #list kosong untuk masukin hasil mvng avrg
window_size = 3                                 #jumlah data yg diitung tiap iterasi
i = 0
while i < len(random_list) - window_size + 1:
    temp = random_list[i : i + window_size]     #buat list sementara dari index i ke index i+wndw size-1
    temp_average = sum(temp) / window_size    #rata2 dari window tersebut
    moving_average.append(temp_average)       #diappend ke akhir list kosong
    i += 1
print(moving_average)