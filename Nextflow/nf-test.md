nf-test
================
Zhenguo Zhang
14 December, 2024

-   [Languages in nf-test](#languages-in-nf-test)
-   [Snapshots](#snapshots)
-   [Some commands](#some-commands)
-   [Generate tests for a pipeline/module/subworkflows/functions,
    run](#generate-tests-for-a-pipelinemodulesubworkflowsfunctions-run)
-   [Running tests](#running-tests)
-   [assertions](#assertions)
-   [writing main.nf.test](#writing-mainnftest)
-   [Configuration](#configuration)
-   [Debug](#debug)

*nf-test* is designed to test nextflow modules, workflows and pipelines,
so ensuring reproducibility.

One can also find documentation at
<https://www.nf-test.com/docs/getting-started/>.

nf-test uses `diff` to compare snapshots, and one can do some
customizations by setting environment variables, check
<https://www.nf-test.com/docs/assertions/snapshots/#snapshot-differences>.

### Languages in nf-test

The language used for writing tests are groovy and the nf-test extended
packages, not nextflow, so the latter such as `flatMap()` won’t work.

### Snapshots

nf-test can also generate and compare to snapshots to make sure the same
results are obtained during the test. Snapshot is a json file that
contains a serialized version of the provided object. Basically, the
md5sum strings are stored in the snapshot file `*.nf.test.snap`, when
difference is detected, test will fail.

One can generate snapshots for the following:

-   workflow

        assert snapshot(workflow.out.channel1).match()
        assert snapshot(workflow.out.channel1, workflow.out.channel2).match()

-   process

        assert snapshot(process.out).match()

-   file

        assert snapshot(path(process.out.get(0))).match()

    Also note that file paths are automatically replaced with a unique
    fingerprint of the files by nf-test that ensures the file content is
    the same. The fingerprint is default the md5 sum.

-   function

        assert snapshot(function.result).match()

-   pipeline Since no channels, one can include the whole workflow
    and/or output files

        assert snapshot(
          workflow,
          path("${params.outdir}/file1.txt"),
          path("${params.outdir}/file2.txt"),
          path("${params.outdir}/file3.txt")
        ).match()

Every object that is serializable can be included into snapshots.
Therefore you can even make a snapshot of the complete workflow or
process object. This includes stdout, stderr, exist status, trace etc.
and is the easiest way to create a test that checks for all of this
properties:

    assert snapshot(workflow).match()

**Note** for large object, it is recommended to store the md5 hashsum in
the snapshot file instead of the content:

     assert snapshot(hugeObject).md5().match()

### Some commands

-   init: initialize a folder by creating nf-test.config and folder
    tests.

-   generate: generate test file main.nf.test for each of the following
    type

    -   pipeline
    -   workflow
    -   process
    -   function

    The command format is

        nf-test generate <type such as pipeline> <script such as main.nf>

    Depending on the setting to *testDir*, the test scripts will be in a
    common folder or in the same folder as the script (if setting to
    ‘.’).

    **Note**: the generated test scripts are still skeleton code, which
    need editting to insert real testing code.

    To generate tests for a pipeline, run the following:

        nf-test init
        nf-test generate pipeline main.nf
        # the generated tests/main.nf.test will simply check whether the pipeline
        # finish successfully, so one can run the following command
        nf-test test --profile test

    to add more tests for a pipeline, please check
    <https://www.nf-test.com/docs/assertions/snapshots/#constructing-complex-snapshots>

-   test: test a script, tag, or all tests in the folder *tests*

-   list: list all the tests in a folder

-   clean: removes the .nf-test directory

### Generate tests for a pipeline/module/subworkflows/functions, run

    nf-test generate <pipeline, module, subworkflow, etc>

See this [video](https://www.youtube.com/watch?v=K9B7JRkMpQ4) for an
introduction.

### Running tests

-   run all the tests in the *tests* folder

        nf-test test

    The command is essentially created a workflow file for each tested
    module/workflow on the fly and test it. One can find the generated
    files in the working folder under .nf-test (default).

-   run specific tests

        nf-test test /path/to/modules/folder/my_module.nf.test

    When this command is first time run, a snapshot file
    *tests/main.nf.test.snap* is generated, which will be compared
    against in the future runs

-   To test tests associated with tags

        nf-test test --tag tag1,tag2

-   update snapshots

        nf-test test  /path/to/modules/folder/my_module.nf.test --update-snapshot

### assertions

Check the link <https://nf-co.re/docs/contributing/nf-test/assertions>

Also check here <https://www.nf-test.com/docs/assertions/assertions/>

### writing main.nf.test

For each module or subworkflow, the test associated test file is named
‘main.nf.test’, and it has the following blocks (check
<https://nf-co.re/docs/tutorials/tests_and_test_data/nf-test_writing_tests>
and <https://www.nf-test.com/docs/getting-started>):

-   setup: this includes the processes to generate inputs for the main
    module/subworkflow.

-   when: this block sets up the inputs for the module/subworkflow. In
    this block, one can use *params* section to set parameters to
    override the nextflow inputs, and use the *process* section to
    provide inputs (via the *input* array). Note that, for subworkflows,
    the channel inputs must be created like Channel.of(), and empty
    array ‘\[\]’ will only work for process tests.

-   then: this block does the tests using assertions

-   global variables: in nf-test blocks, it is better to use the global
    variables to refer to files, instead of the parameters from the
    pipeline such as ‘params.outdir’, because the global variables give
    the absolute paths. Also note that the global variable ‘outputDir’
    is always ending with ‘output’, not the value given by
    ‘params.outdir’; check global variable ‘launchDir’ for potential get
    output dir. One can find more information on global variables at
    <https://www.nf-test.com/docs/testcases/global_variables/>

-   process name: normally the process name defined by the *process*
    directive in the main.nf.test file is the same as the process folder
    name; however, if one changes the process name when defining it in
    *main.nf*, one has the opportunity to change it in the test file
    too, using `process "new_process_name"`, otherwise test will
    complain no such process.

-   One can find more guidance on writing tests at
    <https://nf-co.re/docs/tutorials/tests_and_test_data/nf-test_writing_tests>

-   When referring to the files from test\_data.config, one can’t put
    the map hierachy in a quote, otherwise it would trigger the error
    such as “java.lang.NullPointerException: Cannot get property ‘hello’
    on null object”. Below are the correct and wrong ways, respectively:

    ``` groovy
    # wrong way
    input[0] = file("${params.test_data['hello']}")
    ```

    ``` groovy
    # correct way
    input[0] = file(params.test_data['hello'])
    ```

    To construct new strings using the *params* map, one can use plus
    sign, such as

    ``` groovy
    input[0] = file(params.test_data['testdir'] + "/*.csv")
    ```

### Configuration

One can use the nf-test.config to configure how to run nf-test command.
The available settings can be found at
<https://www.nf-test.com/docs/configuration/>.

If one wants to append commandline options to the nf-test triggered
nextflow run, one can use *options*. For example, one can use the
following to specify the working dir for aws batch run:

    options "-bucket-dir s3://path/to/workdir"

### Debug

One can check the files in the path
<launchDir>/.nf-test/tests/<hash-tag>/meta to exam the structure of each
output channels, for example, for channel `fastq`, the correpondding
file is `output_fastq.json`. Then to get a specific element in nf-test,
one can use, for example, `fastq.get(0).get(1)` to get the 2nd element
of the first array.
