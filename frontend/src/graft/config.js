import { GraftConfig, TodoService } from "@graft/pypi-todo-service";

GraftConfig.host = import.meta.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

export { GraftConfig, TodoService };

export function parseTodo(snapshot) {
  return {
    id: snapshot[0],
    title: snapshot[1],
    description: snapshot[2],
    completed: snapshot[3] === "true",
  };
}

export function parseTodoList(flat) {
  const todos = [];
  const values = flat || [];
  for (let i = 0; i < values.length; i += 4) {
    todos.push(parseTodo(values.slice(i, i + 4)));
  }
  return todos;
}
