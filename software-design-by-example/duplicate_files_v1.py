import os

def get_byte(filepath):
    # assuming filepath exists. 
    # Otherwise, we need to add some checks here
    with open(filepath, 'rb') as f:  
        # `rb` tells python to read as exact bytes
        content_bytes = f.read()
    
    return content_bytes


def find_duplicate(filepaths):
    # filepaths is list of filepaths
    out = []  # list of pairs that are equal
    n = len(filepaths) 
    for i in range(n-1):
        for j in range(i+1, n):
            file_i = filepaths[i]
            file_j = filepaths[j]
            if get_byte(file_i) == get_byte(file_j):
                out.append((file_i, file_j))

    return out


def test_find_duplicate():
    files_name_content = {
        'x.txt' : 'aaa',
        'y.txt' : 'aaa',
        'z.txt' : 'aaa',
        'u.txt' : 'bb',
        'v.txt' : 'bb',
        'w.txt' : 'c',
    }

    # Create files for testing
    for fname, content in files_name_content.items():
        with open(fname, 'w') as f:
            f.write(content)

    actual_out = find_duplicate(list(files_name_content.keys()))

    # Clean up: Delete the files
    for fname in files_name_content.keys():
        os.remove(fname)

    expected_out = [
        ('x.txt', 'y.txt'),
        ('y.txt', 'z.txt'),
        ('x.txt', 'z.txt'),
        ('u.txt', 'v.txt'),
    ]

    actual_out = [sorted(x) for x in actual_out]
    expected_out = [sorted(x) for x in expected_out]

    assert sorted(actual_out) == sorted(expected_out)


test_find_duplicate()