import llvmlite.ir as ll

from mini.internals.wrapper import BaseType


# --- Boolean --- #

class BoolType(BaseType):
    llvm_type = ll.IntType(1)
    size_in_bits = 1
    is_bool_type = True

    def __str__(self):
        return "bool"


# --- Signed Integer Types --- #

class I8Type(BaseType):
    llvm_type = ll.IntType(8)
    size_in_bits = 8
    is_signed_integer = True

    def __str__(self):
        return "i8"


class I16Type(BaseType):
    llvm_type = ll.IntType(16)
    size_in_bits = 16
    is_signed_integer = True

    def __str__(self):
        return "i16"


class I32Type(BaseType):
    llvm_type = ll.IntType(32)
    size_in_bits = 32
    is_signed_integer = True

    def __str__(self):
        return "i32"


class I64Type(BaseType):
    llvm_type = ll.IntType(64)
    size_in_bits = 64
    is_signed_integer = True

    def __str__(self):
        return "i64"


class I128Type(BaseType):
    llvm_type = ll.IntType(128)
    size_in_bits = 128
    is_signed_integer = True

    def __str__(self):
        return "i128"


# --- Unsigned Integer Types --- #

class U8Type(BaseType):
    llvm_type = ll.IntType(8)
    size_in_bits = 8
    is_unsigned_integer = True

    def __str__(self):
        return "u8"


class U16Type(BaseType):
    llvm_type = ll.IntType(16)
    size_in_bits = 16
    is_unsigned_integer = True

    def __str__(self):
        return "u16"


class U32Type(BaseType):
    llvm_type = ll.IntType(32)
    size_in_bits = 32
    is_unsigned_integer = True

    def __str__(self):
        return "u32"


class U64Type(BaseType):
    llvm_type = ll.IntType(64)
    size_in_bits = 64
    is_unsigned_integer = True

    def __str__(self):
        return "u64"


class U128Type(BaseType):
    llvm_type = ll.IntType(128)
    size_in_bits = 128
    is_unsigned_integer = True

    def __str__(self):
        return "u128"


# --- Floating Point Type --- #

class F32Type(BaseType):
    llvm_type = ll.FloatType()
    size_in_bits = 32
    is_floating_point = True

    def __str__(self):
        return "f32"


class F64Type(BaseType):
    llvm_type = ll.DoubleType()
    size_in_bits = 64
    is_floating_point = True

    def __str__(self):
        return "f64"


types = {"u8": U8Type, "u16": U16Type, "u32": U32Type, "u64": U64Type, "u128": U128Type,
         "i8": I8Type, "i16": I16Type, "i32": I32Type, "i64": I64Type, "i128": I128Type,
         "f32": F32Type, "f64": F64Type,
         "bool": BoolType}
