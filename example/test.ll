; ModuleID = '<string>'
source_filename = "<string>"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: norecurse nounwind readnone
define i32 @f(i32 returned %.1) local_unnamed_addr #0 {
f:
  ret i32 %.1
}

; Function Attrs: norecurse nounwind readnone
define i32 @main() local_unnamed_addr #0 {
main:
  ret i32 21
}

attributes #0 = { norecurse nounwind readnone }
