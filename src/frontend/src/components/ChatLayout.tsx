import Sidebar from './Sidebar';
import ChatArea from './ChatArea';
import { useChat } from '../hooks/useChatContext';

export default function ChatLayout() {
  const { currentSession } = useChat();

  return (
    <div className="flex h-screen bg-white">
      {/* Sidebar */}
      <div className="w-80 bg-gray-50 border-r border-gray-200">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {currentSession ? (
          <ChatArea session={currentSession} />
        ) : (
          <div className="flex-1 flex items-center justify-center p-8">
            <div className="text-center max-w-2xl animate-fadeIn">
              {/* Logo */}
              <div className="w-16 h-16 mx-auto mb-8 bg-blue-500 rounded-2xl flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              
              <h1 className="text-4xl font-bold mb-4 text-gray-900">
                Welcome to Langflow AI
              </h1>
              
              <p className="text-xl text-gray-600 mb-8">
                Start a conversation with your AI assistant. Create a new chat to begin.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div className="p-6 bg-white rounded-xl border border-gray-200">
                  <div className="w-12 h-12 mx-auto mb-4 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Lightning Fast</h3>
                  <p className="text-sm text-gray-600">Powered by advanced AI models for instant responses</p>
                </div>
                
                <div className="p-6 bg-white rounded-xl border border-gray-200">
                  <div className="w-12 h-12 mx-auto mb-4 bg-green-100 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Reliable</h3>
                  <p className="text-sm text-gray-600">Built on robust Langflow infrastructure</p>
                </div>
                
                <div className="p-6 bg-white rounded-xl border border-gray-200">
                  <div className="w-12 h-12 mx-auto mb-4 bg-purple-100 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Intuitive</h3>
                  <p className="text-sm text-gray-600">Designed for seamless user experience</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
