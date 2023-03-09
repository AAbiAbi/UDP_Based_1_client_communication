import time

countdown = 3
i = 0
# countdown = 3
start_time = time.monotonic()

while True:
    # elapsed_time = time.monotonic() - start_time
    remaining_time = countdown - time.monotonic() + start_time
    i = 1
    if remaining_time <= 0:
        print("Time's up!")
        break
    # print(int(remaining_time))
print(i)
