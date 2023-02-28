Notes on ggplot2
================
Zhenguo Zhang
February 27, 2023

-   [aesthetic evaluation](#aesthetic-evaluation)
-   [Functions](#functions)
    -   [Aesthetic mapping](#aesthetic-mapping)
-   [Theme](#theme)
    -   [Functions](#functions-1)
-   [Important facts](#important-facts)
-   [References](#references)

All ggplot2 objects are built using the ggproto system of object
oriented programming. An demo of ggproto object looks like below:

``` r
A <- ggproto("A", NULL,
  x = 1,
  inc = function(self) {
    self$x <- self$x + 1
  }
)
A$x
```

    ## [1] 1

``` r
A$inc()
A$x
```

    ## [1] 2

``` r
A$inc()
A$inc()
A$x
```

    ## [1] 4

Most ggplot2 classes are immutable and static: the methods neither use
nor modify state in the class. ggplot2 classes are mostly used as a
convenient way of bundling related methods together.

To create a new geom or stat, one just create a new ggproto that
inherits from Stat or Geom, and override the methods as needed.

It’s harder to create a new geom than a new stat because you also need
to know some grid. ggplot2 is built on top of grid, so you’ll need to
know the basics of drawing with grid.

## aesthetic evaluation

In ggplot2, there are three stages of data from which you can map
aesthetics. They are the start (the user data), after stat (after stat
transformation, only have access to the variables computed by stat), and
after scaling (accessible to variables in final aesthetics).

To use the second and third stages of data, one need use after\_stat()
and after\_scale() functions to mark the variable sources.

## Functions

### Aesthetic mapping

One can use scale\_xxx\_yyy() to change the shapes, colors (fill and
outline), symbols and bars in the plot. This actually includes the
changes on legends. xxx can take values in the following table:

| xxx      | Description                          |
|----------|--------------------------------------|
| colour   | Color of lines and points            |
| fill     | Color of area fills (e.g. bar graph) |
| linetype | Solid/dashed/dotted lines            |
| shape    | Shape of points                      |
| size     | Size of points                       |
| alpha    | Opacity/transparency                 |

yyy \| Description hue \| Equally-spaced colors from the color wheel
manual \| Manually-specified values (e.g., colors, point shapes, line
types) gradient \| Color gradient grey \| Shades of grey discrete \| use
discrete values to automatically determine visual values (e.g., colors,
point shapes, line types, point sizes) continuous \| Continuous values
(e.g., alpha, colors, point sizes)

**Note**: theme() can also be used to change some of the values, usually
effects beyond these commands, i.e. more global. for example,
scale\_fill\_manual(values=c(“red”,”blue”,”green”)) can manually set the
filled colors. All these scale\_xxx\_yyy functions inherit from
discrete\_scale, so one can use the parameters from this function,
including title (name), marker positions (breaks), labels (labels),
range (limits), new guide (guide), etc. With these parameters, one can
change the guide/legend easily, for example, just show certain groups in
legend and set the same color for several groups.

## Theme

Themes are a powerful way to customize the non-data components of your
plots: i.e. titles, labels, fonts, background, gridlines, and legends.

One can find details on the elements of theme at
[here](https://ggplot2.tidyverse.org/reference/theme.html).

### Functions

| Function                 | Description                                                                    |
|--------------------------|--------------------------------------------------------------------------------|
| theme\_get()             | get current theme, returning a list of theme elements.                         |
| theme\_set()             | set new default theme                                                          |
| theme\_update()          | change certain elements to default values for future plots.                    |
| update\_geom\_defaults() | update aesthetic defaults for a given geom, such as ‘point’, ‘GeomPoint’, etc. |

## Important facts

-   The unit of the text size in geom\_xxxx: mm

-   The unit of the text size in theme(): pt, 1pt=0.35mm.

-   The unit of line/point size: mm

-   The base font size in default ggplot2 theme: 11 pts, retriveable
    with `GeomLabel$default_aes$size` in mm.

-   All themes have a base\_size parameter which controls the base font
    size. The base font size is the size that the axis titles use: the
    plot title is usually bigger (1.2x), and the tick and strip labels
    are smaller (0.8x). To get these relative values, one can call the
    following R commands:

        theme_get()$text$size # base size in point
        theme_get()$plot.title$size # for title
        theme_get()$axis.title$size # for axis titles (i.e., xlab, ylab)
        theme_get()$axis.text$size # for axis tick labels

-   There are only three fonts that are guaranteed to work everywhere:
    “sans” (the default), “serif”, or “mono”.

-   Since font size are fixed in physical size, so it will not change
    when the figure size changes. To resolve this issue, one can use the
    package [ragg](https://ragg.r-lib.org/), which replaces the function
    ‘png()’, ‘jpeg()’, and ‘tiff()’ provided by the package
    \[grDevices\].

-   Our plot is a mix of elements positioned and dimensioned based on
    both relative and absolute sizes. While the relative sizes expand
    along with the output size, the absolute sizes does not. The text is
    given in points which, as you recall, is an absolute dimension. The
    same is true for the element sizes in the scatterplot, the grid
    lines, etc. This means that as we scale up the output size, they
    remain the same size and will thus get smaller relative to the full
    image.

## References

1.  Extending ggplot2:
    <https://cran.r-project.org/web/packages/ggplot2/vignettes/extending-ggplot2.html>

2.  Control plot scaling:
    <https://www.tidyverse.org/blog/2020/08/taking-control-of-plot-scaling/>

3.  Understand ggplot2 size dimension:
    <https://www.christophenicault.com/post/understand_size_dimension_ggplot2/>

4.  Good example of how to dynamically fit text:
    <https://stackoverflow.com/questions/36319229/ggplot2-geom-text-resize-with-the-plot-and-force-fit-text-within-geom-bar?rq=1>
