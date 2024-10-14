package BTreeImplement

import (
	"encoding/binary"
	"github.com/ayush-git-hub/CustomDB/Code/Utils"
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

func offsetPosition(node BTNode, idx uint16) uint16 {
    Utils.Assert(1 <= idx && idx <= node.nkeys())
    nkeys := node.nkeys()
    return HEADER + nkeys * 8 + (idx - 1) * 2
}

func (node BTNode) getOffset(idx uint16) uint16 {
    if idx == 0 {
        return 0
    }
    position := offsetPosition(node, idx)
    return binary.LittleEndian.Uint16(node.Data[position:])
}

func (node BTNode) setOffset(idx uint16, offset uint16) {
    position := offsetPosition(node, idx)
    binary.LittleEndian.PutUint16(node.Data[position:], offset)
}

// key-values
// kVPosition(nkeys) returns the size of Data
func (node BTNode) kVPosition(idx uint16) uint16 {
    Utils.Assert(idx <= node.nkeys())
    return HEADER + node.nkeys() * 8 + node.nkeys() * 2 + node.getOffset(idx)
}

func (node BTNode) getKey(idx uint16) []byte {
    Utils.Assert(idx < node.nkeys())
    kvPosition := node.kVPosition(idx)
    keyLength := binary.LittleEndian.Uint16(node.Data[kvPosition:])
    return node.Data[kvPosition+4:][:keyLength]
}

func (node BTNode) getVal(idx uint16) []byte {
    Utils.Assert(idx < node.nkeys())
    kvPosition := node.kVPosition(idx)
    keyLength := binary.LittleEndian.Uint16(node.Data[kvPosition:])
    valLength := binary.LittleEndian.Uint16(node.Data[kvPosition + 2:])
    return node.Data[kvPosition+4+keyLength:][:valLength]
}

func (node BTNode) nbytes() uint16 {
    return node.kVPosition(node.nkeys())
}

// Return true if btree successfully deleted a key
// The btree will shrink if these two conditions satisfied:
// 1. The Root node is not a leaf.
// 2. The Root node has only one child.
func (tree *BTree) DeleteKey(key []byte) bool {
    Utils.Assert(len(key) != 0)
    Utils.Assert(len(key) <= BTREE_MAX_KEY_SIZE)
    
    if tree.Root == 0 {
        return false
    }
    updated := treeDelete(tree, tree.Get(tree.Root), key)
    if len(updated.Data) == 0 {
        return false // not found
    }
    tree.Del(tree.Root)
    
    if updated.btype() == BTNode_NODE && updated.nkeys() == 1 {
        tree.Root = updated.getPtr(0)
    } else {
        tree.Root = tree.New(updated)
    }
    return true
}

// Return true if btree successfully inserted the key, val pair
func (tree *BTree) Insertion(key []byte, val []byte) {
    Utils.Assert(len(key) != 0)
    Utils.Assert(len(key) <= BTREE_MAX_KEY_SIZE)
    Utils.Assert(len(val) <= BTREE_MAX_VALUE_SIZE)
    
    if tree.Root == 0 {
        // first key ever possible
        Root := BTNode{Data: make([]byte, BTREE_PAGE_SIZE)}

        // create a dummy node to pass LE check
        Root.setHeader(BTNode_LEAF, 2)
        nodeAppendKV(Root, 0, 0, nil, nil)
        nodeAppendKV(Root, 1, 0, key, val)
        tree.Root = tree.New(Root)
        return
    }
    
    Root := tree.Get(tree.Root)
    tree.Del(tree.Root)

    newRoot := treeInsert(tree, Root, key, val)
    nsplit, splited := nodeSplit3(newRoot)
    if nsplit > 1 {
        finalRoot := BTNode{Data: make([]byte, BTREE_PAGE_SIZE)}
        finalRoot.setHeader(BTNode_NODE, nsplit)
        for i, node := range splited[:nsplit] {
            nodeAppendKV(
                finalRoot, uint16(i),
                tree.New(node), node.getKey(0), nil,
            )
        }
        tree.Root = tree.New(finalRoot)
    } else {
        tree.Root = tree.New(splited[0])
    }
}

func (tree *BTree) GetKey(key []byte) ([]byte, bool) {
    Utils.Assert(len(key) != 0)
    Utils.Assert(len(key) <= BTREE_MAX_KEY_SIZE)
    if tree.Root == 0 {
        return []byte(nil), false
    }
    root := tree.Get(tree.Root)
    return treeGet(tree, root, key)
}
