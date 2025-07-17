import { WebSocketMessage } from '@/types/index.js';
import { WebSocket } from 'ws';

interface SocketConnection {
  socket: WebSocket;
}

export function websocketHandler(connection: SocketConnection) {
  console.log('WebSocket connection established');

  connection.socket.on('message', (message: Buffer) => {
    try {
      const data: WebSocketMessage = JSON.parse(message.toString());
      
      switch (data.type) {
        case 'message':
          // Handle incoming chat message
          handleChatMessage(connection, data);
          break;
          
        case 'status':
          // Handle status updates
          handleStatusUpdate(connection, data);
          break;
          
        default:
          console.log('Unknown WebSocket message type:', data.type);
      }
    } catch (error) {
      console.error('WebSocket message parsing error:', error);
      connection.socket.send(JSON.stringify({
        type: 'error',
        data: { error: 'Invalid message format' }
      }));
    }
  });

  connection.socket.on('close', () => {
    console.log('WebSocket connection closed');
  });

  connection.socket.on('error', (error: Error) => {
    console.error('WebSocket error:', error);
  });

  // Send initial connection confirmation
  connection.socket.send(JSON.stringify({
    type: 'status',
    data: { status: 'connected', timestamp: new Date().toISOString() }
  }));
}

function handleChatMessage(connection: SocketConnection, data: WebSocketMessage) {
  // Echo back for now - in real implementation, integrate with Langflow streaming
  connection.socket.send(JSON.stringify({
    type: 'message',
    data: {
      ...data.data,
      echo: true,
      timestamp: new Date().toISOString()
    }
  }));
}

function handleStatusUpdate(connection: SocketConnection, data: WebSocketMessage) {
  console.log('Status update:', data);
  // Handle status updates (typing indicators, etc.)
}
