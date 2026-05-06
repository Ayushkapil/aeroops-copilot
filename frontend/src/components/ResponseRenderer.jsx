import React from 'react';

// ─── Shared sub-components ───────────────────────────────────────

const SectionLabel = ({ children, color = 'var(--text-tertiary)' }) => (
  <div className="section-label" style={{ color, marginBottom: 10 }}>{children}</div>
);

const ConfidenceMeter = ({ value }) => {
  if (value == null) return null;
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? 'var(--status-ok)'
    : pct >= 40 ? 'var(--status-caution)'
    : 'var(--status-warn)';
  return (
    <div className="confidence-meter">
      <span style={{ color: 'var(--text-tertiary)' }}>CONFIDENCE</span>
      <div className="confidence-bar">
        <div className="confidence-bar-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span style={{ color, fontWeight: 600 }}>{pct}%</span>
    </div>
  );
};

const CalloutBadge = ({ type }) => {
  if (!type) return null;
  const colors = {
    WARNING: { color: 'var(--status-warn)' },
    CAUTION: { color: 'var(--status-caution)' },
    NOTE: { color: 'var(--accent-blue)' },
  };
  const c = colors[type.toUpperCase()];
  if (!c) return null;
  return (
    <div className="mono" style={{
      fontSize: 10,
      fontWeight: 600,
      letterSpacing: '0.12em',
      color: c.color,
      marginBottom: 4,
    }}>
      ▲ {type.toUpperCase()}
    </div>
  );
};

const Citation = ({ source, section, page }) => (
  <div className="mono" style={{
    fontSize: 10,
    color: 'var(--text-tertiary)',
    marginTop: 6,
    letterSpacing: '0.04em',
  }}>
    REF · {source} · {section} · p.{page}
  </div>
);

const Panel = ({ children, accent }) => (
  <div className="glass-panel" style={{
    padding: '14px 16px',
    marginBottom: 10,
    borderLeft: accent ? `2px solid ${accent}` : undefined,
  }}>
    {children}
  </div>
);

