**NOTE: This is unfinished but please report any bugs if you are able to find any.**

# Turing-Machine.io
The pheonix that rose from the ashes of Turing Machine But Way Worse with a terrible pun on .io games.

## Memory Type
A Turing Machine, and consequently Turing Machine.io, relies on a tape to store information, so it is a tape-based esolang.
### So what is a tape?
A tape, in the context of esolangs, is an infinite list of "cells", each containing a specific value, that can be written and read from.

For some clarification, I would like to turn to brainfuck, widely considered the most popular esolang.
```
...0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0...
                     ^
```
*The ellipsis represents infinite 0s. While the original version of brainfuck only contained a finite amount of cells, we will be presuming an infinite tape.* 

In this esolang the pointer, represented by the caret character, is "looking" at a cell. It can either write to the cell, read from the cell, and switch to a different cell.

It writes to the cell by either executing `+`, to increment the cell's value (if the cell was 0 and the `+` instruction was executed, then cell would be 1); and `-`, to decrement the cell's value.

Reading from the cell is less obvious: how could you read from the cell if there's no direct command for it? brainfuck executes this by incorporating control flow with reading the cell: the `]` command functions as a conditional jump. If the cell is not 0, the program will figuratively jump to the matching `[` bracket.

For example if the cell that the pointer is looking at was 196, `[-]` would decrement the cell until it is 0.

Switching to a different cell is simpler: `<` moves the pointer 1 cell left, and `>` moves the pointer 1 cell right.

brainfuck also manages to incorporate I/O in all these aspects: `.` outputs the ASCII (or Unicode depending on the implementation) 

How does Turing Machine.io incorporate all of these aspects of a tape-based esolang?
## Writing to Cells

Turing Machine.io, much alike brainfuck, has a singular instruction for writing to the tape; however, the user specifies the exact symbol (integer) that the cell is to be replaced with. It also has a way to switch from one cell to the next, almost exactly like brainfuck, `0` means to move left and `1` means to move right.

While the functionality of reading cells is obvious, it takes knowledge of the program structure to understand.

## Program Structure

A Turing Machine, and consequently Turing Machine.io, executes an instruction set based on the "state" that the program is in and the value of cell.

For example an instruction set in a Turing Machine-like language could be that if the state of the program is 0 and the value of the cell is 0, then replace that cell with 1 and move to the right.

Therefore, the reading aspect of a tape-based esolang is embedded in the program structure in a Turing Machine.

However, what is this weird "state" of the program? How would one change it?
## Control Flow

A Turing Machine has a unique control flow that differs from most tape-based esolangs: usually, tape-based esolangs utilized conditional jumps or self-modifying mechanics, but a Turing Machine would utilize its state mechanic.

As shown previously, the instruction set executed is determined based off the state of the program and the value of the cell. However, contained within this instruction set is an instruction that changes the state to an arbitrary value. This can be used to make conditional loops really easily.

For example, in a Turing Machine-like esolang, if one instruction set was to change the cell to 0, don't move to the right or left, and change the state to 0 if the current cell is 1 and the state is 0; and the other was to change the cell to 1, don't move to the right or left, and change the state to 0 if the current cell is 0 and the state is 0, then you would get an infinite loop.

However, where is the defining feature of this esolang, I/O?

## Input and Output

Input is part of the replace instruction: it will replace the current cell with 0 or 1 depending on the bit, 2 if the current character has run out of bits, or -1 if input has ended. Initially, I was intending for the input instruction to replace the current cell with its Unicode representation, but I realized that for a simple cat program, the programmer would have to hardcode 1114112 possible input values.

Clearly, this wouldn't suffice.

Therefore, Turing Machine.io uses binary-like input, with a sequence of 0s and 1s followed by a 2 to symbolize the end of a character, and a -1 to symbolize the end of input.
For example if the input was `abc`, the input buffer would be `1, 1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 1, 0, 2, 1, 1, 0, 0, 0, 1, 1, 2, -1, -1, -1, -1, ...`.

If the replace instruction is -1, it will replace the cell with the leftmost value of the input buffer and then remove that value from the input buffer. For example if the input buffer was `1, 1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 1, 0, 2, 1, 1, 0, 0, 0, 1, 1, 2, -1, -1, -1, -1, ...`, the current cell would be replaced with `1`, and the input buffer would be `1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 1, 0, 2, 1, 1, 0, 0, 0, 1, 1, 2, -1, -1, -1, -1, ...`

Outputting also involves a buffer system like inputting; however, there is an option to directly output: Turing Machine.io outputs the Unicode equivalent of the symbol currently on the tape if the output instruction is `3`. `1` adds the value of the cell to the end of the output buffer if the instruction is `1` and the cell's value is `0` or `1`, and `2` interprets the binary string as binary and prints its Unicode equivalent without a leading newline.

## Halting

Now, it would be pretty stupid to make every Turing machine, and consequently a Turing Machine.io, program to either run infinitely or terminate on an error. To prevent this there is an extra instruction that, after all the instructions are executed, determines whether the program should halt or not. If this instruction is `0`, the program won't halt; however, if this instruction is `1`, the program will halt.

## Syntax

```65 5 66 3 -1 6 0```
This instruction set would mean "If the value of the cell is 65 and the program's state is 5, replace the cell with 66, convert the value of the cell (66) to Unicode ('B') and print it out, move 1 to the left of the cell, change the program's state to 6, and don't halt."

So the general syntax would be:
```<value of cell condition> <state condition> <replace instruction> <output instruction> <move instruction> <change state instruction> <halt instruction>```

A Turing Machine.io program is just a collection of instruction sets. For examples, look at helloworld.tmi and cat.tmi, both files on this repository.

If parts of this documentation were confusing, or you have any suggestions in general, don't hesistate to either contact me directly or raise an issue or pull request.


## To-do List:
- Finish documentation
- Optimize/clean code
- Change the design slightly?
- Make parsing not bad
- Give an error when the user specifies an invalid state change
- Make debugging not bad
- ???
- Profit
