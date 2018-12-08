## simple-db
In-memory database implemented in Python

#### Usage
Start the program:

`python database.py`

You will be prompted for input:

`>>`

Enter commands [(supported commands)](#commands):

`set foo a`

To stop the program, enter the following command:

`end`

#### Supported Commands <a name="commands"></a>
* `set [name] [value]`
* `get [name]`
* `delete [name]`
* `count [value]`
* `end`
* `begin`
* `rollback`
* `commit`

#### Transactions
Transactions and nested transactions are supported, however `commit` will commit all current transactions, regardless of which transaction it is called from.