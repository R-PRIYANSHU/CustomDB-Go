package BTreeImplement

import (
	"bytes"
)

// add a new key to a leaf node
func leafInsert(
    new BTNode, old BTNode, idx uint16,
    key []byte, val []byte,
) {
    new.setHeader(BTNode_LEAF, old.nkeys()+1)
    nodeAppendRange(new, old, 0, 0, idx)
    nodeAppendKV(new, idx, 0, key, val)
    nodeAppendRange(new, old, idx + 1, idx, old.nkeys() - idx)
}

func leafUpdate(new BTNode, old BTNode, idx uint16, key []byte, val []byte) {
    new.setHeader(BTNode_LEAF, old.nkeys())
    nodeAppendRange(new, old, 0, 0, idx)
    nodeAppendKV(new, idx, 0, key, val)
    nodeAppendRange(new, old, idx + 1, idx + 1, old.nkeys() - idx - 1)
}

// insert a KV into a node, the result might be split into 2 nodes.
// the caller is responsible for deallocating the input node
// and splitting and allocating result nodes.
func treeInsert(tree *BTree, node BTNode, key []byte, val []byte) BTNode {
    // the result node, 
    // it's allowed to be greater than one page and will be splitted if so
    new := BTNode{Data: make([]byte, 2 * BTREE_PAGE_SIZE)}

    // where to insert the key
    idx := nodeLookLE(node, key)
    // act based on node type
    switch node.btype() {
    case BTNode_LEAF: 
        // leaf, node.getKey(idx) <= key
        if bytes.Equal(key, node.getKey(idx)) {
            leafUpdate(new, node, idx, key, val)
        } else {
            leafInsert(new, node, idx + 1, key, val)
        }
    case BTNode_NODE:
        nodeInsert(tree, new, node, idx, key, val)
    default:
        panic("unrecognized node type")
    }
    return new
}

func nodeInsert(
    tree *BTree, new BTNode, node BTNode, 
    idx uint16, key []byte, val []byte,
) {
    // Get and deallocate the kid node
    kptr := node.getPtr(idx)
    knode := tree.Get(kptr)
    tree.Del(kptr)
    // recursive insertion to the kid node
    knode = treeInsert(tree, knode, key, val)
    // split the result
    nsplit, splited := nodeSplit3(knode)
    // update the kid links
    nodeReplaceKidN(tree, new, node, idx, splited[:nsplit]...)
}

