import multiprocessing

def poll(f, file):
	with open(file, 'r') as js:
		data = []
		while True:
			for c in js.read(1):
				data.append('%02X' % ord(c))
				if len(data) == 8:
					if data[6] == '01' and (data[4] == '00' or data[4] == '01'):
						f(data[4] == '01', data[7])
					data = []

def queue(file):
	q = multiprocessing.Queue()
	f = lambda x, y: q.put((x, y))
	p = multiprocessing.Process(target=poll, args=(f, file))
	return (p, q)
