class Message:
    def __init__(self, message: str, role: str):
        self.message = message
        self.role = role

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"{self.role}: {self.message}"

    def __eq__(self, other):
        return self.message == other.message and self.role == other.role
