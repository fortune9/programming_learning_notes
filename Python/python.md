Python learning notes
================
Zhenguo Zhang
July 16, 2023

-   [Variables](#variables)
    -   [False values](#false-values)
-   [Functions](#functions)
-   [Classes](#classes)
-   [Packages](#packages)
-   [Modules](#modules)
-   [Code testing](#code-testing)
    -   [Manual and automatic testing](#manual-and-automatic-testing)
    -   [Testing modules](#testing-modules)
-   [Formatting](#formatting)
    -   [PEP8 guideline summary](#pep8-guideline-summary)
    -   [flake8 configuration](#flake8-configuration)
    -   [Static type hinting](#static-type-hinting)
    -   [Docstrings](#docstrings)
-   [Performance test](#performance-test)
-   [Some useful modules and
    packages](#some-useful-modules-and-packages)
-   [Similarity between Python and other
    languages](#similarity-between-python-and-other-languages)
    -   [Perl](#perl)
    -   [R](#r)

## Variables

### False values

-   Empty list/string/tuple: Empty list/string/tuple are all false in
    ‘if’ test, so no need to test length

## Functions

## Classes

## Packages

## Modules

In python, there are different terms to describe files, here is a
summary.

| Name    | Description                                                                                                                   |
|---------|:------------------------------------------------------------------------------------------------------------------------------|
| script  | a single file runnable, it contains code outside the scope of functions and classes.                                          |
| module  | a file intended to be imported and defines members like classes, functions, and variables intended to be used in other files. |
| package | a collection of modules/subpackages in a folder, which needs **init**.py                                                      |
| library | this is a loose term referring any packages or collection of packages, such as python standard library.                       |

## Code testing

### Manual and automatic testing

There are manual and automatic testings. To automate testing, one can
choose from CI/CD tools, including Travis CI, Travis CI service is
available free for all public github repositories, one can activate it
by login to its website and authenticate with your github/gitlab
credentials, and then create a .travis.yml file in the repository, like:

``` yaml
language: python
python:
  - "2.7"
  - "3.7"
install:
  - pip install -r requirements.txt # required packages
script:
  - python -m unittest discover
```

### Testing modules

One can use the “assert a==b” statement to test a function, and can also
use the modules like unittest, nose, nose2, and pytest to test. To use
these modules, the code has requirements, summarized as follows:

| module   | requirements                                                                                                               | implementation                                                                                                                                                                                                                          |
|----------|:---------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| unittest | 1\. put tests into a class as methods, 2. use the assertion methods from unittest.TestCase class instead of builtin assert | create a new class inheriting from unittest.TestCase, and then add methods to run tests. use unittest.main() to run the tests. One can also use ‘python –m unittest discover –s tests’ to test all test\*.py files in the folder tests. |
| nose2    | the test script files need to be importable modules                                                                        | when running “python –m nose2” it runs tests on all test\*.py files in current folder.                                                                                                                                                  |
| pytest   | have test functions’ names start with “test\_”                                                                             | pytest support buitlin ‘assert’ and resume from where failed, also many plugins to extend functionality.                                                                                                                                |

## Formatting

PEP8 is a guide for writing python code, defined in 2001, to increase
the readability of code. There are two types of tools to enforce PEP8
compliance, linters and autoformatters. linters can check code for
compliance to PEP8 and flag errors. One of them is flake8, which will
provide comments/suggestions on the code. Autoformatter directly change
your code directly to comply with PEP8, and one of them is black. For
more on PEP8, here is a good tutorial:
<https://realpython.com/python-pep8/>.

One can install editor extensions to help format code to comply with
PEP8. The vim plugin is at <https://github.com/nvie/vim-flake8>.

One can use the following strategy to automate python code linting: (1)
set a git pre-commit hook (<https://pre-commit.com/>, written in python,
but having hooks for other languages too), so it will be triggered every
time when code changes,
<https://dev.to/m1yag1/how-to-setup-your-project-with-pre-commit-black-and-flake8-183k>
(flake8 hook is at
<https://flake8.pycqa.org/en/latest/user/using-hooks.html>); (2) set
github actions so that it is triggered when push/pull requests (or any
defined actions) occur, see
<https://dev.to/ricardochaves/python-lint-with-github-actions-2i7p>.

To add pre-commit hooks (isort, black, and flake8), one need the
following steps: (1) install pre-commit package and add ‘pre-commit’ to
“requirements.txt”, for python project only, (2) create
.pre-commit-config.yaml (put at the root of git repo) and add hooks into
it; this file defines repos where hooks can be downloaded and high-level
options (see <https://pre-commit.com/#plugins> for more details on
option specifications), (3) run ‘pre-commit install’ to install git
hooks to .git folder. (4) if this is setup for existing repo, one can
run ‘pre-commit run –all-files’ to format existing all files. Now it is
all set, and when every time ‘git commit’ is run, the hooks would be
triggered, black formats code, and flake8 checks it, if anything
changes, the commit will fail and for you to review the changes by
black, and then you can modify code and re-commit, until no more errors.
Normally, these hooks will not prevent creating a commit, but to enforce
it, one can run ‘git config –bool flake8.strict true’ to set the
variable ‘flake8.strict’ to true, and in this way, flake8 needs be
strictly followed. Also, one can create their own hooks by following
instructions at <https://pre-commit.com/#new-hooks>.

To have all git repos install pre-commit hooks automatically, one can
run the following command:

``` bash
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir ~/.git-template
#pre-commit installed at ~/.git-template/hooks/pre-commit
```

And from now on, every time clone or init a repo, the pre-commit hook is
installed there automatically. Otherwise, one need run “pre-commit
install” to install hooks manually.

### PEP8 guideline summary

Nomenclature

| Object                             | Recommendation                                                           | Example                   |
|------------------------------------|:-------------------------------------------------------------------------|:--------------------------|
| Function, variable, method, module | Use lowercase words separated by underscores                             | x, my\_fun, my\_module.py |
| class                              | CamelCase: each word starts with capital letter and don’t use underscore | MyClass                   |
| package                            | Use short lowercase words, but not separated by underscore               | mypackage                 |

Layout

| Object                                        | Recommendation                                                                                                                                                                                                                                                  | Example            |
|-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------|
| Top class, function                           | Two blank lines before them                                                                                                                                                                                                                                     |                    |
| Method in a class                             | One blank line before them                                                                                                                                                                                                                                      |                    |
| within function                               | Use blank lines to separate main steps                                                                                                                                                                                                                          |                    |
| max line length                               | 79 characters. For multiple line code, one can put code in parenthesis, brackets, or braces, or use backslash  to connect lines. For a long string, one can make it by connecting multiple string segments with ‘’ or ‘+’, or use () to enclose multiple lines. |                    |
| indentation                                   | 4 consecutive spaces preferred over tab. For line continuation, one can use ‘hanging indent’ or ‘extra indent’ (align to open delimiter) to improve readability.                                                                                                |                    |
| closing brace                                 | Align with first non-white character of previous line, or the first character of the construct.                                                                                                                                                                 |                    |
| comments                                      | Start with ‘\#’ (a space here), using complete sentence with first letter capitalized. Use inline comments sparingly unless necessary                                                                                                                           |                    |
| docstrings                                    | Enclosed in triple double/single quotes, writing for public modules, functions, methods, classes. Put ending quotes on a single line itself, except for oneline docscript, which should all be in one line.                                                     |                    |
| Binary operators such as =, &lt;=, or, is, in | Add one white space on each side, but no space when assigning default value in function definition. Also add space to lowest operator only, e.g., \* vs +                                                                                                       | z = (x+y) \* (x-y) |

### flake8 configuration

One can put parameters in a flake8 configuration file, and in this way,
one doesn’t need to specify the same parameters many times. Flake8 looks
for configurations in the following places: setup.cfg, tox.ini, .flake8
in the project directory, and \~/.config/flake8 in user space, note that
the former has higher precedence, and command line parameters have even
higher precedence. The config files follow the INI format, starting with
\[flake8\] for the section, and command line parameters can be used in
config in either way: use underscore to replace hyphen, or simply remove
leading hyphens. Also note that flake8 doesn’t support inline comments.
An example flake8 configuration is like this:

``` config
[flake8]
ignore = D203
exclude =
    # No need to traverse our git directory
    .git,
    # There's no value in checking cache directories
    __pycache__,
    # The conf file is mostly autogenerated, ignore it
    docs/source/conf.py,
    # The old directory contains Flake8 2.0
    old,
    # This contains our built documentation
    build,
    # This contains builds of flake8 that we don't want to check
    dist
max-complexity = 10
```

### Static type hinting

One can use the static type hinting format in function definition, such
as

``` python
def myfun(a: str, b: bool=True) -> str:
```

In this way, it tells what kinds of inputs and returns are expected for
a function. To use type built-in data structure (List, Set, Dict, Tuple,
Optional, callable, interators, unions), we can use typing package. For
more advanced usage of types, including creating new types, like
structures in C, one can see the module typing at
<https://docs.python.org/3/library/typing.html>. One tutorial on the
topic is at
<https://medium.com/depurr/python-type-hinting-a7afe4a5637e>. One can
also use mypy (from mypy package) to check whether a script is correct
in static typing.

**Type hints summary**

| Arguments typing                           | Explanation                                                                                                  |
|--------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| Def greeting() -&gt; None:                 | No return value for a function                                                                               |
| \*args: int                                | args is a tuple of ints                                                                                      |
| \*kwargs: float                            | Kwargs is Dict\[str, float\]                                                                                 |
| Names: List\[str\]                         | Names accept a list of str                                                                                   |
| Names: Iterable\[str\]                     | Any iterables of strings, such as list, set, tuple.                                                          |
| Id: Union\[int, str\]                      | Id accepts either int or str                                                                                 |
| Name: Optional\[str\]                      | Equivalent to Union\[str, None\], i.e., accept str or None.                                                  |
| x: Tuple\[str, float, int\]=(“hi”, 3.5, 3) | X is a 3-element tuple with three types                                                                      |
| x: Tuple\[int,…\]                          | Variable size tuple of ints                                                                                  |
| x: Callable\[\[int,int\],float\]=fun       | A function accepts two ints and return a float                                                               |
| def g(n:int) -&gt; Iterator\[int\]:        | Return an iterator, such as generator function                                                               |
| x: List\[Union\[str,int\]\]=\[3,”s”,4\]    | X is a list having mixed elements of str and int.                                                            |
| X: Any = anyType()                         | X can be any type, used when too complicate for typing                                                       |
| X = “smot” \# type: ignore                 | Suppressing type checking for this line                                                                      |
| f(mp:Mapping\[int,str\])-&gt;None          | Here mp is a dict-like data, so call it as f({3:’a’, 5:’b’}), for mutable mapping, use ‘MutableMapping\[\]’. |
| x: MyClass = MyClass()                     | Use user-defined class ‘MyClass’ as a type.                                                                  |
| Seats: ClassVar\[int\]=4                   | Use ‘ClassVar’ type to annotate a class variable.                                                            |
| X: Match\[str\]=re.match(‘+’,”*abc*”)      | X is a regex match object                                                                                    |
| X: IO\[str\] = sys.stdin                   | X is a filehandle by using IO type                                                                           |

### Docstrings

Docstrings should be enclosed in by triple-quotes """, and each line the
maximal length is 72. Docstrings can be classified into the following
categories:

| category         | where to put                                            | what to include                                                                                                                            |
|------------------|:--------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| class docstrings | immediately after class declaration, indented one level | brief summary of the class, public methods with brief description, class attributes, any interface for subclasses.                         |
| class methods    | immediately after the class method declaration          | brief description of the method is for, arguments, , returns, any side effects, exceptions that are raised, restrictions on method call.   |
| package          | at the top of **init**.py file of the package           | list modules and sub-packages exported by the package.                                                                                     |
| module           | at the top before import statements                     | description of the module and its purpose, list of classes, functions, and any other exported objects                                      |
| module function  | immediately after function declaration                  | similar to class methods, including description, arguments, side effects, exceptions, and restrictions on when the function can be called. |
| script           | at the top of the file                                  | description of the purpose, arguments, and dependent packages/modules.                                                                     |

When on run help(obj), it essentially extracts the information stored in
obj.\_\_doc\_\_, i.e., Docstring, which can be generated from the
strategic placement of strings directly below an object. One can
manipulate obj.\_\_doc\_\_ to modify this value

The Docstrings have multiple formats, summarized as below. Among them,
restructured text and NumPy/SciPy Docstrings formats are formal
specification and supported by Sphinx. One can find more on restructured
text syntax at
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>.

| format                                                              | example                                             |
|---------------------------------------------------------------------|:----------------------------------------------------|
| Google                                                              | """Gets and prints the spreadsheet’s header columns |
| Args:                                                               |                                                     |
| file\_loc (str): The file location of the spreadsheet               |                                                     |
| print\_cols (bool): A flag used to print the columns to the console |                                                     |
| (default is False)                                                  |                                                     |
|                                                                     |                                                     |
| Returns:                                                            |                                                     |
| list: a list of strings representing the header columns             |                                                     |
| """                                                                 |                                                     |
| restructured text                                                   | """Gets and prints the spreadsheet’s header columns |
| :param file\_loc: The file location of the spreadsheet              |                                                     |
| :type file\_loc: str                                                |                                                     |
| :param print\_cols: A flag used to print the columns to the console |                                                     |
| (default is False)                                                  |                                                     |
| :type print\_cols: bool                                             |                                                     |
| :returns: a list of strings representing the header columns         |                                                     |
| :rtype: list                                                        |                                                     |
| """                                                                 |                                                     |
|                                                                     |                                                     |
| NumPy/SciPy                                                         | """Gets and prints the spreadsheet’s header columns |
| Parameters                                                          |                                                     |
| ———-                                                                |                                                     |
| file\_loc : str                                                     |                                                     |
| The file location of the spreadsheet                                |                                                     |
| print\_cols : bool, optional                                        |                                                     |
| A flag used to print the columns to the console (default is False)  |                                                     |
|                                                                     |                                                     |
| Returns                                                             |                                                     |
| ——-                                                                 |                                                     |
| list                                                                |                                                     |
| a list of strings representing the header columns                   |                                                     |
| """                                                                 |                                                     |
| Epytext                                                             | """Gets and prints the spreadsheet’s header columns |
| @type file\_loc: str                                                |                                                     |
| @param file\_loc: The file location of the spreadsheet              |                                                     |
| @type print\_cols: bool                                             |                                                     |
| @param print\_cols: A flag used to print the columns to the console |                                                     |
| (default is False)                                                  |                                                     |
| @rtype: list                                                        |                                                     |
| @returns: a list of strings representing the header columns         |                                                     |
| """                                                                 |                                                     |

Sphinx is a powerful document auto-generation system, which can parse
Docstrings in the python code using audodoc extension and can convert
any reStructured and markdown texts to a bunch of different formats such
as html, pdf, manpages, etc. One can learn more at
<https://www.sphinx-doc.org/en/master/usage/quickstart.html>.

## Performance test

To test performance after each change, one can also set up tests, or use
the pytest plugin pytest-benchmark.

## Some useful modules and packages

-   bandit: To test security flaws in your code, one can use the
    ‘bandit’ package. This can also be included in a setup.cfg for CI/CD
    tools

-   mmap: one can use the module mmap to represent file as memory-mapped
    file objects, which behaves like both bytearrays and file objects,
    so one can use the methods from both classes. mmap uses virtual
    memory to handle big files and can allow multiple processes to
    access the same data with shared memory (fileno=-1, not compatible
    with multiprocessing module, for which use shared\_memory module
    instead). mmap object has many methods as file objects have and also
    have find and rfind methods to search subsequences in the whole
    file. But in terms of efficiency, mmap may not be faster than
    regular read/write all the time, depending on the file size (mmap
    performs better in larger files) and specific operations. Also mmap
    object can be used as a string, so operations like regular
    expression can be also used on it. There are four access mode for
    mmap, ACCESS\_READ, ACCESS\_WRITE, ACCESS\_COPY, and
    ACCESS\_DEFAULT. The ACCESS\_WRITE mode writes both to memory and
    underlying file, while ACCESS\_COPY only writes to memory and not to
    file

-   Mypy: a package to statically check code compatibility among
    different parts, to take advantage of the capacity, the code needs
    typing specification/type hints, such as ‘def greeting(name: str)
    -&gt; str’. The code without type annotation is considered
    dynamically typed by mypy, such as ‘def greeting(name)’, and in
    default, mypy will not check dynamical typing.

## Similarity between Python and other languages

### Perl

| Python                              | Perl  | Comment                        |
|-------------------------------------|-------|:-------------------------------|
| List comprehension and map function | map   | Similar between these two      |
| Underscore ‘\_’                     | undef | Disgard returned value         |
| Filter                              | grep  |                                |
| break                               | last  | Stop a loop                    |
| continue                            | next  | Iterate to next item in a loop |

### R

| Python                                                                                                  | R                   | Comment                                         |
|---------------------------------------------------------------------------------------------------------|---------------------|:------------------------------------------------|
| map(fun, args …)                                                                                        | apply               | True when the fun accepting multiple arguments. |
| Zip(list1,list2), return a list of tuples with each containing corresponding elements from list 1 and 2 | cbind(list1, list2) |                                                 |