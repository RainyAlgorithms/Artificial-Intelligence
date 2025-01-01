# Naive Bayes Salary Prediction

This project implements a **Naive Bayesian Network** to predict the salary category (`<50K` or `>=50K`) of individuals based on the 1994 US Census dataset. It uses **Variable Elimination** and other Bayesian inference techniques to compute probabilities and evaluate model fairness.

## Features

- **Bayesian Network Construction:**
  - Defines variables for nine attributes, including work class, education, marital status, etc.
  - Represents conditional probabilities for each attribute based on salary.
- **Inference Techniques:**
  - **Variable Elimination (VE):** Computes probability distributions for query variables given evidence.
  - **Normalization, Restriction, Summation:** Implements core factor operations for VE.
- **Fairness Evaluation:**
  - Measures fairness across gender using demographic parity, separation, and sufficiency metrics.

## Usage

Run the program with the provided training and test datasets to train the Naive Bayes model and perform evaluations:

### Train the Model:
```bash
python3 naive_bayes_solution.py
```

### Input Data:
- `adult-train.csv`: Training data (used to construct the Bayesian Network).
- `adult-test.csv`: Test data (used to evaluate predictions and fairness).

### Output:
- Prints the results for six fairness-related questions directly to the console.

## Input Format
- Each row in the CSV files contains attributes for an individual:
  - Work, Education, MaritalStatus, Occupation, Relationship, Race, Gender, Country, Salary.
- Example:
  ```
  Work,Education,MaritalStatus,Occupation,Relationship,Race,Gender,Country,Salary
  Private,HS-Graduate,Married,Manual Labour,Husband,White,Male,North-America,>=50K
  ```

## Key Functions and Classes

- **`normalize(factor)`**: Normalizes probabilities in a factor.
- **`restrict(factor, variable, value)`**: Restricts a factor to a specific value.
- **`sum_out(factor, variable)`**: Sums out a variable from a factor.
- **`multiply(factor_list)`**: Multiplies a list of factors.
- **`ve(bayes_net, var_query, evidence_vars)`**: Performs Variable Elimination to calculate query probabilities.
- **`naive_bayes_model(data_file)`**: Constructs a Naive Bayes model from the training data.
- **`explore(bayes_net, question)`**: Evaluates six fairness metrics based on gender.

## Requirements

- Python 3.x
- Compatible with the `teach.cs` server.

## Notes

- Avoid modifying `bnetbase.py`, as it contains essential base classes for Bayesian Networks.
- Test your implementation thoroughly beyond the provided autograder.