import React, { useState, useRef, useEffect, useCallback } from 'react';
import { sendQuery, queryChecklist, uploadIncident, uploadSchedule, healthCheck, getSources } from '../api/client';
import ResponseRenderer from '../components/ResponseRenderer';

// ─── Top Status Bar (glass) ──────────────────────────────────────
function StatusBar({ theme, toggleTheme, status, sourceCount }) {
  const [time, setTime] = useState(new Date());
  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 30000);
    return () => clearInterval(t);
  }, []);
  const utc = time.toUTCString().slice(17, 25);

  return (
    <header className="glass-strong" style={{
      padding: '10px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexShrink: 0,
      position: 'sticky',
      top: 0,
      zIndex: 10,
      borderLeft: 'none',
      borderRight: 'none',
      borderTop: 'none',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
          <span style={{
            fontWeight: 700,
            letterSpacing: '0.04em',
            fontSize: 15,
            color: 'var(--text-primary)',
          }}>AEROOPS</span>
          <span style={{
            fontSize: 10,
            color: 'var(--text-tertiary)',
            fontFamily: "'JetBrains Mono', monospace",
            letterSpacing: '0.12em',
          }}>COPILOT // v1.3</span>
        </div>
        <div style={{ width: 1, height: 16, background: 'var(--border-default)' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span className={`status-dot ${status === 'online' ? 'ok' : status === 'offline' ? 'warn' : 'caution'} pulse-indicator`} />
          <span className="mono" style={{ fontSize: 11, color: 'var(--text-secondary)' }}>
            {status === 'online' ? 'SYS ONLINE' : status === 'offline' ? 'SYS OFFLINE' : 'SYS INIT'}
          </span>
        </div>
        <div className="mono" style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
          {sourceCount} SOURCES
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <span className="mono" style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
          {utc} UTC
        </span>
        <button
          onClick={toggleTheme}
          aria-label="Toggle theme"
          className="btn-ghost"
          style={{
            fontSize: 11,
            padding: '4px 12px',
            fontFamily: "'JetBrains Mono', monospace",
            letterSpacing: '0.08em',
          }}
        >
          {theme === 'dark' ? 'DAY' : 'NIGHT'}
        </button>
      </div>
    </header>
  );
}

// ─── Empty State ────────────────────────────────────────────────
function EmptyState({ onExample }) {
  const examples = [
    { label: 'IFR fuel reserve requirements', type: 'SOP' },
    { label: 'Engine failure after V1', type: 'CHECKLIST' },
    { label: 'TCAS RA procedure', type: 'PROCEDURE' },
    { label: 'Wind shear escape maneuver', type: 'EMERGENCY' },
  ];
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100%',
      padding: 32,
      textAlign: 'center',
    }}>
      <div className="section-label" style={{ marginBottom: 20 }}>READY FOR INPUT</div>
      <h1 style={{
        fontSize: 24,
        fontWeight: 500,
        color: 'var(--text-primary)',
        marginBottom: 8,
        letterSpacing: '-0.02em',
      }}>
        Aviation Operations Assistant
      </h1>
      <p style={{
        fontSize: 13,
        color: 'var(--text-secondary)',
        maxWidth: 520,
        lineHeight: 1.6,
        marginBottom: 32,
      }}>
        Query standard operating procedures, submit incident reports for structured analysis,
        or upload crew schedules for fatigue risk assessment. Input routing is automatic.
      </p>
      <div style={{ display: 'grid', gap: 8, maxWidth: 480, width: '100%' }}>
        {examples.map(ex => (
          <button
            key={ex.label}
            onClick={() => onExample(ex.label)}
            className="glass-panel"
            style={{
              color: 'var(--text-primary)',
              padding: '14px 18px',
              textAlign: 'left',
              cursor: 'pointer',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              fontSize: 13,
              transition: 'all 160ms ease',
              border: '1px solid var(--border-default)',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.borderColor = 'var(--border-strong)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.borderColor = 'var(--border-default)';
            }}
          >
            <span>{ex.label}</span>
            <span className="mono" style={{ fontSize: 10, color: 'var(--text-tertiary)', letterSpacing: '0.1em' }}>
              {ex.type}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

// ─── Input Bar (glass) ───────────────────────────────────────────
function InputBar({ input, setInput, onSend, onFile, loading, fileName, onClearFile }) {
  const fileRef = useRef(null);
  const textRef = useRef(null);

  useEffect(() => {
    if (textRef.current) {
      textRef.current.style.height = 'auto';
      textRef.current.style.height = Math.min(textRef.current.scrollHeight, 120) + 'px';
    }
  }, [input]);

  return (
    <div className="glass-strong" style={{
      padding: '16px 20px',
      flexShrink: 0,
      borderLeft: 'none',
      borderRight: 'none',
      borderBottom: 'none',
    }}>
      <div style={{ maxWidth: 960, margin: '0 auto' }}>
        <div className="input-base" style={{
          padding: '10px 12px',
          display: 'flex',
          gap: 10,
          alignItems: 'flex-end',
        }}>
          <input
            ref={fileRef}
            type="file"
            accept=".pdf,.csv,.txt"
            onChange={onFile}
            style={{ display: 'none' }}
          />
          {fileName ? (
            <button
              onClick={onClearFile}
              className="mono"
              style={{
                background: 'var(--accent-glow)',
                border: '1px solid var(--border-focus)',
                color: 'var(--accent-blue)',
                padding: '6px 10px',
                cursor: 'pointer',
                fontSize: 10,
                letterSpacing: '0.04em',
                flexShrink: 0,
                borderRadius: 4,
                display: 'flex',
                alignItems: 'center',
                gap: 6,
              }}
              title="Click to remove"
            >
              <span>{fileName.slice(0, 20)}{fileName.length > 20 ? '…' : ''}</span>
              <span style={{ color: 'var(--text-tertiary)' }}>×</span>
            </button>
          ) : (
            <button
              onClick={() => fileRef.current?.click()}
              aria-label="Attach file"
              className="btn-ghost mono"
              style={{
                padding: '6px 10px',
                fontSize: 10,
                letterSpacing: '0.08em',
                flexShrink: 0,
              }}
            >
              + FILE
            </button>
          )}
          <textarea
            ref={textRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                onSend();
              }
            }}
            rows={1}
            placeholder="Ask about SOPs, or attach a PDF/CSV/TXT…"
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: 'var(--text-primary)',
              fontSize: 14,
              fontFamily: 'inherit',
              resize: 'none',
              padding: '4px 0',
              lineHeight: 1.5,
            }}
          />
          <button
            onClick={onSend}
            disabled={loading}
            className="btn-primary mono"
            style={{
              padding: '7px 18px',
              fontSize: 11,
              letterSpacing: '0.12em',
              flexShrink: 0,
            }}
          >
            {loading ? 'PROCESSING' : 'TRANSMIT'}
          </button>
        </div>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginTop: 6,
          fontSize: 10,
          color: 'var(--text-tertiary)',
          fontFamily: "'JetBrains Mono', monospace",
          letterSpacing: '0.08em',
        }}>
          <span>INTENT: AUTO-DETECTED</span>
          <span>⏎ SEND  //  ⇧⏎ NEWLINE</span>
        </div>
      </div>
    </div>
  );
}

