# -*- coding: utf-8 -*-

import subprocess
from cuter_smt_library import serialize, unserialize

debug = False


if debug:
	import os.path
	filename = "solver.txt"
	if os.path.isfile(filename):
		clog = open(filename, "a")
	else:
		clog = open(filename, "w")


def log(msg = ""):
	if debug:
		clog.write(msg + "\n")


class Solver:

	def __init__(self, arguments):
		"""
		Create a subprocess using provided program arguments.
		"""
		self.process = subprocess.Popen(
			arguments,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			universal_newlines=True
		)
		log("; +" + str(arguments))

	def write(self, stmt):
		line = serialize(stmt)
		self.process.stdin.write(line + "\n")
		log(line)

	def read(self):
		open_cnt = 0
		close_cnt = 0
		lines = []
		while True:
			line = self.process.stdout.readline()[:-1]
			lines.append(line)
			open_cnt += line.count("(")
			close_cnt += line.count(")")
			if open_cnt == close_cnt:
				break;
		smt = "\n".join(lines)
		log(smt)
		if open_cnt == 0 and close_cnt == 0:
			return smt
		return unserialize(smt)

	def check_sat(self):
		self.write(["check-sat"])
		return self.read()

	def get_value(self, expr):
		self.write(["get-value", [expr]])
		return self.read()

	def exit(self):
		self.write(["exit"])


#class SolverCVC4(Solver):
#
#	def __init__(self):
#		Solver.__init__(self, ["cvc4", "--lang", "smt", "--produce-models"])
#
#	@staticmethod
#	def fix_names(obj): # TODO fix_names
#		return [["|{}|".format(item[0]), item[1]] for item in obj]


class SolverZ3(Solver):

	def __init__(self):
		Solver.__init__(self, ["z3", "-smt2", "-in"])
