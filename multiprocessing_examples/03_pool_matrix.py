"""
Перемножение матриц с использованием Pool (пула процессов).
"""

import time
import os
from multiprocessing import Pool


def element(i, j, A, B):
    """Вычисляет элемент C[i][j]."""
    N = len(A[0])
    res = 0
    for k in range(N):
        res += A[i][k] * B[k][j]
    return (i, j, res)


# Генерация матриц побольше для наглядности
SIZE = 50

matrix_a = [[(i + j) % 10 for j in range(SIZE)] for i in range(SIZE)]
matrix_b = [[(i * j) % 10 for j in range(SIZE)] for i in range(SIZE)]


def sequential_multiply(A, B):
    """Последовательное перемножение."""
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            _, _, val = element(i, j, A, B)
            result[i][j] = val
    return result


def pool_multiply(A, B, num_processes):
    """Параллельное перемножение через Pool (TODO 3)."""
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for _ in range(rows)]

    # TODO 3: РЕШЕНО!
    # 1. Список аргументов для каждого элемента
    args = [(i, j, A, B) for i in range(rows) for j in range(cols)]
    
    # 2. Pool + starmap
    with Pool(processes=num_processes) as pool:
        results_list = pool.starmap(element, args)
    
    # 3. Заполняем результат
    for i_pos, j_pos, val in results_list:
        result[i_pos][j_pos] = val

    return result


if __name__ == '__main__':
    cpu_count = os.cpu_count()
    print(f"Размер матриц: {SIZE}x{SIZE}")
    print(f"Доступно ядер CPU: {cpu_count}\n")

    # Последовательное вычисление
    t = time.time()
    seq_result = sequential_multiply(matrix_a, matrix_b)
    time_seq = time.time() - t
    print(f"Последовательно: {time_seq:.4f} сек")

    # TODO 4: РЕШЕНО!
    print("\n=== ТЕСТ ПУЛА ПРОЦЕССОВ ===")
    for n in [1, 2, 4, cpu_count]:
        t = time.time()
        par_result = pool_multiply(matrix_a, matrix_b, n)
        elapsed = time.time() - t
        speedup = time_seq / elapsed
        print(f"Pool ({n} процессов): {elapsed:.4f} сек (ускорение {speedup:.1f}x)")
        
        # Проверка корректности
        if par_result == seq_result:
            print("  ✓ Результаты совпадают")
        else:
            print("  ✗ ОШИБКА: результаты НЕ совпадают!")
        print()
