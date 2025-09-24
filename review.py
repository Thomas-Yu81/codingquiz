# Review 1
""" this function has an issue with mutable default argument

def add_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list
"""
def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)
    return my_list

value = 10
my_list = [2, 2, 2]
print(add_to_list(value, my_list))  


# Review 2
""" this function has 2 issues with string formatting and coding standards.

def format_greeting(name, age):
    return "Hello, my name is {name} and I am {age} years old."

issue 1: it maybe need to use f strings
issue 2: usually use string + variabel
"""
def format_greeting(name, age):
    # return f"Hello, my name is {name} and I am {age} years old."
    return "Hello, my name is " + name + " and I am " + str(age) + " years old."

print(format_greeting("Will", 46))

# Review 3
""" this class has an issue with class variable vs instance variable

class Counter:
    count = 0
    def __init__(self):
        self.count += 1
    def get_count(self):
        return self.count
issue: counter should use class variable to count the number of instances
"""
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1
    def get_count(self):
        return Counter.count

c1 = Counter()
print(c1.get_count()) # Counter result is 1
c2 = Counter()
print(c2.get_count()) # Counter result is 2
c3 = Counter()
print(c3.get_count()) # Counter result is 3

# Review 4
""" this function has an issue with thread safety
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

issue: the increment method is not thread safe.
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

print(counter.count)  # 10000

# Review 5
""" this function has an issue with counting occurrences of elements in a list
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] =+ 1
        else:
            counts[item] = 1
    return counts
issue: it may be the typo, the operator should be += instead of =+
"""
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

print(count_occurrences(['aaaa', 'bbbb', 'aaa', 'a', 'aaaa', 'bbbb'])) 
# {'aaaa': 2, 'bbbb': 2, 'aaa': 1, 'a': 1}
