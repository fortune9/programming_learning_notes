Color theory
================

-   [HCL color space](#hcl-color-space)
-   [Color blindness check](#color-blindness-check)
-   [ggplot2 builtin color scales](#ggplot2-builtin-color-scales)
-   [References](#references)

## HCL color space

HCL colour space has three components of hue, chroma and luminance, and
used to describe the color space in a uniform and continuous way.

-   **Hue** ranges from 0 to 360 (an angle) and gives the “colour” of
    the colour (blue, red, orange, etc).

-   **Chroma** is the “purity” of a colour, ranging from 0 (grey) to a
    maximum that varies with luminance.

-   **Luminance** is the lightness of the colour, ranging from 0 (black)
    to 1 (white).

## Color blindness check

Avoid red-green contrast to help color blindness. One can use
[Visicheck](https://www.vischeck.com/) or R package
[dichromat](https://cran.r-project.org/web/packages/dichromat/) to
simulate color blindness.

## ggplot2 builtin color scales

All the following functions use the scale ‘fill’, but the ‘color’ and
‘shape’ scales also have corresponding functions.

1.  scale\_fill\_viridis\_c(): designed for uniform color as well as
    color blindness friendly.

2.  scale\_fill\_distiller(): color scales derived from R ColorBrewer
    for continuous variables.

3.  scale\_fill\_fermenter(): color scales derived from R ColorBrewer
    scales for binned data.

4.  scale\_fill\_brewer(): color scales derived from R ColorBrewer
    scales for discrete variables.

5.  scale\_fill\_gradient(): produce two-color gradient.
    scale\_fill\_gradient2() and scale\_fill\_gradientn() are for 3- or
    more- color gradient.

6.  scale\_fill\_hue(): get the colors based on HCL colorspace, one can
    use the parameters ‘h’, ‘c’, and ‘l’ to specify the values of hue,
    chroma and luminance.

7.  scale\_fill\_grey(): used to get color scheme in grey scale, good
    for printing in black and white.

8.  scale\_fill\_binned(): create color scheme for binned data (split
    continuous data into bins), and the parameter `n.breaks` determine
    how many bins to create, and good for displaying continuous data if
    edges are preferred.

9.  scale\_fill\_steps(): the default for scale\_fill\_binned(), and it
    is analogous to scale\_fill\_gradient(), so it has versions of
    scale\_fill\_steps2() and scale\_fill\_stepsn().

10. scale\_alpha\_continuous(): map the transparency of shade to a data
    variable.

There are so many palettees in R, and the package paletteer provides a
common interface to all of them.

## References

1.  Color setting in ggplot2:
    <https://ggplot2-book.org/scale-colour.html>
