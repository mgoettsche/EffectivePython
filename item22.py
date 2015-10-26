# Item 22: Prefer Helper Classes Over Bookkeeping with Dictionaries and Tuples
import collections

# The built-in dictionary type is well-suited for maintaining dynamic state. Suppose e.g. you want to store the grades
# of students who are not known in advance. Using a dictionary encapsulated in a gradebook class this can be done
# easily:
class SimpleGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 80)
book.report_grade('Isaac Newton', 50)
book.report_grade('Isaac Newton', 90)
print(book.average_grade('Isaac Newton'))

# 73.33333333333333

# Suppose now you don't want to store by name only, but also distinguish by subject. This can still fairly easily
# be done by nesting dictionaries:
class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = {}

    def report_grade(self, name, subject, score):
        by_subject = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(score)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book = BySubjectGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)
print(book.average_grade('Albert Einstein'))

# 81.25

# Now suppose you have one further requirement, you now also want to track the weight of each score towards the overall
# grade. This could be achieved by storing (score, weight) tuples instead. We omit this code here, what is important is
# that the more complex the data you want to keep track of is, the more complicated it gets to realize it using a simple
# bookkeeping dictionary and further levels of nesting reduce readability.
# When you realize that the task is too complex for the bookkeeping approach, it should be broken up into classes.
# This increases encapsulation and provides a layer of abstraction between interfaces and implementation.

# Refactoring to Classes
# Refactoring can be done bottom-up. For a grade a class seems too heavyweight, but a namedtuple lets you define
# tiny, immutable data classes, e.g:
Grade = collections.namedtuple('Grade', ('score', 'weight'))

# namedtuples can be constructed with both, positional and keyword arguments. There are two limitations to be beware
# of: 1. Default values cannot be specified. This may work well for a small number of properties, but be problematic
# for a larger number.
#     2. The properties are still available via their numerical index. This can cause problems with externalized APIs,
#        because any changes you introduce may break such external usages.

# Using this newly defined Grade namedtuple a class for subjects can be created like this:
class Subject(object):
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

# Next, we need a class that represents a student:
class Student(object):
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if not name in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

# Finally, we need a gradebook class:
class Gradebook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        if not name in self._students:
            self._students[name] = Student()
        return self._students[name]

# The class-based implementation is almost twice as long as the previous, but it is much easier to read and so is the
# usage example:
book = Gradebook()
albert = book.student('Albert Einstein')
math = albert.subject('Math')
math.report_grade(80, 0.10)
math.report_grade(90, 0.15)
math.report_grade(85, 0.10)
print(albert.average_grade())

# 85.71428571428572

# The API is incompatible with that of the dictionary-based implementation, but if needed it is possible to write
# backwards-compatible ones.
