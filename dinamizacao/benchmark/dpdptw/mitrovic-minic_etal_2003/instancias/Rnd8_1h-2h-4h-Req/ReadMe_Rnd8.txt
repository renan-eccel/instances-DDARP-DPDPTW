The Rnd8 Instances of the Dynamic Pickup and Delivery Problem with Time Windows
===============================================================================

The Rnd8 instances is the first set of instances used in the empirical study 
which is reported in paper: 
Snezana Mitrovic-Minic and Gilbert Laporte, in press, "Double-horizon based 
heuristics for the dynamic pickup and delivery problem with time windows", 
Transportation Research B. 


The problem 
...........

The Pickup and Delivery Problem with Time Windows (PDPTW) consists of determining 
optimal routes for a fleet of vehicles in order to serve transportation requests. 
The transportation request is defined by a pickup location and a delivery location.
(The load is assumed to be zero, i.e., there are no capacity constraints.) Each 
stop location has to be served within a given time window. However, if a vehicle 
arrives too early at a location, it is allowed to wait. Distance between two 
locations is equal to the corresponding Euclidean distance. Each request must 
be served entirely by one vehicle (pairing constraints), and each pickup location 
has to be served before its corresponding delivery location (precedence constraints). 
The objective is to minimize total route length, i.e., the sum of the distances 
travelled by all the vehicles.  
The dynamic PDPTW arises when not all requests are known in advance. 


The instances
.............

This set of instances contains 90 instances with 100, 500 and 1000 requests. There 
are 30 instances for each problem size. 
Service period is 10 hours. Service area is 60 km x 60 km, with few delivery locations
(around 6%) out of the area. (The locations out of the area have negative coordinates.) 
Vehicle speed is 60km/h. Service time at each location is 0. The depot is located at 
(20km, 30km). 


Time windows
............

Time windows are generated such that their distribution emulate real-world requests
based on data collected in two medium-to-large courier companies in Vancouver: 
around 28% of requests are 1-hour requests, 
around 30% of requests are 2-hour requests and 
around 42% of requests are 4-hour requests. 
(The k-hour request means that the entire request has to be served within k hours 
from the starting of the pickup time window.) 
Since the service period is 10 hours, 
the 1h-requests are generated within first 9 hours,
the 2h-requests are generated within first 8 hours, and 
the 4h-requests are generated within first 6 hours. 
The start of each pickup time window is equal to the `time-in', the time when the 
request became known. The end of the delivery time window is determined by the request type. 


Location positions
..................

Positions of pickup and delivery locations of one request are randomly generated such 
that direct travel time between the two locations is 
at most 30 minutes for 1-hour requests, 
at most 90 minutes for 2-hour requests, and
at most 180 minutes for 4-hour requests. 
Also the total travel time (depot, pickup location, delivery location) is 
at most 45 minutes for 1-hour requests, 
at most 105 minutes for 2-hour requests, and
at most 210 minutes for 4-hour requests. 


Time-in
.......

Requests appear uniformly during the whole service period. None of the requests is 
known in advance.  
 

Fields in each data file
........................

Each file is a text file consisting of a heading and set of lines. Each line contains
information about one request. 

Heading consists of: 

<empty line> 
<file name> 
<empty line> 
"Number of requests is "<number of requests in the file> 
<empty line> 
"Req no. Time-in Pickup location                  Delivery location"
"                Ser.t.   (x,     y)    Time win. Ser.t.   (x,     y)    Time win."


Fields are as follows: 
"Req no." is the request number. "Time-in" is the time when request become known. 
"Ser.t" is the service time at a location. 
"(x,y)" are the location coordinates, and "Time win." is the location time window. 



Units
.....

Time is stored in minutes and it is an integer from interval [0, 600]. 
The locations are stored in kilometers with one digit after the decimal point.



