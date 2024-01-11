import { CreateTodo } from "@/components/manage/buttons";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { redirect } from "next/navigation";
import * as jose from 'jose'
import { auth } from "@/auth";
const page = async ({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) => {

  const session = await auth() as CustomSession; 
  if (!session || !session.user) redirect('/');

  const user_id = (session.user.id)

  // const secret = new TextEncoder().encode(
  //   user_id,
  // )

  // const alg = process.env.ALGORITHM || "HS256"

  // // Use Jose to create a Short Lived OAuth Code
  // const code = await new jose.SignJWT({ 'urn:example:claim': true })
  // .setProtectedHeader({ alg })
  // .setIssuedAt()
  // .setIssuer('urn:example:issuer')
  // .setAudience('urn:example:audience')
  // .setExpirationTime('1h')
  // .sign(secret)

  // Get all the query params
  const redirect_uri = searchParams.redirect_uri;
  const client_id = searchParams.client_id;
  const response_type = searchParams.response_type;
  const scope = searchParams.scope;
  // const code = searchParams.code;
  const state = searchParams.state;

  if (redirect_uri) {
    redirect(redirect_uri + `?code=${user_id}` + `&state=${state}`)
  }
  return (
    <div className=" min-h-[75%] rounded-sm h-full flex flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-400 to-blue-800">
      <div className="space-y-6 text-center">
        <h1 className={cn(
          "text-3xl lg:text-5xl font-semibold text-white drop-shadow-md"
        )}>
          🔐 Dashboard 
        </h1>
        <p className="text-white text-lg">
          Navigate to manage, Create, Add, Delete & View Todos
        </p>
        <div className="flex flex-col justify-center items-center space-y-5">
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
