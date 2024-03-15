import { Suspense } from "react";
import { Metadata } from "next";
import { InvoicesTableSkeleton } from "@/components/ui/skeletons";
import TodosTable from "@/components/manage/todos-table";
import { fetchAllTodos } from "@/actions/fetch_todos";
import { CreateTodo } from "@/components/manage/buttons";
import { notFound } from "next/navigation";
import { PackageSearch } from "lucide-react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Manage",
};

export default async function Page() {
  const all_todos: TodoList | string = await fetchAllTodos();

  // Check if 'all_todos' is of type 'TodoList'
  if (!Array.isArray(all_todos)) {
    return (
      <main className="flex h-full flex-col items-center justify-center gap-2">
        <PackageSearch className="w-10 text-gray-400" />
        <h2 className="text-xl font-semibold">Your ToDo List is Empty</h2>
        <Link
          href="/dashboard/manage/create"
          className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-400"
        >
          Create New ToDo
        </Link>
      </main>
    );
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