// ─── Module A: Structured SOP Answer ─────────────────────────────
function StructuredAnswer({ data }) {
  const s = data.response?.structured;
  const confidence = data.response?.confidence;

  if (!s) {
    return (
      <div style={{ fontSize: 14, color: 'var(--text-primary)', lineHeight: 1.6 }}>
        {data.response?.answer || 'No response available.'}
      </div>
    );
  }

  const isChecklist = s.type === 'checklist';

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10, flexWrap: 'wrap', gap: 8 }}>
        <SectionLabel color="var(--accent-cyan)">
          {isChecklist ? 'PROCEDURE · CHECKLIST' : 'SOP QUERY · RESPONSE'}
        </SectionLabel>
        <ConfidenceMeter value={confidence} />
      </div>

      <div style={{
        fontSize: 15,
        color: 'var(--text-primary)',
        lineHeight: 1.6,
        marginBottom: 16,
        fontWeight: 500,
      }}>
        {s.summary}
      </div>

      {s.points?.length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <SectionLabel>{isChecklist ? 'STEPS' : 'DETAILS'}</SectionLabel>
          <div>
            {s.points.map((p, i) => (
              <Panel key={i} accent={p.callout ? 'var(--status-warn)' : null}>
                <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                  <div className="mono" style={{
                    fontSize: 11,
                    color: 'var(--text-tertiary)',
                    minWidth: 24,
                    paddingTop: 2,
                    fontWeight: 600,
                  }}>
                    {String(i + 1).padStart(2, '0')}
                  </div>
                  <div style={{ flex: 1 }}>
                    <CalloutBadge type={p.callout} />
                    <div style={{ fontSize: 14, color: 'var(--text-primary)', lineHeight: 1.5 }}>
                      {p.text}
                    </div>
                    {p.detail && (
                      <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4, lineHeight: 1.5 }}>
                        {p.detail}
                      </div>
                    )}
                    <Citation source={p.source_file} section={p.section} page={p.page} />
                  </div>
                </div>
              </Panel>
            ))}
          </div>
        </div>
      )}

      {s.additional_notes?.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <SectionLabel>REMARKS</SectionLabel>
          <div className="glass-panel" style={{ padding: '10px 14px' }}>
            {s.additional_notes.map((n, i) => (
              <div key={i} style={{
                fontSize: 12,
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                paddingLeft: 8,
                borderLeft: '1px solid var(--border-default)',
                marginBottom: i < s.additional_notes.length - 1 ? 6 : 0,
              }}>
                {n}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Module A: Checklist ─────────────────────────────────────────
function ChecklistAnswer({ data }) {
  const r = data.response || {};
  return (
    <div>
      <SectionLabel color="var(--accent-cyan)">PROCEDURE · CHECKLIST</SectionLabel>

      <div style={{
        fontSize: 17,
        color: 'var(--text-primary)',
        marginBottom: 6,
        fontWeight: 600,
        letterSpacing: '-0.01em',
      }}>
        {r.title}
      </div>

      {r.applicable_conditions && (
        <div style={{
          fontSize: 12,
          color: 'var(--text-secondary)',
          marginBottom: 16,
          fontStyle: 'italic',
        }}>
          Applies when: {r.applicable_conditions}
        </div>
      )}

      {r.steps?.length > 0 && (
        <div style={{ marginBottom: 12 }}>
          <SectionLabel>STEPS</SectionLabel>
          {r.steps.map((s, i) => (
            <Panel key={i} accent={s.callout ? 'var(--status-warn)' : null}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                <div className="mono" style={{
                  fontSize: 11,
                  color: 'var(--text-tertiary)',
                  minWidth: 24,
                  paddingTop: 2,
                  fontWeight: 600,
                }}>
                  {String(s.step_number).padStart(2, '0')}
                </div>
                <div style={{ flex: 1 }}>
                  <CalloutBadge type={s.callout} />
                  <div style={{ fontSize: 14, color: 'var(--text-primary)', lineHeight: 1.5, fontWeight: 500 }}>
                    {s.action}
                  </div>
                  {s.details && (
                    <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 4, lineHeight: 1.5 }}>
                      {s.details}
                    </div>
                  )}
                  <Citation source={s.source} section={s.section} page={s.page} />
                </div>
              </div>
            </Panel>
          ))}
        </div>
      )}

      {r.notes?.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <SectionLabel>NOTES</SectionLabel>
          <div className="glass-panel" style={{ padding: '10px 14px' }}>
            {r.notes.map((n, i) => (
              <div key={i} style={{
                fontSize: 12,
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                marginBottom: i < r.notes.length - 1 ? 6 : 0,
              }}>
                — {n}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Module B: Incident Analysis ─────────────────────────────────
function IncidentAnalysis({ data }) {
  const r = data.response || {};
  const sevColor = {
    serious: 'var(--status-warn)',
    moderate: 'var(--status-caution)',
    minor: 'var(--status-ok)',
  }[r.severity] || 'var(--text-secondary)';

  return (
    <div>
      <SectionLabel color="var(--status-caution)">INCIDENT · ANALYSIS</SectionLabel>

      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
        <div className="mono" style={{
          fontSize: 10,
          letterSpacing: '0.14em',
          color: sevColor,
          padding: '4px 8px',
          border: `1px solid ${sevColor}`,
          fontWeight: 600,
          borderRadius: 3,
        }}>
          {r.severity?.toUpperCase() || 'UNKNOWN'}
        </div>
        <div className="mono" style={{ fontSize: 11, color: 'var(--text-tertiary)' }}>
          PHASE: {r.phase_of_flight?.toUpperCase()}
        </div>
      </div>

      <div style={{ fontSize: 14, color: 'var(--text-primary)', lineHeight: 1.6, marginBottom: 16 }}>
        {r.summary}
      </div>

      {r.event_tags?.length > 0 && (
        <div style={{ marginBottom: 16 }}>
          <SectionLabel>EVENT CLASSIFICATION</SectionLabel>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {r.event_tags.map(t => (
              <span key={t} className="mono" style={{
                fontSize: 10,
                color: 'var(--text-secondary)',
                border: '1px solid var(--border-default)',
                padding: '3px 8px',
                letterSpacing: '0.06em',
                borderRadius: 3,
                background: 'var(--bg-elevated)',
              }}>
                {t.replace(/_/g, ' ').toUpperCase()}
              </span>
            ))}
          </div>
        </div>
      )}

      {r.timeline?.length > 0 && (
        <div style={{ marginBottom: 16 }}>
          <SectionLabel>EVENT TIMELINE</SectionLabel>
          <div style={{ borderLeft: '1px solid var(--border-default)', paddingLeft: 14 }}>
            {r.timeline.map((e, i) => (
              <div key={i} style={{ position: 'relative', paddingBottom: 10, marginBottom: 2 }}>
                <div style={{
                  position: 'absolute',
                  left: -17,
                  top: 5,
                  width: 6,
                  height: 6,
                  background: 'var(--accent-cyan)',
                  border: '1px solid var(--bg-base)',
                  borderRadius: '50%',
                }} />
                <div className="mono" style={{ fontSize: 11, color: 'var(--accent-cyan)', marginBottom: 2 }}>
                  {e.timestamp}
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-primary)', lineHeight: 1.5 }}>
                  {e.event}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 16, marginBottom: 16 }}>
        {r.contributing_factors?.length > 0 && (
          <div>
            <SectionLabel>CONTRIBUTING FACTORS</SectionLabel>
            <div className="glass-panel" style={{ padding: '10px 14px' }}>
              {r.contributing_factors.map((f, i) => (
                <div key={i} style={{ fontSize: 13, color: 'var(--text-primary)', padding: '4px 0', display: 'flex', gap: 8 }}>
                  <span className="mono" style={{ color: 'var(--text-tertiary)', fontSize: 11 }}>
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <span>{f}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        {r.recommendations?.length > 0 && (
          <div>
            <SectionLabel>RECOMMENDATIONS</SectionLabel>
            <div className="glass-panel" style={{ padding: '10px 14px' }}>
              {r.recommendations.map((f, i) => (
                <div key={i} style={{ fontSize: 13, color: 'var(--text-primary)', padding: '4px 0', display: 'flex', gap: 8 }}>
                  <span className="mono" style={{ color: 'var(--status-ok)', fontSize: 11 }}>
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <span>{f}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {data.chained_results?.sop_enrichment?.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <SectionLabel color="var(--accent-blue)">RELATED SOPs · AUTO-RETRIEVED</SectionLabel>
          {data.chained_results.sop_enrichment.map((s, i) => (
            <Panel key={i} accent="var(--accent-blue)">
              <div className="mono" style={{ fontSize: 10, color: 'var(--accent-blue)', marginBottom: 6, letterSpacing: '0.06em' }}>
                QUERY · {s.query}
              </div>
              <div style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {s.answer}
              </div>
            </Panel>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Module C: Fatigue Assessment ────────────────────────────────
function FatigueAssessment({ data }) {
  const r = data.response || {};
  const riskColor = {
    high: 'var(--status-warn)',
    moderate: 'var(--status-caution)',
    low: 'var(--status-ok)',
  }[r.overall_risk] || 'var(--text-secondary)';

  return (
    <div>
      <SectionLabel color="var(--accent-cyan)">FATIGUE · RISK ASSESSMENT</SectionLabel>

      <div className="glass-panel" style={{
        display: 'flex',
        gap: 24,
        alignItems: 'center',
        padding: '20px 24px',
        marginBottom: 16,
      }}>
        <div>
          <div className="mono" style={{ fontSize: 10, color: 'var(--text-tertiary)', letterSpacing: '0.12em', marginBottom: 4 }}>
            MAX SCORE
          </div>
          <div className="mono" style={{ fontSize: 44, fontWeight: 600, color: riskColor, lineHeight: 1, textShadow: `0 0 20px ${riskColor}40` }}>
            {r.max_score}
          </div>
          <div className="mono" style={{ fontSize: 10, color: 'var(--text-tertiary)' }}>
            / 100
          </div>
        </div>
        <div style={{ flex: 1 }}>
          <div className="mono" style={{
            fontSize: 14,
            fontWeight: 600,
            color: riskColor,
            letterSpacing: '0.1em',
            marginBottom: 8,
          }}>
            {r.overall_risk?.toUpperCase()} RISK
          </div>
          <div className="data-row">
            <span className="label">Average</span>
            <span className="value">{r.average_score}</span>
          </div>
          <div className="data-row">
            <span className="label">Entries</span>
            <span className="value">{r.total_entries}</span>
          </div>
          {r.llm_reasoning?.peak_risk_window && (
            <div className="data-row">
              <span className="label">Peak Window</span>
              <span className="value">{r.llm_reasoning.peak_risk_window}</span>
            </div>
          )}
        </div>
      </div>

      {r.entries?.length > 0 && (
        <div style={{ marginBottom: 16 }}>
          <SectionLabel>PER-ENTRY RISK DISTRIBUTION</SectionLabel>
          <div className="glass-panel" style={{ padding: '14px 18px' }}>
            {r.entries.map((e, i) => {
              const barColor = e.risk_level === 'high' ? 'var(--status-warn)'
                : e.risk_level === 'moderate' ? 'var(--status-caution)'
                : 'var(--status-ok)';
              return (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '4px 0' }}>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--text-tertiary)', width: 44, letterSpacing: '0.04em' }}>
                    DAY {String(i + 1).padStart(2, '0')}
                  </span>
                  <div style={{
                    flex: 1,
                    background: 'var(--bg-input)',
                    height: 6,
                    border: '1px solid var(--border-default)',
                    borderRadius: 3,
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      height: '100%',
                      background: barColor,
                      width: `${e.score}%`,
                      transition: 'width 400ms ease',
                      boxShadow: `0 0 8px ${barColor}80`,
                    }} />
                  </div>
                  <span className="mono" style={{ fontSize: 11, color: 'var(--text-primary)', width: 32, textAlign: 'right' }}>
                    {String(e.score).padStart(3, ' ')}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {r.llm_reasoning?.reasoning && (
        <div style={{ marginBottom: 16 }}>
          <SectionLabel>ANALYSIS</SectionLabel>
          <div style={{ fontSize: 13, color: 'var(--text-primary)', lineHeight: 1.6, paddingLeft: 12, borderLeft: '1px solid var(--border-default)' }}>
            {r.llm_reasoning.reasoning}
          </div>
        </div>
      )}

      {r.llm_reasoning?.mitigations?.length > 0 && (
        <div style={{ marginBottom: 16 }}>
          <SectionLabel color="var(--status-ok)">MITIGATIONS</SectionLabel>
          <div className="glass-panel" style={{ padding: '10px 14px' }}>
            {r.llm_reasoning.mitigations.map((m, i) => (
              <div key={i} style={{ fontSize: 13, color: 'var(--text-primary)', padding: '4px 0', display: 'flex', gap: 8 }}>
                <span className="mono" style={{ color: 'var(--status-ok)', fontSize: 11 }}>
                  {String(i + 1).padStart(2, '0')}
                </span>
                <span>{m}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {r.llm_reasoning?.augmentation_needed && (
        <div className="glass-panel" style={{
          padding: '12px 16px',
          borderLeft: '3px solid var(--status-warn)',
          marginBottom: 16,
        }}>
          <CalloutBadge type="WARNING" />
          <div style={{ fontSize: 13, color: 'var(--text-primary)' }}>
            Crew augmentation recommended for this schedule
          </div>
        </div>
      )}

      {data.chained_results?.regulation_enrichment?.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <SectionLabel color="var(--status-warn)">APPLICABLE REGULATIONS · AUTO-RETRIEVED</SectionLabel>
          {data.chained_results.regulation_enrichment.map((s, i) => (
            <Panel key={i} accent="var(--status-warn)">
              <div className="mono" style={{ fontSize: 10, color: 'var(--status-warn)', marginBottom: 6, letterSpacing: '0.06em' }}>
                QUERY · {s.query}
              </div>
              <div style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {s.answer}
              </div>
            </Panel>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ResponseRenderer({ data }) {
  if (!data) return null;
  if (data.intent === 'checklist_query') return <ChecklistAnswer data={data} />;
  if (data.module === 'B') return <IncidentAnalysis data={data} />;
  if (data.module === 'C') return <FatigueAssessment data={data} />;
  return <StructuredAnswer data={data} />;
}
