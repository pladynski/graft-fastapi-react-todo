import { GraftConfig, TodoController, TodoCreate, TodoUpdate } from "@graft/pypi-todo";

GraftConfig.host = import.meta.env.VITE_GRAFT_HOST ?? "ws://localhost:8000/ws";
GraftConfig.stateless = true;

/**
 * Todo Service class for managing todo operations
 */
class TodoService {
  /**
   * Get all todos
   * @returns {Promise<Array>}
   */
  async fetchTodos() {
    return TodoController.getAllTodos();
  }

  /**
   * Get a specific todo by ID
   * @param {number} id
   * @returns {Promise<object>}
   */
  async getTodo(id) {
    return TodoController.getTodo(id);
  }

  /**
   * Create a new todo
   * @param {string} title
   * @param {string} description
   * @returns {Promise<object>}
   */
  async createTodo(title, description = '') {
    return TodoController.createTodo(new TodoCreate(title, description));
  }

  /**
   * Update a todo
   * @param {number} id
   * @param {object} updates - Object with title, description, and/or completed fields
   * @returns {Promise<object>}
   */
  async updateTodo(id, updates) {
    return TodoController.updateTodo(
      id,
      new TodoUpdate(updates.title, updates.description, updates.completed),
    );
  }

  /**
   * Toggle a todo's completion status
   * @param {number} id
   * @returns {Promise<object>}
   */
  async toggleTodoCompletion(id) {
    return TodoController.toggleTodoCompletion(id);
  }

  /**
   * Delete a todo
   * @param {number} id
   * @returns {Promise<object>}
   */
  async deleteTodo(id) {
    return TodoController.deleteTodo(id);
  }
}

export default TodoService;
