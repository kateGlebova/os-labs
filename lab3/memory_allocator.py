from terminaltables import AsciiTable
from random import randint

MEMORY_SIZE = 1024

class NotEnoughSpace(Exception):
	def __init__(self, message):
		self.message = message

class NoSuchProcess(Exception):
	def __init__(self, message):
		self.message = message

class ImpossibleToConvert(Exception):
	def __init__(self, message):
		self.message = message

class Process:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __str__(self):
    	return "P%s" % self.id

class Partition:
    def __init__(self, address, size, process=None):
        self.address = address
        self.size = size
        self.process = process
        self.is_allocated = bool(process)


class Memory:
	def __init__(self):
		self.table = [Partition(0, MEMORY_SIZE)]

	def load_process(self, process):
		for i, partition in enumerate(self.table):
			if not partition.is_allocated and process.size <= partition.size:
				self.allocate(i, partition, process)
				break
		else:
			raise NotEnoughSpace('Not enough space for %s of size %s' % (process, process.size))
    
	def allocate(self, index, partition, process):
		old_size = partition.size
		allocated_partition = Partition(partition.address, process.size, process=process)
		self.table[index] = allocated_partition
		free_partition_size = old_size - process.size
		if free_partition_size:
			self.table.insert(index + 1, Partition(allocated_partition.address + allocated_partition.size, free_partition_size))

	def find_partition(self, process_id):
		for partition in self.table:
			if partition.is_allocated and partition.process.id == process_id:
				return partition
		raise NoSuchProcess("Process  %s is not loaded to memory" % process_id)


	def end_process(self, process_id):
		partition = self.find_partition(process_id)
		partition.process = None
		partition.is_allocated = False

	def get_physical_address(self, process_id, offset):
		partition = self.find_partition(process_id)
		if offset < partition.size:
			return self.find_partition(process_id).address + offset
		raise ImpossibleToConvert("Offset cannot be larger than the partition size")

	def __str__(self):
		table_data = [['Address', 'Size', 'Allocation']]
		for partition in self.table:
			partition_row = ["%04X" % partition.address, str(partition.size)]
			if partition.is_allocated:
				partition_row.append(partition.process)
			else:
				partition_row.append('free')
			table_data.append(partition_row)
		return AsciiTable(table_data).table

class Interface:
	def __init__(self):
		self.memory = Memory()
		self.last_process_id = 0

	@staticmethod
	def print_menu():
		print("1. Show memory table")
		print("2. Add process")
		print("3. End process")
		print("4. Convert virtual address to physical")
		print("5. Exit")
    
	def show_memory_table(self):
		print(self.memory)

	def add_process(self):
		process = Process(self.last_process_id + 1, randint(1, MEMORY_SIZE))
		self.last_process_id += 1
		try:
			self.memory.load_process(process)
		except NotEnoughSpace:
			print('Not enough space to load a process')

	def end_process(self):
		process_id = input("Enter a process id: ")
		try:
			self.memory.end_process(int(process_id))
		except ValueError:
			print("Process id must be an integer!")
		except NoSuchProcess as e:
			print(e.message)

	def convert(self):
		process_id = input("Enter a process id: ")
		offset = input("Enter an offset: ")
		try:
			print("%04X" % self.memory.get_physical_address(int(process_id), int(offset)))
		except ValueError:
			print("Process id and offset must be an integers!")
		except NoSuchProcess as e:
			print(e.message)
		except ImpossibleToConvert as e:
			print(e.message)

	def run(self):
		answer_action = {'1': self.show_memory_table, '2': self.add_process, '3': self.end_process, '4': self.convert, '5': exit}
		answer = ''
		while True:
			self.print_menu()
			answer = input("Choose an option: ")
			if answer not in ['1', '2', '3', '4', '5']:
				print('Wrong input\n\n\n')
			else:
				answer_action[answer]()


if __name__ == '__main__':
	interface = Interface()
	interface.run()