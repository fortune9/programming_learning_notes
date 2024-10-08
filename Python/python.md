Python learning notes
================
Zhenguo Zhang
September 13, 2024

-   [Variables](#variables)
    -   [Python data types](#python-data-types)
    -   [False values](#false-values)
-   [Functions](#functions)
    -   [Notes](#notes)
    -   [Useful functions](#useful-functions)
-   [Classes](#classes)
-   [Packages](#packages)
-   [Modules](#modules)
    -   [Load python modules](#load-python-modules)
    -   [Search python modules](#search-python-modules)
    -   [Popuplar modules](#popuplar-modules)
    -   [matplotlib](#matplotlib)
    -   [Pandas](#pandas)
-   [Code testing](#code-testing)
    -   [Manual and automatic testing](#manual-and-automatic-testing)
    -   [Testing modules](#testing-modules)
-   [Formatting](#formatting)
    -   [PEP8 guideline summary](#pep8-guideline-summary)
    -   [flake8 configuration](#flake8-configuration)
    -   [Static type hinting](#static-type-hinting)
    -   [Docstrings](#docstrings)
    -   [Multi-line string](#multi-line-string)
    -   [Multi-line statement](#multi-line-statement)
-   [Parallelization](#parallelization)
    -   [Thread vs process](#thread-vs-process)
    -   [Synchronization](#synchronization)
-   [Performance test](#performance-test)
-   [Some useful modules and
    packages](#some-useful-modules-and-packages)
-   [Debug](#debug)
-   [Similarity between Python and other
    languages](#similarity-between-python-and-other-languages)
    -   [Perl](#perl)
    -   [R](#r)
    -   [python 2 and 3.](#python-2-and-3)
    -   [Tips](#tips)
-   [Notebooks](#notebooks)
    -   [Notebook hosting services](#notebook-hosting-services)

## Variables

### Python data types

| Type                        | Comment                                                                         |
|-----------------------------|---------------------------------------------------------------------------------|
| Tuple, e.g, (1, 3, ‘aha’)   | Similar to list, but immutable                                                  |
| Set. {1, 2, 3,‘aha’}        | Cannot get element by index, and the elements must be different from each other |
| List, \[1,2,3,‘aha’\]       | a list can contain elements of different types                                  |
| Dictionary, {‘a’: 1, ‘b’:2} | Like hash in Perl                                                               |

### False values

-   Empty list/string/tuple: Empty list/string/tuple are all false in
    ‘if’ test, so no need to test length

## Functions

### Notes

-   Every time we pass in an object into a function in Python, what we
    are doing is not passing in a box that contains an object but we are
    passing in a copy of the box that contains an address to the
    specific object, i.e. a reference to an object. And when we change
    the object in place within function, we change the original object
    outside too. However, if we change the passed-in copied box within
    the function (re-assign), Python does some magic and creates a new
    object that the copied box points to. Therefore, depending on
    changing the copied box (the function variable) or the object the
    copied box points to, the side effect to outside variables will
    differ: changing the copied box would not have side effect to
    outside namespace.

-   30. In python, there is a type of function called ‘closure’, it is
        defined as a function in another function and can be returned as
        a variable. The key information is about the lifetime of
        variables when the closure is defined: the closure remembered
        its local environment when it is defined, so even some variables
        have been destroyed after the outer function is called.
        Eg: &gt; &gt;&gt;&gt; def outer(x): &gt; … def inner(): &gt; …
        print x \# 1 &gt; … return inner &gt; &gt;&gt;&gt; print1 =
        outer(1) &gt; &gt;&gt;&gt; print2 = outer(2) &gt; &gt;&gt;&gt;
        print1() &gt; 1 &gt; &gt;&gt;&gt; print2() &gt; 2

### Useful functions

| Function name                                                                                             | purpose                                                                                                                                                                                                |
|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Bin(), hex(),int(), oct()                                                                                 | Convert numbers between oct. hex and decimal formats                                                                                                                                                   |
| Str1\*3, str1\[start:end\], str1+str2                                                                     | Repeat, slice, concatenate strings                                                                                                                                                                     |
| Float(), int(), str()                                                                                     | Convert between float, int, and strings                                                                                                                                                                |
| ord(), chr()                                                                                              | Get ASCII code or convert a code to a character.                                                                                                                                                       |
| Tuple(), list()                                                                                           | Convert to tuple or list                                                                                                                                                                               |
| Capitalize(), lower(), upper(), title(), swapcase(), replace(), startswith(), endswith(), find(), count() | Methods for strings                                                                                                                                                                                    |
| len()                                                                                                     | Get the length of a string, list, tuple                                                                                                                                                                |
| next()                                                                                                    | Get next element from an iterator                                                                                                                                                                      |
| Sum()                                                                                                     | Return the sum of numbers in a list or tuple                                                                                                                                                           |
| isinstance(obj, type)                                                                                     | test whether an object is certain type/class, e.g., isinstance(“a”,str )                                                                                                                               |
| id()                                                                                                      | Get the memory address of a variable                                                                                                                                                                   |
| dir()                                                                                                     | get the attributes of an object or class, such as their methods and variables.                                                                                                                         |
| sys.getsizeof()                                                                                           | Get the memory size of an object (not working on nested object)                                                                                                                                        |
| issubclass(a, b)                                                                                          | testing whether a is a subclass of b.                                                                                                                                                                  |
| locals()                                                                                                  | get a dictionary containing the local variables.                                                                                                                                                       |
| mod=**import**(“file.py”)                                                                                 | import a file into a variable, and then use the variable to access class/functions/var.                                                                                                                |
| globals()                                                                                                 | get a dictionary containing the global variables.                                                                                                                                                      |
| iter(obj\[,sentinel\])                                                                                    | return an iterator which need have **next**() method. If sentinel is absent, obj should supports **iter**() or **getitem**(). If sentinel is present, obj should be a callable with **next**() method. |

## Classes

## Packages

A directory of modules form a package. A module can also be in a
sub-directory, such as a/b/mod.py. To import this module, one can use
import a.b.mod, and then use the module by referring it as a.b.mod.
**All packages are modules with **path** attribute, actually.**

One can put a **init**.py file in the folder, say, “my\_lib”, then
“my\_lib” becomes a package, when loading the package “import my\_lib”
or any module in the folder ‘my\_lib’, the \_\_init\_\_py is also run
first. If you want nothing to run, just keep this file empty.

There are two types of packages: regular and namespace. Regular packages
exist before python 3.2 and needs **init**.py in the directory, where
**init**.py file is implicitly executed when the module is loaded and
all the objects/functions in the file are bound to the namespace of the
package, so it can contain any code which are valid in a module file. In
**init**.py file, the variable ‘**name**’ refers to the module name. and
the **init**.py file can define variables/methods/classes as if they
were defined in the corresponding modules. On the other hand, namespace
packages are composed of portions, where each portion contributes to a
submodule, and these portions can exist in different file systems, even
network, can be zipped. When they are loaded, python creates a namespace
package for the modules (hirachical structure based on module names).
For the namespace modules, there is no need to have **init**.py in each
module folder.

When you import FooPackage, Python searches the directories on
PYTHONPATH until it finds a file called FooPackage.py or a directory
called FooPackage containing a file called **init**.py. However, having
found the package directory, it does not then scan that directory and
automatically import all .py files. There are two reasons for this
behaviour. The first is that importing a module executes Python code
which may take time, memory, or have side effects. So you might want to
import a.b.c.d without necessarily importing all of a huge package a.
It’s up to the package designer to decide whether a’s **init**.py
explicitly imports its modules and subpackages so that they are always
available, or whether or leaves the client program the ability to pick
and choose what is loaded. The second is a bit more subtle, and also a
showstopper. Without an explicit import statement (either in
FooPackage/**init**.py or in the client program), Python doesn’t
necessarily know what name it should import foo.py as. On a case
insensitive file system (such as used in Windows), this could represent
a module named foo, Foo, FOO, fOo, foO, FoO, FOo, or fOO. All of these
are valid, distinct Python identifiers, so Python just doesn’t have
enough information from the file alone to know what you mean. Therefore,
in order to behave consistently on all systems, it requires an explicit
import statement somewhere to clarify the name, even on file systems
where full case information is available.

## Modules

Python modules are python script files; they can contain both
function/class definitions as well as code, just like normal scripts. It
can be imported into other scripts, just like bash’s source command to
import other bash codes; when being imported, the code in the module is
run.

### Load python modules

Each python module is loaded only once in one interpreter session,
subsequent import statements will not reload the module. To reload a
module in a program, run importlib.reload(mod).

Python modules can be as simple as a file with defined functions and
variables, and then one can import the file to use the defined functions
and variables. The standard python modules are also a set of .py files.
If there are codes such as calling some functions in a module, these
calling codes will be executed when importing the module.

Actually, in a python module, one can also define a global variable
‘**all**=\[foo, bar\]’, which will control what variables to import when
one uses "from mod import \*".

When loading a module, the import machinery set up the following
attributes for each module object:

| attribute   | explanation                                                                                                                                |
|-------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| **name**    | the module name, uniquely find the module in the import system.                                                                            |
| **loader**  | loader object used to load the module.                                                                                                     |
| **package** | if loaded is a package, it sets to **name**; if a module, sets to parent’s package name, or empty string for top level module.             |
| **spec**    | module spec that used to import the module.                                                                                                |
| **path**    | must be set if a module is a package, provides a list of locations to search sub-packages. Maybe altered in **init**.py file of a package. |
| **file**    | path to module file; optional                                                                                                              |
| **cached**  | path to compiled code file                                                                                                                 |

There are two ways to import module. Say there is a module a/b/c.py, one
can use:

``` python
import a.b.c;
from a.b import c;
```

The latter will allow one to refer the functions/variables in the module
‘c’ as c.fun() in the short format. Note that, if there is also a module
a/b.py and in it there is a function/variable defined with the name ‘c’,
then this function/variable will be imported, other than the module.

One can import multiple modules once such as ‘import a, z, m;’, but this
style is not recommended.

One can also use "from a.b import \*" to load all modules in the package
a/b. However, depending on whether a variable ‘**all**’ is defined in
the file a/b/**init**.py, it behaves differently: - if **all** is
defined as **all**=\[“x”,“y”\], then the submodules a/b/x.py and
a/b/y.py are loaded. - if **all** is not defined, then the module a.b
and all names in a.b are loaded

One can also use relative path to import modules. For example, if there
are two modules x.py and y.py under the folder mypackage/subpackage.
Then one can use ‘from . import x’ to import the module x to module y,
because they are in the same folder. relative imports are based on the
name of the current module’s package (stored in the variable
**package**), if the module is run as a executable, then the name would
be **main**, and thus can’t determine the folder of this module and so
the modules relative to this current module; in this case, absolute
imports are needed.

When using relative path to import, note that python relies on the
**name** and **package** to determine where to look the packages. For
instance, if there is a directory with the following structure:

> top/  
> —com.py  
> —mod/  
> ——–bar.py

so when the top/mod/bar.py use ‘import ..com’, and we run it as “python
–m mod.bar” or “python mod/bar.py” in the folder top/, it will fail with
error “ValueError: attempted relative import beyond top-level package”.
The reason is this: when calling python –m mod.bar, the package name is
‘mod’ and is regarded as current folder (referred by ‘.’, so .bar can
refer bar.py), so the point ‘..’ goes above the folder ‘mod’, which is
not in the package name. One solution is call ‘python –m top.mod.bar’;
at the same time, the folder ‘top’ needs ‘**init**.py’ file to indicate
it is a package.

Actually, one module can import namespaces imported by another module.
For example, if module x imported module ‘z’, then module y can also
import module z by ‘from x import z’.

There are two common mistakes in module loading: circular imports
(modules load each other) and shadowed imports (creating a module with
the same name as another module, but also import this another module for
functions).

One can run a module file a/b/mod.py using two ways: python –m a.b.mod
and python a/b/mod.py. The former will behave like the module a/b/mod.py
(as well as necessary parent modules) is imported and also run as a
script, but the latter doesn’t import the module, just running as a
standalone script. See this for more
<https://stackoverflow.com/questions/22241420/execution-of-python-code-with-m-option-or-not>.

### Search python modules

Python module search: One can use python -c ‘import sys;
print(sys.path)’ to find where python searches for modules/packages.
Because of this, one can use sys.path.append(‘new\_folder’) to add
another folder for python to search additional modules. sys.path is
initialized from three locations: the directory containing the input
script, the global variable PYTHONPATH (list of colon-separated
directories), and installation-based default libraries.

Python search modules in current folder and those in sys.path. To
include a module in another folder, say /my/python/lib, one can use the
code sys.path.append(“/my/python/lib”) to expend the library/module
search paths. Or one can put the modules in a folder included in the
variable sys.path; in this way the change will be permanent.

95. In python, when one import a module, it actually searches the module
    and binds the results of the search to a local namespace. The search
    operation is done with the **import**() function. On the other hand,
    the importlib module provides APIs to import modules, which are
    simpler than **import**() and provide better control on the import
    machinery. The search of the module (or package) names in the
    following order: sys.modules (a mapping between previously imported
    module/package names and the objects, also called “the module
    cache”), finders (strategies to find the named module and return
    specs) and loaders (load the found modules). Actually, the finders
    are stored in the import hooks, including “meta hooks” and “import
    path hooks”. The meta hooks are stored in sys.meta\_path, including
    three types of finders: builtin modules, frozen modules, and modules
    from import path. import path hooks are triggered when processing
    sys.path, which is after processing meta hooks. After modules are
    found, they are loaded and loaders are triggered to execute the
    module.
96. in addition to meta path finders, there are path entry finders,
    which find modules/packages whose locations are specified with
    string path entries. Three variables are used for finding path
    entries: sys.path, sys.path\_hooks, sys.path\_importer\_cache, also
    for packages, **path** attribute is also used.

### Popuplar modules

| Module name      | Function                                                         | Comment                                                                                                                                             |
|------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| BeautifulSoup    | A module to parse a html/XML file into tree hierarchy structure. |                                                                                                                                                     |
| matplotlib       | Plot figures                                                     | It uses backend to make plots, and it can be setup in configuration file matplotlibrc, which can be found by calling matplotlib.matplotlib\_fname() |
| numpy            | Processing matrix/vector                                         |                                                                                                                                                     |
| json             | Packing data for sharing                                         |                                                                                                                                                     |
| Dateutil.parser  | Parse date/time strings such as Unicode strings                  |                                                                                                                                                     |
| requests, urllib | internet related options, such as download, inquiry              |                                                                                                                                                     |

### matplotlib

-   matplotlibrc file is the central file to set configuration for
    python matplotlib. More info on matplotlibrc can be found at
    <https://gist.github.com/CMCDragonkai/4e9464d9f32f5893d837f3de2c43daa4>.

-   key functions/terms: plt=matplotlib.pyplot; mpl=matplotlib; rcsetup=
    matplotlib.rcsetup

    | Term/function                                                                | Explantion                                                                                                                                                      |
    |------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | Plt.get\_backend()                                                           | Get default plot backend used by matplotlib                                                                                                                     |
    | plt.switch\_backend(“newBk”)                                                 | Switch to new backend.                                                                                                                                          |
    | mpl.matplotlib\_fname()                                                      | Get matplotlibrc file path.                                                                                                                                     |
    | rcsetup.interactive\_bk, rcsetup.non\_interactive\_bk, rcsetup.all\_backends | Get all useable backend string keys.                                                                                                                            |
    | mpl.use(‘agg’)                                                               | Set the backend used by matplotlib. Alternative approaches include set environment variable ‘MPLBACKEND=Qt4Agg’ and put ‘backend: Qt4Agg’ in matplotlibrc file. |

### Pandas

-   Pandas is the package to manipulate data in python, just like the
    data.frame in R. It has three main data types: series, dataFrame,
    and panel, in the order of increasing complexity. Series is actually
    1-dimentional vector, dataFrame is a combination of many same-size
    series, and panel can contain multiple dataFrame as components (like
    the list in R).

-   in pandas, row/column names/ids are called indices in
    pandas.DataFrame, and the row indices can contain more than one
    variable/column (i.e., multiIndex), like a primary key in a database
    table; one can use df.xs() and df.loc() to access rows matching
    certain indice, and one can put slice(None) at an index position
    where all values are allowed such as df.loc\[(“index1”, slice(None),
    “index3”),:\].

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

| Object                                        | Recommendation                                                                                                                                                                                                                                                 | Example            |
|-----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------|
| Top class, function                           | Two blank lines before them                                                                                                                                                                                                                                    |                    |
| Method in a class                             | One blank line before them                                                                                                                                                                                                                                     |                    |
| within function                               | Use blank lines to separate main steps                                                                                                                                                                                                                         |                    |
| max line length                               | 79 characters. For multiple line code, one can put code in parenthesis, brackets, or braces, or use backslash  to connect lines. For a long string, one can make it by connecting multiple string segments with ‘' or’+’, or use () to enclose multiple lines. |                    |
| indentation                                   | 4 consecutive spaces preferred over tab. For line continuation, one can use ‘hanging indent’ or ‘extra indent’ (align to open delimiter) to improve readability.                                                                                               |                    |
| closing brace                                 | Align with first non-white character of previous line, or the first character of the construct.                                                                                                                                                                |                    |
| comments                                      | Start with ‘\#’ (a space here), using complete sentence with first letter capitalized. Use inline comments sparingly unless necessary                                                                                                                          |                    |
| docstrings                                    | Enclosed in triple double/single quotes, writing for public modules, functions, methods, classes. Put ending quotes on a single line itself, except for oneline docscript, which should all be in one line.                                                    |                    |
| Binary operators such as =, &lt;=, or, is, in | Add one white space on each side, but no space when assigning default value in function definition. Also add space to lowest operator only, e.g., \* vs +                                                                                                      | z = (x+y) \* (x-y) |

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
| x: List\[Union\[str,int\]\]=\[3,“s”,4\]    | X is a list having mixed elements of str and int.                                                            |
| X: Any = anyType()                         | X can be any type, used when too complicate for typing                                                       |
| X = “smot” \# type: ignore                 | Suppressing type checking for this line                                                                      |
| f(mp:Mapping\[int,str\])-&gt;None          | Here mp is a dict-like data, so call it as f({3:‘a’, 5:‘b’}), for mutable mapping, use ‘MutableMapping\[\]’. |
| x: MyClass = MyClass()                     | Use user-defined class ‘MyClass’ as a type.                                                                  |
| Seats: ClassVar\[int\]=4                   | Use ‘ClassVar’ type to annotate a class variable.                                                            |
| X: Match\[str\]=re.match(‘+’,“*abc*”)      | X is a regex match object                                                                                    |
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

### Multi-line string

two ways to construct multiple-line strings, using ’' or triple quotes:

> ‘string 1’  
> ‘string 2’.format().

Or

> ’‘’string 1 String 2’’’.format().

One can also use the function textwrap.dedent() from the module textwrap
to remove leading spaces at each line.

### Multi-line statement

To write a statement spreading multiple lines, one need put the state in
a parenthesis or brackets, such as

``` python
if (number > 5 and
            number < 15):
        print "1"
```

or use a backslash, such as:

``` python
if number > 5 and \
        number < 15:
    print "1"
```

## Parallelization

### Thread vs process

One can use multi-threads for I/O bound work, in which case the program
has access to only one CPU, but it can run multiple threads. On the
other hand, for computing-intensive work, one can use multi-processes.

### Synchronization

One can use Semaphore or Queue to limit the number of active processes
or threads. Note that for both, there are thread versions and process
versions:

-   Semaphore:
    -   thread: threading.Semaphore()
    -   process: multiprocessing.Semaphore()
-   Queue:
    -   thread: threading.Queue()
    -   process: multiprocessing.Queue()

When using queue for processes, it is better to create it in the main
function, and let other child processes inherit the same queue (shared
among processes). Otherwise one may meet the RuntimeError: Queue objects
should only be shared between processes through inheritance. Passing the
queue as a parameter to functions is not a good practice.

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

## Debug

-   The following ways can be used to debug python script:
    1.  put pdb.set\_trace() in the program, from where debugging starts
        (don’t forget import pdb);
    2.  python –m pdb myscript.py;
    3.  debug in an interactive interface initiated by typing ‘python’
        in command line.
    4.  in ipython, one can import the module ipdb, and use
        ipdb.runcall(func, arg1, arg2) to debug functions. Check
        <https://docs.python.org/3/library/pdb.html> for details on
        debug commands.

## Similarity between Python and other languages

### Perl

| Python                              | Perl  | Comment                        |
|-------------------------------------|-------|:-------------------------------|
| List comprehension and map function | map   | Similar between these two      |
| Underscore ’\_’                     | undef | Disgard returned value         |
| Filter                              | grep  |                                |
| break                               | last  | Stop a loop                    |
| continue                            | next  | Iterate to next item in a loop |

### R

| Python                                                                                                  | R                   | Comment                                         |
|---------------------------------------------------------------------------------------------------------|---------------------|:------------------------------------------------|
| map(fun, args …)                                                                                        | apply               | True when the fun accepting multiple arguments. |
| Zip(list1,list2), return a list of tuples with each containing corresponding elements from list 1 and 2 | cbind(list1, list2) |                                                 |

Compare pandas data.frame to R data.frame (pd represents the package
pandas, df is the data created)

| Pandas command                                                                                                                                                                                                                         | R command                                      | Comment                                                                                                                           |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| pd.DataFrame(x,y,z,columns=\[‘a’,‘b’,‘c’\]                                                                                                                                                                                             | Data.frame(a=x,b=y,c=z), or cbind(a=x,b=y,c=z) | Create a data frame with 3 columns named a, b and c.                                                                              |
| Pd.Panel() create 3-dimension array with dim names items, major\_axis, and minor\_axis                                                                                                                                                 | Array()                                        | Create a high-dimension array                                                                                                     |
| df.head(n)                                                                                                                                                                                                                             | head(df,n)                                     | Show first n rows.                                                                                                                |
| df.shape                                                                                                                                                                                                                               | Dim(df)                                        | no parenthesis in df.shape, this is an attribute                                                                                  |
| df.columns                                                                                                                                                                                                                             | Names(df) or colnames(df)                      |                                                                                                                                   |
| df.values                                                                                                                                                                                                                              | df                                             | Get the values stored in the data frame                                                                                           |
| df.loc\[0\]\[‘A’\], df.iloc\[0\]\[0\], df.at\[0,‘A’\], df.iat\[0,0\], df.get\_values(0, ‘A’). use df.loc\[:,‘A’\] to select column ‘A’. df.ix\[\] is equivalent to df.loc\[\] when indexes are integers only or df.iloc\[\] otherwise. | df\[1,1\]                                      | Get the element at the first row of first column. In pandas, the index starts with 0. To select a column, use df\[col\] directly. |
| df.drop(“A”, axis=1, inplace=True)                                                                                                                                                                                                     | df\[,“A”\]&lt;-NULL                            | Delete a column                                                                                                                   |
| df.pivot(), df.melt(), df.stack(), df.unstack()                                                                                                                                                                                        | reshape(), reshape2 package                    | Convert between long and wide data.frames.                                                                                        |
| df.isin(a\_list)                                                                                                                                                                                                                       | df %in% a\_list                                | Test whether values in a given list                                                                                               |
| df.where(df &lt; 0)                                                                                                                                                                                                                    | df\[df&lt;0\]                                  |                                                                                                                                   |
| df.apply(fun, axis=1)                                                                                                                                                                                                                  | apply(df, 2, fun)                              | Apply a function to a dataFrame rowwise or columnwise (depending on option ‘axis’)                                                |
| pd.merge(df1, df2, how=“outer”, on=“col1”)                                                                                                                                                                                             | Merge(df1, df2, by=“col1”, all=T)              | Merge two data frame, python’s ‘how’ parameter corresponds to R’s ‘all’.                                                          |
| pd.DataFrame.sort\_index()                                                                                                                                                                                                             |                                                | sort index of a dataframe for efficient operation                                                                                 |
| pd.DataFrame.reset\_index()                                                                                                                                                                                                            |                                                | Remove multiIndex of a DataFrame                                                                                                  |
| df.xs(“indexVal”, level=“indexName”)                                                                                                                                                                                                   |                                                | Select rows matching an index.                                                                                                    |

### python 2 and 3.

Function \| Python 2 \| Python 3 \| Comments print \| Print x \|
Print(x) \| In python 3 Parameters for print must be in parentheses and
has ‘sep’ and ‘end’ options. Division / \| 4/3=1 \| 4/3=1.3333, 4//3=1
\| in python 3, int/int division leads to float, not truncated int as in
python 2. Open file \| file(“myfile.txt”) \| open(“myfile.txt”) \|
File() is deprecated in python 3 Get input from user \| Raw\_input() \|
Input() \| Get a range \| Xrange() \| Range() \| Range() in python 3
does not return a list and can handle large array. Unicode support \|
u“hello” \| “hello” \| Supported as default in python 3

### Tips

-   To get all the callable methods for an object, use the following
    statement: \[m for m in dir(object) if callable(getattr(object,
    m))\]

-   In python, there are different terms to describe files, here is a
    summary.

    | Name    | Description                                                                                                                   |
    |---------|:------------------------------------------------------------------------------------------------------------------------------|
    | script  | a single file runnable, it contains code outside the scope of functions and classes.                                          |
    | module  | a file intended to be imported and defines members like classes, functions, and variables intended to be used in other files. |
    | package | a collection of modules/subpackages in a folder, which needs **init**.py                                                      |
    | library | this is a loose term referring any packages or collection of packages, such as python standard library.                       |

## Notebooks

### Notebook hosting services

| Name            | Description                                                           |
|-----------------|:----------------------------------------------------------------------|
| binder          | sharing notebooks from a GitHub repo; (see related blog post)         |
| nbviewer        | for viewing hosted notebooks from GitHub or a url (as mentioned)      |
| JupyterHub      | hosting notebooks on a private server, e.g. local, DigitalOcean, etc. |
| Azure Notebooks | host notebooks on an Azure server (see sample notebook)               |
| repo2docker     | spawn docker container from a git repo of notebooks                   |
| commuter        | read notebooks from a local directory or S3 service                   |
| Colaboratory    | google’s host for python notebooks                                    |
| cocalc          | collaborative and share private notebooks                             |
