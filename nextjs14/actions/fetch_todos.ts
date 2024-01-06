import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export async function fetchAllTodos() {
    const session = await auth() as CustomSession; 
    if (!session || !session.user) redirect('/');

    const accessToken = (session.user.accessToken)

    // Get All Todos
    const all_todos_request = await fetch(`${process.env.BACKEND_URL}/api/todos/`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
            },
        cache: 'no-store',
        next: { tags: ['get_todos'] }
    });

    if (!all_todos_request.ok) {
        return 'Failes to Load Todos'
    }

    const all_todos: TodoList = await all_todos_request.json();

    return all_todos;
}