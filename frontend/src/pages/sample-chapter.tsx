import React from 'react';
import Layout from '@theme/Layout';
import { ChapterComponent } from '../components/Chapter/ChapterComponent';
import { RAGChatComponent } from '../components/RAGChat/RAGChatComponent';
import { useLanguage } from '../contexts/LanguageContext';
import { translateContentBlock } from '../services/translationService';
import { useState, useEffect } from 'react';

const SampleChapter = () => {
  const [translatedContent, setTranslatedContent] = useState<string | null>(null);
  const [translatedTitle, setTranslatedTitle] = useState<string>('');
  const [isTranslating, setIsTranslating] = useState(false);
  const { currentLanguage } = useLanguage();

  const chapterData = {
    title: "Foundations of Physical AI",
    content: `
      <h2>Introduction to Physical AI</h2>
      <p>Physical AI represents a paradigm shift in artificial intelligence, emphasizing the integration of AI with the physical world through embodied systems. Unlike traditional AI that operates primarily in digital spaces, Physical AI leverages the physical properties of systems to achieve intelligent behavior.</p>

      <h3>Defining Physical AI</h3>
      <p>Physical AI encompasses approaches where intelligence emerges from the interaction between computational algorithms and physical systems. This includes:</p>
      <ul>
        <li>Embodied cognition principles</li>
        <li>Morphological computation</li>
        <li>Material intelligence</li>
        <li>Sensorimotor learning</li>
      </ul>

      <h3>Key Principles</h3>
      <h4>Embodiment</h4>
      <p>The body is not merely an output device for AI but an integral part of intelligence. The physical form influences cognitive processes and learning capabilities.</p>

      <h4>Morphological Computation</h4>
      <p>Physical properties of the body (e.g., elasticity, compliance, dynamics) contribute to computation, reducing the burden on central processing units.</p>
    `,
    learningObjectives: [
      "Define Physical AI and distinguish it from traditional AI",
      "Explain the concept of embodied cognition",
      "Identify applications of Physical AI in robotics"
    ],
    prerequisites: [
      "Basic understanding of robotics concepts",
      "Familiarity with AI fundamentals"
    ],
    quizQuestions: [
      {
        id: 1,
        question: "What distinguishes Physical AI from traditional AI?",
        options: [
          "Focus on digital spaces only",
          "Integration with the physical world through embodied systems",
          "Emphasis on computational speed",
          "Exclusively software-based approaches"
        ],
        correctAnswer: 1
      },
      {
        id: 2,
        question: "In Physical AI, what does 'embodiment' refer to?",
        options: [
          "The use of advanced processors",
          "The AI operating only in cloud environments",
          "The body being an integral part of intelligence",
          "The physical appearance of robots"
        ],
        correctAnswer: 2
      }
    ]
  };

  // Handle translation when language changes
  useEffect(() => {
    const handleTranslation = async () => {
      if (currentLanguage === 'en') {
        // Switch back to original content
        setTranslatedContent(null);
        setTranslatedTitle('');
      } else {
        // Translate content to Urdu
        setIsTranslating(true);
        try {
          // Translate content
          const translatedContentResult = await translateContentBlock(chapterData.content, currentLanguage);
          setTranslatedContent(translatedContentResult);

          // Translate title
          const translatedTitleResult = await translateContentBlock(chapterData.title, currentLanguage);
          setTranslatedTitle(translatedTitleResult);
        } catch (error) {
          console.error('Translation error:', error);
          // Fallback to original content if translation fails
          setTranslatedContent(null);
          setTranslatedTitle('');
        } finally {
          setIsTranslating(false);
        }
      }
    };

    handleTranslation();
  }, [currentLanguage]);

  // Add direction attribute based on language
  const contentDirection = currentLanguage === 'ur' ? 'rtl' : 'ltr';
  const contentLang = currentLanguage === 'ur' ? 'ur' : 'en';

  return (
    <Layout title="Sample Chapter - Physical AI Foundations" description="A chapter on Physical AI foundations">
      <div className="container mx-auto px-4 py-8 max-w-6xl" dir={contentDirection}>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-3">
            <ChapterComponent
              title={currentLanguage === 'en' ? chapterData.title : (translatedTitle || chapterData.title)}
              content={currentLanguage === 'en' ? chapterData.content : (translatedContent || chapterData.content)}
              learningObjectives={chapterData.learningObjectives}
              prerequisites={chapterData.prerequisites}
              quizQuestions={chapterData.quizQuestions}
              onProgressUpdate={(progress) => console.log(`Chapter progress: ${progress}%`)}
              lang={contentLang}
            />
          </div>

          <div className="lg:col-span-1">
            <div className="sticky top-4">
              <div className="mb-6">
                <h3 className="text-lg font-semibold mb-3">Chapter Content</h3>
                <ul className="space-y-2">
                  <li><a href="#" className="text-blue-600 hover:underline">Introduction</a></li>
                  <li><a href="#" className="text-blue-600 hover:underline">Defining Physical AI</a></li>
                  <li><a href="#" className="text-blue-600 hover:underline">Key Principles</a></li>
                  <li><a href="#" className="text-blue-600 hover:underline">Applications</a></li>
                  <li><a href="#" className="text-blue-600 hover:underline">Challenges</a></li>
                </ul>
              </div>

              <div className="bg-white p-4 rounded-lg shadow border">
                <h3 className="font-semibold mb-3">Ask AI Assistant</h3>
                <RAGChatComponent chapterId={1} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SampleChapter;