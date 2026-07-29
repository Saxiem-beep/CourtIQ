from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

class CoachingRAG:
    def __init__(self):
        # Mock Sports Science Corpus
        self.corpus = [
            "Knee Recovery: After extensive box jumps, patellar tendon stress increases. Recommended recovery protocol involves 48 hours of rest, ice therapy, and eccentric squatting exercises to rebuild tissue resilience.",
            "Overtraining Signs: Chronic fatigue, resting heart rate elevated by more than 5 bpm, mood irritability, and consecutive days of perceived exertion above 8/10 are primary indicators of Central Nervous System (CNS) overtraining.",
            "Basketball Conditioning: Anaerobic capacity is vital. Interval sprints (15s work, 30s rest) mimic the stop-and-go nature of court play better than steady-state cardio.",
            "Sleep and Performance: Athletes getting less than 7 hours of sleep show a 30% increase in injury risk during high-load training blocks.",
            "Jump Load Management: Exceeding 250 high-impact jumps per week correlates strongly with shin splints and jumper's knee. Deload weeks should halve jump volume."
        ]
        
        # Use lightweight local embeddings so it runs out-of-the-box without OpenAI keys
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        documents = [Document(page_content=text) for text in self.corpus]
        
        self.vectorstore = Chroma.from_documents(
            documents, 
            self.embeddings,
            collection_name="courtiq_knowledge"
        )

    def query_coaching_rag(self, question: str) -> dict:
        results = self.vectorstore.similarity_search_with_score(question, k=2)
        
        if not results:
            return {"answer": "I don't have enough data to answer that confidently.", "sources": []}
            
        # Synthesize a direct answer from the retrieved chunks (simulating an LLM for the prototype)
        context_chunks = [doc.page_content for doc, score in results]
        synthesized_answer = (
            f"Based on the coaching knowledge base, here is the relevant guidance:\n\n"
            f"- {context_chunks[0]}\n"
        )
        if len(context_chunks) > 1:
            synthesized_answer += f"- {context_chunks[1]}"
            
        return {
            "answer": synthesized_answer,
            "sources": context_chunks
        }
