import { Plus, MessageSquare, Trash2, Search } from 'lucide-react';
import { useChat } from '../hooks/useChatContext';
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
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
            <MessageSquare className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-lg font-semibold text-gray-900">Langflow AI</h1>
        </div>
        
        <button
          onClick={handleNewChat}
          className="w-full btn-primary"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </button>
      </div>

      {/* Search */}
      <div className="p-4">
        <div className="relative">
          <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search chats..."
            className="w-full pl-10 input-field"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Chat Sessions */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {filteredSessions.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <MessageSquare className="w-8 h-8 mx-auto mb-2 text-gray-300" />
            <p className="text-sm">No chats yet</p>
            <p className="text-xs">Start a new conversation</p>
          </div>
        ) : (
          filteredSessions.map((session) => (
            <div
              key={session.id}
              onClick={() => selectSession(session.id)}
              className={`p-3 rounded-lg cursor-pointer transition-all group ${
                currentSession?.id === session.id
                  ? 'bg-blue-100 border border-blue-200'
                  : 'hover:bg-gray-100 border border-transparent'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-sm text-gray-900 truncate">
                    {session.title}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1">
                    {session.messages.length} messages
                  </p>
                  <p className="text-xs text-gray-400 mt-1">
                    {formatDistanceToNow(new Date(session.createdAt), { addSuffix: true })}
                  </p>
                </div>
                <button
                  onClick={(e) => handleDeleteSession(session.id, e)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 rounded text-red-600 transition-all"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
