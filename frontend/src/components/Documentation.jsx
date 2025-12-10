import React from 'react'
import { BookOpen, Code2, Lightbulb, Zap, Shield, TrendingUp } from 'lucide-react'

function Documentation() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <h1 className="text-2xl font-bold mb-2 flex items-center">
          <BookOpen className="w-6 h-6 mr-2 text-blue-400" />
          Technical Documentation
        </h1>
        <p className="text-gray-400">
          Comprehensive guide to self-healing RAG systems and advanced retrieval techniques
        </p>
      </div>

      {/* Table of Contents */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[
          { icon: Zap, title: 'HyDE', color: 'blue' },
          { icon: Code2, title: 'Query Decomposition', color: 'purple' },
          { icon: Shield, title: 'CRAG', color: 'green' },
          { icon: TrendingUp, title: 'Cross-Encoder', color: 'yellow' },
          { icon: Lightbulb, title: 'Dynamic Learning', color: 'pink' },
          { icon: BookOpen, title: 'DSPy', color: 'indigo' }
        ].map(({ icon: Icon, title, color }) => (
          <a
            key={title}
            href={`#${title.toLowerCase().replace(/\s+/g, '-')}`}
            className={`
              bg-gray-800 border border-gray-700 rounded-lg p-4 hover:border-${color}-500/50 
              transition-all group cursor-pointer
            `}
          >
            <Icon className={`w-5 h-5 mb-2 text-${color}-400 group-hover:scale-110 transition-transform`} />
            <h3 className="font-semibold">{title}</h3>
          </a>
        ))}
      </div>

      {/* HyDE Section */}
      <div id="hyde" className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Zap className="w-6 h-6 text-blue-400" />
          <h2 className="text-xl font-bold">HyDE: Hypothetical Document Embeddings</h2>
        </div>
        
        <div className="space-y-4 text-gray-300">
          <p className="leading-relaxed">
            Traditional vector search suffers from a <strong className="text-blue-400">modality mismatch</strong>: 
            short queries are used to match long documents. HyDE solves this by generating a hypothetical 
            document that would answer the query, then searching for real documents similar to this hypothetical one.
          </p>

          <div className="bg-gray-900 rounded-lg p-4 border-l-4 border-blue-500">
            <p className="text-sm font-mono text-blue-300 mb-2">Example:</p>
            <p className="text-sm mb-2">
              <span className="text-gray-400">Query:</span> "How does CRAG work?"
            </p>
            <p className="text-sm mb-2">
              <span className="text-gray-400">HyDE Generated:</span> "CRAG (Corrective RAG) operates by evaluating 
              the relevance of retrieved documents using an LLM grader. It assigns scores to each document..."
            </p>
            <p className="text-sm">
              <span className="text-gray-400">Result:</span> Vector search uses the generated text instead of 
              the original query, improving recall.
            </p>
          </div>

          <div className="bg-blue-900/20 rounded-lg p-4">
            <h4 className="font-semibold text-blue-300 mb-2">Key Benefits</h4>
            <ul className="space-y-1 text-sm list-disc list-inside">
              <li>Bridges the semantic gap between queries and documents</li>
              <li>Improves recall quality by 15-30% in most benchmarks</li>
              <li>Works with any embedding model without retraining</li>
              <li>Particularly effective for technical and domain-specific queries</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Query Decomposition */}
      <div id="query-decomposition" className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Code2 className="w-6 h-6 text-purple-400" />
          <h2 className="text-xl font-bold">Query Decomposition</h2>
        </div>
        
        <div className="space-y-4 text-gray-300">
          <p className="leading-relaxed">
            Complex queries that compare multiple entities or require information from disparate sources 
            often fail with standard retrieval. Query decomposition breaks these into <strong className="text-purple-400">
            atomic sub-queries</strong> that can be independently answered and then synthesized.
          </p>

          <div className="bg-gray-900 rounded-lg p-4 border-l-4 border-purple-500">
            <p className="text-sm font-mono text-purple-300 mb-2">Example:</p>
            <p className="text-sm mb-3">
              <span className="text-gray-400">Complex Query:</span> "Which performs better on coding tasks, 
              Llama-3 or GPT-4?"
            </p>
            <p className="text-sm mb-1">
              <span className="text-gray-400">Sub-Query 1:</span> "Llama-3 coding capability benchmarks"
            </p>
            <p className="text-sm">
              <span className="text-gray-400">Sub-Query 2:</span> "GPT-4 coding task performance"
            </p>
          </div>

          <div className="bg-purple-900/20 rounded-lg p-4">
            <h4 className="font-semibold text-purple-300 mb-2">When to Use</h4>
            <ul className="space-y-1 text-sm list-disc list-inside">
              <li>Questions with "and", "or", "versus", "compare"</li>
              <li>Multi-part questions requiring different information sources</li>
              <li>Queries that combine multiple concepts or entities</li>
            </ul>
          </div>
        </div>
      </div>

      {/* CRAG Section */}
      <div id="crag" className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Shield className="w-6 h-6 text-green-400" />
          <h2 className="text-xl font-bold">CRAG: Corrective RAG</h2>
        </div>
        
        <div className="space-y-4 text-gray-300">
          <p className="leading-relaxed">
            Standard RAG is fragile because it blindly trusts retrieved documents. CRAG adds a 
            <strong className="text-green-400"> self-correction layer</strong> that grades document 
            relevance and triggers fallback strategies when quality is low.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-green-900/20 rounded-lg p-4 border border-green-500/30">
              <h4 className="font-semibold text-green-400 mb-2">✓ Correct</h4>
              <p className="text-sm">Documents are relevant. Proceed to generation.</p>
            </div>
            <div className="bg-yellow-900/20 rounded-lg p-4 border border-yellow-500/30">
              <h4 className="font-semibold text-yellow-400 mb-2">⚡ Ambiguous</h4>
              <p className="text-sm">Mixed quality. Apply knowledge refinement.</p>
            </div>
            <div className="bg-red-900/20 rounded-lg p-4 border border-red-500/30">
              <h4 className="font-semibold text-red-400 mb-2">✗ Incorrect</h4>
              <p className="text-sm">Irrelevant docs. Trigger web search fallback.</p>
            </div>
          </div>

          <div className="bg-gray-900 rounded-lg p-4">
            <h4 className="font-semibold mb-2">Implementation with LangGraph</h4>
            <pre className="text-xs overflow-x-auto"><code>{`workflow = StateGraph(GraphState)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("web_search", web_search)
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {"web_search": "web_search", "generate": "generate"}
)`}</code></pre>
          </div>
        </div>
      </div>

      {/* Cross-Encoder Reranking */}
      <div id="cross-encoder" className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="w-6 h-6 text-yellow-400" />
          <h2 className="text-xl font-bold">Cross-Encoder Reranking</h2>
        </div>
        
        <div className="space-y-4 text-gray-300">
          <p className="leading-relaxed">
            Bi-encoders are fast but sacrifice accuracy by encoding query and documents separately. 
            Cross-encoders achieve <strong className="text-yellow-400">higher precision</strong> by 
            processing query-document pairs together with full cross-attention.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-900 rounded-lg p-4">
              <h4 className="font-semibold text-blue-400 mb-2">Bi-Encoder</h4>
              <ul className="text-sm space-y-1">
                <li>• Separate encoding: Query → [768d], Doc → [768d]</li>
                <li>• Cosine similarity for scoring</li>
                <li>• Fast: O(n) after pre-computation</li>
                <li>• Used for: Initial recall (Top 50-100)</li>
              </ul>
            </div>
            <div className="bg-gray-900 rounded-lg p-4">
              <h4 className="font-semibold text-yellow-400 mb-2">Cross-Encoder</h4>
              <ul className="text-sm space-y-1">
                <li>• Joint encoding: [CLS] Q [SEP] D [SEP]</li>
                <li>• Direct relevance prediction</li>
                <li>• Slow: O(n×m) for each pair</li>
                <li>• Used for: Precision reranking (Top 5-10)</li>
              </ul>
            </div>
          </div>

          <div className="bg-yellow-900/20 rounded-lg p-4">
            <h4 className="font-semibold text-yellow-300 mb-2">Two-Stage Strategy</h4>
            <p className="text-sm">
              Stage 1: Bi-encoder rapid recall → Top 50 candidates (1-2ms)<br/>
              Stage 2: Cross-encoder precision rerank → Top 5 results (50-100ms)<br/>
              <strong>Result:</strong> Best of both worlds - fast and accurate
            </p>
          </div>
        </div>
      </div>

      {/* Dynamic Learning */}
      <div id="dynamic-learning" className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Lightbulb className="w-6 h-6 text-pink-400" />
          <h2 className="text-xl font-bold">Dynamic Few-Shot Learning</h2>
        </div>
        
        <div className="space-y-4 text-gray-300">
          <p className="leading-relaxed">
            Instead of static prompts, the system <strong className="text-pink-400">learns from successful 
            interactions</strong>. When users give positive feedback, that query-answer pair is stored 
            and retrieved as an example for similar future queries.
          </p>

          <div className="bg-gray-900 rounded-lg p-4 border-l-4 border-pink-500">
            <h4 className="font-semibold text-pink-300 mb-2">Workflow</h4>
            <ol className="text-sm space-y-2 list-decimal list-inside">
              <li>User gives 👍 to a good answer</li>
              <li>System stores (query, answer) in vector index</li>
              <li>For new queries, retrieve similar past successes</li>
              <li>Include retrieved examples in prompt as few-shot context</li>
              <li>LLM generates answer guided by successful patterns</li>
            </ol>
          </div>

          <div className="bg-pink-900/20 rounded-lg p-4">
            <h4 className="font-semibold text-pink-300 mb-2">Benefits</h4>
            <ul className="space-y-1 text-sm list-disc list-inside">
              <li>Continuous improvement without model retraining</li>
              <li>Domain-specific knowledge accumulation</li>
              <li>Reduces hallucinations by providing grounded examples</li>
              <li>Personalizes to organization or user patterns</li>
            </ul>
          </div>
        </div>
      </div>

      {/* DSPy */}
      <div id="dspy" className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center space-x-2 mb-4">
          <BookOpen className="w-6 h-6 text-indigo-400" />
          <h2 className="text-xl font-bold">DSPy: Automatic Prompt Optimization</h2>
        </div>
        
        <div className="space-y-4 text-gray-300">
          <p className="leading-relaxed">
            DSPy treats prompts as <strong className="text-indigo-400">programs that can be compiled and 
            optimized</strong>. Instead of manual prompt engineering, you define a metric (e.g., accuracy) 
            and let DSPy automatically optimize the prompt against a validation set.
          </p>

          <div className="bg-gray-900 rounded-lg p-4">
            <h4 className="font-semibold mb-2">Key Concepts</h4>
            <div className="space-y-2 text-sm">
              <div className="flex items-start space-x-2">
                <span className="text-indigo-400 font-semibold min-w-[120px]">Signatures:</span>
                <span>Define input/output schema (question → answer)</span>
              </div>
              <div className="flex items-start space-x-2">
                <span className="text-indigo-400 font-semibold min-w-[120px]">Modules:</span>
                <span>Composable LLM operations (ChainOfThought, ReAct)</span>
              </div>
              <div className="flex items-start space-x-2">
                <span className="text-indigo-400 font-semibold min-w-[120px]">Optimizers:</span>
                <span>MIPROv2 rewrites prompts based on validation metrics</span>
              </div>
            </div>
          </div>

          <div className="bg-indigo-900/20 rounded-lg p-4">
            <h4 className="font-semibold text-indigo-300 mb-2">Example Workflow</h4>
            <pre className="text-xs overflow-x-auto"><code>{`# Define what you want
class GenerateAnswer(dspy.Signature):
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()

# Let DSPy optimize
optimizer = dspy.MIPROv2(metric=dspy.evaluate.SemanticF1)
optimized_rag = optimizer.compile(RAG(), trainset=data)`}</code></pre>
          </div>
        </div>
      </div>

      {/* Best Practices */}
      <div className="bg-gradient-to-r from-blue-900/30 to-purple-900/30 rounded-lg border border-blue-500/30 p-6">
        <h3 className="text-xl font-semibold mb-4">🎯 Best Practices for Production</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="space-y-2">
            <h4 className="font-semibold text-blue-300">Query Enhancement</h4>
            <ul className="space-y-1 text-gray-300 list-disc list-inside">
              <li>Use HyDE for technical/domain-specific queries</li>
              <li>Apply decomposition for comparison questions</li>
              <li>Cache hypothetical documents to reduce latency</li>
            </ul>
          </div>
          <div className="space-y-2">
            <h4 className="font-semibold text-purple-300">Document Validation</h4>
            <ul className="space-y-1 text-gray-300 list-disc list-inside">
              <li>Always grade documents before generation</li>
              <li>Set strict relevance thresholds for CRAG</li>
              <li>Implement web search fallback for critical queries</li>
            </ul>
          </div>
          <div className="space-y-2">
            <h4 className="font-semibold text-green-300">Reranking</h4>
            <ul className="space-y-1 text-gray-300 list-disc list-inside">
              <li>Use cross-encoders only on top-k candidates</li>
              <li>Fine-tune on domain data for best results</li>
              <li>Monitor latency vs accuracy trade-offs</li>
            </ul>
          </div>
          <div className="space-y-2">
            <h4 className="font-semibold text-yellow-300">Learning System</h4>
            <ul className="space-y-1 text-gray-300 list-disc list-inside">
              <li>Collect explicit feedback (👍/👎)</li>
              <li>Regularly curate example library</li>
              <li>A/B test with and without examples</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Documentation
