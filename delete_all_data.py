import tarantool
from connection import Connection

conn = Connection()

conn.eval("box.space.users:drop()")
conn.eval("box.sequence.id_seq:drop()")