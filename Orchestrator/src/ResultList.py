class ResultList:
    def __init__(self):
        self.items = []

    def append(self, clientId, distance, isHit, workItemId):
        # Add a tuple (clientId, x, y, z) to the list
        self.items.append((clientId, distance, isHit, workItemId))

    def remove(self, clientId, workItemId):
        # Remove the first occurrence of the item with the specified clientId
        for i, item in enumerate(self.items):
            if item[0] == clientId and item[3] == workItemId:
                del self.items[i]
                return

    def remove_all_from_client(self, clientId):
        # Remove the first occurrence of the item with the specified clientId
        for i, item in enumerate(self.items):
            if item[0] == clientId:
                del self.items[i]
                return

    def size(self):
        return len(self.items)

    def get(self, clientId, workItemId):
        # Get the item with the specified clientId
        for item in self.items:
            if item[0] == clientId and item[3] == workItemId:
                return item
        return None

    def size(self):
        # Return the number of items in the list
        return len(self.items)

    def __str__(self):
        # Return a string representation of the list
        return str(self.items)