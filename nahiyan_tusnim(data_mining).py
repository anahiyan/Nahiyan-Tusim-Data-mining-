# -*- coding: utf-8 -*-
"""Nahiyan Tusnim(Data mining).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ASbjhiAovlmzAHrXjSnwBaAIfoVZEcck
"""

!pip install -q kaggle

from google.colab import files

# Upload your Kaggle API key (kaggle.json) file
files.upload()

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets list

!kaggle datasets download -d heeraldedhia/groceries-dataset

!mkdir groceries

!unzip groceries-dataset.zip -d groceries

cd/content/groceries/

#Dataset_1 "Comparative Analysis Between Apriori and Fp Growth"

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth

groceries = pd.read_csv("Groceries_dataset.csv")

groceries.shape

groceries.head()

# Get all the transactions as a list of lists
all_transactions = [transaction[1]['itemDescription'].tolist() for transaction in list(groceries.groupby(['Member_number', 'Date']))]

# First 21st transactions in the transactional dataset
len(all_transactions)

# Look at the 10 first transactions
all_transactions[0:10]

# The following instructions transform the dataset into the required format
trans_encoder = TransactionEncoder() # Instanciate the encoder
trans_encoder_matrix = trans_encoder.fit(all_transactions).transform(all_transactions)
trans_encoder_matrix = pd.DataFrame(trans_encoder_matrix, columns=trans_encoder.columns_)

trans_encoder_matrix.head()

def perform_rule_calculation(transact_items_matrix, rule_type="fpgrowth", min_support=0.001):
    """
    desc: this function performs the association rule calculation
    @params:
        - transact_items_matrix: the transaction X Items matrix
        - rule_type:
                    - apriori or Growth algorithms (default="fpgrowth")

        - min_support: minimum support threshold value (default = 0.001)

    @returns:
        - the matrix containing 3 columns:
            - support: support values for each combination of items
            - itemsets: the combination of items
            - number_of_items: the number of items in each combination of items

        - the excution time for the corresponding algorithm

    """
    start_time = 0
    total_execution = 0

    if(not rule_type=="fpgrowth"):
        start_time = time.time()
        rule_items = apriori(transact_items_matrix,
                       min_support=min_support,
                       use_colnames=True)
        total_execution = time.time() - start_time
        print("Computed Apriori!")

    else:
        start_time = time.time()
        rule_items = fpgrowth(transact_items_matrix,
                       min_support=min_support,
                       use_colnames=True)
        total_execution = time.time() - start_time
        print("Computed Fp Growth!")

    rule_items['number_of_items'] = rule_items['itemsets'].apply(lambda x: len(x))

    return rule_items, total_execution

def compute_association_rule(rule_matrix, metric="lift", min_thresh=1):
    """
    @desc: Compute the final association rule
    @params:
        - rule_matrix: the corresponding algorithms matrix
        - metric: the metric to be used (default is lift)
        - min_thresh: the minimum threshold (default is 1)

    @returns:
        - rules: all the information for each transaction satisfying the given metric & threshold
    """
    rules = association_rules(rule_matrix,
                              metric=metric,
                              min_threshold=min_thresh)

    return rules

# Plot Lift Vs Coverage(confidence)
def plot_metrics_relationship(rule_matrix, col1, col2):
    """
    desc: shows the relationship between the two input columns
    @params:
        - rule_matrix: the matrix containing the result of a rule (apriori or Fp Growth)
        - col1: first column
        - col2: second column
    """
    fit = np.polyfit(rule_matrix[col1], rule_matrix[col2], 1)
    fit_funt = np.poly1d(fit)
    plt.plot(rule_matrix[col1], rule_matrix[col2], 'yo', rule_matrix[col1],
    fit_funt(rule_matrix[col1]))
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.title('{} vs {}'.format(col1, col2))

def compare_time_exec(algo1=list, alg2=list):
    """
    @desc: shows the execution time between two algorithms
    @params:
        - algo1: list containing the description of first algorithm, where

        - algo2: list containing the description of second algorithm, where
    """

    execution_times = [algo1[1], algo2[1]]
    algo_names = (algo1[0], algo2[0])
    y=np.arange(len(algo_names))

    plt.bar(y,execution_times,color=['orange', 'blue'])
    plt.xticks(y,algo_names)
    plt.xlabel('Algorithms')
    plt.ylabel('Time')
    plt.title("Execution Time (seconds) Comparison")
    plt.show()

val = {'name':12}
value = list(val.items())[0]

value

fpgrowth_matrix, fp_growth_exec_time = perform_rule_calculation(trans_encoder_matrix) # Run the algorithm
print("Fp Growth execution took: {} seconds".format(fp_growth_exec_time))

fpgrowth_matrix.head()

fpgrowth_matrix.tail()

fp_growth_rule_lift = compute_association_rule(fpgrowth_matrix)

fp_growth_rule_lift.head()

plot_metrics_relationship(fp_growth_rule_lift, col1='lift', col2='confidence')

fp_growth_rule = compute_association_rule(fpgrowth_matrix, metric="confidence", min_thresh=0.2)
fp_growth_rule.head()

apriori_matrix, apriori_exec_time = perform_rule_calculation(trans_encoder_matrix, rule_type="apriori")
print("Apriori Execution took: {} seconds".format(apriori_exec_time))

apriori_matrix.head()

apriori_matrix.tail()

apriori_rule_lift = compute_association_rule(apriori_matrix)

apriori_rule_lift.head()

plot_metrics_relationship(apriori_rule_lift, col1='lift', col2='confidence')

apripri_rule = compute_association_rule(apriori_matrix, metric="confidence", min_thresh=0.2)
apripri_rule.head()

algo1 = ['Fp Growth', fp_growth_exec_time]
algo2 = ['Apriori', apriori_exec_time]

compare_time_exec(algo1, algo2)

#solution code of dataset_1

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth

# Load the dataset
groceries = pd.read_csv("Groceries_dataset.csv")
print(groceries.shape)
print(groceries.head())

# Get all the transactions as a list of lists
all_transactions = [transaction[1]['itemDescription'].tolist() for transaction in list(groceries.groupby(['Member_number', 'Date']))]

# First 21 transactions in the transactional dataset
print(len(all_transactions))

# Look at the 10 first transactions
print(all_transactions[0:10])

# The following instructions transform the dataset into the required format
trans_encoder = TransactionEncoder()  # Instantiate the encoder
trans_encoder_matrix = trans_encoder.fit(all_transactions).transform(all_transactions)
trans_encoder_matrix = pd.DataFrame(trans_encoder_matrix, columns=trans_encoder.columns_)
print(trans_encoder_matrix.head())

def perform_rule_calculation(transact_items_matrix, rule_type="fpgrowth", min_support=0.001):
    """
    desc: this function performs the association rule calculation
    @params:
        - transact_items_matrix: the transaction X Items matrix
        - rule_type:
                    - apriori or Growth algorithms (default="fpgrowth")
        - min_support: minimum support threshold value (default = 0.001)
    @returns:
        - the matrix containing 3 columns:
            - support: support values for each combination of items
            - itemsets: the combination of items
            - number_of_items: the number of items in each combination of items
        - the execution time for the corresponding algorithm
    """
    start_time = 0
    total_execution = 0

    if not rule_type == "fpgrowth":
        start_time = time.time()
        rule_items = apriori(transact_items_matrix,
                             min_support=min_support,
                             use_colnames=True)
        total_execution = time.time() - start_time
        print("Computed Apriori!")

    else:
        start_time = time.time()
        rule_items = fpgrowth(transact_items_matrix,
                              min_support=min_support,
                              use_colnames=True)
        total_execution = time.time() - start_time
        print("Computed Fp Growth!")

    rule_items['number_of_items'] = rule_items['itemsets'].apply(lambda x: len(x))

    return rule_items, total_execution

def compute_association_rule(rule_matrix, metric="lift", min_thresh=1):
    """
    @desc: Compute the final association rule
    @params:
        - rule_matrix: the corresponding algorithms matrix
        - metric: the metric to be used (default is lift)
        - min_thresh: the minimum threshold (default is 1)
    @returns:
        - rules: all the information for each transaction satisfying the given metric & threshold
    """
    rules = association_rules(rule_matrix,
                              metric=metric,
                              min_threshold=min_thresh)

    return rules

def plot_metrics_relationship(rule_matrix, col1, col2):
    """
    desc: shows the relationship between the two input columns
    @params:
        - rule_matrix: the matrix containing the result of a rule (apriori or Fp Growth)
        - col1: first column
        - col2: second column
    """
    fit = np.polyfit(rule_matrix[col1], rule_matrix[col2], 1)
    fit_funt = np.poly1d(fit)
    plt.plot(rule_matrix[col1], rule_matrix[col2], 'yo', rule_matrix[col1],
             fit_funt(rule_matrix[col1]))
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.title('{} vs {}'.format(col1, col2))

def compare_time_exec(algo1, algo2):
    """
    @desc: shows the execution time between two algorithms
    @params:
        - algo1: list containing the description of the first algorithm
        - algo2: list containing the description of the second algorithm
    """
    execution_times = [algo1[1], algo2[1]]
    algo_names = (algo1[0], algo2[0])
    y = np.arange(len(algo_names))

    plt.bar(y, execution_times, color=['orange', 'blue'])
    plt.xticks(y, algo_names)
    plt.xlabel('Algorithms')
    plt.ylabel('Time')
    plt.title("Execution Time (seconds) Comparison")
    plt.show()

val = {'name': 12}
value = list(val.items())[0]
print(value)

fpgrowth_matrix, fp_growth_exec_time = perform_rule_calculation(trans_encoder_matrix)
print("Fp Growth execution took: {} seconds".format(fp_growth_exec_time))
print(fpgrowth_matrix.head())
print(fpgrowth_matrix.tail())

fp_growth_rule_lift = compute_association_rule(fpgrowth_matrix)
print(fp_growth_rule_lift.head())

plot_metrics_relationship(fp_growth_rule_lift, col1='lift', col2='confidence')

fp_growth_rule = compute_association_rule(fpgrowth_matrix, metric="confidence", min_thresh=0.2)
print(fp_growth_rule.head())

apriori_matrix, apriori_exec_time = perform_rule_calculation(trans_encoder_matrix, rule_type="apriori")
print("Apriori Execution took: {} seconds".format(apriori_exec_time))
print(apriori_matrix.head())
print(apriori_matrix.tail())

apriori_rule_lift = compute_association_rule(apriori_matrix)
print(apriori_rule_lift.head())

plot_metrics_relationship(apriori_rule_lift, col1='lift', col2='confidence')

apriori_rule = compute_association_rule(apriori_matrix, metric="confidence", min_thresh=0.2)
print(apriori_rule.head())

algo1 = ['Fp Growth', fp_growth_exec_time]
algo2 = ['Apriori', apriori_exec_time]

compare_time_exec(algo1, algo2)

#Dataset_2 "apriori_vs_FPGrowth"

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth

groceries = pd.read_csv("Groceries_dataset.csv")

groceries.head()

all_transactions = [transaction[1]['itemDescription'].tolist() for transaction in list(groceries.groupby(['Member_number', 'Date']))]

#all_transactions

trans_encoder = TransactionEncoder() # Instanciate the encoder
trans_encoder_matrix = trans_encoder.fit(all_transactions).transform(all_transactions)
trans_encoder_matrix = pd.DataFrame(trans_encoder_matrix, columns=trans_encoder.columns_)

trans_encoder_matrix.head()

def perform_rule_calculation(transact_items_matrix, rule_type="fpgrowth", min_support=0.001):

    start_time = 0
    total_execution = 0

    if(not rule_type=="fpgrowth"):
        start_time = time.time()
        rule_items = apriori(transact_items_matrix,
                       min_support=min_support,
                       use_colnames=True)
        total_execution = time.time() - start_time
        print("Computed Apriori!")

    else:
        start_time = time.time()
        rule_items = fpgrowth(transact_items_matrix,
                       min_support=min_support,
                       use_colnames=True)
        total_execution = time.time() - start_time
        print("Computed Fp Growth!")

    rule_items['number_of_items'] = rule_items['itemsets'].apply(lambda x: len(x))

    return rule_items, total_execution

def compute_association_rule(rule_matrix, metric="lift", min_thresh=1):

    rules = association_rules(rule_matrix,
                              metric=metric,
                              min_threshold=min_thresh)

    return rules

def plot_metrics_relationship(rule_matrix, col1, col2):

    fit = np.polyfit(rule_matrix[col1], rule_matrix[col2], 1)
    fit_funt = np.poly1d(fit)
    plt.plot(rule_matrix[col1], rule_matrix[col2], 'yo', rule_matrix[col1],
    fit_funt(rule_matrix[col1]))
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.title('{} vs {}'.format(col1, col2))

def compare_time_exec(algo1=list, alg2=list):


    execution_times = [algo1[1], algo2[1]]
    algo_names = (algo1[0], algo2[0])
    y=np.arange(len(algo_names))

    plt.bar(y,execution_times,color=['orange', 'blue'])
    plt.xticks(y,algo_names)
    plt.xlabel('Algorithms')
    plt.ylabel('Time')
    plt.title("Execution Time (seconds) Comparison")
    plt.show()

val = {'name':12}
value = list(val.items())[0]

fpgrowth_matrix, fp_growth_exec_time = perform_rule_calculation(trans_encoder_matrix) # Run the algorithm
print("Fp Growth execution took: {} seconds".format(fp_growth_exec_time))

fpgrowth_matrix.head()

fpgrowth_matrix.tail()

fp_growth_rule_lift = compute_association_rule(fpgrowth_matrix)

fp_growth_rule_lift.head()

plot_metrics_relationship(fp_growth_rule_lift, col1='lift', col2='confidence')

fp_growth_rule = compute_association_rule(fpgrowth_matrix, metric="confidence", min_thresh=0.2)
fp_growth_rule.head()

apriori_matrix, apriori_exec_time = perform_rule_calculation(trans_encoder_matrix, rule_type="apriori")
print("Apriori Execution took: {} seconds".format(apriori_exec_time))

apriori_matrix.head()

apriori_matrix.tail()

apriori_rule_lift = compute_association_rule(apriori_matrix)

apriori_rule_lift.head()

plot_metrics_relationship(apriori_rule_lift, col1='lift', col2='confidence')

apripri_rule = compute_association_rule(apriori_matrix, metric="confidence", min_thresh=0.2)
apripri_rule.head()

algo1 = ['Fp Growth', fp_growth_exec_time]
algo2 = ['Apriori', apriori_exec_time]

compare_time_exec(algo1, algo2)

# Extract 25% of the data
sample_size = int(0.25 * len(groceries))
sample_data = groceries.sample(n=sample_size, random_state=42)

# Prepare transactions
all_transactions_sample = [transaction[1]['itemDescription'].tolist() for transaction in list(sample_data.groupby(['Member_number', 'Date']))]

# Instantiate and transform the TransactionEncoder
trans_encoder_sample = TransactionEncoder()
trans_encoder_matrix_sample = trans_encoder_sample.fit(all_transactions_sample).transform(all_transactions_sample)
trans_encoder_matrix_sample = pd.DataFrame(trans_encoder_matrix_sample, columns=trans_encoder_sample.columns_)

# Perform FP-Growth and measure execution time
fpgrowth_matrix_sample, fp_growth_exec_time_sample = perform_rule_calculation(trans_encoder_matrix_sample)
print("Fp Growth Execution on Sample took: {} seconds".format(fp_growth_exec_time_sample))

fpgrowth_matrix_sample.head()

fpgrowth_matrix_sample.tail()

fp_growth_rule_lift = compute_association_rule(fpgrowth_matrix_sample)
fp_growth_rule_lift

plot_metrics_relationship(fp_growth_rule_lift, col1='lift', col2='confidence')

# Perform Apriori and measure execution time
apriori_matrix_sample, apriori_exec_time_sample = perform_rule_calculation(trans_encoder_matrix_sample, rule_type="apriori")
print("Apriori Execution on Sample took: {} seconds".format(apriori_exec_time_sample))

apriori_matrix_sample.head()

apriori_matrix_sample.tail()

apriori_rule_lift = compute_association_rule(apriori_matrix_sample)
apriori_rule_lift

plot_metrics_relationship(apriori_rule_lift, col1='lift', col2='confidence')

algo1 = ['Fp Growth', fp_growth_exec_time_sample]
algo2 = ['Apriori', apriori_exec_time_sample]

compare_time_exec(algo1, algo2)