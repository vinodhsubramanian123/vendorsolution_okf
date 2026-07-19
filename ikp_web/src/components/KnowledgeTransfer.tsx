import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { BookOpen } from 'lucide-react';

export function KnowledgeTransfer() {
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await fetch('/KT_WALKTHROUGH.md');
        if (!response.ok) {
          throw new Error('Failed to load KT documentation');
        }
        const text = await response.text();
        setContent(text);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  return (
    <div className="panel" style={{ height: 'calc(100vh - 40px)', overflowY: 'auto' }}>
      <div className="panel-header">
        <BookOpen className="icon" />
        <h2>Knowledge Transfer (KT) Guide</h2>
      </div>
      <div className="panel-content markdown-body">
        {loading && <div className="loading">Loading documentation...</div>}
        {error && <div className="error-message">Error: {error}</div>}
        {!loading && !error && (
          <ReactMarkdown
            components={{
              code({ node, inline, className, children, ...props }: any) {
                const match = /language-(\w+)/.exec(className || '');
                return !inline ? (
                  <div className="code-block-wrapper">
                    <pre className={className}>
                      <code className={className} {...props}>
                        {children}
                      </code>
                    </pre>
                  </div>
                ) : (
                  <code className="inline-code" {...props}>
                    {children}
                  </code>
                );
              }
            }}
          >
            {content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}
