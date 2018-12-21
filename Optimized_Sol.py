import networkx as nx
import numpy as np
from Graph_Class import Graph
import pandas

graph = Graph()
#weights = nx.floyd_warshall(graph)
wait_times = []


# okay so move the append for completed into the send car function so you only have to write it once
# it's coming together just keep finishing the cases, also gonna have to add a case that it keeps going until
# curr_requests is empty. Maybe a safe guard saying don't let something stay in curr requests for too long.

def send_car(car, index):
    car["count"] += 1
    # time taken to get to next source node for pick up
    getting_to_source = nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[index]-1)
    # time taken from pick up to drop off
    getting_to_dest = nx.dijkstra_path_length(graph, source_nodes[index]-1, dest_nodes[index]-1)
    # if the car is already on time or running late
    if car["next_available_time"] > time_stamps[index]: # took out the equals cause I think its covered in the else anyways
        # set last drop off to current drop off point
        car["last_drop_off"] = dest_nodes[index] - 1
        # wait time is equal to dispatched time plus time taken to get to pick up, minus the equest time
        wait_time = (car["next_available_time"] + getting_to_source) - time_stamps[index]
        wait_times.append(wait_time)
        wait_time = "wait time = " + str(wait_time)
        car["next_available_time"] += getting_to_source + getting_to_dest
        completed.append(index)
        print("should pop1: ", index)
        curr_requests.pop(curr_requests.index(index))
        return wait_time
    else:
        # if it was available before request
        car["last_drop_off"] = dest_nodes[index] - 1
        # next available time would be the request time plus the getting to pick and getting to drop off
        car["next_available_time"] = time_stamps[index] + getting_to_source + getting_to_dest
        wait_times.append(getting_to_source)
        completed.append(index)
        print("should pop2: ", index)
        curr_requests.pop(curr_requests.index(index))



def read_requests():
    colnames = ['time_stamp', 'source', 'dest']
    data = pandas.read_csv(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\requests.csv', names=colnames)
    time_stamps = data.time_stamp.tolist()
    source_nodes = data.source.tolist()
    dest_nodes = data.dest.tolist()
    return time_stamps, source_nodes, dest_nodes


def val_less_than(list, val): # this should only happen if
    templist = []
    for index, item in enumerate(list):
        if item <= val:
            templist.append(index)
    return max(templist)

def optimize_route(list, car): # list of indexes
    # send car to whichever one is decided should be done first
    lengths = []
    for request in list:
        lengths.append(nx.dijkstra_path_length(graph, car["last_drop_off"], source_nodes[request]-1))
    shortest = lengths.index(min(lengths))  #index of shortest path
    length = lengths[shortest]  # so should be returning the index to of the shortest next trip
    return shortest, length
        # maybe just have it return an index and a length


        # append the absolute index of the request to completed, start using the actual indexes of the request
        # because they can't be duplicated


time_stamps, source_nodes, dest_nodes = read_requests()
curr_requests = []
temp_curr_requests = []
completed = []

# class Car:
#     def __init__(self):
#         self.loc = 0
#         self.free = 0

car_one = {"last_drop_off": 1, "next_available_time": 10, "count": 0}
car_two = {"last_drop_off": 1, "next_available_time": 10, "count": 0}

# car_one = Car()
# car_two = Car()

for request in time_stamps:
    #curr_requests.append(time_stamps.index(request)) # add request to active requests
    request_index = time_stamps.index(request)
    if request_index > 55:
        break
    print("request index: ", request_index)
    min_free = min(car_one["next_available_time"], car_two["next_available_time"])# earliest next available car
    closest_val = val_less_than(time_stamps, min_free)
    if closest_val < request_index:
        closest_val = request_index
    print(closest_val) # this is zero cause or equal
    #temp_curr_requests = time_stamps[request_index:closest_val+1] # this is value not index, need to make it index
    r = range(request_index, closest_val+1)
    temp_curr_requests = [*r]
    print("temp_curr_requests:", temp_curr_requests)
    print("completed: ", completed)
    for i in temp_curr_requests:
        if i not in completed:
            curr_requests.append(i)
    print("current requests: ", curr_requests)
    # by here current requests should always have at least 1 element in it
    # if there are multiple requests to choose from
    if len(curr_requests) > 1:
        print("hello")
        # if the car was early would this even apply?
        index1, length1 = optimize_route(curr_requests, car_one)
        print("index1: ", index1)
        index2, length2 = optimize_route(curr_requests, car_two)
        print("index2: ", index2)
        if car_one["next_available_time"] < time_stamps[request_index] and car_two["next_available_time"] < time_stamps[request_index] or car_one["next_available_time"] == car_two["next_available_time"]:
            print("im here")
            if length1 <= length2:
                print("now here")
                send_car(car_one, curr_requests[index1])
            elif length1 > length2:
                send_car(car_two, curr_requests[index2])

        elif car_one["next_available_time"] < time_stamps[request_index]:
            send_car(car_one, curr_requests[index1])

        elif car_two["next_available_time"] < time_stamps[request_index]:
            send_car(car_two, curr_requests[index2])

        elif car_two["next_available_time"] < car_one["next_available_time"]:
            send_car(car_two, curr_requests[index2])
        elif car_one["next_available_time"] < car_two["next_available_time"]:
            send_car(car_one, curr_requests[index1])
    else:
        # just send whatever car is closest/ available soonest
        if (car_one["next_available_time"] < time_stamps[request_index] and car_two["next_available_time"] < time_stamps[request_index]) or (car_one["next_available_time"] == car_two["next_available_time"]):
            # check which car is closer because they are both available
            # going to have to calculate and set that cars new "next_available_time"
            car_one_dist = nx.dijkstra_path_length(graph, car_one["last_drop_off"], source_nodes[request_index]-1)
            car_two_dist = nx.dijkstra_path_length(graph, car_two["last_drop_off"], source_nodes[request_index]-1)
            if car_one_dist == car_two_dist:
                # they are equal, you can't look into the future of the next request so send the first one
                # could also add functionality saying if the available time is behind enough that the next request has
                # already been made, then it could take that into account

                #for now just send car one by default
                send_car(car_one, curr_requests[0])

            # if car one is closer
            if car_one_dist < car_two_dist:
                # send car one, setting last drop off node to the dest of that request, and next available time to
                # its next available time + car_two_dist + travel_dist
                send_car(car_one, curr_requests[0])

            # if care two is closer
            if car_two_dist < car_one_dist:
                # send car two, setting last drop off node to the dest of that request, and next available time to
                # its next available time + car_two_dist + travel_dist
                send_car(car_two, curr_requests[0])

        elif car_one["next_available_time"] < time_stamps[request_index]:
            # send car one
            send_car(car_one, curr_requests[0])
        elif car_two["next_available_time"] < time_stamps[request_index]:
            # send car two
            send_car(car_two, request_index)

        elif car_two["next_available_time"] < car_one["next_available_time"]:
            send_car(car_two, curr_requests[0])
        elif car_one["next_available_time"] < car_two["next_available_time"]:
            send_car(car_one, curr_requests[0])
    time_stamps[request_index] = -1

print("final completed: ", completed)
print(wait_times)
print(len(wait_times))
avg_wait_time = sum(wait_times) / len(wait_times)
print("Avg wait times: ", avg_wait_time)
print("total waiting time: ", sum(wait_times))
print("Car one: ", car_one["count"])
print("car two: ", car_two["count"])




