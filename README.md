# CustomDB-Go

A simple key-value store database implemented in Go.

## Overview

This project implements a basic key-value store using a B-tree for indexing. It utilizes memory mapping for efficient disk access and supports basic operations like `Get`, `Set`, and `Delete`.

## Features

* **B-tree indexing:** Efficiently stores and retrieves key-value pairs.
* **Memory mapping:**  Uses `mmap` for fast disk access.
* **Basic operations:** Supports `Get`, `Set`, and `Delete` operations.
* **Page management:** Implements page allocation, deallocation, and persistence.
* **Master page:** Stores metadata like the root of the B-tree and used page count.

