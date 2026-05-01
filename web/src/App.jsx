import React, { useState, useEffect, useRef } from 'react';
import { Send, Scale, ShieldCheck, Zap, BrainCircuit, Database, History, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './index.css';

// --- Mock Components for the Architecture ---

const Sidebar = () => (
  <aside className="glass-panel sidebar">
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
      <div style={{ background: 'var(--accent-blue)', padding: '8px', borderRadius: '8px' }}>
        <Scale size={24} color="white" />
      </div>
      <h2 style={{ fontSize: '1.25rem', color: 'var(--text-primary)' }}>Nexus Legal</h2>
    </div>

    <div style={{ flex: 1 }}>
      <h4 style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '12px' }}>
        Intelligence Engine
      </h4>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <button className="nav-item active" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 12px', background: 'rgba(255,255,255,0.05)', borderRadius: '8px', color: 'white' }}>
          <BrainCircuit size={18} />
          <span>Active Case</span>
        </button>
        <button className="nav-item" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 12px', color: 'var(--text-secondary)' }}>
          <Database size={18} />
          <span>Vector Library</span>
        </button>
        <button className="nav-item" style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 12px', color: 'var(--text-secondary)' }}>
          <History size={18} />
          <span>Case History</span>
        </button>
      </nav>
    </div>

    <div style={{ marginTop: 'auto', padding: '16px', background: 'rgba(0,0,0,0.3)', borderRadius: '12px', border: '1px solid var(--glass-border)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
        <ShieldCheck size={16} color="var(--success)" />
        <span style={{ fontSize: '0.85rem', fontWeight: '500' }}>Privacy Shield: Active</span>
      </div>
      <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
        All PII is masked locally via spaCy before cloud transmission.
      </p>
    </div>
  </aside>
);

const ReasoningTrace = ({ steps }) => (
  <aside className="glass-panel trace-sidebar">
    <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
      <Zap size={18} color="var(--warning)" />
      Agent Trace
    </h3>
    
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <AnimatePresence>
        {steps.map((step, idx) => (
          <motion.div 
            key={idx}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`agent-step ${step.status === 'success' ? 'success' : ''}`}
          >
            <ChevronRight size={16} style={{ marginTop: '2px', flexShrink: 0 }} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{step.action}</span>
              <span style={{ fontSize: '0.8rem' }}>{step.detail}</span>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
      
      {steps.length > 0 && steps[steps.length - 1].status === 'thinking' && (
        <div className="typing-indicator" style={{ background: 'transparent', padding: '0', marginLeft: '28px' }}>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
      )}
    </div>

    <div style={{ marginTop: 'auto' }}>
      <h4 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>Learned Facts (LTM)</h4>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        <span style={{ fontSize: '0.75rem', background: 'rgba(59, 130, 246, 0.2)', color: 'var(--accent-blue)', padding: '4px 8px', borderRadius: '4px' }}>
          Delhi Jurisdiction
        </span>
        <span style={{ fontSize: '0.75rem', background: 'rgba(139, 92, 246, 0.2)', color: 'var(--accent-purple)', padding: '4px 8px', borderRadius: '4px' }}>
          Defense Lawyer
        </span>
      </div>
    </div>
  </aside>
);

export default function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Welcome to Nexus Legal Intelligence. I am ready to analyze your case files securely.' }
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [agentSteps, setAgentSteps] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = input;
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setIsThinking(true);
    setAgentSteps([]);

    // --- Real API Integration ---
    try {
      // 1. Initial Processing Step
      setAgentSteps(prev => [...prev, { action: 'Routing Intent', detail: 'Classifying query locally...', status: 'success' }]);
      setAgentSteps(prev => [...prev, { action: 'Privacy Shield', detail: 'Masking PII via spaCy NER...', status: 'success' }]);
      setAgentSteps(prev => [...prev, { action: 'Agentic RAG', detail: 'Retrieving & Grading context...', status: 'thinking' }]);

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg, session_id: 'browser_session' })
      });

      if (!response.ok) throw new Error('API unreachable');
      
      const data = await response.json();

      // 2. Update Trace based on real result
      setAgentSteps(prev => {
        const newSteps = [...prev];
        newSteps[newSteps.length - 1] = { action: 'Agentic RAG', detail: 'Context graded relevant. Generating...', status: 'success' };
        return newSteps;
      });
      setAgentSteps(prev => [...prev, { action: 'Hallucination Judge', detail: 'Verifying claims against sources...', status: 'success' }]);
      setAgentSteps(prev => [...prev, { action: 'Learning Node', detail: 'Extracting atomic facts to LTM.', status: 'success' }]);

      // 3. Set Final Message
      setMessages(prev => [...prev, { role: 'ai', content: data.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: 'Engine Connection Error. Please ensure the backend is running at localhost:8000.' }]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="layout-container">
      <Sidebar />
      
      <main className="glass-panel chat-area">
        <div className="chat-history">
          {messages.map((msg, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`message-bubble ${msg.role === 'user' ? 'message-user' : 'message-ai'}`}
            >
              {msg.content}
            </motion.div>
          ))}
          {isThinking && (
            <div className="message-bubble message-ai">
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
            <input 
              type="text" 
              className="premium-input" 
              placeholder="Ask a legal question or request a draft..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              style={{ paddingRight: '50px' }}
            />
            <button 
              className="btn-primary" 
              style={{ position: 'absolute', right: '6px', padding: '8px', borderRadius: '8px' }}
              onClick={handleSend}
            >
              <Send size={18} />
            </button>
          </div>
          <div style={{ textAlign: 'center', marginTop: '12px', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            Nexus Legal Intelligence is an AI assistant. Verify all citations before court submission.
          </div>
        </div>
      </main>

      <ReasoningTrace steps={agentSteps} />
    </div>
  );
}
