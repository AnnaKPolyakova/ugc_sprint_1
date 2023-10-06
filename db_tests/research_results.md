### Data based on the results of 100 consecutive tests


#### Testing cassanda:

Data scheme: 2 node (replicas)

Without load

| test                                      |     min - max, s:ms     | median, s:ms |
|-------------------------------------------|:-----------------------:|:------------:|
| insert test                               |  0: 5 435 - 0: 15 572   |   0: 6 488   |
| get all from 2 000 000 obj test           | 0: 49 099 - 0: 902 875  |  0: 72 526   |
| select where timestamp = 1 where from 10 000 000 obj test | 0: 678 426 - 1: 119 818 |  0: 695 296  |
| SELECT sum(timestamp) FROM test.views WHERE timestamp > 50 from 10 000 000 obj test |        get error        |  get error   |


With load (a parallel process is running, recording 100 records per 0.01 sec)

| Тест        |     min - max, s:ms     | median, s:ms |
|-------------|:-----------------------:|:------------:|
| insert test |    0: 7 584 - 27 762    |  0: 13 239   |
| select where timestamp = 1 from 10 000 000 obj test | 0: 762 829 - 1: 371 429 |  0: 789 158  |
| SELECT sum(timestamp) FROM test.views WHERE timestamp > 50 from 10 000 000 obj test | get error    |  get error     |


#### Testing clickhouse:

Data schema: 4 node (2 replicas, 2 partitions)

Without load

| Тест                                               |     min - max, s:ms     | median, s:ms |
|----------------------------------------------------|:-----------------------:|:------------:|
| insert test                                        |  0: 3 512 - 0: 16 689   |   0: 4 889   |
| get all from 2 000 000 obj test                    |  0: 30 717 - 0: 46 275  |  0: 33 772   |
| select where timestamp = 1 from 10 000 000 obj test | 0: 636078 - 0: 733 061  |  0: 668 870  |
| SELECT sum(timestamp) FROM test.views WHERE timestamp > 50 from 10 000 000 obj test | 0: 038 698 - 0: 100 078 |  0: 041 365  |


With load (a parallel process is running, recording 100 records per 0.01 sec)

| Тест        |     min - max, s:ms     | median, s:ms |
|-------------|:-----------------------:|:------------:|
| insert test |    0: 4 098 - 14 540    |   0: 6 614   |
| select where timestamp = 1 from 10 000 000 obj test | 0: 907 240 - 5: 250 530 |  1: 554 646  |
| SELECT sum(timestamp) FROM test.views WHERE timestamp > 50 from 10 000 000 obj test | 0: 047 936 - 0: 091 991 |  0: 054 389  |


During testing of Cassandra, the following disadvantages were identified:
- we get an error when making an aggregation request with a database with 10,000,000 objects,
   although a similar request passes with an almost empty database
- complex configuration settings Example:
1) You need to think very well in advance
   what queries will be sent to the database before generating the key?
   parties and so on.
2) Initially I planned 4 nodes (2 partitions and 2 replicas) for comparability
    testing with clickhouse. But docker doesn't pull more than 3 (or go back to 1
    point - it’s difficult to configure or doesn’t have the resources, I’m inclined towards 2)
etc.

Additionally, read the comparative characteristics of Cassandra and clickhouse in
on the Internet I concluded that clickhouse itself is younger, more convenient,
fast database

Conclusion: choose clickhouse
