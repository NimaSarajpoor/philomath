# Software Design by Example

This is based on the book [Software Design by Example](https://third-bit.com/sdxpy/). Note that the goal here is not to cover all chapters but just the ones that are of my interest.

## Chapter 2: Objects and Classes

According to the book, object-oriented programming (OOP) was invented to solve two problems: <br>
* What is a natural way to represent real-world “things” in code?
* How can we organize code to make it easier to understand, test, and extend?


**I would like to add one more note here:** OOP is useful when the goal is to track something. For instance, when you want to track the number of available spots in a theatre as people register their seats.


### Example:
```{python}
class Shape:
    def __init__(self, name):
        self.name = name

    def perimeter(self):
        raise NotImplementedError("perimeter")

    def area(self):
        raise NotImplementedError("area")
```
