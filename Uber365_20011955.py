import numpy as np
import networkx as nx
import pandas


#******Written by Connor Moore, 15cpm@queensu.ca, 20011955*****#

###### HELPER FUNCTIONs ######

# Generate graph from matrix
def Graph():
    adj_mat = np.loadtxt(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\network.csv', delimiter=',')
    graph_ = nx.from_numpy_matrix(adj_mat, create_using=nx.MultiGraph)
    return graph_


# Read in the requests csv and return three lists, one for each column
def read_requests():
    colnames = ['time_stamp', 'source', 'dest']
    data = pandas.read_csv(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\requests.csv', names=colnames)
    time_stamps = data.time_stamp.tolist()
    source_nodes = data.source.tolist()
    dest_nodes = data.dest.tolist()
    return time_stamps, source_nodes, dest_nodes


# function that updates the cars attributes as well as calculating the wait time of each request
def send_car(car, index, getting_to_source):
    car["count"] += 1
    # memoized
    if (source_nodes[index]-1, dest_nodes[index]-1) in prev_trips:
        memoCount.append(1)
        # time taken from pick up to drop off
        getting_to_dest = prev_trips[(source_nodes[index]-1, dest_nodes[index]-1)]
    else:
        getting_to_dest = nx.dijkstra_path_length(graph, source_nodes[index]-1, dest_nodes[index]-1)
        prev_trips[(source_nodes[index]-1, dest_nodes[index]-1)] = getting_to_dest

    # if the car running late
    if car["next_available_time"] > time_stamps[index]:
        # set last drop off to current drop off point
        car["last_drop_off"] = dest_nodes[request] - 1
        # wait time is equal to dispatched time plus time taken to get to pick up, minus the request time
        wait_time = (car["next_available_time"] + getting_to_source) - time_stamps[index]
        wait_times.append(wait_time)
        # update the cars next available time by adding the length of the trip
        car["next_available_time"] += getting_to_source + getting_to_dest
        return wait_time
    else:
        # if it was available at or before request
        car["last_drop_off"] = dest_nodes[request] - 1
        # next available time would be the request time plus the getting to pick and getting to drop off
        car["next_available_time"] = time_stamps[index] + getting_to_source + getting_to_dest
        wait_times.append(getting_to_source)




###### MAIN ######


# Initialize Cars
car_one = {"last_drop_off": 0, "next_available_time": 0, "count": 0}
car_two = {"last_drop_off": 0, "next_available_time": 0, "count": 0}

memoCount = []

# Create Graph using graph class
graph = Graph()

wait_times = []
prev_trips = {}

# initialize lists using read_requests
time_stamps, source_nodes, dest_nodes = read_requests()

# iterate all requests
for request in range(len(time_stamps)):

# what if you did for all indexes with the same request value
   #memoize
    if (car_one["last_drop_off"], source_nodes[request]-1) in prev_trips:
        memoCount.append(1)
        # car one's distance to the next request
        car_one_dist = prev_trips[(car_one["last_drop_off"], source_nodes[request]-1)]
    else:
        car_one_dist = nx.dijkstra_path_length(graph, car_one["last_drop_off"], source_nodes[request]-1)
        prev_trips[(car_one["last_drop_off"], source_nodes[request]-1, car_one_dist)] = car_one_dist

    if (car_two["last_drop_off"], source_nodes[request]-1) in prev_trips:
        memoCount.append(1)
         # car two's distance to the next request
        car_two_dist = prev_trips[(car_two["last_drop_off"], source_nodes[request]-1)]
    else:
        car_two_dist = nx.dijkstra_path_length(graph, car_two["last_drop_off"], source_nodes[request]-1)
        prev_trips[(car_two["last_drop_off"], source_nodes[request]-1)] = car_two_dist

    # car one and two's proposed time of arrival
    car_one_eta = car_one["next_available_time"] + car_one_dist
    car_two_eta = car_two["next_available_time"] + car_two_dist

    # if they are both available or will be available at the same time
    if car_one["next_available_time"] < time_stamps[request] and car_two["next_available_time"] < time_stamps[request]: #or car_one["next_available_time"] == car_two["next_available_time"]:
        # who is closest
        if car_one_dist < car_two_dist:
            send_car(car_one, request, car_one_dist)
        elif car_two_dist < car_one_dist:
            send_car(car_two, request, car_two_dist)
        else:
            send_car(car_two, request, car_two_dist)
    # else who would get there first if they aren't both available
    elif car_one_eta < car_two_eta:
        send_car(car_one, request, car_one_dist)
    elif car_two_eta < car_one_eta:
        send_car(car_two, request, car_two_dist)
    else:
        send_car(car_one, request, car_one_dist)


print(wait_times)
print(len(wait_times))
avg_wait_time = sum(wait_times) / len(wait_times)
print("Avg wait times: ", avg_wait_time)
print("total waiting time: ", sum(wait_times))
print("Car one: ", car_one["count"])
print("car two: ", car_two["count"])
print("memocount", len(memoCount))








