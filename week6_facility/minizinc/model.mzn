% robert sparks naive facility location problem in minizinc

% variables
int num_facilities = 3;
int num_customers = 4;

var 1..num_facilities: facilities;
var 1..num_customers: customers;

array[1..num_facilities] of int: setup_cost = [100, 100, 100];
array[1..num_facilities] of int: capacity = [100, 100, 500];
array[1..num_customers] of int: demand = [50, 50, 75, 75];

array[1..num_facilities, 1..num_customers] of int: costs = 
  array2d(1..num_facilities, 1..num_customers, [
	470, 471, 472, 677
	474, 475, 477, 673
	1976, 1977, 1978, 829]);

% is this facility open?
array[1..num_facilities] of var 0..1: open;
% what facility for each customer
array[1..num_facilities, 1..num_customers] of var 0..1: c_to_f;
% total cost
var 0..3000: tot_cost;

% solve minimize tot_cost;
solve :: int_search(
	open ++ [c_to_f[i, j] | i in 1..num_facilities, j in 1..num_customers],
	smallest,
	indomain_split,
	complete)
	minimize tot_cost;

constraint
	% facility demand not exceeded
	forall(j in 1..num_customers) (
	  sum(i in 1..num_facilities) (open[i]*c_to_f[i, j]) <= demand[j]
	)

	/\ % connect open with c_to_f

