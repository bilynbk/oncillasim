package main

type NotImplementedError struct {
	Method string
	Struct string
}

func NewNotImplementedFunction(function string) *NotImplementedError {
	return &NotImplementedError{function, ""}
}

func NewNotImplementedMethod(struct_, method string) *NotImplementedError {
	return &NotImplementedError{method, struct_}
}

func (e *NotImplementedError) Error() string {
	if len(e.Struct) > 0 {
		return "Function " + e.Method + "() is not implemented"
	}
	return "Method " + e.Struct + "." + e.Method + "() is not implemented"
}
