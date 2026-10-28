# R → Python: daily data operations

Condensed from [data_operations.Rmd](data_operations.Rmd) and [data_operations.md](data_operations.md). Print the companion PDF at actual size on US Letter paper; five pages (three sheets double-sided). The HTML is also printable.

**Conventions:** R examples assume dplyr/tidyr where needed. Python examples use pandas and NumPy. Each row is an independent recipe. Substitute your own names and assign returned results as needed.

## 1. Inspect, select & clean

### Start here

R code uses dplyr/tidyr where needed. In both columns, df is a table; x is a numeric vector (R) or Series (Python). Examples are independent recipes; assign returned tables to keep changes.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `Libraries` | `import numpy as np`<br>`import pandas as pd` |
| `df$score; df$group` | `x = df["score"]; g = df["group"]` |

### Inspect a table

| R operation / intent | Python equivalent |
| :--- | :--- |
| `head(df); tail(df)` | `df.head(); df.tail()` |
| `dim(df); nrow(df); ncol(df)` | `df.shape; len(df); df.shape[1]` |
| `names(df); str(df)` | `df.columns; df.info(); df.dtypes` |
| `summary(df)` | `df.describe(include="all")` |
| `unique(df$group)` | `g.unique()` |
| `table(df$group, useNA="ifany")` | `g.value_counts(dropna=False)` |

### Select rows & columns

| R operation / intent | Python equivalent |
| :--- | :--- |
| `df[1, , drop=FALSE]; df[1:3, ]` | `df.iloc[[0]]; df.iloc[:3]` |
| `df$score; df["score"]` | `df["score"]; df[["score"]]` |
| `select(df, id, score)` | `df[["id", "score"]]` |
| `filter(df, age >= 30, group == "treated")` | `df.loc[(df["age"] >= 30) &`<br>`       (g == "treated")]` |
| `filter(df, id %in% c(1, 3))` | `df.loc[df["id"].isin([1, 3])]` |
| `filter(df, !(id %in% c(1, 3)))` | `df.loc[~df["id"].isin([1, 3])]` |
| `any(x > 10); all(x > 10)` | `(x > 10).any(); (x > 10).all()` |

### Missing values & types

| R operation / intent | Python equivalent |
| :--- | :--- |
| `is.na(x); sum(is.na(x))` | `x.isna(); x.isna().sum()` |
| `drop_na(df, score)` | `df.dropna(subset=["score"])` |
| `replace_na(x, 0)` | `x.fillna(0)` |
| `mean(x, na.rm=TRUE)` | `x.mean()` |
| `mean(x)  # retain missingness` | `x.mean(skipna=False)` |
| `as.numeric(x)` | `pd.to_numeric(x, errors="coerce")` |
| `as.integer(x)` | `x.astype("Int64")  # nullable integer` |

**Remember:** Indexing: iloc uses zero-based positions; slices exclude the stop. loc uses labels; label slices include the stop. After filtering, use iloc[0] for the first row. Combine masks with & / | / ~ and parentheses. Int64 permits missing integers but does not truncate fractional values like R as.integer().

## 2. Transform, summarize & apply

### Change, sort & deduplicate

Most methods return a result: write df = ... to retain it. Use df.copy() for an independent table; alias = df shares the same object.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `mutate(df, doubled=score * 2)` | `df.assign(doubled=df["score"] * 2)` |
| `df$score[df$group == "treated"] <- 100` | `df.loc[df["group"] == "treated",`<br>`       "score"] = 100` |
| `rename(df, response=score)` | `df.rename(columns={"score": "response"})` |
| `arrange(df, desc(score))` | `df.sort_values("score", ascending=False)` |
| `distinct(df)` | `df.drop_duplicates()` |
| `distinct(df, id, .keep_all=TRUE)` | `df.drop_duplicates("id", keep="first")` |
| `if_else(x >= 15, "high", "low",`<br>`        missing="unknown")` | `np.select([x.isna(),`<br>` (x >= 15).fillna(False).to_numpy(dtype=bool)],`<br>` ["unknown", "high"], default="low")` |

### Summaries, groups & ordered operations

