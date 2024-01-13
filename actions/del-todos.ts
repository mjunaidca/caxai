'use server'
import { auth } from '@/auth';
import { redirect } from 'next/navigation';
import { revalidateTag } from 'next/cache'

export async function deleteTodo(id: string) {
    
    const session = await auth(); 

    if (!session) {
        console.log("[session] No cookies. Redirecting...");
        redirect('/auth/login')
    }

    const accessToken = (session.access_token)

    const all_todos_request = await fetch(`${process.env.BACKEND_URL}/api/todos/${id}`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
            },
        method: 'DELETE',
        cache: 'no-store',
        next: { tags: ['get_todos'] }
    });

    console.log('DELETE_TODO_STATUS', all_todos_request.status, all_todos_request.statusText);        

    if (!all_todos_request.ok) {
        return { error: 'Error deleting todo' };
    } 
    revalidateTag('get_todos')
    return { message: 'Deleted Todo' };

  }