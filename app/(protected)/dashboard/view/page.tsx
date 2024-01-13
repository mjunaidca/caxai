import { fetchAllTodos } from '@/actions/fetch_todos';
import TodosViewTable from '@/components/dashboard/todos-view-table';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';


export const metadata: Metadata = {
  title: 'View All ToDos',
};

export default async function Page() {

    const all_todos: TodoList | string = await fetchAllTodos();

    // Check if 'all_todos' is of type 'TodoList'
    if (!Array.isArray(all_todos)) {
      notFound();
    }

  return (
    <main>
      <TodosViewTable todos={all_todos} />
    </main>
  );
}
