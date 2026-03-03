# B- (.bh) Programming Language

Welcome to **B-**, a minimal virtual CPU language designed to feel like real assembly — but simple enough for beginners to understand.

This tutorial assumes **no prior knowledge of assembly**.

---

# 1. What Is B-?

B- is a low-level programming language that runs on a virtual CPU written in Python.

That means:

* You control registers directly
* You control memory directly
* You control jumps and function calls
* Nothing happens automatically

It is designed to teach how computers actually work internally.

---

# 2. File Extension

All B- programs must use:

```
.bh
```

Example:

```
program.bh
```

---

# 3. Program Structure

Every B- program **must start with a header**:

```
mom = 64
pth = 'memory.txt'
pers = 0
dbg = 0
```

### Header Options

## mom

Memory size in **kilobytes**.

```
mom = 64
```

This allocates 64 KB of RAM.

---

## pth

Memory output file.

```
pth = 'memory.txt'
```

If the file ends with:

* `.txt` → readable memory snapshot
* `.bin` → raw binary memory

---

## pers

Persistence flag.

```
pers = 1
```

* `1` → memory persists between runs (binary only)
* `0` → memory resets every execution

---

## dbg

Debug mode.

```
dbg = 1
```

* `1` → prints register state after every instruction
* `0` → normal execution

---

# 4. Registers (Tiny CPU Storage)

Registers are small storage slots inside the CPU.

Available registers:

```
r0
r1
r2
r3
r4
r5
sp   (stack pointer)
ip   (instruction pointer)
fl   (flag register)
```

You mainly use `r0`–`r5`.

---

# 5. Basic Instructions

## mov (move data)

```
mov r0 5
```

Put value `5` into register `r0`.

You can also copy registers:

```
mov r1 r0
```

---

## Math Instructions

```
add r0 r1
sub r0 1
mul r0 2
div r0 3
```

These modify the **first value**.

Example:

```
mov r0 10
add r0 5
```

Result: `r0` becomes 15.

---

# 6. Comparing Values

## iseq (is equal)

```
iseq r0 r1
```

If they are equal:

```
fl = 1
```

Otherwise:

```
fl = 0
```

The `fl` register stores comparison results.

---

# 7. Jumping (Control Flow)

## Labels

Create a label like this:

```
loop:
```

---

## jum (jump always)

```
jum loop
```

This moves execution back to the label.

---

## jeq (jump if equal)

```
jeq done
```

Jumps only if `fl == 1`.

---

## jneq (jump if not equal)

Jumps if `fl == 0`.

---

# 8. The Stack

The stack is special memory used for temporary storage.

## push

```
push r0
```

Places value onto the stack.

## pop

```
pop r1
```

Removes value from stack into register.

---

# 9. Functions

## call

```
call myFunction
```

Jumps to a label and remembers where to return.

## ret

```
ret
```

Returns to where `call` happened.

---

# 10. Output (Printing Text)

B- uses software interrupts.

## int 1

Print number in `r0`.

```
mov r0 42
int 1
```

---

## int 2

Print character from ASCII value in `r0`.

```
mov r0 72
int 2
```

72 = H

---

## int 3

Take user input and store in `r0`.

---

# 11. Memory Access

You can access memory directly using brackets:

```
mov [100] r0
mov r1 [100]
```

This stores and retrieves values from RAM.

---

# 12. Ending a Program

```
end
```

Stops execution.

---

# 13. Full Beginner Example

```
mom = 64
pth = 'memory.txt'
pers = 0
dbg = 0

mov r0 0
mov r1 5

loop:
iseq r0 r1
jeq done

add r0 1
jum loop

done:
mov r0 10
int 1

end
```

This program:

* Counts from 0 to 5
* Stops when equal
* Prints 10

---

# 14. What Happens After Execution?

If `pth` is a `.txt` file, you will see:

* Register values
* Stack contents
* First section of memory

This lets you inspect how the program behaved internally.

---

# 15. How to Run a Program

From terminal:

```
python bminus_vm.py program.bh
```

---

# 16. What You’re Learning

By using B-, you are learning:

* How CPUs move data
* How stacks work
* How function calls work
* How jumps control execution
* How memory is structured

You are programming closer to the hardware than most developers ever do.

---

# 17. Next Steps

After mastering basics, try:

* Writing a calculator
* Making a loop that prints text
* Building a small function library
* Experimenting with persistent memory

---

Welcome to low-level programming.

You now control the machine.
