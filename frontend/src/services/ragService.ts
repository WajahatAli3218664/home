// Mock service for RAG functionality - in a real implementation, this would connect to your backend API
export interface RagQueryResponse {
  answer: string;
  sources: string[];
  confidence: number;
  isGrounded: boolean;
}

export interface RagValidationRequest {
  question: string;
}

export interface RagValidationResponse {
  canAnswer: boolean;
  relevantChapters: string[];
  confidence: number;
}

// Mock data for demonstration
const MOCK_KNOWLEDGE_BASE: Record<string, string[]> = {
  "physical ai": [
    "Physical AI represents a paradigm shift in artificial intelligence, emphasizing the integration of AI with the physical world through embodied systems.",
    "Unlike traditional AI that operates primarily in digital spaces, Physical AI leverages the physical properties of systems to achieve intelligent behavior."
  ],
  "ros": [
    "Robot Operating System (ROS) is a flexible framework for writing robot software.",
    "ROS provides libraries and tools to help software developers create robot applications."
  ],
  "simulation": [
    "Simulation plays a crucial role in robotics by allowing testing of algorithms in virtual environments.",
    "Physics-based simulators help bridge the reality gap between simulated and real-world behaviors."
  ],
  "isaac": [
    "NVIDIA Isaac is a robotics platform that provides tools for simulation, training, and deployment of AI robots.",
    "The platform includes Isaac Sim for photorealistic simulation and Isaac ROS for accelerated computing."
  ]
};

export const validateRagQuery = async (request: RagValidationRequest): Promise<RagValidationResponse> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 300));
  
  const lowerCaseQuestion = request.question.toLowerCase();
  const matchingChapters = Object.keys(MOCK_KNOWLEDGE_BASE)
    .filter(key => lowerCaseQuestion.includes(key))
    .map(key => `Chapter on ${key.charAt(0).toUpperCase() + key.slice(1)}`);
  
  return {
    canAnswer: matchingChapters.length > 0,
    relevantChapters: matchingChapters,
    confidence: matchingChapters.length > 0 ? 0.7 + Math.random() * 0.3 : 0.1
  };
};

export const queryRagSystem = async (question: string): Promise<RagQueryResponse> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  const lowerCaseQuestion = question.toLowerCase();
  const relevantSources: string[] = [];
  let answer = "Based on the textbook content, ";
  
  // Build answer and sources based on the question
  Object.entries(MOCK_KNOWLEDGE_BASE).forEach(([topic, content]) => {
    if (lowerCaseQuestion.includes(topic)) {
      answer += content.join(" ");
      relevantSources.push(`Chapter on ${topic.charAt(0).toUpperCase() + topic.slice(1)}`);
    }
  });
  
  if (relevantSources.length === 0) {
    return {
      answer: "I cannot answer this question from the textbook content. Please refer to the relevant chapters first.",
      sources: [],
      confidence: 0.0,
      isGrounded: true
    };
  }
  
  return {
    answer,
    sources: [...new Set(relevantSources)], // Remove duplicates
    confidence: 0.8 + Math.random() * 0.2,
    isGrounded: true
  };
};

// Function to simulate sending chat history for context
export const getConversationContext = async (userId: string) => {
  // This would typically fetch the conversation history from your backend
  return {
    recentQueries: ["What is Physical AI?", "How does ROS work?"],
    commonTopics: ["Physical AI concepts", "Robot Operating System"],
    userProfile: {
      background: "beginner",
      lastActive: new Date(Date.now() - 24 * 60 * 60 * 1000)
    }
  };
};