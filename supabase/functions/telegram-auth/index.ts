import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

async function verifyTelegramAuth(data: Record<string, string>, botToken: string): Promise<boolean> {
  const checkHash = data.hash;
  if (!checkHash) return false;

  const dataCheckArr: string[] = [];
  for (const key of Object.keys(data).sort()) {
    if (key === "hash") continue;
    dataCheckArr.push(`${key}=${data[key]}`);
  }
  const dataCheckString = dataCheckArr.join("\n");

  const encoder = new TextEncoder();
  const secretKey = await crypto.subtle.digest("SHA-256", encoder.encode(botToken));

  const key = await crypto.subtle.importKey(
    "raw",
    secretKey,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(dataCheckString));
  const hex = Array.from(new Uint8Array(signature))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  return hex === checkHash;
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const botToken = Deno.env.get("TELEGRAM_BOT_TOKEN");
    if (!botToken) {
      throw new Error("TELEGRAM_BOT_TOKEN is not configured");
    }

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, serviceRoleKey, {
      auth: { autoRefreshToken: false, persistSession: false },
    });

    const telegramData = await req.json();

    // Verify Telegram auth hash
    const isValid = await verifyTelegramAuth(telegramData, botToken);
    if (!isValid) {
      return new Response(
        JSON.stringify({ error: "Invalid Telegram authentication data" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Check auth_date is not too old (1 day)
    const authDate = parseInt(telegramData.auth_date);
    if (Date.now() / 1000 - authDate > 86400) {
      return new Response(
        JSON.stringify({ error: "Authentication data expired" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const telegramId = telegramData.id;
    const displayName = [telegramData.first_name, telegramData.last_name]
      .filter(Boolean)
      .join(" ") || "Telegram User";
    const avatarUrl = telegramData.photo_url || null;
    const email = `tg_${telegramId}@youssofgpt.app`;
    const encoder = new TextEncoder();
    const pwKey = await crypto.subtle.digest(
      "SHA-256",
      encoder.encode(`${telegramId}:${botToken}:youssofgpt`)
    );
    const password = Array.from(new Uint8Array(pwKey))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");

    // Try to sign in first
    let { data: signInData, error: signInError } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (signInError) {
      // User doesn't exist, create them
      const { data: signUpData, error: signUpError } =
        await supabase.auth.admin.createUser({
          email,
          password,
          email_confirm: true,
          user_metadata: {
            display_name: displayName,
            avatar_url: avatarUrl,
            telegram_id: telegramId,
          },
        });

      if (signUpError) {
        console.error("Sign up error:", signUpError);
        return new Response(
          JSON.stringify({ error: "Failed to create account" }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      if (signUpData.user) {
        await supabase
          .from("profiles")
          .update({
            telegram_id: parseInt(telegramId),
            display_name: displayName,
            avatar_url: avatarUrl,
          })
          .eq("id", signUpData.user.id);
      }

      const { data: newSignIn, error: newSignInError } =
        await supabase.auth.signInWithPassword({ email, password });

      if (newSignInError) {
        return new Response(
          JSON.stringify({ error: "Failed to sign in after account creation" }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }
      signInData = newSignIn;
    } else {
      if (signInData.user) {
        await supabase
          .from("profiles")
          .update({
            display_name: displayName,
            avatar_url: avatarUrl,
          })
          .eq("id", signInData.user.id);
      }
    }

    return new Response(
      JSON.stringify({
        session: signInData.session,
        user: {
          id: signInData.user?.id,
          display_name: displayName,
          avatar_url: avatarUrl,
          telegram_id: telegramId,
        },
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("telegram-auth error:", e);
    return new Response(
      JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
