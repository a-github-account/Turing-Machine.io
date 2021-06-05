## Turing Machine with I/O by MilkyWay90
## A better version of my previous esolang, Turing Machine But Way Worse
## Started in august 2020 or smth, hopefully finished by 10/2/2020
## Haha it's the second week of November (11/9/2020) and it's still not completely done
## Haha it's 11/16/2020 and it's actually almost done gg


import sys # Library for reading
import ctypes # Library that is used for enabling ANSI
from debug import infoOutput # Another file in the directory that's used to debug


debug_info = '''
State: {0}
Value of position: {1}
Position: {2}
Instruction executed: {3}
Instruction to execute next: {4}
Current instruction set: {5}
Current Output: {6}
Negative Tape: {7}
Positive Tape: {8}
Input buffer: {9}
Output buffer: {10}
Press ^C to continue
'''


# Execute the code from a list of states
def execute(states, debug = False):
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
	if debug:
		debug_output = ""
	
	while True:
		instructions = states[(str(tape[pos]), state)] # Fetch the list of instructions
		
		debug and\
			infoOutput(
				debug_info.format(
					state,
					str(tape[pos]),
					pos - offset,
					"halt/none",
					"replace",
					", ".join(instructions),
					debug_output,
					str(tape[:offset]),
					str(tape[offset:]),
					input_buffer,
					output_buffer
				)
			)
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

		debug and\
			infoOutput(
				debug_info.format(
					state,
					str(tape[pos]),
					pos - offset,
					"replace",
					"output",
					", ".join(instructions),
					debug_output,
					str(tape[:offset]),
					str(tape[offset:]),
					input_buffer,
					output_buffer
				)
			)

		# Print/Output to STDOUT instruction
		output = int(instructions[1])
		if output:
			try:
				#print("a", state, tape[:pos], "[" + str(tape[pos]) + "]", tape[pos+1:], instructions)
				if output == 1:
					if tape[pos] in [0, 1]:
						output_buffer += str(tape[pos])
					else:
						pass # Might put an error here
				elif output == 2:
					if debug:
						debug_output += chr(int(output_buffer, 2))
					else:
						sys.stdout.write(chr(int(output_buffer, 2)))
					output_buffer = ""
				elif output == 3:
					if debug:
						debug_output += chr(tape[pos])
					else:
						sys.stdout.write(chr(tape[pos]))
				sys.stdout.flush()
			except ValueError:
				pass # Don't output if the character is out of Unicode range
		
		debug and\
			infoOutput(
				debug_info.format(
					state,
					str(tape[pos]),
					pos - offset,
					"output",
					"move",
					", ".join(instructions),
					debug_output,
					str(tape[:offset]),
					str(tape[offset:]),
					input_buffer,
					output_buffer
				)
			)
			
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
			
		debug and\
			infoOutput(
				debug_info.format(
					state,
					str(tape[pos]),
					pos - offset,
					"move",
					"change state",
					", ".join(instructions),
					debug_output,
					str(tape[:offset]),
					str(tape[offset:]),
					input_buffer,
					output_buffer
				)
			)
		
		
		# Change state instruction
		state = instructions[3]

		debug and\
			infoOutput(
				debug_info.format(
					state,
					str(tape[pos]),
					pos - offset,
					"change state",
					"halt",
					", ".join(instructions),
					debug_output,
					str(tape[:offset]),
					str(tape[offset:]),
					input_buffer,
					output_buffer
				)
			)

		# Halt instruction
		halt = int(instructions[4])
		if halt:
			sys.exit(0)
			
		debug and\
			infoOutput(
				debug_info.format(
					state,
					str(tape[pos]),
					pos - offset,
					"halt",
					"replace",
					", ".join(instructions),
					debug_output,
					str(tape[:offset]),
					str(tape[offset:]),
					input_buffer,
					output_buffer
				)
			)
		


# Parse the code and return a dictionary
def parse(code):
	# Convert text to a dictionary
	states = dict(((line.split()[0], line.split()[1]), line.split()[2:]) for line in code.split("\n"))
	
	# Make sure that all instructions are numbers and that all instructions are valid
	line_counter = 0
	for line in code.split("\n"):
		instruction_counter = 0
		for instruction in line.split():
			try:
				int(instruction) # Attempt to make an integer version of the instruction
			except ValueError:
				# Throw an error
				sys.exit(
					"\033[31mError: Line {0}, instruction {1} is not a number.\033[0m"\
					.format(line_counter, instruction_counter)
				)

			if instruction_counter == 3: # Check for print instruction validity
				if instruction not in "0 1 2 3".split():
					sys.exit(
						"\033[31mError: Line {0}, instruction {1} is a print instruction but isn't 0 or 1.\033[0m"\
						.format(line_counter, instruction_counter)
					)
					
			
			elif instruction_counter == 4: # Check for move instruction validity
				if instruction not in "-1 0 1".split():
					sys.exit(
						"\033[31mError: Line {0}, instruction {1} is a move instruction but isn't -1, 0, or 1.\033[0m"\
						.format(line_counter, instruction_counter)
					)
					
			elif instruction_counter == 6: # Check for halt instruction validity
				if instruction not in "0 1".split():
					sys.exit(
						"\033[31mError: Line {0}, instruction {1} is a move instruction but isn't 0, or 1.\033[0m"\
						.format(line_counter, instruction_counter)
					)
				
			instruction_counter += 1
		line_counter += 1
		
	return states

# Read a file's contents and return it
def readfile(filename):
	file = open(filename, 'r')
	contents = file.read()
	file.close()
	return contents
	
def main():
	# Two lines of random code I got from Stack Overflow (https://stackoverflow.com/a/36760881 because CC BY-SA)
	# I don't know what they do but they make ANSI magically work
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
	
	if '-d' in sys.argv:
		debug = True
		args = sys.argv[:(index:=sys.argv.index('-d'))] + sys.argv[index+1:]
	else:
		debug = False
		args = sys.argv
	
	contents = readfile(args[1]) # Get file contents
	states = parse(contents) # Get the converted form of the file
	execute(states, debug = debug) # Execute the program
	

if __name__ == "__main__": # Something unnecessary that's considered "good coding practice"
	main()
