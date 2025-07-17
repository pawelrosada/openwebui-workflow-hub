import { useState, useRef, useEffect } from 'react';
import { Send, Paperclip } from 'lucide-react';
import { useChat } from '../hooks/useChatContext';
import MessageList from './MessageList';
import { ChatSession } from '@/types';

interface ChatAreaProps {
  session: ChatSession;
}

export default function ChatArea({ session }: ChatAreaProps) {
  const [message, setMessage] = useState('');
  const { sendMessage, isLoading, isTyping } = useChat();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;

    const messageContent = message;
    setMessage('');
    
    try {
      await sendMessage(messageContent);
    } catch (error) {
      console.error('Failed to send message:', error);
      // You could show an error toast here
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-border p-4">
        <h2 className="font-semibold text-lg truncate">{session.title}</h2>
        <p className="text-sm text-muted-foreground">
          {session.messages.length} messages
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList 
          messages={session.messages} 
          isTyping={isTyping}
        />
      </div>

      {/* Input Area */}
      <div className="border-t border-border p-4">
        <form onSubmit={handleSubmit} className="flex items-end gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className="w-full resize-none rounded-lg border border-input bg-background px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent max-h-32 min-h-[44px]"
              rows={1}
              disabled={isLoading}
            />
            <button
              type="button"
              className="absolute right-2 bottom-2 p-1 text-muted-foreground hover:text-foreground transition-colors"
              disabled={isLoading}
            >
              <Paperclip className="w-4 h-4" />
            </button>
          </div>
          
          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="p-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <div className="spinner" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </form>
        
        <p className="text-xs text-muted-foreground mt-2 text-center">
          Press Enter to send, Shift + Enter for new line
        </p>
      </div>
    </div>
  );
}
