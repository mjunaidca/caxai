import Breadcrumbs from '@/components/manage/breadcrumbs';
import CreateTodoForm from '@/components/manage/create-todo';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Create Invoice',
};

export default async function Page() {

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: 'Manage Todos', href: '/dashboard/manage' },
          {
            label: 'Create Todo',
            href: '/dashboard/manage/create',
            active: true,
          },
        ]}
      />
      <CreateTodoForm />
    </main>
  );
}
