import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const exchangeCode = async () => {
      const code = searchParams.get("code");
      const state = searchParams.get("state");

      if (!code) {
        setError("No authorization code received");
        return;
      }

      // Verify state matches
      const savedState = sessionStorage.getItem("tg_oauth_state");
      if (state !== savedState) {
        setError("Invalid state parameter - possible CSRF attack");
        return;
      }

      const codeVerifier = sessionStorage.getItem("tg_code_verifier");
      if (!codeVerifier) {
        setError("Missing PKCE verifier - please try logging in again");
        return;
      }

      // Clean up sessionStorage
      sessionStorage.removeItem("tg_code_verifier");
      sessionStorage.removeItem("tg_oauth_state");

      try {
        const response = await fetch(
          `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/telegram-auth`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY}`,
            },
            body: JSON.stringify({
              code,
              code_verifier: codeVerifier,
              redirect_uri: `${window.location.origin}/auth/callback`,
            }),
          }
        );

        const data = await response.json();
        if (!response.ok) {
          setError(data.error || "Login failed");
          toast.error(data.error || "Login failed");
          return;
        }

        if (data.session) {
          await supabase.auth.setSession({
            access_token: data.session.access_token,
            refresh_token: data.session.refresh_token,
          });
          toast.success(`Welcome, ${data.user.display_name}!`);
          navigate("/", { replace: true });
        }
      } catch (e) {
        console.error("Auth callback error:", e);
        setError("Failed to complete authentication");
        toast.error("Failed to complete authentication");
      }
    };

    exchangeCode();
  }, [searchParams, navigate]);

  if (error) {
    return (
      <div className="flex h-dvh flex-col items-center justify-center bg-background px-4 gap-4">
        <p className="text-destructive text-sm">{error}</p>
        <button
          onClick={() => navigate("/auth", { replace: true })}
          className="text-sm text-primary underline"
        >
          Back to login
        </button>
      </div>
    );
  }

  return (
    <div className="flex h-dvh items-center justify-center bg-background">
      <div className="flex items-center gap-2">
        <span className="typing-dot h-2 w-2 rounded-full bg-cream-dim" />
        <span className="typing-dot h-2 w-2 rounded-full bg-cream-dim" />
        <span className="typing-dot h-2 w-2 rounded-full bg-cream-dim" />
      </div>
    </div>
  );
};

export default AuthCallback;
