import React, { useState } from 'react'
import { Brain, BookOpen, FlaskConical, BarChart3 } from 'lucide-react'
import Playground from './components/Playground'
import Architecture from './components/Architecture'
import Documentation from './components/Documentation'
import Statistics from './components/Statistics'

function App() {
  const [activeTab, setActiveTab] = useState('playground')

  const tabs = [
    { id: 'playground', name: 'Playground', icon: FlaskConical },
    { id: 'architecture', name: 'Architecture', icon: Brain },
    { id: 'documentation', name: 'Documentation', icon: BookOpen },
    { id: 'statistics', name: 'Statistics', icon: BarChart3 },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-700 bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                  Self-Healing RAG System
                </h1>
                <p className="text-sm text-gray-400">
                  Advanced Retrieval-Augmented Generation with Closed-Loop Agents
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2 text-sm">
              <div className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full border border-green-500/30">
                ● System Online
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="border-b border-gray-700 bg-gray-900/30">
        <div className="container mx-auto px-4">
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    flex items-center space-x-2 px-6 py-3 font-medium transition-all
                    ${activeTab === tab.id
                      ? 'border-b-2 border-blue-500 text-blue-400 bg-blue-500/10'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className={`fade-in ${activeTab === 'playground' ? '' : 'hidden'}`}>
          <Playground />
        </div>
        <div className={`fade-in ${activeTab === 'architecture' ? '' : 'hidden'}`}>
          <Architecture />
        </div>
        <div className={`fade-in ${activeTab === 'documentation' ? '' : 'hidden'}`}>
          <Documentation />
        </div>
        <div className={`fade-in ${activeTab === 'statistics' ? '' : 'hidden'}`}>
          <Statistics />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-700 bg-gray-900/50 mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-center text-sm text-gray-400">
            <p className="flex items-center gap-2">
              Built by{' '}
              <a 
                href="https://aianytime.net" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 transition-colors font-semibold"
              >
                AI Anytime
              </a>
              {' '}with ❤️
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
