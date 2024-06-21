import json

class FileStorage:
    @staticmethod
    def save(data, filename):
        with open(filename, 'a') as file:
            file.write(json.dumps(data) + "\n")

    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            return [json.loads(line) for line in file]

