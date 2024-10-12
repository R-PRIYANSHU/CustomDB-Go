package BTreeImplement

import "bytes"

// get a key from tree
func treeGet(tree *BTree, node BTNode, key[]byte) ([]byte, bool) {
    idx := nodeLookLE(node, key)

    switch node.btype() {
    case BTNode_LEAF:
        if bytes.Equal(key, node.getKey(idx)) {
            return node.getVal(idx), true
        } else {
            return nil, false // not found
        }
    case BTNode_NODE:
        childNode := tree.Get(node.getPtr(idx))
        return treeGet(tree, childNode, key)
    default:
        panic("unrecognized node type")
    }
}
