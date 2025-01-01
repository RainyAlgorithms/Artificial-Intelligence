from bnetbase import Variable, Factor, BN
import csv
import itertools


def normalize(factor):
    """
    Normalize the factor such that its values sum to 1.
    Do not modify the input factor.

    :param factor: a Factor object.
    :return: a new Factor object resulting from normalizing factor.
    """
    normal = sum(factor.values)
    new_values = []
    for value in factor.values:
        new_values.append(value / normal)
    new_factor = Factor(factor.name, factor.scope)
    new_factor.values = new_values
    return new_factor


def restrict(factor, variable, value):
    """
    Restrict a factor by assigning value to variable.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to restrict.
    :param value: the value to restrict the variable to
    :return: a new Factor object resulting from restricting variable to value.
             This new factor no longer has variable in it.

    """
    values, scope = factor.values, factor.get_scope()
    var_index = scope.index(variable)
    value_index = variable.value_index(value)

    size = 1
    for s in scope[:var_index]:
        size *= s.domain_size()

    diff = 1
    for s in scope[var_index + 1:]:
        diff *= s.domain_size()

    scope.pop(var_index)
    size = len(values) // size
    start = value_index * diff
    new_vals = []

    for i in range(0, len(values), size):
        for j in range(start, diff + start):
            new_vals.append(values[j + i])

    factor_name = f'r({factor.name}, {variable.name}={value})'
    restrict_factor = Factor(factor_name, scope)
    restrict_factor.values = new_vals
    return restrict_factor


def sum_out(factor, variable):
    """
    Sum out a variable variable from factor factor.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to sum out.
    :return: a new Factor object resulting from summing out variable from the factor.
             This new factor no longer has variable in it.
    """
    values = factor.values
    scope = factor.get_scope()
    var_index = scope.index(variable)

    diff = 1
    for s in scope[var_index + 1:]:
        diff *= s.domain_size()

    scope.pop(var_index)
    new_values = []

    val = 0
    while val < len(values):
        temp_values = []
        for j in range(val, val + diff):
            sum_value = 0
            for k in range(variable.domain_size()):
                ind = k * diff + j
                sum_value += values[ind]
            temp_values.append(sum_value)
        new_values.extend(temp_values)
        val += variable.domain_size() * diff

    new_factor = Factor(f's({factor.name}, {variable.name})', scope)
    new_factor.values = new_values
    return new_factor


def multiply(factor_list):
    """
    Multiply a list of factors together.
    Do not modify any of the input factors.

    :param factor_list: a list of Factor objects.
    :return: a new Factor object resulting from multiplying all the factors in factor_list.
    """
    all_variables = []
    for factor in factor_list:
        for variable in factor.scope:
            if variable not in all_variables:
                all_variables.append(variable)

    variable_domains = [variable.domain() for variable in all_variables]
    new_factor_entries = []
    for values in itertools.product(*variable_domains):
        assignment = dict(zip(all_variables, values))
        product_value = 1
        for factor in factor_list:
            factor_assignment = tuple(assignment[var] for var in factor.scope)
            factor_value = factor.get_value(factor_assignment)
            product_value *= factor_value
        new_factor_entries.append(list(values) + [product_value])

    new_factor_name = ' * '.join([factor.name for factor in factor_list])
    result_factor = Factor(f'({new_factor_name})', all_variables)
    result_factor.add_values(new_factor_entries)
    return result_factor


def ve(bayes_net, var_query, EvidenceVars):
    """

    Execute the variable elimination algorithm on the Bayesian network bayes_net
    to compute a distribution over the values of var_query given the
    evidence provided by EvidenceVars.

    :param bayes_net: a BN object.
    :param var_query: the query variable. we want to compute a distribution
                     over the values of the query variable.
    :param EvidenceVars: the evidence variables. Each evidence variable has
                         its evidence set to a value from its domain
                         using set_evidence.
    :return: a Factor object representing a distribution over the values
             of var_query. that is a list of numbers, one for every value
             in var_query's domain. These numbers sum to 1. The i-th number
             is the probability that var_query is equal to its i-th value given
             the settings of the evidence variables.

    For example, assume that
        var_query = A with Dom[A] = ['a', 'b', 'c'],
        EvidenceVars = [B, C], and
        we have called B.set_evidence(1) and C.set_evidence('c'),
    then VE would return a list of three numbers, e.g. [0.5, 0.24, 0.26].
    These numbers would mean that
        Pr(A='a'|B=1, C='c') = 0.5,
        Pr(A='a'|B=1, C='c') = 0.24, and
        Pr(A='a'|B=1, C='c') = 0.26.

    """
    factors_lst = apply_evidence(bayes_net.factors(), EvidenceVars)
    hidden_vars = get_hidden_variables(factors_lst, var_query, set(EvidenceVars))
    eliminate_order = get_elimination_order(factors_lst, hidden_vars)
    for var in eliminate_order:
        factors_lst = eliminate(factors_lst, var)

    multiply_factor = multiply(factors_lst)
    return normalize(multiply_factor)


