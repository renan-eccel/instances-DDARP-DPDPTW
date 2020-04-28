'''
Script to fix the lr205*.pdp Pankratz(2005) instances
using the data from Li and Lim(2003) instances

@author renan-eccel
'''
import os

correct_coordinates = \
'''0	40	50
1	25	85
2	22	75
3	22	85
4	20	80
5	20	85
6	18	75
7	15	75
8	15	80
9	10	35
10	10	40
11	8	40
12	8	45
13	5	35
14	5	45
15	2	40
16	0	40
17	0	45
18	44	5
19	42	10
20	42	15
21	40	5
22	40	15
23	38	5
24	38	15
25	35	5
26	95	30
27	95	35
28	92	30
29	90	35
30	88	30
31	88	35
32	87	30
33	85	25
34	85	35
35	67	85
36	65	85
37	65	82
38	62	80
39	60	80
40	60	85
41	58	75
42	55	80
43	55	85
44	55	82
45	20	82
46	18	80
47	2	45
48	42	5
49	42	12
50	72	35
51	55	20
52	25	30
53	20	50
54	55	60
55	30	60
56	50	35
57	30	25
58	15	10
59	10	20
60	15	60
61	45	65
62	65	35
63	65	20
64	45	30
65	35	40
66	41	37
67	64	42
68	40	60
69	31	52
70	35	69
71	65	55
72	63	65
73	2	60
74	20	20
75	5	5
76	60	12
77	23	3
78	8	56
79	6	68
80	47	47
81	49	58
82	27	43
83	37	31
84	57	29
85	63	23
86	21	24
87	12	24
88	24	58
89	67	5
90	37	47
91	49	42
92	53	43
93	61	52
94	57	48
95	56	37
96	55	54
97	4	18
98	26	52
99	26	35
100	31	67
101	31	67
102	4	18
'''


def fix_file(filename):
    output_filename = filename + ".tmp"
    with open(filename) as file_to_fix,\
            open(output_filename, 'w') as output_file:
        current_line = file_to_fix.readline()

        while current_line != "NODE_COORD_SECTION:\n":
            output_file.write(current_line)
            current_line = file_to_fix.readline()

        output_file.write(current_line)
        output_file.write(correct_coordinates)

        while current_line != "DEMAND_SECTION:\n":
            current_line = file_to_fix.readline()

        output_file.write(current_line)
        for line in file_to_fix.readlines():
            output_file.write(line)

    return output_filename


ROOT = "./DPDPTW-Instances/"
for directory in os.listdir(ROOT):
    for filename in os.listdir(ROOT + directory + "/"):
        if "lr205" in filename:
            fixed_filename = fix_file(ROOT + directory + "/" + filename)
            os.remove(ROOT + directory + "/" +  filename)
            os.rename(fixed_filename, ROOT + directory + "/" + filename)
