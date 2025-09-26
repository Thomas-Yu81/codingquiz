#reverse_list
def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    count = 0
    for _ in l:
        count += 1 

    right = count - 1
    left = 0
    reverse_list = l

    while left < right:
        temp = reverse_list[left]
        reverse_list[left] = reverse_list[right]
        reverse_list[right] = temp
        left += 1
        right -= 1
    return reverse_list

def reverse_list_comparation(l: list):
    
    length = 0
    reverse_list_comparation = []
    for _ in l:
        length += 1 
    i = 0
    while i < length:
        #reverse_list_comparation.append(l[length - 1 - i])
        reverse_list_comparation[length - 1 - i] = l[i]
        i += 1
    return reverse_list_comparation

def test_reverse_list():
    test_cases = [
        [1, 2, 3, 4, 5],
        ['a', 'b', 'c', 'd'],
        [1, 'hello', 3.14, True],
        [42],
        []
    ]
    for test in test_cases:
            assert reverse_list(test) == reverse_list_comparation(test)

    

#sudoku
def solve_sudoku(matrix):
    candidates = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(set(range(1, 10)))
        candidates.append(row)

    for i in range(9):
        for j in range(9):
            if matrix[i][j] != 0:
                candidates[i][j] = set()
                update_candidates(matrix, candidates, i, j, matrix[i][j])

    changed = True
    while changed:
        changed = False
        for i in range(9):
            for j in range(9):
                if matrix[i][j] == 0 and len(candidates[i][j]) == 1:
                    num = candidates[i][j].pop()
                    matrix[i][j] = num
                    update_candidates(matrix, candidates, i, j, num)
                    changed = True

    if not is_complete(matrix):
        min_len = 10
        pos = None
        for i in range(9):
            for j in range(9):
                if matrix[i][j] == 0 and 0 < len(candidates[i][j]) < min_len:
                    min_len = len(candidates[i][j])
                    pos = (i, j)
        if pos:
            i, j = pos
            for num in list(candidates[i][j]):
                new_matrix = [row[:] for row in matrix]
                new_matrix[i][j] = num
                if solve_sudoku(new_matrix):
                    for r in range(9):
                        for c in range(9):
                            matrix[r][c] = new_matrix[r][c]
                    return True
            return False
        else:
            return False

    return True


def update_candidates(mat, candidates, row, col, num):
    for j in range(9):
        if num in candidates[row][j]:
            candidates_set = candidates[row][j]
            candidates_set.remove(num)
            
    for i in range(9):
        if num in candidates[i][col]:
            candidates[i][col].remove(num)

    sr = row // 3
    sr = sr * 3
    sc = col // 3
    sc = sc * 3

    for i in range(sr, sr + 3):
        for j in range(sc, sc + 3):
            if num in candidates[i][j]:
                candidates[i][j].remove(num)


def is_complete(mat):
    for row in mat:
        if 0 in row:
            return False
    return True


if __name__ == "__main__":
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    if solve_sudoku(board):
        print("solved")
        for row in board:
            print(row)
    else:
        print("failed")