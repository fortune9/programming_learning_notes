Learning tidymodels: A Modern Framework for Modeling in R
================
Learning Notes
2026-03-26

  - [1 Introduction to tidymodels](#1-introduction-to-tidymodels)
      - [1.1 Core Packages](#11-core-packages)
  - [2 The tidymodels Workflow](#2-the-tidymodels-workflow)
  - [3 1. Data Splitting with rsample](#3-1-data-splitting-with-rsample)
      - [3.1 Basic Train/Test Split](#31-basic-traintest-split)
      - [3.2 Cross-Validation](#32-cross-validation)
      - [3.3 Validation Set](#33-validation-set)
      - [3.4 Key Methods for rsample
        Objects](#34-key-methods-for-rsample-objects)
          - [3.4.1 For `initial_split`
            objects:](#341-for-initial_split-objects)
          - [3.4.2 For resampling objects (`vfold_cv`, `bootstraps`,
            etc.):](#342-for-resampling-objects-vfold_cv-bootstraps-etc)
          - [3.4.3 Common resampling
            functions:](#343-common-resampling-functions)
      - [3.5 Cross-Package
        Compatibility](#35-cross-package-compatibility)
  - [4 2. Feature Engineering with
    recipes](#4-2-feature-engineering-with-recipes)
      - [4.1 Basic Recipe](#41-basic-recipe)
      - [4.2 Common Recipe Steps](#42-common-recipe-steps)
      - [4.3 Important Recipe Concepts](#43-important-recipe-concepts)
          - [4.3.1 Recipes as Blueprints](#431-recipes-as-blueprints)
          - [4.3.2 Variable Roles](#432-variable-roles)
          - [4.3.3 Recipe Role Selectors](#433-recipe-role-selectors)
          - [4.3.4 Handling Class Imbalance in
            Recipes](#434-handling-class-imbalance-in-recipes)
      - [4.4 Key Methods for Recipe
        Objects](#44-key-methods-for-recipe-objects)
          - [4.4.1 Important `prep()`
            arguments:](#441-important-prep-arguments)
          - [4.4.2 Important `bake()`
            arguments:](#442-important-bake-arguments)
      - [4.5 Recipe Step Categories](#45-recipe-step-categories)
  - [5 3. Model Specification with
    parsnip](#5-3-model-specification-with-parsnip)
      - [5.1 Linear Regression](#51-linear-regression)
      - [5.2 Elastic Net Regression (Regularized
        Regression)](#52-elastic-net-regression-regularized-regression)
          - [5.2.1 When to Use Each Regularization
            Method](#521-when-to-use-each-regularization-method)
      - [5.3 Random Forest](#53-random-forest)
      - [5.4 Boosted Trees (XGBoost)](#54-boosted-trees-xgboost)
      - [5.5 Other Common Models](#55-other-common-models)
      - [5.6 Key Methods for Parsnip Model
        Objects](#56-key-methods-for-parsnip-model-objects)
          - [5.6.1 For model specifications (before
            fitting):](#561-for-model-specifications-before-fitting)
          - [5.6.2 For fitted models (after
            fitting):](#562-for-fitted-models-after-fitting)
          - [5.6.3 Available prediction types by
            mode:](#563-available-prediction-types-by-mode)
  - [6 4. Creating Workflows](#6-4-creating-workflows)
      - [6.1 Basic Workflow](#61-basic-workflow)
      - [6.2 Fit Workflow](#62-fit-workflow)
      - [6.3 Multiple Workflows](#63-multiple-workflows)
      - [6.4 Key Methods for Workflow
        Objects](#64-key-methods-for-workflow-objects)
          - [6.4.1 Building workflows:](#641-building-workflows)
          - [6.4.2 Fitting and using
            workflows:](#642-fitting-and-using-workflows)
          - [6.4.3 Extracting from fitted
            workflows:](#643-extracting-from-fitted-workflows)
          - [6.4.4 Workflow sets (multiple
            workflows):](#644-workflow-sets-multiple-workflows)
  - [7 5. Hyperparameter Tuning](#7-5-hyperparameter-tuning)
      - [7.1 Define Tunable Parameters](#71-define-tunable-parameters)
      - [7.2 Grid Search](#72-grid-search)
      - [7.3 Random Search](#73-random-search)
      - [7.4 Space-Filling Designs (Irregular
        Grids)](#74-space-filling-designs-irregular-grids)
      - [7.5 Bayesian Optimization](#75-bayesian-optimization)
      - [7.6 Key Methods for Tuning
        Results](#76-key-methods-for-tuning-results)
          - [7.6.1 Exploring tuning
            results:](#761-exploring-tuning-results)
          - [7.6.2 Selecting best
            parameters:](#762-selecting-best-parameters)
          - [7.6.3 Finalizing workflows:](#763-finalizing-workflows)
          - [7.6.4 Special methods for `last_fit()`
            results:](#764-special-methods-for-last_fit-results)
  - [8 6. Model Evaluation with
    yardstick](#8-6-model-evaluation-with-yardstick)
      - [8.1 Regression Metrics](#81-regression-metrics)
      - [8.2 Classification Metrics](#82-classification-metrics)
      - [8.3 Key Methods for yardstick
        Metrics](#83-key-methods-for-yardstick-metrics)
          - [8.3.1 Using individual
            metrics:](#831-using-individual-metrics)
          - [8.3.2 Creating metric sets:](#832-creating-metric-sets)
          - [8.3.3 Confusion matrix
            methods:](#833-confusion-matrix-methods)
          - [8.3.4 ROC and PR curves:](#834-roc-and-pr-curves)
          - [8.3.5 Grouped and multi-class
            metrics:](#835-grouped-and-multi-class-metrics)
  - [9 7. Complete Example: End-to-End
    Workflow](#9-7-complete-example-end-to-end-workflow)
  - [10 8. Advanced Topics](#10-8-advanced-topics)
      - [10.1 Custom Metrics](#101-custom-metrics)
      - [10.2 Model Stacking](#102-model-stacking)
      - [10.3 Feature Importance](#103-feature-importance)
      - [10.4 Parallel Processing](#104-parallel-processing)
      - [10.5 Comparing Modeling Frameworks: tidymodels vs caret vs Base
        R](#105-comparing-modeling-frameworks-tidymodels-vs-caret-vs-base-r)
          - [10.5.1 Overview Comparison](#1051-overview-comparison)
          - [10.5.2 Detailed Comparison with
            Examples](#1052-detailed-comparison-with-examples)
          - [10.5.3 Pros and Cons](#1053-pros-and-cons)
          - [10.5.4 Migration Guide](#1054-migration-guide)
          - [10.5.5 Recommendation](#1055-recommendation)
          - [10.5.6 Real-World Performance
            Comparison](#1056-real-world-performance-comparison)
          - [10.5.7 When Speed vs Features
            Matters](#1057-when-speed-vs-features-matters)
          - [10.5.8 Summary Table: Practical
            Considerations](#1058-summary-table-practical-considerations)
  - [11 9. Using btw to Learn More](#11-9-using-btw-to-learn-more)
      - [11.1 Learn About Specific
        Functions](#111-learn-about-specific-functions)
      - [11.2 Get Package Overview](#112-get-package-overview)
      - [11.3 Interactive Learning with
        AI](#113-interactive-learning-with-ai)
  - [12 10. Best Practices](#12-10-best-practices)
      - [12.1 Data Leakage Prevention](#121-data-leakage-prevention)
      - [12.2 Workflow Organization](#122-workflow-organization)
      - [12.3 Model Comparison](#123-model-comparison)
  - [13 Resources](#13-resources)
      - [13.1 Documentation](#131-documentation)
      - [13.2 Learning with btw](#132-learning-with-btw)
      - [13.3 Community](#133-community)
      - [13.4 Comparisons and
        Benchmarks](#134-comparisons-and-benchmarks)
  - [14 Quick Reference](#14-quick-reference)
      - [14.1 Common Workflow Pattern](#141-common-workflow-pattern)

# 1 Introduction to tidymodels

`tidymodels` is a collection of packages for modeling and machine
learning using tidyverse principles. It provides a consistent, modular
framework for:

  - Data preprocessing and feature engineering
  - Model specification and training
  - Hyperparameter tuning
  - Model evaluation and comparison
  - Workflow management

Note that Tidymodels itself doesn’t implement any statistical or machine
learning models. It’s a framework to organize all the tasks around
modeling.

## 1.1 Core Packages

``` r
library(tidymodels) # Loads the core tidymodels packages
library(tidyverse) # For data manipulation

# Core packages included in tidymodels:
# - rsample: data splitting and resampling
# - recipes: data preprocessing and feature engineering
# - parsnip: unified model interface
# - workflows: combine preprocessing and modeling
# - tune: hyperparameter tuning
# - yardstick: model performance metrics
# - broom: tidy model outputs
# - dials: hyperparameter space definitions
```

-----

# 2 The tidymodels Workflow

A typical tidymodels workflow follows these steps:

1.  **Split data** (rsample)
2.  **Create recipe** for preprocessing (recipes)
3.  **Specify model** (parsnip)
4.  **Create workflow** (workflows)
5.  **Fit model** or **tune hyperparameters** (tune)
6.  **Evaluate performance** (yardstick)

-----

# 3 1. Data Splitting with rsample

## 3.1 Basic Train/Test Split

``` r
# Example dataset
data(ames, package = "modeldata")

# Set seed for reproducibility
set.seed(123)

# Split data: 75% training, 25% testing
ames_split <- initial_split(ames, prop = 0.75, strata = Sale_Price)

ames_train <- training(ames_split)
ames_test <- testing(ames_split)

cat("Training set size:", nrow(ames_train), "\n")
```

    ## Training set size: 2197

``` r
cat("Testing set size:", nrow(ames_test), "\n")
```

    ## Testing set size: 733

## 3.2 Cross-Validation

``` r
# 10-fold cross-validation
ames_folds <- vfold_cv(ames_train, v = 10, strata = Sale_Price)

# Bootstrap resampling
ames_boots <- bootstraps(ames_train, times = 25, strata = Sale_Price)

# Time-series cross-validation
# For time series data
# time_slices <- rolling_origin(data, initial = 365, assess = 30, cumulative = TRUE)
```

## 3.3 Validation Set

``` r
# Create train/validation/test split
set.seed(456)

# First split: separate test set
ames_split2 <- initial_split(ames, prop = 0.8, strata = Sale_Price)
ames_other <- training(ames_split2)
ames_test2 <- testing(ames_split2)

# Second split: separate training and validation
ames_val_split <- initial_split(ames_other, prop = 0.75, strata = Sale_Price)
ames_train2 <- training(ames_val_split)
ames_val <- testing(ames_val_split)
```

## 3.4 Key Methods for rsample Objects

Understanding the methods available for different rsample objects helps
you work efficiently with data splits and resamples.

### 3.4.1 For `initial_split` objects:

| Method              | Description                 | Returns           |
| :------------------ | :-------------------------- | :---------------- |
| `training(split)`   | Extract training data       | Data frame/tibble |
| `testing(split)`    | Extract test data           | Data frame/tibble |
| `complement(split)` | Get indices not in training | Integer vector    |

``` r
split <- initial_split(data, prop = 0.75)
train <- training(split)  # Get training set
test <- testing(split)    # Get test set
```

### 3.4.2 For resampling objects (`vfold_cv`, `bootstraps`, etc.):

| Method                 | Description                        | Returns         |
| :--------------------- | :--------------------------------- | :-------------- |
| `analysis(resample)`   | Extract analysis/training fold     | Data frame      |
| `assessment(resample)` | Extract assessment/validation fold | Data frame      |
| `rsample2caret(folds)` | Convert to caret format            | List of indices |
| `pretty.rsplit()`      | Print split information            | Text summary    |

``` r
folds <- vfold_cv(data, v = 10)

# Access individual fold
fold1 <- folds$splits[[1]]
fold1_train <- analysis(fold1)      # Training portion of fold 1
fold1_validate <- assessment(fold1) # Validation portion of fold 1

# Convert for caret compatibility
caret_indices <- rsample2caret(folds)
```

### 3.4.3 Common resampling functions:

| Function           | Purpose                 | Key Parameters                           |
| :----------------- | :---------------------- | :--------------------------------------- |
| `vfold_cv()`       | V-fold cross-validation | `v` (\# folds), `repeats`, `strata`      |
| `bootstraps()`     | Bootstrap resampling    | `times` (\# bootstrap samples), `strata` |
| `mc_cv()`          | Monte Carlo CV          | `prop`, `times`                          |
| `rolling_origin()` | Time series CV          | `initial`, `assess`, `cumulative`        |
| `group_vfold_cv()` | Grouped CV              | `group`, `v`                             |
| `loo_cv()`         | Leave-one-out CV        | None (one-per-observation)               |

## 3.5 Cross-Package Compatibility

If you need to compare tidymodels with caret using identical resamples:

``` r
# Create tidymodels folds
tidy_folds <- vfold_cv(ames_train, v = 10, strata = Sale_Price)

# Convert to caret format for fair comparison
caret_folds <- rsample2caret(tidy_folds)

# Now both packages use identical data splits
tidy_results <- workflow %>% fit_resamples(resamples = tidy_folds)
caret_results <- train(..., trControl = trainControl(index = caret_folds))

# Convert back if needed
back_to_tidy <- caret2rsample(caret_folds)
```

**Why this matters**: When benchmarking frameworks, using identical
resamples ensures performance differences are due to the framework, not
random variation in splits.

-----

# 4 2. Feature Engineering with recipes

Recipes define preprocessing steps that are applied consistently to
training and test data.

## 4.1 Basic Recipe

``` r
# Create a simple recipe
ames_recipe <- recipe(Sale_Price ~ ., data = ames_train) %>%
  # Remove zero variance predictors
  step_zv(all_predictors()) %>%
  # Normalize numeric predictors
  step_normalize(all_numeric_predictors()) %>%
  # Create dummy variables for factors
  step_dummy(all_nominal_predictors())

# View recipe
ames_recipe
```

## 4.2 Common Recipe Steps

``` r
advanced_recipe <- recipe(Sale_Price ~ ., data = ames_train) %>%
  # Handle missing data
  step_impute_median(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  # Feature engineering
  step_log(Sale_Price, base = 10) %>% # Log transform outcome
  step_date(all_date_predictors(), features = c("dow", "month", "year")) %>%
  # Handle categorical variables
  step_other(all_nominal_predictors(), threshold = 0.01) %>% # Pool rare levels
  step_dummy(all_nominal_predictors(), one_hot = FALSE) %>%
  # Handle correlations and variance
  step_zv(all_predictors()) %>%
  step_corr(all_numeric_predictors(), threshold = 0.9) %>%
  # Normalization (choose one)
  step_normalize(all_numeric_predictors()) %>% # Center and scale
  # step_range(all_numeric_predictors(), min = 0, max = 1) %>%  # Scale to range

  # Interaction terms
  step_interact(~ Gr_Liv_Area:starts_with("Bldg_Type"))

# Prep and bake to see the result
advanced_recipe %>%
  prep() %>%
  bake(new_data = NULL) %>%
  glimpse()
```

    ## Rows: 2,197
    ## Columns: 190
    ## $ Lot_Frontage                                          <dbl> 0.36988074, -1.0…
    ## $ Lot_Area                                              <dbl> -0.20459440, -0.…
    ## $ Year_Built                                            <dbl> -0.05555905, -0.…
    ## $ Year_Remod_Add                                        <dbl> -0.69017890, -0.…
    ## $ Mas_Vnr_Area                                          <dbl> -0.56135250, 2.1…
    ## $ BsmtFin_SF_1                                          <dbl> -1.4273777, 0.81…
    ## $ BsmtFin_SF_2                                          <dbl> 0.1896883, -0.29…
    ## $ Bsmt_Unf_SF                                           <dbl> -1.26061912, -0.…
    ## $ Total_Bsmt_SF                                         <dbl> -0.36424940, -1.…
    ## $ First_Flr_SF                                          <dbl> -0.6958220444, -…
    ## $ Second_Flr_SF                                         <dbl> -0.78663287, 0.5…
    ## $ Gr_Liv_Area                                           <dbl> -1.20792407, -0.…
    ## $ Bsmt_Full_Bath                                        <dbl> 1.0905034, -0.81…
    ## $ Bsmt_Half_Bath                                        <dbl> -0.2518688, -0.2…
    ## $ Full_Bath                                             <dbl> -1.0481912, -1.0…
    ## $ Half_Bath                                             <dbl> -0.7489047, 1.24…
    ## $ Bedroom_AbvGr                                         <dbl> -1.0405629, 0.16…
    ## $ Kitchen_AbvGr                                         <dbl> -0.208534, -0.20…
    ## $ TotRms_AbvGrd                                         <dbl> -1.5335141, -0.2…
    ## $ Fireplaces                                            <dbl> -0.9220114, -0.9…
    ## $ Garage_Cars                                           <dbl> 0.3023882, -1.00…
    ## $ Garage_Area                                           <dbl> 0.2405208, -0.69…
    ## $ Wood_Deck_SF                                          <dbl> 1.15922645, -0.7…
    ## $ Open_Porch_SF                                         <dbl> -0.69380079, -0.…
    ## $ Enclosed_Porch                                        <dbl> -0.3437388, -0.3…
    ## $ Three_season_porch                                    <dbl> -0.09663697, -0.…
    ## $ Screen_Porch                                          <dbl> -0.2870279, -0.2…
    ## $ Misc_Val                                              <dbl> -0.08536273, -0.…
    ## $ Mo_Sold                                               <dbl> -0.79073528, -1.…
    ## $ Year_Sold                                             <dbl> 1.669834, 1.6698…
    ## $ Longitude                                             <dbl> 0.6225228, 0.606…
    ## $ Latitude                                              <dbl> 1.03393870, 0.94…
    ## $ Sale_Price                                            <dbl> 5.100371, 5.0232…
    ## $ MS_SubClass_One_Story_1945_and_Older                  <dbl> -0.2194655, -0.2…
    ## $ MS_SubClass_One_and_Half_Story_Finished_All_Ages      <dbl> -0.3309775, -0.3…
    ## $ MS_SubClass_Two_Story_1946_and_Newer                  <dbl> -0.4974675, -0.4…
    ## $ MS_SubClass_Two_Story_1945_and_Older                  <dbl> -0.2090109, -0.2…
    ## $ MS_SubClass_Split_or_Multilevel                       <dbl> -0.2066285, -0.2…
    ## $ MS_SubClass_Split_Foyer                               <dbl> -0.1272059, -0.1…
    ## $ MS_SubClass_One_Story_PUD_1946_and_Newer              <dbl> -0.2744905, -0.2…
    ## $ MS_SubClass_Two_Story_PUD_1946_and_Newer              <dbl> -0.2206019, 4.53…
    ## $ MS_SubClass_Two_Family_conversion_All_Styles_and_Ages <dbl> -0.1462042, -0.1…
    ## $ MS_SubClass_other                                     <dbl> -0.1429241, -0.1…
    ## $ MS_Zoning_Residential_Low_Density                     <dbl> 0.5440867, -1.83…
    ## $ MS_Zoning_Residential_Medium_Density                  <dbl> -0.4352129, 2.29…
    ## $ MS_Zoning_other                                       <dbl> -0.1412578, -0.1…
    ## $ Street_other                                          <dbl> -0.0709206, -0.0…
    ## $ Alley_No_Alley_Access                                 <dbl> 0.2744905, 0.274…
    ## $ Alley_Paved                                           <dbl> -0.1731792, -0.1…
    ## $ Lot_Shape_Slightly_Irregular                          <dbl> -0.7234225, -0.7…
    ## $ Lot_Shape_Moderately_Irregular                        <dbl> -0.1616914, -0.1…
    ## $ Lot_Shape_other                                       <dbl> -0.06412077, -0.…
    ## $ Land_Contour_HLS                                      <dbl> -0.211371, -0.21…
    ## $ Land_Contour_Low                                      <dbl> -0.1429241, -0.1…
    ## $ Land_Contour_Lvl                                      <dbl> 0.3468313, 0.346…
    ## $ Utilities_other                                       <dbl> -0.03696949, -0.…
    ## $ Lot_Config_CulDSac                                    <dbl> -0.2497013, -0.2…
    ## $ Lot_Config_FR2                                        <dbl> -0.1773163, -0.1…
    ## $ Lot_Config_Inside                                     <dbl> -1.6538286, 0.60…
    ## $ Lot_Config_other                                      <dbl> -0.0740911, -0.0…
    ## $ Land_Slope_Mod                                        <dbl> -0.2183242, -0.2…
    ## $ Land_Slope_other                                      <dbl> -0.06760468, -0.…
    ## $ Neighborhood_College_Creek                            <dbl> -0.3198619, -0.3…
    ## $ Neighborhood_Old_Town                                 <dbl> -0.2941234, -0.2…
    ## $ Neighborhood_Edwards                                  <dbl> -0.266744, -0.26…
    ## $ Neighborhood_Somerset                                 <dbl> -0.2628085, -0.2…
    ## $ Neighborhood_Northridge_Heights                       <dbl> -0.2445188, -0.2…
    ## $ Neighborhood_Gilbert                                  <dbl> -0.242422, -0.24…
    ## $ Neighborhood_Sawyer                                   <dbl> -0.2228605, -0.2…
    ## $ Neighborhood_Northwest_Ames                           <dbl> -0.2194655, -0.2…
    ## $ Neighborhood_Sawyer_West                              <dbl> -0.2262142, -0.2…
    ## $ Neighborhood_Mitchell                                 <dbl> -0.1956076, -0.1…
    ## $ Neighborhood_Brookside                                <dbl> -0.1905367, -0.1…
    ## $ Neighborhood_Crawford                                 <dbl> -0.1879572, -0.1…
    ## $ Neighborhood_Iowa_DOT_and_Rail_Road                   <dbl> -0.1918152, -0.1…
    ## $ Neighborhood_Timberland                               <dbl> -0.1631668, -0.1…
    ## $ Neighborhood_Northridge                               <dbl> -0.1556644, -0.1…
    ## $ Neighborhood_Stone_Brook                              <dbl> -0.1361464, -0.1…
    ## $ Neighborhood_South_and_West_of_Iowa_State_University  <dbl> -0.1234609, -0.1…
    ## $ Neighborhood_Clear_Creek                              <dbl> -0.1196059, -0.1…
    ## $ Neighborhood_Meadow_Village                           <dbl> -0.1094102, -0.1…
    ## $ Neighborhood_Briardale                                <dbl> -0.1072608, 9.31…
    ## $ Neighborhood_other                                    <dbl> -0.1827043, -0.1…
    ## $ Condition_1_Feedr                                     <dbl> -0.2476383, -0.2…
    ## $ Condition_1_Norm                                      <dbl> 0.4097796, 0.409…
    ## $ Condition_1_PosN                                      <dbl> -0.1215478, -0.1…
    ## $ Condition_1_RRAn                                      <dbl> -0.1308504, -0.1…
    ## $ Condition_1_other                                     <dbl> -0.1510018, -0.1…
    ## $ Condition_2_other                                     <dbl> -0.1005502, -0.1…
    ## $ Bldg_Type_Duplex                                      <dbl> -0.1993384, -0.1…
    ## $ Bldg_Type_Twnhs                                       <dbl> -0.1905367, 5.24…
    ## $ Bldg_Type_TwnhsE                                      <dbl> -0.3049467, -0.3…
    ## $ House_Style_One_Story                                 <dbl> 0.9902613, -1.00…
    ## $ House_Style_SFoyer                                    <dbl> -0.1660823, -0.1…
    ## $ House_Style_Two_Story                                 <dbl> -0.6558526, 1.52…
    ## $ House_Style_other                                     <dbl> -0.1344026, -0.1…
    ## $ Overall_Cond_Below_Average                            <dbl> -0.1853469, -0.1…
    ## $ Overall_Cond_Average                                  <dbl> 0.8645646, 0.864…
    ## $ Overall_Cond_Above_Average                            <dbl> -0.4615679, -0.4…
    ## $ Overall_Cond_Good                                     <dbl> -0.3883242, -0.3…
    ## $ Overall_Cond_Very_Good                                <dbl> -0.2306245, -0.2…
    ## $ Overall_Cond_Excellent                                <dbl> -0.11563, -0.115…
    ## $ Overall_Cond_other                                    <dbl> -0.07713411, -0.…
    ## $ Roof_Style_Hip                                        <dbl> -0.4810373, -0.4…
    ## $ Roof_Style_other                                      <dbl> -0.1344026, -0.1…
    ## $ Roof_Matl_other                                       <dbl> -0.11563, -0.115…
    ## $ Exterior_1st_BrkFace                                  <dbl> -0.1689528, -0.1…
    ## $ Exterior_1st_CemntBd                                  <dbl> -0.2206019, -0.2…
    ## $ Exterior_1st_Plywood                                  <dbl> 3.4744616, -0.28…
    ## $ Exterior_1st_Stucco                                   <dbl> -0.11563, -0.115…
    ## $ Exterior_1st_Wd.Sdng                                  <dbl> -0.4029391, -0.4…
    ## $ Exterior_1st_WdShing                                  <dbl> -0.1445727, -0.1…
    ## $ Exterior_1st_other                                    <dbl> -0.06043983, -0.…
    ## $ Exterior_2nd_BrkFace                                  <dbl> -0.1253465, -0.1…
    ## $ Exterior_2nd_HdBoard                                  <dbl> -0.4014121, 2.49…
    ## $ Exterior_2nd_MetalSd                                  <dbl> -0.4225716, -0.4…
    ## $ Exterior_2nd_Plywood                                  <dbl> 3.0998630, -0.32…
    ## $ Exterior_2nd_Stucco                                   <dbl> -0.1253465, -0.1…
    ## $ Exterior_2nd_VinylSd                                  <dbl> -0.7256135, -0.7…
    ## $ Exterior_2nd_Wd.Sdng                                  <dbl> -0.3898745, -0.3…
    ## $ Exterior_2nd_Wd.Shng                                  <dbl> -0.1745678, -0.1…
    ## $ Exterior_2nd_other                                    <dbl> -0.1361464, -0.1…
    ## $ Mas_Vnr_Type_None                                     <dbl> 0.8072069, -1.23…
    ## $ Mas_Vnr_Type_Stone                                    <dbl> -0.3076127, -0.3…
    ## $ Mas_Vnr_Type_other                                    <dbl> -0.09086754, -0.…
    ## $ Exter_Cond_Good                                       <dbl> -0.3326673, -0.3…
    ## $ Exter_Cond_Typical                                    <dbl> 0.3805275, 0.380…
    ## $ Exter_Cond_other                                      <dbl> -0.06043983, -0.…
    ## $ Foundation_CBlock                                     <dbl> 1.1691170, 1.169…
    ## $ Foundation_PConc                                      <dbl> -0.906284, -0.90…
    ## $ Foundation_Slab                                       <dbl> -0.1378697, -0.1…
    ## $ Foundation_other                                      <dbl> -0.0709206, -0.0…
    ## $ Bsmt_Cond_Good                                        <dbl> -0.1956076, -0.1…
    ## $ Bsmt_Cond_Typical                                     <dbl> 0.3468313, 0.346…
    ## $ Bsmt_Cond_other                                       <dbl> -0.05652338, -0.…
    ## $ Bsmt_Exposure_Gd                                      <dbl> -0.318997, -0.31…
    ## $ Bsmt_Exposure_Mn                                      <dbl> -0.2950355, -0.2…
    ## $ Bsmt_Exposure_No                                      <dbl> 0.7256135, 0.725…
    ## $ Bsmt_Exposure_No_Basement                             <dbl> -0.1773163, -0.1…
    ## $ BsmtFin_Type_1_BLQ                                    <dbl> -0.3172626, -0.3…
    ## $ BsmtFin_Type_1_GLQ                                    <dbl> -0.6508892, -0.6…
    ## $ BsmtFin_Type_1_LwQ                                    <dbl> -0.2295283, -0.2…
    ## $ BsmtFin_Type_1_Rec                                    <dbl> -0.3181305, 3.14…
    ## $ BsmtFin_Type_1_Unf                                    <dbl> -0.6487642, -0.6…
    ## $ BsmtFin_Type_2_BLQ                                    <dbl> -0.1510018, -0.1…
    ## $ BsmtFin_Type_2_GLQ                                    <dbl> -0.1135927, -0.1…
    ## $ BsmtFin_Type_2_LwQ                                    <dbl> -0.1717806, -0.1…
    ## $ BsmtFin_Type_2_Rec                                    <dbl> 5.3179371, -0.18…
    ## $ BsmtFin_Type_2_Unf                                    <dbl> -2.4347279, 0.41…
    ## $ Heating_GasW                                          <dbl> -0.1028337, -0.1…
    ## $ Heating_other                                         <dbl> -0.08563145, -0.…
    ## $ Heating_QC_Fair                                       <dbl> -0.1905367, -0.1…
    ## $ Heating_QC_Good                                       <dbl> -0.4403787, -0.4…
    ## $ Heating_QC_Typical                                    <dbl> 1.5767592, 1.576…
    ## $ Heating_QC_other                                      <dbl> -0.03696949, -0.…
    ## $ Central_Air_Y                                         <dbl> 0.2706374, 0.270…
    ## $ Electrical_FuseF                                      <dbl> -0.1361464, -0.1…
    ## $ Electrical_SBrkr                                      <dbl> 0.3049467, 0.304…
    ## $ Electrical_other                                      <dbl> -0.05231854, -0.…
    ## $ Functional_Min2                                       <dbl> -0.1587037, -0.1…
    ## $ Functional_Mod                                        <dbl> -0.1050696, -0.1…
    ## $ Functional_Typ                                        <dbl> 0.278305, 0.2783…
    ## $ Functional_other                                      <dbl> -0.1094102, -0.1…
    ## $ Garage_Type_Basment                                   <dbl> -0.1135927, -0.1…
    ## $ Garage_Type_BuiltIn                                   <dbl> -0.2588287, -0.2…
    ## $ Garage_Type_Detchd                                    <dbl> -0.6064879, 1.64…
    ## $ Garage_Type_No_Garage                                 <dbl> -0.242422, -0.24…
    ## $ Garage_Type_other                                     <dbl> -0.1176338, -0.1…
    ## $ Garage_Finish_RFn                                     <dbl> -0.6240589, -0.6…
    ## $ Garage_Finish_Unf                                     <dbl> -0.8485933, 1.17…
    ## $ Garage_Cond_Typical                                   <dbl> 0.3172626, 0.317…
    ## $ Garage_Cond_other                                     <dbl> -0.1072608, -0.1…
    ## $ Paved_Drive_Partial_Pavement                          <dbl> -0.1462042, -0.1…
    ## $ Paved_Drive_Paved                                     <dbl> 0.3267299, 0.326…
    ## $ Pool_QC_other                                         <dbl> -0.0709206, -0.0…
    ## $ Fence_Good_Wood                                       <dbl> -0.203011, -0.20…
    ## $ Fence_Minimum_Privacy                                 <dbl> 2.8819334, -0.34…
    ## $ Fence_No_Fence                                        <dbl> -2.0655852, 0.48…
    ## $ Fence_other                                           <dbl> -0.06043983, -0.…
    ## $ Misc_Feature_Shed                                     <dbl> -0.1745678, -0.1…
    ## $ Misc_Feature_other                                    <dbl> -0.06412077, -0.…
    ## $ Sale_Type_WD.                                         <dbl> 0.3906485, 0.390…
    ## $ Sale_Type_other                                       <dbl> -0.1510018, -0.1…
    ## $ Sale_Condition_Family                                 <dbl> -0.1326376, -0.1…
    ## $ Sale_Condition_Normal                                 <dbl> 0.4695265, 0.469…
    ## $ Sale_Condition_Partial                                <dbl> -0.3013679, -0.3…
    ## $ Sale_Condition_other                                  <dbl> -0.1135927, -0.1…
    ## $ Gr_Liv_Area_x_Bldg_Type_Duplex                        <dbl> 0.24078569, 0.15…
    ## $ Gr_Liv_Area_x_Bldg_Type_Twnhs                         <dbl> 0.23015383, -4.1…
    ## $ Gr_Liv_Area_x_Bldg_Type_TwnhsE                        <dbl> 0.36835244, 0.24…

## 4.3 Important Recipe Concepts

### 4.3.1 Recipes as Blueprints

**Key insight**: A recipe is a *blueprint* that defines your
preprocessing steps **before their actual execution**. This ensures: -
Preprocessing is consistent between training and test data - Statistics
(means, SDs, etc.) are computed only on training data - No data leakage
occurs

``` r
# Recipe creation (just defines the steps)
my_recipe <- recipe(y ~ ., data = train) %>%
  step_normalize(all_numeric_predictors()) # Doesn't normalize yet!

# Prepare recipe (calculates statistics from training data)
prepped_recipe <- prep(my_recipe, training = train)

# Apply recipe (uses training statistics)
train_processed <- bake(prepped_recipe, new_data = train)
test_processed <- bake(prepped_recipe, new_data = test) # Uses train stats!
```

### 4.3.2 Variable Roles

Tidymodels allows assigning roles to variables - useful for keeping IDs
without using them in modeling:

``` r
recipe(outcome ~ ., data = train) %>%
  update_role(employee_id, new_role = "id") %>% # Keep but don't model
  step_normalize(all_numeric_predictors())

# employee_id is retained but excluded from preprocessing and modeling
```

### 4.3.3 Recipe Role Selectors

Recipes provides powerful selector functions to target specific groups
of variables based on their role and type. These are essential for
writing flexible, maintainable preprocessing code.

| Selector Function          | Description                                    | Example Use Case                     |
| :------------------------- | :--------------------------------------------- | :----------------------------------- |
| `all_predictors()`         | All predictor variables (not outcomes)         | Apply transformation to all features |
| `all_outcomes()`           | All outcome/target variables                   | Transform the response variable      |
| `all_numeric()`            | All numeric variables (including outcomes)     | Select all numeric columns           |
| `all_nominal()`            | All categorical variables (factors/characters) | Select all categorical columns       |
| `all_numeric_predictors()` | Numeric predictor variables only               | Normalize or scale features          |
| `all_nominal_predictors()` | Categorical predictor variables only           | Create dummy variables               |
| `has_role()`               | Variables with a specific role                 | Target custom roles like “ID”        |
| `has_type()`               | Variables of a specific type                   | Target specific data types           |

**Type-based selectors:**

| Selector Function | Selects                  |
| :---------------- | :----------------------- |
| `all_integer()`   | Integer columns          |
| `all_double()`    | Double/numeric columns   |
| `all_logical()`   | Logical/boolean columns  |
| `all_string()`    | Character/string columns |
| `all_factor()`    | Factor columns           |
| `all_ordered()`   | Ordered factor columns   |
| `all_date()`      | Date columns             |
| `all_datetime()`  | Datetime columns         |

**Combining selectors:**

``` r
recipe(Sale_Price ~ ., data = train) %>%
  # Normalize all numeric predictors
  step_normalize(all_numeric_predictors()) %>%

  # Create dummies for all categorical predictors
  step_dummy(all_nominal_predictors()) %>%

  # Log transform outcome and specific predictors
  step_log(all_outcomes(), Lot_Area, Gr_Liv_Area) %>%

  # Remove zero variance from all predictors
  step_zv(all_predictors()) %>%

  # Use tidyselect helpers
  step_rm(starts_with("temp_")) %>%
  step_interact(~ Gr_Liv_Area:ends_with("_Area"))
```

**Using `has_role()` for custom roles:**

``` r
recipe(Sale_Price ~ ., data = train) %>%
  # Assign custom roles
  update_role(property_id, new_role = "id") %>%
  update_role(sale_date, new_role = "date_variable") %>%

  # Target variables by custom role
  step_rm(has_role("id")) %>%  # Remove ID variables before modeling
  step_date(has_role("date_variable"), features = c("month", "year"))
```

**Selector precedence and specificity:**

  - Selectors are evaluated in order within each step
  - More specific selectors override general ones when combined
  - Use `-` to exclude: `step_normalize(all_numeric_predictors(),
    -Sale_Price)`

### 4.3.4 Handling Class Imbalance in Recipes

Use the `themis` package for oversampling/undersampling:

``` r
library(themis)

balanced_recipe <- recipe(churn ~ ., data = train) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_rose(churn) # ROSE algorithm for synthetic oversampling

# Other options:
# step_upsample() - random oversampling
# step_downsample() - random undersampling
# step_smote() - SMOTE algorithm
# step_adasyn() - ADASYN algorithm
```

## 4.4 Key Methods for Recipe Objects

Recipe objects have specific methods for preparation, application, and
inspection.

| Method                   | Description                             | When to Use                              | Returns             |
| :----------------------- | :-------------------------------------- | :--------------------------------------- | :------------------ |
| `prep(recipe)`           | Calculate statistics from training data | After defining recipe, before applying   | Prepped recipe      |
| `bake(recipe, new_data)` | Apply recipe to new data                | After prep(), for test/new data          | Processed data      |
| `juice(recipe)`          | Extract processed training data         | After prep(), shortcut for training data | Processed data      |
| `tidy(recipe)`           | Extract step information                | Inspect what each step does              | Tibble of steps     |
| `summary(recipe)`        | Variable summary                        | See variable roles and types             | Tibble of variables |
| `update_role()`          | Change variable roles                   | Assign custom roles (e.g., “ID”)         | Updated recipe      |
| `step_*()`               | Add preprocessing steps                 | Building the recipe                      | Updated recipe      |

``` r
# Create recipe
my_recipe <- recipe(y ~ ., data = train) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors())

# Prepare (fit to training data)
prepped_recipe <- prep(my_recipe, training = train)

# Apply to data
train_processed <- juice(prepped_recipe)              # Training data (cached)
test_processed <- bake(prepped_recipe, new_data = test) # Test data

# Inspect recipe
summary(prepped_recipe)       # See all variables and their roles
tidy(prepped_recipe)          # See all steps
tidy(prepped_recipe, number = 1)  # See specific step details
```

### 4.4.1 Important `prep()` arguments:

| Argument             | Description                       | Default  |
| :------------------- | :-------------------------------- | :------- |
| `training`           | Data to calculate statistics from | Required |
| `fresh`              | Recalculate from scratch?         | `FALSE`  |
| `verbose`            | Print progress?                   | `FALSE`  |
| `retain`             | Keep processed training data?     | `TRUE`   |
| `strings_as_factors` | Convert strings to factors?       | `TRUE`   |

### 4.4.2 Important `bake()` arguments:

| Argument      | Description                                          | Default       |
| :------------ | :--------------------------------------------------- | :------------ |
| `new_data`    | Data to process (use `NULL` for training)            | Required      |
| `composition` | How to return data (“tibble”, “matrix”, “dgCMatrix”) | “tibble”      |
| `...`         | Specific variables to return                         | All variables |

``` r
# Bake specific columns only
bake(prepped_recipe, new_data = test, Sale_Price, Gr_Liv_Area)

# Return as matrix for some models
bake(prepped_recipe, new_data = test, composition = "matrix")
```

## 4.5 Recipe Step Categories

``` r
# Data cleaning
step_filter() # Filter rows
step_select() # Select columns
step_naomit() # Remove rows with NAs
step_zv() # Remove zero variance
step_nzv() # Remove near-zero variance

# Missing data
step_impute_mean() # Impute with mean
step_impute_median() # Impute with median
step_impute_mode() # Impute with mode
step_impute_knn() # KNN imputation
step_impute_bag() # Bagged tree imputation

# Transformations
step_log() # Log transformation
step_sqrt() # Square root
step_BoxCox() # Box-Cox transformation
step_YeoJohnson() # Yeo-Johnson transformation

# Categorical variables
step_dummy() # Create dummy variables
step_other() # Pool infrequent levels
step_novel() # Handle new factor levels in test data
step_unknown() # Assign missing to "unknown" level

# Normalization
step_normalize() # Center and scale (z-score)
step_center() # Center only
step_scale() # Scale only
step_range() # Scale to min-max range

# Feature engineering
step_poly() # Polynomial features
step_interact() # Interaction terms
step_date() # Extract date features
step_holiday() # Create holiday indicators
step_pca() # Principal component analysis
step_ica() # Independent component analysis

# Text processing
step_tokenize() # Tokenize text
step_stopwords() # Remove stop words
step_stem() # Stem words
step_tf() # Term frequency
step_tfidf() # TF-IDF
```

-----

# 5 3. Model Specification with parsnip

Parsnip provides a unified interface to many modeling engines.

## 5.1 Linear Regression

``` r
# Specify linear regression model
lm_spec <- linear_reg() %>%
  set_engine("lm") %>%
  set_mode("regression")

# Alternative engines
# lm_spec_glmnet <- linear_reg(penalty = 0.1, mixture = 0.5) %>%
#   set_engine("glmnet")
#
# lm_spec_stan <- linear_reg() %>%
#   set_engine("stan")
```

## 5.2 Elastic Net Regression (Regularized Regression)

Elastic Net combines L1 (Lasso) and L2 (Ridge) regularization,
controlled by the `mixture` parameter.

``` r
# Elastic Net with glmnet engine
# mixture: 0 = Ridge, 1 = Lasso, 0.5 = Elastic Net
# penalty: amount of regularization (lambda)

# Ridge Regression (L2 only)
ridge_spec <- linear_reg(penalty = 0.1, mixture = 0) %>%
  set_engine("glmnet") %>%
  set_mode("regression")

# Lasso Regression (L1 only)
lasso_spec <- linear_reg(penalty = 0.1, mixture = 1) %>%
  set_engine("glmnet") %>%
  set_mode("regression")

# Elastic Net (mix of L1 and L2)
elastic_spec <- linear_reg(penalty = 0.1, mixture = 0.5) %>%
  set_engine("glmnet") %>%
  set_mode("regression")

# For tuning penalty and mixture
elastic_tune_spec <- linear_reg(
  penalty = tune(),
  mixture = tune()
) %>%
  set_engine("glmnet") %>%
  set_mode("regression")
```

### 5.2.1 When to Use Each Regularization Method

``` r
# Ridge (mixture = 0):
# - Good when all predictors are relevant
# - Shrinks coefficients but keeps all variables
# - Better for multicollinearity
# - Use when: p < n and you want to keep all features

# Lasso (mixture = 1):
# - Good for feature selection
# - Shrinks some coefficients to exactly zero
# - Creates sparse models
# - Use when: you have many irrelevant features

# Elastic Net (mixture = 0.1 to 0.9):
# - Balances feature selection and coefficient shrinkage
# - Good when features are correlated
# - More stable than Lasso with correlated predictors
# - Use when: p > n or highly correlated features

# Tuning example with elastic net
elastic_recipe <- recipe(Sale_Price ~ ., data = ames_train) %>%
  step_log(Sale_Price) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors())

elastic_workflow <- workflow() %>%
  add_recipe(elastic_recipe) %>%
  add_model(elastic_tune_spec)

# Create tuning grid
elastic_grid <- grid_regular(
  penalty(range = c(-5, 0)), # 10^-5 to 10^0
  mixture(range = c(0, 1)),
  levels = c(penalty = 10, mixture = 5)
)

# Tune
elastic_results <- elastic_workflow %>%
  tune_grid(
    resamples = ames_folds,
    grid = elastic_grid,
    metrics = metric_set(rmse, rsq)
  )

# View best parameters
elastic_results %>%
  show_best(metric = "rmse")

# Visualize
elastic_results %>%
  collect_metrics() %>%
  filter(.metric == "rmse") %>%
  ggplot(aes(x = penalty, y = mean, color = factor(mixture))) +
  geom_line() +
  geom_point() +
  scale_x_log10() +
  labs(
    title = "Elastic Net Tuning Results",
    x = "Penalty (lambda)",
    y = "RMSE",
    color = "Mixture (alpha)"
  )
```

## 5.3 Random Forest

``` r
# Random forest for regression
rf_spec <- rand_forest(
  trees = 1000,
  min_n = 5
) %>%
  set_engine("ranger", importance = "impurity") %>%
  set_mode("regression")

# For classification
rf_class_spec <- rand_forest(
  trees = 1000,
  min_n = 5
) %>%
  set_engine("ranger") %>%
  set_mode("classification")
```

## 5.4 Boosted Trees (XGBoost)

``` r
# XGBoost specification
xgb_spec <- boost_tree(
  trees = 1000,
  tree_depth = 6,
  learn_rate = 0.01,
  loss_reduction = 0,
  sample_size = 0.8,
  mtry = 10,
  min_n = 5
) %>%
  set_engine("xgboost") %>%
  set_mode("regression")
```

## 5.5 Other Common Models

``` r
# Logistic regression
logistic_spec <- logistic_reg() %>%
  set_engine("glm") %>%
  set_mode("classification")

# Decision tree
tree_spec <- decision_tree() %>%
  set_engine("rpart") %>%
  set_mode("regression")

# Support vector machine
svm_spec <- svm_rbf() %>%
  set_engine("kernlab") %>%
  set_mode("regression")

# K-nearest neighbors
knn_spec <- nearest_neighbor(neighbors = 5) %>%
  set_engine("kknn") %>%
  set_mode("regression")

# Neural network
nnet_spec <- mlp(hidden_units = 10, epochs = 100) %>%
  set_engine("nnet") %>%
  set_mode("regression")
```

## 5.6 Key Methods for Parsnip Model Objects

Parsnip model specifications have methods for configuration, fitting,
and translation.

### 5.6.1 For model specifications (before fitting):

| Method                     | Description                 | Arguments                              | Returns             |
| :------------------------- | :-------------------------- | :------------------------------------- | :------------------ |
| `set_engine(spec, engine)` | Choose computational engine | `engine`, `...` (engine-specific args) | Updated spec        |
| `set_mode(spec, mode)`     | Set prediction mode         | `"regression"` or `"classification"`   | Updated spec        |
| `set_args(spec, ...)`      | Update model arguments      | Named arguments to update              | Updated spec        |
| `translate(spec)`          | Show underlying model call  | `engine` (optional)                    | Printed translation |
| `fit(spec, formula, data)` | Fit model to data           | `formula`, `data`, or `x`/`y`          | Fitted model        |
| `fit_xy(spec, x, y)`       | Fit with matrix interface   | `x` (predictors), `y` (outcome)        | Fitted model        |

``` r
# Inspect what the spec will do
rf_spec <- rand_forest(trees = 500, mtry = 3) %>%
  set_engine("ranger") %>%
  set_mode("regression")

translate(rf_spec)  # Shows: ranger::ranger(num.trees = 500, mtry = 3, ...)

# Update arguments
rf_spec <- rf_spec %>%
  set_args(trees = 1000)

# Fit directly (without workflow)
rf_fit <- rf_spec %>%
  fit(Sale_Price ~ ., data = train)
```

### 5.6.2 For fitted models (after fitting):

| Method                         | Description                     | Returns                            |
| :----------------------------- | :------------------------------ | :--------------------------------- |
| `predict(fit, new_data)`       | Generate predictions            | Tibble with `.pred` column         |
| `predict(fit, new_data, type)` | Predictions of specific type    | Tibble (type-dependent columns)    |
| `extract_fit_engine(fit)`      | Get underlying fitted model     | Engine-specific object             |
| `tidy(fit)`                    | Extract model coefficients/info | Tibble of parameters               |
| `glance(fit)`                  | Model-level summaries           | Tibble of fit statistics           |
| `augment(fit, new_data)`       | Add predictions to data         | Tibble with original + predictions |

``` r
# Different prediction types
predict(rf_fit, new_data = test)                    # Point predictions
predict(rf_fit, new_data = test, type = "conf_int") # Confidence intervals
predict(rf_fit, new_data = test, type = "raw")      # Engine-specific format

# For classification:
predict(logit_fit, test, type = "class")  # Predicted classes
predict(logit_fit, test, type = "prob")   # Class probabilities

# Extract underlying model for package-specific functions
ranger_obj <- extract_fit_engine(rf_fit)
ranger_obj$variable.importance  # Use ranger-specific features

# Tidy model output
tidy(lm_fit)     # Coefficients table
glance(lm_fit)   # R-squared, AIC, etc.
```

### 5.6.3 Available prediction types by mode:

**Regression:** - `type = "numeric"` (default): Predicted numeric values
- `type = "conf_int"`: Confidence/prediction intervals - `type =
"pred_int"`: Prediction intervals - `type = "raw"`: Engine-specific
format

**Classification:** - `type = "class"` (default): Predicted class labels
- `type = "prob"`: Class probabilities - `type = "conf_int"`: Confidence
intervals for probabilities - `type = "raw"`: Engine-specific format

-----

# 6 4. Creating Workflows

Workflows combine preprocessing (recipe) and model specification.

## 6.1 Basic Workflow

``` r
# Create simple recipe (without outcome transformation for prediction compatibility)
simple_recipe <- recipe(Sale_Price ~ Gr_Liv_Area + Year_Built + Lot_Area,
  data = ames_train
) %>%
  step_normalize(all_numeric_predictors())

# Create workflow
lm_workflow <- workflow() %>%
  add_recipe(simple_recipe) %>%
  add_model(lm_spec)

# View workflow
lm_workflow
```

    ## ══ Workflow ════════════════════════════════════════════════════════════════════
    ## Preprocessor: Recipe
    ## Model: linear_reg()
    ## 
    ## ── Preprocessor ────────────────────────────────────────────────────────────────
    ## 1 Recipe Step
    ## 
    ## • step_normalize()
    ## 
    ## ── Model ───────────────────────────────────────────────────────────────────────
    ## Linear Regression Model Specification (regression)
    ## 
    ## Computational engine: lm

## 6.2 Fit Workflow

``` r
# Fit the workflow
lm_fit <- lm_workflow %>%
  fit(data = ames_train)

# Extract the fitted model
lm_fit %>%
  extract_fit_parsnip() %>%
  tidy()
```

    ## # A tibble: 4 × 5
    ##   term        estimate std.error statistic   p.value
    ##   <chr>          <dbl>     <dbl>     <dbl>     <dbl>
    ## 1 (Intercept)  180467.      994.    182.   0        
    ## 2 Gr_Liv_Area   45735.     1066.     42.9  1.11e-292
    ## 3 Year_Built    33522.     1023.     32.8  3.96e-192
    ## 4 Lot_Area       7357.     1038.      7.09 1.83e- 12

``` r
# Make predictions
predictions <- lm_fit %>%
  predict(ames_test)

head(predictions)
```

    ## # A tibble: 6 × 1
    ##     .pred
    ##     <dbl>
    ## 1 115885.
    ## 2 153392.
    ## 3 222932.
    ## 4 218526.
    ## 5 178776.
    ## 6 235336.

## 6.3 Multiple Workflows

``` r
# Create workflow set with different models
workflow_set <- workflow_set(
  preproc = list(simple = simple_recipe),
  models = list(
    lm = lm_spec,
    rf = rf_spec,
    tree = tree_spec
  ),
  cross = TRUE
)

workflow_set
```

    ## # A workflow set/tibble: 3 × 4
    ##   wflow_id    info             option    result    
    ##   <chr>       <list>           <list>    <list>    
    ## 1 simple_lm   <tibble [1 × 4]> <opts[0]> <list [0]>
    ## 2 simple_rf   <tibble [1 × 4]> <opts[0]> <list [0]>
    ## 3 simple_tree <tibble [1 × 4]> <opts[0]> <list [0]>

## 6.4 Key Methods for Workflow Objects

Workflows bundle preprocessing and modeling, with methods for
construction, fitting, and extraction.

### 6.4.1 Building workflows:

| Method                                    | Description              | Arguments              | Returns          |
| :---------------------------------------- | :----------------------- | :--------------------- | :--------------- |
| `workflow()`                              | Create empty workflow    | None                   | Empty workflow   |
| `add_recipe(wf, recipe)`                  | Add preprocessing recipe | `recipe` object        | Updated workflow |
| `add_model(wf, spec)`                     | Add model specification  | `spec` (parsnip model) | Updated workflow |
| `add_formula(wf, formula)`                | Add formula (no recipe)  | R formula              | Updated workflow |
| `add_variables(wf, outcomes, predictors)` | Add variables directly   | Variable selectors     | Updated workflow |
| `remove_recipe(wf)`                       | Remove recipe            | None                   | Updated workflow |
| `remove_model(wf)`                        | Remove model             | None                   | Updated workflow |
| `update_recipe(wf, recipe)`               | Replace recipe           | New `recipe`           | Updated workflow |
| `update_model(wf, spec)`                  | Replace model            | New `spec`             | Updated workflow |

``` r
# Build workflow step by step
wf <- workflow() %>%
  add_recipe(my_recipe) %>%
  add_model(rf_spec)

# Update components
wf <- wf %>%
  update_model(xgb_spec)  # Switch to different model

# Remove and re-add
wf <- wf %>%
  remove_recipe() %>%
  add_formula(y ~ x1 + x2)  # Use formula instead
```

### 6.4.2 Fitting and using workflows:

| Method                           | Description               | Arguments                 | Returns                 |
| :------------------------------- | :------------------------ | :------------------------ | :---------------------- |
| `fit(wf, data)`                  | Fit workflow to data      | Training data             | Fitted workflow         |
| `predict(fitted_wf, new_data)`   | Generate predictions      | New data, `type`          | Tibble with predictions |
| `last_fit(wf, split)`            | Fit and evaluate on split | `initial_split` object    | Special results object  |
| `fit_resamples(wf, resamples)`   | Fit on resamples          | Cross-validation folds    | Resampling results      |
| `tune_grid(wf, resamples, grid)` | Tune hyperparameters      | Resamples, parameter grid | Tuning results          |

``` r
# Basic fitting
fitted_wf <- wf %>%
  fit(data = train)

# Predict
predictions <- fitted_wf %>%
  predict(new_data = test)

# Fit and immediately evaluate on test set
final_results <- wf %>%
  last_fit(split = train_test_split)

final_results %>% collect_metrics()  # Test set metrics
```

### 6.4.3 Extracting from fitted workflows:

| Method                            | Description                       | Returns                |
| :-------------------------------- | :-------------------------------- | :--------------------- |
| `extract_recipe(fitted_wf)`       | Get fitted recipe                 | Prepped recipe         |
| `extract_fit_parsnip(fitted_wf)`  | Get parsnip model fit             | Fitted parsnip object  |
| `extract_fit_engine(fitted_wf)`   | Get underlying model              | Engine-specific object |
| `extract_spec_parsnip(fitted_wf)` | Get model specification           | Parsnip spec           |
| `extract_preprocessor(fitted_wf)` | Get preprocessor (recipe/formula) | Recipe or formula      |
| `extract_mold(fitted_wf)`         | Get processed training data       | Mold object            |

``` r
# Extract components
fitted_recipe <- extract_recipe(fitted_wf)
fitted_model <- extract_fit_parsnip(fitted_wf)
engine_model <- extract_fit_engine(fitted_wf)

# Use extracted components
tidy(fitted_model)  # Model coefficients
bake(fitted_recipe, new_data = new_data)  # Apply preprocessing

# Access underlying model for package-specific features
engine_model$variable.importance  # If using ranger
```

### 6.4.4 Workflow sets (multiple workflows):

| Method                          | Description               | Arguments                | Returns       |
| :------------------------------ | :------------------------ | :----------------------- | :------------ |
| `workflow_set(preproc, models)` | Create multiple workflows | Lists of recipes/models  | Workflow set  |
| `workflow_map(wf_set, fn)`      | Apply function to all     | Function name, resamples | Updated set   |
| `rank_results(wf_set)`          | Rank by performance       | `rank_metric`            | Ranked tibble |
| `autoplot(wf_set)`              | Visualize results         | `metric`                 | ggplot object |

``` r
# Create and fit multiple workflows
wf_set <- workflow_set(
  preproc = list(basic = recipe1, engineered = recipe2),
  models = list(rf = rf_spec, xgb = xgb_spec)
) %>%
  workflow_map(fn = "fit_resamples", resamples = folds)

# Compare results
wf_set %>%
  rank_results(rank_metric = "rmse")

# Visualize
wf_set %>%
  autoplot(metric = "rmse")
```

-----

# 7 5. Hyperparameter Tuning

## 7.1 Define Tunable Parameters

``` r
# Create a model with tunable parameters
rf_tune_spec <- rand_forest(
  trees = 1000,
  mtry = tune(), # Number of predictors to sample
  min_n = tune() # Minimum observations in node
) %>%
  set_engine("ranger") %>%
  set_mode("regression")

# Create workflow
rf_tune_workflow <- workflow() %>%
  add_recipe(simple_recipe) %>%
  add_model(rf_tune_spec)
```

## 7.2 Grid Search

``` r
# Create regular grid
rf_grid <- grid_regular(
  mtry(range = c(1, 5)),
  min_n(range = c(2, 10)),
  levels = 5
)

# Tune with cross-validation
rf_tune_results <- rf_tune_workflow %>%
  tune_grid(
    resamples = ames_folds,
    grid = rf_grid,
    metrics = metric_set(rmse, rsq)
  )

# View results
rf_tune_results %>%
  collect_metrics() %>%
  arrange(mean)

# Select best parameters
best_rf <- rf_tune_results %>%
  select_best(metric = "rmse")

# Finalize workflow with best parameters
final_rf_workflow <- rf_tune_workflow %>%
  finalize_workflow(best_rf)

# Fit final model
final_rf_fit <- final_rf_workflow %>%
  last_fit(ames_split)

# Get test set performance
final_rf_fit %>%
  collect_metrics()
```

## 7.3 Random Search

``` r
# Create random grid
rf_random_grid <- grid_random(
  mtry(range = c(1, 10)),
  min_n(range = c(2, 20)),
  size = 20 # Number of combinations
)

# Tune with random search
rf_random_results <- rf_tune_workflow %>%
  tune_grid(
    resamples = ames_folds,
    grid = rf_random_grid
  )
```

## 7.4 Space-Filling Designs (Irregular Grids)

For more efficient parameter space exploration, use **space-filling
designs** like Latin hypercube:

``` r
# Latin hypercube sampling - better coverage of parameter space
latin_grid <- grid_latin_hypercube(
  penalty(range = c(-5, 0)),
  mixture(range = c(0, 1)),
  size = 20 # Number of parameter combinations
)

# Advantages over regular grid:
# - Better coverage with fewer combinations
# - Avoids clustering of points
# - More efficient for expensive models
# - Recommended for irregular/non-linear parameter relationships

# Example: Compare grid sizes
regular_grid <- grid_regular(penalty(), mixture(), levels = 5) # 5x5 = 25 points
latin_grid <- grid_latin_hypercube(penalty(), mixture(), size = 20) # 20 points, better coverage
```

## 7.5 Bayesian Optimization

``` r
library(finetune)

# Bayesian optimization
rf_bayes_results <- rf_tune_workflow %>%
  tune_bayes(
    resamples = ames_folds,
    initial = 5, # Initial random parameter sets
    iter = 20, # Additional iterations
    metrics = metric_set(rmse)
  )

# View best results
rf_bayes_results %>%
  show_best(metric = "rmse")
```

## 7.6 Key Methods for Tuning Results

After tuning, these methods help you explore results, select best
parameters, and finalize models.

### 7.6.1 Exploring tuning results:

| Method                         | Description                       | Arguments           | Returns               |
| :----------------------------- | :-------------------------------- | :------------------ | :-------------------- |
| `collect_metrics(results)`     | Get all metrics across parameters | `summarize = TRUE`  | Tibble of metrics     |
| `show_best(results, metric)`   | Show top parameter sets           | `metric`, `n`       | Tibble (best n sets)  |
| `autoplot(results)`            | Visualize tuning results          | `metric`            | ggplot object         |
| `collect_predictions(results)` | Get predictions from resamples    | `summarize = FALSE` | Tibble of predictions |
| `conf_mat_resampled(results)`  | Confusion matrix (classification) | None                | Summary object        |

``` r
# Get all metrics
all_metrics <- tune_results %>%
  collect_metrics()

# See best 5 parameter combinations
tune_results %>%
  show_best(metric = "rmse", n = 5)

# Visualize performance
tune_results %>%
  autoplot(metric = "rmse")

# Get all predictions
all_preds <- tune_results %>%
  collect_predictions(summarize = FALSE)
```

### 7.6.2 Selecting best parameters:

| Method                           | Description             | Arguments         | Returns        |
| :------------------------------- | :---------------------- | :---------------- | :------------- |
| `select_best(results, metric)`   | Choose best by metric   | `metric`          | Tibble (1 row) |
| `select_by_pct_loss(results)`    | Select within % of best | `metric`, `limit` | Tibble (1 row) |
| `select_by_one_std_err(results)` | One SE rule selection   | `metric`          | Tibble (1 row) |

``` r
# Select absolute best
best_params <- tune_results %>%
  select_best(metric = "rmse")

# Select simpler model within 2% of best performance
simple_params <- tune_results %>%
  select_by_pct_loss(metric = "rmse", limit = 2)

# One standard error rule (simpler model)
simple_params <- tune_results %>%
  select_by_one_std_err(metric = "rmse", desc(trees))  # Prefer fewer trees
```

### 7.6.3 Finalizing workflows:

| Method                            | Description                      | Arguments                  | Returns          |
| :-------------------------------- | :------------------------------- | :------------------------- | :--------------- |
| `finalize_workflow(wf, params)`   | Update workflow with best params | Workflow, parameter tibble | Updated workflow |
| `finalize_model(spec, params)`    | Update model spec with params    | Model spec, parameters     | Updated spec     |
| `finalize_recipe(recipe, params)` | Update recipe with params        | Recipe, parameters         | Updated recipe   |

``` r
# Get best parameters
best <- tune_results %>%
  select_best("rmse")

# Finalize workflow
final_wf <- tune_workflow %>%
  finalize_workflow(best)

# Fit on all training data
final_fit <- final_wf %>%
  fit(data = train)

# Or use last_fit for automatic train/test evaluation
final_results <- tune_workflow %>%
  finalize_workflow(best) %>%
  last_fit(split = train_test_split)

final_results %>% collect_metrics()  # Test set performance
```

### 7.6.4 Special methods for `last_fit()` results:

| Method                          | Description          | Returns                 |
| :------------------------------ | :------------------- | :---------------------- |
| `collect_metrics(last_fit)`     | Test set metrics     | Tibble of metrics       |
| `collect_predictions(last_fit)` | Test set predictions | Tibble with predictions |
| `extract_workflow(last_fit)`    | Get fitted workflow  | Fitted workflow         |

``` r
# Evaluate on test set
test_metrics <- final_results %>%
  collect_metrics()

# Get test predictions
test_preds <- final_results %>%
  collect_predictions()

# Extract for deployment
deployment_wf <- final_results %>%
  extract_workflow()

# Save for later
saveRDS(deployment_wf, "final_model.rds")
```

-----

# 8 6. Model Evaluation with yardstick

## 8.1 Regression Metrics

``` r
# Get predictions with actual values
results <- lm_fit %>%
  predict(ames_test) %>%
  bind_cols(ames_test %>% select(Sale_Price))

# Calculate metrics
metrics_regression <- metric_set(rmse, rsq, mae, mape)

results %>%
  metrics_regression(truth = Sale_Price, estimate = .pred)

# Individual metrics
results %>%
  rmse(truth = Sale_Price, estimate = .pred)

results %>%
  rsq(truth = Sale_Price, estimate = .pred)
```

## 8.2 Classification Metrics

``` r
# For binary classification
# Assume we have predictions and true classes
classification_results <- tibble(
  truth = factor(c("Yes", "No", "Yes", "Yes", "No")),
  estimate = factor(c("Yes", "No", "No", "Yes", "No")),
  .pred_Yes = c(0.9, 0.3, 0.4, 0.8, 0.2)
)

# Confusion matrix
classification_results %>%
  conf_mat(truth = truth, estimate = estimate)

# Multiple metrics
metrics_classification <- metric_set(accuracy, sensitivity, specificity, f_meas)

classification_results %>%
  metrics_classification(truth = truth, estimate = estimate)

# ROC curve
classification_results %>%
  roc_curve(truth = truth, .pred_Yes) %>%
  autoplot()

# AUC
classification_results %>%
  roc_auc(truth = truth, .pred_Yes)
```

## 8.3 Key Methods for yardstick Metrics

Yardstick provides consistent functions for calculating model
performance metrics.

### 8.3.1 Using individual metrics:

All metric functions follow the same pattern:

``` r
metric_function(data, truth, estimate, ...)
```

**Common regression metrics:**

| Function       | Metric                            | Range                                                                                                         | Better     |
| :------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------ | :--------- |
| `rmse()`       | Root Mean Squared Error           | ![0, ∞](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20%E2%88%9E "0, ∞") | Lower      |
| `mae()`        | Mean Absolute Error               | ![0, ∞](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20%E2%88%9E "0, ∞") | Lower      |
| `rsq()`        | R-squared                         | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")         | Higher     |
| `mape()`       | Mean Absolute % Error             | ![0, ∞](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20%E2%88%9E "0, ∞") | Lower      |
| `smape()`      | Symmetric MAPE                    | ![0, 200](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20200 "0, 200")   | Lower      |
| `msd()`        | Mean Signed Deviation             | (-∞, ∞)                                                                                                       | Close to 0 |
| `ccc()`        | Concordance Correlation           | ![-1, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;-1%2C%201 "-1, 1")      | Higher     |
| `rpd()`        | Ratio of Performance to Deviation | ![0, ∞](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20%E2%88%9E "0, ∞") | Higher     |
| `rpiq()`       | Ratio of Performance to IQR       | ![0, ∞](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20%E2%88%9E "0, ∞") | Higher     |
| `huber_loss()` | Huber Loss (robust)               | ![0, ∞](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%20%E2%88%9E "0, ∞") | Lower      |

**Common classification metrics:**

| Function                   | Metric                    | Range                                                                                                    | Better |
| :------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------------- | :----- |
| `accuracy()`               | Overall accuracy          | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `bal_accuracy()`           | Balanced accuracy         | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `sens()` / `sensitivity()` | True positive rate        | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `spec()` / `specificity()` | True negative rate        | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `precision()` / `ppv()`    | Positive predictive value | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `recall()`                 | Same as sensitivity       | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `f_meas()`                 | F1-score                  | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `kap()`                    | Cohen’s Kappa             | ![-1, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;-1%2C%201 "-1, 1") | Higher |
| `mcc()`                    | Matthews Correlation      | ![-1, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;-1%2C%201 "-1, 1") | Higher |
| `roc_auc()`                | Area under ROC curve      | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |
| `pr_auc()`                 | Area under PR curve       | ![0, 1](https://latex.codecogs.com/png.image?%5Cdpi%7B110%7D&space;%5Cbg_white&space;0%2C%201 "0, 1")    | Higher |

``` r
# Single metric
results %>%
  rmse(truth = actual, estimate = predicted)

# With grouped data
results %>%
  group_by(model_type) %>%
  rmse(truth = actual, estimate = predicted)
```

### 8.3.2 Creating metric sets:

| Function                         | Description              | Arguments                | Returns             |
| :------------------------------- | :----------------------- | :----------------------- | :------------------ |
| `metric_set(...)`                | Combine multiple metrics | Metric functions         | Metric set function |
| `metrics(data, truth, estimate)` | Default metrics          | Data with truth/estimate | Tibble of metrics   |

``` r
# Create custom metric set
my_metrics <- metric_set(rmse, rsq, mae, mape)

# Apply all at once
results %>%
  my_metrics(truth = actual, estimate = predicted)

# Default metrics (quick evaluation)
results %>%
  metrics(truth = actual, estimate = predicted)
```

### 8.3.3 Confusion matrix methods:

| Method                            | Description                | Returns           |
| :-------------------------------- | :------------------------- | :---------------- |
| `conf_mat(data, truth, estimate)` | Create confusion matrix    | conf\_mat object  |
| `summary(conf_mat)`               | All classification metrics | Tibble of metrics |
| `autoplot(conf_mat)`              | Visualize confusion matrix | ggplot object     |
| `tidy(conf_mat)`                  | Convert to tibble          | Tibble            |

``` r
# Create confusion matrix
cm <- classification_results %>%
  conf_mat(truth = truth, estimate = estimate)

# Get all metrics at once
summary(cm)

# Visualize
autoplot(cm, type = "heatmap")
autoplot(cm, type = "mosaic")

# Extract as data
tidy(cm)
```

### 8.3.4 ROC and PR curves:

| Function                       | Description                | Returns                           |
| :----------------------------- | :------------------------- | :-------------------------------- |
| `roc_curve(data, truth, ...)`  | Calculate ROC curve points | Tibble of sensitivity/specificity |
| `pr_curve(data, truth, ...)`   | Calculate PR curve points  | Tibble of precision/recall        |
| `gain_curve(data, truth, ...)` | Cumulative gain curve      | Tibble                            |
| `lift_curve(data, truth, ...)` | Lift curve                 | Tibble                            |
| `autoplot(curve)`              | Visualize curve            | ggplot object                     |

``` r
# ROC curve
roc_data <- classification_results %>%
  roc_curve(truth = truth, .pred_Yes)

autoplot(roc_data)

# PR curve
pr_data <- classification_results %>%
  pr_curve(truth = truth, .pred_Yes)

autoplot(pr_data)

# Compare multiple models
bind_rows(
  roc_curve(results1, truth, .pred_Yes) %>% mutate(model = "Model 1"),
  roc_curve(results2, truth, .pred_Yes) %>% mutate(model = "Model 2")
) %>%
  ggplot(aes(x = 1 - specificity, y = sensitivity, color = model)) +
  geom_path() +
  geom_abline(linetype = "dashed")
```

### 8.3.5 Grouped and multi-class metrics:

``` r
# Metrics by group
results %>%
  group_by(model_type) %>%
  rmse(truth = actual, estimate = predicted)

# Multi-class classification (macro/micro averaging)
multiclass_results %>%
  accuracy(truth = class, estimate = predicted_class)

multiclass_results %>%
  roc_auc(
    truth = class,
    .pred_A, .pred_B, .pred_C,  # Probability columns
    estimator = "macro"  # or "micro", "macro_weighted"
  )
```

-----

# 9 7. Complete Example: End-to-End Workflow

``` r
# Load data
data(ames)
set.seed(123)

# 1. Split data
ames_split <- initial_split(ames, prop = 0.75, strata = Sale_Price)
ames_train <- training(ames_split)
ames_test <- testing(ames_split)

# Create cross-validation folds
ames_folds <- vfold_cv(ames_train, v = 5, strata = Sale_Price)

# 2. Create recipe
ames_recipe <- recipe(
  Sale_Price ~ Lot_Area + Neighborhood + Gr_Liv_Area +
    Year_Built + Bldg_Type + Overall_Qual,
  data = ames_train
) %>%
  step_log(Sale_Price, Gr_Liv_Area, Lot_Area) %>%
  step_other(Neighborhood, threshold = 0.05) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_normalize(all_numeric_predictors())

# 3. Specify models with tuning
xgb_spec <- boost_tree(
  trees = 1000,
  tree_depth = tune(),
  learn_rate = tune(),
  mtry = tune()
) %>%
  set_engine("xgboost") %>%
  set_mode("regression")

# 4. Create workflow
xgb_workflow <- workflow() %>%
  add_recipe(ames_recipe) %>%
  add_model(xgb_spec)

# 5. Define tuning grid
xgb_grid <- grid_latin_hypercube(
  tree_depth(range = c(3, 10)),
  learn_rate(range = c(-3, -0.5)),
  finalize(mtry(), ames_train %>% select(-Sale_Price)),
  size = 20
)

# 6. Tune model
xgb_tune <- xgb_workflow %>%
  tune_grid(
    resamples = ames_folds,
    grid = xgb_grid,
    control = control_grid(save_pred = TRUE),
    metrics = metric_set(rmse, rsq, mae)
  )

# 7. Evaluate tuning results
xgb_tune %>%
  collect_metrics() %>%
  filter(.metric == "rmse") %>%
  arrange(mean)

# Visualize tuning results
xgb_tune %>%
  collect_metrics() %>%
  filter(.metric == "rmse") %>%
  ggplot(aes(x = learn_rate, y = mean, color = factor(tree_depth))) +
  geom_point() +
  geom_line() +
  scale_x_log10() +
  labs(
    title = "Tuning Results: RMSE by Learning Rate and Tree Depth",
    y = "Mean RMSE",
    color = "Tree Depth"
  )

# 8. Select best model
best_xgb <- xgb_tune %>%
  select_best(metric = "rmse")

# 9. Finalize workflow
final_xgb <- xgb_workflow %>%
  finalize_workflow(best_xgb)

# 10. Fit on all training data and evaluate on test set
final_fit <- final_xgb %>%
  last_fit(ames_split)

# 11. Get test set performance
final_fit %>%
  collect_metrics()

# 12. Get predictions
test_predictions <- final_fit %>%
  collect_predictions()

test_predictions %>%
  ggplot(aes(x = Sale_Price, y = .pred)) +
  geom_point(alpha = 0.5) +
  geom_abline(color = "red", linetype = "dashed") +
  labs(
    title = "Predicted vs Actual Sale Price",
    x = "Actual (log10)",
    y = "Predicted (log10)"
  )

# 13. Fit final model on all data for deployment
final_model <- final_xgb %>%
  fit(ames)

# Save model for later use
# saveRDS(final_model, "ames_price_model.rds")
```

-----

# 10 8. Advanced Topics

## 10.1 Custom Metrics

``` r
# Create custom metric
mean_absolute_percentage_error <- function(data, truth, estimate, ...) {
  mape_impl <- function(truth, estimate) {
    mean(abs((truth - estimate) / truth)) * 100
  }

  metric_summarizer(
    metric_nm = "mape",
    metric_fn = mape_impl,
    data = data,
    truth = !!rlang::enquo(truth),
    estimate = !!rlang::enquo(estimate),
    ...
  )
}

# Use custom metric
custom_metrics <- metric_set(rmse, rsq, mean_absolute_percentage_error)
```

## 10.2 Model Stacking

``` r
library(stacks)

# Create multiple tuned models
# ... (tune several models as shown above)

# Initialize stack
model_stack <- stacks() %>%
  add_candidates(rf_tune_results) %>%
  add_candidates(xgb_tune) %>%
  add_candidates(lm_tune_results)

# Blend predictions
blended_stack <- model_stack %>%
  blend_predictions()

# Fit stack members
fitted_stack <- blended_stack %>%
  fit_members()

# Predict with stack
stack_pred <- fitted_stack %>%
  predict(ames_test)
```

## 10.3 Feature Importance

``` r
library(vip)

# For models with built-in importance
lm_fit %>%
  extract_fit_parsnip() %>%
  vip()

# Model-agnostic importance with DALEX
library(DALEXtra)

explainer <- explain_tidymodels(
  final_model,
  data = ames_train %>% select(-Sale_Price),
  y = ames_train$Sale_Price,
  label = "XGBoost"
)

# Variable importance
vi <- model_parts(explainer)
plot(vi)

# Partial dependence plots
pdp <- model_profile(explainer, variables = "Gr_Liv_Area")
plot(pdp)
```

## 10.4 Parallel Processing

``` r
library(doParallel)

# Setup parallel backend
cl <- makePSOCKcluster(parallel::detectCores() - 1)
registerDoParallel(cl)

# Tuning will now use parallel processing
tune_results <- workflow %>%
  tune_grid(
    resamples = folds,
    grid = tuning_grid,
    control = control_grid(parallel_over = "resamples")
  )

# Stop cluster when done
stopCluster(cl)
```

## 10.5 Comparing Modeling Frameworks: tidymodels vs caret vs Base R

Understanding the differences between R’s modeling frameworks helps you
choose the right tool for your needs.

### 10.5.1 Overview Comparison

| Feature                 | tidymodels                 | caret                   | Base R                     |
| :---------------------- | :------------------------- | :---------------------- | :------------------------- |
| **Philosophy**          | Modular, tidyverse-aligned | All-in-one wrapper      | Direct model access        |
| **Learning Curve**      | Moderate                   | Moderate                | Varies by package          |
| **Code Style**          | Pipe-friendly (`%>%`)      | Function-based          | Function-based             |
| **Consistency**         | High (unified interface)   | High (unified wrapper)  | Low (package-specific)     |
| **Preprocessing**       | recipes package            | preProcess, formula     | Manual or package-specific |
| **Model Specification** | parsnip (declarative)      | train() method argument | Package-specific functions |
| **Active Development**  | Very active                | Maintenance mode\*      | Package-specific           |
| **Extensibility**       | Highly modular             | Limited                 | Unlimited                  |

\*Note: caret is in maintenance mode as Max Kuhn (creator) moved to
tidymodels

### 10.5.2 Detailed Comparison with Examples

#### 10.5.2.1 1. Data Splitting

``` r
# tidymodels
library(tidymodels)
set.seed(123)
split <- initial_split(mtcars, prop = 0.75, strata = mpg)
train_data <- training(split)
test_data <- testing(split)
cv_folds <- vfold_cv(train_data, v = 10)

# caret
library(caret)
set.seed(123)
train_index <- createDataPartition(mtcars$mpg, p = 0.75, list = FALSE)
train_data <- mtcars[train_index, ]
test_data <- mtcars[-train_index, ]
cv_folds <- createFolds(train_data$mpg, k = 10)

# Base R
set.seed(123)
train_index <- sample(1:nrow(mtcars), size = 0.75 * nrow(mtcars))
train_data <- mtcars[train_index, ]
test_data <- mtcars[-train_index, ]
# CV folds require manual implementation
```

#### 10.5.2.2 2. Preprocessing and Feature Engineering

``` r
# tidymodels - recipes
recipe_tm <- recipe(mpg ~ ., data = train_data) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_zv(all_predictors()) %>%
  step_corr(all_numeric_predictors(), threshold = 0.9)

# Apply to new data
prepped_recipe <- prep(recipe_tm, training = train_data)
train_processed <- bake(prepped_recipe, new_data = train_data)
test_processed <- bake(prepped_recipe, new_data = test_data)

# caret - preProcess
preproc_caret <- preProcess(
  train_data[, -1], # Exclude outcome
  method = c("center", "scale", "zv", "corr")
)
train_processed <- predict(preproc_caret, train_data)
test_processed <- predict(preproc_caret, test_data)

# Base R - manual
train_means <- colMeans(train_data[, sapply(train_data, is.numeric)])
train_sds <- apply(train_data[, sapply(train_data, is.numeric)], 2, sd)
train_processed <- scale(train_data[, -1], center = train_means[-1], scale = train_sds[-1])
test_processed <- scale(test_data[, -1], center = train_means[-1], scale = train_sds[-1])
# Dummy coding, correlation removal, etc. require manual implementation
```

#### 10.5.2.3 3. Model Training

``` r
# tidymodels - workflow approach
rf_spec <- rand_forest(trees = 500, mtry = 3) %>%
  set_engine("ranger") %>%
  set_mode("regression")

wf <- workflow() %>%
  add_recipe(recipe_tm) %>%
  add_model(rf_spec)

fitted_model <- wf %>%
  fit(data = train_data)

# caret - unified interface
fitted_model_caret <- train(
  mpg ~ .,
  data = train_data,
  method = "ranger",
  preProcess = c("center", "scale"),
  trControl = trainControl(method = "cv", number = 10),
  tuneGrid = expand.grid(
    mtry = 3,
    splitrule = "variance",
    min.node.size = 5
  ),
  num.trees = 500
)

# Base R - direct package calls
library(ranger)
fitted_model_base <- ranger(
  mpg ~ .,
  data = train_processed, # Must preprocess first
  num.trees = 500,
  mtry = 3
)
```

#### 10.5.2.4 4. Hyperparameter Tuning

``` r
# tidymodels - declarative tuning
rf_tune_spec <- rand_forest(
  trees = 500,
  mtry = tune(),
  min_n = tune()
) %>%
  set_engine("ranger") %>%
  set_mode("regression")

wf_tune <- workflow() %>%
  add_recipe(recipe_tm) %>%
  add_model(rf_tune_spec)

tune_results <- wf_tune %>%
  tune_grid(
    resamples = cv_folds,
    grid = 20,
    metrics = metric_set(rmse, rsq)
  )

best_params <- select_best(tune_results, "rmse")

# caret - grid search built-in
tune_grid_caret <- expand.grid(
  mtry = c(2, 3, 4, 5),
  splitrule = "variance",
  min.node.size = c(5, 10, 15)
)

tuned_model_caret <- train(
  mpg ~ .,
  data = train_data,
  method = "ranger",
  trControl = trainControl(method = "cv", number = 10),
  tuneGrid = tune_grid_caret,
  num.trees = 500
)

# Base R - manual grid search
param_grid <- expand.grid(
  mtry = c(2, 3, 4, 5),
  min.node.size = c(5, 10, 15)
)

cv_results <- data.frame()
for (i in 1:nrow(param_grid)) {
  # Implement CV loop manually
  fold_rmse <- numeric(10)
  for (fold in 1:10) {
    # Split data into train/validation
    # Train model with params
    # Calculate RMSE
  }
  # Store results
}
# Select best parameters
```

#### 10.5.2.5 5. Predictions and Evaluation

``` r
# tidymodels
predictions_tm <- fitted_model %>%
  predict(test_data) %>%
  bind_cols(test_data)

metrics_tm <- predictions_tm %>%
  metrics(truth = mpg, estimate = .pred)

# caret
predictions_caret <- predict(fitted_model_caret, newdata = test_data)
metrics_caret <- postResample(pred = predictions_caret, obs = test_data$mpg)

# Base R
predictions_base <- predict(fitted_model_base, data = test_data)$predictions
rmse_base <- sqrt(mean((test_data$mpg - predictions_base)^2))
rsq_base <- cor(test_data$mpg, predictions_base)^2
```

### 10.5.3 Pros and Cons

#### 10.5.3.1 tidymodels

**Pros:** - **Modern design**: Built with tidyverse principles,
pipe-friendly - **Modularity**: Each package has a focused purpose, easy
to extend - **Reproducibility**: Recipes ensure consistent preprocessing
across train/test - **Active development**: New features, models, and
improvements regularly added - **Better documentation**: Comprehensive
website and “Tidy Modeling with R” book - **Type safety**: Strong typing
and error checking prevent common mistakes - **Workflow objects**:
Preprocessing + model bundled together, easier deployment - **Advanced
features**: Model stacking, Bayesian optimization, workflow sets -
**Consistent interface**: Same syntax across 100+ models

**Cons:** - **Newer ecosystem**: Less mature than caret, some rough
edges - **Steeper learning curve initially**: Need to understand
multiple packages - **More verbose**: Requires more code than caret for
simple tasks - **Performance overhead**: Recipes re-apply preprocessing
in each resample (correctness over speed) - **Training speed**: Can be
significantly slower than caret for tuning (48× in one benchmark) -
**Breaking changes**: API still evolving (though stabilizing)

**Best for:** - Production pipelines requiring reproducibility - Complex
preprocessing workflows - Projects using tidyverse extensively - Teams
wanting consistent, maintainable code - Advanced modeling techniques
(ensembles, stacking)

**Important preprocessing philosophy**: Tidymodels prioritizes
**correctness over speed**. Recipes ensure preprocessing statistics are
computed only on training folds and applied to validation folds within
each resample, preventing data leakage. This is more rigorous but slower
than caret’s approach.

#### 10.5.3.2 caret

**Pros:** - **Mature and stable**: 15+ years of development, well-tested
- **Comprehensive**: 238+ models with unified interface - **Simple
syntax**: Less verbose for basic tasks - **Extensive documentation**:
Many tutorials and examples available - **Feature engineering**:
Built-in functions for preprocessing - **Variable importance**:
Standardized across models - **Large community**: Lots of Stack Overflow
answers and blog posts

**Cons:** - **Maintenance mode**: No major new features (creator moved
to tidymodels) - **Less flexible preprocessing**: preProcess limited
compared to recipes - **Harder to extend**: Adding new models or methods
requires package updates - **Not tidyverse-native**: Doesn’t integrate
well with dplyr, ggplot2, etc. - **Formula interface limitations**: Can
be clunky for complex feature engineering - **Inconsistent behavior**:
Some models have unique quirks despite wrapper - **Memory intensive**:
Can be slow with large datasets

**Best for:** - Quick prototyping and experimentation - Legacy projects
already using caret - Users familiar with traditional R syntax - Simple
modeling tasks without complex preprocessing - When you need one of
caret’s specialized features

#### 10.5.3.3 Base R

**Pros:** - **Full control**: Direct access to all model parameters and
internals - **No dependencies**: Lightweight, no extra packages needed
(for base models) - **Performance**: No abstraction overhead, can be
fastest option - **Flexibility**: Can implement any custom logic -
**Stability**: Core functions rarely change - **Learning**:
Understanding base functions teaches fundamentals

**Cons:** - **Inconsistent APIs**: Each package has different syntax and
conventions - **Manual work**: Must implement train/test splits, CV,
preprocessing manually - **Error-prone**: Easy to make data leakage
mistakes - **More code**: Requires significantly more lines for complete
workflows - **Limited scalability**: Hard to maintain as projects grow -
**Harder to reproduce**: More manual steps mean more places for errors

**Best for:** - Learning fundamentals of machine learning - Custom
algorithms or research - Simple models without preprocessing -
Performance-critical applications - When you need package-specific
features not exposed by wrappers

### 10.5.4 Migration Guide

#### 10.5.4.1 From caret to tidymodels

``` r
# caret code
library(caret)
model <- train(
  mpg ~ .,
  data = train_data,
  method = "rf",
  preProcess = c("center", "scale"),
  trControl = trainControl(method = "cv", number = 10)
)

# Equivalent tidymodels code
library(tidymodels)

# Split data
split <- initial_split(mtcars, prop = 0.75)
train_data <- training(split)

# Create recipe (preprocessing)
rec <- recipe(mpg ~ ., data = train_data) %>%
  step_normalize(all_numeric_predictors())

# Create model spec
rf_spec <- rand_forest() %>%
  set_engine("ranger") %>%
  set_mode("regression")

# Create workflow
wf <- workflow() %>%
  add_recipe(rec) %>%
  add_model(rf_spec)

# Fit with cross-validation
cv_folds <- vfold_cv(train_data, v = 10)
cv_results <- wf %>%
  fit_resamples(resamples = cv_folds)

# Final fit
final_fit <- wf %>%
  fit(train_data)
```

#### 10.5.4.2 From Base R to tidymodels

``` r
# Base R code
library(randomForest)
train_idx <- sample(1:nrow(mtcars), 0.75 * nrow(mtcars))
train <- mtcars[train_idx, ]
test <- mtcars[-train_idx, ]
train_scaled <- scale(train[, -1])
model <- randomForest(mpg ~ ., data = as.data.frame(train_scaled))
predictions <- predict(model, newdata = scale(test[, -1]))

# tidymodels equivalent
library(tidymodels)
split <- initial_split(mtcars, prop = 0.75)
rec <- recipe(mpg ~ ., data = training(split)) %>%
  step_normalize(all_numeric_predictors())
rf_spec <- rand_forest() %>%
  set_engine("randomForest") %>%
  set_mode("regression")
wf <- workflow() %>%
  add_recipe(rec) %>%
  add_model(rf_spec)
fit <- wf %>% fit(training(split))
predictions <- fit %>% predict(testing(split))
```

### 10.5.5 Recommendation

**Choose tidymodels if:** - Starting a new project in 2024+ - Need
reproducible, production-ready pipelines - Working with complex
preprocessing - Want modern R programming practices - Plan to use
advanced techniques (stacking, tuning)

**Choose caret if:** - Maintaining existing caret code - Need quick
prototyping with minimal setup - Have simple preprocessing needs - Want
maximum model variety with minimal code

**Choose Base R if:** - Learning ML fundamentals - Building custom
algorithms - Need maximum performance and control - Have very simple
modeling needs - Working with specialized packages not wrapped by
tidymodels/caret

**General guideline**: For new projects, **tidymodels** is the
recommended choice as it’s the future of modeling in R and provides the
best balance of power, flexibility, and maintainability.

### 10.5.6 Real-World Performance Comparison

A detailed comparison using the IBM HR Analytics dataset (employee churn
prediction) revealed important practical differences:

#### 10.5.6.1 Training Speed

**Critical Finding**: In a real-world benchmark, **caret was 48×
faster** than tidymodels for hyperparameter tuning: - tidymodels: 6+
hours for workflow\_map() with 3,240 iterations - caret: \< 8 minutes
for the same task

**Why the difference?** - Recipes in tidymodels re-apply all
preprocessing steps within each resample - This ensures perfect
reproducibility but adds computational overhead - Caret caches
preprocessing results more efficiently

**Mitigation strategies for tidymodels:** 1. Use smaller tuning grids
initially 2. Leverage parallel processing with `doParallel` 3. Consider
simpler recipes when speed is critical 4. Use `workflow_map()` with
`control = control_grid(save_pred = FALSE)`

#### 10.5.6.2 Model Performance

Surprisingly, in the benchmark study: - **caret achieved higher
F1-scores** on the test set - This was attributed to caret’s targeted
optimization (explicitly optimizing for F1) - tidymodels used default
metrics which may not have prioritized F1

**Key lesson**: Always specify your optimization metric explicitly in
tidymodels:

``` r
tune_grid(
  resamples = folds,
  grid = tuning_grid,
  metrics = metric_set(f_meas, roc_auc, accuracy)  # Specify your priority metric
)
```

#### 10.5.6.3 Workflow Differences

**tidymodels approach:**

``` r
# Create workflow set for multiple models
workflow_set <- workflow_set(
  preproc = list(recipe1, recipe2),
  models = list(glmnet = glmnet_spec, xgb = xgb_spec),
  cross = TRUE
)

# Tune all at once
results <- workflow_set %>%
  workflow_map(fn = "tune_grid", resamples = folds)
```

**caret approach:**

``` r
# Must create custom function to compare models
train_model <- function(method) {
  train(outcome ~ ., data = train_data, method = method,
        trControl = trainControl(...))
}

models <- lapply(c("glmnet", "xgbTree"), train_model)
```

#### 10.5.6.4 Cross-Package Compatibility

For fair comparisons between frameworks:

``` r
# Convert resamples between packages
caret_folds <- rsample2caret(tidymodels_folds)
tidymodels_folds <- caret2rsample(caret_folds)
```

### 10.5.7 When Speed vs Features Matters

**Choose caret when:** - Time-constrained exploratory analysis - Need to
quickly prototype many models - Working with standard preprocessing
workflows - CPU resources are limited

**Choose tidymodels when:** - Building production pipelines
(reproducibility \> speed) - Complex, custom preprocessing required -
Need explicit workflow documentation - Long-term maintainability matters
more than initial speed - Working in tidyverse-heavy projects

### 10.5.8 Summary Table: Practical Considerations

| Consideration          | tidymodels                          | caret                         |
| :--------------------- | :---------------------------------- | :---------------------------- |
| **Initial setup time** | Longer (more code)                  | Faster (compact syntax)       |
| **Tuning speed**       | Slower (recipe overhead)            | Faster (cached preprocessing) |
| **Reproducibility**    | Excellent (explicit recipes)        | Good (but less transparent)   |
| **Debugging**          | Easier (step-by-step)               | Harder (black box)            |
| **Memory usage**       | Higher                              | Lower                         |
| **Parallelization**    | Built-in support                    | Built-in support              |
| **Custom metrics**     | Easy to define                      | More complex                  |
| **Deployment**         | Workflow objects are self-contained | Requires manual tracking      |

-----

# 11 9. Using btw to Learn More

The `btw` package is excellent for learning tidymodels functions
interactively.

## 11.1 Learn About Specific Functions

``` r
library(btw)

# Learn about recipes
btw(recipe, ames_train)

# Learn about specific preprocessing steps
btw(step_normalize, step_dummy, step_impute_median)

# Learn about model specification
btw(rand_forest, ames_train, "Show me examples of random forest regression")

# Learn about tuning
btw(tune_grid, ames_folds, "How do I tune hyperparameters?")

# Compare related functions
btw(
  initial_split, vfold_cv, bootstraps,
  "What's the difference between these resampling methods?"
)

# Learn about metrics
btw(rmse, rsq, mae, "Explain these regression metrics")

# Workflow creation
btw(workflow, "Show me how to create and use workflows")
```

## 11.2 Get Package Overview

``` r
# Overview of recipes package
btw(btw_tool_docs_package_help_topics("recipes"))

# Overview of parsnip
btw(btw_tool_docs_package_help_topics("parsnip"))

# Get vignettes
btw(vignette("workflows"))
btw(vignette("tuning", "tune"))
```

## 11.3 Interactive Learning with AI

``` r
library(ellmer)

# Create chat session
chat <- chat_anthropic() # or chat_ollama()

# Ask questions with context
chat$chat(
  btw(
    tune_grid,
    ames_folds,
    "I'm getting an error when tuning. How do I fix it?"
  )
)

# Get examples
chat$chat(
  btw(
    recipe,
    ames_train,
    "Show me 3 different ways to handle missing data in recipes"
  )
)
```

-----

# 12 10. Best Practices

## 12.1 Data Leakage Prevention

``` r
# WRONG: Computing statistics on full data
# mean_price <- mean(ames$Sale_Price)
# ames_normalized <- ames %>% mutate(Sale_Price = Sale_Price / mean_price)

# RIGHT: Let recipe handle preprocessing
# Statistics are computed only on training data
# and applied to test data
correct_recipe <- recipe(Sale_Price ~ ., data = ames_train) %>%
  step_normalize(all_numeric_predictors()) # Uses training means/SDs only
```

## 12.2 Workflow Organization

``` r
# Good practice: Organize your modeling project

# 1. Data preparation script
# data_prep.R

# 2. Feature engineering and recipe
# recipe_definitions.R

# 3. Model specifications
# model_specs.R

# 4. Training script
# train_models.R

# 5. Evaluation script
# evaluate_models.R

# 6. Deployment script
# deploy_model.R
```

## 12.3 Model Comparison

``` r
# Compare multiple models systematically
library(workflowsets)

# Define recipes
recipe_basic <- recipe(Sale_Price ~ ., data = ames_train) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors())

recipe_engineered <- recipe(Sale_Price ~ ., data = ames_train) %>%
  step_log(Sale_Price) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_interact(~ Gr_Liv_Area:Year_Built)

# Define models
models <- list(
  lm = linear_reg() %>% set_engine("lm"),
  rf = rand_forest() %>% set_engine("ranger") %>% set_mode("regression"),
  xgb = boost_tree() %>% set_engine("xgboost") %>% set_mode("regression")
)

# Create all combinations
all_workflows <- workflow_set(
  preproc = list(basic = recipe_basic, engineered = recipe_engineered),
  models = models,
  cross = TRUE
)

# Fit all workflows
all_results <- all_workflows %>%
  workflow_map(
    fn = "fit_resamples",
    resamples = ames_folds,
    metrics = metric_set(rmse, rsq)
  )

# Compare results
all_results %>%
  rank_results(rank_metric = "rmse") %>%
  filter(.metric == "rmse")

# Visualize
all_results %>%
  autoplot()
```

-----

# 13 Resources

## 13.1 Documentation

  - [tidymodels.org](https://www.tidymodels.org/) - Official
    documentation
  - [Tidy Modeling with R](https://www.tmwr.org/) - Free online book
  - [recipes
    reference](https://recipes.tidymodels.org/reference/index.html)
  - [parsnip models](https://www.tidymodels.org/find/parsnip/)

## 13.2 Learning with btw

``` r
# Get started with btw
btw::btw() # Describe current workspace

# Learn any tidymodels function
btw::btw(your_function_here, your_data, "your question")

# Use with AI chat
library(ellmer)
chat <- chat_anthropic()
chat$chat(btw(function_name, data, "question"))
```

## 13.3 Community

  - [RStudio Community](https://community.rstudio.com/) - Ask questions
  - [tidymodels GitHub](https://github.com/tidymodels) - Source code and
    issues
  - [\#tidymodels on Twitter](https://twitter.com/hashtag/tidymodels)

## 13.4 Comparisons and Benchmarks

  - [Caret
    vs. tidymodels](https://medium.com/data-science/caret-vs-tidymodels-create-complete-reusable-machine-learning-workflows-5c50a7befd2d)
    - Real-world comparison by Hannah Roos
  - [From caret to
    tidymodels](https://www.tidyverse.org/blog/2020/04/tidymodels-org/)
    - Official migration guide

-----

# 14 Quick Reference

## 14.1 Common Workflow Pattern

``` r
# 1. Split
split <- initial_split(data, prop = 0.75)
train <- training(split)
test <- testing(split)
folds <- vfold_cv(train, v = 10)

# 2. Recipe
rec <- recipe(outcome ~ ., data = train) %>%
  step_normalize(all_numeric_predictors()) %>%
  step_dummy(all_nominal_predictors())

# 3. Model
model <- rand_forest(mtry = tune(), min_n = tune()) %>%
  set_engine("ranger") %>%
  set_mode("regression")

# 4. Workflow
wf <- workflow() %>%
  add_recipe(rec) %>%
  add_model(model)

# 5. Tune
results <- wf %>%
  tune_grid(resamples = folds, grid = 10)

# 6. Finalize
best <- select_best(results, "rmse")
final_wf <- finalize_workflow(wf, best)
final_fit <- last_fit(final_wf, split)

# 7. Evaluate
collect_metrics(final_fit)
```

-----

**Happy modeling with tidymodels\!**
