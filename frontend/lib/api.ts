/**
 * API Client for Advanced Customer Service AI
 * Handles SSE streaming communication with FastAPI backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  agentType?: 'billing' | 'technical' | 'policy';
  timestamp?: string;
}

export interface StreamEvent {
  type: 'start' | 'agent' | 'token' | 'complete' | 'error';
  content?: string;
  agent_type?: 'billing' | 'technical' | 'policy';
  session_id?: string;
  message?: string;
  timestamp?: string;
}

export interface StreamCallbacks {
  onStart?: (sessionId: string) => void;
  onAgent?: (agentType: 'billing' | 'technical' | 'policy') => void;
  onToken?: (token: string) => void;
  onComplete?: (sessionId: string, agentType: string) => void;
  onError?: (error: string) => void;
}

/**
 * Send a chat message and stream the response via SSE
 */
export async function sendMessage(
  message: string,
  sessionId: string | null,
  callbacks: StreamCallbacks
): Promise<void> {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    if (!response.body) {
      throw new Error('Response body is null');
    }

    // Read the SSE stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        break;
      }

      // Decode the chunk and add to buffer
      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE messages
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // Keep incomplete line in buffer

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data: StreamEvent = JSON.parse(line.slice(6));

            switch (data.type) {
              case 'start':
                if (data.session_id && callbacks.onStart) {
                  callbacks.onStart(data.session_id);
                }
                break;

              case 'agent':
                if (data.agent_type && callbacks.onAgent) {
                  callbacks.onAgent(data.agent_type);
                }
                break;

              case 'token':
                if (data.content && callbacks.onToken) {
                  callbacks.onToken(data.content);
                }
                break;

              case 'complete':
                if (data.session_id && data.agent_type && callbacks.onComplete) {
                  callbacks.onComplete(data.session_id, data.agent_type);
                }
                break;

              case 'error':
                if (data.message && callbacks.onError) {
                  callbacks.onError(data.message);
                }
                break;
            }
          } catch (e) {
            console.error('Error parsing SSE event:', e);
          }
        }
      }
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    if (callbacks.onError) {
      callbacks.onError(errorMessage);
    }
    throw error;
  }
}

/**
 * Check backend health
 */
export async function checkHealth(): Promise<{
  status: string;
  service: string;
  agents: string[];
  sessions_active: number;
}> {
  const response = await fetch(`${API_URL}/health`);
  
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }

  return response.json();
}

/**
 * Get session information
 */
export async function getSession(sessionId: string): Promise<{
  session_id: string;
  message_count: number;
  current_agent: string | null;
  has_cached_billing: boolean;
}> {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to get session: ${response.status}`);
  }

  return response.json();
}

/**
 * Delete a session
 */
export async function deleteSession(sessionId: string): Promise<void> {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error(`Failed to delete session: ${response.status}`);
  }
}

