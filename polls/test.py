def solution(array, commands):
    answer = []
    
    for command in commands:
        i = command[0]-1
        j = command[1]
        k = command[2]-1
    
        arr = sorted(array[i:j], key = lambda x : x)
        print(arr)
        answer.append(arr[k])

    
    return answer

array = [1, 5, 2, 6, 3, 7, 4]
commands = [[2, 5, 3], [4, 4, 1], [1, 7, 3]]
a =solution(array,commands)
print(a)