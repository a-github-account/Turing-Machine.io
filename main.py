## Turing Machine with I/O by MilkyWay90/a-github-account
## A better version of my previous esolang, Turing Machine But Way Worse
## Started progress on August 2020
## Finished somewhere on December 2020-January 2021
## First public release on May 2021

import sys # Library for reading cmd args
import ctypes # Library that is used for enabling ANSI


# Execute the code from a list of states
def execute(states):
	tape = [0] # Tape that the Turing Machine operates on
	offset = 0 # Anything that is below the offset is part of the negative tape.
			   #(for example if the offset was 2 and the list was [2, 3, 4, 5] 
			   # then 2 and 3 would be part of the negative tape.
	
	pos = 0	   # Position that the Turing Machine is at.
			   # For example, if the tape was [2, 3, 4] and pos was 0, then
			   # the Turing Machine would be pointing at 2.
			   
	state = "0" # State that the Turing Machine is in
	input_buffer = "" # Dunno if "_buffer" belongs here
	output_buffer = "" # Same here
	
	while True:
		instructions = states[(str(tape[pos]), state)] # Fetch the list of instructions
		
		# Replace instruction
		replace = int(instructions[0])
		if not replace + 1: # If the replace instruction is -1 (aka take input)
			if input_buffer:
				tape[pos] = int(input_buffer[0])
				input_buffer = input_buffer[1:]
			else:
				temp_char = sys.stdin.read(1)
				try:
					tape[pos], input_buffer = int((temp_val := bin(ord(temp_char)))[2]), temp_val[3:] + '2'
					del temp_val
				except TypeError: # If STDIN has ended and stdin.read(1) returns a 0-length string, ord() would throw a TypeError
					tape[pos] = 3
				del temp_char
		else: # If the replace instruction >= 0
			tape[pos] = replace # Replace this position with the replace instruction

		# Print/Output to STDOUT instruction
		output = int(instructions[1])
		if output:
			try:
				if output == 1:
					if tape[pos] in [0, 1]:
						output_buffer += str(tape[pos])
				elif output == 2:
					sys.stdout.write(chr(int(output_buffer, 2)))
					output_buffer = ""
				elif output == 3:
					sys.stdout.write(chr(tape[pos]))
				sys.stdout.flush()
			except ValueError:
				pass # Don't output if the character is out of Unicode range
			
		# Move instruction
		move = int(instructions[2])
		pos += move # Move the pointer
		# Utilize the offset variable to prevent negative pos issue
		if pos == -1:
			pos = 0
			tape = [0] + tape
			offset += 1
		# If the position goes out of bounds
		elif pos >= len(tape):
			tape.append(0)
		
		# Change state instruction
		state = instructions[3]

		# Halt instruction
		halt = int(instructions[4])
		if halt:
			sys.exit(0)

# Parse the code and return a dictionary
def parse(code):
	# Convert text to a dictionary
	states = dict(((line.split(" ")[0], line.split(" ")[1]), line.split(" ")[2:]) for line in code.split("\n"))
	return states

# Validate the code to make sure that it's valid (yeah pretty self-explanatory)
def validate(code):
	instruction_sets = [i.split(" ") for i in code.split("\n")] # List of instruction sets
	conditionals = {} # Keep track of states and cells so that there are no duplicates
	error = False # Keep track of whether there's an error or not
	for line in range(len(instruction_sets)):
		instruction_set = instruction_sets[line]
		if len(instruction_set) == 0:
			print(
				"Validation Error: Empty line on line {}; did you leave a trailing newline?".format(
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
			continue
		elif len(instruction_set) != 7:
			print(
				"Validation Error: Incorrect number of instructions in instruction set {0} on line {1}".format(
					" ".join(instruction_set),
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
			continue
		
		# Check if the conditional value of the cell is a whole number
		try:
			assert int(instruction_set[0]) > -1
		except:
			print(
				"Validation Error: Value of cell conditional, instruction 1 of instruction set {0} on line {1}, is not a whole number.".format(
					" ".join(instruction_set),
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
		
		# Check for no duplicates within conditionals and if there are no duplicates, add it to the list of conditionals
		try:
			line_other = conditionals[(instruction_set[0], instruction_set[1])]
			print(
				"Validation Error: Value of cell + state conditions, instructions 1 and 2, respectively, are duplicated in instruction sets {1} and {3}, on lines {0} and {2}, respectively.".format(
					str(line_other + 1),
					" ".join(instruction_sets[line_other]),
					str(line + 1),
					" ".join(instruction_sets[line])
				),
				file = sys.stderr
			)
			error = True
		except KeyError:
			conditionals[(instruction_set[0], instruction_set[1])] = line
		
		# Check for replace instruction validity (whole numbers and -1)
		try:
			assert int(instruction_set[2]) > -2
		except:
			print(
				"Validation Error: Replace instruction, instruction 3 of instruction set {0} on line {1}, is not -1 or a whole number.".format(
					" ".join(instruction_set),
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
		
		# Check for output instruction validity (numbers 0 - 3)
		try:
			assert -1 < int(instruction_set[3]) < 4
		except:
			print(
				"Validation Error: Output instruction, instruction 4 of instruction set {0} on line {1}, is not a whole number inclusively between 0 and 3.".format(
					" ".join(instruction_set),
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
		
		# Check for move instruction validity (-1, 0, or 1)
		try:
			assert -2 < int(instruction_set[4]) < 2
		except:
			print(
				"Validation Error: Move instruction, instruction 5 of instruction set {0} on line {1}, is not -1, 0, or 1.".format(
					" ".join(instruction_set),
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
		
		# Check for halt instruction validity (0 or 1)
		try:
			assert int(instruction_set[4]) in (0, 1)
		except:
			print(
				"Validation Error: Halt instruction, instruction 6 of instruction set {0} on line {1}, is not 0 or 1.".format(
					" ".join(instruction_set),
					str(line + 1)
				),
				file = sys.stderr
			)
			error = True
	
	if error == True:
		sys.exit("Program terminated due to validation error(s).")
		
		

# Read a file's contents and return it
def readfile(filename):
	file = open(filename, 'r')
	contents = file.read()
	file.close()
	return contents
	
def main():
	# Two lines of code that enables ANSI in Windows cmd that I got from Stack Overflow (https://stackoverflow.com/a/36760881 because CC BY-SA)
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
	args = sys.argv
	
	contents = readfile(args[1]) # Get file contents
	validate(contents)
	states = parse(contents) # Get the converted form of the file
	execute(states) # Execute the program

if __name__ == "__main__":
	main()
