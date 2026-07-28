import AuthLayout from "@/app/components/auth/AuthLayout";
import { RegisterForm } from "@/app/components/auth/RegisterForm";

export default function RegisterPage() {
    return (
        <AuthLayout
            title="Create your account"
            subtitle="Start using Project Helix in minutes."
            footerText="Already have an account?"
            footerLinkText="Sign In"
            footerHref="/auth/login"
        >
            <RegisterForm />
        </AuthLayout>
    );
}