def apply_evidence(factors, evidence_vars):
    """
    Restricts factors given the evidence
    """
    new_factors = []
    for factor in factors:
        restricted_factor = factor
        for variable in evidence_vars:
            if variable in factor.get_scope():
                value = variable.get_evidence()
                restricted_factor = restrict(restricted_factor, variable, value)
        new_factors.append(restricted_factor)
    return new_factors


def get_hidden_variables(factors, query_var, evidence_vars):
    """
    Find and return hidden variables
    """
    variables = set(var for factor in factors for var in factor.get_scope())
    hidden = variables - {query_var} - evidence_vars
    return hidden


def get_elimination_order(factors, hidden_vars):
    order = []
    scopes = [set(factor.get_scope()) for factor in factors]

    while hidden_vars:
        var_degrees = {}
        for var in hidden_vars:
            degree = sum(1 for scope in scopes if var in scope)
            var_degrees[var] = degree
        min_var = min(var_degrees, key=var_degrees.get)
        order.append(min_var)
        hidden_vars.remove(min_var)
        related_scopes = [scope for scope in scopes if min_var in scope]
        new_scope = set().union(*related_scopes) - {min_var}
        scopes = [scope for scope in scopes if min_var not in scope]
        if new_scope:
            scopes.append(new_scope)

    return order


def eliminate(factors, variable):
    variable_factors = [f for f in factors if variable in f.get_scope()]
    if not variable_factors:
        return factors
    multiply_factor = multiply(variable_factors)
    sum_out_factor = sum_out(multiply_factor, variable)
    remaining_factors = [f for f in factors if f not in variable_factors]
    remaining_factors.append(sum_out_factor)
    return remaining_factors


