package BTreeImplement

import (
	"bytes"
	"github.com/ayush-git-hub/CustomDB/Code/Utils"
)

// remove a key from a leaf node
func leafDelete(New BTNode, old BTNode, idx uint16) {
    New.setHeader(old.btype(), old.nkeys() - 1)
    nodeAppendRange(New, old, 0, 0, idx)
    nodeAppendRange(New, old, idx, idx + 1, old.nkeys() - idx - 1)
}

// delete a key from the tree
func treeDelete(tree *BTree, node BTNode, key []byte) BTNode {
    idx := nodeLookLE(node, key)
    switch node.btype() {
    case BTNode_LEAF:
        if !bytes.Equal(key, node.getKey(idx)) {
            return BTNode{} // key does not exist
        }
        New := BTNode{Data: make([]byte, BTREE_PAGE_SIZE)}
        leafDelete(New, node, idx)
        return New
    case BTNode_NODE:
        return nodeDelete(tree, node, idx, key)
    default:
        panic("unknown BTNode type")
    }
}

// delete a node from internal node
func nodeDelete(tree *BTree, node BTNode, idx uint16, key []byte) BTNode {
    ptr := node.getPtr(idx)
    updated := treeDelete(tree, tree.Get(ptr), key)
    if len(updated.Data) == 0 {
        return BTNode{} // key does not exist
    }
    tree.Del(ptr)
    
    New := BTNode{Data: make([]byte, BTREE_PAGE_SIZE)}
    // check for merging
    mergeDir, sibling := shouldMerge(tree, node, idx, updated)
    switch {
    case mergeDir < 0: // left
        merged := BTNode{Data: make([]byte, BTREE_PAGE_SIZE)}
        nodeMerge(merged, sibling, updated)
        tree.Del(node.getPtr(idx - 1))
        nodeReplace2Kid(New, node, idx - 1, tree.New(merged), merged.getKey(0))
    case mergeDir > 0: // right
        merged := BTNode{Data: make([]byte, BTREE_PAGE_SIZE)}
        nodeMerge(merged, updated, sibling)
        tree.Del(node.getPtr(idx + 1))
        nodeReplace2Kid(New, node, idx, tree.New(merged), merged.getKey(0))
    case mergeDir == 0: // no merge needed
        Utils.Assert(updated.nkeys() > 0)
        nodeReplaceKidN(tree, New, node, idx, updated)
    }
    return New
}

// sizeof(merge(left, right)) <= BTREE_PAGE_SIZE, this condition
// must be checked by the caller
func nodeMerge(merged BTNode, left BTNode, right BTNode) {
    Utils.Assert(left.btype() == right.btype())
    merged.setHeader(left.btype(), left.nkeys() + right.nkeys())
    nodeAppendRange(merged, left, 0, 0, left.nkeys())
    nodeAppendRange(merged, right, left.nkeys(), 0, right.nkeys())
}

// can be merged as long as these two conditions suffice
// 1. node size is less than 1/4 of a page
// 2. has sibling and merge size is less than a page size
func shouldMerge(
    tree *BTree, node BTNode, 
    idx uint16, updated BTNode,
) (int, BTNode) {
    if updated.nbytes() > BTREE_PAGE_SIZE / 4 {
        return 0, BTNode{}
    }
    if idx > 0 {
        leftChildPtr := node.getPtr(idx - 1)
        leftChildNode := tree.Get(leftChildPtr)
        merged := leftChildNode.nbytes() + updated.nbytes() - HEADER
        if merged <= BTREE_PAGE_SIZE {
            return -1, leftChildNode
        }
    }
    if idx < node.nkeys() - 1 {
        rightChildPtr := node.getPtr(idx + 1)
        rightChildNode := tree.Get(rightChildPtr)
        merged := rightChildNode.nbytes() + updated.nbytes() - HEADER
        if merged <= BTREE_PAGE_SIZE {
            return +1, rightChildNode
        }
    }
    return 0, BTNode{}
}