// ─── Main Console ────────────────────────────────────────────────
export default function UnifiedConsole({ theme, toggleTheme }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('checking');
  const [sourceCount, setSourceCount] = useState(0);
  const [pendingFile, setPendingFile] = useState(null);
  const endRef = useRef(null);

  useEffect(() => {
    healthCheck().then(() => setStatus('online')).catch(() => setStatus('offline'));
    getSources().then(r => setSourceCount(r.data.sources?.length || 0)).catch(() => {});
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const addMsg = (role, content, data) =>
    setMessages(prev => [...prev, { role, content, data, ts: new Date() }]);

  const isChecklistQuery = (q) =>
    /checklist|procedure|steps|how to|what steps|emergency procedure|what should|what do i do/i.test(q);

  const handleSend = async () => {
    const q = input.trim();

    if (pendingFile) {
      addMsg('user', `[FILE] ${pendingFile.name}${q ? ` — ${q}` : ''}`);
      setInput('');
      setLoading(true);
      try {
        const isTextDoc = /\.(pdf|txt)$/i.test(pendingFile.name);
        const res = isTextDoc ? await uploadIncident(pendingFile) : await uploadSchedule(pendingFile);
        addMsg('assistant', null, res.data);
      } catch (e) {
        addMsg('assistant', `ERROR: ${e.response?.data?.detail || e.message}`);
      }
      setPendingFile(null);
      setLoading(false);
      return;
    }

    if (!q || loading) return;
    addMsg('user', q);
    setInput('');
    setLoading(true);
    try {
      const res = isChecklistQuery(q) ? await queryChecklist(q) : await sendQuery(q);
      addMsg('assistant', null, res.data);
    } catch (e) {
      addMsg('assistant', `ERROR: ${e.response?.data?.detail || e.message}`);
    }
    setLoading(false);
  };

  const handleFile = (e) => {
    const file = e.target.files?.[0];
    if (file) setPendingFile(file);
    e.target.value = '';
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      background: 'var(--bg-base)',
      color: 'var(--text-primary)',
    }}>
      <StatusBar theme={theme} toggleTheme={toggleTheme} status={status} sourceCount={sourceCount} />

      <main style={{
        flex: 1,
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
      }}>
        {messages.length === 0 ? (
          <EmptyState onExample={setInput} />
        ) : (
          <div style={{
            maxWidth: 960,
            width: '100%',
            margin: '0 auto',
            padding: '24px 20px',
          }}>
            {messages.map((m, i) => (
              <MessageBlock key={i} msg={m} />
            ))}
            {loading && <LoadingBlock />}
            <div ref={endRef} />
          </div>
        )}
      </main>

      <InputBar
        input={input}
        setInput={setInput}
        onSend={handleSend}
        onFile={handleFile}
        loading={loading}
        fileName={pendingFile?.name}
        onClearFile={() => setPendingFile(null)}
      />
    </div>
  );
}

