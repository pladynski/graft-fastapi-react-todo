import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@chakra-ui/react";
import { TodoController, toTodo, toTodoList } from "../graft/config.js";

const createStyledToast =
  (toast) =>
  ({ title, description, status, duration = 3000, isClosable = true }) => {
    return toast({
      title,
      description,
      status,
      duration,
      isClosable,
      position: "top-right",
      variant: "subtle",
      containerStyle: {
        bg: "white",
        border: "1px solid",
        borderColor: status === "success" ? "green.200" : status === "error" ? "red.200" : "blue.200",
        borderRadius: "lg",
        boxShadow: "lg",
        color: "gray.800",
      },
    });
  };

const useTodos = () => {
  const queryClient = useQueryClient();
  const toast = useToast();
  const styledToast = createStyledToast(toast);

  const todosQuery = useQuery({
    queryKey: ["todos"],
    queryFn: async () => toTodoList(await TodoController.getAllTodos()),
  });

  const createTodoMutation = useMutation({
    mutationFn: ({ title, description }) => TodoController.createTodo(title, description ?? ""),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      styledToast({
        title: "Todo created",
        description: "Todo created successfully",
        status: "success",
      });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
        duration: 5000,
      });
    },
  });

  const updateTodoMutation = useMutation({
    mutationFn: ({ id, updates }) =>
      TodoController.updateTodo(id, updates.title, updates.description ?? ""),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
      });
    },
  });

  const toggleCompletionMutation = useMutation({
    mutationFn: (id) => TodoController.toggleTodoCompletion(id),
    onSuccess: (todo) => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      const data = toTodo(todo);
      styledToast({
        title: data.completed ? "Todo completed" : "Todo uncompleted",
        description: `"${data.title}" marked as ${data.completed ? "completed" : "incomplete"}`,
        status: "info",
        duration: 2000,
      });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
      });
    },
  });

  const deleteTodoMutation = useMutation({
    mutationFn: (id) => TodoController.deleteTodo(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      styledToast({
        title: "Todo deleted",
        description: "Todo deleted successfully",
        status: "info",
      });
    },
    onError: (error) => {
      styledToast({
        title: "Error",
        description: error.message,
        status: "error",
      });
    },
  });

  return {
    todos: todosQuery.data || [],
    isLoading: todosQuery.isLoading,
    error: todosQuery.error,
    createTodo: createTodoMutation.mutate,
    updateTodo: updateTodoMutation.mutate,
    toggleTodoCompletion: toggleCompletionMutation.mutate,
    deleteTodo: deleteTodoMutation.mutate,
    isCreating: createTodoMutation.isPending,
    isUpdating: updateTodoMutation.isPending,
    isToggling: toggleCompletionMutation.isPending,
    isDeleting: deleteTodoMutation.isPending,
  };
};

export default useTodos;
