import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { ChapterContent } from '../components/ChapterContent';
import { RAGChatComponent } from '../components/RAGChat/RAGChatComponent';
import { TranslationControls } from '../components/TranslationControls';

const TextbookPage = () => {
  const chapterData = {
    title: "Foundations of Physical AI",
    number: 1,
    content: `
      <h2 id="introduction">Introduction to Physical AI</h2>
      <p>Physical AI represents a paradigm shift in artificial intelligence, emphasizing the integration of AI with the physical world through embodied systems. Unlike traditional AI that operates primarily in digital spaces, Physical AI leverages the physical properties of systems to achieve intelligent behavior.</p>

      <h3 id="defining-physical-ai">Defining Physical AI</h3>
      <p>Physical AI encompasses approaches where intelligence emerges from the interaction between computational algorithms and physical systems. This includes:</p>
      <ul>
        <li>Embodied cognition principles</li>
        <li>Morphological computation</li>
        <li>Material intelligence</li>
        <li>Sensorimotor learning</li>
      </ul>

      <h3 id="key-principles">Key Principles</h3>
      <h4 id="embodiment">Embodiment</h4>
      <p>The body is not merely an output device for AI but an integral part of intelligence. The physical form influences cognitive processes and learning capabilities.</p>

      <h4 id="morphological-computation">Morphological Computation</h4>
      <p>Physical properties of the body (e.g., elasticity, compliance, dynamics) contribute to computation, reducing the burden on central processing units.</p>

      <h4 id="environmental-interaction">Environmental Interaction</h4>
      <p>Intelligence arises through continuous interaction with the environment, not just from internal processing.</p>
    `,
    duration: "Approx. 8 minutes reading",
    objectives: [
      "Define Physical AI and distinguish it from traditional AI",
      "Explain the concept of embodied cognition",
      "Identify applications of Physical AI in robotics"
    ],
    prerequisites: [
      "Basic understanding of robotics concepts",
      "Familiarity with AI fundamentals"
    ]
  };

  return (
    <Layout title="Textbook - Foundations of Physical AI" description="Chapter 1: Foundations of Physical AI">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <nav className="flex mb-6" aria-label="Breadcrumb">
            <ol className="inline-flex items-center space-x-1 md:space-x-3">
              <li className="inline-flex items-center">
                <Link to="/" className="text-sm text-blue-600 hover:underline">Home</Link>
              </li>
              <li>
                <div className="flex items-center">
                  <span className="mx-2 text-gray-400">/</span>
                  <Link to="/textbook" className="text-sm text-blue-600 hover:underline">Textbook</Link>
                </div>
              </li>
              <li aria-current="page">
                <div className="flex items-center">
                  <span className="mx-2 text-gray-400">/</span>
                  <span className="text-sm text-gray-500">{chapterData.title}</span>
                </div>
              </li>
            </ol>
          </nav>

          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">Physical AI & Humanoid Robotics Textbook</h1>
          <p className="text-lg text-gray-600">Comprehensive educational platform for embodied intelligence</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8">
            <ChapterContent
              content={chapterData.content}
              chapterTitle={chapterData.title}
              chapterNumber={chapterData.number}
              duration={chapterData.duration}
              objectives={chapterData.objectives}
              prerequisites={chapterData.prerequisites}
            />
          </div>

          <div className="lg:col-span-4 space-y-8">
            <div className="sticky top-4 space-y-8">
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Chapter Content</h2>
                <ul className="space-y-3">
                  <li>
                    <Link to="#introduction" className="block py-2 px-3 rounded-lg hover:bg-gray-50 text-blue-600 font-medium">
                      1. Introduction
                    </Link>
                  </li>
                  <li className="pl-4 border-l-2 border-blue-200">
                    <Link to="#defining-physical-ai" className="block py-2 px-3 rounded-lg hover:bg-gray-50 text-gray-700">
                      1.1 Defining Physical AI
                    </Link>
                  </li>
                  <li className="pl-4 border-l-2 border-blue-200">
                    <Link to="#key-principles" className="block py-2 px-3 rounded-lg hover:bg-gray-50 text-gray-700">
                      1.2 Key Principles
                    </Link>
                  </li>
                  <li className="pl-4 border-l-2 border-blue-200">
                    <Link to="#embodiment" className="block py-2 px-3 rounded-lg hover:bg-gray-50 text-gray-700">
                      1.2.1 Embodiment
                    </Link>
                  </li>
                  <li className="pl-4 border-l-2 border-blue-200">
                    <Link to="#morphological-computation" className="block py-2 px-3 rounded-lg hover:bg-gray-50 text-gray-700">
                      1.2.2 Morphological Computation
                    </Link>
                  </li>
                  <li className="pl-4 border-l-2 border-blue-200">
                    <Link to="#environmental-interaction" className="block py-2 px-3 rounded-lg hover:bg-gray-50 text-gray-700">
                      1.2.3 Environmental Interaction
                    </Link>
                  </li>
                </ul>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h2 className="text-xl font-bold text-gray-900 mb-4">AI Textbook Assistant</h2>
                <p className="text-gray-600 text-sm mb-4">Ask questions about this chapter's content. Responses are grounded in the textbook.</p>
                <RAGChatComponent chapterId={1} />
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Navigation</h2>
                <div className="space-y-3">
                  <Link to="/docs/intro" className="block w-full text-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg transition">
                    Browse All Chapters
                  </Link>
                  <Link to="/modules" className="block w-full text-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
                    View Curriculum Modules
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default TextbookPage;