import math 

file = open("download_times_100", "r")
lines = file.readlines()
sum_download_times = 0
download_times = []
for line in lines:
    download_time = download_times.append(float(line.strip()))

average_download_time = sum(download_times) / len(download_times)
sum_of_squares = sum((x - average_download_time) ** 2 for x in download_times)
variance = sum_of_squares / len(download_times)
standard_deviation = math.sqrt(variance)
print(average_download_time, standard_deviation)
file.close()
