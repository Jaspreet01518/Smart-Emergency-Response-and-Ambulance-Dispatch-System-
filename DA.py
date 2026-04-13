import tkinter as tk
from tkinter import ttk, messagebox
import heapq

ambulances = [
    ("Ambulance 1", 10),
    ("Ambulance 2", 5),
    ("Ambulance 3", 8)
]

emergency_requests = []

# ---------------- QUICK SORT ----------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr)//2][1]

    left = [x for x in arr if x[1] < pivot]
    middle = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]

    return quick_sort(left) + middle + quick_sort(right)

# ---------------- MERGE SORT ----------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ---------------- DIJKSTRA ----------------
graph = {
    "Hospital": {"Sector 17": 4, "Sector 22": 2},
    "Sector 17": {"Hospital": 4, "Patient": 6},
    "Sector 22": {"Hospital": 2, "Patient": 3},
    "Patient": {"Sector 17": 6, "Sector 22": 3}
}

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous

def get_path(previous, node):
    path = []
    while node:
        path.append(node)
        node = previous[node]
    return path[::-1]

# ---------------- KNAPSACK ----------------
def knapsack(weights, values, capacity):
    n = len(values)
    dp = [[0]*(capacity+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for w in range(capacity+1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]

# ---------------- FUNCTIONS ----------------
def save_request():
    patient = patient_entry.get()
    location = location_var.get()
    emergency = emergency_var.get()

    if patient == "":
        messagebox.showerror("Error", "Enter Patient Name")
        return

    # Save in list instead of DB
    emergency_requests.append((patient, location, emergency))

    messagebox.showinfo("Saved", "Emergency Request Saved Successfully")

def find_ambulance():
    output.delete("1.0", tk.END)

    sorted_ambulances = quick_sort(ambulances)
    nearest = sorted_ambulances[0]

    output.insert(tk.END, "Nearest Ambulance\n\n")
    output.insert(tk.END, f"{nearest[0]} - {nearest[1]} km\n\n")

    output.insert(tk.END, "All Ambulances After Sorting\n")
    for amb in sorted_ambulances:
        output.insert(tk.END, f"{amb[0]} : {amb[1]} km\n")

def shortest_route():
    output.delete("1.0", tk.END)

    distances, previous = dijkstra(graph, "Hospital")
    path = get_path(previous, "Patient")

    output.insert(tk.END, "Shortest Route\n\n")
    output.insert(tk.END, " -> ".join(path))
    output.insert(tk.END, f"\nDistance = {distances['Patient']} km")

def hospital_sort():
    output.delete("1.0", tk.END)

    hospitals = ["City Hospital", "Apollo Hospital", "Civil Hospital", "Fortis Hospital"]
    sorted_hospitals = merge_sort(hospitals)

    output.insert(tk.END, "Hospitals After Merge Sort\n\n")
    for h in sorted_hospitals:
        output.insert(tk.END, h + "\n")

def select_items():
    output.delete("1.0", tk.END)

    items = ["Oxygen Cylinder", "First Aid Kit", "Injection Kit"]
    weights = [5, 3, 2]
    values = [10, 8, 6]

    result = knapsack(weights, values, 7)

    output.insert(tk.END, "Medical Item Selection\n\n")
    for i in range(len(items)):
        output.insert(tk.END, f"{items[i]}  Weight={weights[i]}  Value={values[i]}\n")

    output.insert(tk.END, f"\nMaximum Importance Value = {result}")

def clear_all():
    patient_entry.delete(0, tk.END)
    location_var.set("Sector 22")
    emergency_var.set("Heart Attack")
    output.delete("1.0", tk.END)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Smart Emergency Response System")
root.geometry("1000x700")
root.configure(bg="#e6f2ff")

heading = tk.Label(root, text="Smart Emergency Response and Ambulance Dispatch System",
                   font=("Arial", 20, "bold"), bg="#e6f2ff", fg="darkblue")
heading.pack(pady=10)

form = tk.Frame(root, bg="#e6f2ff")
form.pack(pady=10)

tk.Label(form, text="Patient Name:", bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=5)
patient_entry = tk.Entry(form, width=25)
patient_entry.grid(row=0, column=1)

tk.Label(form, text="Location:", bg="#e6f2ff").grid(row=1, column=0)
location_var = tk.StringVar(value="Sector 22")
ttk.Combobox(form, textvariable=location_var, values=["Sector 17", "Sector 22"]).grid(row=1, column=1)

tk.Label(form, text="Emergency Type:", bg="#e6f2ff").grid(row=2, column=0)
emergency_var = tk.StringVar(value="Heart Attack")
ttk.Combobox(form, textvariable=emergency_var,
             values=["Heart Attack", "Accident", "Fire", "Other"]).grid(row=2, column=1)

btn_frame = tk.Frame(root, bg="#e6f2ff")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Save Request", width=20, command=save_request, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Find Ambulance", width=20, command=find_ambulance, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Shortest Route", width=20, command=shortest_route, bg="#9C27B0", fg="white").grid(row=1, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Sort Hospitals", width=20, command=hospital_sort, bg="#FF9800", fg="white").grid(row=1, column=1, padx=10)
tk.Button(btn_frame, text="Medical Items", width=20, command=select_items, bg="#F44336", fg="white").grid(row=2, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Clear", width=20, command=clear_all, bg="#607D8B", fg="white").grid(row=2, column=1, padx=10, pady=10)

output = tk.Text(root, width=100, height=20)
output.pack(pady=20)

root.mainloop()