Test word template
================

-   [This is heading 2, corresponding to heading
    2](#this-is-heading-2-corresponding-to-heading-2)
    -   [This is heading 3, corresponding to heading
        3](#this-is-heading-3-corresponding-to-heading-3)
-   [Here we have a bullet list](#here-we-have-a-bullet-list)
-   [Try bold and italics](#try-bold-and-italics)
-   [A block](#a-block)
-   [New section](#new-section)
-   [Use fenced\_divs to specify a certain
    style](#use-fenced_divs-to-specify-a-certain-style)

This is a test document to see how word template affects the output of
the Rmarkdown. This corresponds to `First Paragraph`.

The different markdown styles below correspond to the styles in the word
template, thus controlled by changing those styles in the word template.
This corresponds to `Body Text`.

Table of index corresponds to `Hyperlink`.

## This is heading 2, corresponding to heading 2

### This is heading 3, corresponding to heading 3

And this is a normal text paragraph.

## Here we have a bullet list

-   item 1, corresponding to `compact`
-   item 2
    -   sub-item 1, corresponding to compact
    -   sub-item 2

## Try bold and italics

This is a text in **bold** and *italics*.

## A block

> this is a block text. Corresponding to `Block Text`

## New section

I have using the above sections generated a first version document, and
then editted it by changing and updating the styles, and named it
`word_template.docx`. I then use this new word document as template by
providing the parameter `reference_docx`.

## Use fenced\_divs to specify a certain style

<div custom-style="Block Text">

This is a block text controlled with custom style ‘Block Text’.

</div>
