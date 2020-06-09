; ModuleID = '.\example\test.soda'
source_filename = "<string>"
target triple = "i686-pc-windows-msvc"

; Function Attrs: norecurse nounwind readonly
define i32 @main() local_unnamed_addr #0 {
main:
  %.6 = load i32, i32* inttoptr (i32 800 to i32*), align 32
  ret i32 %.6
}

attributes #0 = { norecurse nounwind readonly }
