import sys
import numpy as np
import multiprocessing

def calculate_row_sums(matrix, result, row_index):
    row_sum = np.sum(matrix[row_index])
    result.put((row_index, row_sum))

def main():

    if len(sys.argv) < 3:
        print("Использование: python parallel_matrix_sum.py <количество строк> <количество столбцов> <значение1> <значение2> ...")
        sys.exit(1)
        
    num_rows = int(sys.argv[1])
    num_cols = int(sys.argv[2])
    
    expected_num_elements = num_rows * num_cols
    if len(sys.argv) != 3 + expected_num_elements:
        print("Неверное количество элементов матрицы.")
        sys.exit(1)
        
    matrix_values = [int(sys.argv[i + 3]) for i in range(expected_num_elements)]

    matrix = np.array(matrix_values).reshape(num_rows, num_cols)

    result_queue = multiprocessing.Queue()

    processes = []
    for row_index in range(num_rows):
        process = multiprocessing.Process(target=calculate_row_sums, args=(matrix, result_queue, row_index))
        processes.append(process)
        process.start()
        
    for process in processes:
        process.join()

    row_sums = {}
    while not result_queue.empty():
        row_index, row_sum = result_queue.get()
        row_sums[row_index] = row_sum

    total_sum = sum(row_sums.values())

    for i, row_sum in row_sums.items():
        print(f"Сумма элементов в строке {i}: {row_sum}")

    print(f"Итоговая сумма элементов: {total_sum}")

if __name__ == "__main__":
    main()
