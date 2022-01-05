###### Classification Metrics
- *Purpose*: Investigate binary classification metrics.  
- *Process*: Write functions to compute binary classification metrics: accuracy, precision, sensitivity, specificity, F1. Write a function to plot a ROC curve and compute AUC. Use the functions we implemented to compute metrics for a given data set. Compare output from our functions to that of standard libraries.  
- *Toolkit*: Programming in R, the libraries pROC, caret.  
- *Metric*: Do our functions and the standard libraries return the same values? Yes.  

###### Crime
- *Purpose*: Predict whether a neighborhood's crime rate lies above or below the city's median crime rate.  
- *Process*: Perform exploratory analysis, variable transformations, logistic regression, model selection, and discuss results.  
- *Toolkit*: Logistic regression in R, various libraries for analysis including caret, tidyverse, and pROC, and R Markdown formatting libraries like stargazer and knitr.  
- *Metric*: We considered model parsimony, AIC, precision, accuracy, and AUC in selecting a model. Final model accuracy = 0.86 on test data.

###### Insurance
- *Purpose*: Predict whether a given customer will be involved in a car crash, and predict the cost of the crash to an insurance company.  
- *Process*: Perform exploratory analysis, variable transformations including imputation for missing values, logistic and OLS regression, and discuss results.  
- *Toolkit*: Linear modeling in R, various libraries for analysis including caret, mice, tidyverse, and MASS, and R Markdown formatting libraries like flextable.  
- *Metric*: AIC for logistic regression, r-squared for cost estimation.  

###### Wine Sales
- *Purpose*: Predict wine sales based on chemical properties. Compare Poisson, negative binomial, and multiple linear regression models.  
- *Process*: Perform exploratory analysis, variable transformations, model construction and selection, and generate predictions. Discuss results.  
- *Toolkit*: Linear modeling in R.  
- *Metric*: 