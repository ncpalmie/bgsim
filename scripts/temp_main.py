import ray, time
from t_client import Client
from datetime import datetime
ray.init()


# Create an actor process.
clients = []
for i in range(6):
    c = Client.remote(True)
    clients.append(c)
c = Client.remote(False)
clients.append(c)

# Check the actor's counter value.
for c in clients:
    print(ray.get(c.get_status.remote()))  # 0
    c.ready_up.remote("Ready at ")

# Increment the counter twice and check the value again.
for c in clients:
    print(ray.get(c.get_status.remote()))  # 2
