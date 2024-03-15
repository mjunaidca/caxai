import { fetchAllTodos } from "@/actions/fetch_todos";
import TodosViewTable from "@/components/dashboard/todos-view-table";
import { PackageSearch } from "lucide-react";
import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

export const metadata: Metadata = {
  title: "View All ToDos",
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
    <main>
      <TodosViewTable todos={all_todos} />
    </main>
  );
}
