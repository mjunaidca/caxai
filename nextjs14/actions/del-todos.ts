'use server'
import { auth } from '@/auth';
import { redirect } from 'next/navigation';
import { revalidateTag } from 'next/cache'

export async function deleteTodo(id: string) {
    // throw new Error('Failed to Delete Invoice');

    const session = await auth() as CustomSession; 
    if (!session || !session.user) redirect('/');

    const accessToken = (session.user.accessToken)

    // Get All Todos
    try {
        const all_todos_request = await fetch(`${process.env.BACKEND_URL}/api/todos/${id}`, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
                },
            method: 'DELETE',
            cache: 'no-store',
            next: { tags: ['get_todos'] }
        });

        if (all_todos_request.status === 200) {
            revalidateTag('get_todos')
            return { message: 'Deleted Todo' };
        } 

        return { message: 'Failed to Delete Todo' };

    } catch (error) {
      return { message: 'Database Error: Failed to Delete Invoice.' };
    }
  }