def naive_bayes_model(data_file):
    """
   NaiveBayesModel returns a BN that is a Naive Bayes model that
   represents the joint distribution of value assignments to
   variables in the Adult Dataset from UCI.  Remember a Naive Bayes model
   assumes P(X1, X2,.... XN, Class) can be represented as
   P(X1|Class)*P(X2|Class)* .... *P(XN|Class)*P(Class).
   When you generated your Bayes bayes_net, assume that the values
   in the SALARY column of the dataset are the CLASS that we want to predict.
   @return a BN that is a Naive Bayes model and which represents the Adult Dataset.
    """
    # READ IN THE DATA
    input_data = []
    with open(data_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # skip header row
        for row in reader:
            input_data.append(row)

    # DOMAIN INFORMATION REFLECTS ORDER OF COLUMNS IN THE DATA SET
    variable_domains = {
        "Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
        "Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'],
        "Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'],
        "MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
        "Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
        "Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'],
        "Gender": ['Male', 'Female'],
        "Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'],
        "Salary": ['<50K', '>=50K']
    }

    # variables
    WORK = Variable('Work', variable_domains['Work'])
    EDUCATION = Variable('Education', variable_domains['Education'])
    MARTIAL_STATUS = Variable('MaritalStatus', variable_domains['MaritalStatus'])
    OCCUPATION = Variable('Occupation', variable_domains['Occupation'])
    RELATIONSHIP = Variable('Relationship', variable_domains['Relationship'])
    RACE = Variable('Race', variable_domains['Race'])
    GENDER = Variable('Gender', variable_domains['Gender'])
    COUNTRY = Variable('Country', variable_domains['Country'])
    SALARY = Variable('Salary', variable_domains['Salary'])

    # factors
    work_factor = Factor('Work', [WORK, SALARY])
    education_factor = Factor('Education', [EDUCATION, SALARY])
    martial_status_factor = Factor('MaritalStatus', [MARTIAL_STATUS, SALARY])
    occupation_factor = Factor('Occupation', [OCCUPATION, SALARY])
    relationship_factor = Factor('Relationship', [RELATIONSHIP, SALARY])
    race_factor = Factor('Race', [RACE, SALARY])
    gender_factor = Factor('Gender', [GENDER, SALARY])
    country_factor = Factor('Country', [COUNTRY, SALARY])
    salary_factor = Factor('Salary', [SALARY])
    factors = [work_factor, education_factor, martial_status_factor, occupation_factor, relationship_factor,
               race_factor, gender_factor, country_factor]

    # salary count
    salary_count = {'<50K': 0., '>=50K': 0.}
    for work, edu, mar, occ, rs, race, gen, count, sal in input_data:
        salary_count[sal] += 1

    each_salary_count = [dict() for _ in range(8)]
    for work, edu, mar, occ, rs, race, gen, count, sal in input_data:
        each_salary_count[0][(work, sal)] = each_salary_count[0].get((work, sal), 0) + 1
        each_salary_count[1][(edu, sal)] = each_salary_count[1].get((edu, sal), 0) + 1
        each_salary_count[2][(mar, sal)] = each_salary_count[2].get((mar, sal), 0) + 1
        each_salary_count[3][(occ, sal)] = each_salary_count[3].get((occ, sal), 0) + 1
        each_salary_count[4][(rs, sal)] = each_salary_count[4].get((rs, sal), 0) + 1
        each_salary_count[5][(race, sal)] = each_salary_count[5].get((race, sal), 0) + 1
        each_salary_count[6][(gen, sal)] = each_salary_count[6].get((gen, sal), 0) + 1
        each_salary_count[7][(count, sal)] = each_salary_count[7].get((count, sal), 0) + 1

    for x in range(8):
        values = []
        for key, value in each_salary_count[x].items():
            w, s = key
            values.append([w, s, value / salary_count[s]])
        factors[x].add_values(values)

    salary_values = []
    for key, value in salary_count.items():
        avg = value / len(input_data)
        salary_values.append([key, avg])

    salary_factor.add_values(salary_values)
    factors.append(salary_factor)

    return BN('bayes_net', [WORK, EDUCATION, MARTIAL_STATUS, OCCUPATION, RELATIONSHIP,
                            RACE, GENDER, COUNTRY, SALARY], factors)


def explore(bayes_net, question):
    """    Input: bayes_net---a BN object (a Bayes bayes_net)
           question---an integer indicating the question in HW4 to be calculated. Options are:
           1. What percentage of the women in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
           2. What percentage of the men in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
           3. What percentage of the women in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
           4. What percentage of the men in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
           5. What percentage of the women in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           6. What percentage of the men in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           @return a percentage (between 0 and 100)
    """
    variables = bayes_net.variables()
    VAR_WORK_CLASS, VAR_EDUCATION, VAR_MARITAL_STATUS, VAR_OCCUPATION, \
        VAR_RELATIONSHIP, VAR_RACE, VAR_GENDER, VAR_COUNTRY, VAR_SALARY = variables

    with open('data/adult-test.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # Skip header row
        data_samples = [row for row in csv_reader]

    gender_counts = {'Male': 0, 'Female': 0}
    for sample in data_samples:
        gender = sample[6]
        if gender in gender_counts:
            gender_counts[gender] += 1

    match_count = 0
    total_relevant = 0

    if question == 1 or question == 2:
        target_gender = 'Female' if question == 1 else 'Male'
        total_count = gender_counts[target_gender]

        for sample in data_samples:
            if sample[6] != target_gender:
                continue

            evidence_vars_E1 = [VAR_WORK_CLASS, VAR_OCCUPATION, VAR_EDUCATION, VAR_RELATIONSHIP]
            evidence_vals_E1 = [sample[0], sample[3], sample[1], sample[4]]
            for var, val in zip(evidence_vars_E1, evidence_vals_E1):
                var.set_evidence(val)

            factor_E1 = ve(bayes_net, VAR_SALARY, evidence_vars_E1)
            prob_E1 = factor_E1.values[1]

            evidence_vars_E2 = evidence_vars_E1 + [VAR_GENDER]
            evidence_vals_E2 = evidence_vals_E1 + [sample[6]]
            for var, val in zip(evidence_vars_E2, evidence_vals_E2):
                var.set_evidence(val)

            factor_E2 = ve(bayes_net, VAR_SALARY, evidence_vars_E2)
            prob_E2 = factor_E2.values[1]

            if prob_E1 > prob_E2:
                match_count += 1

        percentage = (match_count / total_count) * 100 if total_count > 0 else 0.0

    elif question == 3 or question == 4:
        target_gender = 'Female' if question == 3 else 'Male'

        for sample in data_samples:
            if sample[6] != target_gender:
                continue

            evidence_vars_E1 = [VAR_WORK_CLASS, VAR_OCCUPATION, VAR_EDUCATION, VAR_RELATIONSHIP]
            evidence_vals_E1 = [sample[0], sample[3], sample[1], sample[4]]
            for var, val in zip(evidence_vars_E1, evidence_vals_E1):
                var.set_evidence(val)

            factor_E1 = ve(bayes_net, VAR_SALARY, evidence_vars_E1)
            prob_E1 = factor_E1.values[1]

            if prob_E1 > 0.5:
                total_relevant += 1
                if sample[8] == '>=50K':
                    match_count += 1

        percentage = (match_count / total_relevant) * 100 if total_relevant > 0 else 0.0

    elif question == 5 or question == 6:
        target_gender = 'Female' if question == 5 else 'Male'
        total_count = gender_counts[target_gender]

        for sample in data_samples:
            if sample[6] != target_gender:
                continue

            evidence_vars_E1 = [VAR_WORK_CLASS, VAR_OCCUPATION, VAR_EDUCATION, VAR_RELATIONSHIP]
            evidence_vals_E1 = [sample[0], sample[3], sample[1], sample[4]]
            for var, val in zip(evidence_vars_E1, evidence_vals_E1):
                var.set_evidence(val)

            factor_E1 = ve(bayes_net, VAR_SALARY, evidence_vars_E1)
            prob_E1 = factor_E1.values[1]

            if prob_E1 > 0.5:
                match_count += 1

        percentage = (match_count / total_count) * 100 if total_count > 0 else 0.0

    return percentage


if __name__ == '__main__':
    nb = naive_bayes_model('data/adult-train.csv')
    for i in range(1, 7):
        print("explore(nb,{}) = {}".format(i, explore(nb, i)))
