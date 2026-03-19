"""
Перемножение матриц с использованием multiprocessing.Process и Queue.
"""

import time
from multiprocessing import Process, Queue


def element(index, A, B):
    """Вычисляет один элемент произведения матриц A * B."""
    i, j = index
    res = 0
    N = len(A[0])
    for k in range(N):
        res += A[i][k] * B[k][j]
    return res


def element_to_queue(index, A, B, q):
    """Обёртка над element(), записывающая результат в Queue."""
    result = element(index, A, B)
    q.put((index, result))


# Исходные матрицы (3x3)
matrix_a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

matrix_b = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1],
]


def sequential_multiply(A, B):
    """Последовательное перемножение матриц (для сравнения)."""
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = element((i, j), A, B)
    return result


def parallel_multiply(A, B):
    """Параллельное перемножение матриц: один процесс на каждый элемент."""
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for _ in range(rows)]

    # TODO 1: РЕШЕНО!
    q = Queue()
    processes = []

    # Создаём процесс ДЛЯ КАЖДОГО элемента (i,j)
    for i in range(rows):
        for j in range(cols):
            p = Process(target=element_to_queue, args=((i, j), A, B, q))
            processes.append(p)

    # Запускаем ВСЕ процессы
    for p in processes:
        p.start()

    # Ждём завершения ВСЕХ процессов
    for p in processes:
        p.join()

    # Собираем результаты из очереди
    results_dict = {}
    for _ in range(rows * cols):
        idx, value = q.get()
        results_dict[idx] = value

    # Заполняем результирующую матрицу
    for i in range(rows):
        for j in range(cols):
            result[i][j] = results_dict[(i, j)]

    return result


if __name__ == '__main__':
    print("Матрица A:")
    for row in matrix_a:
        print(f"  {row}")
    print("Матрица B:")
    for row in matrix_b:
        print(f"  {row}")
    print()

    # Последовательное вычисление (TODO 2)
    print("=== ПОСЛЕДОВАТЕЛЬНО ===")
    t1 = time.time()
    result_seq = sequential_multiply(matrix_a, matrix_b)
    time_seq = time.time() - t1

    print("Результат (последовательно):")
    for row in result_seq:
        print(f"  {row}")
    print(f"Время: {time_seq:.6f} сек")
    print()

    # Параллельное вычисление (TODO 2)
    print("=== ПАРАЛЛЕЛЬНО ===")
    t2 = time.time()
    result_par = parallel_multiply(matrix_a, matrix_b)
    time_par = time.time() - t2

    print("Результат (параллельно):")
    for row in result_par:
        print(f"  {row}")
    print(f"Время: {time_par:.6f} сек")
    print()
    print(f"Ускорение: {time_seq / time_par:.2f}x")
