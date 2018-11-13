import networkx as nx
import numpy as np
from Graph_Class import Graph
import pandas

# okay there is something going wrong somewhere because the times aren't adding up
# I think it must be in my send car function

def read_requests():
    colnames = ['time_stamp', 'source', 'dest']
    data = pandas.read_csv(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\requests_sample.csv', names=colnames)
    time_stamps = data.time_stamp.tolist()
    source_nodes = data.source.tolist()
    dest_nodes = data.dest.tolist()
    return time_stamps, source_nodes, dest_nodes


def send_car(car, index):
    getting_to_source = nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[index]-1)
    getting_to_dest = nx.dijkstra_path_length(graph, source_nodes[index]-1, dest_nodes[index]-1)
    # if the car is already ontime or running late
    if car["next_available_time"] >= time_stamps[index]:
        car["last_drop_off"] = dest_nodes[request] - 1
        wait_time = (car["next_available_time"] + getting_to_source) - time_stamps[index]
        wait_times.append(wait_time)
        wait_time = "wait time = " + str(wait_time)
        car["next_available_time"] += getting_to_source + getting_to_dest
        return wait_time
    else:
        # if it was available before request
        car["last_drop_off"] = dest_nodes[request] - 1
        car["next_available_time"] = time_stamps[index] + getting_to_source + getting_to_dest
        wait_times.append(0)
        return "wait time = 0.0"
    car["last_drop_off"] = dest_nodes[index]


time_stamps, source_nodes, dest_nodes = read_requests()

graph = Graph()

wait_times = []

car_one = {"busy": 0, "last_drop_off": 0, "next_available_time": 0}

for request in range(len(time_stamps)):
    dist_to_dest = nx.dijkstra_path_length(graph, source_nodes[request]-1, dest_nodes[request]-1)
    dist_to_next_source = nx.dijkstra_path_length(graph, dest_nodes[request]-1, source_nodes[request+1]-1)
    print("distance to destination", dist_to_dest)
    print("distance to next source", dist_to_next_source)
    send_car(car_one, request)

avg_wait_time = sum(wait_times) / len(wait_times)
print("Avg wait times: ", avg_wait_time)
