import { Suspense } from "react";
import { Metadata } from "next";
import { InvoicesTableSkeleton } from "@/components/ui/skeletons";
import TodosTable from "@/components/manage/todos-table";
import { fetchAllTodos } from "@/actions/fetch_todos";
import { CreateTodo } from "@/components/manage/buttons";
import { notFound } from "next/navigation";

export const metadata: Metadata = {
  title: "Manage",
};

export default async function Page() {
  const all_todos: TodoList | string = await fetchAllTodos();

  // Check if 'all_todos' is of type 'TodoList'
  if (!Array.isArray(all_todos)) {
    notFound();
  }

  return (
    <div className="w-full">
      <div className="flex w-full items-center justify-between">
        <h1 className={` text-2xl`}>Todos Manager</h1> <CreateTodo />
      </div>
      <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
        {/* <Search placeholder="Search invoices..." />
        <CreateInvoice /> */}
      </div>
      <Suspense fallback={<InvoicesTableSkeleton />}>
        <TodosTable todos={all_todos} />
      </Suspense>
    </div>
  );
}
