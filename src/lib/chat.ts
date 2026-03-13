export type MessageRole = "user" | "assistant";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  image?: string;
  generatedImage?: string;
  audioUrl?: string;
}

export type ChatMode = "chat" | "image-gen" | "image-edit" | "song-gen";

const CHAT_URL = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/chat`;
const SONG_URL = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/song-generate`;

interface StreamChatParams {
  messages: { role: string; content: string | Array<{ type: string; text?: string; image_url?: { url: string } }> }[];
  mode: ChatMode;
  onDelta: (delta: string) => void;
  onDone: () => void;
  onImage?: (imageUrl: string) => void;
  onAudio?: (audioUrl: string, title: string, imageUrl?: string) => void;
  onError?: (error: string) => void;
}

export async function streamChat({ messages, mode, onDelta, onDone, onImage, onAudio, onError }: StreamChatParams) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY}`,
  };

  // Song generation - separate flow
  if (mode === "song-gen") {
    try {
      // Extract the last user message as the song idea
      const lastMsg = messages[messages.length - 1];
      const idea = typeof lastMsg.content === "string" ? lastMsg.content : "Create a song";

      onDelta("🎵 Starting song generation...\n\n");

      // Start generation
      const startResp = await fetch(SONG_URL, {
        method: "POST",
        headers,
        body: JSON.stringify({ action: "start", idea }),
      });
      const startData = await startResp.json();

      if (!startData.track_id) {
        onError?.("Failed to start song generation");
        onDone();
        return;
      }

      onDelta("⏳ Generating your song, this may take a minute...\n");

      // Poll for status
      const trackId = startData.track_id;
      let attempts = 0;
      const maxAttempts = 60;

      const poll = async () => {
        while (attempts < maxAttempts) {
          attempts++;
          await new Promise((r) => setTimeout(r, 5000));

          try {
            const statusResp = await fetch(SONG_URL, {
              method: "POST",
              headers,
              body: JSON.stringify({ action: "status", track_id: trackId }),
            });
            const statusData = await statusResp.json();

            if (statusData.status === "success") {
              onDelta(`\n✅ **${statusData.title || "Your Song"}** is ready!\n`);
              onAudio?.(statusData.audio_url, statusData.title || "AI Song", statusData.image_url);
              onDone();
              return;
            }

            if (statusData.status === "failed") {
              onError?.("Song generation failed. Please try again.");
              onDone();
              return;
            }
          } catch {
            // Continue polling
          }
        }

        onError?.("Song generation timed out. Please try again.");
        onDone();
      };

      await poll();
      return;
    } catch (e) {
      onError?.("Failed to generate song");
      onDone();
      return;
    }
  }

  const resp = await fetch(CHAT_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({ messages, mode }),
  });

  if (!resp.ok) {
    const errorData = await resp.json().catch(() => ({ error: "Request failed" }));
    onError?.(errorData.error || `Error ${resp.status}`);
    onDone();
    return;
  }

  // Image generation/editing returns JSON directly
  if (mode === "image-gen" || mode === "image-edit") {
    const data = await resp.json();
    const images = data.choices?.[0]?.message?.images;
    
    if (mode === "image-edit") {
      // For image editing, only show the edited image, minimal text
      if (images?.[0]?.image_url?.url) {
        onDelta("✅ Here's your edited image:");
        onImage?.(images[0].image_url.url);
      } else {
        const text = data.choices?.[0]?.message?.content || "";
        if (text) onDelta(text);
      }
    } else {
      // Image generation - show text + image
      const text = data.choices?.[0]?.message?.content || "";
      if (text) onDelta(text);
      if (images?.[0]?.image_url?.url) {
        onImage?.(images[0].image_url.url);
      }
    }
    onDone();
    return;
  }

  // Streaming text
  if (!resp.body) {
    onError?.("No response body");
    onDone();
    return;
  }

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let textBuffer = "";
  let streamDone = false;

  while (!streamDone) {
    const { done, value } = await reader.read();
    if (done) break;
    textBuffer += decoder.decode(value, { stream: true });

    let newlineIndex: number;
    while ((newlineIndex = textBuffer.indexOf("\n")) !== -1) {
      let line = textBuffer.slice(0, newlineIndex);
      textBuffer = textBuffer.slice(newlineIndex + 1);

      if (line.endsWith("\r")) line = line.slice(0, -1);
      if (line.startsWith(":") || line.trim() === "") continue;
      if (!line.startsWith("data: ")) continue;

      const jsonStr = line.slice(6).trim();
      if (jsonStr === "[DONE]") {
        streamDone = true;
        break;
      }

      try {
        const parsed = JSON.parse(jsonStr);
        const content = parsed.choices?.[0]?.delta?.content as string | undefined;
        if (content) onDelta(content);
      } catch {
        textBuffer = line + "\n" + textBuffer;
        break;
      }
    }
  }

  // Final flush
  if (textBuffer.trim()) {
    for (let raw of textBuffer.split("\n")) {
      if (!raw) continue;
      if (raw.endsWith("\r")) raw = raw.slice(0, -1);
      if (raw.startsWith(":") || raw.trim() === "") continue;
      if (!raw.startsWith("data: ")) continue;
      const jsonStr = raw.slice(6).trim();
      if (jsonStr === "[DONE]") continue;
      try {
        const parsed = JSON.parse(jsonStr);
        const content = parsed.choices?.[0]?.delta?.content as string | undefined;
        if (content) onDelta(content);
      } catch { /* ignore */ }
    }
  }

  onDone();
}
