 import React, { JSX, useState } from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import api from '../services/api';
const { generateText, generateMultipleTexts } = api;

function GeneratePage(): JSX.Element {
  const [generatedText, setGeneratedText] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [history, setHistory] = useState<string[]>([]);

  const generateTextFromAPI = async () => {
    setIsLoading(true);

    try {
      const text = await generateText();
      setGeneratedText(text);
      setHistory(prev => [text, ...prev.slice(0, 4)]); // Keep only last 5 items
    } catch (error) {
      console.error('Error generating text:', error);
      setGeneratedText("Error generating text. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const generateMultipleTextsFromAPI = async () => {
    setIsLoading(true);

    try {
      const texts = await generateMultipleTexts(5);
      const combinedText = texts.join(' ');
      setGeneratedText(combinedText);
      setHistory(prev => [...texts, ...prev.slice(0, 5)]);
    } catch (error) {
      console.error('Error generating multiple texts:', error);
      setGeneratedText("Error generating text. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout title="Text Generator" description="AI-powered text generation for robotics and AI education">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h1 className="text--center margin-bottom--lg">AI-Powered Text Generator</h1>

            <div className="margin-bottom--lg text-center">
              <button
                className={clsx(
                  'button button--primary button--lg margin-right--sm',
                  isLoading && 'button--disabled'
                )}
                onClick={generateTextFromAPI}
                disabled={isLoading}
              >
                {isLoading ? 'Generating...' : 'Generate Text'}
              </button>

              <button
                className={clsx(
                  'button button--secondary button--lg',
                  isLoading && 'button--disabled'
                )}
                onClick={generateMultipleTextsFromAPI}
                disabled={isLoading}
              >
                {isLoading ? 'Generating...' : 'Generate Multiple'}
              </button>
            </div>

            {generatedText && (
              <div className="card margin-bottom--lg">
                <div className="card__body text--left">
                  <h3>Generated Text:</h3>
                  <p className="font--large padding--sm" style={{backgroundColor: '#f8f9fa', borderRadius: '4px'}}>
                    {generatedText}
                  </p>
                </div>
              </div>
            )}

            {history.length > 0 && (
              <div className="card">
                <div className="card__header">
                  <h3>Generation History</h3>
                </div>
                <div className="card__body text--left">
                  <ol>
                    {history.map((text, index) => (
                      <li key={index} className="margin-bottom--sm">{text}</li>
                    ))}
                  </ol>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default GeneratePage;