Below: x = df["score"]; gb = df.groupby("group", as_index=False, observed=True, dropna=False). Missing group keys are retained; only observed categorical groups appear.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `mean(x, na.rm=TRUE); sd(x, na.rm=TRUE)` | `x.mean(); x.std()` |
| `count(df, group)` | `gb.size()` |
| `group_by(df, group) \|> summarise(`<br>` n=n(), valid=sum(!is.na(score)),`<br>` avg=mean(score, na.rm=TRUE))` | `gb.agg(n=("score", "size"),`<br>`       valid=("score", "count"),`<br>`       avg=("score", "mean"))` |
| `group_by(df, group) \|> mutate(`<br>` avg=mean(score, na.rm=TRUE))` | `df.assign(avg=df.groupby("group",`<br>` dropna=False)["score"].transform("mean"))` |
| `lag(x); cumsum(x)` | `x.shift(1); x.cumsum()` |
| `zoo::rollmean(x, 3,`<br>` align="right", fill=NA)` | `x.rolling(3).mean()` |
| `group_by(df, group) \|>`<br>` mutate(prev=lag(score))` | `df.assign(prev=df.groupby("group")`<br>` ["score"].shift(1))` |

### The apply family

mat is a 2D NumPy array; fun is a callable; xs / ys are collections. For columns use axis=0; for rows use axis=1. Prefer built-in vectorized operations when available.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `colMeans(mat); rowMeans(mat)` | `mat.mean(axis=0); mat.mean(axis=1)` |
| `apply(mat, 2, FUN)` | `np.apply_along_axis(fun, 0, mat)` |
| `apply(mat, 1, FUN)` | `np.apply_along_axis(fun, 1, mat)` |
| `apply(df, 2, FUN); apply(df, 1, FUN)` | `df.apply(fun, axis=0); df.apply(fun, axis=1)` |
| `lapply(xs, FUN)` | `[fun(v) for v in xs]` |
| `sapply(xs, FUN)  # scalar results` | `np.array([fun(v) for v in xs])` |
| `mapply(FUN, xs, ys)` | `[fun(a, b) for a, b in`<br>` zip(xs, ys, strict=True)]` |
| `tapply(x, group, mean, na.rm=TRUE)` | `df.groupby("group")["score"].mean()` |
| `Vectorize(FUN); sqrt(mat)` | `np.vectorize(fun); np.sqrt(mat)` |

**Remember:** size counts rows; count counts nonmissing values. agg reduces groups; transform retains row alignment. Sort by subject/time before lags and windows. pandas std uses ddof=1 (R sd); NumPy std defaults to 0. cumsum skips NaN by default; R propagates NA. Never use chained assignment df[mask]["col"] = ... .

## 3. Files, text, joins & reshaping

### Read & write

Optional engines: openpyxl for typical Excel files; pyarrow for Parquet. CSV does not preserve all types or category levels.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `read.csv("data.csv")` | `pd.read_csv("data.csv")` |
| `read.delim("data.tsv")` | `pd.read_csv("data.tsv", sep="\t")` |
| `write.csv(df, "data.csv", row.names=FALSE)` | `df.to_csv("data.csv", index=False)` |
| `readxl::read_excel("data.xlsx", sheet="S1")` | `pd.read_excel("data.xlsx", sheet_name="S1")` |
| `writexl::write_xlsx(df, "data.xlsx")` | `df.to_excel("data.xlsx", index=False)` |
| `arrow::read_parquet("data.parquet")` | `pd.read_parquet("data.parquet")` |
| `arrow::write_parquet(df, "data.parquet")` | `df.to_parquet("data.parquet", index=False)` |

### Strings, dates & categories

s is a text Series; d is a datetime Series. Use .str for text columns and .dt for datetime columns.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `toupper(s); trimws(s)` | `s.str.upper(); s.str.strip()` |
| `grepl("text", s, fixed=TRUE)` | `s.str.contains("text", regex=False, na=False)` |
| `paste(group, id, sep="_")` | `df["group"] + "_" + df["id"].astype("string")` |
| `as.Date(s, format="%Y-%m-%d")` | `pd.to_datetime(s, format="%Y-%m-%d")` |
| `lubridate::year(d)` | `d.dt.year` |
| `as.integer(d - min(d))` | `(d - d.min()).dt.days` |
| `factor(s, levels=c("control", "treated"))` | `pd.Categorical(s,`<br>` categories=["control", "treated"])` |

### Bind & join

a and b are tables. For multi-key joins use on=["id", "visit"]; differing names use left_on="id", right_on="subject_id".

