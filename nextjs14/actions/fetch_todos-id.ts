import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export async function fetchTodoById(id: string) {
    try {
        const session = await auth() as CustomSession; 
        if (!session || !session.user) {
            redirect('/');
            return null; // Stop execution if no session
        }

        const accessToken = session.user.accessToken;

        const todo_request = await fetch(`${process.env.BACKEND_URL}/api/todos/${id}`, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
            cache: 'no-store'
        });

        if (!todo_request.ok) {
            return { error: 'Failed to load todo', status: todo_request.status };
        }

        try {
            const todo: TodoItem = await todo_request.json();
            return todo;
        } catch (jsonError) {
            return { error: 'Invalid JSON response', status: 500 };
        }
    } catch (networkError) {
        return { error: 'Network error', status: 500 };
    }
}
