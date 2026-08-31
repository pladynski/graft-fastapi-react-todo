import { GraftConfig, TodoService } from "@graft/pypi-todo-service";

GraftConfig.host = process.env.GRAFT_HOST ?? process.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

const parseTodo = (snapshot) => ({
  id: snapshot[0],
  title: snapshot[1],
  description: snapshot[2],
  completed: snapshot[3] === "true",
});

const parseTodoList = (flat) => {
  const todos = [];
  for (let i = 0; i < (flat?.length ?? 0); i += 4) {
    todos.push(parseTodo(flat.slice(i, i + 4)));
  }
  return todos;
};

const created = parseTodo(await TodoService.createTodo("Smoke todo", "Created by frontend/scripts/smoke.mjs"));
console.log("created", created);

const listed = parseTodoList(await TodoService.listTodos());
console.log("listed", listed);

const toggled = parseTodo(await TodoService.toggleTodo(created.id));
console.log("toggled", toggled);

const deleted = await TodoService.deleteTodo(created.id);
console.log("deleted", deleted);
console.log("remaining", parseTodoList(await TodoService.listTodos()).length);
console.log("smoke ok");
