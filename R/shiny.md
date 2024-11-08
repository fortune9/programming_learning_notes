Shiny programming
================
November 07, 2024

-   [Structure](#structure)
-   [Reactive expressions](#reactive-expressions)
-   [Reactive values and expressions](#reactive-values-and-expressions)
    -   [Errors](#errors)
-   [Observers](#observers)
-   [Isolation and invalidation](#isolation-and-invalidation)
-   [Scoping](#scoping)
-   [Useful functions](#useful-functions)
-   [Shiny functions](#shiny-functions)
-   [Shiny modules](#shiny-modules)
-   [Components](#components)
    -   [Tables](#tables)
-   [Useful packages](#useful-packages)
-   [Build shiny into standalone desktop
    app](#build-shiny-into-standalone-desktop-app)
-   [Shiny server](#shiny-server)
-   [References](#references)

## Structure

For a shiny App, it has UI and server sections. And the two parts are
connected with the global variables `input` and `output`, which are
named lists. Each element in the lists represent an input or output
element, named by their IDs.

Shiny uses reactive programming, in which reactive expressions
automatically track and update their values when its dependencies are
changed. The outputs are reactive consumers and reactive
inputs/expressions are reactive producers. When R renders outputs, its
outputs look for its reactive producers that it depends on, and these
reactive producers will look for its dependencies too if applicable. If
any of the reactive producers change (are invalidated), the outputs will
be recalculated because the outputs have also been invalidated (taking
place when reactive inputs change and the dependent outputs are notified
to be invalidated).

There are three fundamental building blocks of reactive programming:
reactive values, reactive expressions, and observers.

## Reactive expressions

Two properties

1.  lazy: do nothing until it is called.

2.  cached: use cached value unless dependencies change.

## Reactive values and expressions

Reactive values are reference-based, so modify any copy of one reactive
value will leading to changes of all copies.

The `input` argument to shiny server function is a natural reactive
value. One can also create reactive values by using the following
functions:

| Function         | Lazy loading | Return values | Note                                                                                                                                                                                           |
|------------------|--------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| reactive()       | Y            |               | just return one single reactive value (can be any R data type). Useful when only updated in one place                                                                                          |
| reactiveValues() |              |               | hold a list of reactive values. Useful when updated in multiple places.                                                                                                                        |
| reactiveVal()    |              |               | similar to `reactive()` to hold a single value (number, matrix, data.frame, etc). return a function: calling the function without argument to get the value, with one argument to set a value. |
| eventReactive()  | Y            | Y             | the same as observeEvent, only triggered by sepecified event, but return reactive expression.                                                                                                  |

### Errors

Reactive expressions cache errors in exactly the same way as they cache
values. Errors are also treated the same way as values when it comes to
the reactive graph: errors propagate through the reactive graph exactly
the same way as regular values. The only difference is what happens when
an error hits an output or observer:

-   An error in an output will be displayed in the app49.
-   An error in an observer will cause the current session to terminate.
    If you don’t want this to happen, you’ll need to wrap the code in
    try() or tryCatch().

## Observers

Observers and outputs are terminal nodes in reactive graphs. They are
all implemented by the underlying tool \[observe()\]. It’s important to
note that observe() and the reactive outputs don’t **do** something, but
**create** something (which then takes action as needed)

Reactive outputs are a special type of observers that have two important
properties:

-   They are defined when you assign them into output, i.e. output\$text
    &lt;- … creates the observer.

-   They have some limited ability to detect when they’re not visible
    (i.e. they’re in non-active tab) so they don’t have to recompute.

Observers differ from reactive expressions in two ways:

-   they are eager and forgetful, and they run as soon as possibly and
    don’t remember their previous action.

-   the value returned is ignored because they are designed to use the
    side effect such as writing a file or making plots.

The observers \[observeEvent()\] and \[eventReactive()\] are all powered
by funciton \[isolate()\].

| Function        | Lazy loading | Return values | Note                                                                                          |
|-----------------|--------------|---------------|-----------------------------------------------------------------------------------------------|
| observeEvent()  |              | N             | triggered by specified event only, and ignores all other invalidating events on dependencies. |
| observe()       | N            |               | will run immediately if its any reactive dependencies change, and its side effects are used.  |
| eventReactive() | Y            | Y             | the same as observeEvent, only triggered by sepecified event, but return reactive expression. |

Unless needed, one recommend to use \[observeEvent()\] and
\[eventReactive()\] to handle reactive actions. They have the following
arguments to tune their behavior:

-   `ignoreNULL`: in default, an event yiedling `NULL` is ignored,
    setting this argument to ‘TRUE’ will have the observer handle the
    event.

-   `ignoreInit`: in default, both functions run when they are created,
    but set this argument to ‘FALSE’ will disable this action.

-   `once`: for \[observeEvent()\] only, setting this to ‘TRUE’ will let
    the handler run only once.

## Isolation and invalidation

\[isolate()\] allows one to access a reactive value/expression but not
take the dependency on it. Below is an example:

    r <- reactiveValues(count = 0, x = 1)
    observe({
      r$x
      r$count <- isolate(r$count) + 1 # without isolate(), this will trigger infinite loop
    })

\[invalidateLater()\] causes any reactive cunsumer to be invalidated in
a specified period, even though no data change. One can use that to
frequently check and read data stored on a disk.

A more appropriate function to read data from disk is \[reactivePoll()\]
which uses a checker function to see whether data have changed, if yes,
then the executor function is run; in this way, it avoids reading the
same data.

## Scoping

One R process can support multiple Shiny sessions, and these sessions
may share some R objects.

The variables defined in the `server` function are session-specific, so
they are all instantiated when a session is started (including input,
output, and session objects).

The variables and functions defined outside the `server` function are
visible to all sessions in the same R process, and this is a good place
to read big dataset or define some utility functions.

Things work this way because app.R is sourced when you start your Shiny
app. Everything in this script is run immediately. However, your server
function is only actually called when a web browser connects and a new
session is started.

Objects defined in global.R are similar to those defined in app.R
outside of the server function definition, with one important
difference: they are loaded into the global environment of the R
session; all R code in a Shiny app is run in the global environment or a
child of it.

If you want to split the server or ui code into multiple files, you can
use source(local = TRUE) to load each file. You can think of this as
putting the code in-line, so the code from the sourced files will
receive the same scope as if you copied and pasted the text right there.

One can see [here](https://shiny.rstudio.com/articles/scoping.html) for
more details on scoping.

## Useful functions

| Function              | Note                                                                                                             |
|-----------------------|------------------------------------------------------------------------------------------------------------------|
| reactiveConsole(TRUE) | enable reactive environment in the console, so that one can call reactive functions to see the effect or values. |
| req(var)              | make sure a variable available before going forward.                                                             |
| insertUI()            | insert an UI element dynamically.                                                                                |
| removeUI()            | remove an UI element dynamically.                                                                                |

## Shiny functions

When one wants to pass a reactive value or expression to a user-defined
function, he need pass it without the parenthesis, because with
parenthesis, the value passed in is a normal value rather than reactive
one, and so the user-function would not react when the reactive value
changes. Below is an example:

    library(shiny)
    reactiveConsole(T)
    # create a reactive value
    tmpv<-reactiveVal(10)

    # then create two functions returning an reactive value depending on the reactive value 'tmpv',
    # one accepts the value provided by tmpv()
    tmpf1<-function(val) {
        return(reactive( { paste("I received", val, "in tmpf1") }) )
    }

    # and one accepts the reactive value tmpv
    tmpf2<-function(val) {
        return(reactive( { paste("I received", val(), "in tmpf2") }) )
    }

    # run the two functions to get two reactive values
    tmpv1<-tmpf1(tmpv())
    tmpv2<-tmpf2(tmpv)
    is.reactive(tmpv1)
    #[1] TRUE
    is.reactive(tmpv2)
    #[1] TRUE
    tmpv1()
    # [1] "I received 10 in tmpf1"
    tmpv2()
    # [1] "I received 10 in tmpf2"

    # then update the reactive value tmpv, and check tmpv1 and tmpv2
    tmpv(20)
    tmpv1()
    # [1] "I received 10 in tmpf1"
    tmpv2()
    # [1] "I received 20 in tmpf2"
    # as you can see tmpv1 actually lost the dependency on tmpv

It is recommended to isolate the reactivity from user functions, so that
the reactivity stays in the server function and computation goes into
user function. However, sometimes these functions rely on user input,
and then reactivity may not be separable.

## Shiny modules

Modules allow one to write isolated reusable code so that each module
can run independently and reduce repeated components.

Compared to functions which can only support UI or server functions at a
time, modules can include both UI and server functions.

In fact, a module consists of UI and server functions, and one can call
these functions when constructing shinyApps. The magic of modules comes
because these functions are constructed in a special way that creates a
“namespace”. So far, when writing an app, the names (ids) of the
controls are global: all parts of your server function can see all parts
of your UI. Modules give you the ability to create controls that can
only be seen from within the module. This is called a namespace because
it creates “spaces” of “names” that are isolated from the rest of the
app.

A module is composed of module UI function and module server function,
both need take an argument as the namespace. Here is an example of
module UI function:

    histogramUI <- function(id) {
      tagList(
        selectInput(NS(id, "var"), "Variable", choices = names(mtcars)),
        numericInput(NS(id, "bins"), "bins", value = 10, min = 1),
        plotOutput(NS(id, "hist"))
      )
    }

And here is a module server function:

    histogramServer <- function(id) {
      moduleServer(id, 
                    function(input, output, session) {
                        data <- reactive(mtcars[[input$var]])
                        output$hist <- renderPlot({
                        hist(data(), breaks = input$bins, main = input$var)
                        }, res = 96)
                    }
     )
    }

Note that the function `moduleServer()` takes care of the namespacing
automatically: inside of moduleServer(id),
input![var and input](http://chart.apis.google.com/chart?cht=tx&chl=var%20and%20input "var and input")bins
refer to the inputs with names NS(id, “var”) and NS(id, “bins”).

And here is how to use the module:

    histogramApp <- function() {
      ui <- fluidPage(
        histogramUI("hist1")
      )
      server <- function(input, output, session) {
        histogramServer("hist1")
      }
      shinyApp(ui, server)  
    }

Note that, like all Shiny control, you need to use the same id in both
UI and server, otherwise the two pieces will not be connected.

## Components

### Tables

One can use DT package to generate interactive datatables. The table is
also allowed to edit. When editting it, there are several important
points to keep in mind:

1.  One need get a copy of the table object using
    \[DT::dataTableProxy(“outputId”)\], and this copy need be updated
    using the method \[DT::replaceData(proxy, newData, …)\].

2.  It is important to keep the parameter ‘rownames’ the same when in
    \[renderDT()\] and \[replaceData()\], i.e., set to `TRUE` or `FALSE`
    in both places.

3.  If `rownames=FALSE`, then the column number returned in
    `input$outputId_cell_edit` is shifted by one, so one need use
    `input$outputId_cell_edit + 1` to get the column number.

Useful links:

-   DataTable options: <https://rstudio.github.io/DT/options.html>

-   extensions: <https://rstudio.github.io/DT/extensions.html>

-   bootstrap style: <https://rstudio.github.io/DT/005-bootstrap.html>

-   operating table proxy: <https://yihui.shinyapps.io/DT-proxy/>

## Useful packages

-   reactlog: package to draw reactive graphs for real apps. To use it,
    one need turn it on before running an app by typing
    `reactlog::reactlog_enable()`, and then press ‘Ctrl+F3’ to show
    reactlog generated at that point, or after the app is closed, run
    `shiny::reactlogShow()` to see the log of whole session.

## Build shiny into standalone desktop app

One can use Electron to build shinyApp into a standalone app, see
[here](https://www.travishinkelman.com/deploy-shiny-electron/).

## Shiny server

One can install shiny sever from the website
<https://posit.co/products/open-source/shiny-server/>, and then deploy
his shiny apps by putting into the folder */srv/shiny-server/*.

Note that shiny server can be configured using the file
/etc/shiny-server/shiny-server.conf, including where to load apps and
where to write logs. It also makes the app running user as *shiny* via
the option *run\_as*. One can find more about shiny server configuration
at <https://docs.posit.co/shiny-server/>.

-   Permission: since the apps will be run under user *shiny*, so it is
    important to make sure that *shiny* has the correct write and read
    permissions to relevant files/folders used by the apps. Typically,
    the apps won’t be able to access any files in another user’s home
    folder hierachy: unless one specify *run\_as: :HOME\_USER:* in
    configuration, then an app from a specific user home folder will
    assume that user when running the app; for example, an application
    stored in /home/jim/ShinyApps/app1 would run as jim.

-   Dockerize shiny apps: one can build docker images based on the image
    *rocker/shiny*, which includes a shiny server. One can copy apps to
    the container’s folder /srv/shiny-server/, then trigger the shiny
    server using the command */usr/bin/shiny-server* or use *CMD
    \[“/usr/bin/shiny-server”\]* in the Dockerfile. Alternatively, one
    can trigger the app too in the dockerfile, if that is the only one;
    for example, see
    <https://hosting.analythium.io/dockerizing-shiny-applications/>,
    which directly triggered a shiny app instead of shiny server though.

-   Environment variables: when starting R via shiny server, most
    environment variables are scrubbed to avoid exposure of sensitive
    info, which means that some user-set environment variables won’t be
    accessible in shiny apps, including environment variable *PATH*. One
    solution is that putting enviroment variables in the file
    /home/shiny/.profile, because R processes are spawned using the Bash
    login shell, so prior to the execution of the R session, the Bash
    shell will read and execute user bash settings. However, this will
    not work if one already starts the shiny server using the user
    shiny, such as given by ‘USER shiny’ in a Dockerfile.

## References

1.  Mastering shiny book: <https://mastering-shiny.org/>

2.  Engineering production-grade shiny apps:
    <https://engineering-shiny.org/>

3.  All books related to shiny: <https://www.bigbookofr.com/shiny.html>
