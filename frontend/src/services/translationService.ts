// Mock service for translation functionality - in a real implementation, this would connect to your backend API
export interface TranslationRequest {
  text: string;
  sourceLang: string;
  targetLang: string;
}

export interface TranslationResponse {
  translatedText: string;
  sourceLang: string;
  targetLang: string;
  confidence: number;
}

export interface TerminologyMapping {
  [englishTerm: string]: string;
}

// Mock terminology mappings for technical terms
const TERMINOLOGY_MAPPING: Record<string, TerminologyMapping> = {
  ur: {
    'Physical AI': 'متعامدہ ای آئی',
    'Embodied AI': 'جسمانی ذہانت',
    'Robotics': 'روبوٹکس',
    'Machine Learning': 'مشین لرننگ',
    'Computer Vision': 'کمپیوٹر وژن',
    'Natural Language Processing': 'قدرتی زبان کی پروسیسنگ',
    'ROS': 'ROS',
    'Isaac Sim': 'آئزیک سیم',
    'Gazebo': 'گزیبو',
    'VLA Models': 'وی ایل اے ماڈلز',
    'Embodied Intelligence': 'جسمانی ذہانت',
    'Human-Robot Interaction': 'انسان-روبوٹ تعامل',
    'Sim-to-Real Transfer': 'سیم ٹو رئل ٹرانسفر',
    'Manipulation': 'ہاتھ سے کام',
    'Locomotion': 'چلنے کی صلاحیت',
    'Perception': 'ادراک',
    'Planning': 'منصوبہ بندی',
    'Control Systems': 'کنٹرول سسٹم',
    'Learning and Adaptation': 'سیکھنے اور موافقت کے نظام',
    'Ethics and Society': 'اخلاقیات اور معاشرہ',
    'Future Directions': 'مستقبل کی سمت',
    'Humanoid Robotics': 'ہیومنوائڈ روبوٹکس',
    'Humanoid Robot': 'ہیومنوائڈ روبوٹ',
    'Artificial Intelligence': 'مصنوعی ذہانت',
    'Simulation': 'سیمولیشن',
    'Physics': 'فزکس',
    'Middleware': 'مڈل ویئر',
    'Framework': '-framework',
    'Platform': 'پلیٹ فارم',
    'Algorithm': 'الگورتھم',
    'Sensor': 'سینسر',
    'Actuator': 'اکچو ایٹر',
    'Kinematics': 'کائنیمیٹکس',
    'Dynamics': 'ڈائنامکس',
    'Trajectory': 'مسیر',
    'Control': 'کنٹرول'
  }
};

export const translateText = async (request: TranslationRequest): Promise<TranslationResponse> => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 800));
  
  if (request.targetLang === 'ur') {
    // Apply terminology mapping for technical terms
    let translatedText = request.text;
    const mapping = TERMINOLOGY_MAPPING[request.targetLang] || {};
    
    Object.entries(mapping).forEach(([englishTerm, urduTerm]) => {
      // Create a case-insensitive replacement for technical terms
      translatedText = translatedText.replace(new RegExp(englishTerm, 'gi'), (match) => {
        if (match === englishTerm) return urduTerm; // Exact match
        if (match === englishTerm.toLowerCase()) return urduTerm.toLowerCase(); // Lowercase match
        if (match === englishTerm.charAt(0).toUpperCase() + englishTerm.slice(1).toLowerCase()) {
          return urduTerm.charAt(0).toUpperCase() + urduTerm.slice(1).toLowerCase(); // Capitalized match
        }
        return urduTerm; // Default
      });
    });
    
    // For this mock implementation, we'll return a simplified version
    if (request.text.includes("Introduction to Physical AI")) {
      translatedText = `<h2>متعامدہ ای آئی کا تعارف</h2>
        <p>متعامدہ ای آئی مصنوعی ذہانت میں ایک نظریاتی بارش کی نمائندگی کرتا ہے، جو کہ مادی دنیا کے ساتھ ای آئی کو ضم کرنے پر زور دیتا ہے۔ روایتی ای آئی کے برعکس جو بنیادی طور پر ڈیجیٹل خلا میں کام کرتا ہے، متعامدہ ای آئی نظام کی مادی خصوصیات کا استعمال ذہانت مندی حاصل کرنے کے لئے کرتا ہے۔</p>
        
        <h3>متعامدہ ای آئی کی وضاحت</h3>
        <p>متعامدہ ای آئی ایس طریقہ کار کا احاطہ کرتا ہے جہاں ذہانت کمپیوٹیشنل الگورتھمز اور مادی نظام کے تعامل سے نمودار ہوتی ہے۔ اس میں شامل ہیں:</p>
        <ul>
          <li>جسمانی شعور کے اصول</li>
          <li>روپ و محسوس کی معلومات</li>
          <li>مواد کی ذہانت</li>
          <li>احساس و عمل کے سیکھنے کا طریقہ</li>
        </ul>`;
    } else {
      // Return the original text as a mock translation for other content
      translatedText = request.text;
    }
    
    return {
      translatedText: translatedText,
      sourceLang: request.sourceLang,
      targetLang: request.targetLang,
      confidence: 0.92
    };
  } else {
    // For other languages, just return the original text
    return {
      translatedText: request.text,
      sourceLang: request.sourceLang,
      targetLang: request.targetLang,
      confidence: 1.0
    };
  }
};

export const translateContentBlock = async (content: string, targetLang: string): Promise<string> => {
  if (targetLang === 'en') return content; // No translation needed
  
  const translationReq: TranslationRequest = {
    text: content,
    sourceLang: 'en',
    targetLang: targetLang
  };
  
  const response = await translateText(translationReq);
  return response.translatedText;
};

// Function to get supported languages
export const getSupportedLanguages = () => {
  return [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'ur', name: 'Urdu', nativeName: 'اردو' },
    { code: 'es', name: 'Spanish', nativeName: 'Español' },
    { code: 'fr', name: 'French', nativeName: 'Français' },
    { code: 'de', name: 'German', nativeName: 'Deutsch' }
  ];
};