| R operation / intent | Python equivalent |
| :--- | :--- |
| `bind_rows(a, b)` | `pd.concat([a, b], ignore_index=True)` |
| `bind_cols(a, b)  # by position` | `pd.concat([a.reset_index(drop=True),`<br>` b.reset_index(drop=True)], axis=1)` |
| `left_join(a, b, by="id")` | `a.merge(b, on="id", how="left")` |
| `inner_join(a, b, by="id")` | `a.merge(b, on="id", how="inner")` |
| `full_join(a, b, by="id")` | `a.merge(b, on="id", how="outer")` |
| `semi_join(a, b, by="id")` | `a.loc[a["id"].isin(b["id"])]` |
| `anti_join(a, b, by="id")` | `a.loc[~a["id"].isin(b["id"])]` |

### Wide ↔ long

| R operation / intent | Python equivalent |
| :--- | :--- |
| `pivot_longer(wide, c(before, after),`<br>` names_to="time", values_to="value")` | `wide.melt(id_vars="id",`<br>` value_vars=["before", "after"],`<br>` var_name="time", value_name="value")` |
| `pivot_wider(long, names_from=time,`<br>` values_from=value)` | `long.pivot(index="id", columns="time",`<br>` values="value").reset_index()` |

**Remember:** Read leading-zero IDs with dtype={"id": "string"}. To keep literal "NA" text, use keep_default_na=False with explicit na_values. Join duplicates can multiply rows: add validate="many_to_one" where appropriate. Missing keys may match. pivot requires unique key pairs; pivot_table(..., aggfunc="mean") explicitly aggregates duplicates. Melt row order can differ from R.

## 4. Statistics, models & Python habits

### Tests & correlation

Imports: from scipy import stats; import statsmodels.formula.api as smf. x and y below are numeric samples with missing values removed; paired tests/correlations require the same complete pairs.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `t.test(x, y)  # Welch` | `stats.ttest_ind(x, y, equal_var=False)` |
| `t.test(x, y, paired=TRUE)` | `stats.ttest_rel(x, y)` |
| `cor.test(x, y, method="pearson")` | `stats.pearsonr(x, y)` |
| `cor.test(x, y, method="spearman",`<br>` exact=FALSE)` | `stats.spearmanr(x, y)` |
| `wilcox.test(x, y)` | `stats.mannwhitneyu(x, y)` |
| `chisq.test(tab)` | `stats.chi2_contingency(tab)` |
| `test$statistic; test$p.value` | `test.statistic; test.pvalue  # t/correlation` |

### Linear & binary logistic regression

Use the same complete rows and categorical reference levels. Formulas include an intercept; 0 + removes it. C(cyl) treats cyl as categorical. Binary am must be numeric 0/1.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `fit <- lm(mpg ~ wt + factor(cyl), data=df)` | `fit = smf.ols("mpg ~ wt + C(cyl)",`<br>` data=df).fit()` |
| `summary(fit); coef(fit); confint(fit)` | `fit.summary(); fit.params; fit.conf_int()` |
| `predict(fit, newdata=new)` | `fit.predict(new)` |
| `predict(fit, newdata=new,`<br>` interval="confidence")` | `fit.get_prediction(new).summary_frame()`<br>`# mean_ci_*: mean; obs_ci_*: observation` |
| `logit <- glm(am ~ wt + hp, data=df,`<br>` family=binomial())` | `logit = smf.logit("am ~ wt + hp",`<br>` data=df).fit(disp=False)` |
| `predict(logit, newdata=new, type="response")` | `logit.predict(new)  # probabilities` |
| `exp(coef(logit))` | `np.exp(logit.params)  # odds ratios` |

### Syntax, iteration & array habits

| R operation / intent | Python equivalent |
| :--- | :--- |
| `TRUE; FALSE; NULL; x <- 1` | `True; False; None; x = 1` |
| `c(1, 2, 3)` | `np.array([1, 2, 3])  # arithmetic vector` |
| `list(a=1, b=2)` | `{"a": 1, "b": 2}  # dictionary` |
| `function(x) x * 2` | `lambda x: x * 2` |
| `lapply(named_list, FUN)  # keep names` | `{k: fun(v) for k, v in items.items()}` |
| `Map(FUN, xs, ys)` | `list(map(fun, xs, ys))` |
| `by(df, df$group, FUN)` | `{k: fun(part) for k, part in`<br>` df.groupby("group")}` |
| `mean(v, na.rm=TRUE)  # NumPy array v` | `np.nanmean(v)` |
| `set.seed(42); rnorm(3)` | `rng = np.random.default_rng(42)`<br>`rng.normal(size=3)  # differs from R` |
| `plot(df$age, df$score)` | `import matplotlib.pyplot as plt`<br>`plt.scatter(df["age"], df["score"])` |

