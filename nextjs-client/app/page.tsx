import { Poppins } from "next/font/google";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LoginButton } from "@/components/auth/login-button";
import { RegisterButton } from "@/components/auth/register-button";

const font = Poppins({
  subsets: ["latin"],
  weight: ["600"]
})

export default async function Home() {
  
  return (
    <main className="flex h-screen flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-400 to-blue-800">
      <div className="space-y-6 text-center">
        <h1 className={cn(
          "text-6xl font-semibold text-white drop-shadow-md",
          font.className,
        )}>
          🔐 CAX
        </h1>
        <p className="text-white text-lg">
          Multi User Custom GPT Connected with NextJS14 Web App
        </p>
        <div className="flex w-full justify-center space-x-2">
          <LoginButton  asChild>
            <Button variant="secondary" size="lg">
              Sign in
            </Button>
          </LoginButton>
          <RegisterButton  asChild>
            <Button variant="secondary" size="lg">
              Sign up
            </Button>
          </RegisterButton>
        </div>
      </div>
    </main>
  )
}
