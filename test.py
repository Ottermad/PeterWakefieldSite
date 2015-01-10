import os


def get_key(a_list):
    return a_list[1]

def listing():
    array1 = os.listdir("stories")
    array2 = []
    for item in array1:
        array2.append([item, os.path.getmtime("stories/" + item)])
    array3 = sorted(array2, key=get_key, reverse=True)
    return array3

print listing()
