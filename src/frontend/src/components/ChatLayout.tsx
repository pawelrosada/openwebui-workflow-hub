import Sidebar from './Sidebar';
import ChatArea from './ChatArea';
import { useChat } from '../hooks/useChatContext';

export default function ChatLayout() {
  const { currentSession } = useChat();

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="sidebar-width flex-shrink-0 bg-card border-r border-border">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {currentSession ? (
          <ChatArea session={currentSession} />
        ) : (
          <div className="flex-1 flex items-center justify-center p-8 bg-background">
            <div className="text-center max-w-3xl animate-fadeIn">
              {/* Logo */}
              <div className="w-20 h-20 mx-auto mb-8 bg-primary rounded-3xl flex items-center justify-center shadow-lg">
                <svg className="w-10 h-10 text-primary-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              
              <h1 className="text-5xl font-bold mb-6 text-foreground tracking-tight">
                Welcome to Langflow AI
              </h1>
              
              <p className="text-xl text-muted-foreground mb-12 max-w-2xl mx-auto leading-relaxed">
                Start a conversation with your AI assistant. Create a new chat to begin exploring the possibilities.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
                <div className="p-8 bg-card rounded-2xl border border-border shadow-sm hover:shadow-md transition-all duration-200">
                  <div className="w-16 h-16 mx-auto mb-6 bg-blue-50 rounded-2xl flex items-center justify-center">
                    <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold mb-3 text-card-foreground">Lightning Fast</h3>
                  <p className="text-muted-foreground leading-relaxed">Powered by advanced AI models for instant, intelligent responses</p>
                </div>
                
                <div className="p-8 bg-card rounded-2xl border border-border shadow-sm hover:shadow-md transition-all duration-200">
                  <div className="w-16 h-16 mx-auto mb-6 bg-green-50 rounded-2xl flex items-center justify-center">
                    <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold mb-3 text-card-foreground">Reliable</h3>
                  <p className="text-muted-foreground leading-relaxed">Built on robust Langflow infrastructure for consistent performance</p>
                </div>
                
                <div className="p-8 bg-card rounded-2xl border border-border shadow-sm hover:shadow-md transition-all duration-200">
                  <div className="w-16 h-16 mx-auto mb-6 bg-purple-50 rounded-2xl flex items-center justify-center">
                    <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold mb-3 text-card-foreground">Intuitive</h3>
                  <p className="text-muted-foreground leading-relaxed">Designed for seamless, natural conversation experiences</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
