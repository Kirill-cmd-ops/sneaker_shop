"use client";
import LoginForm from "../components/LoginForm";

export default function LoginPage() {
  return (
    <main className="flex flex-col items-center min-h-screen bg-white text-black p-10">
      <h1 className="text-3xl font-bold mb-6">Авторизация</h1>
      <LoginForm/>
    </main>
  );
}
