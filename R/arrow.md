Example code for using R arrow package to handle big dataset
================
Zhenguo Zhang
2026-01-11

- [Getting data](#getting-data)
  - [Data](#data)
  - [Download data](#download-data)
  - [Read data](#read-data)
- [Explore data](#explore-data)
- [parquet format](#parquet-format)
  - [Partitioning](#partitioning)
  - [Read parquet data](#read-parquet-data)
  - [Compare the performance between single csv file and multiple
    parquet
    files](#compare-the-performance-between-single-csv-file-and-multiple-parquet-files)
  - [Challenge examples](#challenge-examples)
- [Using duckdb with arrow](#using-duckdb-with-arrow)
- [Resources](#resources)

This document is based on the example at <https://r4ds.hadley.nz/arrow>.

Apache Arrow, a multi-language toolbox designed for efficient analysis
and transport of large datasets. We’ll use Apache Arrow via the arrow
package, which provides a dplyr backend allowing you to analyze
larger-than-memory datasets using familiar dplyr syntax.

``` r
library(arrow)
library(tidyverse)
```

## Getting data

### Data

- Content: how many times each book was checked out each month from
  April 2005 to October 2022
- url: data.seattle.gov/Community/Checkouts-by-Title/tmmm-ytt6
- size: 41,389,465 rows, 9GB
- format: csv

### Download data

``` r
dir.create(file.path(workDir,"data"), showWarnings = FALSE)
dataUrl<-"https://r4ds.s3.us-west-2.amazonaws.com/seattle-library-checkouts.csv"
dataFile<-file.path(workDir,"data","seattle-library-checkouts.csv")
curl::multi_download(dataUrl, destfiles = dataFile, resume=TRUE)
```

    ## # A tibble: 1 × 10
    ##   success status_code resumefrom url    destfile error type  modified           
    ##   <lgl>         <dbl>      <dbl> <chr>  <chr>    <chr> <chr> <dttm>             
    ## 1 TRUE            200          0 https… /tmp/Rt… <NA>  text… 2022-12-04 11:29:58
    ## # ℹ 2 more variables: time <dbl>, headers <list>

### Read data

We will use `arrow::open_dataset()` to read the data, which will

- scan a few thousand rows to figure out the structure of the dataset
- records what it’s found and stops
- only read further rows as you specifically request them.

This would avoid reading all the data into memory

``` r
seattle_csv <- open_dataset(
  sources = file.path(workDir, "data/seattle-library-checkouts.csv"), 
  col_types = schema(ISBN = string()),
  format = "csv"
)

seattle_csv
```

    ## FileSystemDataset with 1 csv file
    ## 12 columns
    ## UsageClass: string
    ## CheckoutType: string
    ## MaterialType: string
    ## CheckoutYear: int64
    ## CheckoutMonth: int64
    ## Checkouts: int64
    ## Title: string
    ## ISBN: string
    ## Creator: string
    ## Subjects: string
    ## Publisher: string
    ## PublicationYear: string

As shown in the first line in the output, it tells you that seattle_csv
is stored locally on-disk as a single CSV file.

## Explore data

Let’s see what is actually in the dataset

``` r
seattle_csv |> glimpse()
```

    ## FileSystemDataset with 1 csv file
    ## 41,389,465 rows x 12 columns
    ## $ UsageClass      <string> "Physical", "Physical", "Digital", "Physical", "Physi…
    ## $ CheckoutType    <string> "Horizon", "Horizon", "OverDrive", "Horizon", "Horizo…
    ## $ MaterialType    <string> "BOOK", "BOOK", "EBOOK", "BOOK", "SOUNDDISC", "BOOK",…
    ## $ CheckoutYear     <int64> 2016, 2016, 2016, 2016, 2016, 2016, 2016, 2016, 2016,…
    ## $ CheckoutMonth    <int64> 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,…
    ## $ Checkouts        <int64> 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 2, 3, 2, 1, 3, 2, 3,…
    ## $ Title           <string> "Super rich : a guide to having it all / Russell Simm…
    ## $ ISBN            <string> "", "", "", "", "", "", "", "", "", "", "", "", "", "…
    ## $ Creator         <string> "Simmons, Russell", "Barclay, James, 1965-", "Tim Par…
    ## $ Subjects        <string> "Self realization, Conduct of life, Attitude Psycholo…
    ## $ Publisher       <string> "Gotham Books,", "Pyr,", "Random House, Inc.", "Dial …
    ## $ PublicationYear <string> "c2011.", "2010.", "2015", "2005.", "c2004.", "c2005.…

Now let’s use dplyr verbs to explore the dataset and use `collect()` to
force arrow to perform computation and return some data.

``` r
seattle_csv |> 
  group_by(CheckoutYear) |> 
  summarise(Checkouts = sum(Checkouts)) |> 
  arrange(CheckoutYear) |> 
  collect()
```

    ## # A tibble: 18 × 2
    ##    CheckoutYear Checkouts
    ##           <int>     <int>
    ##  1         2005   3798685
    ##  2         2006   6599318
    ##  3         2007   7126627
    ##  4         2008   8438486
    ##  5         2009   9135167
    ##  6         2010   8608966
    ##  7         2011   8321732
    ##  8         2012   8163046
    ##  9         2013   9057096
    ## 10         2014   9136081
    ## 11         2015   9084179
    ## 12         2016   9021051
    ## 13         2017   9231648
    ## 14         2018   9149176
    ## 15         2019   9199083
    ## 16         2020   6053717
    ## 17         2021   7361031
    ## 18         2022   7001989

## parquet format

The Parquet format is a columnar storage file format that is optimized
for use with big data processing frameworks. It is designed to be
efficient in terms of both storage space and query performance.

Like CSV, parquet is used for rectangular data, but instead of being a
text format that you can read with any file editor, it’s a custom binary
format designed specifically for the needs of big data. This means that:

- Parquet files are usually smaller than the equivalent CSV file, using
  efficient encodings to keep file size down supporting file compression

- Parquet files have a rich type system and store data in a way that
  records the type along with the data.

- Parquet files are “column-oriented”, much like R’s data frame, leading
  to better performance for data analysis

- Parquet files are “chunked”, which makes it possible to work on
  different parts of the file at the same time

### Partitioning

When you have a very large dataset, it’s often useful to split it into
multiple files based on the values of one or more columns (the variables
you likely filter on), which will help you to access the data faster.

Arrow suggests that you avoid files smaller than 20MB and larger than
2GB and avoid partitions that produce more than 10,000 files.

Now let’s rewrite the Seattle library data into different files based on
`CheckoutYear`, because it is likely that some analyses will only want
to look at a single year or a few years of data.

``` r
seattle_csv |> 
  write_dataset(
    path = file.path(workDir, "data/seattle_parquet"),
    format = "parquet",
    partitioning = "CheckoutYear"
  )
# alternatively, one can use group_by(CheckoutYear) before write_dataset() to achieve the same effect by replacing the parameter partitioning
```

Let’s check the files we just produced

``` r
tibble(
  files = list.files(
    path = file.path(workDir, "data/seattle_parquet"), 
    recursive = TRUE, 
    full.names = TRUE
  ),
  size_MB = file.info(files)$size / 2^20
)
```

    ## # A tibble: 18 × 2
    ##    files                                                                 size_MB
    ##    <chr>                                                                   <dbl>
    ##  1 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2005/part-0.parquet    108.
    ##  2 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2006/part-0.parquet    161.
    ##  3 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2007/part-0.parquet    175.
    ##  4 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2008/part-0.parquet    192.
    ##  5 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2009/part-0.parquet    211.
    ##  6 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2010/part-0.parquet    219.
    ##  7 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2011/part-0.parquet    235.
    ##  8 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2012/part-0.parquet    245.
    ##  9 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2013/part-0.parquet    265.
    ## 10 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2014/part-0.parquet    278.
    ## 11 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2015/part-0.parquet    289.
    ## 12 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2016/part-0.parquet    296.
    ## 13 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2017/part-0.parquet    300.
    ## 14 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2018/part-0.parquet    288.
    ## 15 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2019/part-0.parquet    284.
    ## 16 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2020/part-0.parquet    149.
    ## 17 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2021/part-0.parquet    225.
    ## 18 /tmp/Rtmpr36k9Z/data/seattle_parquet/CheckoutYear=2022/part-0.parquet    237.

The file names use a “self-describing” convention used by the [Apache
Hive](https://hive.apache.org/) project. Hive-style partitions name
folders with a “key=value” convention.

Another important things is that the total size of the files (around
4GB) is much smaller than the original CSV file.

### Read parquet data

Now we have split the data into multiple parquet files, let’s read them
back, the syntax is similar to reading a single file, but the input is
the folder containing all the parquet files.

``` r
seattle_pq <- open_dataset(
  sources = file.path(workDir, "data/seattle_parquet"), 
  format = "parquet"
)
print(seattle_pq)
```

    ## FileSystemDataset with 18 Parquet files
    ## 12 columns
    ## UsageClass: string
    ## CheckoutType: string
    ## MaterialType: string
    ## CheckoutMonth: int64
    ## Checkouts: int64
    ## Title: string
    ## ISBN: string
    ## Creator: string
    ## Subjects: string
    ## Publisher: string
    ## PublicationYear: string
    ## CheckoutYear: int32

Now let’s found out the number of books checked each month in the last 5
years:

``` r
seattle_pq |> 
  filter(CheckoutYear >= 2018, MaterialType == "BOOK") |> 
  group_by(CheckoutYear, CheckoutMonth) |> 
  summarise(TotalCheckouts = sum(Checkouts)) |> 
  arrange(CheckoutYear, CheckoutMonth) ->
  query
# show what will happen when collect() is called
print(query)
```

    ## FileSystemDataset (query)
    ## CheckoutYear: int32
    ## CheckoutMonth: int64
    ## TotalCheckouts: int64
    ## 
    ## * Grouped by CheckoutYear
    ## * Sorted by CheckoutYear [asc], CheckoutMonth [asc]
    ## See $.data for the source Arrow object

And now let’s collect the results into R

``` r
query |> collect()
```

    ## # A tibble: 58 × 3
    ## # Groups:   CheckoutYear [5]
    ##    CheckoutYear CheckoutMonth TotalCheckouts
    ##           <int>         <int>          <int>
    ##  1         2018             1         355101
    ##  2         2018             2         309813
    ##  3         2018             3         344487
    ##  4         2018             4         330988
    ##  5         2018             5         318049
    ##  6         2018             6         341825
    ##  7         2018             7         351207
    ##  8         2018             8         352977
    ##  9         2018             9         319587
    ## 10         2018            10         338497
    ## # ℹ 48 more rows

Notes:

- Writing dplyr code for arrow data is conceptually similar to dbplyr:
  the dplyr code is automatically transformed into a query that the
  Apache Arrow C++ library understands, which is then executed when you
  call collect().
- Like dbplyr, arrow only understands some R expressions, so you may not
  be able to write exactly the same code you usually would. One can find
  all supported functions in `?acero`

### Compare the performance between single csv file and multiple parquet files

First, let’s see how long does it take to calculate the nunber of
checkouts in each month of 2021:

``` r
seattle_csv |> 
  filter(CheckoutYear == 2021, MaterialType == "BOOK") |>
  group_by(CheckoutMonth) |>
  summarize(TotalCheckouts = sum(Checkouts)) |>
  arrange(desc(CheckoutMonth)) |>
  collect() |> 
  system.time()
```

    ##    user  system elapsed 
    ##  29.164   6.085  27.106

``` r
seattle_pq |> 
  filter(CheckoutYear == 2021, MaterialType == "BOOK") |>
  group_by(CheckoutMonth) |>
  summarize(TotalCheckouts = sum(Checkouts)) |>
  arrange(desc(CheckoutMonth)) |>
  collect() |> 
  system.time()
```

    ##    user  system elapsed 
    ##   0.448   0.015   0.123

As we can see, reading from multiple parquet files is much faster than
reading from a single csv file, which was achieved for the following
reasons:

- arrow is smart enough to recognize that it only needs to read 1 of the
  18 parquet files based on the filering condition
  `CheckoutYear == 2021`, while for the csv file, it has to read the
  whole file

- parquet is binary format, more efficient to read into memory.

- parquet stores data column-wise, and it can only read the four needed
  columns here in the query: `CheckoutYear`, `MaterialType`,
  `CheckoutMonth`, and `Checkouts`, while for the csv file, it has to
  read all nine columns.

### Challenge examples

Now let’s find out the most popular book of each year

``` r
seattle_pq |> 
  filter(MaterialType == "BOOK") |>
  group_by(CheckoutYear, Title) |>
  summarize(TotalCheckouts = sum(Checkouts)) |>
  arrange(CheckoutYear, desc(TotalCheckouts)) |>
  to_duckdb() |> # needs to_duckdb() here to use slice_max()
  slice_max(TotalCheckouts) |>
  collect() |>
  arrange(CheckoutYear)
```

    ## # A tibble: 18 × 3
    ## # Groups:   CheckoutYear [18]
    ##    CheckoutYear Title                                             TotalCheckouts
    ##           <int> <chr>                                                      <dbl>
    ##  1         2005 <Unknown Title>                                            11793
    ##  2         2006 <Unknown Title>                                            15148
    ##  3         2007 <Unknown Title>                                            13312
    ##  4         2008 <Unknown Title>                                            11784
    ##  5         2009 <Unknown Title>                                            10623
    ##  6         2010 <Unknown Title>                                             8200
    ##  7         2011 <Unknown Title>                                             5637
    ##  8         2012 <Unknown Title>                                             3606
    ##  9         2013 Where'd you go, Bernadette : a novel / Maria Sem…           3977
    ## 10         2014 The goldfinch / Donna Tartt.                                2919
    ## 11         2015 The girl on the train / Paula Hawkins.                      3333
    ## 12         2016 The girl on the train / Paula Hawkins.                      2727
    ## 13         2017 The Underground Railroad : a novel / Colson Whit…           3525
    ## 14         2018 Educated : a memoir / Tara Westover.                        5417
    ## 15         2019 Where the crawdads sing / Delia Owens.                      6913
    ## 16         2020 Such a fun age : a novel / Kiley Reid.                      1776
    ## 17         2021 The vanishing half / Brit Bennett.                          3793
    ## 18         2022 The maid : a novel / Nita Prose.                            3145

## Using duckdb with arrow

[DuckDB](https://duckdb.org/) is an in-process SQL OLAP database
management system. It can query various data sources including parquet
files using SQL syntax. It’s very easy to turn an arrow dataset into a
DuckDB database by calling arrow::to_duckdb(), and we can convert the
Seattle parquet dataset into a DuckDB database, followed by operations,
like:

``` r
seattle_pq |> 
  to_duckdb() |>
  filter(CheckoutYear == 2021, MaterialType == "BOOK") |>
  group_by(CheckoutMonth) |>
  summarize(TotalCheckouts = sum(Checkouts)) |>
  arrange(desc(CheckoutMonth)) |>
  collect() |> 
  system.time()
```

    ## Warning: Missing values are always removed in SQL aggregation functions.
    ## Use `na.rm = TRUE` to silence this warning
    ## This warning is displayed once every 8 hours.

    ##    user  system elapsed 
    ##  14.983   1.199   2.923

The nice thing about `to_duckdb()` is that the conversion doesn’t
involve any memory copying, enabling seamless transitions from one
system to another.

## Resources

- parquet format: <https://parquet.apache.org/>
