
# Distributed Checkpointing Simulator

## Project Overview

The Distributed Checkpointing Simulator is a Python-based desktop application that demonstrates the basic concepts of checkpointing, process failure, and rollback recovery in distributed systems.

The application provides an interactive graphical user interface (GUI) built using Tkinter. It simulates multiple processes, allows users to execute operations, send messages, save checkpoints, simulate failures, and restore processes to a previously saved state.

## Features

- Interactive graphical user interface using Tkinter
- Simulation of three distributed processes: P1, P2, and P3
- Process execution and counter management
- Message passing between processes
- Checkpoint creation and state saving
- Process failure simulation
- Rollback recovery from a saved checkpoint
- Event log for tracking simulation activities
- Automatic checkpoint storage in JSON format
- Reset functionality to restart the simulation

## Technologies Used

- Programming Language: Python
- GUI Framework: Tkinter
- Data Storage: JSON
- Development Environment: Visual Studio Code

## Project Structure

```text
DistributedCheckpointingSimulator/
│
├── main.py
├── README.md
└── checkpoints.json
```

Note: `checkpoints.json` is created automatically when a checkpoint is saved.

## Requirements

- Python 3.10 or later recommended
- Visual Studio Code or another Python editor
- Tkinter library

Tkinter and JSON are included with most standard Python installations.

## Installation and Setup

### Step 1: Install Python

Download Python from:

https://www.python.org/downloads/

During installation on Windows, enable the option to add Python to PATH.

### Step 2: Open the Project

1. Open Visual Studio Code.
2. Select File → Open Folder.
3. Open the `DistributedCheckpointingSimulator` folder.
4. Make sure `main.py` is inside the folder.

### Step 3: Run the Application

Open the VS Code terminal and execute:

```bash
python main.py
```

Alternatively, on Windows, use:

```bash
py main.py
```

The simulator window will open.

## How to Use

### 1. Execute Process

Select a process and click **Execute Process** to increment its operation counter.

### 2. Send Message

Select a running process and click **Send Message** to simulate message passing to another running process.

### 3. Create Checkpoint

Click **Create Checkpoint** to save the current states of all processes and the message history.

The checkpoint information is also saved to `checkpoints.json`.

### 4. Simulate Failure

Select a process and click **Simulate Failure** to mark it as failed.

### 5. Rollback Recovery

Click **Rollback Recovery** to restore all processes to the most recently created checkpoint.

### 6. Reset Simulation

Click **Reset Simulation** to reset process states and remove the current checkpoint.

## Checkpointing and Recovery

Checkpointing saves the state of a system at a particular point in time. If a failure occurs, the system can restore its saved state instead of starting from the beginning.

In this project:

1. Process states are maintained in memory.
2. A checkpoint captures the current state of all three processes.
3. A simulated failure changes a process status to Failed.
4. Rollback recovery restores all processes from the saved checkpoint.
5. The restored processes continue from their saved counters and message counts.

## Limitations

- The application simulates distributed processes within a single Python program.
- It does not use real network connections or multiple computers.
- It implements a simplified global checkpoint and rollback mechanism.
- It does not implement advanced distributed checkpointing algorithms or message-consistency protocols.

## Future Enhancements

- Add real communication between processes using sockets.
- Implement coordinated checkpointing algorithms.
- Add multiple checkpoint history and selection.
- Introduce random process failures.
- Visualize process communication and recovery.
- Add checkpoint loading after application restart.

## Conclusion

The Distributed Checkpointing Simulator demonstrates the fundamental principles of checkpoint creation, process failure, and rollback recovery through an interactive Python GUI.

It provides a simple environment for understanding how saved states can help recover a simulated distributed system after a failure.

## Author

MCA Student

## License

This project is intended for educational and academic purposes.
