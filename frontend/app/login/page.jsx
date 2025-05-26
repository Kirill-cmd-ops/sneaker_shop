"use client";
import Link from "next/link";
import LoginForm from "../components/LoginForm";

export default function LoginPage() {
  return (
    <main className="flex flex-col items-center min-h-screen bg-white text-black p-10">
      <h1 className="text-3xl font-bold mb-6">Авторизация</h1>
      <LoginForm />
      <div className="mt-4">
        <Link
          href="/profile"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          Перейти к профилю
        </Link>
      </div>
    </main>
  );
}
