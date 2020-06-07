	.text
	.file	"<string>"
	.globl	v                       # -- Begin function v
	.p2align	4, 0x90
	.type	v,@function
v:                                      # @v
# %bb.0:                                # %v
	movl	%edi, %eax
	retq
.Lfunc_end0:
	.size	v, .Lfunc_end0-v
                                        # -- End function
	.globl	main                    # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
# %bb.0:                                # %main
	movl	$10, %eax
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
                                        # -- End function

	.section	".note.GNU-stack","",@progbits
