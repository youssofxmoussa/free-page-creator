import { useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/lib/auth";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import { motion } from "framer-motion";

const TELEGRAM_BOT_USERNAME = "youssofxxmoussabot";

const Auth = () => {
  const { session, loading } = useAuth();
  const navigate = useNavigate();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!loading && session) {
      navigate("/", { replace: true });
    }
  }, [session, loading, navigate]);

  const handleTelegramAuth = useCallback(async (telegramUser: Record<string, string>) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/telegram-auth`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY}`,
          },
          body: JSON.stringify(telegramUser),
        }
      );

      const data = await response.json();
      if (!response.ok) {
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
      toast.error("Failed to authenticate with Telegram");
      console.error(e);
    }
  }, [navigate]);

  // Expose callback to window for Telegram widget
  useEffect(() => {
    (window as any).onTelegramAuth = handleTelegramAuth;
    return () => {
      delete (window as any).onTelegramAuth;
    };
  }, [handleTelegramAuth]);

  // Load Telegram widget script
  useEffect(() => {
    if (!containerRef.current) return;
    containerRef.current.innerHTML = "";

    const script = document.createElement("script");
    script.src = "https://telegram.org/js/telegram-widget.js?22";
    script.setAttribute("data-telegram-login", TELEGRAM_BOT_USERNAME);
    script.setAttribute("data-size", "large");
    script.setAttribute("data-onauth", "onTelegramAuth(user)");
    script.setAttribute("data-request-access", "write");
    script.setAttribute("data-userpic", "true");
    script.setAttribute("data-radius", "12");
    script.async = true;
    containerRef.current.appendChild(script);
  }, []);

  if (loading) {
    return (
      <div className="flex h-dvh items-center justify-center bg-background">
        <div className="flex items-center gap-2">
          <span className="typing-dot h-2 w-2 rounded-full bg-cream-dim" />
          <span className="typing-dot h-2 w-2 rounded-full bg-cream-dim" />
          <span className="typing-dot h-2 w-2 rounded-full bg-cream-dim" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-dvh flex-col items-center justify-center bg-background px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col items-center gap-8"
      >
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-bold tracking-[0.2em] text-primary uppercase">
            YoussofGPT
          </h1>
          <p className="text-sm text-muted-foreground">
            Sign in with Telegram to continue
          </p>
        </div>

        <div
          ref={containerRef}
          className="flex items-center justify-center min-h-[50px]"
        />

        <p className="text-[10px] text-muted-foreground/50 text-center max-w-xs">
          By signing in, your chats will be saved and synced across sessions.
        </p>
      </motion.div>
    </div>
  );
};

export default Auth;
