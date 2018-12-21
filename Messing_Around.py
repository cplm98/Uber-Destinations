import networkx as nx
import numpy as np
from Graph_Class import Graph
import pandas

def read_requests():
    colnames = ['time_stamp', 'source', 'dest']
    data = pandas.read_csv(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\supplementpickups.csv', names=colnames)
    time_stamps = data.time_stamp.tolist()
    source_nodes = data.source.tolist()
    dest_nodes = data.dest.tolist()
    return time_stamps, source_nodes, dest_nodes

# sends car to next source, updating car fields
def send_car(car, index):
    car["count"] += 1
    # time taken to get to next source node for pick up
    getting_to_source = nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[index]-1)
    # time taken from pick up to drop off
    getting_to_dest = nx.dijkstra_path_length(graph, source_nodes[index]-1, dest_nodes[index]-1)
    # if the car is already on time or running late
    if car["next_available_time"] > time_stamps[index]:  # took out the equals cause I think its covered in the else anyways
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


def eta_calc(car, index):
    dist_to_next_source = nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[index]-1)
    eta = dist_to_next_source + car["next_available_time"]
    return eta


time_stamps, source_nodes, dest_nodes = read_requests()

graph = Graph()

wait_times = []

car_one = {"last_drop_off": 9, "next_available_time": 0, "count": 0}
car_two = {"last_drop_off": 0, "next_available_time": 0, "count": 0}

for request in range(len(time_stamps)):
    # calculate eta for each ca rand go from there, that would technically be the shortest possible wait times
    car_one_eta = eta_calc(car_one, request)
    car_two_eta = eta_calc(car_two, request)
    if car_one_eta == car_two_eta:
        send_car(car_one, request)
    elif car_one_eta < car_two_eta:
        send_car(car_one, request)
    else:
        # car_two_eta < car_one_eta so send car 2
        send_car(car_two, request)


# for some reason this shows 3 more minutes of wait time than the original one
# can't seem to drop it below 625 without knowing something about the next
# request, ask jonny about his code


print(wait_times)
print(len(wait_times))
avg_wait_time = sum(wait_times) / len(wait_times)
print("Avg wait times: ", avg_wait_time)
print("total waiting time: ", sum(wait_times))
print("Car one: ", car_one["count"])
print("car two: ", car_two["count"])


# print(sum(wait_times))
