import { motion, AnimatePresence } from "framer-motion";
import { X, Plus, MessageSquare, Sparkles, Trash2 } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/lib/auth";
import { useEffect, useState } from "react";

interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}

interface AppSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onNewChat: () => void;
  onSelectConversation: (id: string) => void;
  activeConversationId: string | null;
}

export const AppSidebar = ({
  isOpen,
  onClose,
  onNewChat,
  onSelectConversation,
  activeConversationId,
}: AppSidebarProps) => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);

  useEffect(() => {
    if (!user || !isOpen) return;
    loadConversations();
  }, [user, isOpen]);

  const loadConversations = async () => {
    if (!user) return;
    const { data } = await supabase
      .from("conversations")
      .select("id, title, updated_at")
      .eq("user_id", user.id)
      .order("updated_at", { ascending: false })
      .limit(50);
    if (data) setConversations(data);
  };

  const deleteConversation = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    await supabase.from("conversations").delete().eq("id", id);
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeConversationId === id) {
      onNewChat();
    }
  };

  const handleNewChat = () => {
    onNewChat();
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
          />

          <motion.aside
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="fixed inset-y-0 left-0 z-50 w-72 flex flex-col border-r border-border/40 bg-background/95 backdrop-blur-2xl"
          >
            <div className="flex items-center justify-between px-5 py-4 border-b border-border/30">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cream/20 to-cream/5 ring-1 ring-cream/10">
                  <Sparkles className="h-4 w-4 text-cream" />
                </div>
                <div>
                  <p className="text-sm font-bold tracking-wider text-cream">YoussofGPT</p>
                  <p className="text-[10px] text-muted-foreground">AI Assistant</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition-all hover:bg-secondary hover:text-cream"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            {/* New Chat Button */}
            <div className="px-3 pt-4 pb-2">
              <button
                onClick={handleNewChat}
                className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm text-cream transition-all duration-200 hover:bg-secondary/60 border border-border/30"
              >
                <Plus className="h-4 w-4" />
                <span className="font-medium">New Chat</span>
              </button>
            </div>

            {/* Conversations List */}
            <nav className="flex-1 overflow-y-auto px-3 py-2 space-y-0.5">
              {conversations.length === 0 ? (
                <p className="text-xs text-muted-foreground/50 text-center py-8">
                  No conversations yet
                </p>
              ) : (
                conversations.map((conv, i) => (
                  <motion.button
                    key={conv.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.03 * i, duration: 0.2 }}
                    onClick={() => {
                      onSelectConversation(conv.id);
                      onClose();
                    }}
                    className={`group flex w-full items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm transition-all duration-200 ${
                      activeConversationId === conv.id
                        ? "bg-secondary/80 text-cream"
                        : "text-cream-dim hover:bg-secondary/40 hover:text-cream"
                    }`}
                  >
                    <MessageSquare className="h-3.5 w-3.5 shrink-0 opacity-50" />
                    <span className="truncate flex-1 text-left text-[13px]">{conv.title}</span>
                    <button
                      onClick={(e) => deleteConversation(conv.id, e)}
                      className="opacity-0 group-hover:opacity-100 flex h-6 w-6 items-center justify-center rounded-md transition-all hover:bg-destructive/20 hover:text-destructive"
                    >
                      <Trash2 className="h-3 w-3" />
                    </button>
                  </motion.button>
                ))
              )}
            </nav>

            <div className="border-t border-border/30 px-5 py-4">
              <p className="text-[10px] text-muted-foreground/40 text-center">
                YoussofGPT • Powered by AI
              </p>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
};
