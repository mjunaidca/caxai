type TodoItem = {
    title: string;
    description: string;
    completed: boolean;
    id: string;
    created_at: string; // or Date if you prefer to work with Date objects
    updated_at: string; // or Date if you prefer to work with Date objects
    user_id: string;
  };
  
  type TodoList = TodoItem[];

  type PagiantedTodos = {
    todos: TodoList;
    count: number;
    next: number;
    previous: number;
  }
  