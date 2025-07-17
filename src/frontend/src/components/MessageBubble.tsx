import { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { Message } from '@/types';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { formatDistanceToNow } from 'date-fns';

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy message:', error);
    }
  };

  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} group`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted border border-border'
        }`}
      >
        {/* Avatar and Role */}
        <div className="flex items-center gap-2 mb-2">
          <div
            className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
              isUser
                ? 'bg-primary-foreground/20 text-primary-foreground'
                : 'bg-primary text-primary-foreground'
            }`}
          >
            {isUser ? 'U' : 'AI'}
          </div>
          <span className="text-xs opacity-75">
            {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
          </span>
          
          <button
            onClick={handleCopy}
            className="opacity-0 group-hover:opacity-100 ml-auto p-1 hover:bg-background/20 rounded transition-all"
            title="Copy message"
          >
            {copied ? (
              <Check className="w-3 h-3" />
            ) : (
              <Copy className="w-3 h-3" />
            )}
          </button>
        </div>

        {/* Message Content */}
        <div className={`prose prose-sm max-w-none ${
          isUser ? 'prose-invert' : 'dark:prose-invert'
        }`}>
          <ReactMarkdown
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={match[1]}
                    PreTag="div"
                    className="rounded-md text-sm"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Metadata */}
        {message.metadata && (
          <div className="mt-2 pt-2 border-t border-current/20">
            <div className="text-xs opacity-75 space-y-1">
              {message.metadata.duration && (
                <div>Duration: {message.metadata.duration}ms</div>
              )}
              {message.metadata.tokens && (
                <div>Tokens: {message.metadata.tokens}</div>
              )}
              {message.metadata.sources && message.metadata.sources.length > 0 && (
                <div>
                  Sources: {message.metadata.sources.join(', ')}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
