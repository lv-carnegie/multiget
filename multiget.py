
   
import argparse
from urllib.request import urlopen, Request 
import math
import threading

##############################################


# define function to request individual chunks
def fetchChunk(url, start, end, results, index): 
   
	# reads chunk between start and end range 
	# saves chunk to indexed results list
	
	headers = dict(Range = 'bytes=%d-%d' % (start, end))
	request = Request(url, headers=headers)
	results[index] = urlopen(request).read()

	return True


# define main download function		
def multiGet(url, n, chunk_size, output_path):
	
	# downloads data from url and writes to output path
	# downloads n chunks of chunk_size bytes
	
	
	#### Run checks on request

	# open object for reading
	try: 
		request = Request(url)
		request.get_method = lambda : 'HEAD'
		r = urlopen(request)
	except Exception as e:
		return str(e)

	# verify that the server supports range requests
	if r.headers.get('Accept-Ranges', '') != 'bytes':
		return 'range requests not supported'
		
	# check the contents size against requested size
	# and set the number of bytes to be downloaded to the smaller value	
	requested_length = n * chunk_size
	content_length = int(r.headers['content-length'])	
	download_length = min([requested_length, content_length])
	
	# update number of chunks to download	
	n = int(math.ceil(download_length / chunk_size))

	
	
	#### Download the data
	
	# create list to store retrived chunks in order
	results = [{} for i in range(n)]

	# create list to store threads
	threads=[]

	# loop through the chunks
	for i in range(n):
			
		# calculate chunk range start and end bytes inclusive
		start = i * chunk_size
		end = start + chunk_size - 1  
		
		# start a thread for each chunk
		process = threading.Thread(target=fetchChunk, args=(url, start, end, results, i))
		process.start() 
		threads.append(process)

	# join threads so that main thread will pause untill all chunks are collected
	for process in threads:
		process.join()
	
	
	
	#### Save to disk

	# write the chunks to the output file
	count_bytes = 0
	output_file = open(output_path, 'wb')
	for chunk in results:
		count_bytes += len(chunk)
		output_file.write(chunk)

		
	return 'download complete: {:10f} MiB'.format(1.0 * count_bytes / 2 ** 20)


##############################################


#### Parse command line option

parser = argparse.ArgumentParser(description='Parallel download file chunks. Default 4 chunks of size 1 MiB ')
parser.add_argument('url',
		help='source url')
			
parser.add_argument('-n', type=int, default=4,
		help='number of chunks - default 4 chunks')
				
parser.add_argument('-s', type=float, default=1,
		help='chunk size in MiB, rounded down to nearest integer - default 1 MiB')
				
parser.add_argument('-o', default='data.bin',
		help='output file path - default data.bin')

args = parser.parse_args()


##############################################


#### Run main function

if __name__ == "__main__":

	# run the main multiGet function to download file
	# convert chunk size s from MiB to bytes and round down to nearest integer
	
	res = multiGet(args.url, args.n, int(args.s * 2**20), args.o)
	print(res)
