import heapq
import streamlit as st # type: ignore

class MetroSystem:
    def __init__(self):
        self.graph = {}

    # Add station
    def add_station(self, station_name):
        if station_name not in self.graph:
            self.graph[station_name] = {}

    # Add route between stations
    def add_route(self, start, end, distance):
        if start in self.graph and end in self.graph:
            self.graph[start][end] = distance
            self.graph[end][start] = distance

    # Dijkstra's algorithm for shortest path
    def dijkstra(self, start, end):
        pq = [(0, start)]
        visited = set()
        distances = {station: float('inf') for station in self.graph}
        distances[start] = 0

        while pq:
            curr_dist, curr_station = heapq.heappop(pq)
            if curr_station in visited:
                continue
            visited.add(curr_station)

            for neighbor, weight in self.graph[curr_station].items():
                distance = curr_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances[end] if distances[end] != float('inf') else -1

    # Book ticket
    def book_ticket(self, source, destination):
        if source not in self.graph or destination not in self.graph:
            return "Invalid stations!"
        
        fare = self.dijkstra(source, destination) * 2  # Fare: 2 units per distance
        if fare == -1:
            return "No route available between the stations."
        else:
            return f"Ticket booked! Fare: {fare}"

# Initialize the Metro System
metro = MetroSystem()
metro.add_station("Station A")
metro.add_station("Station B")
metro.add_station("Station C")
metro.add_station("Station D")

metro.add_route("Station A", "Station B", 5)
metro.add_route("Station B", "Station C", 7)
metro.add_route("Station C", "Station D", 4)
metro.add_route("Station A", "Station C", 10)

# Streamlit UI for interaction
st.title("Metro Ticket Booking System")

# User ticket booking
source_station = st.selectbox("Select source station", metro.graph.keys())
destination_station = st.selectbox("Select destination station", metro.graph.keys())
if st.button("Book Ticket"):
    ticket_response = metro.book_ticket(source_station, destination_station)
    st.write(ticket_response)
