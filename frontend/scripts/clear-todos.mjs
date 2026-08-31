import { GraftConfig, TodoController } from "@graft/pypi-todo";

GraftConfig.host = process.env.GRAFT_HOST ?? process.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

const todos = (await TodoController.getAllTodos()) || [];
let cleared = 0;
for (const todo of todos) {
  const id = typeof todo.getId === "function" ? todo.getId() : todo.id;
  await TodoController.deleteTodo(id);
  cleared += 1;
}
console.log(`cleared ${cleared} todos`);
process.exit(0);
