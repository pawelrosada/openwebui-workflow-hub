import { useState, useEffect } from 'react';
import { ChatProvider } from './hooks/useChatContext';
import ChatLayout from './components/ChatLayout';
import { ThemeProvider } from './hooks/useTheme';

function App() {
  return (
    <ThemeProvider>
      <ChatProvider>
        <div className="h-screen bg-background text-foreground">
          <ChatLayout />
        </div>
      </ChatProvider>
    </ThemeProvider>
  );
}

export default App;
