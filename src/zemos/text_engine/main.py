# coding=utf-8


import sys
import time
import xlrd


class Unbuffered(object):
	def __init__(self, stream):
		self.stream = stream

	def write(self, data):
		self.stream.write(data)
		self.stream.flush()

	def __getattr__(self, attr):
		return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


class Block(object):
	def __init__(self, block_id, contents, options):
		self.id = block_id
		self.contents = contents
		self.options = options


class Content(object):
	def __init__(self, text, wait):
		self.text = text
		self.wait = wait


class Option(object):
	def __init__(self, text, jump_id):
		self.text = text
		self.jump_id = jump_id


COL_ID = 0
COL_TEXT = 1
COL_WAIT = 2
COL_OPTION_BEGIN = 3
COL_OPTION_END = 6


def parse_block(sheet, begin):
	if begin >= sheet.nrows:
		return None, None
	row = sheet.row_values(begin)
	if row[COL_ID] == '' or row[COL_TEXT] == '':
		return None, None
	block_id = int(row[COL_ID])
	row_idx = begin
	contents = []
	while True:
		if row_idx >= sheet.nrows:
			break
		row = sheet.row_values(row_idx)
		if (row_idx != begin and row[COL_ID] != '') or row[COL_TEXT] == '':
			break
		wait = 0
		if row[COL_WAIT] != '':
			wait = int(row[COL_WAIT])
		contents.append(Content(row[COL_TEXT], wait))
		row_idx += 1
	options = []
	option_row = sheet.row_values(row_idx - 1)
	for col_idx in range(COL_OPTION_BEGIN, COL_OPTION_END + 1, 2):
		if option_row[col_idx] != '':
			options.append(Option(option_row[col_idx], int(option_row[col_idx + 1])))
	block = Block(block_id, contents, options)
	return block, row_idx


def out_text(text):
	for char in text:
		print(char, end='')
		time.sleep(0.2)


def play_block(block):
	for content in block.contents:
		out_text(content.text)
		time.sleep(content.wait)
		print()


def wait_option(block):
	for i in range(0, len(block.options)):
		option = block.options[i]
		print('\t选项{}：'.format(i + 1), option.text)
	while True:
		try:
			choice_id = int(input('\t选择：'))
			if 0 < choice_id <= len(block.options):
				return block.options[choice_id - 1].jump_id
		except ValueError:
			pass
		print('\ttips：输入选项编号，回车')


def run():
	workbook = xlrd.open_workbook('data.xlsx')
	sheet = workbook.sheet_by_name('data')
	blocks = {}
	cur_block = None

	# parse
	begin = 1
	while True:
		block, begin = parse_block(sheet, begin)
		if block is None:
			break
		blocks[block.id] = block
		if cur_block is None:
			cur_block = block

	# play
	while True:
		play_block(cur_block)
		if cur_block.id < 0:
			print('game over')
			break
		jump_id = wait_option(cur_block)
		cur_block = blocks[jump_id]
	input()


if __name__ == "__main__":
	run()
