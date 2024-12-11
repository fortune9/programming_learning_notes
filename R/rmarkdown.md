Rmarkdown notes
================
December 10, 2024

-   [Syntax](#syntax)
    -   [Print chunk code as it is](#print-chunk-code-as-it-is)
    -   [Child documents](#child-documents)
-   [FAQs](#faqs)
-   [Errors](#errors)
-   [Caveats](#caveats)

## Syntax

### Print chunk code as it is

Sometimes, we just want to print out chunk code without evaluating it,
even not recognized by *knitr*. To do so we have the following
approaches:

-   use *verbatim* enegine, this is the most powerful one, and the
    preferred approach.

    ```` default
    ```{r, eval=TRUE}
    1 + 1
    ```
    ````

-   adding an empty string as *inline R code* after ```` ```{r} ````

    `{r eval=TRUE}   n = 10   rnorm(x)`

-   a comment string after ```` ```{r} ````

    `{r label} # this comment de-evaluate this r code chunk   cat("This is not executed")`

-   put the code into the block quoted by markdown

    The problem with the above two methods is the code will be displayed
    in one line. So to avoid that, one can put the code as below:

    ```` markdown
    ```{r label} 
    rnorm(10)
    ```
    ````

-   for inline R code, one can use *knitr::inline\_expr()*. Check
    <https://yihui.org/knitr/faq/>

Also refer to this document
<https://github.com/yihui/knitr-examples/blob/master/065-rmd-chunk.Rmd>
for more details.

### Child documents

In knitr, one can put some Rmarkdown code in a child document, and then
load them via the following approaches:

-   knit(): knit a document and return the resulted file path, unless
    the option *text* is given.

-   knit\_child(): return knitted text string which can be inserted into
    current rmarkdown document via *cat()*.

    If knit\_child is called within a function, then the execution
    environment of the function is not inherited by knit\_child (can be
    resolved by providing parameter ‘envir=environment()’); in this
    sense, the function ‘knit’ is much easier to understand.

    This function can also accept text string as input using the option
    ‘text’ instead of a file.

-   knit\_expand(): similar to *knit\_child()*, but it can specify which
    parts of the child document will be evaluated as code using the
    option *delim* (see the examples below).

In all cases, one can update parameters and variables in the parent
document, and then load child document with the updated variables taking
effect.

As one example, the following code modifies figure width and then load
the child document afterwards:

**Main document:**

```` markdown
```{r run-all, results="asis"} 
src <- NULL
for (i in 1:3) {
  figWidth<-i*2
  src <- c(src, knit_expand("child_knit_expand.Rmd", delim=c('<','>'))) # use knit_expand
  # src <- c(src, knit_child("child_knit_child.Rmd",quiet=T)) #  use knit_child
}
src <- knit(text = src, quiet=T) # knit again, this is unneeded if the variables are not in the chunk header as shown here.
cat(paste(src, collapse = '\n'))
```
````

**Child Rmd file for knit\_expand:**

```` markdown
## Now i is <i>


```{r <paste("child",i, sep='-')>, fig.width=<figWidth>, results="asis", comment=""} 
print (<i>)
kable(iris[<i>, ], format="markdown")
boxplot (iris[, <i>] ~ iris$Species)
```
````

**Child document for knit\_child():**

```` default
## Now i is `r i`

```{r `r paste("child",i, sep='-')`, fig.width=`r figWidth`, results="asis", comment=""} `r ''`
print (`r i`)
kable(iris[`r i`, ], format="markdown")
boxplot (iris[, `r i`] ~ iris$Species)
```
````

Note we add an empty string after the ```` ```{r} ```` to prevent it is
evaluated in first round of knitting as the chunk label can’t get value
from inline code. Therefore, we replace the variables (‘i’ and
‘figWidth’ here) with their values first, and then evaluate again with
knit in the main rmarkdown file.

One can find more info at
<https://bookdown.org/yihui/rmarkdown-cookbook/child-document.html>

## FAQs

-   How to finish knitting a document early?

    One can use the following code to do it without causing errors.

        knitr::knit_exit()

## Errors

-   ‘Error in setwd(opts\_knit\$get(“output.dir”)) : character argument
    expected’

    This happens when one wants to run *knitr::knit\_child()*
    interactively, i.e., run the code section in Rstudio. This error
    will go away when one render the whole document via knit button or
    *rmarkdown::render()*

    One may tend to set the option *output.dir* using the following
    before knit child document,

        opts_knit$set(output.dir=getwd())

    But this will not work: the child document will generate outputs if
    successful, but the returned text won’t be rendered correctly in the
    parent document, and figures will be generated in pdf format and not
    loaded.

## Caveats

1.  Normally R objects (e.g., plots, strings, etc) will be print out
    directly when these objects are placed on one line separately.
    However, this won’t work when it is in blocks like `if-else`, `for`,
    etc. In this case, these objects need be print out explicitly using
    functions like `print()` or `cat()`.
