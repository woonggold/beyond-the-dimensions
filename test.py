import multiprocessing
import time

def intensive_task():
    # 무거운 계산 작업을 반복하여 CPU를 많이 사용하게 함
    while True:
        result = 0
        for i in range(1000000):
            result += i ** 2

if __name__ == "__main__":
    # 시스템의 CPU 코어 수를 가져옴
    num_cores = multiprocessing.cpu_count()

    # 각 코어에 프로세스를 하나씩 할당
    processes = []
    for _ in range(num_cores):
        process = multiprocessing.Process(target=intensive_task)
        processes.append(process)
        process.start()

    # 프로세스가 잘 동작하고 있는지 확인을 위해 잠시 대기
    time.sleep(10)

    # 프로세스 중지
    for process in processes:
        process.terminate()

    for process in processes:
        process.join()

    print("All processes have been terminated.")
