import math

file = open("download_times", "r")
lines = file.readlines()
file.close()

qsize_20 = lines[:3]
qsize_100 = lines[-3:]

first_three_times = [float(line.strip()) for line in qsize_20]
last_three_times = [float(line.strip()) for line in qsize_100]

def calculate_statistics(times):
    average_time = sum(times) / len(times)
    sum_of_squares = sum((x - average_time) ** 2 for x in times)
    variance = sum_of_squares / len(times)
    standard_deviation = math.sqrt(variance)
    return average_time, standard_deviation

average_first_three, stddev_first_three = calculate_statistics(first_three_times)
average_last_three, stddev_last_three = calculate_statistics(last_three_times)

print("20 packages - Average:", average_first_three, "Standard Deviation:", stddev_first_three)
print("100 packages - Average:", average_last_three, "Standard Deviation:", stddev_last_three)