import ray, time
from client import Client
from datetime import datetime
ray.init()

@ray.remote
class Client(object):
    def __init__(self, ai):
        self.x = 0
        self.status = 'Unready'
        self.ai = ai
    
    def inc(self):
        self.x += 1
    
    def get_value(self):
        return self.x

    def ready_up(self, string):
        if self.ai:
            time.sleep(2)
            self.status = string + str(datetime.now())
        else:
            input()
            self.status = string + str(datetime.now())

    def get_status(self):
        return self.status

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
