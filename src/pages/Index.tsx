import { useState, useRef, useEffect, useCallback } from "react";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { ChatHeader } from "@/components/ChatHeader";
import { WelcomeScreen } from "@/components/WelcomeScreen";
import { AppSidebar } from "@/components/AppSidebar";
import { Message, ChatMode, streamChat } from "@/lib/chat";
import { useAuth } from "@/lib/auth";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

const Index = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const saveMessage = async (convId: string, msg: Message) => {
    if (!user) return;
    await supabase.from("messages").insert({
      id: msg.id,
      conversation_id: convId,
      role: msg.role,
      content: msg.content,
      image: msg.image || null,
      generated_image: msg.generatedImage || null,
      audio_url: msg.audioUrl || null,
    });
  };

  const createConversation = async (firstMessage: string): Promise<string | null> => {
    if (!user) return null;
    const title = firstMessage.slice(0, 50) + (firstMessage.length > 50 ? "..." : "");
    const { data, error } = await supabase
      .from("conversations")
      .insert({ user_id: user.id, title })
      .select("id")
      .single();
    if (error || !data) {
      console.error("Failed to create conversation:", error);
      return null;
    }
    return data.id;
  };

  const loadConversation = async (id: string) => {
    const { data } = await supabase
      .from("messages")
      .select("*")
      .eq("conversation_id", id)
      .order("created_at", { ascending: true });
    if (data) {
      setMessages(
        data.map((m: any) => ({
          id: m.id,
          role: m.role as "user" | "assistant",
          content: m.content,
          timestamp: new Date(m.created_at),
          image: m.image || undefined,
          generatedImage: m.generated_image || undefined,
          audioUrl: m.audio_url || undefined,
        }))
      );
      setConversationId(id);
    }
  };

  const handleSend = async (content: string, image?: File) => {
    const hasImage = !!image;

    let imageDataUrl: string | undefined;
    if (image) {
      imageDataUrl = await fileToBase64(image);
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content,
      timestamp: new Date(),
      image: imageDataUrl,
    };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setIsLoading(true);

    // Create conversation if needed
    let convId = conversationId;
    if (!convId && user) {
      convId = await createConversation(content);
      setConversationId(convId);
    }

    // Save user message
    if (convId) {
      saveMessage(convId, userMessage);
    }

    // Build ALL messages for API
    const apiMessages: Array<{ role: string; content: string | Array<{ type: string; text?: string; image_url?: { url: string } }> }> = [];

    for (const msg of updatedMessages) {
      if (msg.image && msg.role === "user") {
        apiMessages.push({
          role: "user",
          content: [
            { type: "text", text: msg.content || "What is in this image?" },
            { type: "image_url", image_url: { url: msg.image } },
          ],
        });
      } else {
        apiMessages.push({ role: msg.role, content: msg.content });
      }
    }

    const mode = detectMode(content, hasImage);

    let assistantContent = "";
    let assistantId = crypto.randomUUID();

    try {
      await streamChat({
        messages: apiMessages,
        mode,
        onDelta: (chunk) => {
          assistantContent += chunk;
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant") {
              return prev.map((m, i) =>
                i === prev.length - 1 ? { ...m, content: assistantContent } : m
              );
            }
            return [
              ...prev,
              {
                id: assistantId,
                role: "assistant" as const,
                content: assistantContent,
                timestamp: new Date(),
              },
            ];
          });
        },
        onDone: () => {
          setIsLoading(false);
          // Save assistant message
          if (convId) {
            setMessages((prev) => {
              const lastAssistant = prev.find((m) => m.id === assistantId);
              if (lastAssistant) {
                saveMessage(convId!, lastAssistant);
              }
              return prev;
            });
            // Update conversation timestamp
            supabase
              .from("conversations")
              .update({ updated_at: new Date().toISOString() })
              .eq("id", convId);
          }
        },
        onImage: (imageUrl) => {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant") {
              return prev.map((m, i) =>
                i === prev.length - 1 ? { ...m, generatedImage: imageUrl } : m
              );
            }
            return [
              ...prev,
              {
                id: assistantId,
                role: "assistant" as const,
                content: assistantContent || "Here's your image:",
                timestamp: new Date(),
                generatedImage: imageUrl,
              },
            ];
          });
        },
        onAudio: (audioUrl, title, imageUrl) => {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant") {
              return prev.map((m, i) =>
                i === prev.length - 1 ? { ...m, audioUrl } : m
              );
            }
            return [
              ...prev,
              {
                id: assistantId,
                role: "assistant" as const,
                content: assistantContent || `🎵 ${title}`,
                timestamp: new Date(),
                audioUrl,
              },
            ];
          });
        },
        onError: (error) => {
          toast.error(error);
          setIsLoading(false);
        },
      });
    } catch (e) {
      toast.error("Failed to connect to AI. Please try again.");
      setIsLoading(false);
    }
  };

  const detectMode = (content: string, hasImage: boolean): ChatMode => {
    const lower = content.toLowerCase();

    const editKeywords = ["edit", "change", "modify", "transform", "remove", "add to", "replace", "fix", "enhance", "improve", "adjust", "crop", "resize", "filter", "recolor", "make it", "turn it", "convert", "swap", "blend", "merge", "overlay", "mask", "inpaint", "outpaint", "extend", "upscale", "sharpen", "blur", "brighten", "darken", "saturate", "desaturate", "stylize"];

    const genKeywords = ["generate", "create", "draw", "picture", "image of", "photo of", "illustration", "render", "visualize", "paint", "sketch", "design", "make me", "make a", "show me", "depict", "portrait of", "landscape of", "artwork", "poster", "logo of", "icon of", "wallpaper", "banner", "thumbnail"];

    const songKeywords = ["song", "music", "melody", "lyrics", "compose", "beat", "track", "sing", "rap", "instrumental", "chord", "tune", "anthem", "remix", "acoustic", "generate a song", "create a song", "write a song", "make a song", "produce", "اغنية", "اغنيه", "موسيقى", "لحن", "أغنية"];

    if (hasImage && editKeywords.some((k) => lower.includes(k))) {
      return "image-edit";
    }
    if (!hasImage && songKeywords.some((k) => lower.includes(k))) {
      return "song-gen";
    }
    if (!hasImage && genKeywords.some((k) => lower.includes(k))) {
      return "image-gen";
    }
    return "chat";
  };

  const handleNewChat = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="flex h-dvh flex-col bg-background">
      <AppSidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewChat={handleNewChat}
        onSelectConversation={loadConversation}
        activeConversationId={conversationId}
      />

      <ChatHeader
        onNewChat={handleNewChat}
        messageCount={messages.length}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        sidebarOpen={sidebarOpen}
      />

      <div ref={scrollRef} className="flex-1 overflow-y-auto scroll-smooth">
        {messages.length === 0 ? (
          <WelcomeScreen />
        ) : (
          <div className="mx-auto max-w-3xl px-4 py-6 md:px-6">
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isLoading && messages[messages.length - 1]?.role !== "assistant" && (
              <TypingIndicator />
            )}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <ChatInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
};

const TypingIndicator = () => (
  <div className="flex items-center gap-1.5 py-5 animate-fade-up">
    <span className="typing-dot h-1.5 w-1.5 rounded-full bg-cream-dim" />
    <span className="typing-dot h-1.5 w-1.5 rounded-full bg-cream-dim" />
    <span className="typing-dot h-1.5 w-1.5 rounded-full bg-cream-dim" />
  </div>
);

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export default Index;
