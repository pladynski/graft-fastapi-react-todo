import { GraftConfig, TodoController } from "@graft/pypi-todo";

GraftConfig.host = process.env.GRAFT_HOST ?? process.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

const toTodo = (todo) => ({
  id: typeof todo.getId === "function" ? todo.getId() : todo.id,
  title: typeof todo.getTitle === "function" ? todo.getTitle() : todo.title,
  description: typeof todo.getDescription === "function" ? todo.getDescription() : todo.description,
  completed: typeof todo.getCompleted === "function" ? todo.getCompleted() : todo.completed,
});

const created = toTodo(await TodoController.createTodo("Smoke todo", "Created by frontend/scripts/smoke.mjs"));
console.log("created", created);

const listed = (await TodoController.getAllTodos()).map(toTodo);
console.log("listed", listed);

const toggled = toTodo(await TodoController.toggleTodoCompletion(created.id));
console.log("toggled", toggled);

const deleted = await TodoController.deleteTodo(created.id);
console.log("deleted", deleted);
console.log("remaining", (await TodoController.getAllTodos()).length);
console.log("smoke ok");
