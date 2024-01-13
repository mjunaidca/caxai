import { CreateTodo } from "@/components/manage/buttons";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { redirect } from "next/navigation";
import { auth } from "@/auth";

type TempCode = {
  code: string;
};

// Function to get temporary code
async function getTempCode(user_id: string) {
  const res = await fetch(
    `${process.env.BACKEND_URL}/api/oauth/temp-code?user_id=${user_id}`,
    {
      cache: "no-store",
    }
  );
  const data = await res.json();
  return data as TempCode;
}

const page = async ({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) => {
  const session = await auth();
  if (!session) {
    console.log("[session] No cookies. Redirecting...");
    redirect("/auth/login");
  }

  const redirect_uri = searchParams.redirect_uri;
  const state = searchParams.state;

  if (redirect_uri && state && session) {
    const user_id = session.user.id;
    const tempCode = await getTempCode(user_id);
    redirect(redirect_uri + `?code=${tempCode.code}` + `&state=${state}`);
  }

  return (
    <div className=" min-h-[75%] rounded-sm h-full flex flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-400 to-blue-800">
      <div className="space-y-6 text-center">
        <h1
          className={cn(
            "text-3xl lg:text-5xl font-semibold text-white drop-shadow-md"
          )}
        >
          🔐 Dashboard
        </h1>
        <p className="text-white text-lg">
          Navigate to manage, Create, Add, Delete & View Todos
        </p>
        <div className="flex flex-col justify-center items-center space-y-5">
          <Link
            href="https://chat.openai.com/g/g-fC8sZoDCi-cax-taskpal"
            target="_blank"
          >
            <Button variant="secondary" size="lg">
              TaskPal GPT 🤖
            </Button>
          </Link>
          <Link href="/dashboard/manage">
            <Button variant="secondary" size="lg">
              Manage ToDos
            </Button>
          </Link>
          <Link href="/dashboard/view">
            <Button variant="secondary" size="lg">
              View All ToDos
            </Button>
          </Link>
          <CreateTodo />
        </div>
      </div>
    </div>
  );
};

export default page;
