'''
short script to generate realistic data for IntVis hw6

author: urygam
'''

from dataclasses import dataclass
import numpy as np
import sys
import csv
import pandas as pd

# constants
WORD_LIMIT = 1_000_000
MAX_READING_RATE = 400_000 # words per day
AVG_READING_RATE = 40_000 # words per day
MIN_READING_RATE = 10 # words per day

@dataclass
class Book:
	'''
	dataclass to store book information
	'''

	title: str
	start_day: int
	words: int
	rate: int

	def __repr__(self):
		'''
		overwrite repr - default is too long
		'''

		return '"' + self.title + '" ' + self.start_day

	def generate_reading_data_cumulative(self):
		'''
		function to generate words read per day for current Book
		'''

		# each book will have 5k to 1M words (increments of 1k)
		words_left = [1000 * np.random.randint(5, high=WORD_LIMIT // 1_000)]

		# read a random amt of words each day until none left
		while words_left[-1] > 0:
			# sample number of words read from normal distribution
			words_read = np.clip(np.random.normal(loc=AVG_READING_RATE,scale=AVG_READING_RATE * 1.5), MIN_READING_RATE, MAX_READING_RATE)
			# if the book is finished, return
			if words_left[-1] - words_read <= 0:
				words_left.append(0)
				self.words_left = words_left
				return
			else:
				words_left.append(np.round(words_left[-1] - words_read, 0))

	def generate_reading_data(self):
		'''
		function to generate words read per day for current Book
		'''

		# each book will have 5k to 1M words (increments of 1k)
		# words_left = 1000 * np.random.randint(5, high=WORD_LIMIT // 1_000)
		words_left = self.words
		words_read = []

		# read a random amt of words each day until none left
		while words_left > 0:
			# sample number of words read from normal distribution
			# read = np.clip(np.random.normal(loc=AVG_READING_RATE,scale=AVG_READING_RATE * 2), MIN_READING_RATE, MAX_READING_RATE)
			read = np.clip(np.random.normal(loc=self.rate, scale=self.rate * 0.4), MIN_READING_RATE, MAX_READING_RATE)

			# if the book is finished, return
			if words_left - read <= 0:
				words_read.append(0)
				self.words_left = words_read
				return
			else:
				words_read.append(np.round(read, 0))
				words_left -= read

def parse_books(fname):
	'''
	function to read in and parse data from
	csv file

	param fname (str): path to source csv file
	returns: list of Book objects

	format of csv file:b
	"<name of book 2>",<number of words>
	"<name of book 1>",<number of words>
	'''

	output = []
	with open(fname, 'r') as f:
		# use csv reader
		csv_file = csv.reader(f)

		# create a new Book from each line in the csv file
		output = [Book(line[0], int(line[1]), int(line[2]), int(line[3])) for line in csv_file]

	return output

def generate_matrix(books):
	'''
	function to generate 2D matrix from each book's reading data

	param books (list of Book)
	returns: 2D matrix
	'''

	# calculate number of days needed
	num_days = np.max([b.start_day + len(b.words_left) for b in books])

	# create output matrix
	out = np.zeros((num_days, len(books)))

	# populate book word values
	for i, b in enumerate(books):
		out[b.start_day:b.start_day+len(b.words_left), i] = b.words_left

	return out

def write_matrix_to_file(mat, books, fname):
	'''
	function to format the matrix into the specific input
	format for D3

	param mat (2D int matrix): matrix of word_left values
	param books (list of Book): list of all books
	param fname (str): filename to write output to
	'''

	# generate header labels
	header = [b.title for b in books]

	# convert to pd DataFrame
	df = pd.DataFrame(data=mat.astype(np.uint64))

	# write to file
	df.to_csv(fname, mode='w', header=header)

def main():
	# parse books from file
	books = parse_books('books.csv')

	# generate random reading data from each book
	for b in books:
		b.generate_reading_data()

	# parse new random data into matrix
	mat = generate_matrix(books)

	# parse and write to file for input into D3
	write_matrix_to_file(mat, books, 'book_data.csv')

if __name__ == '__main__':
	main()