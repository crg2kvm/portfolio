# Operating Systems Projects
## Overview
This directory contains various projects related to Operating Systems, demonstrating different aspects of OS functionalities and concepts.

## Projects
### Custom Built Shell:

The Custom Built Shell Command Line project implements a simple yet functional command-line shell that mimics basic Unix shell functionalities. It supports command execution, input/output redirection, pipelining, and background process execution. The project includes the main shell driver, command parser, and command executor, demonstrating key concepts such as command parsing, process creation, and inter-process communication. This project provides a practical example of how an operating system shell operates at a fundamental level.
### Dynamic Page Allocation:

The Dynamic Page Allocation project for the Xv6 operating system extends the Xv6 kernel to support dynamic page allocation. This includes implementing a system call for allocating and deallocating memory pages at runtime, allowing for more efficient memory management and utilization. The project demonstrates modifications to the Xv6 kernel to handle dynamic memory requests, showcasing the principles of virtual memory management and system call integration within a simple Unix-like operating system.
### Lottery Scheduling:

The Lottery Scheduling project for the Xv6 operating system implements a probabilistic scheduling algorithm that allocates CPU time to processes based on "lottery tickets." Each process is assigned a certain number of tickets, and the scheduler randomly selects a ticket to determine which process runs next. This project modifies the Xv6 kernel to support this lottery-based scheduling, providing a fair and randomized method for CPU allocation and demonstrating advanced process scheduling concepts within a simple Unix-like operating system.
### Multithread Game of Life:

The MultiThread Game of Life project implements a multithreaded version of Conway's Game of Life, a cellular automaton simulation. This project leverages multithreading to enhance performance and efficiency, allowing the simulation to run concurrently across multiple threads. It demonstrates the use of thread synchronization and coordination to update the game grid, showcasing principles of parallel computing and concurrency control within an operating systems context.
