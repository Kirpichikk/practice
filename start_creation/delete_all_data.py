from connection import Connection

conn = Connection()

#conn.eval("box.space.users:drop()")
conn.eval("box.space.cache1:truncate()")
conn.eval("box.space.cache2:truncate()")
#conn.eval("box.space.cache2:drop()")
#conn.eval("box.sequence.id_seq:drop()")