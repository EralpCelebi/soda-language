from copy import deepcopy

from soda.internals.types import *

import llvmlite.ir as ll
import llvmlite.binding as llvm


class BaseType:
    llvm_type = None
    size_in_bits = 0

    def __init__(self, span=None, depth=0):
        self.pointer_depth = depth
        self.span = span

    def getLLVMType(self):
        if self.pointer_depth != 0:
            for _ in range(self.pointer_depth):
                self.llvm_type = self.llvm_type.as_pointer()

        return self.llvm_type

    def getLLVMBaseType(self):
        return self.llvm_type

    def getSizeInBits(self):
        return self.size_in_bits

    def isPointer(self):
        if self.pointer_depth != 0:
            return True
        else:
            return False

    def getPointerDepth(self):
        return self.pointer_depth

    def setPointerDepth(self, value):
        self.pointer_depth = value

    def addPointerDepth(self, value=1):
        self.pointer_depth += value

    def getMemoryLLVMType(self):
        self.addPointerDepth(-1)
        temp = self.getLLVMType()
        self.addPointerDepth()
        return temp

    def getMemoryWrappedType(self):
        temp = deepcopy(self)
        temp.addPointerDepth(-1)
        return temp

    def __eq__(self, other):
        return type(self) == type(other)


class InternalValue:
    def __init__(self, wrapped_type, llvm_value=None, python_value=None, span=None):
        self.python_value = python_value
        self.llvm_value = llvm_value

        self.wrapped_type = deepcopy(wrapped_type)
        self.llvm_type = None

        self.span = span

        self.is_variable = False
        self.is_argument = True

        self.is_used = True

    def getLLVMValue(self):
        if self.llvm_value is None:
            self.llvm_value = self.getLLVMType()(self.python_value)

        return self.llvm_value

    def getWrappedType(self):
        return self.wrapped_type

    def setWrappedType(self, value):
        self.wrapped_type = value

    def getLLVMType(self):
        return self.wrapped_type.getLLVMType()

    def getLLVMBaseType(self):
        return self.wrapped_type.getLLVMBaseType()

    def getSizeInBits(self):
        return self.wrapped_type.getSizeInBits()

    def isPointer(self):
        return self.wrapped_type.isPointer()

    def getPointerDepth(self):
        return self.wrapped_type.getPointerDepth()

    def setPointerDepth(self, value):
        self.wrapped_type.pointer_depth = value

    def addPointerDepth(self, value=1):
        self.wrapped_type.addPointerDepth(value)

    def getMemoryLLVMType(self):
        return self.getWrappedType().getMemoryLLVMType()

    def getMemoryWrappedType(self):
        return self.getWrappedType().getMemoryWrappedType()

    def markVariable(self):
        self.is_variable = True
        self.is_used = False

    def markArgument(self):
        self.is_argument = True
        self.is_used = False

    def isArgument(self):
        return self.is_used

    def isVariable(self):
        return self.is_variable

    def markUsed(self):
        self.is_used = True

    def isUsed(self):
        return self.is_used

    def getSpan(self):
        return self.span


class InternalModuleLLVM:
    def __init__(self, state):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        llvm.initialize_all_asmprinters()

        self.mod_pass_manager = llvm.create_module_pass_manager()
        llvm.create_pass_manager_builder().populate(self.mod_pass_manager)

        self.module = ll.Module(name=str(state.current_file))
        self.module.triple = llvm.get_default_triple()

        state.module = self.module

    def build(self):
        mod = llvm.parse_assembly(str(self.module))
        mod.verify()

        result = self.mod_pass_manager.run(mod)

        return str(mod)


def CreateSIntFromSize(size):
    if size is 1:
        return I8Type()
    elif size is 2:
        return I16Type()
    elif size is 4:
        return I32Type()
    elif size is 8:
        return I64Type()
    elif size is 16:
        return I128Type()


def CreateUIntFromSize(size):
    if size is 1:
        return U8Type()
    elif size is 2:
        return U16Type()
    elif size is 4:
        return U32Type()
    elif size is 8:
        return U64Type()
    elif size is 16:
        return U128Type()


def CreateFPFromSize(size):
    if size is 4:
        return F32Type()
    elif size is 8:
        return F64Type()
