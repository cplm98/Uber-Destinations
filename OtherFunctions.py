import pandas
import networkx as nx


def read_requests():
    colnames = ['time_stamp', 'source', 'dest']
    data = pandas.read_csv(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\requests.csv', names=colnames)
    time_stamps = data.time_stamp.tolist()
    source_nodes = data.source.tolist()
    dest_nodes = data.dest.tolist()
    return time_stamps, source_nodes, dest_nodes


def send_car(car, index):
    car["count"] += 1
    # time taken to get to next source node for pick up
    getting_to_source = nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[index]-1)
    # time taken from pick up to drop off
    getting_to_dest = nx.dijkstra_path_length(graph, source_nodes[index]-1, dest_nodes[index]-1)
    # if the car is already on time or running late
    if car["next_available_time"] > time_stamps[index]: # took out the equals cause I think its covered in the else anyways
        # set last drop off to current drop off point
        car["last_drop_off"] = dest_nodes[request] - 1
        # wait time is equal to dispatched time plus time taken to get to pick up, minus the request time
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
