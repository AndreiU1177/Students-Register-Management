from src.utils.exceptions import UndoRedoException


class Command:
    def __init__(self, fn, *args):
        self._fn = fn
        self._fn_params = args

    def execute(self):
        self._fn(*self._fn_params)


class Operation:
    def __init__(self, undo_action: Command, redo_action: Command):
        self.__undo_action = undo_action
        self.__redo_action = redo_action

    def undo_op(self):
        self.__undo_action.execute()

    def redo_op(self):
        self.__redo_action.execute()


class CascadedOperation:
    def __init__(self, operation_list: list[Operation]):
        self.__operation_list = operation_list

    def undo_op(self):
        for op in self.__operation_list:
            op.undo_op()

    def redo_op(self):
        for op in reversed(self.__operation_list):
            op.redo_op()


class UndoService:
    def __init__(self):
        self.__undo_stack = []
        self.__redo_stack = []

    def undo_append(self, operation: Operation):
        self.__undo_stack.append(operation)

    def undo(self):
        if len(self.__undo_stack) == 0:
            raise UndoRedoException("No undos available")
        operation = self.__undo_stack.pop()
        operation.undo_op()
        self.__redo_stack.append(operation)

    def redo(self):
        if len(self.__redo_stack) == 0:
            raise UndoRedoException("No redos available")
        operation = self.__redo_stack.pop()
        operation.redo_op()
        self.__undo_stack.append(operation)

    def clear_redo_stack(self):
        self.__redo_stack.clear()

