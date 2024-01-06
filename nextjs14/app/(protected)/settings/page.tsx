import { LogoutButton } from "@/components/auth/logout-button";
import { Button } from "@/components/ui/button";
import Link from "next/link";

const page = () => {
  return (
    <div className=" min-h-screen h-full w-full flex flex-col gap-y-10  justify-between bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-400 to-blue-800">
      <nav className="flex p-4 items-center justify-between">
        <Link href='/' className="text-2xl font-semibold text-white drop-shadow-md">
          🔐 CAl AI
        </Link >
        <LogoutButton>
          <Button>Logout</Button>
        </LogoutButton>
      </nav>
    </div>
  );
};

export default page;