**Remember:** Match statistical defaults and methods: rank-test statistics and p-value approximations can differ. pandas Series align labels in arithmetic/assignment; use to_numpy() only for intentional positional matching. Python lists concatenate with +; NumPy arrays add elementwise. zip(strict=True) rejects unequal lengths (Python 3.10+); map truncates. vapply needs explicit output validation; rapply needs recursion. np.vectorize is a loop convenience, not a speed guarantee.

## 5. Probability distributions: d / p / q / r

### Translate the R prefix

Import: from scipy import stats. dist is a configured distribution from the table below. For random draws, first set rng = np.random.default_rng(42).

| R operation / intent | Python equivalent |
| :--- | :--- |
| `d*(x, ...)  # continuous density` | `dist.pdf(x)` |
| `d*(k, ...)  # discrete P(X = k)` | `dist.pmf(k)` |
| `p*(x, ...)  # P(X <= x)` | `dist.cdf(x)` |
| `p*(x, ..., lower.tail=FALSE)` | `dist.sf(x)  # P(X > x)` |
| `q*(p, ...)` | `dist.ppf(p)  # inverse CDF / quantile` |
| `q*(p, ..., lower.tail=FALSE)` | `dist.isf(p)  # upper-tail quantile` |
| `r*(n, ...)` | `dist.rvs(size=n, random_state=rng)` |
| `d*(x, ..., log=TRUE)` | `dist.logpdf(x) / dist.logpmf(x)` |
| `p*(x, ..., log.p=TRUE)` | `dist.logcdf(x)  # logsf(x) for upper tail` |

### Choose the distribution & translate its parameters

Each expression creates dist; then use the methods above. For example, pnorm(12, 10, 2) → stats.norm(loc=10, scale=2).cdf(12); dpois(2, 3) → stats.poisson(mu=3).pmf(2). Parameter names below are placeholders.

| R operation / intent | Python equivalent |
| :--- | :--- |
| `norm: mean=mu, sd=sigma` | `stats.norm(loc=mu, scale=sigma)` |
| `pois: lambda=lam` | `stats.poisson(mu=lam)` |
| `binom: size=trials, prob=p` | `stats.binom(n=trials, p=p)` |
| `nbinom: size=s, prob=p` | `stats.nbinom(n=s, p=p)` |
| `nbinom: size=s, mu=m` | `stats.nbinom(n=s, p=s/(s+m))` |
| `geom: prob=p  # failures before success` | `stats.geom(p=p, loc=-1)` |
| `hyper: m=good, n=bad, k=draws` | `stats.hypergeom(M=good+bad,`<br>` n=good, N=draws)` |
| `unif: min=a, max=b` | `stats.uniform(loc=a, scale=b-a)` |
| `exp: rate=r` | `stats.expon(scale=1/r)` |
| `gamma: shape=k, rate=r` | `stats.gamma(a=k, scale=1/r)` |
| `beta: shape1=a, shape2=b` | `stats.beta(a=a, b=b)` |
| `t: df=v; chisq: df=v` | `stats.t(df=v); stats.chi2(df=v)` |
| `f: df1=v1, df2=v2` | `stats.f(dfn=v1, dfd=v2)` |
| `lnorm: meanlog=m, sdlog=s` | `stats.lognorm(s=s, scale=np.exp(m))` |
| `weibull: shape=k, scale=s` | `stats.weibull_min(c=k, scale=s)` |

### Count probabilities & interval probabilities

| R operation / intent | Python equivalent |
| :--- | :--- |
| `ppois(2, 3)  # at most 2` | `stats.poisson(mu=3).cdf(2)` |
| `ppois(1, 3, lower.tail=FALSE)  # at least 2` | `stats.poisson(mu=3).sf(1)` |
| `pnorm(b) - pnorm(a)  # a < X <= b` | `stats.norm.cdf(b) - stats.norm.cdf(a)` |

**Remember:** Density is not point probability for continuous variables. Use sf(x) for upper tails; it is more accurate than 1 - cdf(x). For integer counts, P(X >= k) = sf(k - 1). Normal scale = SD; exponential/gamma scale = 1/rate; uniform scale = max - min. R geometric starts at 0, so use loc=-1. Discrete ppf(0) can differ from R at the support boundary. The same seed does not reproduce R samples. t / chisq / f above are central distributions.
