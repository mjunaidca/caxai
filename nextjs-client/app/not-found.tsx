"use client";
import { PackageSearch } from "lucide-react";
import { useRouter } from "next/navigation";

export default function NotFound() {
  const router = useRouter();
  return (
    <main className="flex h-full flex-col items-center justify-center gap-2">
      <PackageSearch className="w-10 text-gray-400" />
      <h2 className="text-xl font-semibold">Not Found</h2>
      <button
        onClick={() => router.push("/dashboard")}
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-400"
      >
        Go to Dashboard
      </button>
      <button
        onClick={() => router.push("/")}
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-400"
      >
        Visit Home Page
      </button>
    </main>
  );
}
