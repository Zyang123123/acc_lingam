Here, we consider time series collected from an IT monitoring system provided by EasyVista. The sampling rate in two different systems can be different.

In each system, we consider two settings:
	- Data from the system at the normal regime, i.e., when there is no incident
	- Data from the system at the anomalous regime, i.e., when there is an incident

In each setting, we consider two data type: 
	- Quantitative data available at ./Quantitative_data
	- Mixed data available at ./Mixed_data

In each data type, one can find two main folders: 
	- ground_truth: the ground truth of a summary causal graph for a given scenario
	- returns: time series for a given scenario

Note that a file in the ground_truth folder that has the same name as a subfolder in the returns folder are associated with each other.
Example: if there exist a file in ground_truth called "A.csv" and a subfolder in returns called "A", then the datasets in the subfolder "A" correspond to the summary causal graph represented in "A.csv"


The first column of each file in the ground truth folder represents the causes, and the second colomun represents the effects.




#############################################################################################################################
#############################################################################################################################
Data description
#############################################################################################################################
#############################################################################################################################

Quantitative data:
	1. metric_extraction: activity of extraction of metrics from messages;
	2. message_dispatcher: activity of a process that orient messages to other process with respect to different types of messages; 
	3. metric_insertion: activity of insertion of data in a database; 
	4. group_history insertion: activity of insertion of historical status in database;
	5. collector_monitoring_information: activity of updates in a given database.

Qualitative data:
	1. status_metric_extraction: status of activity of extraction of metrics from messages;



#############################################################################################################################
#############################################################################################################################
Remarks
#############################################################################################################################
#############################################################################################################################
To know which dataset corresponds to which paper please check the ./Guide_For_Papers.txt

