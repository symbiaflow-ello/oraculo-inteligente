```python
from langchain.agents import initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from notion_client import Client
import wolframalpha
from config import Config
import traceback

class IRISOracle:
    def __init__(self):
        self.status = {"initialized": False, "error": None}
        
        try:
            Config.validate()
            
            # Inicializar componentes principais
            self.llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo", 
                openai_api_key=Config.OPENAI_API_KEY
            )
            
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Wolfram Alpha
            self.wolfram_client = wolframalpha.Client(Config.WOLFRAM_APP_ID)
            
            # Notion (opcional)
            if Config.NOTION_TOKEN:
                self.notion = Client(auth=Config.NOTION_TOKEN)
            else:
                self.notion = None
            
            # Configurar agente com Wolfram Alpha  
            tools = load_tools(["wolfram-alpha"], llm=self.llm, wolfram_alpha_appid=Config.WOLFRAM_APP_ID)
            self.agent = initialize_agent(
                tools,
                self.llm,
                verbose=True,
                memory=self.memory,
                handle_parsing_errors=True
            )
            
            self.status = {"initialized": True, "error": None}
            print("✅ ÍRIS Oracle inicializada com sucesso!")
            
        except Exception as e:
            self.status = {"initialized": False, "error": str(e)}
            print(f"❌ Erro na inicialização: {e}")
            print(traceback.format_exc())
    
    def process_query(self, user_input):
        """Processa consulta do usuário"""
        if not self.status["initialized"]:
            return {
                "response": f"❌ ÍRIS não inicializada: {self.status['error']}",
                "type": "error",
                "saved": False
            }
        
        try:
            # Decidir estratégia baseada no conteúdo
            if self._needs_calculation(user_input):
                print("🔢 Usando Wolfram Alpha...")
                response = self.agent.run(input=user_input)
                query_type = "calculation"
            else:
                print("💭 Usando GPT...")
                response = self.llm.predict(user_input)
                query_type = "conversation"
            
            # Tentar salvar no Notion
            saved = self._save_to_notion(user_input, response, query_type)
            
            return {
                "response": response,
                "type": query_type,
                "saved": saved
            }
            
        except Exception as e:
            error_msg = f"🔥 Erro ao processar: {str(e)}"
            print(error_msg)
            return {
                "response": error_msg,
                "type": "error", 
                "saved": False
            }
    
    def _needs_calculation(self, text):
        """Detecta se precisa de cálculo matemático"""
        calc_keywords = [
            'calcule', 'resolva', 'integral', 'derivada', 'equação',
            'gráfico', 'conversão', 'distância', 'raiz', 'potência',
            'matemática', 'física', 'química', 'estatística',
            '+', '-', '*', '/', '=', '^', '√', 'sen', 'cos', 'log'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in calc_keywords)
    
    def _save_to_notion(self, query, response, query_type):
        """Salva interação no Notion (se configurado)"""
        if not self.notion or not Config.NOTION_DATABASE_ID:
            print("⚠️ Notion não configurado ou sem database ID")
            return False
            
        try:
            self.notion.pages.create(
                parent={"database_id": Config.NOTION_DATABASE_ID},
                properties={
                    "Título": {"title": [{"text": {"content": query[:100]}}]},
                    "Tipo": {"select": {"name": query_type}},
                    "Resposta": {"rich_text": [{"text": {"content": response[:2000]}}]}
                }
            )
            print("💾 Salvo no Notion com sucesso!")
            return True
        except Exception as e:
            print(f"⚠️ Erro ao salvar no Notion: {e}")
            return False
    
    def get_conversation_history(self):
        """Retorna histórico da conversa"""
        if hasattr(self.memory, 'chat_memory'):
            return str(self.memory.chat_memory.messages[-10:])  # Últimas 10
        return "Histórico vazio"
