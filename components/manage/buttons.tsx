import { deleteTodo } from '@/actions/del-todos';
import { PencilIcon, PlusIcon, TrashIcon } from 'lucide-react';
import { revalidateTag } from 'next/cache';
import Link from 'next/link';

export function CreateTodo() {
  return (
    <Link
      href="/dashboard/manage/create"
      className="flex h-10 items-center rounded-lg bg-blue-600 px-4 text-sm font-medium text-white transition-colors hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
    >
      <span className="hidden md:block">Create Todo</span>{' '}
      <PlusIcon className="h-5 md:ml-4" />
    </Link>
  );
}

export function UpdateTodo({ id }: { id: string }) {
  return (
    <Link
      href={`/dashboard/manage/${id}/edit`}
      className="rounded-md border p-2 hover:bg-gray-100"
    >
      <PencilIcon className="w-5" />
    </Link>
  );
}

export function DeleteTodo({ id }: { id: string }) {
  const deleteTodoeWithId = deleteTodo.bind(null, id);
  
  revalidateTag('get_todos')

  return (
    <form action={deleteTodoeWithId}>
      <button className="rounded-md border p-2 hover:bg-gray-100 bg-red-50">
        <span className="sr-only">Delete</span>
        <TrashIcon className="w-5 text-red-900" />
      </button>
    </form>
  );
}
