import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// ── Small helper components ────────────────────────────────────────────────

function Toggle({ id, label, checked, onChange, colorClass = "peer-checked:bg-[var(--accent-green)]" }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm text-[var(--text-muted)] capitalize font-medium">
        {label.replace(/_/g, ' ')}
      </span>
      <label className="relative inline-flex items-center cursor-pointer">
        <input
          id={id}
          type="checkbox"
          className="sr-only peer"
          checked={checked}
          onChange={onChange}
        />
        <div className={`w-10 h-5 bg-[#EBE5DC] peer-focus:outline-none rounded-full peer
                        peer-checked:after:translate-x-full peer-checked:after:border-white
                        after:content-[''] after:absolute after:top-[2px] after:left-[2px]
                        after:bg-white after:border-[#EBE5DC] after:border after:rounded-full
                        after:h-4 after:w-4 after:transition-all ${colorClass} shadow-inner`} />
      </label>
    </div>
  );
}

function TypingDots() {
  return (
    <div className="flex gap-1 px-5 py-4 rounded-[1.5rem] rounded-bl-sm bg-[var(--bot-msg)] w-fit">
      {[0, 150, 300].map((delay) => (
        <span
          key={delay}
          className="w-2 h-2 rounded-full bg-[#8A7B72] animate-bounce"
          style={{ animationDelay: `${delay}ms` }}
        />
      ))}
    </div>
  );
}

// ── PDF Upload Panel ───────────────────────────────────────────────────────

