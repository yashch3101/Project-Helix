import AuthLayout from "@/app/components/auth/AuthLayout";
import LoginForm from "@/app/components/auth/LoginForm";

export default function LoginPage() {
    return (
        <AuthLayout
            title="Welcome Back"
            subtitle="Sign in to continue to Project Helix."
            footerText="Don't have an account?"
            footerLinkText="Create Account"
            footerHref="/auth/register"
        >
            <LoginForm />
        </AuthLayout>
    );
}