import llvmlite.ir as ll

from soda.internals.wrapper import BaseType


# --- Void --- #

class VoidType(BaseType):
    base_llvm_type = ll.IntType(8)
    size_in_bits = 0
    is_void = True
    str_repr = "void"


# --- Boolean --- #

class BoolType(BaseType):
    base_llvm_type = ll.IntType(1)
    size_in_bits = 1
    is_bool_type = True
    str_repr = "bool"


# --- Signed Integer Types --- #

class I8Type(BaseType):
    base_llvm_type = ll.IntType(8)
    size_in_bits = 8
    is_signed_integer = True
    str_repr = "i8"


class I16Type(BaseType):
    base_llvm_type = ll.IntType(16)
    size_in_bits = 16
    is_signed_integer = True
    str_repr = "i16"


class I32Type(BaseType):
    base_llvm_type = ll.IntType(32)
    size_in_bits = 32
    is_signed_integer = True
    str_repr = "i32"


class I64Type(BaseType):
    base_llvm_type = ll.IntType(64)
    size_in_bits = 64
    is_signed_integer = True
    str_repr = "i64"


class I128Type(BaseType):
    base_llvm_type = ll.IntType(128)
    size_in_bits = 128
    is_signed_integer = True
    str_repr = "i128"


# --- Unsigned Integer Types --- #

class U8Type(BaseType):
    base_llvm_type = ll.IntType(8)
    size_in_bits = 8
    is_unsigned_integer = True
    str_repr = "u8"

class U16Type(BaseType):
    base_llvm_type = ll.IntType(16)
    size_in_bits = 16
    is_unsigned_integer = True
    str_repr = "u16"


class U32Type(BaseType):
    base_llvm_type = ll.IntType(32)
    size_in_bits = 32
    is_unsigned_integer = True
    str_repr = "u32"


class U64Type(BaseType):
    base_llvm_type = ll.IntType(64)
    size_in_bits = 64
    is_unsigned_integer = True
    str_repr = "u64"


class U128Type(BaseType):
    base_llvm_type = ll.IntType(128)
    size_in_bits = 128
    is_unsigned_integer = True
    str_repr = "u128"


# --- Floating Point Type --- #

class F32Type(BaseType):
    base_llvm_type = ll.FloatType()
    size_in_bits = 32
    is_floating_point = True
    str_repr = "f32"


class F64Type(BaseType):
    base_llvm_type = ll.DoubleType()
    size_in_bits = 64
    is_floating_point = True
    str_repr = "f64"


types = {"u8": U8Type, "u16": U16Type, "u32": U32Type, "u64": U64Type, "u128": U128Type,
         "i8": I8Type, "i16": I16Type, "i32": I32Type, "i64": I64Type, "i128": I128Type,
         "f32": F32Type, "f64": F64Type, "void": VoidType,
         "bool": BoolType}
