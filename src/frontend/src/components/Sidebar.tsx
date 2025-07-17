import { Plus, MessageSquare, Trash2, Search, Moon, Sun } from 'lucide-react';
import { useChat } from '../hooks/useChatContext';
import { useTheme } from '../hooks/useTheme';
import { formatDistanceToNow } from 'date-fns';
import { useState } from 'react';

export default function Sidebar() {
  const { 
    sessions, 
    currentSession, 
    createNewSession, 
    selectSession, 
    deleteSession 
  } = useChat();
  const { theme, toggleTheme } = useTheme();
  const [searchQuery, setSearchQuery] = useState('');

  const handleNewChat = async () => {
    try {
      await createNewSession();
    } catch (error) {
      console.error('Failed to create new chat:', error);
    }
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this chat?')) {
      await deleteSession(sessionId);
    }
  };

  const filteredSessions = sessions.filter(session =>
    session.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex flex-col h-full bg-card border-r border-border">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-sm">
              <MessageSquare className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-semibold text-card-foreground">Langflow AI</h1>
          </div>
          
          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-3 rounded-xl bg-secondary hover:bg-accent transition-all duration-200 shadow-sm"
            title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
          >
            {theme === 'light' ? (
              <Moon className="w-5 h-5 text-secondary-foreground" />
            ) : (
              <Sun className="w-5 h-5 text-secondary-foreground" />
            )}
          </button>
        </div>
        
        <button
          onClick={handleNewChat}
          className="w-full btn-primary text-base font-medium"
        >
          <Plus className="w-5 h-5" />
          New Chat
        </button>
      </div>

      {/* Search */}
      <div className="p-6 pb-4">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search conversations..."
            className="w-full pl-12 input-field"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Chat Sessions */}
      <div className="flex-1 overflow-y-auto px-3">
        {filteredSessions.length === 0 ? (
          <div className="p-6 text-center text-muted-foreground">
            <div className="text-sm">No conversations yet</div>
            <div className="text-xs mt-1">Start a new chat to begin</div>
          </div>
        ) : (
          <div className="space-y-2">
            {filteredSessions.map((session) => (
              <div
                key={session.id}
                onClick={() => selectSession(session.id)}
                className={`group flex items-center justify-between p-4 rounded-xl cursor-pointer transition-all duration-200 ${
                  currentSession?.id === session.id
                    ? 'bg-primary/10 border border-primary/20 shadow-sm'
                    : 'hover:bg-secondary hover:shadow-sm'
                }`}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <MessageSquare className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                    <h3 className={`font-medium truncate text-sm ${
                      currentSession?.id === session.id
                        ? 'text-primary'
                        : 'text-card-foreground'
                    }`}>
                      {session.title}
                    </h3>
                  </div>
                  <p className="text-xs text-muted-foreground ml-7">
                    {formatDistanceToNow(new Date(session.createdAt), { addSuffix: true })}
                  </p>
                </div>
                
                <button
                  onClick={(e) => handleDeleteSession(session.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-2 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all duration-200"
                  title="Delete conversation"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
