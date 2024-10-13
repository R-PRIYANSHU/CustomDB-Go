package BTreeImplement

import (
)


// Structure of BTree Node 
// BTree node basic structure, we use same structures for 
// internal node
// +--------+------------+------------+------------+------------+------------+------------+
// | Header | Pointer 1   | Pointer 2  | Pointer 3  | Pointer 4  | ...        | Pointer N  |
// +--------+------------+------------+------------+------------+------------+------------+
// | 4 bytes| 8 bytes     | 8 bytes    | 8 bytes    | 8 bytes    | ...        | 8 bytes    |
// +--------+------------+------------+------------+------------+------------+------------+
//                           Keys Section
// +----------------+----------------+----------------+----------------+----------------+
// | Key 1          | Key 2          | Key 3          | Key 4          | ...            |
// +----------------+----------------+----------------+----------------+----------------+
// | Variable bytes | Variable bytes | Variable bytes | Variable bytes | ...            |
// +----------------+----------------+----------------+----------------+----------------+
//&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
// leaf node.
// | type | nkeys | pointers    | offsets   | key-values
// | 2B   | 2B    |  nkeys * 8B | nkeys * 2B| ...

// | klen | vlen  |  key |  val |
// | 2B   | 2B    | ...  |  ... |

type BTNode struct {
    Data []byte // can be dumped to disk
}

const (
    BTNode_NODE = 1 // internal node without value
    BTNode_LEAF = 2 // leaf node with value
)

const (
    HEADER = 4 // type + nkeys
    BTREE_PAGE_SIZE = 4096
    BTREE_MAX_KEY_SIZE = 1000
    BTREE_MAX_VALUE_SIZE = 3000
)

type BTree struct {
    // pointer (a nonzero page number)
    Root uint64
    // callbacks for managing on-disk pages
    Get func(uint64) BTNode // dereference a pointer
    New func(BTNode) uint64 // allocate a New page
    Del func(uint64)       // deallocate a New page

    mockNodeList []BTNode   // for testing usage
}


func init() { 
    node1max := HEADER + 8 + 2 + 4 + BTREE_MAX_KEY_SIZE + BTREE_MAX_VALUE_SIZE
    Utils.Assert(node1max <= BTREE_PAGE_SIZE)
}

// decoding BTNode
// header 
func (node BTNode) btype() uint16 {
    return binary.LittleEndian.Uint16(node.Data)    
}

func (node BTNode) nkeys() uint16 {
    return binary.LittleEndian.Uint16(node.Data[2:4])
}

func (node BTNode) setHeader(btype uint16, nkeys uint16) {
    binary.LittleEndian.PutUint16(node.Data, btype)
    binary.LittleEndian.PutUint16(node.Data[2:4], nkeys)
}

// pointers
func (node BTNode) getPtr(idx uint16) uint64 {
    Utils.Assert(idx < node.nkeys())
    index := HEADER + idx * 8
    return binary.LittleEndian.Uint64(node.Data[index:])
}

func (node BTNode) setPtr(idx uint16, ptr uint64) {
    Utils.Assert(idx < node.nkeys());
    index := HEADER + idx * 8
    binary.LittleEndian.PutUint64(node.Data[index:], ptr);
}


// The offset is relative to the position of the first KV pair.
// The offset of the first KV pair is always zero, so it is not stored in the 
// list. 

// important: 
// We store the offset to the end of the last KV pair in the offset list,
// which is used to determine the size of the node.
// |1st node offset| ... |n - 1th node offset| end of node offset|
// there are n offset nums in offset list