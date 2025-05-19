"use client";
import RegisterForm from "../components/RegisterForm";

export default function RegisterPage() {
  return (
    <main className="flex flex-col items-center min-h-screen bg-white text-black p-10">
      <h1 className="text-3xl font-bold mb-6">Регистрация</h1>
      <RegisterForm />
    </main>
  );
}
