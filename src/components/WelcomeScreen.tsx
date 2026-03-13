import { motion } from "framer-motion";

export const WelcomeScreen = () => {
  return (
    <div className="flex h-full flex-col items-center justify-center px-4 py-16">
      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.4 }}
        className="text-sm text-muted-foreground"
      >
        What can I help you with?
      </motion.p>
    </div>
  );
};
