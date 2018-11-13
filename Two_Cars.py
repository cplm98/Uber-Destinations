import networkx as nx
import numpy as np
from Graph_Class import Graph
import pandas



def read_requests():
    colnames = ['time_stamp', 'source', 'dest']
    data = pandas.read_csv(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\requests.csv', names=colnames)
    time_stamps = data.time_stamp.tolist()
    source_nodes = data.source.tolist()
    dest_nodes = data.dest.tolist()
    return time_stamps, source_nodes, dest_nodes


# sends car to next source, updating car fields
def send_car(car, index):
    # time taken to get to next source node for pick up
    getting_to_source = nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[index]-1)
    # time taken from pick up to drop off
    getting_to_dest = nx.dijkstra_path_length(graph, source_nodes[index]-1, dest_nodes[index]-1)
    # if the car is already on time or running late
    if car["next_available_time"] >= time_stamps[index]:
        # set last drop off to current drop off point
        car["last_drop_off"] = dest_nodes[request] - 1
        # wait time is equal to dispatched time plus time taken to get to pick up, minus the equest time
        wait_time = (car["next_available_time"] + getting_to_source) - time_stamps[index]
        wait_times.append(wait_time)
        wait_time = "wait time = " + str(wait_time)
        car["next_available_time"] += getting_to_source + getting_to_dest
        return wait_time
    else:
        # if it was available before request
        car["last_drop_off"] = dest_nodes[request] - 1
        # next available time would be the request time plus the getting to pick and getting to drop off
        car["next_available_time"] = time_stamps[index] + getting_to_source + getting_to_dest
        wait_times.append(getting_to_source)
    # car["last_drop_off"] = dest_nodes[index]




# so you're just gonna make your way through these requests, comparing the request time, to the previeous trip time, and your travel time
# to the next pick up and keep track of waiting times, next step implement second car
# have to keep track of where the cars are

time_stamps, source_nodes, dest_nodes = read_requests()

graph = Graph()

wait_times = []

# could you add memoization to this solution? Get rid of some of the djikstra calls?
car_one = {"last_drop_off": 0, "next_available_time": 0}
car_two = {"last_drop_off": 0, "next_available_time": 0}  # probably don't need busy if you have next available time

# Cars become available after drop off
# assume car just appears at first  request, then location is logged after that

for request in range(len(time_stamps)):

    # if they are both available or will become free at the same time
    if (car_one["next_available_time"] < time_stamps[request] and car_two["next_available_time"] < time_stamps[request]) or (car_one["next_available_time"] == car_two["next_available_time"]):
        # check which car is closer because they are both available
        # going to have to calculate and set that cars new "next_available_time"
        car_one_dist = nx.dijkstra_path_length(graph, car_one["last_drop_off"], source_nodes[request]-1)
        car_two_dist = nx.dijkstra_path_length(graph, car_two["last_drop_off"], source_nodes[request]-1)
        if car_one_dist == car_two_dist:
            # they are equal, you can't look into the future of the next request so send the first one
            # could also add functionality saying if the available time is behind enough that the next request has
            # already been made, then it could take that into account

            #for now just send car one by default
            send_car(car_one, request)

        # if car one is closer
        if car_one_dist < car_two_dist:
            # send car one, setting last drop off node to the dest of that request, and next available time to
            # its next available time + car_two_dist + travel_dist
            send_car(car_one, request)

        # if care two is closer
        if car_two_dist < car_one_dist:
            # send car two, setting last drop off node to the dest of that request, and next available time to
            # its next available time + car_two_dist + travel_dist
            send_car(car_two, request)

    elif car_one["next_available_time"] < time_stamps[request]:
        # send car one
        send_car(car_one, request)
    elif car_two["next_available_time"] < time_stamps[request]:
        # send car two
        send_car(car_two, request)

    elif car_two["next_available_time"] < car_one["next_available_time"]:
        send_car(car_two, request)
    elif car_one["next_available_time"] < car_two["next_available_time"]:
        send_car(car_one, request)
    # if neither are available check which one will be first and calculate wait time


print(wait_times)
print(len(wait_times))
avg_wait_time = sum(wait_times) / len(wait_times)
print("Avg wait times: ", avg_wait_time)





