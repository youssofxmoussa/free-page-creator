import { motion } from "framer-motion";
import { useAuth } from "@/lib/auth";
import { LogOut } from "lucide-react";

interface ChatHeaderProps {
  onNewChat: () => void;
  messageCount: number;
  onToggleSidebar: () => void;
  sidebarOpen: boolean;
}

export const ChatHeader = ({ onNewChat, messageCount, onToggleSidebar, sidebarOpen }: ChatHeaderProps) => {
  const { profile, signOut } = useAuth();

  return (
    <header className="flex items-center justify-between px-4 py-3 md:px-6 bg-background/80 backdrop-blur-xl sticky top-0 z-10">
      {/* Animated Hamburger */}
      <button
        onClick={onToggleSidebar}
        className="group relative flex h-10 w-10 items-center justify-center rounded-xl transition-all duration-300"
        title="Menu"
      >
        <div className="flex flex-col items-center justify-center gap-[5px]">
          <motion.span
            animate={sidebarOpen ? { rotate: 45, y: 7, width: 20 } : { rotate: 0, y: 0, width: 20 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="block h-[2px] rounded-full bg-cream-dim transition-colors group-hover:bg-cream origin-center"
          />
          <motion.span
            animate={sidebarOpen ? { opacity: 0, scaleX: 0 } : { opacity: 1, scaleX: 1 }}
            transition={{ duration: 0.2 }}
            className="block h-[2px] w-3.5 rounded-full bg-cream-dim transition-colors group-hover:bg-cream"
          />
          <motion.span
            animate={sidebarOpen ? { rotate: -45, y: -7, width: 20 } : { rotate: 0, y: 0, width: 16 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="block h-[2px] rounded-full bg-cream-dim transition-colors group-hover:bg-cream origin-center"
          />
        </div>
      </button>

      {/* Center Title */}
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
        <h1 className="text-sm font-bold tracking-[0.2em] text-cream uppercase">YoussofGPT</h1>
      </div>

      {/* User Avatar / Sign Out */}
      <div className="flex items-center gap-2">
        {profile && (
          <button
            onClick={signOut}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-cream"
            title="Sign out"
          >
            <LogOut className="h-4 w-4" />
          </button>
        )}
      </div>
    </header>
  );
};
