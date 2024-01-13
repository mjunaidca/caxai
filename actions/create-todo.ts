"use server";
import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { revalidateTag } from "next/cache";
import * as z from "zod";
import { TodoSchema } from "@/schemas/todo";

export async function createTodoAction(values: z.infer<typeof TodoSchema>) {
  const validatedFields = TodoSchema.safeParse(values);

  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { title, completed, description } = validatedFields.data;

  console.log("updateTodoAction", title, completed, description);

  const session = await auth();
  if (!session) {
    console.log("[session] No cookies. Redirecting...");
    redirect("/auth/login");
  }

  const accessToken = session.access_token;

  console.log("accessToken", accessToken);

  // Get All Todos
  const create_todo = await fetch(`${process.env.BACKEND_URL}/api/todos`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      title: title,
      description: description,
      completed: completed,
    }),
    cache: "no-store",
    next: { tags: ["get_todos"] },
  });

  console.log("create_todo_STATUS", create_todo.status, create_todo.statusText);

  if (create_todo.status !== 201) {
    return { error: "Failed to Create Todo" };
  }

  revalidateTag("get_todos");
  // redirect("/dashboard/manage");
  return { success: "Too Created!" };
}
