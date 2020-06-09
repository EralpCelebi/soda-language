# ### Bases ### #
import llvmlite.ir as ll

from soda.analysis.state import State
from soda.internals.casts import CastTo, deepcopy
from soda.internals.checks import *
from soda.internals.types import *
from soda.internals.wrapper import InternalValue


# ### Derivatives & Others ### #
# --- Program Structure --- #

class ProgramNode:
    def __init__(self, children):
        self.children = children

    def build(self, state):
        self.children.build(state)


class DefinitionsNode:
    def __init__(self, children):
        self.children = children

    def build(self, state):
        for child in self.children:
            child.build(state)


class FunctionsNode:
    def __init__(self, children):
        self.children = children

    def build(self, state):
        for child in self.children:
            child.build(state)


class ArgumentsNode:
    def __init__(self, children):
        self.children = children

    def build(self, state):
        for child in self.children:
            child.build(state)


class ClosureNode:
    def __init__(self, children):
        self.children = children

    def build(self, state):
        for child in self.children:
            child.build(state)
        # --- Checks --- #
        FindUnusedParameters(state)
        # --- Checks --- #


class StatementsNode:
    def __init__(self, children):
        self.children = children

    def build(self, state):
        for child in self.children:
            child.build(state)


# --- Definitions --- #

class FunctionNode:
    def __init__(self, span, return_type, name, args, closure):
        self.span = span.getsourcepos()
        self.return_type = return_type
        self.name = name.getstr()
        self.args = args
        self.closure = closure

    def build(self, state):
        internal_state = State().cloneState(state)
        internal_state.enter_function()

        # -- Checks -- #
        if self.name in internal_state.defined_functions.keys():
            internal_state.error_handler("Redefinition of function.", self.span)
        # -- Checks -- #

        self.args.build(internal_state)

        internal_state.current_function_return_type = self.return_type.build(internal_state)

        temp_return_llvm_type = internal_state.current_function_return_type.getLLVMType()
        temp_return_type = internal_state.current_function_return_type
        temp_argument_llvm_types = []
        temp_argument_types = []
        for arg_type in internal_state.current_function_argument_wrapped_types:
            temp_argument_llvm_types.append(arg_type.getLLVMType())
            temp_argument_types.append(arg_type)

        temp_function_type = ll.FunctionType(temp_return_llvm_type, temp_argument_llvm_types)
        temp_function = ll.Function(internal_state.module, temp_function_type, self.name)

        for i, arg_names in enumerate(internal_state.current_function_argument_names):
            internal_state.defined_variables[arg_names.getstr()] = \
                InternalValue(wrapped_type=internal_state.current_function_argument_wrapped_types[i],
                              llvm_value=temp_function.args[i],
                              span=arg_names.getsourcepos())

            internal_state.defined_variables[arg_names.getstr()].markArgument()

        internal_state.basic_block = temp_function.append_basic_block(self.name)
        internal_state.builder = ll.IRBuilder(internal_state.basic_block)

        internal_state.defined_functions[self.name] = temp_function
        state.defined_functions[self.name] = temp_function

        temp_argument_types.insert(0, temp_return_type)

        internal_state.defined_functions_argument_types[self.name] = temp_argument_types
        state.defined_functions_argument_types[self.name] = temp_argument_types

        self.closure.build(internal_state)

        internal_state.exit_function()


# --- Internals

class ArgumentNode:
    def __init__(self, name, typ):
        self.name = name
        self.span = name.getsourcepos()
        self.type = typ

    def build(self, state):
        # -- Checks -- #
        if self.name in state.current_function_argument_names:
            state.error_handler("Repeated usage of argument name.", self.span)

        # -- Checks -- #

        state.current_function_argument_names.append(self.name)
        state.current_function_argument_wrapped_types.append(self.type.build(state))


# --- Calls & Nodes --- #

class CallNode:
    def __init__(self, name, call_op_node):
        self.name = name.getstr()
        self.span = name.getsourcepos()
        self.node = call_op_node

    def build(self, state):

        # -- Checks -- #

        if self.name not in state.defined_functions.keys():
            state.error_handler("Call to an undefined function.", self.span)

        # -- Checks -- #

        temp_defined_argument_types = deepcopy(state.defined_functions_argument_types[self.name])
        temp_return_type = temp_defined_argument_types.pop()

        temp_defined_argument_types.reverse()

        temp_argument_types = temp_defined_argument_types

        state.wanted_types.extend(temp_argument_types)

        state.current_call_arguments_types = temp_argument_types
        self.node.build(state)

        temp = None
        temp_wanted_type = None

        if len(state.wanted_types) > 0:
            temp_wanted_type = state.wanted_types.pop()

        else:
            temp_wanted_type = temp_return_type

        temp_argument_llvm_values = []

        for argument in state.current_call_arguments_values.pop():
            temp_argument_llvm_values.append(argument.getLLVMValue())

        if len(state.wanted_types) > 0:
            temp = InternalValue(wrapped_type=temp_wanted_type,
                                 llvm_value=state.builder.call(state.defined_functions[self.name],
                                                               temp_argument_llvm_values),
                                 span=self.span)

            if not temp_return_type == temp_wanted_type:
                temp = CastTo(temp_wanted_type, temp, state, self.span)

        else:
            temp = InternalValue(wrapped_type=temp_return_type,
                                 llvm_value=state.builder.call(state.defined_functions[self.name],
                                                               temp_argument_llvm_values),
                                 span=self.span)

        return temp


