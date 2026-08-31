import { GraftConfig, TodoController } from "@graft/pypi-todo";

GraftConfig.host = import.meta.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

export { GraftConfig, TodoController };

function readField(obj, getterName, fieldName) {
  if (obj == null) return undefined;
  const getter = obj[getterName];
  if (typeof getter === "function") {
    const value = getter.call(obj);
    if (value != null && typeof value.getValue === "function") {
      return value.getValue();
    }
    return value;
  }
  return obj[fieldName];
}

export function toTodo(todo) {
  return {
    id: readField(todo, "getId", "id"),
    title: readField(todo, "getTitle", "title"),
    description: readField(todo, "getDescription", "description"),
    completed: Boolean(readField(todo, "getCompleted", "completed")),
  };
}

export function toTodoList(todos) {
  return (todos || []).map(toTodo);
}
