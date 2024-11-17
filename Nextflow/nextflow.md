Notes on NextFlow
================
Zhenguo Zhang
November 17, 2024

-   [Installation](#installation)
-   [Run it](#run-it)
-   [Structure](#structure)
-   [script](#script)
-   [Channel factories](#channel-factories)
-   [Input type](#input-type)
-   [input channel combination](#input-channel-combination)
-   [Output](#output)
-   [Variables](#variables)
-   [Operators on channels](#operators-on-channels)
-   [process control](#process-control)
    -   [if-else](#if-else)
    -   [for-loop](#for-loop)
    -   [when](#when)
-   [File staging](#file-staging)
-   [Functions](#functions)
-   [nextflow running options](#nextflow-running-options)
-   [Directives](#directives)
-   [Operators](#operators)
    -   [Note on groupTuple](#note-on-grouptuple)
-   [Groovy language](#groovy-language)
    -   [Comments](#comments)
    -   [Variables](#variables-1)
    -   [Strings](#strings)
    -   [File operations](#file-operations)
-   [NextFlow configuration](#nextflow-configuration)
    -   [nextflow.config](#nextflowconfig)
    -   [Syntax](#syntax)
    -   [Important variables](#important-variables)
    -   [Bulk-set attributes](#bulk-set-attributes)
-   [Cloud deployment](#cloud-deployment)
    -   [AWS batch](#aws-batch)
-   [Monitoring workflow](#monitoring-workflow)
-   [DSL2](#dsl2)
    -   [Functions](#functions-1)
    -   [Process](#process)
    -   [Workflow](#workflow)
    -   [Module](#module)
    -   [Channel forking](#channel-forking)
    -   [Pipes](#pipes)
-   [Triger nextflow from git repos](#triger-nextflow-from-git-repos)
-   [Tricks](#tricks)
-   [Caveats](#caveats)
-   [Plugins](#plugins)
    -   [nf-validation, renamed to
        nf-schema](#nf-validation-renamed-to-nf-schema)
-   [Cool facts](#cool-facts)
-   [FAQs](#faqs)
-   [Resources](#resources)

[NextFlow](https://www.nextflow.io/) is a platform to creat and run data
analysis pipelines, and each step or module can be written in any
language. It lets users focus on a pipeline’s logic and takes of the
execution on different platforms: write code once, run everywhere.

The implementation of [NextFlow](https://www.nextflow.io/) is based on
Groovy language (a super set of Java). To learn more about Groovy, one
can check this
[link](https://www.manning.com/books/groovy-in-action-second-edition).

## Installation

nextflow requires Java, so one need to install java before nextflow. To
do so, one can install [Amazon
Corretto](https://aws.amazon.com/corretto/?filtered-posts.sort-by=item.additionalFields.createdDate&filtered-posts.sort-order=desc)
OpenJDK.

Following that, there are two ways to install
[NextFlow](https://www.nextflow.io/):

``` bash
# 1. installed in current directory
curl -fsSL https://get.nextflow.io | bash 

#To install a specific version, one need set environment variable
#`NXF_VER` first, such as

export NXF_VER=22.9.0-edge
curl -fsSL https://get.nextflow.io | bash

# 2. install using Bioconda, may be outdated
conda install -c bioconda nextflow 
```

## Run it

The command to run it is as follows:

    # run through a github repo
    nextflow run git-name/repo --opt1 val1
    # or a local script
    nextflow run local.nf --opt1 val1

To run a command in background (continue running even terminate the
terminal), use the option ‘-bg’. Note that *nohup* can’t be used with
nextflow because the pipeline will stopped.

Nextflow pipeline can also be run from public repositories such as
github, gitlab, etc. To do so, one can run in one of the following way:

    # find the pipeline in public repo host, default github
    nextflow run owner/repoName -hub github
    # or specify the full path to the repo, then option '-hub' is unneeded.
    nextflow run http://github.com/owner/repoName

To access private repo, provide `-user` argument and input password when
prompted, or setup SCM file by following the instruction
[here](https://www.nextflow.io/docs/latest/sharing.html#scm-configuration-file).

Here are some nextflow commands to manage repositories (see [this
doc](https://www.nextflow.io/docs/latest/sharing.html) for details):

| command | explanation                                    |
|---------|:-----------------------------------------------|
| list    | show all downloaded repos.                     |
| info    | show info of a downloaded repo.                |
| pull    | pull a repo.                                   |
| view    | print out the pipeline script, such as main.nf |
| clone   | clone repo to a target folder                  |
| drop    | delete a downloaded repo.                      |

## Structure

A nextflow pipeline consists of processes, and each process is block of
code that run a task. A process contains input, output, and the code to
process input and generate output. The running of each process is
independent in its own temporarily generated folder and don’t share
common state.

Another important component for nextflow is channel. Channel connects
output of preceeding/feeding processes to the input of
following/consuming processes. The consuming processes needn’t wait for
the completion of the feeding process, as long as data avaliable in the
channel, the consuming processes are started. Because of this structure,
the parallel processing is achieved.

A process can define one or more input and outpur channels, and these
channels connect processes and drive the running of pipelines.

There are two types of channels: **queue** and **value**. The queue
channels are created implicitly by channel factories such as
Channel.from() and Channel.fromPath(), or by process output definitions.
They are asynchronous unidirectional FIFO queues.

**Note: in old nextflow version, a queue channel can only be consumed
once**. For example, the following code will show that the second call
of ‘ch.view()’ would fail.

    ch=Channel.from(1,2,3)
    ch.view()
    ch.view()

However, a *value* channel, which is bound to a **single value**, can be
consumed unlimited times, and can be created using the `value` factory
method or by operators returning a single value, such us first, last,
collect, count, min, max, reduce, sum. See example below:

    ch=Channel.value("hello nextflow")
    ch.view()
    ch.view()

In general, a process’s architecture is as follows:

    process <name> {
        [directives]
        input:
        <process inputs>
        output:
        <process outputs>
        when:
        <condition>
        [script|shell|exec]:
        <user script>
    }

*directives*, *input*, *output*, and *when* are all optional.

## script

A process contains one and only one script block, and must be the last
statement.

In default, the script block can be a mix of groovy languages and
strings, and the strings are explained as bash, but any language can be
specified by adding a Shebang declaration at the begining of string.
Actually, any groovy statements can be put before the ‘script:’ block,
which can be used to define some variables (need `def` keyword) or
output information. See groovy document
[here](http://groovy-lang.org/single-page-documentation.html). Also see
the nextflow’s introduction on scripting at
[here](https://www.nextflow.io/docs/latest/script.html), which includes
some operations of strings and files such as `file.copyTo()`.

Strings can be defined using single or double quote, and multi-line
strings can use triple quotes. Note that single-quote prevents
interpolation of pipeline variables.

An alternative keyword to ‘script’ is ‘shell’. They are identical,
except for the following:

1.  using single quote to enclose the code; otherwise dollar variable is
    explained as pipeline variable.

2.  using `!{var}` to refer to pipeline variable, and use `${sys}` to
    refer to environment variable.

Finally, one can also use the keyword ‘exec’ instead of ‘script’, to
write some code using native nextflow/groovy language, one example is as
below:

    x = Channel.from( 'a', 'b', 'c')

    process simpleSum {
        input:
        val x

        exec:
        println "Hello Mr. $x"
    }

To call a user script, the script needs be put into a ‘bin’ subfolder
located in the same folder as ‘nextflow.config’, or in the folders in
‘PATH’ environment variable. If in the ‘bin’ subfolder, the folder will
also be uploaded to working directory when using awsbatch to execute the
pipeline, or add to PATH variable when running locally.

Note that it may fail when running a workflow in a sub-folder and the
workflow refers to the executables in the root bin/ folder, because
nextflow only upload/add the ‘bin’ folder which is in the same folder as
the triggering script. To solve this problem, one may use the variable
`moduleDir` to refer to the bin folder and add it to the PATH
environment variable. See the following folder structure as an example:

    rootdir |
            |___main.nf (call my_exe)
            |___bin
               |___my_exe
            |___workflow
               |___wf1.nf (call my_exe)

    ## successful run
    nextflow run main.nf
    ## failed run
    nextflow run workflow/wf1.nf
    ## to fix this problem, the file workflow/wf1.nf need add
    ## "$moduleDir/../bin" to PATH or use "$moduleDir/../bin/my_exe"
    ## to refer the executable.    

Note that the above method of setting PATH will fail the pipeline if it
is run on AWS batch or alike, because the ‘PATH’ variable always refer
to the user’s local environment variable, not the one in task instance.
One solution to this is that one can use a condition
`${task.executor} == 'local'` to test whether the task is run locally,
if so, set PATH, otherwise not.

Another solution is to make a symbolic link in the subworkflow folder to
the ‘bin’ folder; however, if any script in the bin folder refers to
other resources, those resources have to be linked, too.

The next solution can be one include the sub-workflow modules in the
main script ‘main.nf’, and then use the option ‘-entry’ to specify
certain sub-workflow to execute.

The last solution is one can set `env.PATH` to include the `bin` folder
in nextflow.config. This will ensure that the executables are accessible
in all workflows. Note that the path to the `bin` folder needs to be
absolute path. Note that this will not work for remote executors such as
aws batch, because the bin folder won’t be uploaded and thus
inaccessible.

To include the nextflow.config file in the project root folder to
sub-workflow (workflow/) in this case, and use
`includeConfig ../nextflow.config` to add main configuration file.

## Channel factories

| factory       | queue type | description                                                                                                                                                                                                                                                                                             |
|---------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| value         | value      | bind a single string/list to a channel, and emit it as a whole.                                                                                                                                                                                                                                         |
| from          | queue      | accept a list of values, and emit each element separately, deprecated soon, and should use Channel.of() instead                                                                                                                                                                                         |
| of            | queue      | similar to *from*, can also handle range values like 1..23                                                                                                                                                                                                                                              |
| fromList      | queue      | accept a list and creates a channel emitting elements                                                                                                                                                                                                                                                   |
| fromPath      | queue      | accept a string (possibly with file glob pattern) and return a file list channel. One can add options by appending {opt: value}. The string can contain ’\*‘,’?’ wildcards. And to get into sub-folders, use ’\*\*‘, and also consider use option ’maxDepth’ to control the folder levels to search in. |
| fromFilePairs | queue      | similar to *fromPath*, but return groups of files for each element, like \[id, \[file1, file2\]\]. Option `size` can be used to return how many files for each record.                                                                                                                                  |
| fromSRA       | queue      | query NCBI SRA using accessions or project IDs and return a list of fastq files.                                                                                                                                                                                                                        |

Note that nextflow can’t set a channel if a channel’s name has been used
before, for example if you do:

    my_ch = Channel.empty();

then

    Channel.of(1,3,4).set { my_ch }

will not work.

## Input type

The input block can contain one or more inputs declarations, using the
following format

    input:
        <qualifier> <variable name> from <source channel> 

| qualifier | source type       | return type          | description                                                                                                                                            |
|-----------|-------------------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| val       | any               | strings              | accepts any data type and return string elements                                                                                                       |
| file      | file path         | file path            | accepts file paths from file factories; files are also staged. If inputs are simply strings, then the strings will be the content of a temporary file. |
| path      | string            | file path            | accept a string and return file object, solves the problem of ‘file’ when using string. Note that the string need be in absolute path format.          |
| tuple     | composite channel | composite elements   | comma separated vals and files                                                                                                                         |
| each      | a list            | each list element    | input repeater, it runs the whole process with each input element (over all other input values for each element by this qualifier).                    |
| env       | string            | environment variable | set input value as environment variable named with specified qualifier name.                                                                           |

## input channel combination

If the input block has multiple channels, it can generate combined
values, see the examples below:

      input:
      val x from Channel.from(1,2,3)
      val y from Channel.from('a','b','c')
      script:
      """
      echo $x and $y
      """

it emits three pairs (1,a), (2,b), (3,c).

**Note**: When one channel has fewer elements than the others, the
process will end after consuming all the elements in the channel with
the fewest elements. However, the number of elements in value channels
will not terminate processes, because it can be consumed unlimited
times.

**IMPORTANT**

There are senarios that one channel A has only one element and channel B
has multiple, like aligning multiple fastq files to a genome file. In
this case, one can use the operator ‘toList()’ or ‘collect()’ to convert
A `queue` channel to a `value` channel, and this will ensure each
element from channel B is run against the only element in channel A.
This also works for the channel that emits tuples.

To check a channel type, one can do the following:

``` nextflow
// assume there are two channels: ch1 and ch2 for value and queue channel, respectively
println ch1.getClass() // get groovyx.gpars.dataflow.DataflowVariable for value channel
println ch1.getClass() // get groovyx.gpars.dataflow.DataflowQueue for queue channel
```

Also a input value channel is implicitly created by a process when an
input specifies a simple value (not a channel) in the `from` clause.
Moreover, an output value channel is also implicitly created for a
process whose inputs are only value channels. The code below will show
the cases:

``` nextflow
// simple value as input to create input value channel, so can be combined with other multi-value channels as input for other processes.
input:
    path fa from params.fasta

// this will create a queue channel instead, so processes using this channel as input will run only once.
input:
    path fa from Channel.fromPath(params.fasta)
```

**Input is a list**

When input is a list, such as `Channel.fromPath("*.txt").collect()`,
this input value is automatically converted to an array in script
section, so one can use `${inputList}` to refer to this array in the
script section. Note that when the input is a list of lists, such as
`[[1, hello], [1, ciao], [2, hello], [2, ciao], [3, hello], [3, ciao]]`,
this array will be actually be a string, so they will be split at spaces
when used in a loop. Check
<https://github.com/fortune9/sample-programs/blob/master/nextflow/misc/dsl2/workflow/input_deep_list.nf>
for examples.

## Output

Only output block can be provided for each task, and it can contain one
or more declarations. The declaration follows the following format:

    output:
        <qualifier> <variable name> into <channel 1>[,<channel 2>, ...]

The qualifiers can be summarized as below:

| qualifier | source type   | return type   | description                                   |
|-----------|---------------|---------------|-----------------------------------------------|
| val       | value element | value element | it sends value elements to output channel     |
| path      | file names    | file object   | sends file objects to output channel.         |
| tuple     | tuple list    | tuple list    | it sends a tuple as element to output channel |

One can use a file glob format such as ’chunk\_\*’ to generate a set of
files. The glob matching has the following properties:

1.  input files are never matched against.
2.  it matches both files and directories.
3.  if ’\*\*’ is used instead of ’\*’, it will cross over directory
    boundaries and only match files.

**Note** one can use `arity` to control the expected number of items for
a channel, and this arity specification has higher priority than the
`optional` specification, for example, with the following specification,
the process will fail when no outfiles matching the pattern, even though
it sets “optional: true”. To resolve it, one need to provide ‘0..2’ to
arity.

    path("*_val_{1,2}_fastqc.zip", arity: '1..2'), optional: true

One can also put several files into a list, using the format like below
(enclosed with braces):

``` nextflow
output: path '{f1.txt,f2.txt}' into ch_out
```

Note that the local variable defined in the format ‘def
local\_var=some\_value’ in the script section isn’t visible in the
“output:” section. However, removing the ‘def’ in definition resolved
the issue, but no idea whether other side-effect exist.

## Variables

In nextflow, there are both pipeline variables and environment
variables. The former are the variables that are defined in the
pipeline, such as *params*, *val x from ch\_x*, and the latter are
defined in the system running the pipeline or in the script block, such
as variables for bash, python, perl, etc. Depending on how the commands
are quoted in the script block, different methods are needed for access
these variables:

-   tri-double quotes: pipeline variable uses prefix ‘\$’, such as
    ‘\$params.num’, and environment variables use escape ‘\\’, such as
    ‘\\\$enVar’.

-   tri-single quotes: pipeline variables are not accessible, and
    environment variables use ‘\$’ prefix, such as ‘\$enVar’.

-   use ‘shell’ block instead of ‘script’: pipeline variable uses
    ‘!{params.num}’, and environment variables use ‘\$enVar’. Note that
    pipeline variable must be put in ‘{}’ and the code block must be
    quoted using single quotes.

Also if a pipeline variable is enclosed in single quotes when declared,
then it will still need a ‘\$’ in script block, for example, the
following two are equivalent:

    params.txt=Channel.from("Hello","NextFlow")
    params.txt1=Channel.from("Hello1","NextFlow1")

    process quotes{
        input:
            val 'x' from params.txt
        
        script:
        """
        echo $x
        """
    }

    process noquotes{
        input:
            val x from params.txt1
        
        script:
        """
        echo $x
        # this is a bash comment with unknown variable $y; error will be triggered
        """
    }

Note that in the script block, any variable, even the one in bash
comments, such as in the last code block, need a definition, otherwise
error is triggered.

Also there are predefined variables in nextflow, summarized as below

| variableName | source  | description            |
|--------------|---------|------------------------|
| it           | channel | each item in a channel |

## Operators on channels

| operator | target  | description                        |
|----------|---------|------------------------------------|
| view     | channel | print out the content of a channel |
| flatten  |         |                                    |
| collect  |         |                                    |
| join     |         |                                    |
| map      |         |                                    |
| mix      |         |                                    |

## process control

### if-else

The if-else structure follows the same style in C and Java.

    params.p="hello"

    process ifelse {
            input:
            val x from params.p

            script:
            if(x == 'hello')
                    """
                    echo This is block 1 $x
                    """
            else if(x=="world")
                    """
                    echo This is block 2 $x
                    """
            else
                    """
                    echo This is a surprise $x
                    """
    }

It also has ternary expression like ‘a? a &gt; 10 : -1’.

### for-loop

It has two structures as below:

    for( int i=0; i<3; i++)
    {
        println "here is $i"
    }
    // or using a list
    names=['a','b','c']
    for(String el : names)
    {
        println("my name is $el")
    }

### when

Conditional execution

    params.do = true
    process {
        output:
        path 'out.txt' into out_ch
        
        when:
        params.do
        
        // the following code is run only when params.do is true
        script:
        '''
        echo "This is a conditional process" > out.txt
        '''
    }

Note that if a process is skipped, then its output is also skipped, so
one can’t rely on the output channel.

## File staging

nextflow stages files so that they can be cached/reused in future runs.
However, if the staging process was interrupted and the file was not
correctly staged, it will not report errors in the following runs. Need
be very careful. This issue was discussed
[here](https://github.com/nextflow-io/nextflow/issues/1552). If a
pipeline was interrupted forcibly, then one should delete the working
directory before resume/rerun the pipeline.

Note that for fromPath, the input can be a folder or file. If it is a
folder, the whole folder is staged. When providing inputs on command
line, if the path contains wildcard symbols such as ’\*’ and ‘?’, these
paths need be quoted, otherwise they will be expanded on the command
line and only first element is passed into program.

## Functions

One can define functions in a script as follows:

    int sum(int x, int y){
        return(x+y)
    }

One can also define closures as below:

    double={it * 2} // define a closure to double input. it is the implict variable
    double.call(4) // call the closure with argument 4
    sum={x,y -> x+y} // two arguments
    sum.call(5,6)

Some bultin functions:

| function           | purpose                                                                                                                  |
|--------------------|--------------------------------------------------------------------------------------------------------------------------|
| template           | load external script into a process. The script should exist in the templates folder, otherwise absolute path is needed. |
| log.info           | print out strings, like println                                                                                          |
| string.stripIndent | remove indent spaces from a multi-line string                                                                            |

## nextflow running options

| option         | description                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------|
| -resume        | continue from where last run stopped                                                                         |
| -process.echo  | print out the result from script blocks                                                                      |
| -with-docker   | use the docker environment setup in the nextflow.config file                                                 |
| -with-conda    | activate a conda environment by specifying an environment recipe file or its name                            |
| -with-report   | create execution report                                                                                      |
| -with-trace    | create file trace.txt containing running information for each task                                           |
| -with-timeline | show the time used by each task.                                                                             |
| -with-dag      | render workflow using direct acyclic graph, needing Graphviz installed if format other than html is needed.  |
| -w             | the folder in which tasks are run, default is ‘work’.                                                        |
| -preview       | go through the pipeline without running any tasks, good to generate workflow graph with the option -with-dag |

Note when specififying parameters, one need use double dashes, such as
*–greeting nextflow* to provide value for params.greeting.

## Directives

Directives defines optional settings that affects the execution of
current process, without affecting the semantic of the task itself. It
stays at the top of a process.

A complete list of directives is at
<https://www.nextflow.io/docs/latest/process.html#directives>.

A summary of the major directives is as follows:

| directive     | example                                     | explanation                                                                                                                                                                                                                                                                                                                                                       |
|---------------|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cpus          | cpus 2                                      | claim the number of cpus to use per task. If this is 2, and the number of tasks running in parallel is 4, then the machine needs 8 cpus.                                                                                                                                                                                                                          |
| memory        | memory ‘8.0 GB’                             | claim the amount of memory to use                                                                                                                                                                                                                                                                                                                                 |
| disk          | disk ‘2.0 GB’                               | disk amount required for the process.                                                                                                                                                                                                                                                                                                                             |
| tag           | tag “\$sampleId”                            | assign a label to a running task                                                                                                                                                                                                                                                                                                                                  |
| echo          | echo true                                   | let task to print out to standard output                                                                                                                                                                                                                                                                                                                          |
| container     | container ‘image/name’                      | docker container to be used by the workflow.                                                                                                                                                                                                                                                                                                                      |
| publishDir    | publishDir “/path/to/results”, mode: ‘copy’ | send the results to directory, otherwise task-specific output files are deleted upon completion. The directory can be remote, too. One can use –outdir to change this folder. ‘saveAs’ use a closure to accept filename as string and set output filename. Also note that the option ‘pattern’ is globbing, so ’\*’ won’t match any files prepended with folders. |
| errorStrategy | errorStrategy ‘ignore’                      | how to handle errors occured in a process. Available options are: terminate (terminate the whole pipeline immediately), finish (terminate after submitted jobs completed), ignore (ignore the error), retry (rerun the errored process).                                                                                                                          |
| maxErrors     | maxErrors 3                                 | the number of retries for the whole process across all tasks when errorStrategy is set to ‘retry’.                                                                                                                                                                                                                                                                |
| maxRetries    | maxRetries 2                                | the number of retries for a task (different from maxErrors) when errorStrategy is set to ‘retry’.                                                                                                                                                                                                                                                                 |
| label         | label ‘big\_mem4’                           |                                                                                                                                                                                                                                                                                                                                                                   |
| maxForks      | maxForks 4                                  | the number of tasks for this process to run in parallel.                                                                                                                                                                                                                                                                                                          |

Also note that all directives can be assigned dynamically such as using
ternary conditions, except the following three:

-   executor
-   label
-   maxForks

However, these directives can still be set based on other parameters
before the process starts. For example, one can choose to set executor
based on hostname:

``` yaml
def hostname = 'hostname'.execute().text.trim() // this variable must be defined in the same file as the process scope
process {
    withName: 'hello' {
    
        if(hostname=="linux-2") {
            executor='local'
        } else { // the else section can be omitted if using default
            executor='awsbatch'
        }
    
    }
}
```

## Operators

Operators are bultin functions that applied to channels and can be used
to transform, filter, fork, and combine channels. The full list of
operators is at <https://www.nextflow.io/docs/latest/operator.html>.

A summary of useful operators:

| operator    | example                                       | description                                                                                                                                                               |
|-------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| map         | numCh.map(it -&gt; it\*it)                    | transform each element using a function, here to get the squares.                                                                                                         |
| view        | myCh.view()                                   | print out the elements and each is appended a new line.                                                                                                                   |
| into        | myCh.into {aCh; bCh}                          | copy the source channel to each target channel.                                                                                                                           |
| mix         | myCh.mix(aCh,bCh)                             | merge all channels into one.                                                                                                                                              |
| flatten     | tupleCh.flatten()                             | tuples in a channel is flattened and each element is emitted separately.                                                                                                  |
| collect     | myCh.collect()                                | collect all elements into a list and emit as one; the opposite of flatten. Don’t use this on a file path, which will lead to a list of items separated by path separator. |
| groupTuple  | tupleCh.groupTuple()                          | group all tuples that have the same key into one tuple.                                                                                                                   |
| join        | leftCh.join(rightCh)                          | like ‘merge’ in R, merge two channels into one based on key match.                                                                                                        |
| branch      | myCh.branch{small: it &lt; 5; big: it &gt;=5} | return a multi-channel object, with labels as keys.                                                                                                                       |
| set         | Channel.from(1,2,34).set(numCh)               | set channel name                                                                                                                                                          |
| cross       | srcCh.cross(targetCh)                         | output only the source items whose keys (default: 1st item) have a match in the target channel. Like R’s merge() function.                                                |
| subscribe   | ch.subscribe { println “Got: \$it” }          | allow user to define a function to run on each emit element.                                                                                                              |
| collectFile | ch.collectFile(name:“outfile.txt”)            | store all emited elements into the specified file. can be used for both saving maps/lists as well as concatenating files.                                                 |
| combine     | ch1.combine(ch2)                              | combine two channels in the form of cartesian product, or based on a key given by option ‘by: pos’.                                                                       |
| concat      | ch1.concat(ch2,ch3)                           | concatenate the elements in multiple channels into one.                                                                                                                   |

### Note on groupTuple

One running `groupTuple()`, it will emit any elements until the input
channel is completed, which leads to blocking. One solution is to use
`groupKey()` to add size attribute to the grouping keys before applying
`groupTuple()`.

One can also sort the grouped items using a sort closure, such as

``` nextflow
Channel.of([1,'A'],[1,'B'],[2,'D'],[2,'A'])
    .groupTuple(
        sort: { a,b -> b <=> a}
    )
    .view()
```

Note that the closure function applies to the grouped items in each
group, here are the letters A, B, and D.

If one applies `groupKey(meta, size)` to a groovy map named `meta`, then
this map becomes a GroupKey object, see
<https://github.com/nextflow-io/nextflow/blob/master/modules/nextflow/src/main/groovy/nextflow/extension/GroupKey.groovy>.
Then some methods of a map such as `findAll()` will not work any more.
One solution is to get the map object back by using the method
`getGroupTarget()`. Also see the `groupKey()` definition here:
<https://github.com/nextflow-io/nextflow/blob/9c63e784f65e5a55a3dae59d02ba0582372634b8/modules/nextflow/src/main/groovy/nextflow/Nextflow.groovy#L376>

## Groovy language

[NextFlow](https://www.nextflow.io/) is a DSL implementation on Groovy
language, so it can run any Groovy and Java code.

Below is a summary of the major operations by Groovy language:

### Comments

The same as C-style syntax, one can use

    // single line comments

    /* comments
    block
    */

### Variables

There are global and local variables. Global variables are directly
created by assigning a value, such as

    x=1
    x=-3.14
    x="Hello"
    x=new java.util.Date()

While local variables are created using keyword *def* as

    def localX="for a closure or function"

#### Lists

In addition to simple variables, there are also lists. They are created
by putting elements in a square-bracket. The examples are below:

    list=[0,1,2,3]
    list[0] // get the first element
    list.get(0) // the same thing
    list.size() // get the list size
    list.reverse() // reverse the list
    list[-1] // last element
    list.unique() // unique elements
    list.min() // minimal element
    list.max() // maximum
    list.count(3) // count the element '3'
    list.sort() // sort elements
    list.flatten() // flatten out list elements to single-value elements
    list.sum() // total
    list.find{it % 2 == 0} // find first even elements
    list.findAll{it % 2 == 0} // find all even elements

#### Maps

Maps are more like dictionaries in other languages. It has all methods
implemented in
[java.util.Map](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html)
and [Groovy
API](http://docs.groovy-lang.org/latest/html/groovy-jdk/java/util/Map.html).
Below are some frequent operations:

    map=[a:1, b:2, c:3] // define a map
    map['a'] // get the element with key 'a'
    map.a // the same as above
    map.get('a') // the same as above
    map.put('z', 100) // add a value with key 'z'

### Strings

Strings can be defined by enclosing them in single or double quotes.
When using double quotes, it can use
‘$' for including variables or any expression, like '$var’ or
\${command/operation}.

Strings can also be defined using ‘/’ as delimiter, such as ‘/here/’,
often used for defining regular expressions. These are called slashy
strings.

Slashy strings can have multiple lines. Another way to have multi-line
strings is using triple single and double quotes. Note that slashy
strings and double-quote strings support variable interpolation.

### File operations

-   Convert a string to a file object: myFile=file(‘path/to/file’)

-   Get a file content as text: myFile.text

-   Get a file content as byte array for binary data: myFile.bytes

-   Save binary data to a file: myFile.bytes = binaryBuffer

-   Add new content to a file: myFile.append(‘line 1’)

-   Read lines as an array of strings: myFile.readLines()

## NextFlow configuration

The documentation can be found here
<https://www.nextflow.io/docs/latest/config.html>

### nextflow.config

This file hosts the settings for pipelines, and it may appear in
multiple locations. Here are the locations that a nextflow script
searches for settings in the order of decreasing priority (top ones
override bottom ones):

1.  values provided with command line as –option ‘value’.

2.  values set in file provided by -params-file.

3.  values set in file provided by -c ‘config-file’.

4.  file `nextflow.config` in current folder.

5.  file `nextflow.config` in the workflow project folder.

6.  file \$HOME/.nextflow/config.

7.  values defined in pipeline script itself.

If one doesn’t want to use default nextflow.config files mentioned
above, but only user-specified one, use the option ‘-C user.config’
(note capitalized *C* is used here).

One config file can include other config files using the keyword
*includeConfig*.

**Note** that in a config file, a value set later will override the
value set earlier, including the sections imported with the keyword
*includeConfig* and defined in *profiles*. Therefore, it is very
important to make sure the order of the sections match the need of
priority expectation: put high-priority settings at later sections.

Also when specifying multiple profiles like ‘-profile a,b’, then the
profile defined later has higher priority than the one defined earlier.
So if profile ‘a’ is defined later, then its setting has higher priority
than ’b’s.

### Syntax

The syntax to define variales in config files are as follows:

> name = value

1.  Note that value has type: characters should be quoted, while numbers
    and logical (true or false) should not be quoted.

2.  The variables defined in config file can be used in other variables
    in the format of \$configVar or \${configExp}.

3.  The environment variables defined in host such as \$PATH, \$PWD, etc
    can also be used in config file.

4.  The same comment syntax is used in config file, i.e., ‘//’ or ’/\*
    comment \*/’.

5.  variables can be in a scope by adding a prefix, such as ‘params.x’.
    There are two ways to define variables in a scope,

<!-- -->

    params.x="way 1"

    params {
        x="way 2"
        y="extra"
    }

Note that variables defined in the same scope can be used directly
without prefix and override any variables defined outside, for example:

    params.X = "outsideX"

    params {
        X = "globalX"
        
        vars {
            X = "localX"
            Y = "This $X is always 'localX', overriding globalX"
            Yp = "This ${params.X} is affected by input parameters, default is 'globalX'"
        }
    }

    // test with the following code
    println ${params.vars.X}
    println ${params.vars.Y}
    println ${params.vars.Yp}

Major scopes/variables

| scope   | description                                                                                                                             |
|---------|-----------------------------------------------------------------------------------------------------------------------------------------|
| params  | Define parameters used in script. The precedence for parameters are as follows: command line &gt; nextflow.config &gt; workflow script. |
| env     | export variables to the environment where workflow tasks to execute.                                                                    |
| process | set process directives, such as cpus, memory, and container.                                                                            |

### Important variables

| variable      | scope   | example                                                   | description                                                                                                                                                    |
|---------------|---------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| executor      | process | process.executor = “awsbatch”                             | set the deployment cluster                                                                                                                                     |
| queue         | process | process.queue = “myqueue”                                 | set the queue in the cluster/environment                                                                                                                       |
| cpus          | process | cpus = 4                                                  | the number of cpus for a task execution                                                                                                                        |
| memory        | process | memory = ‘10 GB’                                          | the needed memory for a task execution                                                                                                                         |
| disk          | process | disk = “100 GB”                                           | the disk storage required by a task                                                                                                                            |
| workDir       | N/A     | workDir=“s3://aws/data/dir”                               | the directory where tasks temporary files are created, one can use ‘-w /new/path’ to set it on cmdline                                                         |
| region        | aws     | aws.region = “us-east-1”                                  | the AWS region for awsbatch                                                                                                                                    |
| batch.cliPath | aws     | aws.batch.cliPath = ‘/home/ec2-user/miniconda/bin/aws’    | path to ‘aws’ command                                                                                                                                          |
| batch.volumes | aws     | aws.batch.volumes = \[‘/tmp’, ‘/host/path:/mnt/path:ro’\] | attach host volumes to docker; the setting applies to all processes                                                                                            |
| baseDir       | global  |                                                           | The directory where the main workflow script is located (deprecated in favour of projectDir since 20.04.0).                                                    |
| launchDir     | global  |                                                           | The directory where the workflow is launched (requires version 20.04.0 or later).                                                                              |
| moduleDir     | global  |                                                           | The directory where a module/process script is located for DSL2 modules or the same as projectDir for a non-module script (requires version 20.04.0 or later). |
| nextflow      | global  |                                                           | Dictionary like object representing nextflow runtime information (see Nextflow metadata).                                                                      |
| params        | global  |                                                           | Dictionary like object holding workflow parameters specifing in the config file or as command line options.                                                    |
| projectDir    | global  |                                                           | The directory where the main script is located (requires version 20.04.0 or later).                                                                            |
| workflow      | global  |                                                           | Dictionary like object representing workflow runtime information (see Runtime metadata).                                                                       |

One can use the following variables in nextflow.config to choose and set
the environment for running the workflow:

    // using docker
    process.container="image/name"
    docker.enabled = true
    // use singularity, can also use library://, shub://, docker://, docker-daemon:// protocols
    process.container="path/to/file.sif"
    singularity.enabled = true
    // configue conda environment, provide an environment or YAML file to build environment
    process.conda = "path/to/environment"

### Bulk-set attributes

One can use the following ways to set attributes (resources, containers,
etc) for processes or pipelines:

1.  “withName: procName {}”: set attributes for processes by name.
    ‘procName’ can be regular expression such as ‘abc\|def’ (matching
    two processes) and ‘!bar’ (not process ‘bar’).

    The *withName* selector applies to a process even when it is
    included from a module under an alias. For example,
    `withName: hello` will apply to any process originally defined as
    *hello*, regardless of whether it is included under an alias.
    Similarly, it will not apply to any process not originally defined
    as *hello*, even if it is included under the alias *hello*.

2.  “withLabel: ‘procLabel’ {}”: set attributes for processes by label,
    also accept regular expression as above.

3.  profiles: set execution profile (see below) for the whole pipeline.

A profile is a set of configuration attributes that can be
activated/chosen when launching a pipeline execution by using the
-profile command line option. An example is shown below:

    profiles {

        standard {
            params.genome = '/local/path/ref.fasta'
            process.executor = 'local'
        }

        cluster {
            params.genome = '/data/stared/ref.fasta'
            process.executor = 'sge'
            process.queue = 'long'
            process.memory = '10GB'
            process.conda = '/some/path/env.yml'
        }

        cloud {
            params.genome = '/data/stared/ref.fasta'
            process.executor = 'awsbatch'
            process.container = 'cbcrg/imagex'
            docker.enabled = true
        }

    }

The *standard* profile is the default one, and others can be specified
with the option ‘-profile’.

One can specify multiple profiles, such as `-profile cluster,standard`,
then the one appearing later in the config file (here `cluster`) will
override the same options in the earlier profiles.

4.  Selector priority When one attribute is set in multiple places, the
    one with higher priority will replace the one with lower priority,
    and the priority is as follows:

    1.  Process configuration settings (without a selector)

    2.  Process directives in the process definition

    3.  withLabel selectors matching any of the process labels

    4.  withName selectors matching the process name, such as
        `withName:bar`

    5.  withName selectors matching the process included alias, such as
        `withName:bar` and `bar` is an alias of process `hello`

    6.  withName selectors matching the process fully qualified name,
        such as `withName: 'wf:bar'` will override the setting by
        `withName:bar`

    Also note that if the same selector shows multiple times, then the
    last one takes priority, and the settings will be merged, for
    example:

        withName: bar {
            cpus = 4
            memory = 4.GB
        }

        withName: bar {
            memory = 8.GB
            time = '1.d'
        }

    is equivalent to

        withName: bar {
            cpus = 4
            memory = 8.GB
            time = '1.d'
        }

5.  Selector syntax

    Note that one can refer to input channels of a process when
    configuring it using selectors in any configuration files such as
    conf/modules.config, nextflow.config, for example, here the process
    `fastqc` uses the input `reads`. See below:

    ``` yaml
    process {
        withName: 'fastqc' {
            cpus = { reads.size()*task.attempt }
            tag = { "Processing ${reads}" }
        }
    }
    ```

    However, note that for processes which accept multiple files as one,
    such as `reads`, it will be an array, so one need to treat it
    accordingly (instead of the above, one need to use
    `reads*.size().sum()` to calculate total size); when only one file
    is given as input, the variable automatically changes into a single
    value from array, so this special case also needs to be taken care
    of.

    Note that the dynamic directives need to be provided in curly braces
    and assigned with a equal sign.

    Also in the selectors, or the process scope, one can use the groovy
    control syntax to determine the operations. For example, in the
    following example, one can determine whether to setup cpus based on
    host IP address:

    ``` yaml
    def host_ip = InetAddress.localHost.hostAddress
    process {
        withName: 'fastqc' {
            if(host_ip=='192.168.1.11') {
                cpus = 4
            }
        }
    }
    ```

    Also note that when setting dynamic directive in configuration files
    instead of in process files, the referred groovy/java/nextflow
    classes need to given in full path, so

        def minTime = Duration.of('1d')

    will not work in configuration files, and it should be

        def minTime = nextflow.util.Duration.of('1d')

    To find the full path for classes, search google.

## Cloud deployment

### AWS batch

1.  credentials

    nextflow will find aws credentials in the following order:

    1.  Looking for the following environment variables:
        -   AWS\_ACCESS\_KEY\_ID
        -   AWS\_SECRET\_ACCESS\_KEY
        -   AWS\_DEFAULT\_REGION
    2.  read \~/.aws/credentials or \~/.aws/config for such information.
    3.  or it can be configured in nextflow config file using variables
        ‘aws.accessKey’, ‘aws.secretKey’, and ‘aws.region’; look at
        <https://www.nextflow.io/docs/latest/config.html#config-aws>

2.  AWS-cli tools

    Nextflow requires to access the AWS command line tool (aws) from the
    container in which the job runs in order to stage the required input
    files and to copy back the resulting output files in the S3 storage.

    The aws tool can either be included in container image(s) used by
    your pipeline execution or installed in a custom AMI that needs to
    used in place of the default AMI when configuring the Batch
    Computing environment. For the latter, one can start an EC2 instance
    and install awscli using conda, and create an AMI from it. Don’t use
    pip to install awscli, which may not work in container. Finally use

        aws.batch.cliPath = '/home/ec2-user/miniconda/bin/aws'

    to specify the path where aws is installed in the AMI.

3.  Nextflow creates job definitions (tasks and containers) and jobs to
    run on aws batch, but users need create computer environments and
    awsbatch queues to run the jobs. Each process in the job can use
    different queue and docker images if necessary.

4.  Docker images

    The container image(s) must be published in a Docker registry that
    is accessible from the instances run by AWS Batch eg. Docker Hub,
    Quay or AWS ECS Container Registry.

5.  Container properties When nextflow define a batch job, it sets
    container properties (see [this
    page](https://docs.aws.amazon.com/batch/latest/APIReference/API_ContainerProperties.html)).
    The properties include command to run and cpu/memory limits usable
    by a container. nextflow may put a very low value for cpus and
    memory, leading to the container killed when running a job task. It
    is always safer to specify the memory/cpu resource when using docker
    image in a nextflow process.

6.  Monitor jobs

    When a job is submitted to an AWS batch queue, one can go to AWS
    batch queue console to see the status of running jobs. In the log
    stream page, one can see the progress of a job running. The
    ‘container’ section shows the command called and the resources such
    as cpus and memory assigned.

7.  Compute environment

    Compute enviroment is associated with an AWS batch queue, and
    determines how resources are allocated in the queue. One can let AWS
    assign any EC2 instance types according to resource requests, or
    select a list of EC2 instances for the queue to choose from. Note
    that it is important to specify a diverse of EC2 instances if you do
    the latter, otherwise nextflow jobs may be stuck at `runnable` for a
    long time due to lack of specified instance types.

    Also the request memory is better to smaller than the available
    memory in the target instance. For example, if an instance has 16GB
    memory, then the request can be 15GB; if 16GB is requested, then
    this 16GB memory may not satisfy the request and thus won’t be
    assigned to the requesting task.

    One can update compute environment associated with a AWS batch queue
    so that new jobs with use the new settings. But note that if some
    tasks are using a compute environment when updating, the tasks will
    be terminated (and requeued) after a certain time (given by the
    timeout option) if the compute enviroment is updated. So it is
    better to update compute environment when no taks are running in it.

## Monitoring workflow

One can monitor the running a pipeline/workflow using the *workflow*
object, such as

    println "Project : $workflow.projectDir"
    println "Git info: $workflow.repository - $workflow.revision [$workflow.commitId]

The table below lists the properties accessible from the *workflow*
object:

| Name            | Description                                                                                                                                             |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| scriptId        | Project main script unique hash ID.                                                                                                                     |
| scriptName      | Project main script file name.                                                                                                                          |
| scriptFile      | Project main script file path.                                                                                                                          |
| repository      | Project repository Git remote URL.                                                                                                                      |
| commitId        | Git commit ID of the executed workflow repository.                                                                                                      |
| revision        | Git branch/tag of the executed workflow repository.                                                                                                     |
| projectDir      | Directory where the workflow project is stored in the computer.                                                                                         |
| launchDir       | Directory where the workflow execution has been launched.                                                                                               |
| workDir         | Workflow working directory.                                                                                                                             |
| homeDir         | User system home directory.                                                                                                                             |
| userName        | User system account name.                                                                                                                               |
| configFiles     | Configuration files used for the workflow execution.                                                                                                    |
| container       | Docker image used to run workflow tasks. When more than one image is used it returns a map object containing \[process name, image name\] pair entries. |
| containerEngine | Returns the name of the container engine (e.g. docker or singularity) or null if no container engine is enabled.                                        |
| commandLine     | Command line as entered by the user to launch the workflow execution.                                                                                   |
| profile         | Used configuration profile.                                                                                                                             |
| runName         | Mnemonic name assigned to this execution instance.                                                                                                      |
| sessionId       | Unique identifier (UUID) associated to current execution.                                                                                               |
| resume          | Returns true whenever the current instance is resumed from a previous execution.                                                                        |
| start           | Timestamp of workflow at execution start.                                                                                                               |
| manifest        | Entries of the workflow manifest.                                                                                                                       |
| ✝ complete      | Timestamp of workflow when execution is completed.                                                                                                      |
| ✝ duration      | Time elapsed to complete workflow execution.                                                                                                            |
| \* success      | Reports if the execution completed successfully.                                                                                                        |
| \* exitStatus   | Exit status of the task that caused the workflow execution to fail.                                                                                     |
| \* errorMessage | Error message of the task that caused the workflow execution to fail.                                                                                   |
| \* errorReport  | Detailed error of the task that caused the workflow execution to fail.                                                                                  |

Also there are two handlers to handle the workflow:

| Handler             | Description                           |
|---------------------|---------------------------------------|
| workflow.onComplete | what to do when the pipeline complete |
| workflow.onError    | what to do when error occured         |

## DSL2

DSL2 is an extension of previous syntax, to enable it, one need put
`nextflow.enable.dsl=2` at the beginning of the workflow script.

The DSL2 has the following features:

### Functions

    def <function name> ( arg1, arg, .. ) {
        <function body>
    }

Functions return the result of the last statement. To explicitly return
a result, use the keyword `return`.

Note that functions don’t accept default arguments, so one has to call a
function with all arguments all the time. For example, the following
doesn’t work:

``` nextflow
def f(a, b=10) { a + b }
// you can't call
f(1)
// you need call
f(1, 20)
```

### Process

The new syntax is the same as the old one in defining process, and the
only difference is to omit the ‘from’ and ‘into’ channel declaration,
and then the process will be invoked in the workflow scope just like a
function (so no invocation during the definition of process). Note that
a process component can be invoked only once in the same workflow
context.

An example is as follows:

    nextflow.enable.dsl=2

    process foo {
        output:
          path 'foo.txt'
        script:
          """
          your_command > foo.txt
          """
    }

     process bar {
        input:
          path x
        output:
          path 'bar.txt'
        script:
          """
          another_command $x > bar.txt
          """
    }

    workflow {
        data = channel.fromPath('/some/path/*.txt')
        foo()
        bar(data)
    }

In this way, one can use process composition like proc1(proc2()) as long
as proc2’s output matches the requirement of proc1’s input. The output a
process can be reached like proc.out. When a process defines two or more
output channels, each of them can be accessed using the array element
operator e.g. out\[0\], out\[1\], etc. or using named outputs.

To name a output channel which can be used in external scope, one can
use syntax like `path '*.bam', emit: samples_bam`.

### Workflow

one can use the *workflow* keyword to define sub-workflow, which can be
called in other workflow definitions. See the below example:

    nextflow.enable.dsl=2
    // define process
    process abc {
        output:
            val x
        
        script:
            x="Excellent nextflow"
    }

    process ddd {
        input:
            val x
        output:
            stdout
        
        script:
            """
            echo "Hello world: $x"
            """
    }

    // define sub-workflow component
    workflow sub_flow {
        word=abc()
        res=ddd(word)
        res.view()
    }

    // triger workflow
    workflow {
        sub_flow()
    }

A workflow definition which does not declare any name is assumed to be
the main workflow and it’s implicitly executed. Therefore it’s the entry
point of the workflow application. An alternative workflow entry can be
specified using the -entry command line option.

To refer to a process in a workflow component, one can use the format
like ‘sub\_flow:abc’, here it refers to the ‘abc’ process in workflow
‘sub\_flow’. This reference can be used in nextflow.config file to setup
configurations for a specific process, especially when one process is
invoked in multiple workflows.

A workflow may contain the following 4 main segments: take, main, and
emit. An example as follows:

``` nextflow
include { foo } from '../some/module.nf'

workflow {
    // use take to list input channels
    take:
        x
        y
    // main contains the running processes/workflows
    main:
        foo(x,y)
    // emit to set output channels
    emit:
        foo.out
        res = foo.out // a named version
}
```

Note that when calling a workflow in another script/workflow, one can’t
assign it to a variable and then use the variable to access the result.
As an example:

``` nextflow
process proc1 {
    ...
}

workflow wf1 {
    ...
}

workflow {
    procRes=proc1() // valid for process
    procRes.out.view()
    wf1() // can't assign to a variable
    wf1.out.view() // the only way to view workflow outputs
}
```

**Same-name workflows and processes**

Also note that the same-named process can’t be included in the same
workflow, but can be in different workflows.

One can’t call the same workflow more than once in the same workflow
context (even different input parameters). This is valid because if the
same workflow is called twice and then it is confusing from which call
the results come from.

### Module

A module can contain the definition of a function, process and workflow
definitions. And module can be included or shared among workflow
applications. Just like python modules. One example of including a
module is as below:

``` nextflow
include { foo; bar } from './some/module'

workflow {
    data = channel.fromPath('/some/data/*.txt')
    foo(data)
}
```

Note all the module paths should start with ‘./’, ‘../’, or ‘/’.

Including a module is equivalent to copy the relevant code from the
module into the current pipeline, unless some modifications made (see
below). So the included processes/workflows use current pipeline’s
configurations.

When including a process from a module file, all code outside processes
are also run, so channels and parameters defined outside processes are
run, but these channels/parameters are invisible in current workflow,
and so not usable. However, including a workflow has no such issue: the
variables defined outside included workflows are available in that
workflow, so one needn’t worry about that.

When including a module component it’s possible to specify a name alias.
This allows the inclusion and the invocation of the same component
multiple times in your script using different names: this is essential
if one wants to use the same process multiple times in the same
workflow.

``` nextflow
include { foo } from './some/module'
include { foo as bar } from './other/module'

workflow {
    foo(some_data)
    bar(other_data)
}
```

Note that when including a module, by default, the parameters defined in
current including main script will override those with the same names in
the included modules (assuming the main script’s parameters are defined
before module inclusion, otherwise the module values will be taken).

To avoid this issue, one can use the option *params* to specify one or
more parameters from the included module and set values, and these
values are not affected by the including script’s environment, nor by
command line inputs. And for module-specific parameters that are not
specified in *params*, they use the values set in the module, not
changeable by including script or command line values.

Let’s take the following module as an example:

``` nextflow
nextflow.enable.dsl=2

// this parameter is also defined in including parameter too.
params.globalInput="global input in module"
// the following parameters are module-specific
params.moduleInput="module input"
params.moduleInputNoChange="module input no change"

workflow wf_module {
    log.info """
    In workflow wf_module:
    globalInput: ${params.globalInput}
    moduleInput: ${params.moduleInput}
    moduleInputNoChange: ${params.moduleInputNoChange}
    """
}
```

And when one uses the following to include the module using the options,
we will see some interesting output:

``` nextflow
//
nextflow.enable.dsl=2
// global parameter
params.globalInput="global input in main"
include { wf_module as wf1 } from "./wf_module.nf" params (
    globalInput: "global input set in params",
    moduleInput: "module input set in params"
)

workflow {
    wf1()
    // the main script has no access to the two module-specific parameters
    // moduleInput and moduleInputNoChange, unless they are
    // specified in command to implicitly added these two parameters
}

/* expected output (run without command params setting):
    In workflow wf_module:
    globalInput: global input set in params
    moduleInput: module input set in params
    moduleInputNoChange: module input no change // set by module
*/
```

**Since version 24.07.0-edge: parameters should be used in the entry
workflow and passed to workflows, processes, and functions as explicit
inputs. So the methods such as *addParams* and *params* are deprecated**

Another way to set module-specific parameters is to use the option
*addParams*. Different from *params*, *addParams* exposes all parameters
in the module, even those not specified in *addParams*. All the
parameters set in the included module can be changed by the including
script or command line, making it vulnerable to parameter changes,
because change in one place may change the value for all
processes/workflows using the parameter. Also these added
module-specific parameters are not accessible in the including script,
too, unless the same-name parameters are specified at the command line.

Let’s have a look at an example. Using the above *wf\_module* as
included module:

    nextflow.enable.dsl=2

    params.globalInput="global input in main"

    // use addParams to add user-specific params
    include { wf_module as wf2} from "./wf_module.nf" addParams (
        globalInput: "global input added",
        moduleInput: "module input added"
    )
    workflow {
        wf2()
    /* expected output without command line params setting
        In workflow wf_module:
        globalInput: global input in main // not affected by addParams because it was set before this.
        moduleInput: module input added // set by addParams
        moduleInputNoChange: module input no change // use the module value
    */
    }

Note that the parameters set for an included process/workflow are bound
to that included process name, even a separate inclusion uses a
different parameter, below is an example:

    nextflow.enable.dsl=2

    include { print_msg as msg1 } from \
        '../process/msg.nf' addParams (
            msg: "workflow msg1"
            )


    include { print_msg as msg2 } from \
        '../process/msg.nf' addParams (
            msg: "workflow msg2"
            )


    workflow {
        msg1() // output: workflow msg1
        msg2() // output: workflow msg2
    }

And the process `print_msg` is simply a process to print out the
parameter `msg`, and defined as below:

    params.msg="This is default msg in msg.nf"
    process print_msg1 {
        echo true

        script:
        """
        echo ${params.msg}
        """
    }

Also note that the command line parameter setting does not overrides
that set by addParams(), so if, for the above example, one provides
‘–msg “command line msg”’ on command line, then msg1() and msg2() will
still print out old message.

Bug report: 08/01/2022, nextflow version 21.10.6 build 5660. When the
parameter names have uppercase letters, the statement in the last
paragraph isn’t true, and all the paramters using ‘addParams()’ will be
overriden by global or commandline parameters. For example, in the
following setting, `params.msG` is always “message in main”:

    params.msG="message in main"

    include { print_msg } from \
        'process.nf' addParams (
            msG: "setting a message which will be always overriden by main"
        )

Update: 08/01/2022 This bug remains there in nextflow version 22.04.5

### Channel forking

Channel is automatically forked when it is consumed by multiple
processes, so no more need *into* operator.

### Pipes

One can use the pipe `|` and the *and* `&` operator in workflow to
connect predefined processes and functions. For example:

    process foo {
      input: val data
      output: val result
      exec:
        result = "$data world"
    }

    process bar {
        input: val data
        output: val result
        exec:
          result = data.toUpperCase()
    }

    workflow {
       channel.from('Hello') | map { it.reverse() } | (foo & bar) | mix | view
    }

in the above snippet the channel emitting the Hello is piped with the
map which reverses the string value. Then, the result is passed to
either foo and bar processes which are executed in parallel. The result
is pair of channels whose content is merged into a single channel using
the mix operator. Finally the result is printed using the view operator.

## Triger nextflow from git repos

One can find more info at
<https://www.nextflow.io/docs/latest/sharing.html>.

Briefly, one needs to create a file `~/.nextflow/scm` file and store the
credentials for corresponding git providers. For example, for gitlab,
the file may look like this

    providers {
        gitlab {
            user = 'gitlab-username'
            password = 'use-gitlab-token'
        }
    }

Then one can run a pipeline by typing

    nextflow run https://gitlab.com/path/to/repo.git

Note that the short form

    nextflow run -hub github path/to/repo

may only work for github repos.

## Tricks

1.  Methods to convert a groovy map to string

    -   Map.inspect(): all strings are quoted, good for strings with
        spaces
    -   Map.toMapString(): convert to a string, similar to
        `Map.inspect()`, but strings are not quoted
    -   JsonOutput.toJson(myMap): convert to a json string. Note that
        any value with ‘/’ must be quoted as strings, otherwise
        JsonOutput will reports the error ‘Unexpected error
        \[StackOverflowError\]’.

## Caveats

1.  Zero is treated as false in logical test.
    `a=0     if(! a) {         // this will be printed         println "0 is false in groovy"     }`

2.  When a file channel is created from a string containing wildcard
    symbols, the order of the files in the channel is unknown, and may
    vary among operating systems. Below is an example:

        file_ch = Channel.fromPath('dataDir/{total,perc,meth}*.txt.gz').collect()
        file_ch.view()
        /* output in aws ubuntu instance, and this order may change in other systems
        [meth_cov_matrix_CpG.txt.gz, perc_matrix_CpG.txt.gz, total_cov_matrix_CpG.txt.gz]
        */

    To ensure the right file is used, one need find the filenames or
    emit the files into individual channels.

3.  If an input channel is empty, then the process won’t be run at all,
    so the whole pipeline will exit silently without error. One solution
    is that one can provide a default value when a channel is empty, so
    that the process can run and check the received value and respond
    accordingly.

4.  The symbol ‘' is a special variable in nextflow for escaping
    characters. If one wants to use it in shell command, it has to be
    escaped by using double backslashes’\\‘; otherwise nextflow may
    interpret the script code in an unexpected way. For example, in the
    following code, double backslashes are used in front of’+’ sign.

        script:
        """
        o="dmr_test.a_vs_b"
        label=\$(echo \$o | sed -e 's/^dmr_[^.]\\+.//');
        echo \$label
        """

5.  There are two ways for one to write values into a file: (1) via
    Channel’s collectFile() operator, (2) via the methods of the Path
    object. The below are two examples:

    ``` nextflow
    // via Channel
    myStr="hello world"
    Channel.of(myStr).collectFile(name:"/path/to/outfile")
    ```

        // via Path
        myFile=file("/path/to/outfile")
        myFile.text=myStr

    Note that there are some key differences between the two ways:

    -   The *Path* operation needs the outdir already exists (unless it
        is an AWS S3 path), otherwise it reports error. The *Channel*
        operation has no this issue.

    -   If one file is operated by a Channel, this file seems not
        operable by the *Path* operation in the same nextflow process.

## Plugins

### nf-validation, renamed to nf-schema

To update the code from nf-validation to nf-schema, please see the
migration guide at
<https://nextflow-io.github.io/nf-schema/latest/migration_guide/>.

Please check the repo here <https://github.com/nextflow-io/nf-schema>.

Here are some useful functions from the plugin:

-   paramsHelp: print help messages

-   paramsSummaryLog: print a log of non-default values in a pipeline
    run

-   validateParameters: validate input parameters

-   Channel.fromSamplesheet: read and validate samplesheet, and create a
    samplesheet channel.

## Cool facts

1.  When resuming a pipeline run by using a new working directory, it
    will not invalidate the finished tasks. For example, if one uses one
    s3 bucket for a run, and then use another s3 bucket to resume the
    run, then finished tasks will just read from cache.

    Also when re-running a pipeline, it will determine whether to rerun
    a task based on the following things:

    -   input values, files, and commands,
    -   environments such as containers.
    -   status of previous run, success?
    -   the output files/paths.

    The last one is very important: if the output filename/path changes
    when re-running, the task will be rerun. A bad practice is to use
    task id in the output filename/path, so please avoid this.

2.  In nextflow workflow and process definitions, use the ‘def’ define
    local variables as much as possible, unless the variables are
    expected to be global. The variables in the map {} closure without
    `def` are also global variables. These same-name variables may be
    modified by other channels and process, leading to racing conditions
    among global variables.

    Related to this, when a pipeline uses a map to propogate meta
    information along the pipeline, it had better not to modifying the
    map, because such modification may interfere with other processes
    using the same map. This will cause troubles, and become obvious
    that some finished tasks are re-executed when resuming. Therefore,
    the suggested solution is to use the operator ‘+’ to create a new
    map when necessary or `clone()` it before modification.

3.  Note that the `join` operator is different from the SQL’s join,
    because it expects unique key values from each channel, and each
    time a matched key is found between two channels, the key is emitted
    and consumed and it won’t wait for other items with the same key. By
    contrast, the operator `combine` allows duplicated keys.

4.  There is no way to convert a nextflow channel (no matter what type:
    valuel, queue, etc) to a groovy list or map. A workaround is to save
    the channel to a file and then read back using groovy function. But
    this won’t work for channel processes because the function may have
    not been executed when a channel is reading the returned values from
    the function.

5.  nextflow aws batch container working dir is the one specified by the
    environment variable TMPDIR, default to /tmp.

6.  In nextflow, changing workdir does not invalidate the completed
    tasks, so resume will use the cached results, this also applies to
    aws batch. Therefore, one can speficify a different workdir when
    resuming a failed job.

7.  One can’t assign a process name to another name, unless using alias
    during include step.

        include { proc_a as proc_b } from './process.nf' // work
        proc_c = proc_b // not work

8.  When using AWS batch to run nextflow, S3 bucket is more efficient
    than EFS in saving big datasets: the former is more robust and
    scalable (parallelization), while the latter can fail in data
    transfer, even though EFS is way more expensive. So choose S3 as
    output dir instead of EFS volumes.

9.  Enabling virtual threads in Java (available from Java 19) slows down
    job submission speed, not as described in this post:
    <https://nextflow.io/blog/2024/optimizing-nextflow-for-hpc-and-cloud-at-scale.html>,
    so just set *NXF\_ENABLE\_VIRTUAL\_THREADS=false*

10. If a job needs to take longer time to transfer data to/from S3, set
    the following parameter in nextflow.config to a bigger value
    (default: 12 hours):

        threadPool.publishDir.maxAwait=48.h

11. When a process task fails, it can be re-submitted for execution. The
    process directive *maxRetries* can be used to control how many
    resubmissions. But note that if a task fails due to *spot* instance
    outbid, the failure is not counted into re-submissions.

12. When setting up AWS batch compute environments, one can either use a
    pre-built AMI, or use a launch template for new instances in the
    compute environment. Note that using launch template also needs a
    source AMI which can pre-installed some tools. The advantage of
    launch template is that one can change many settings of new
    instances without creating a new AMI, such as (1) change attached
    volume size and properties,

    2.  instance types, (3) security groups, etc; of course, many of
        these except (1) can also be set when setting a compute
        environment.

13. When specifying input and output channels in a process, if a folder
    is provided, there is risk that the folder may not be fully
    transferred when one resumes a failed pipeline run. So it is always
    safer to pass files using the format like ’folder/\*.gz’.

14. When running a pipeline, nextflow will add the *bin/* folder located
    in the same folder as the nextflow script to the variable *PATH*,
    however, depending on the executor, this *bin/* folder can be added
    at the beginning or at the end of *PATH*:

    -   at the beginning: awsbatch
    -   at the end: docker, local

15. To run a pipeline in hybrid mode, one need to specify the working
    directories for remote tasks (e.g., running on aws batch) and local
    tasks separately, using the command option -bucket-dir and
    -work-dir, respectively, because the remote tasks must use S3
    buckets while the local tasks can’t use S3 buckets at all.

    Actually, one can also set the following variables in the
    configuration files such as *nextflow.config* to get the same
    effect:

    ``` nextflow
    workDir = "/path/to/local/dir"
    bucketDir = "s3://aws-bucket/subfolder"
    ```

16. How does nextflow publish files when using aws batch as the
    executor?

    Nextflow publish files in the following steps:

    1.  finish the running task, generating all output files
    2.  copy all output files to a work directory in AWS S3; this step
        is done by the task’s EC2 instance. The speed is determined by
        the parameter `aws.batch.maxParallelTransfers` and the number of
        available CPUs on the EC2 instance. After this is done, the
        task’s EC2 instance will be terminated or used for another
        pending task.
    3.  copy the output files from the work directory to the final
        output folder given by the `publishDir` directory; this is done
        by the machine launching the workflow.

    Note that both step b and c can take significant time when output
    files are big.

## FAQs

1.  How to feed a program with multiple input files?

    A: Use ==path fs from Channel.fromPath("/path/\*.fa").collect()==,
    where `fs` will contain all the files.

2.  How to merge all output files into one file?

    A: one can use collectFile() operator to collect all the values
    emitted from a channel.

    Note that when one uses this method, the outpuut file path (provided
    via the option *name*) must be an absolute path and the prepending
    folder must exist, making it less flexible. One workaround is to
    save these files using collectFile() first and then use the operator
    subscribe to copy the files into target folder, like:

        def ch_files = my_channel.collectFile(name: "target.tsv")

        ch_files.subscribe { f -> f.copyTo("${params.outdir}") }

3.  How to run a process in parallel?

    A: one can check an FAQ at
    <https://www.nextflow.io/docs/latest/faq.html>. Basically, one need
    create a channel to hold all input values, and then call this
    channel as input in a process, which will trigger the process on
    each of the input values.

4.  Nextflow pipeline hangs without completion, why?

    A. Possible reasons: (1) a channel is explicitly created using
    Channel.create(), and it needs be closed using ch.close(), otherwise
    the pipeline will not stop.

5.  The cached files are not updated even though input files have
    changed. Why?

    A. This can happen when input files are localed at AWS S3 and the
    executor is local and workdir is also in a local directory. In this
    case, even though files in the remote S3 folders have changed, the
    pipeline may not update local cache when re-run the pipeline, no
    matter -resume is used or not.

6.  A nextflow pipeline may not re-run and report error like
    \[UnsupportedOperationException\]. Why?

    A. This is more likely caused by existing files in S3 and the
    pipeline tries to rename it, but this renaming/moving operation in
    S3 is not supported by nextflow. One well known issue is the
    trace.txt file. One solution is that add “overwrite=true” to the
    ‘trace’ scope; or alternatively change trace dir to a different
    folder when re-running a pipeline. The same issue may exist for
    report, timeline, and dag; if it is necessary, add “overwrite=true”
    to those scopes, too.

7.  Can I stop a pipeline run by ‘Ctrl-C’?

    A: Yes, you can, especially when the run hangs. But be prepared that
    some weird issues may pop up when you resume the run later (with
    option -resume). Nextflow caches results and reuse them when a run
    is resumed. However, if a file transfer (staging) or writing is
    interrupted by a user, the resumed run may pick up these truncated
    or missing (if applicable) files, yielding wrong results or causing
    a breakdown. Therefore, ideally one should let a pipeline to finish
    started tasks before exiting when errors happened, rather than force
    stopping the run by ‘Ctrl-C’. If weird things happen, try to run
    pipelines without ‘-resume’, which may fix the issues.

8.  Can I set dynamic label for a process?

    A: If the variables used in dynamic label come from the inputs in
    the process or the attributes of `task`, the answer is NO. However,
    if the variable is defined in the scope outside the process, then it
    is YES. See the discussion
    [here](https://github.com/nextflow-io/nextflow/issues/894).

    Actually, all process directives can accept dynamic values (thus
    input variables) except the following 3 directives: executor, label,
    and maxForks, so only these 3 directives need variables defined
    outside process scope. One can find more about dynamic directives
    [here](https://www.nextflow.io/docs/latest/process.html#dynamic-directives).

    Also note that dynamic directive has higher priority than the
    settings in the configuration files.

9.  How to get store the size of a channel into a variable?

    A: This is actually not doable in nextflow due to the static nature
    of groovy language. To get the number of files in a channel, and
    assume the string `params.infiles` contains the filename string
    (with wildcards), one can do the following:

    ``` nextflow
    numFiles = file(params.infiles).size()
    // then numFiles can be used as a variable in comparison
    if(numFiles > 100) {
        println "Too many files"
    } else {
        println "Just right"
    }
    ```

10. How to run a pipeline under a different AWS account?

    A: First, one need to setup two files `~/.aws/credentials` and
    `~/.aws/config` by following the
    [instruction](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).

    Say, the aws account has a profile name ‘User1’, then one can run
    nextflow under this account by setting environment variable
    `AWS_PROFILE=User1`. For example:

    ``` bash
    AWS_PROFILE=User1  nextflow run /path/to/pipeline
    ```

    More details can be found at [nextflow
    page](https://www.nextflow.io/docs/latest/awscloud.html).

11. How to activate docker to let processes run in container?

    A: The directive `process.container` specifies the docker
    container(s) that each process is run. However, this container won’t
    be used unless certain conditions are met.

        For AWS batch, by default, all processes will be run in a container, so
        no more settings are needed.

        For a local run, one need use the command option `-with-docker` to activate the
        running of processes in the specified containers. Alternatively, one
        can set `docker.enabled = true` in nextflow.config to activate this option. However,
        the former allows one to specify a different docker image other than that set
        in nextflow.config.

        One can also use the command option `-without-docker` to disable running
        processes in containers.

12. How to fix the error: ‘java.nio.file.AccessDeniedException’?

    A: This error is caused by the no permission to access files/folders
    created by docker containers. To fix this, one need do one of the
    following two settings in nextflow.config, so that the created files
    have the right ownership:

        ```
        // set docker run option; use single quotes
        docker.runOptions='-u $(id -u):$(id -g)'
        // alternatively, one can just set the following
        docker.fixOwnership = true
        ```

        Also see this [link](https://github.com/nf-core/tools/issues/336).

13. How to fix error: “Unknown method invocation `collect` on
    GroupTupleOp type”?

    A: This error can be caused by a wrong input type to the operator
    *groupTuple()*. One situation is the output from the operator
    *splitCsv()*. To solve this issue, one can explicitly transform each
    input element into a list, as shown in the below example:

        ```
        Channel
            .fromPath("test.tsv")
            .splitCsv(header: false, skip: 1, sep: "\t")
            .map{row -> [row[0], row[1], row[2]] } // convert row into list to avoid the error
            .groupTuple(by: 0)
            .view()
        ```

14. If there is a program named ‘exe’ in both container and the ‘bin’
    folder, which will be used by the processes?

    A: If there is the same-named program in both container and nextflow
    project’s ‘bin’ folder, then the one in the ‘bin’ folder will be
    called.

15. What caused the following error:
    ‘java.lang.UnsupportedOperationException: null at
    com.upplication.s3fs.S3FileSystemProvider.getFileAttributeView(S3FileSystemProvider.java:697)’

    A: This error occurred when I ran the nxf-sesame pipeline via
    awsbatch and both workdir and outdir are in AWS S3. It turned out
    that this looks like a bug in nextflow version 22.04.5. After I
    changed to use the version 22.09.5-edge, the problem is gone.

        So in general, when errors like "UnsupportedOperationException" happens, in
        addition to check the pipeline code, one may also try different nextflow
        versions for debugging.

16. How to accept a groovy variable (e.g., list, map, string) in a
    nextflow process?

    A: one can pass a groovy variable to a process, and this process
    needs to handle this variable in groovy space before using it in
    bash script. Here, we use a *Map* object as an example.

        ```
        // create a map
        myMap=[a: 1, b:100, c: "a string"]
        // create the process
        process display_map {

            debug true

            input:
            val info

            script:
            println info.getClass()
            //set=info.entrySet()
            // create a string which can be used in bash
            bashCmd=""
            info.each { entry ->
                bashCmd += "$entry.key --> $entry.value\n"
                }
            """
            echo "$bashCmd" # print the string, if it is a command, one can run it directly 
            """
        }   

        // start the workflow
        workflow {
            display_map(myMap)
        }
        ```

17. How does nextflow trigger commands in docker container?

    When one uses container to run processes, nextflow uses the
    following command to trigger a task:

    ``` bash
    docker run -i --cpu-shares xxx --memory xxxm -e "NXF_DEBUG=${NXF_DEBUG:=0}" \
        -e "NXF_OWNER=$(id -u):$(id -g)" -v /src/path:/target/path -w "$PWD" \
        --name $NXF_BOXID my_image:latest /bin/bash -c \
        "eval $(nxf_container_env); /bin/bash /path/to/.command.run nxf_trace"
    ```

    This format doesn’t trigger login shell, so the file `~/.bashrc` is
    not read.

18. How to solve the following errors:

    -   DockerTimeoutError: Could not transition to created; timed out
        after waiting 4m0s
    -   CannotInspectContainerError: Could not transition to inspecting;
        timed out after waiting 30s

    The cause: such errors are usually caused by the read/write of
    **many big** datasets on EC2 instance which uses an EBS volume. It
    is because such EBS volumes are designed to read/write not too
    frequent, constrained by available burst balance. When
    reading/writing big files such as from S3 buckets, particularly when
    multiple programs are writing/reading data from the same EBS, the
    burst balance drops quickly to zero, and causes the above errors.
    One can find more explanation
    [here](https://repost.aws/knowledge-center/batch-docker-timeout-error)

    The solutions:

    1.  increases the EBS volume size associated with the EC2 instance.
    2.  reduce the number of applications read/write from S3
        simutaneously. For the situation of AWS batch, multiple
        containers may run on one EC2 instance, will exhaust burst
        balance quickly. Therefore, one can choose an instance with
        smaller number of CPUs and/or memory, so aws batch would not
        assign many tasks on one EC2 instance.
    3.  Change the configuration `aws.batch.maxParallelTransfers` to a
        smaller number such as 5.
    4.  Change the configuration `aws.client.maxConnection` to a smaller
        number such as 20 (default 50), which controls the number of
        connections to S3 bucket for a single EC2 instance.
    5.  Decrease the job submission rates such as
        `executor.submitRateLimit` to ‘20/1min’.
    6.  Attach an EFS or FSX volume to the AMI used by batch compute
        environment and attach it to the container’s ‘/tmp’ folder (used
        by nextflow to run tasks) via the option ‘aws.batch.volumes’.
    7.  use other high I/O file systems such as io1.
    8.  For gp3 volume, when creating AMI, set the IOPS value to higher
        value, say 9000 (default is 3000) and the throughput to 500MB
        (default is 125MB), even though this will increases the cost,
        but not as much as io1/2 with the same performance.

    I have tested the method 8 with a volume size 2TB, and it seems
    working. Also the method 4 also worked in some cases.

19. How to attach an S3 volume to an AWS batch container in nextflow?

    One can use the option `aws.batch.volumes` to attach host folders to
    containers dispatched by AWS batch. To do so, one need the following
    steps:

    1.  creating an AMI to mount S3 buckets on boot. To this end, one
        need run the following steps:

        1.  start an EC2 instance with the correct settings. For
            nextflow use, one can refer to
            <https://www.nextflow.io/docs/latest/awscloud.html#custom-ami>.
            The instance need to have the correct IAM roles for
            accessing needed S3 buckets.

        2.  in the EC2 instance, download the software
            [goofys](https://github.com/kahing/goofys) and put it into a
            folder, say /home/ec2-user/bin/goofys

        3.  add the following line into the file `/etc/fstab`

                /home/ec2-user/bin/goofys#s3bucket   /mnt/mountpoint        fuse     _netdev,allow_other,--file-mode=0666,--dir-mode=0777    0       0

            Note that the first portion provides the path to the
            executable `goofys`.

            Then test it with the following command to see whether the
            S3 bucket is attached:

                sudo mount -a

            If any errors, one can use the following command to see the
            details:

                goofys -f <s3-bucket> </path/to/mount/on/host>

            Make sure the system `fuse` package is installed.

        4.  reboot the EC2 to see whether the S3 buckets are
            automatically attached.

        5.  if successful, create a new AMI from the EC2 instance, and
            record the AMI-ID.

    2.  Create a new AWS batch compute environment and use the new
        AMI-ID to override the default AMI in the settings, and then
        create a new batch queue to use the new compute environment.
        Note that the compute environment need to choose the right IAM
        role for starting EC2 instances so that the new instances have
        the access to the S3 buckets mentioned above.

    3.  in the file `nextflow.config`, add the following settings:

            aws.batch.volumes = ['/host/path1:/container/path1', '/host/path2:/container/path2']
            process.queue = <newly created queue in previous step>

    4.  Now one can refer to the attached host folders in containers
        using the the specified folders such as ‘/container/path1’ when
        writing nextflow processes.

    5.  One can start to run nextflow pipeline based on the
        configuration.

20. How to boost AWS batch performance

    The recommended setup for maximum performance with AWS Batch is to
    mount an NVMe disk as the temporary folder and run the pipeline with
    the scratch directive set to false to avoid stage-out transfer time.
    You can accomplish this by adding the following lines to your
    Nextflow config file:

        ```
        aws.batch.volumes = '/path/to/ec2/nvme:/tmp'
        process.scratch = false
        ```

    A related configuration for docker container is `docker.temp`, which
    can be set to a host path which can be used as ‘/tmp’ folder in the
    container (the /tmp folder in container is used by nextflow to run
    tasks). Not sure that this has the same effect as the option
    `aws.batch.volumes`.

21. Can I convert a nextflow channel to a groovy object?

    No. There is no way to do it, because they are totally different
    objects. I also tried to save a channel’s content into a file via
    the operator `collectFile()` and then used a groovy function to read
    the content from the file. However, this would not work in a
    workflow, because the reading of this file is not well coordinated
    with generating the file (i.e., reading can happen before
    generating). Therefore, it is hard to work out.

    Also read “How to apply a groovy function on a channel?” for a
    solution.

22. How to end a workflow early?

    Use the keyword `return` on a single line to exit from a workflow
    without error code.

23. Can I call nextflow in a bash for loop?

    Yes. If one calls `nextflow run` in a bash for loop, then each
    pipeline run will finish sequentially, i.e., move to next step after
    the current one finishes.

24. How does nextflow call a docker container?

    It triggered docker containers using the following format:

        nxf_launch() {
        docker run -i --cpu-shares 6144 --memory 49152m -e "NXF_DEBUG=${NXF_DEBUG:=0}" -e "NXF_OWNER=$(id -u):$(id -g)" -v /home/ubuntu/work:/home/ubuntu/work -w "$PWD" --name $NXF_BOXID my_image:tag /bin/bash -c "eval $(nxf_container_env); /bin/bash /home/ubuntu/work/Projects/test/nf_work/a5/6d782b9bc26da73cb71fa9b94b23ae/.command.run nxf_trace"
        }

25. What causes the error: DataflowBroadcast around DataflowStream\[?\]

    This error happens when one uses channels as inputs for other
    channel operator or channel factory such as map() or Channel.of(),
    which accept list or values only.

26. How to apply a groovy function on a channel?

    Normally, one can’t convert a nextflow channel into any Java objects
    such as List, Map, etc, so that one can operate on the objects,
    because a channel operation such as *toList()* or *collect()* still
    emits a channel object. One workaround is to apply a function via
    *flatMap()* operator on a converted list, such as below:

    ``` nextflow
    nums = Channel.of(1..10)

    def get_pair(a) {
      def s = a.size
      def p = []
      for(int i = 0; i < s; i++) {
        for(j = i+1; j<s; j++) {
          p.add([a[i],a[j]])
        }
      }

      return(p)
    }

    // get a channel emitting pairs of numbers
    nums.toList().flatMap{ it -> get_pair(it) }.view()
    ```

27. When running `def bar_out = process_bar(ch_input)`, got error
    `ch_input` already defined in the process scope @line \#\#, column
    \#\#

    This error can be a bug of nextflow, which will be triggered when
    calling a process/workflow, some places assign the calling to a
    variable and some places are not.

    The solutions is to make all calling assigned to variables or for
    the places using assignment, define a variable in one line and then
    assign the process calling to it in next line, such as

    ``` nextflow
    def bar_out = null
    bar_out = process_bar(ch_input)
    ```

28. How to handle error: “download failed: s3://bucket/path/…. An error
    occured (Slowdown) when calling the GetObject operation: please
    reduce your request rate”.

    This happens due to many parallel downloading requests from S3, and
    may happen occasionally. Here are some solutions to try: (1) re-try
    the pipeline without changing anything, (2) reduce the parameter
    aws.client.maxConnections to a lower number, say 40, (3) increases
    aws.batch.maxTransferAttempts to a bigger number, say 5.

29. How to handle error: “DEBUG nextflow.could.aws.nio.S3Client - Failed
    to upload part 733 attempt 1 for …. – Caused by: Unable to execute
    HTTP request: Timeout waiting for connection from pool” and
    “\[PublishDir-8\] WARN nextflow.processor.PublishDir - Failed to
    publish file : s3://path …”

    These errors are basically cause by many parallel uploading file
    parts to S3, and some file parts can’t connect to S3 before timeout.
    The solution is to set the parameter `aws.client.connectionTimeout`
    to a big number, say, 30000. At the same time, remove the setting
    ‘aws.client.uploadChunkSize’, since nextflow might calculate the
    value dynamically based on file size. It is also possible to
    increase the number of simutaneous connections by increasing
    ‘aws.client.maxConnections’, so that more parts can be uploaded at
    the same time, but this may cause the issue for downloading big
    files as in the previous issue. So it is better to change
    `aws.client.connectionTimeout` only.

    Also see AWS explanation:
    <https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/troubleshooting.html#faq-pool-timeout>

## Resources

1.  Nextflow documentation: <https://www.nextflow.io/docs/latest>
2.  AWS batch deployment:
    <https://www.nextflow.io/docs/latest/awscloud.html#aws-batch>
3.  AWS batch permission configuration:
    <https://apeltzer.github.io/post/01-aws-nfcore/>
4.  Nextflow training:
    <https://codata-rda-advanced-bioinformatics-2019.readthedocs.io/en/latest/4.Day4.html>