class CallOpNode:
    def __init__(self, argument_node):
        self.args = argument_node

    def build(self, state):
        state.current_call_arguments_values.append([])

        for arg in self.args:
            arg.build(state)

        for i, argument_value in enumerate(state.current_call_arguments_values[-1]):
            if not argument_value.getWrappedType() == state.current_call_arguments_types[i]:
                state.error_handler("Wrong argument type supplied.", argument_value.getSpan())
            else:
                state.current_call_arguments_llvm_values.append(argument_value.getLLVMValue())


class CallArgumentsNode:
    def __init__(self, expressions):
        self.exprs = expressions

    def build(self, state):
        for expr in self.exprs:
            state.current_call_arguments_values[-1] \
                .append(expr.build(state))


# --- Statements --- #

class LetNode:
    def __init__(self, name, typ, value=None):
        self.name = name.getstr()
        self.type = typ
        self.value = value
        self.span = name.getsourcepos()

    def build(self, state):
        if self.value is not None:
            if self.type is not None:
                temp_type = self.type.build(state)
                state.wanted_types.append(temp_type)

                temp_value = self.value.build(state)
            else:
                temp_value = self.value.build(state)
                temp_type = temp_value.getWrappedType()
        else:
            temp_value = None
            temp_type = self.type.build(state)

        # -- Checks -- #
        if self.name in state.defined_variables:
            if state.defined_variables[self.name].getWrappedType() == temp_type:
                state.warning_handler("Redefinition of variable with same type.", self.span)
            elif state.defined_variables[self.name].isArgument():
                state.error_handler("Redefinition of function argument.", self.span)

        # -- Checks -- #

        state.defined_variables[self.name] = InternalValue(wrapped_type=temp_type,
                                                           span=self.span,
                                                           llvm_value=state.builder.alloca(temp_type.getLLVMType(),
                                                                                           name=self.name))

        state.defined_variables[self.name].addPointerDepth()
        state.defined_variables[self.name].markVariable()

        if temp_value is not None:
            temp_cast = CastTo(target=state.defined_variables[self.name].getMemoryWrappedType(),
                               value=temp_value,
                               state=state,
                               span=self.span)

            state.builder.store(temp_cast.getLLVMValue(),
                                state.defined_variables[self.name].getLLVMValue())


class ReturnNode:
    def __init__(self, span, value):
        self.span = span.getsourcepos()
        self.value = value

    def build(self, state):
        if self.value is not None:
            temp_value = self.value.build(state)
            temp_type = temp_value.getWrappedType()
            temp_return_value = temp_value

            if state.current_function_return_type == temp_type:
                return state.builder.ret(temp_return_value.getLLVMValue())
            
            else:
                temp_return_value = CastTo(state.current_function_return_type, temp_value, state, self.span)
                return state.builder.ret(temp_return_value.getLLVMValue())

        else:
            state.builder.ret_void()


# --- Pointers --- #

class RefNode:
    def __init__(self, span, value):
        self.span = span.getsourcepos()
        self.value = value
    
    def build(self, state):
        temp_value = self.value.build(state)

        temp_llvm_value = state.builder.alloca(temp_value.getLLVMType())
        state.builder.store(temp_value.getLLVMValue(), temp_llvm_value)

        temp_value.addPointerDepth()

        temp = InternalValue(temp_value.getWrappedType(),
                             llvm_value=temp_llvm_value)

        return temp


class DerefNode:
    def __init__(self, span, value):
        self.span = span.getsourcepos()
        self.value = value
    
    def build(self, state):
        temp_value = self.value.build(state)

        # -- Checks -- #

        if not temp_value.isPointer():
            state.error_handler("Can't derefrence non-refrence value.", self.span)

        # -- Checks -- #

        temp_llvm_value = state.builder.load(temp_value.getLLVMValue())

        temp_value.addPointerDepth(-1)

        temp = InternalValue(temp_value.getWrappedType(),
                             llvm_value=temp_llvm_value)

        return temp


