# CustomDB-Go

A simple key-value store database implemented in Go.

<img src="https://miro.medium.com/v2/resize:fit:860/1*Y9G_TqTbTq2khs7L4j_9_w.png" alt="Go-Lang logo" width="300" height="200">


## Overview

This project implements a basic key-value store using a B-tree for indexing. It utilizes memory mapping for efficient disk access and supports basic operations like `Get`, `Set`, and `Delete`.

## Features

* **B-tree indexing:** Efficiently stores and retrieves key-value pairs.
* **Memory mapping:**  Uses `mmap` for fast disk access.
* **Basic operations:** Supports `Get`, `Set`, and `Delete` operations.
* **Page management:** Implements page allocation, deallocation, and persistence.
* **Master page:** Stores metadata like the root of the B-tree and used page count.

## Project Structure

```txt
.
├── Code
│   ├── BTreeImplement
│   │   ├── BTree.go       # Main B-Tree structure
│   │   ├── Commons.go     # Common utilities for B-Tree
│   │   ├── Delete.go      # Deletion functionality for B-Tree
│   │   ├── Get.go         # Retrieval functionality for B-Tree
│   │   └── Insert.go      # Insert functionality for B-Tree
│   ├── KVStoreImplement
│   │   ├── KVStore.go     # Key-Value store implementation
│   │   ├── KVUtils.go     # Utility functions for Key-Value store
│   │   └── Master.go      # Master control for Key-Value operations
│   └── Utils
│       └── Utils.go       # General utility functions
├── go.mod                 # Golang module information
├── go.sum                 # Dependency file
├── main.go                # Main entry point of the application
├── oldmain                # Archive of older code
└── Sqlite.db              # Sample SQLite database

```

## Installation

### Prerequisites
- **Golang**: Make sure Golang is installed on your machine (version 1.17 or higher).
- **Git**: Clone this repository.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/custom-sqlite-query-processor.git
   ```
2. Navigate to the project directory:
   ```bash
   cd custom-sqlite-query-processor
   ```
3. Install the dependencies:
   ```bash
   go mod tidy
   ```
4. Run the project:
   ```bash
   go run main.go
   ```

---

## Usage

- The B-Tree structure provides fast and efficient insert, delete, and search operations.
- The Key-Value store enables users to store and retrieve data in a key-value pair format.
- The backend is optimized to handle large datasets and complex queries.

### Example Commands:
```go
// Inserting a key-value pair into the B-Tree
Insert(key, value)

// Retrieving a value by key
Get(key)

// Deleting a key-value pair
Delete(key)

// Getall  function to retrieve all key-value pairs
GetAll()

```

---

## OOP Concepts Applied

- **Encapsulation**: Structs like `BTNode` encapsulate the data of B-tree nodes.
- **Abstraction**: B-tree and key-value store operations abstract the underlying data handling mechanisms.
- **Composition**: Go uses composition to reuse struct functionality instead of traditional inheritance.
- **Polymorphism**: Implemented through interfaces to allow different data structures to use the same operations.

---

