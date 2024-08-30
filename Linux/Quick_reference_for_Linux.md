Quick Reference for Linux
================

-   [Programming](#programming)
    -   [File processing](#file-processing)
    -   [Shell](#shell)
-   [File system](#file-system)
-   [Compilation](#compilation)
-   [Conda](#conda)
-   [User management](#user-management)
-   [Remote access](#remote-access)
-   [Other useful commands](#other-useful-commands)
-   [Session management](#session-management)
    -   [tmux](#tmux)

## Programming

### File processing

Here are for tools such as sed, awk, etc.

-   in gawk, regular expression be used in the following way, depending
    on whether the pattern is in a variable:

        "string" ~ /pattern/
        # if variable, no forward slashes
        patVar="hello$"
        "string" ~ patVar

-   join two files based on a common field

    One can use `join` to merge two files based on a common field. The
    two files need to be pre-sorted on the common field. In default, it
    only outputs rows have matching fields of the two input files. To
    output all rows, including those don’t have a match in the other
    file, add the option `-a` and `-o`,for example:

    ``` bash
    join -1 1 -2 1 -t $'\t' -a 1 -a 2 -o 0,1.2,2.2 test1.tsv test2.tsv 
    ```

    Explanation:

    -   -1 1 -2 1: use the 1st field from both file as common fields
    -   -a 1 -a 2: output unmatching rows from both files
    -   -o 0,1.2,2.2: output common field, 2nd field of 1st file and 2nd
        field of 2nd file
    -   -t $’: field separator is a tab

### Shell

-   Do not use

        n=0; (( n++ ))

    in bash, as this returns a status 1, i.e., error code, which may
    break the program. For safety, use

        (( n += 1))

-   Sub-shell is a shell lauched by a shell process and any changes in
    the sub-shell will not affect parental shell. Sub-shells can be
    created by:

    -   calling external programs
    -   command substitutions, eg: `$(ls)`
    -   pipe: each command in a pipe is executed in a separate process,
        i.e., sub-shell, so any changes made in these commands will not
        be visible in the main script. Also the pipe size is 64KB, when
        it is full, the write would be blocked; similarly when it is
        empty, the read will be blocked. Note that the pipe buffer is in
        memory and never goes through disk.

-   To access the value of a variable whose name is stored in another
    variable, one can use the following format in Bash `${!varName}`.
    For example,

        var=”variable content”
        varName=”var” 
        echo ${!varName}
        # will output ”variable content”

## File system

-   One can use symbolic links to link other files required by a
    software.

        ln -s <source-file> <link-name>

    When making it, one either does it in the target folder, or provide
    the full path for the source-file; otherwise, the link may fail.

-   Bash or perl scripts (I guess others, too) are unable to read
    aliases defined in shell, because aliases are stored in memory and
    behave like environment variables.

-   List the hierachical structure of a folder.

        tree <folder>
        # to limit to a certain depth, use the option -L
        tree -L 2 <folder> 

-   Copy a file with its parent folders

        cp --parents a/b/c existing_dir

    This copies the file `a/b/c' to`existing\_dir/a/b/c’, and the
    missing intermediate folders would be created.

-   File globbing

    One can use the following patterns to match files:

    | Pattern      | Description                                                     |
    |--------------|:----------------------------------------------------------------|
    | \*           | Match zero or more characters                                   |
    | ?            | Match any single character                                      |
    | \[…\]        | Match any of the characters in a set                            |
    | {abc,def}    | Match any strings in a set                                      |
    | ?(patterns)  | Match zero or one occurrences of the patterns (extglob)         |
    | \*(patterns) | Match zero or more occurrences of the patterns (extglob)        |
    | +(patterns)  | Match one or more occurrences of the patterns (extglob)         |
    | @(patterns)  | Match one occurrence of the patterns (extglob)                  |
    | !(patterns)  | Match anything that doesn’t match one of the patterns (extglob) |

    For example, one can use the following to match any files ending
    with jpg or gif

    ``` bash
    ls *.?(jpg|gif)
    # equivalent to
    ls *.{jpg,gif}
    ```

    Note the pattern modifiers for extended globbing are put ahead of
    patterns, different from the regular expression in other language
    such as Perl and Python. These extended patterns can also be used in
    string operations such as “%”, “\#\#”, “//”.

    One can find more examples at
    <https://www.linuxjournal.com/content/pattern-matching-bash>

-   Untar a file into a folder

    ``` bash
    mkdir targetDir
    tar -xzf test.tar.gz -C targetDir --strip-components=1
    ```

-   File permission

normally, each file and folder have its read/write/executable
permissions set for owner, group, and other users. This traditional way
allows permission is set to a single owner and group, so no way to give
permissions to different users or groups.

One solution to this is to use
[ACL](https://www.geeksforgeeks.org/access-control-listsacl-linux/).

To add permission for a user, say, *special*, one can run

``` bash
setfacl -m u:special:rw needed/file
```

To add permission for a group, say, *sgroup*, one can run

``` bash
setfacl -m g:sgroup:rwx needed/dir
```

To apply the permission recursively in a folder, add option `-R`.

To revoke the acl permisions set on a file or folder, run

``` bash
setfacl -b needed/file
```

To get the acl setting of a file/folder, run the following:

``` bash
getfacl needed/file
```

Also, when a file/folder has ACL settings, it will show a ‘+’ sign in
the permission string when one run `ls -l`, like ‘rwxr-x—+’.

## Compilation

1.  When a certain lib file can’t be found, one can use the following
    ways to fix it:

    -   create a symbolic link to targett in the stardard library folder
        such as /usr/bin/lib
    -   export environment variable LD\_LIBRARY\_PATH=/path/to/lib

2.  To see what paths are searched for dynamic libraries by compilers,
    use the following commands:

         ld --verbose | grep -i search_dir | tr -s ' ;' '\n'

3.  To get the paths of libraries at run-time, run the following
    command, which searches the files in /etc/ld.so.conf and
    /etc/ld.so.conf.d/

        ldconfig -v 2>/dev/null | grep -vP "^\s"

    The libraries are search in the following order:

    -   Paths by `LD_LIBRARY_PATH`
    -   rpath hard-coded in executables
    -   system default paths (as above)

4.  To add paths which are searched during run time, one can add the
    path to `/etc/ld.so.conf` or put an additional file with the paths
    (one per line) in the folder `/etc/ld.so.conf.d`, and then run
    ldconfig. Alternatively, one can encode a search path in an
    executable as rpath, with two ways:

    1.  setting an environment variable LD\_RUN\_PATH which contains
        directories separated with colons (note, don’t include system
        default directories);
    2.  add a linker flag –R /extra/link/path (the flag can be repeated
        many times). (If –R not work, one may use
        –Wl,-rpath,/extra/link/path \[note: no space here between –Wl,
        -rpath, and the path\]).

5.  To test whether a program works at run time, one can run ldd on the
    program, which will print out found and not found libraries.

        ldd /bin/ls

6.  one can use a program patchelf or charpath to modify the rpath in a
    program, but this works only on ELF-type systems such as Linux or
    Solaris. For others, one may think build their programs using a
    static other dyamic library.

7.  don’t forget to run ‘ldconfig’ to update installed libraries after
    intall any library, otherwise the compiler remains complaining
    missing the library.

8.  To create a shared library, one can use the following steps:

        gcc –fPIC –g –c –Wall a.c
        gcc –fPIC –g –c –Wall b.c
        gcc –shared –Wl,-soname,libmystuff.so.1 –o libmystuff.so.1.0.1 a.o b.o –lc

    where the first commands generated position-independent-code
    objects, and the last one creates the library.

## Conda

-   channel priority is so important, if not set right, some packages
    would not be installed.

    to show the channel order, run `conda config --show channels`

    To prepend a channel, `conda config --prepend channels channel_name`

    To ask conda to follow the priority order strictly, use
    `conda config --system --set channel_priority strict`

## User management

## Remote access

One can connect to a remote Linux system graphically via the following
tools:

-   windows remote desktop: this tool is available for both windows and
    MacOs, and relies on the xrdp service on the host Linux machine. My
    experience with this tool is that it can easily get stuck in login
    if sessions are not closed properly.

-   NoMachine: this is another tool to get a remote desktop. The
    solution is to install the tool in both client (say, MacOS) machine
    and host (e.g. Ubuntu) machine (starting a service listening on 4000
    after installation), and then follow the instruction to connect.

## Other useful commands

-   dmesg: Get the kernel log, useful for knowing the reason for killing
    an process

-   file –s /dev/sda: Get the file system information for a mounted
    device.

-   resize2fs /dev/sda: Expand the file system after allocating more
    space to the partition /dev/sda.

-   `echo "scale=2; 12/5" | bc`: get the numeric division of the two
    numbers. Note only division ‘/’ reads the parameter ‘scale’, add,
    multiply, and subtraction does not read it.

-   printf “%.3f” 12.1234: Format the output

-   lscpu or nproc: Show CPUs’ hardware information

-   lsb\_release -a: show the system information such as version and
    name

## Session management

### tmux

tmux can keep an ssh session active even the window is terminated.

-   Some useful plugins
    -   tmux-resurrect: save sessions to a file, default
        *\~/.local/share/tmux/resurrect*, can be set via *set -g
        @resurrect-dir <path>* in *\~/.tmux.conf*.
    -   tmux plugin manager: plugin manager