class AddressNode:
    def __init__(self, span, value):
        self.span = span.getsourcepos()
        self.value = value
    
    def build(self, state):
        temp_value = self.value.build(state)

        # -- Checks -- #

        if not IsNumber(temp_value.getWrappedType()):
            state.error_handler("Can't create reference from value.", self.span)

        # -- Checks -- #

        temp_wanted_type = state.types["void"](depth=1) 

        if len(state.wanted_types) > 0:
            temp_wanted_type = state.wanted_types.pop()

        temp_llvm_value = state.builder.inttoptr(temp_value.getLLVMValue(),
                                                 temp_wanted_type.getLLVMType())    

        temp = InternalValue(temp_wanted_type,
                             llvm_value=temp_llvm_value)

        return temp


# --- Base Type Nodes --- #

class VariableNode:
    def __init__(self, value):
        self.value = value.getstr()
        self.span = value.getsourcepos()

    def build(self, state):
        if self.value not in state.defined_variables:
            state.error_handler("Usage of undefined variable.", self.span)

        temp = state.defined_variables[self.value]

        if temp.isVariable():
            state.defined_variables[self.value].markUsed()
            temp_llvm_value = state.builder.load(temp.getLLVMValue())
            temp.addPointerDepth(-1)

        else:
            state.defined_variables[self.value].markUsed()
            temp_llvm_value = temp.getLLVMValue()

        return InternalValue(wrapped_type=temp.getWrappedType(),
                             llvm_value=temp_llvm_value)


class NumberNode:
    def __init__(self, value):
        self.value = int(value.getstr())
        self.span = value.getsourcepos()

    def build(self, state):
        temp_value = InternalValue(I32Type(), python_value=self.value)
        if len(state.wanted_types) != 0:
            # -- Checks -- #
            if IsNumber(state.wanted_types[-1]):
                temp_value = InternalValue(wrapped_type=state.wanted_types.pop().getWrappedBaseType(),
                                           python_value=self.value,
                                           span=self.span)
            else:
                state.error_handler("Usage of expression with a wrong type.", self.span)
            # -- Checks -- #

        return temp_value


class FloatNode:
    def __init__(self, value):
        self.value = float(value.getstr())
        self.span = value.getsourcepos()

    def build(self, state):
        temp_value = InternalValue(F32Type(), python_value=self.value)
        if len(state.wanted_types) != 0:
            # -- Checks -- #
            if IsFloat(state.wanted_types[-1]):
                temp_value = InternalValue(wrapped_type=state.wanted_types.pop().getWrappedBaseType(),
                                           python_value=self.value,
                                           span=self.span)
            else:
                state.error_handler("Usage of expression with a wrong type.", self.span)
            # -- Checks -- #

        return temp_value


class BoolNode:
    def __init__(self, value):
        if value.getstr() == "true":
            self.value = True
        elif value.getstr() == "false":
            self.value = False
        else:
            self.value = bool(value.getstr())
        self.span = value.getsourcepos()

    def build(self, state):
        temp_value = InternalValue(BoolType(), python_value=self.value)
        if len(state.wanted_types) != 0:
            # -- Checks -- #
            if IsBool(state.wanted_types[-1]):
                temp_value = InternalValue(wrapped_type=state.wanted_types.pop().getWrappedBaseType(),
                                           python_value=self.value,
                                           span=self.span)
            elif IsNumber(state.wanted_types[-1]):
                temp_value = InternalValue(wrapped_type=BoolType(),
                                           python_value=self.value,
                                           span=self.span)

                temp_value = CastTo(state.wanted_types.pop().getWrappedBaseType(), temp_value, state, self.span)
            else:
                state.error_handler("Usage of expression with a wrong type.", self.span)
            # -- Checks -- #

        return temp_value


# --- Type Node --- #

class TypeNode:
    def __init__(self, value, depth=0, is_ptr=None):
        self.depth = depth
        self.is_ptr = is_ptr
        self.value = value.getstr()
        self.span = value.getsourcepos()

    def build(self, state):
        state.enter_type()

        temp = None
        
        if self.is_ptr is not None:
            self.is_ptr.build(state)
        
        if self.value not in state.types.keys():
            state.error_handler("Usage of unknown type.", self.span)
        else:
            temp = state.types[self.value](span=self.span)
            temp.setPointerDepth(state.current_pointer_depth)
        
        state.exit_type()

        return temp


class PtrNode:
    def __init__(self, nodes):
        self.nodes = nodes
    
    def build(self, state):
        if len(self.nodes) > 0:
            for node in self.nodes:
                node.build(state)
        else:
            state.current_pointer_depth += 1
        
        
        