// ─── Message Block ───────────────────────────────────────────────
function MessageBlock({ msg }) {
  const isUser = msg.role === 'user';
  const ts = msg.ts ? msg.ts.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' }) : '';

  if (isUser) {
    return (
      <div className="fade-up" style={{ marginBottom: 24 }}>
        <div className="section-label" style={{ marginBottom: 4 }}>
          USER · {ts}
        </div>
        <div style={{
          fontSize: 14,
          color: 'var(--text-primary)',
          paddingLeft: 12,
          borderLeft: '2px solid var(--accent-blue)',
        }}>
          {msg.content}
        </div>
      </div>
    );
  }

  return (
    <div className="fade-up" style={{ marginBottom: 28 }}>
      <div className="section-label" style={{ marginBottom: 8 }}>
        SYSTEM · {ts}
      </div>
      {msg.content ? (
        <div style={{
          fontSize: 13,
          color: 'var(--text-primary)',
          paddingLeft: 12,
          borderLeft: '2px solid var(--status-warn)',
        }}>
          {msg.content}
        </div>
      ) : (
        <div style={{ paddingLeft: 12, borderLeft: '2px solid var(--accent-cyan)' }}>
          <ResponseRenderer data={msg.data} />
        </div>
      )}
    </div>
  );
}

function LoadingBlock() {
  return (
    <div style={{ marginBottom: 24, paddingLeft: 12, borderLeft: '2px solid var(--accent-cyan)' }}>
      <div className="section-label" style={{ marginBottom: 8 }}>
        SYSTEM · PROCESSING
      </div>
      <div style={{ display: 'flex', gap: 4, padding: '4px 0' }}>
        <span className="loading-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-cyan)' }} />
        <span className="loading-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-cyan)' }} />
        <span className="loading-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-cyan)' }} />
      </div>
    </div>
  );
}
