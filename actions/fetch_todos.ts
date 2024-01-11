import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export async function fetchAllTodos() {
    const session = await auth() as CustomSession; 
    if (!session || !session.user) redirect('/');

    const accessToken = (session.user.accessToken)

    const page = 1;
    const perPage = 10;

    // Get All Todos
    const all_todos_request = await fetch( `${process.env.BACKEND_URL}/api/todos/?page=${page}&per_page=${perPage}`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
            },
        cache: 'force-cache',
        next: { tags: ['get_todos'] }
    });

    if (!all_todos_request.ok) {
        return 'Failes to Load Todos'
    }

    console.log(all_todos_request.status);
    

    const paginated_all_todos: PagiantedTodos = await all_todos_request.json();

    const all_todos: TodoList = paginated_all_todos.todos;

    return all_todos;
}