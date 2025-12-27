import React from 'react';

interface CurriculumModule {
  id: number;
  title: string;
  description: string;
  topics: string[];
  duration: string;
  prerequisites: string[];
  learningOutcomes: string[];
}

interface CurriculumComponentProps {
  modules: CurriculumModule[];
}

export const CurriculumComponent: React.FC<CurriculumComponentProps> = ({ modules }) => {
  return (
    <div className="max-w-6xl mx-auto p-6">
      <header className="mb-10 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Physical AI & Humanoid Robotics Curriculum</h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          A comprehensive learning path designed to take you from robotics fundamentals to advanced humanoid systems
        </p>
      </header>

      <div className="space-y-12">
        {modules.map((module, index) => (
          <div key={module.id} className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{module.title}</h2>
                  <p className="text-gray-600 mt-2">{module.description}</p>
                </div>
                <div className="mt-4 md:mt-0">
                  <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                    {module.duration}
                  </span>
                </div>
              </div>
            </div>

            <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Topics Covered</h3>
                <ul className="space-y-2">
                  {module.topics.map((topic, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-500 mr-2">•</span>
                      <span className="text-gray-700">{topic}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-3">Prerequisites</h3>
                  <ul className="space-y-2">
                    {module.prerequisites.map((prereq, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-blue-500 mr-2">→</span>
                        <span className="text-gray-700">{prereq}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Learning Outcomes</h3>
                  <ul className="space-y-2">
                    {module.learningOutcomes.map((outcome, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-purple-500 mr-2">✓</span>
                        <span className="text-gray-700">{outcome}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="p-4 bg-gray-50 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <div>
                  <span className="text-sm text-gray-600">Module {module.id} of {modules.length}</span>
                </div>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                  Start Module
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};