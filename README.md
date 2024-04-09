# Connect 4 Application in the Blackboard and C2 Architecture

## 1. Compilation & Implementation Platform

### Platform Version & Download Instructions
This project is developed and tested with Python 3.10

You can download Python from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation & Configuration
After downloading the installer for your operating system (Windows, macOS, Linux/UNIX), run the installer and follow the
on-screen instructions. Ensure you select the option to add Python to your PATH environment variable to execute Python
from the command line.

The only dependent library is tkinter, to download this either let your python IDE (if available) install it for you, or
navigate to the python command line and run
```bash
pip install tkinter
```

## 2. Compilation
Python is an interpreted language, so you do not need to compile the code before execution.


## 3. How to Execute Your System
To run the main script of this project, navigate to the project directory in your terminal or command prompt.
From this directory, to run the blackboard version run:
```bash
python Selected/blackboard_concurrent.py
```

To run the C2 version, run
```bash
python Selected/C2_concurrent.py
```

Note that these concurrent scripts are the same as what is located in the unselected portions, however every class is instead compiled into one script rather than being seperated out by files and imported.

## 4. Architectural Design Choices

When designing the architecture for our Python-based Connect4 game, we evaluated several architectural styles. Our primary goal was to ensure that the architecture supported modularity, ease of maintenance, scalability, and a clean separation of concerns.

### Blackboard Architecture

The **Blackboard Architecture** was initially considered due to its flexibility in integrating diverse problem-solving modules. This architecture style revolves around a shared knowledge base (the "blackboard") where different components read from and write to. It's particularly well-suited for problems where the solution emerges from the incremental contributions of diverse subsystems. In our case, the gradual process to complete a game using the same board and starting variables allows it to work well with the architecture.

- **Pros**:
  - Facilitates the integration of diverse algorithms or modules.
  - Incremental solution building allows for dynamic adaptation.
- **Cons**:
  - Complexity in managing the central knowledge base, especially with concurrent accesses.
  - Correctly calling and limiting access to the blackboard to when its only necessary is very complex.
  - Tight coupling between the problem-solving components and the blackboard structure.

For a game like Connect4, where the state of the game board is central, the Blackboard architecture initially seemed appealing for managing game state and integrating different AI strategies.

### C2 Architectural Style

The **C2 Architectural Style** is a component-based architecture designed for networked and interactive systems, emphasizing loosely coupled components that communicate through asynchronous message passing. Components in a C2 architecture are organized in a hierarchical manner, and communication occurs via connectors, facilitating a decoupled interaction model that enhances modularity and scalability. In the case for Connect 4, our many different parts seemed like they could work well from all being defined in the beginning and called upon if the event needed them.

- **Pros**:
  - Decoupled Components: Each component, such as game logic, AI algorithms, or UI, operates independently and does not need access to a central data structure, instead communicating through well-defined messages. This separation allows for easy modification of one component without affecting others.
  - Asynchronous Communication: Fits well with event-driven applications like games, where user actions or AI decisions trigger changes in the game state.
  - Scalability: Components can be added or removed easily, allowing for future expansion, such as adding new AI strategies or multiplayer features if we were to take this to further development.
- **Cons**:
  - Requires careful design of message protocols to ensure clarity in communication between components.
  - Potentially more overhead in managing asynchronous messages compared to direct method calls in more tightly coupled architectures.
  - Publishing many different messages to complete a simple task that could be handled by one or 2 more tightly couples things is wasteful.


### Implementations
Ultimately, we decided on the blackboard and C2 style over other architectures due to their ability to integrate well with the system we were developing. By allowing for any number of components to operate separately yet smoothly these architectures seemed to be ideal. The **blackboard style** offers dynamic strategy development, making it ideal for games where AI complexity and adaptability are paramount. Because all components operate off this one set of data, it was easy to develop many different components and pass the same data onto them all. The **C2 Architectural Style** was selected for the second implementation because it focused on modularity, event-driven interactions, and the decoupling of components. C2's hierarchical, message-passing model is ideal for interactive applications like games, where user actions trigger updates to the game state and UI and the overall game process occurs in a hierarchical manner.
