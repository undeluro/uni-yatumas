# Turing Machine Simulator 🖥️ (Lab from uni course)

The goal of this lab was to implement a visual interface for a Turing Machine simulator.

![Demo](demo.mp4)

## Introduction to Turing Machines 🧠

A Turing Machine is a mathematical model of computation introduced by Alan Turing in 1936. It consists of:
- An infinite tape divided into cells, each containing a symbol
- A head that can read and write symbols on the tape and move left or right
- A state register that stores the machine's current state
- A finite table of instructions that tells the machine what to do based on its current state and the symbol it reads

Despite its simplicity, Turing Machines can simulate any computer algorithm, making them foundational to computer science and computational theory.

## Features ✨

- **Customizable Turing Machines**: Define your own Turing Machines using configuration files.
- **Step-by-Step Simulation**: Visualize the execution of the machine step by step.
- **Terminal-Based Interface**: Runs directly in the terminal with a clean and interactive display.
- **Extensible Design**: Easily add new features or modify existing ones.

## Requirements 📋

- Python 3.11 or higher
- Required Python packages (listed in `requirements.txt`)

## Installation ⚙️

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage 🚀

Run the simulator with the following command:

```bash
python yatumas.py -m <machine-file> -i <interval> <input>
```

- `<machine-file>`: Path to the Turing Machine definition file.
- `<interval>`: Time interval (in seconds) between steps.
- `<input>`: Input string for the Turing Machine.

Example:
```bash
python yatumas.py -m examples/add_one.tm -i 0.1 10111
```

## Project Structure 📁

```
.
├── examples                        # Example Turing Machine definitions
├── yatumas                         # Core simulator code
│   ├── machine                     # Turing Machine logic
│   ├── parser                      # Parsing utilities
│   ├── simulator                   # Simulation components
├── requirements.txt                # Python dependencies
├── yatumas.py                      # Main entry point
└── README.md                       # Project documentation
```

## Contributing 🤝

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License 📄

This project is licensed under the MIT License. See `LICENSE` for details.