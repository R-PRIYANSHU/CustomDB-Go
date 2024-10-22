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
├── Code
│   ├── BTreeImplement
│   │   ├── BTree.go
│   │   ├── Commons.go
│   │   ├── Delete.go
│   │   ├── Get.go
│   │   └── Insert.go
│   ├── KVStoreImplement
│   │   ├── KVStore.go
│   │   ├── KVUtils.go
│   │   └── Master.go
│   └── Utils
│       └── Utils.go
├── Sqlite.db
├── go.mod
├── go.sum
├── main.go
└── tree.py
```
