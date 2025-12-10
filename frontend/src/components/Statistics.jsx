import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart3, TrendingUp, Clock, Brain, RefreshCw, AlertCircle } from 'lucide-react'

function Statistics() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchStats = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.get('/api/statistics')
      setStats(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch statistics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 text-blue-400 animate-spin mx-auto mb-2" />
          <p className="text-gray-400">Loading statistics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6">
        <div className="flex items-center space-x-3">
          <AlertCircle className="w-6 h-6 text-red-400" />
          <div>
            <h3 className="font-semibold text-red-400">Error Loading Statistics</h3>
            <p className="text-sm text-gray-300 mt-1">{error}</p>
            <button
              onClick={fetchStats}
              className="mt-3 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 
                       rounded-lg text-sm transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!stats) {
    return null
  }

  const { system_stats, learning_stats } = stats

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2 flex items-center">
              <BarChart3 className="w-6 h-6 mr-2 text-blue-400" />
              System Statistics
            </h1>
            <p className="text-gray-400">
              Real-time performance metrics and usage analytics
            </p>
          </div>
          <button
            onClick={fetchStats}
            className="px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 
                     rounded-lg transition-colors flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Total Queries</span>
            <TrendingUp className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-3xl font-bold text-blue-400">
            {system_stats.total_queries}
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Avg Processing Time</span>
            <Clock className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-3xl font-bold text-purple-400">
            {system_stats.avg_processing_time}
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Learned Examples</span>
            <Brain className="w-4 h-4 text-green-400" />
          </div>
          <p className="text-3xl font-bold text-green-400">
            {system_stats.learning_examples}
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-400 text-sm">Avg Feedback Score</span>
            <BarChart3 className="w-4 h-4 text-yellow-400" />
          </div>
          <p className="text-3xl font-bold text-yellow-400">
            {learning_stats.avg_feedback_score}/1.0
          </p>
        </div>
      </div>

      {/* Technique Usage Rates */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <h2 className="text-xl font-semibold mb-4">Technique Usage Rates</h2>
        
        <div className="space-y-4">
          {[
            { name: 'HyDE', rate: system_stats.hyde_rate, color: 'blue' },
            { name: 'Query Decomposition', rate: system_stats.decomposition_rate, color: 'purple' },
            { name: 'CRAG Activation', rate: system_stats.crag_rate, color: 'green' },
            { name: 'Cross-Encoder Reranking', rate: system_stats.reranking_rate, color: 'yellow' },
            { name: 'Dynamic Learning', rate: system_stats.learning_rate, color: 'pink' }
          ].map(({ name, rate, color }) => {
            const percentage = parseFloat(rate)
            
            return (
              <div key={name}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">{name}</span>
                  <span className={`text-sm font-semibold text-${color}-400`}>{rate}</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                  <div
                    className={`bg-${color}-500 h-2 rounded-full transition-all duration-500`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            )
          })}
        </div>

        <div className="mt-6 pt-6 border-t border-gray-700">
          <p className="text-xs text-gray-400">
            These metrics show how often each technique is triggered during query processing. 
            Higher rates indicate more complex queries requiring advanced techniques.
          </p>
        </div>
      </div>

      {/* Learning System Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <h2 className="text-xl font-semibold mb-4">Learning System</h2>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b border-gray-700">
              <span className="text-gray-400">Total Examples</span>
              <span className="font-semibold text-green-400">
                {learning_stats.total_examples}
              </span>
            </div>
            
            <div className="flex items-center justify-between py-3 border-b border-gray-700">
              <span className="text-gray-400">Avg Feedback Score</span>
              <span className="font-semibold text-yellow-400">
                {learning_stats.avg_feedback_score}
              </span>
            </div>
            
            {learning_stats.oldest_example && (
              <div className="flex items-center justify-between py-3 border-b border-gray-700">
                <span className="text-gray-400">Oldest Example</span>
                <span className="font-mono text-sm text-gray-300">
                  {new Date(learning_stats.oldest_example).toLocaleDateString()}
                </span>
              </div>
            )}
            
            {learning_stats.newest_example && (
              <div className="flex items-center justify-between py-3">
                <span className="text-gray-400">Newest Example</span>
                <span className="font-mono text-sm text-gray-300">
                  {new Date(learning_stats.newest_example).toLocaleDateString()}
                </span>
              </div>
            )}
          </div>

          {learning_stats.total_examples === 0 && (
            <div className="mt-4 p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
              <p className="text-sm text-blue-300">
                💡 No examples yet. Use the playground to test queries and give positive 
                feedback (👍) to start building the learning library!
              </p>
            </div>
          )}
        </div>

        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Example Queries</h2>
          
          {learning_stats.example_queries && learning_stats.example_queries.length > 0 ? (
            <div className="space-y-2">
              {learning_stats.example_queries.map((query, idx) => (
                <div
                  key={idx}
                  className="bg-gray-900 rounded-lg p-3 border border-gray-700 text-sm"
                >
                  <span className="text-gray-400 font-mono">#{idx + 1}</span>
                  <p className="text-gray-300 mt-1">{query}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Brain className="w-12 h-12 text-gray-600 mx-auto mb-3" />
              <p className="text-gray-400">No example queries yet</p>
            </div>
          )}
        </div>
      </div>

      {/* System Health */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <h2 className="text-xl font-semibold mb-4">System Health</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-green-900/20 rounded-lg p-4 border border-green-500/30">
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="font-semibold text-green-400">API Server</span>
            </div>
            <p className="text-sm text-gray-400">Online and responding</p>
          </div>

          <div className="bg-green-900/20 rounded-lg p-4 border border-green-500/30">
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="font-semibold text-green-400">RAG Components</span>
            </div>
            <p className="text-sm text-gray-400">All systems operational</p>
          </div>

          <div className="bg-green-900/20 rounded-lg p-4 border border-green-500/30">
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="font-semibold text-green-400">Vector Index</span>
            </div>
            <p className="text-sm text-gray-400">Documents loaded</p>
          </div>
        </div>
      </div>

      {/* Performance Insights */}
      <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg border border-blue-500/30 p-6">
        <h3 className="text-lg font-semibold mb-3">📊 Performance Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-blue-300 font-medium mb-1">Query Complexity</p>
            <p className="text-gray-400">
              {system_stats.decomposition_rate !== '0.0%' 
                ? `About ${system_stats.decomposition_rate} of queries require decomposition, indicating moderate complexity.`
                : 'Most queries are simple and don\'t require decomposition.'}
            </p>
          </div>
          <div>
            <p className="text-purple-300 font-medium mb-1">Retrieval Quality</p>
            <p className="text-gray-400">
              {system_stats.crag_rate !== '0.0%'
                ? `CRAG filters ${system_stats.crag_rate} of results, showing active quality control.`
                : 'Retrieval quality is consistently high with minimal filtering needed.'}
            </p>
          </div>
          <div>
            <p className="text-green-300 font-medium mb-1">Learning Progress</p>
            <p className="text-gray-400">
              {learning_stats.total_examples > 0
                ? `System has learned from ${learning_stats.total_examples} successful interactions.`
                : 'Learning system is ready to collect examples from user feedback.'}
            </p>
          </div>
          <div>
            <p className="text-yellow-300 font-medium mb-1">Optimization Status</p>
            <p className="text-gray-400">
              Average processing time of {system_stats.avg_processing_time} shows 
              {parseFloat(system_stats.avg_processing_time) < 3 ? ' excellent' : ' good'} performance.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Statistics
