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

    
