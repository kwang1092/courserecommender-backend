from threading import Thread
from Queue import Queue, Empty
import mysql.connector


class DbThread(Thread):
  def __init__(self, connection_pool, input_queue, queue_timeout=0.5):
    super(DbThread, self).__init__()
    self.connection_pool = connection_pool
    self.input_queue = input_queue
    self.queue_timeout = queue_timeout


class WriterThread(DbThread):
  def __init__(self, connection_pool, input_queue, table, queue_timeout=0.5):
    super(WriterThread, self).__init__(connection_pool, input_queue,
                                       queue_timeout=queue_timeout)
    self.table = table

  def run(self):
    # Create query in the format:
    #   "INSERT INTO salaries (emp_no, salary, from_date, to_date)
    #     VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)"
    # data is dictionary such as {'emp_no': 1, 'salary': 2, ...}
    while not self.input_queue.empty():
      connection = self.connection_pool.get()
      cursor = connection.cursor()
      try:
        # A thread may enter the loop, but another thread could pluck the
        # last item. This timeout is to prevent a thread from waiting for
        # another item that will never come.
        data = self.input_queue.get(timeout=self.queue_timeout)
      except Empty:
        self.connection_pool.put(connection)
        break
      placeholder_values_array = ['%({})s'.format(col) for col in data.keys()]
      insert_query = "INSERT INTO {} ({}) VALUES ({})" \
        .format(self.table, ', '.join(data.keys()),
                ', '.join(placeholder_values_array))
      cursor.execute(insert_query, data)
      connection.commit()
      self.input_queue.task_done()
      self.connection_pool.put(connection)

class ReaderThread(DbThread):
  def __init__(self, connection_pool, input_queue,
               result_queue, queue_timeout=0.5):
    super(ReaderThread, self).__init__(connection_pool, input_queue,
                                       queue_timeout=queue_timeout)
    self.result_queue = result_queue

  def run(self):
    while not self.input_queue.empty():
      connection = self.connection_pool.get()
      cursor = connection.cursor(dictionary=True)
      try:
        query = self.input_queue.get(timeout=self.queue_timeout)
      except Empty:
        self.connection_pool.put(connection)
        break
      cursor.execute(query)
      result = []
      for row in cursor:
        result.append(row)
      self.input_queue.task_done()
      if result:
        self.result_queue.put(result)
      connection.commit()
      self.connection_pool.put(connection)


class MySQLConnector(object):
  def __init__(self, user, password, host, database,
               num_connections=10, num_threads=10):
    self.config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database
    }
    self.connection_pool = Queue()
    self.num_connections = num_connections
    self.num_threads = num_threads
    for _ in range(num_connections):
      cnx = mysql.connector.connect(**self.config)
      self.connection_pool.put(cnx)

  def close(self):
    while not self.connection_pool.empty():
      connection = self.connection_pool.get()
      connection.close()

  def scale_connection_pool(self, num_connections):
    """
      Alters the connection pool to have `num_connections` of connections in the
      pool. Note `num_connections` must be a positive integer.
    """
    assert num_connections > 0, "`num_connections` must be a positive integer"
    if self.num_connections < num_connections:
      # Scale up
      for _ in range(num_connections - self.num_connections):
        cnx = mysql.connector.connect(**self.config)
        self.connection_pool.put(cnx)
    elif self.num_connections > num_connections:
      # Scale down
      for _ in range(self.num_connections - num_connections):
        connection = self.connection_pool.get()
        connection.close()
    self.num_connections = num_connections

  def read_batch(self, table, start=0, end=None, interval_size=10):
    assert end is None or start <= end
    input_queue = Queue()
    result_queue = Queue()
    a = start
    if end is None:
      end = self.get_count(table)
    while a <= end:
      b = a + interval_size
      read_query = "SELECT * FROM {} LIMIT {} OFFSET {}" \
                     .format(table, b-a, a)
      input_queue.put(read_query)
      a += interval_size
    for _ in range(self.num_threads):
      ReaderThread(self.connection_pool, input_queue, result_queue).start()
    input_queue.join()
    rows = []
    while not result_queue.empty():
      rows.extend(result_queue.get())
    return rows

  def get_count(self, table):
    connection = self.connection_pool.get()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table))
    result = []
    for row in cursor:
      result.append(row)
    self.connection_pool.put(connection)
    return result[0][0]

  def write_batch(self, table, rows):
    input_queue = Queue()
    for row in rows:
      input_queue.put(row)
    for _ in range(self.num_threads):
      WriterThread(self.connection_pool, input_queue, table).start()
    input_queue.join()

  def execute_batch(self, queries):
    input_queue = Queue()
    result_queue = Queue()
    for q in queries:
      input_queue.put(q)
    for _ in range(self.num_threads):
      ReaderThread(self.connection_pool, input_queue, result_queue).start()
    input_queue.join()
    rows = []
    while not result_queue.empty():
      rows.append(result_queue.get())
    return rows
