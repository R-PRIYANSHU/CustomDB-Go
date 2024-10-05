package Utils

func Assert(val bool) {
    if (!val) {
        panic("assertion failed");
    }
}
