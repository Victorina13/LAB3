import json


def quick_sort(data,key):
    if len(data) < 2:
        return
    start_end = [[0, len(data) - 1]]
    while len(start_end) > 0:
        start, end = start_end.pop()
        pivot = data[(start + end) // 2]
        i = start - 1
        j = end + 1
        while True:
            while True:
                i = i + 1
                if pivot[key] <= data[i][key]:
                    break
            while True:
                j = j - 1
                if data[j][key] <= pivot[key]:
                    break
            if i >= j:
                break
            data[i], data[j] = data[j], data[i]
        if start < j:
            start_end.append([start, j])
        j = j + 1
        if j < end:
            start_end.append([j, end])


data = json.load(open("result.txt", encoding="windows-1251"))
quick_sort(data,'weight')

json.dump(data, open("result_sort.json", "w", encoding="windows-1251"), ensure_ascii=False, indent=5)
result = json.load(open("result_sort.json", encoding="windows-1251"))
print(result)
