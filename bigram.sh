rm -rf /home/hadoop/output/*
hdfs dfs -rm -r TwitterDataInput
hdfs dfs -rm -r TwitterData
hdfs dfs -rm -r NewsDataInput
hdfs dfs -rm -r NewsData
hdfs dfs -put /home/hadoop/input/TwitterData TwitterDataInput
hdfs dfs -put /home/hadoop/input/NewsData NewsDataInput
hadoop jar /home/hadoop/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.4.jar -mapper 'python /home/hadoop/code/mapper.py 2' -reducer 'python /home/hadoop/code/reducer.py' -input TwitterDataInput -output TwitterData
hadoop jar /home/hadoop/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.4.jar -mapper 'python /home/hadoop/code/mapper.py 2' -reducer 'python /home/hadoop/code/reducer.py' -input NewsDataInput -output NewsData
hdfs dfs -get TwitterData /home/hadoop/output/
hdfs dfs -get NewsData /home/hadoop/output/