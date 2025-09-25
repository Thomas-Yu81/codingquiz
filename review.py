# Review 1
""" 
this function has an issue with mutable default argument

def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

print(add_to_list(5))
print(add_to_list(6))

the result is:
[5]
[5, 6]

issue: my_list is mutable, can not use default [] as paramter, it should be None and then initialize inside the function. 
        default [] is created only once, when the function is defined, rather than creating a new instance each time the function is called. 
        so all calls to add_to_list which don't provide my_list will share the same list object, it will cause an unexpected accumulation of values.
"""
def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list

value = 10
my_list = [2, 2, 2]

# my_list is [2, 2, 2, 10]
print(add_to_list(value, my_list))

# my_list is [2, 2, 2, 10, 3]
print(add_to_list(3, my_list))

# my_list is [2, 2, 2, 10, 3, 4]
print(add_to_list(4, my_list))

# my_list is [5]
print(add_to_list(5))

# my_list is [6]
print(add_to_list(6))


# Review 2
""" 
this function has 2 issues with string formatting and coding standards.

def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."

print(format_greeting("Will", 46))

the result is:
Hello, my name is {name} and I am {age} years old.

issue 1: string formatting issue, it maybe need to use f strings
issue 2: for very simple, static string combinations, usually use string + variabel
"""
def format_greeting(name, age):
    # return f"Hello, my name is {name} and I am {age} years old."
    return "Hello, my name is " + name + " and I am " + str(age) + " years old."

print(format_greeting("Will", 46))

# Review 3
""" 
this class has an issue with class variable vs instance variable

class Counter:
    count = 0
    def __init__(self):
        self.count += 1
    def get_count(self):
        return self.count


c1 = Counter()
print(c1.get_count()) 

c2 = Counter()
print(c2.get_count()) 

c3 = Counter()
print(c3.get_count())   
the result is:
1
1
1

issue: the counter cannot continue counting through multiple calls, 
        counter should use class variable to count the number of instances
"""

class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
    def get_count(self):
        return Counter.count

# Counter result is 1
c1 = Counter()
print(c1.get_count()) 

# Counter result is 2
c2 = Counter()
print(c2.get_count()) 

# Counter result is 3
c3 = Counter()
print(c3.get_count()) 


# Review 4
""" 
this function has an issue with thread safety

import threading
class SafeCounter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
 
def worker(counter):
    for _ in range(1000):
        counter.increment()
 
counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)
 
for t in threads:
    t.join()

print(counter.count)
the result may be less than 10000.

issue: when multiple threads are running, they may all read the same old value, and then increment it, the result will be less than expected.
        use threading.Lock to ensure that only one thread can modify the count at a time.
"""
import threading
class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    def increment(self):
        with self.lock:
            self.count += 1
def worker(counter):
    for _ in range(1000):
        counter.increment()

counter = SafeCounter()
threads = []
for _ in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(counter.count)

# Review 5
""" this function has an issue with operator
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] =+ 1
        else:
            counts[item] = 1
    return counts

print(count_occurrences(['aaaa', 'bbbb', 'aaa', 'a', 'aaaa', 'bbbb']))
the result is:
{'aaaa': 1, 'bbbb': 1, 'aaa': 1, 'a': 1}

issue: it may be the typo, the operator should be += , not =+
"""
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

# {'aaaa': 2, 'bbbb': 2, 'aaa': 1, 'a': 1}
print(count_occurrences(['aaaa', 'bbbb', 'aaa', 'a', 'aaaa', 'bbbb'])) 

