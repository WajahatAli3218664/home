import { useEffect, useState } from 'react';
import { getProgressForUser } from '../services/progressService';
import { ProgressRecord } from '../types/progress';

const ProgressPage = () => {
  const [progressRecords, setProgressRecords] = useState<ProgressRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        // Using a placeholder user ID of 1 for this example
        const userId = 1;
        const progressData = await getProgressForUser(userId);
        setProgressRecords(progressData);
      } catch (err) {
        setError('Failed to load progress data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Loading progress data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  // Calculate overall progress
  const completedChapters = progressRecords.filter(record => record.completed).length;
  const totalChapters = progressRecords.length;
  const overallProgress = totalChapters > 0 ? Math.round((completedChapters / totalChapters) * 100) : 0;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Learning Progress</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">Overall Progress</h2>
        <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
          <div 
            className="bg-blue-600 h-4 rounded-full" 
            style={{ width: `${overallProgress}%` }}
          ></div>
        </div>
        <p>{overallProgress}% Complete ({completedChapters}/{totalChapters} chapters)</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Chapter Progress</h2>
        {progressRecords.length === 0 ? (
          <p>No progress data available yet. Start reading chapters to track your progress!</p>
        ) : (
          <div className="space-y-4">
            {progressRecords.map(record => (
              <div key={record.id} className="border-b pb-4 last:border-b-0">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-medium">Chapter {record.chapter_id}: {record.chapter_title}</h3>
                  <span className={`px-2 py-1 rounded text-sm ${
                    record.completed 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {record.completed ? 'Completed' : 'In Progress'}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full" 
                    style={{ width: `${record.progress_percentage}%` }}
                  ></div>
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  {record.progress_percentage}% complete
                  {record.time_spent > 0 && ` • Spent ${Math.floor(record.time_spent / 60)} min reading`}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProgressPage;