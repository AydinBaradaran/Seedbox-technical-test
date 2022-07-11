import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats





def generate_combined_graph(combined_data, group_ids):
	plt.figure()
	plt.bar(group_ids, combined_data.groupby("test_group").count()["transaction_id"] )
	plt.xlabel("Group ID (0=Control, 1 = Test)")
	plt.ylabel("Number of occurences")
	plt.title("merged tables group id's # of occurences")
	plt.show()

def generate_test_samples_graph(test_sample, group_ids):
	plt.figure()
	plt.bar(group_ids, test_sample.groupby("test_group").count()["sample_id"])
	plt.xlabel("Group ID (0=Control, 1 = Test)")
	plt.ylabel("Number of occurences")
	plt.title("TestSamples.csv group id's # of occurences")
	plt.show()


def rebill_of_groups(group_0, group_1):
	# grab the unique users values for each group
	group_0["sample_id"] = group_0["sample_id"].drop_duplicates()
	group_0.dropna(inplace=True)
	group_1["sample_id"] = group_1["sample_id"].drop_duplicates()
	group_1.dropna(inplace=True)
	# grab the number of rebills between the groups
	data_rebill_0 = group_0[group_0["transaction_type"] == "REBILL"]
	data_rebill_1 = group_1[group_1["transaction_type"] == "REBILL"]
	# compare and show results
	if data_rebill_0.shape[0] > data_rebill_1.shape[0]:
		print("If a user must call-in to cancel they are less likely to have an additional rebill over a user who can cancel from web form")
	elif data_rebill_1.shape[0] > data_rebill_0.shape[0]:
		print("If a user must call-in to cancel they are more likely to have an additional rebill over a user who can cancel from web form")
	else:
		print("no difference between the groups and their number of rebills")
	print("Control group # of rebills: ", data_rebill_0.shape[0])
	print("Test group # of rebills: ", data_rebill_1.shape[0])
	print("------------------")


def total_rev_of_groups(group_0, group_1):
	# calculate the total revenue per group
	total_rev_0 = group_0.groupby(["test_group"]).sum("transaction_amount")["transaction_amount"]
	total_rev_1 = group_1.groupby(["test_group"]).sum("transaction_amount")["transaction_amount"]
	# calculate the average revenue per group
	avg_rev_0 = group_0.groupby(["test_group"]).mean("transaction_amount")["transaction_amount"]
	avg_rev_1 = group_1.groupby(["test_group"]).mean("transaction_amount")["transaction_amount"]
	# compare total revenue, display finding
	if total_rev_0.values > total_rev_1.values:
		print("those cancel over web form generate more total revenue than those who call in")
	elif total_rev_0.values < total_rev_1.values:
		print("those who cancel by call-in generate more total revenue than those who over web form")
	else:
		print("both methods of cancelation generate the same total revenue")
	print("Control groups total revenue: ", total_rev_0.values)
	print("Test groups total revenue: ", total_rev_1.values)
	print("------------------")
	# compare average revenue and compare findings
	if avg_rev_0.values > avg_rev_1.values:
		print("those cancel over web form generate more average revenue than those who call in")
	elif avg_rev_0.values < avg_rev_1.values:
		print("those who cancel by call-in generate more average revenue than those who over web form")
	else:
		print("both methods of cancelation generate the same average revenue")
	print("Control groups average revenue: ", avg_rev_0.values)
	print("Test groups average revenue: ", avg_rev_1.values)
	print("------------------")

def chargeback_rate_of_groups(group_0, group_1):
	# calculate the chargeback rate from the equation given
	chargeback_rate_0 = group_0[group_0["transaction_type"] == "CHARGEBACK"].shape[0]/group_0[group_0["transaction_type"] == "REBILL"].shape[0]
	chargeback_rate_1= group_1[group_1["transaction_type"] == "CHARGEBACK"].shape[0]/group_1[group_1["transaction_type"] == "REBILL"].shape[0]
	# compare the rates and show findings
	if chargeback_rate_1 > chargeback_rate_0:
		print("Those who call-in to cancel have a larger chargeback rate than those who cancel over web")
	elif chargeback_rate_1 < chargeback_rate_0:
		print("Those who cancel over web have a larger chargeback rate than those cancel by call-in")
	else:
		print("both groups share the same chargeback rate")
	print("Control group chargeback rate is: ", chargeback_rate_0)
	print("Test group chargeback rate is: ", chargeback_rate_1)


if __name__ == '__main__':
	# read the csv files given
	transaction_data = pd.read_csv("transData.csv")
	test_sample = pd.read_csv("testSamples.csv")
	# merge the datasets on the sample_id
	combined_data = pd.merge(transaction_data, test_sample, how="inner", on=["sample_id","sample_id"])
	# generate the x-axis for the bar graph
	group_ids = combined_data.groupby("test_group").count().index
	group_ids = [str(i) for i in group_ids]
	generate_combined_graph(combined_data, group_ids)
	generate_test_samples_graph(test_sample, group_ids)
	# isolate each group, so we do it once and not in each function call
	group_0 = combined_data[combined_data["test_group"] == 0]
	group_1 = combined_data[combined_data["test_group"] == 1]
	# the three functions answer questions 2-4 respectively
	rebill_of_groups(group_0, group_1)
	total_rev_of_groups(group_0, group_1)
	chargeback_rate_of_groups(group_0, group_1)