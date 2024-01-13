"use server";
import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { revalidateTag } from "next/cache";
import * as z from "zod";
import { TodoSchema } from "@/schemas/todo";

export async function updateTodoAction(
  id: string,
  values: z.infer<typeof TodoSchema>
) {
  console.log("updateTodoAction");

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

  // Get All Todos
  const update_todo = await fetch(
    `${process.env.BACKEND_URL}/api/todos/${id}`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      method: "PATCH",
      body: JSON.stringify({
        title: title,
        description: description,
        completed: completed,
      }),
      cache: "no-store",
      next: { tags: ["get_todos"] },
    }
  );

  console.log("UPDATE_TODO_STATUS", update_todo.status, update_todo.statusText);

  if (update_todo.status !== 200) {
    return { error: "Failed to Update Todo" };
  }

  revalidateTag("get_todos");
  // redirect("/dashboard/manage");
  return { success: "Todo Updated!" };
}