function FileUploadPanel() {
  const [status, setStatus] = useState('idle'); // idle | uploading | success | error
  const [message, setMessage] = useState('');
  const [chunks, setChunks] = useState(0);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  const uploadFile = async (file) => {
    const allowedExts = ['.pdf', '.docx', '.pptx', '.html', '.htm', '.txt'];
    const ext = file ? file.name.substring(file.name.lastIndexOf('.')).toLowerCase() : '';
    if (!file || !allowedExts.includes(ext)) {
      setStatus('error');
      setMessage('Please select a valid document file.');
      return;
    }

    setStatus('uploading');
    setMessage(`Uploading "${file.name}"…`);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_BASE_URL}/api/upload-file`, {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || 'Upload failed');

      setStatus('success');
      setChunks(data.chunks_loaded);
      setMessage(`"${data.filename}" — ${data.chunks_loaded} chunks indexed`);
    } catch (err) {
      setStatus('error');
      setMessage(err.message);
    }
  };

  const onFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) uploadFile(file);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) uploadFile(file);
  };

  const statusColor = {
    idle: 'border-[var(--border-color)] bg-[var(--app-bg)]',
    uploading: 'border-[var(--accent-orange)] bg-[#FDFBF7]',
    success: 'border-[var(--accent-green)] bg-[#FDFBF7]',
    error: 'border-red-400 bg-[#FDFBF7]',
  };

  return (
    <div className="pt-5 border-t border-[var(--border-color)]">
      <h3 className="text-xs uppercase tracking-wider text-[var(--text-muted)] font-bold mb-3">
        Upload Document
      </h3>

      <div
        onClick={() => status !== 'uploading' && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`
          relative flex flex-col items-center justify-center gap-2
          border-2 border-dashed rounded-[1.5rem] p-5 cursor-pointer
          transition-all duration-200
          ${statusColor[status]}
          ${dragging ? 'scale-[1.02] border-[var(--accent-orange)]' : 'hover:border-[#C6AFA1]'}
        `}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.pptx,.html,.htm,.txt"
          className="hidden"
          onChange={onFileChange}
        />

        {status === 'uploading' ? (
          <>
            <svg className="animate-spin w-6 h-6 text-[var(--accent-orange)]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
            </svg>
            <span className="text-xs text-[var(--text-muted)] text-center font-medium">{message}</span>
          </>
        ) : status === 'success' ? (
          <>
            <svg className="w-6 h-6 text-[var(--accent-green)]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-xs text-[var(--text-main)] font-medium text-center">{message}</span>
            <button
              onClick={(e) => { e.stopPropagation(); setStatus('idle'); setMessage(''); }}
              className="text-xs text-[var(--text-muted)] underline hover:text-[var(--text-main)] mt-1"
            >
              Upload another
            </button>
          </>
        ) : status === 'error' ? (
          <>
            <svg className="w-6 h-6 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-xs text-red-500 text-center font-medium">{message}</span>
            <button
              onClick={(e) => { e.stopPropagation(); setStatus('idle'); setMessage(''); }}
              className="text-xs text-[var(--text-muted)] underline hover:text-[var(--text-main)] mt-1"
            >
              Try again
            </button>
          </>
        ) : (
          <>
            <svg className="w-7 h-7 text-[var(--text-muted)]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 16v-8m0 0l-3 3m3-3l3 3M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1" />
            </svg>
            <p className="text-xs text-[var(--text-muted)] font-medium text-center leading-relaxed">
              Click or drag &amp; drop a file
            </p>
          </>
        )}
      </div>
    </div>
  );
}

// ── Main App ───────────────────────────────────────────────────────────────

export default function App() {
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [config, setConfig] = useState({
    manual_override: false,
    enable_decomposition: true,
    enable_hyde: true,
    enable_crag: true,
    enable_reranking: true,
    enable_learning: true,
  });
  const [sessionsList, setSessionsList] = useState([]);

  const chatEndRef = useRef(null);

  // ── Session Management ──────────────────────────────────────────────────
  const loadSessions = () => {
    const list = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('rag_messages_')) {
        const sid = key.replace('rag_messages_', '');
        try {
          const msgs = JSON.parse(localStorage.getItem(key));
          const userMsg = msgs.find(m => m.sender === 'user');
          const title = userMsg ? userMsg.text.substring(0, 30) + (userMsg.text.length > 30 ? '...' : '') : 'New Chat';
          list.push({ id: sid, title, timestamp: msgs[0]?.id || 0 });
        } catch(e) {}
      }
    }
    list.sort((a, b) => b.timestamp - a.timestamp);
    setSessionsList(list);
  };

  const switchSession = (sid) => {
    localStorage.setItem('rag_session_id', sid);
    setSessionId(sid);
    const saved = localStorage.getItem(`rag_messages_${sid}`);
    if (saved) {
      setMessages(JSON.parse(saved));
    }
    setIsSidebarOpen(false);
  };

  // ── Initialise session + memory ─────────────────────────────────────────
  useEffect(() => {
    loadSessions();
    let sid = localStorage.getItem('rag_session_id');
    if (!sid) {
      sid = 'session_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('rag_session_id', sid);
    }
    setSessionId(sid);

    const saved = localStorage.getItem(`rag_messages_${sid}`);
    setMessages(
      saved
        ? JSON.parse(saved)
        : [
            {
              id: Date.now(),
              sender: 'bot',
              text:
                "Hello! I'm the Self-Healing RAG assistant. My conversation is persisted locally — I'll remember our chat even if you refresh. Upload a PDF or ask me anything!",
            },
          ]
    );
  }, []);

  // ── Persist + auto-scroll ────────────────────────────────────────────────
  useEffect(() => {
    if (sessionId && messages.length > 0) {
      localStorage.setItem(`rag_messages_${sessionId}`, JSON.stringify(messages));
      loadSessions();
    }
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sessionId]);

  // ── New chat ─────────────────────────────────────────────────────────────
  const startNewChat = () => {
    const sid = 'session_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('rag_session_id', sid);
    setSessionId(sid);
    const initialMsg = {
      id: Date.now(),
      sender: 'bot',
      text: 'New conversation started. How can I help?',
    };
    setMessages([initialMsg]);
    localStorage.setItem(`rag_messages_${sid}`, JSON.stringify([initialMsg]));
    loadSessions();
  };

  // ── Submit Feedback ──────────────────────────────────────────────────────
  const submitFeedback = async (query, answer, isPositive, msgId) => {
    try {
      await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, answer, is_positive: isPositive }),
      });
      setMessages((prev) =>
        prev.map((m) => (m.id === msgId ? { ...m, feedbackSubmitted: true } : m))
      );
    } catch (err) {
      console.error('Failed to submit feedback', err);
    }
  };

  // ── Send message ─────────────────────────────────────────────────────────
  const sendMessage = async (e) => {
    e.preventDefault();
    const query = inputQuery.trim();
    if (!query) return;

    setMessages((prev) => [...prev, { id: Date.now(), sender: 'user', text: query }]);
    setInputQuery('');
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: sessionId, ...config }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, sender: 'bot', text: data.answer, metadata: data, originalQuery: query, feedbackSubmitted: false },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'bot',
          text: `Error: ${err.message}. Is the backend running at ${API_BASE_URL}?`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="flex h-screen bg-[var(--bg-color)] p-2 md:p-4 items-center justify-center font-sans">
      <div className="w-full h-full flex flex-row rounded-[1.5rem] md:rounded-[2rem] overflow-hidden shadow-[0_20px_50px_rgba(72,57,51,0.2)] bg-[var(--app-bg)] relative">

      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div className="absolute inset-0 bg-black/20 z-10 md:hidden" onClick={() => setIsSidebarOpen(false)} />
      )}

      {/* ── Sidebar ──────────────────────────────────────────────────────── */}
      <aside className={`w-72 md:w-80 bg-[var(--sidebar-bg)] border-r border-[var(--border-color)] flex flex-col flex-shrink-0 absolute md:relative z-20 h-full transition-transform duration-300 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        {/* Header */}
        <div className="p-7 border-b border-[var(--border-color)]">
          <h1 className="text-2xl font-extrabold tracking-tight flex items-center gap-2.5">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="url(#logo-gradient)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <defs>
                <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="var(--accent-orange)" />
                  <stop offset="100%" stopColor="var(--accent-green)" />
                </linearGradient>
              </defs>
              <path d="M2 12h4l3-9 5 18 3-9h5" />
            </svg>
            <span className="drop-shadow-sm">
              <span className="text-[var(--accent-orange)]">Docu</span><span className="text-[var(--accent-green)]">Mind</span>
            </span>
          </h1>
          <p className="text-[11px] text-[var(--text-muted)] mt-2 font-bold uppercase tracking-widest">Self-Healing RAG Engine</p>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-7">
          {/* New chat */}
          <button
            onClick={startNewChat}
            className="w-full flex items-center justify-center gap-2
                       bg-[var(--accent-green)] hover:bg-[#798C5A] active:bg-[#68784D]
                       text-white text-[15px] font-semibold py-3.5 px-4 rounded-full
                       shadow-md shadow-[#8BA067]/20 transition-all transform hover:scale-[1.02]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            New Chat
          </button>

          {/* Recent Chats */}
          {sessionsList.length > 0 && (
            <div className="pt-2">
              <h3 className="text-[11px] uppercase tracking-wider text-[var(--text-muted)] font-bold mb-3 pl-1">Recent Chats</h3>
              <div className="space-y-1.5 max-h-40 overflow-y-auto pr-2">
                {sessionsList.map(session => (
                  <button
                    key={session.id}
                    onClick={() => switchSession(session.id)}
                    className={`w-full text-left px-4 py-3 rounded-2xl text-[14px] truncate transition-colors font-medium ${
                      session.id === sessionId
                        ? 'bg-[var(--border-color)] text-[var(--text-main)] font-bold'
                        : 'text-[var(--text-muted)] hover:bg-[var(--border-color)]/50 hover:text-[var(--text-main)]'
                    }`}
                  >
                    {session.title}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Toggles */}
          <div className="space-y-4 pt-5 border-t border-[var(--border-color)]">
            <h3 className="text-[11px] uppercase tracking-wider text-[var(--text-muted)] font-bold mb-2 pl-1">Pipeline Config</h3>
            
            {/* Always show manual override */}
            <Toggle
              id="manual_override"
              label="manual override"
              checked={config.manual_override}
              onChange={() => setConfig((prev) => ({ ...prev, manual_override: !prev.manual_override }))}
              colorClass="peer-checked:bg-[#ef4444]"
            />

            {/* Conditionally show other toggles */}
            {config.manual_override && Object.entries(config)
              .filter(([key]) => key !== 'manual_override')
              .map(([key, value]) => (
                <div key={key} className="pl-4 border-l-2 border-[#EBE5DC]">
                  <Toggle
                    id={key}
                    label={key.replace('enable_', '')}
                    checked={value}
                    onChange={() => setConfig((prev) => ({ ...prev, [key]: !prev[key] }))}
                  />
                </div>
            ))}
          </div>

          {/* File Upload */}
          <FileUploadPanel />
        </div>


      </aside>

      {/* ── Chat area ────────────────────────────────────────────────────── */}
      <main className="flex-1 flex flex-col min-w-0 bg-[var(--app-bg)] relative">
        {/* Mobile Header */}
        <div className="md:hidden flex items-center justify-between p-4 border-b border-[var(--border-color)] bg-[var(--app-bg)] z-10 shadow-sm">
          <button onClick={() => setIsSidebarOpen(true)} className="p-2 -ml-2 text-[var(--text-main)] active:scale-95 transition-transform">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
          </button>
          <span className="font-extrabold tracking-tight flex items-center gap-1.5 text-lg">
            <span className="text-[var(--accent-orange)]">Docu</span><span className="text-[var(--accent-green)]">Mind</span>
          </span>
          <div className="w-8"></div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6 md:px-12 space-y-7">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col max-w-[78%] ${
                msg.sender === 'user' ? 'ml-auto items-end' : 'mr-auto items-start'
              }`}
            >
              <div
                className={`px-6 py-4 leading-relaxed text-[15px] shadow-sm ${
                  msg.sender === 'user'
                    ? 'bg-[var(--user-msg)] text-[#FDFBF7] rounded-[1.5rem] rounded-br-sm whitespace-pre-wrap'
                    : msg.text === 'New conversation started. How can I help?'
                    ? 'bg-[var(--sidebar-bg)] border border-[var(--border-color)] text-[var(--text-muted)] rounded-[1.5rem] rounded-bl-sm font-medium'
                    : 'bg-[var(--bot-msg)] text-[var(--text-main)] rounded-[1.5rem] rounded-bl-sm prose prose-sm prose-stone max-w-none'
                }`}
              >
                {msg.sender === 'user' ? (
                  msg.text
                ) : (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
                )}
              </div>

              {msg.metadata && (
                <div className="flex flex-wrap gap-4 mt-2.5 text-[12px] font-medium text-[var(--text-muted)]">
                  {msg.metadata.processing_time != null && (
                    <span className="flex items-center gap-1.5">
                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />
                      </svg>
                      {msg.metadata.processing_time}s
                    </span>
                  )}
                  {msg.metadata.techniques_used?.length > 0 && (
                    <span className="flex items-center gap-1.5">
                      <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
                      </svg>
                      {msg.metadata.techniques_used.join(' · ')}
                    </span>
                  )}
                  {msg.metadata.final_documents != null && (
                    <span>{msg.metadata.final_documents} docs used</span>
                  )}
                </div>
              )}
              
              {msg.sender === 'bot' && msg.originalQuery && !msg.feedbackSubmitted && (
                <div className="flex gap-4 mt-3 ml-2 items-center">
                  <span className="text-[11px] font-bold text-[var(--text-muted)] uppercase tracking-wide">Was this helpful?</span>
                  <button onClick={() => submitFeedback(msg.originalQuery, msg.text, true, msg.id)} className="text-[var(--text-muted)] hover:text-[var(--accent-green)] transition-transform hover:scale-110" title="Good answer">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
                  </button>
                  <button onClick={() => submitFeedback(msg.originalQuery, msg.text, false, msg.id)} className="text-[var(--text-muted)] hover:text-red-500 transition-transform hover:scale-110" title="Bad answer">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-2"></path></svg>
                  </button>
                </div>
              )}
              {msg.sender === 'bot' && msg.feedbackSubmitted && (
                <div className="flex gap-2 mt-3 ml-2 items-center text-[12px] font-bold text-[var(--accent-green)]">
                  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  Feedback recorded!
                </div>
              )}
            </div>
          ))}

          {isLoading && (
            <div className="mr-auto">
              <TypingDots />
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div className="px-4 py-5 md:px-12 border-t border-[var(--border-color)] bg-[var(--app-bg)] relative z-10">
          <form
            onSubmit={sendMessage}
            className="flex items-center max-w-4xl mx-auto
                       bg-[var(--sidebar-bg)] border-2 border-[var(--border-color)] rounded-full
                       px-3 py-2.5 focus-within:border-[var(--accent-orange)] focus-within:bg-[#FDFBF7]
                       transition-all shadow-sm"
          >
            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              placeholder="Ask anything about your documents…"
              className="flex-1 bg-transparent border-none text-[var(--text-main)] placeholder-[var(--text-muted)]
                         px-4 py-2.5 outline-none text-[15px] font-medium"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputQuery.trim()}
              className="bg-[var(--accent-orange)] hover:bg-[#E06A4B] disabled:bg-[var(--border-color)] disabled:text-[var(--text-muted)]
                         disabled:cursor-not-allowed text-white rounded-full
                         p-3 ml-2 transition-transform transform hover:scale-105 active:scale-95 flex items-center justify-center
                         h-[48px] w-[48px] flex-shrink-0 shadow-md shadow-[#F57D5C]/30"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </form>
        </div>
      </main>
      </div>
    </div>
  );
}
