# Software Design by Example

This is based on the book [Software Design by Example](https://third-bit.com/sdxpy/). Note that the goal here is not to cover all chapters but just the ones that are of my interest.

### Objects and Classes

According to the book, object-oriented programming (OOP) was invented to solve two problems: <br>
* What is a natural way to represent real-world “things” in code?
* How can we organize code to make it easier to understand, test, and extend?


**I would like to add one more note here:** OOP is useful when the goal is to track something. For instance, when you want to track the number of available spots in a theatre as people register their seats.


```python
class Shape:
    def __init__(self, name):
        self.name = name

    def perimeter(self):
        raise NotImplementedError("perimeter")

    def area(self):
        raise NotImplementedError("area")
```


**Note:**<br>
A specification like this is sometimes called a "contract" because an object must satisfy it in order to be considered a shape, i.e., must provide methods with these names that do what those names suggest. For example, we can derive classes from Shape to represent squares and circles.

```python
class Square(shape):  # inheritence
    def __init__(self, name, side_length):
        super().__init__(name)
        self.side_length = side_length

    def perimeter(self):
        return 4 * self.side_length

    def area(self):
        return self.side_length ** 2
```


### args and kwargs

```python
def show_arguments(title, *args, **kwargs):
    print("type of args: ", type(args))
    print("type of kwargs: ", type(kwargs))

    print(f"{title} args '{args}' and kwargs '{kwargs}'")
```

Let's call `show_arguments('example', 1, 'a', x='b', y=0)`. This should gives:

```
type of args:  <class 'tuple'>
type of kwargs:  <class 'dict'>
example args '(1, 'a')' and kwargs '{'x': 'b', 'y': 0}'
```

Note that we did not specify any particular parameter. We just allow the function to get several arguments and kwargs as needed. This mechanism is called `varargs`. So, when is this useful? Suppose that you want to write a wrapper for several functions. We do not want to create different wrapper with different signature. We can just have one `function wrapper` that takes the function `f`, and the required argument and keyword aeguments, and then call the function. 

```python
def call_func(f, *args, **kwargs):
    return f(*args, **kwargs)  
    # Here we use the complementary mechanism known as `spreading`
```

### type vs isinstance
One of them can check if a object is subclass of a class. Let's check it with the following example:

```python
class dummy_class(list):
    pass

d = dummy_class()
print(type(d))  # <class '__main__.dummy_class'>
print('=' * 50) 
print(isinstance(d, list))  # True
```

* `type` reports the most specific type of an object
* `isinstance` determines whether an object inherits from a type either directly or indirectly. 


### Finding duplicate files

Let's start with a naive implementation. For `N` files, we need to check all pairs one by one, and see if any two files are equal or not. `Choose(N, 2)` gives $\frac{N(N-1)}{2}$. Let's implement it.

```python 
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
```

Let's test it. For that, we can create some files and put some values in those files, and then see if the function
can detect the duplicates. We also do not want to leave any unnecessary files after the testing. So, make sure to remove the files that were created for the sake of testing. See `duplicate_files_v1.py`.

How can we do better? We can add an intermediate step in which the hash value of each file's content is computed. After grouping files according to their corresponding hash values, we know that:
* A file from one group is definitely not duplicate of a file from another group because their hash is different.
* For any two files in one group, their content might be equal.

This means that we can narrow down our seach by exploring files in each group. So, if we have `g` groups, then the time complexity becomes `O(N^2/g)`. See `duplicate_files_v2.py`.

How can we enhance the second bullet point above? In other words, how can we create groups via hash that contains exactly-identical files? What we are asking here is basically related to having a hash function with (almost) no collision. We can use `cryptographic hash function`. 

**Note:** `Cryptographic Hash Function (CHF)` is a hash algorithm (a map of an arbitrary binary string to a binary string with a fixed size of `n` bits) that has special properties desirable for a cryptographic application.

**Note:** finding any pair of different messages that yield the same hash value (a collision) is also infeasible: a cryptographic hash is expected to have a collision resistance strength of `n/2 bits` (lower due to the birthday paradox).

**Note:** With use of CHF, we can use the "You Look Only Once" as we only need need to get hash of each file once, and that's it. Since we do not have collision, we know that all files in a group have identical content. So, the time complexity is `O(N)`. 