|K| n T Q L
i x_i y_i d_i q_i pt_i dt_i
.
.
.


where:
|K|: number of vehicles
n: number of requests
T: maximum route duration
Q: vehicles capacity
L: maximum ride time   

i: pickup id for request i
x_i: x coordinate for pickup i
y_i: y coordinate for pickup i
d_i: pickup service duration
q_i: load
pt_i: lower pickup time window
dt_i: upper pickup time window

i+n: delivery id for request i
x_{i+n}: x coordinate for delivery i
y_{i+n}: y coordinate for delivery i
d_{i+n}: delivery service duration
q_{i+n}: load
pt_{i+n}: lower delivery time window
dt_{i+n}: upper delivery time window

c_{ij} = t_{ij} = EuclideanDistance(i,j)

More Information {
	2006_cordeau,
	2007_ropke
}
