import React, { useState } from 'react'
import axios from 'axios'
import {
  Send,
  ThumbsUp,
  ThumbsDown,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Clock,
  FileText,
  Layers
} from 'lucide-react'

function Playground() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // Configuration toggles
  const [config, setConfig] = useState({
    enable_hyde: true,
    enable_decomposition: true,
    enable_crag: true,
    enable_reranking: true,
    enable_learning: true
  })

  const handleQuery = async () => {
    if (!query.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/query', {
        query: query.trim(),
        ...config
      })
      
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to process query')
    } finally {
      setLoading(false)
    }
  }

  const handleFeedback = async (isPositive) => {
    if (!result) return

    try {
      await axios.post('/api/feedback', {
        query: result.query,
        answer: result.answer,
        is_positive: isPositive
      })
      
      alert(isPositive ? '✓ Feedback recorded! System will learn from this.' : 'Feedback recorded.')
    } catch (err) {
      alert('Failed to submit feedback')
    }
  }

  const toggleConfig = (key) => {
    setConfig(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const sampleQueries = [
    "What is RAG and how does it work?",
    "Compare HyDE and standard retrieval methods",
    "How does CRAG improve retrieval quality?",
    "Explain cross-encoder reranking",
    "What are self-healing RAG systems?"
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Query Panel */}
      <div className="lg:col-span-2 space-y-6">
        {/* Query Input */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Send className="w-5 h-5 mr-2 text-blue-400" />
            Query Input
          </h2>
          
          <div className="space-y-4">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your question about RAG systems..."
              className="w-full h-32 px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg 
                       text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 
                       focus:ring-blue-500 focus:border-transparent resize-none"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                  handleQuery()
                }
              }}
            />
            
            <div className="flex items-center justify-between">
              <button
                onClick={handleQuery}
                disabled={loading || !query.trim()}
                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white 
                         rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 
                         disabled:opacity-50 disabled:cursor-not-allowed flex items-center 
                         space-x-2 transition-all"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span>Submit Query</span>
                  </>
                )}
              </button>
              
              <span className="text-sm text-gray-400">
                Ctrl+Enter to submit
              </span>
            </div>
          </div>

          {/* Sample Queries */}
          <div className="mt-4 pt-4 border-t border-gray-700">
            <p className="text-sm text-gray-400 mb-2">Sample queries:</p>
            <div className="flex flex-wrap gap-2">
              {sampleQueries.map((sq, idx) => (
                <button
                  key={idx}
                  onClick={() => setQuery(sq)}
                  className="text-xs px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded-full 
                           text-gray-300 transition-colors"
                >
                  {sq}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Result Display */}
        {error && (
          <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6">
            <div className="flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-red-400 mt-0.5" />
              <div>
                <h3 className="font-semibold text-red-400 mb-1">Error</h3>
                <p className="text-sm text-gray-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result && (
          <div className="space-y-4">
            {/* Answer */}
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold flex items-center">
                  <CheckCircle2 className="w-5 h-5 mr-2 text-green-400" />
                  Answer
                </h2>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleFeedback(true)}
                    className="p-2 hover:bg-green-500/20 rounded-lg transition-colors group"
                    title="Good answer"
                  >
                    <ThumbsUp className="w-5 h-5 text-gray-400 group-hover:text-green-400" />
                  </button>
                  <button
                    onClick={() => handleFeedback(false)}
                    className="p-2 hover:bg-red-500/20 rounded-lg transition-colors group"
                    title="Bad answer"
                  >
                    <ThumbsDown className="w-5 h-5 text-gray-400 group-hover:text-red-400" />
                  </button>
                </div>
              </div>
              
              <div className="prose prose-invert max-w-none">
                <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
                  {result.answer}
                </p>
              </div>
            </div>

            {/* Metadata */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                <div className="flex items-center space-x-2 text-blue-400 mb-2">
                  <Clock className="w-4 h-4" />
                  <span className="font-semibold text-sm">Processing Time</span>
                </div>
                <p className="text-2xl font-bold">{result.processing_time}s</p>
              </div>
              
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                <div className="flex items-center space-x-2 text-purple-400 mb-2">
                  <FileText className="w-4 h-4" />
                  <span className="font-semibold text-sm">Documents</span>
                </div>
                <p className="text-2xl font-bold">
                  {result.documents_retrieved} → {result.final_documents}
                </p>
              </div>
              
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                <div className="flex items-center space-x-2 text-green-400 mb-2">
                  <Layers className="w-4 h-4" />
                  <span className="font-semibold text-sm">Techniques</span>
                </div>
                <p className="text-sm font-medium">{result.techniques_used.length} active</p>
              </div>
            </div>

            {/* Techniques Used */}
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
              <h3 className="font-semibold mb-3">Techniques Applied</h3>
              <div className="flex flex-wrap gap-2">
                {result.techniques_used.map((tech, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-blue-500/20 text-blue-300 rounded-full 
                             text-sm border border-blue-500/30"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            {/* Retrieved Documents */}
            {result.document_contents && result.document_contents.length > 0 && (
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
                <h3 className="font-semibold mb-3">Top Retrieved Documents</h3>
                <div className="space-y-3">
                  {result.document_contents.map((doc, idx) => (
                    <div key={idx} className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="px-2 py-0.5 bg-gray-700 text-gray-300 rounded text-xs font-mono">
                          Doc {idx + 1}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">{doc}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Configuration Panel */}
      <div className="space-y-6">
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 sticky top-6">
          <h2 className="text-xl font-semibold mb-4">Configuration</h2>
          
          <div className="space-y-4">
            {[
              { key: 'enable_hyde', label: 'HyDE', desc: 'Hypothetical Document Embeddings' },
              { key: 'enable_decomposition', label: 'Query Decomposition', desc: 'Break complex queries' },
              { key: 'enable_crag', label: 'CRAG', desc: 'Corrective RAG validation' },
              { key: 'enable_reranking', label: 'Cross-Encoder Reranking', desc: 'Precision document scoring' },
              { key: 'enable_learning', label: 'Dynamic Learning', desc: 'Use past successful examples' }
            ].map(({ key, label, desc }) => (
              <div key={key} className="flex items-start space-x-3">
                <button
                  onClick={() => toggleConfig(key)}
                  className={`
                    mt-0.5 w-11 h-6 rounded-full transition-colors relative
                    ${config[key] ? 'bg-blue-500' : 'bg-gray-600'}
                  `}
                >
                  <div
                    className={`
                      absolute top-1 w-4 h-4 bg-white rounded-full transition-transform
                      ${config[key] ? 'left-6' : 'left-1'}
                    `}
                  />
                </button>
                <div className="flex-1">
                  <p className="font-medium text-sm">{label}</p>
                  <p className="text-xs text-gray-400">{desc}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 pt-6 border-t border-gray-700">
            <p className="text-xs text-gray-400 leading-relaxed">
              Toggle techniques to see how they affect retrieval quality and processing time.
              All techniques are designed to work together in a self-healing pipeline.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Playground
