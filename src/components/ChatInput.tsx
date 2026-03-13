import { useState, useRef, KeyboardEvent } from "react";
import { ArrowUp, ImagePlus, X, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (content: string, image?: File) => void;
  isLoading: boolean;
}

export const ChatInput = ({ onSend, isLoading }: ChatInputProps) => {
  const [input, setInput] = useState("");
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isFocused, setIsFocused] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const canSend = (input.trim() || selectedImage) && !isLoading;

  const handleSend = () => {
    if (!canSend) return;
    onSend(input.trim(), selectedImage || undefined);
    setInput("");
    setSelectedImage(null);
    setImagePreview(null);
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
    // Reset file input so same file can be re-selected
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Revoke previous preview URL to avoid memory leaks
      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }
      setSelectedImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
    // Reset file input value so the same file or a new file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleTextareaInput = () => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 180) + "px";
    }
  };

  const removeImage = () => {
    if (imagePreview) {
      URL.revokeObjectURL(imagePreview);
    }
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="px-4 pb-5 pt-2 md:px-6">
      <div className="mx-auto max-w-3xl">
        {imagePreview && (
          <div className="mb-3 flex items-start gap-2">
            <div className="relative group">
              <img
                src={imagePreview}
                alt="Preview"
                className="h-20 w-20 rounded-xl border border-border/50 object-cover"
              />
              <button
                onClick={removeImage}
                className="absolute -right-2 -top-2 flex h-6 w-6 items-center justify-center rounded-full bg-secondary ring-1 ring-border text-cream-dim hover:text-cream transition-colors"
              >
                <X className="h-3 w-3" />
              </button>
            </div>
          </div>
        )}

        <div
          className={cn(
            "relative flex items-end gap-2 rounded-2xl border bg-secondary/50 p-2 transition-all duration-200",
            isFocused ? "border-cream/15 shadow-[0_0_0_1px_hsl(var(--cream)/0.05)]" : "border-border/60"
          )}
        >
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-muted-foreground transition-colors hover:text-cream-dim hover:bg-accent/50"
            title="Attach image"
          >
            <ImagePlus className="h-[18px] w-[18px]" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            className="hidden"
          />

          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              handleTextareaInput();
            }}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Message YoussofGPT..."
            rows={1}
            className="max-h-44 flex-1 resize-none bg-transparent text-[13.5px] text-foreground placeholder:text-muted-foreground/60 focus:outline-none py-2"
          />

          <button
            onClick={handleSend}
            disabled={!canSend}
            className={cn(
              "flex h-9 w-9 shrink-0 items-center justify-center rounded-xl transition-all duration-200",
              canSend
                ? "bg-cream text-primary-foreground hover:opacity-90 scale-100"
                : "bg-muted text-muted-foreground scale-95 opacity-50"
            )}
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <ArrowUp className="h-4 w-4" />
            )}
          </button>
        </div>

        <p className="mt-2.5 text-center text-[10px] text-muted-foreground/50">
          YoussofGPT may produce inaccurate results. Verify important information.
        </p>
      </div>
    </div>
  );
};
