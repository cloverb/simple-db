class Database:
    """In memory database"""

    operations = {
        'GET': (1, lambda db, name: print(db.get(name) if db.get(name) is not None else 'NULL')),
        'SET': (2, lambda db, name, value: db.set(name, value)),
        'DELETE': (1, lambda db, name: db.delete(name)),
        'COUNT': (1, lambda db, value: print(db.count(value))),
        'BEGIN': (0, lambda db: db.begin_transaction()),
        'ROLLBACK': (0, lambda db: print('TRANSACTION NOT FOUND') if not db.is_transaction else db.rollback()),
        'COMMIT': (0, lambda db: db.commit()),
        'END': (0, lambda db: exit())
    }

    def __init__(self):
        self.db = {}
        self.counts = {}
        self.transactions = []
        self.is_transaction = False
        self.is_rollback = False

    def get(self, name):
        """Get value for key in the database"""
        return self.db.get(name, None)

    def set(self, name, value):
        """Set a key/value pair in the database"""
        previous_value = self.db.get(name, None)
        if previous_value == value:
            return
        self.db[name] = value
        self.counts[value] = self.counts.get(value, 0) + 1
        if previous_value is not None:
            self.counts[previous_value] -= 1
        if self.is_transaction and not self.is_rollback:
            self.transactions[-1].append((name, previous_value))

    def delete(self, name):
        """Delete a key/value pair from the database"""
        if name in self.db:
            value = self.db.get(name)
            del self.db[name]
            self.counts[value] -= 1
            if self.is_transaction and not self.is_rollback:
                self.transactions[-1].append((name, value))

    def count(self, value):
        """Get the count of a value in the database"""
        return self.counts.get(value, 0)

    def begin_transaction(self):
        """Open a transaction"""
        self.transactions.append([])
        self.is_transaction = True

    def rollback(self):
        """Rollback changes from most recent transaction"""
        self.is_rollback = True
        history = self.transactions.pop()
        while history:
            name, value = history.pop()
            self.delete(name) if value is None else self.set(name, value)
        self.is_rollback = False
        if not self.transactions:
            self.is_transaction = False

    def commit(self):
        """Commit all current transactions"""
        self.transactions.clear()
        self.is_transaction = False

    def apply(self, command):
        """Apply a command to the database"""
        command = command.split()
        operation = command.pop(0).upper() if command else None
        if operation not in self.operations or len(command) != self.operations[operation][0]:
            print('INVALID COMMAND')
        else:
            self.operations[operation][1](self, *command)
        return True


def start():
    """Start database and take user commands"""
    database = Database()
    while database.apply(input('>>')):
        pass


start()
