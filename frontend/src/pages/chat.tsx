import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { RAGChatComponent } from '../components/RAGChat/RAGChatComponent';

const ChatPage = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'about'>('chat');

  return (
    <Layout title="AI Assistant - RoboLearn" description="AI-powered chatbot for Physical AI & Humanoid Robotics textbook">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <header className="mb-10 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">AI Textbook Assistant</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Ask questions about the Physical AI & Humanoid Robotics textbook. Our AI assistant only answers from the textbook content with proper citations.
          </p>
        </header>

        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('chat')}
                className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                  activeTab === 'chat'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Ask Questions
              </button>
              <button
                onClick={() => setActiveTab('about')}
                className={`py-4 px-6 text-center border-b-2 font-medium text-sm ${
                  activeTab === 'about'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                How It Works
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'chat' ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2">
                  <RAGChatComponent />
                </div>
                
                <div className="lg:col-span-1">
                  <div className="bg-blue-50 p-6 rounded-lg">
                    <h3 className="font-bold text-lg text-blue-800 mb-3">Guidelines for Asking Questions</h3>
                    <ul className="space-y-2 text-sm text-blue-700">
                      <li className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>Ask about specific concepts from the textbook</span>
                      </li>
                      <li className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>Reference chapter or section if known</span>
                      </li>
                      <li className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>Ask for explanations of complex topics</span>
                      </li>
                      <li className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>Request examples or applications</span>
                      </li>
                    </ul>
                    
                    <div className="mt-6">
                      <h3 className="font-bold text-lg text-blue-800 mb-3">Example Questions</h3>
                      <ul className="space-y-2 text-sm text-blue-700">
                        <li className="p-2 bg-white rounded border border-blue-100">Explain embodied cognition principles</li>
                        <li className="p-2 bg-white rounded border border-blue-100">What are morphological computation techniques?</li>
                        <li className="p-2 bg-white rounded border border-blue-100">How does sensorimotor learning work?</li>
                        <li className="p-2 bg-white rounded border border-blue-100">Compare different humanoid robot designs</li>
                      </ul>
                    </div>
                  </div>
                  
                  <div className="mt-6 bg-yellow-50 p-6 rounded-lg">
                    <h3 className="font-bold text-lg text-yellow-800 mb-3">Grounding Notice</h3>
                    <p className="text-sm text-yellow-700">
                      This AI assistant only responds based on information found in the Physical AI & Humanoid Robotics textbook. 
                      Responses are grounded in actual content with citations to source material.
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="prose max-w-none">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">How the AI Assistant Works</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <div className="text-blue-600 text-2xl mb-3">🔍</div>
                    <h3 className="font-bold text-lg text-gray-900 mb-2">Retrieval-Augmented Generation</h3>
                    <p className="text-gray-700">
                      Our system combines information retrieval with language generation to provide accurate answers based solely on your textbook content.
                    </p>
                  </div>
                  
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <div className="text-blue-600 text-2xl mb-3">📋</div>
                    <h3 className="font-bold text-lg text-gray-900 mb-2">Grounded Responses</h3>
                    <p className="text-gray-700">
                      Every answer is backed by specific passages from the textbook, eliminating hallucinations and ensuring educational accuracy.
                    </p>
                  </div>
                  
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <div className="text-blue-600 text-2xl mb-3">🔗</div>
                    <h3 className="font-bold text-lg text-gray-900 mb-2">Citation System</h3>
                    <p className="text-gray-700">
                      Responses include citations to specific chapters, sections, and pages where the information appears in the textbook.
                    </p>
                  </div>
                  
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <div className="text-blue-600 text-2xl mb-3">📚</div>
                    <h3 className="font-bold text-lg text-gray-900 mb-2">Textbook Integration</h3>
                    <p className="text-gray-700">
                      The system understands the structure and content of your textbook to provide contextually relevant answers.
                    </p>
                  </div>
                </div>
                
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="font-bold text-lg text-gray-900 mb-3">Technical Implementation</h3>
                  <p className="text-gray-700 mb-3">
                    The RAG (Retrieval-Augmented Generation) system uses vector embeddings to match your questions with relevant textbook passages, then generates responses that cite the exact sources used.
                  </p>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Vector database stores textbook content embeddings</li>
                    <li>Similarity search finds relevant passages</li>
                    <li>Language model generates responses based on retrieved content</li>
                    <li>All responses are verified against original source material</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ChatPage;