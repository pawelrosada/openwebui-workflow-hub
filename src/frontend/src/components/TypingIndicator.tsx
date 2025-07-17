export default function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="max-w-[80%] rounded-lg px-4 py-3 bg-muted border border-border">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium bg-primary text-primary-foreground">
            AI
          </div>
          <span className="text-xs opacity-75">typing...</span>
        </div>
        
        <div className="typing-indicator">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
      </div>
    </div>
  );
}
