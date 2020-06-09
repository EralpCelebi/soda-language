from soda.internals.wrapper import *


def CastTo(target, value, state, span):
    temp = None
    if target.isPointer() or value.isPointer():
        if target.getPointerDepth() == value.getPointerDepth():
            temp = PointerCastTo(target, value, state, span)
        else:
            state.error_handler(f"Can't cast {value.getWrappedType()} to "\
                f"{target}", span)

    elif not target.isPointer() and not value.isPointer():
        temp = TypeCastTo(target, value, state, span)

    else:
        state.error_handler(f"Can't cast {value.getWrappedType()} to "\
                f"{target}", span)
    return temp


# TODO Maybe tidy this up a bit.
def TypeCastTo(target, value, state, span):
    temp = value
    temp_value_size = value.getSizeInBits()
    temp_target_size = target.getSizeInBits()

    if target is not temp.getWrappedType():
        # * -type- To Signed (Extension / Truncation / Casting)
        if hasattr(target, "is_signed_integer"):
            if hasattr(value.getWrappedType(), "is_signed_integer"):

                if temp_value_size > temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.trunc(value.getLLVMValue(),
                                                                        target.getLLVMType()))
                elif temp_value_size < temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.sext(value.getLLVMValue(),
                                                                       target.getLLVMType()))
                else:
                    pass

            elif hasattr(value.getWrappedType(), "is_unsigned_integer"):
                if temp_value_size > temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.trunc(value.getLLVMValue(),
                                                                        target.getLLVMType()))
                elif temp_value_size < temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.zext(value.getLLVMValue(),
                                                                       target.getLLVMType()))
                else:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=value.getLLVMValue())

            elif hasattr(value.getWrappedType(), "is_floating_point"):
                temp = InternalValue(wrapped_type=target,
                                     llvm_value=state.builder.fptosi(value=value.getLLVMValue(),
                                                                     typ=target.getLLVMType()))

            elif hasattr(value.getWrappedType(), "is_bool_type"):
                temp = InternalValue(wrapped_type=target,
                                     llvm_value=state.builder.zext(value.getLLVMValue(),
                                                                    target.getLLVMType()))

        # * -type- To Unsigned (Extension / Truncation / Casting)
        elif hasattr(target, "is_unsigned_integer") or hasattr(target, "is_bool_type"):

            if hasattr(value.getWrappedType(), "is_signed_integer"):
                if temp_value_size > temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.trunc(value.getLLVMValue(),
                                                                        target.getLLVMType()))
                elif temp_value_size < temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.sext(value.getLLVMValue(),
                                                                       target.getLLVMType()))
                else:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=value.getLLVMValue())

            elif hasattr(value.getWrappedType(), "is_unsigned_integer"):
                if temp_value_size > temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.trunc(value.getLLVMValue(),
                                                                        target.getLLVMType()))
                elif temp_value_size < temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.zext(value.getLLVMValue(),
                                                                       target.getLLVMType()))
                else:
                    pass

            elif hasattr(value.getWrappedType(), "is_floating_point"):
                temp = InternalValue(wrapped_type=target,
                                     llvm_value=state.builder.fptoui(value=value.getLLVMValue(),
                                                                     typ=target.getLLVMType()))

            elif hasattr(value.getWrappedType(), "is_bool_type"):
                if temp_value_size < temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.zext(value.getLLVMValue(),
                                                                       target.getLLVMType()))
        # * -type- To Float (Extension / Truncation / Casting)

        elif hasattr(target, "is_floating_point"):
            if hasattr(value.getWrappedType(), "is_signed_integer"):
                temp = InternalValue(wrapped_type=target,
                                     llvm_value=state.builder.sitofp(value.getLLVMValue(),
                                                                     target.getLLVMType()))

            elif hasattr(value.getWrappedType(), "is_unsigned_integer"):
                temp = InternalValue(wrapped_type=target,
                                     llvm_value=state.builder.uitofp(value.getLLVMValue(),
                                                                     target.getLLVMType()))

            elif hasattr(value.getWrappedType(), "is_floating_point"):
                if temp_value_size > temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.fptrunc(value.getLLVMValue(),
                                                                          target.getLLVMType()))

                elif temp_value_size < temp_target_size:
                    temp = InternalValue(wrapped_type=target,
                                         llvm_value=state.builder.fpext(value.getLLVMValue(),
                                                                        target.getLLVMType()))

            elif hasattr(value.getWrappedType(), "is_bool_type"):
                temp = InternalValue(wrapped_type=target,
                                     llvm_value=state.builder.fptoui(value.getLLVMValue(),
                                                                     target.getLLVMType()))

        else:
            state.error_handler(f"Can't cast {value.getWrappedType()} " +
                                f"to {target}"
                                , span)

    return temp


def PointerCastTo(target, value, state, span):
    temp = value
    temp_llvm_value = None

    if not target == value.getWrappedType():
        temp_llvm_value = state.builder.bitcast(value.getLLVMValue(), target.getLLVMType())
        temp = InternalValue(wrapped_type=target,
                         llvm_value=temp_llvm_value)
        
    return temp