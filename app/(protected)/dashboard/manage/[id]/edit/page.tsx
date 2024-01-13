// import Form from '@/app/ui/invoices/edit-form';
import { notFound } from "next/navigation";
import { Metadata } from "next";

import Breadcrumbs from "@/components/manage/breadcrumbs";
import EditTodoForm from "@/components/manage/edit-tod-form";

import { fetchTodoById } from "@/actions/fetch_todos-id";

export const metadata: Metadata = {
  title: "Edit Invoice",
};

export default async function Page({ params }: { params: { id: string } }) {
  const id = params.id;

  const todoResponse = await fetchTodoById(id);
  
  if (!todoResponse || "error" in todoResponse) {
    notFound();
  }

  console.log("Todo:", todoResponse);

  return (
    <main>
      <Breadcrumbs
        breadcrumbs={[
          { label: "Manage Todos", href: "/dashboard/manage" },
          {
            label: "Edit Todo",
            href: `/dashboard/manage/${id}/edit`,
            active: true,
          },
        ]}
      />
      <EditTodoForm todo={todoResponse} />
    </main>
  );
}
