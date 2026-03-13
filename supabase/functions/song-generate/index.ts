import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
};

const KILWA_API = "https://moazjk-kilwa-music.hf.space/api";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { action, idea, track_id } = await req.json();

    if (action === "start") {
      // Submit song idea
      const resp = await fetch(`${KILWA_API}/generate_idea`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea }),
      });
      const data = await resp.json();
      
      if (!data.track_id) {
        return new Response(
          JSON.stringify({ error: "Failed to start song generation" }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      return new Response(
        JSON.stringify({ track_id: data.track_id, status: "processing" }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    if (action === "status") {
      const resp = await fetch(`${KILWA_API}/status/${track_id}`, { 
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await resp.json();

      if (data.status === "success") {
        return new Response(
          JSON.stringify({
            status: "success",
            title: data.title || "AI Song",
            audio_url: data.audio_url,
            image_url: data.image_url,
          }),
          { headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      if (data.status === "failed") {
        return new Response(
          JSON.stringify({ status: "failed", error: "Song generation failed" }),
          { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
        );
      }

      return new Response(
        JSON.stringify({ status: data.status || "processing" }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: "Invalid action. Use 'start' or 'status'" }),
      { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (e) {
    console.error("song-generate error:", e);
    return new Response(
      JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
