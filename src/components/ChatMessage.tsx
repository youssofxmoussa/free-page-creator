import { cn } from "@/lib/utils";
import { Download, Music } from "lucide-react";
import { Message } from "@/lib/chat";
import ReactMarkdown from "react-markdown";
import { motion } from "framer-motion";

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={cn("py-3", isUser ? "flex justify-end" : "")}
    >
      {isUser ? (
        <div className="max-w-[85%]">
          {message.image && (
            <div className="mb-2 flex justify-end">
              <div className="overflow-hidden rounded-2xl border border-border/50 inline-block">
                <img src={message.image} alt="Uploaded" className="max-h-72 w-auto object-cover" />
              </div>
            </div>
          )}
          {message.content && (
            <div className="inline-block float-right rounded-2xl rounded-tr-md bg-secondary px-4 py-3 text-[13.5px] text-foreground leading-[1.7]">
              {message.content}
            </div>
          )}
        </div>
      ) : (
        <div className="w-full space-y-3">
          {message.content && (
            <div className="text-[13.5px] leading-[1.7] text-foreground/90 prose-noir">
              <ReactMarkdown
                components={{
                  strong: ({ children }) => <strong className="font-semibold text-cream">{children}</strong>,
                  code: ({ children, className }) => {
                    const isInline = !className;
                    return isInline ? (
                      <code className="rounded bg-secondary px-1.5 py-0.5 text-xs font-mono text-cream">{children}</code>
                    ) : (
                      <code className={cn("block rounded-xl bg-secondary/80 p-4 text-xs font-mono text-cream-dim overflow-x-auto border border-border/50", className)}>{children}</code>
                    );
                  },
                  pre: ({ children }) => <pre className="my-3 overflow-x-auto rounded-xl bg-secondary/80 border border-border/50">{children}</pre>,
                  ul: ({ children }) => <ul className="my-2 ml-4 list-disc space-y-1 text-foreground/80">{children}</ul>,
                  ol: ({ children }) => <ol className="my-2 ml-4 list-decimal space-y-1 text-foreground/80">{children}</ol>,
                  p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                  h1: ({ children }) => <h1 className="text-lg font-semibold text-cream mb-2 mt-4">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-base font-semibold text-cream mb-2 mt-3">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-sm font-semibold text-cream mb-1.5 mt-2">{children}</h3>,
                  a: ({ href, children }) => <a href={href} target="_blank" rel="noopener noreferrer" className="text-cream underline underline-offset-2 hover:text-cream/80">{children}</a>,
                  blockquote: ({ children }) => <blockquote className="border-l-2 border-cream/30 pl-4 my-2 text-foreground/70 italic">{children}</blockquote>,
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}

          {message.generatedImage && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
              className="relative group overflow-hidden rounded-2xl border border-border/50 inline-block"
            >
              <img src={message.generatedImage} alt="Generated" className="max-h-96 w-auto object-cover" />
              <div className="absolute inset-0 bg-gradient-to-t from-background/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end justify-end p-3">
                <a
                  href={message.generatedImage}
                  download="youssofgpt-generated.png"
                  className="flex h-8 w-8 items-center justify-center rounded-full bg-secondary/90 ring-1 ring-border backdrop-blur-sm transition-transform hover:scale-110"
                >
                  <Download className="h-3.5 w-3.5 text-cream" />
                </a>
              </div>
            </motion.div>
          )}

          {message.audioUrl && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
              className="rounded-2xl border border-border/50 bg-secondary/30 p-4 space-y-3"
            >
              <div className="flex items-center gap-2 text-cream">
                <Music className="h-4 w-4" />
                <span className="text-sm font-medium">Generated Song</span>
              </div>
              <audio
                controls
                className="w-full h-10 [&::-webkit-media-controls-panel]:bg-secondary [&::-webkit-media-controls-current-time-display]:text-cream-dim [&::-webkit-media-controls-time-remaining-display]:text-cream-dim"
                src={message.audioUrl}
              />
              <a
                href={message.audioUrl}
                download="youssofgpt-song.mp3"
                className="inline-flex items-center gap-1.5 text-xs text-cream-dim hover:text-cream transition-colors"
              >
                <Download className="h-3 w-3" />
                Download
              </a>
            </motion.div>
          )}
        </div>
      )}
    </motion.div>
  );
};
