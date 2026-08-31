import { GraftConfig, TodoService } from "@graft/pypi-todo-service";

GraftConfig.host = process.env.GRAFT_HOST ?? process.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

const flat = await TodoService.listTodos();
let cleared = 0;
for (let i = 0; i < (flat?.length ?? 0); i += 4) {
  await TodoService.deleteTodo(flat[i]);
  cleared += 1;
}
console.log(`cleared ${cleared} todos`);
