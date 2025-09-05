```python
import gradio as gr
from iris_core import IRISOracle
from config import Config
import time

# Inicializar ÍRIS
print("🌌 Iniciando ÍRIS Oracle...")
iris = IRISOracle()

if iris.status["initialized"]:
    status_msg = "✅ ÍRIS Oracle inicializada com sucesso!"
    status_color = "green"
else:
    status_msg = f"❌ Erro na inicialização: {iris.status['error']}"
    status_color = "red"

print(status_msg)

def chat_with_iris(message, history):
    """Interface de chat com ÍRIS"""
    if not iris.status["initialized"]:
        return "❌ ÍRIS não está disponível. Verifique as configurações das APIs nos Repository Secrets."
    
    try:
        # Processar consulta
        result = iris.process_query(message)
        response = result["response"]
        
        # Adicionar informações de status
        if result["type"] == "calculation":
            response += "\n\n🔢 *Processado com Wolfram Alpha*"
        elif result["type"] == "conversation":
            response += "\n\n💭 *Processado com GPT*"
        
        if result["saved"]:
            response += " • 💾 Salvo no Notion"
        elif Config.NOTION_DATABASE_ID:
            response += " • ⚠️ Erro ao salvar no Notion" 
        
        return response
    
    except Exception as e:
        return f"🔥 Erro inesperado: {str(e)}"

def get_system_status():
    """Retorna status do sistema"""
    status = Config.get_status()
    
    status_html = f"""
    <div style="padding: 15px; background: #f8f9fa; border-radius: 8px; margin: 10px 0;">
        <h4>📊 Status do Sistema</h4>
        <ul style="list-style: none; padding-left: 0;">
            <li>🤖 OpenAI GPT: {status['openai']}</li>
            <li>🔢 Wolfram Alpha: {status['wolfram']}</li>
            <li>📝 Notion API: {status['notion']}</li>
            <li>🗃️ Database: {status['database']}</li>
            <li>🌐 HuggingFace: ✅</li>
            <li>🌌 ÍRIS Core: {'✅' if iris.status["initialized"] else '❌'}</li>
        </ul>
    </div>
    """
    return status_html

def create_interface():
    """Criar interface Gradio"""
    
    # CSS customizado
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    """
    
    with gr.Blocks(
        title="🌌 ÍRIS Oracle", 
        theme=gr.themes.Soft(),
        css=custom_css
    ) as demo:
        
        # Cabeçalho
        gr.HTML(f"""
        <div class="header">
            <h1>🌌 ÍRIS Oracle</h1>
            <p style="font-size: 1.2em; margin: 10px 0;">
                Seu assistente inteligente com GPT + Wolfram Alpha + Notion
            </p>
            <p style="color: {status_color}; font-weight: bold;">
                {status_msg}
            </p>
        </div>
        """)
        
        with gr.Row():
            # Coluna principal - Chat
            with gr.Column(scale=3):
                chatbot = gr.ChatInterface(
                    chat_with_iris,
                    title="💬 Converse com ÍRIS",
                    description="""
                    🔮 **Faça qualquer pergunta ou peça cálculos complexos!**
                    
                    • **Conversação geral**: Perguntas, análises, discussões
                    • **Cálculos matemáticos**: Use palavras como "calcule", "resolva", etc.
                    • **Consultas científicas**: Física, química, estatística
                    • **Tudo é salvo automaticamente no seu Notion!**
                    """,
                    examples=[
                        "Olá ÍRIS! Como você funciona?",
                        "Calcule a integral de x² de 0 a 10", 
                        "Qual a distância da Terra à Lua?",
                        "Resolva a equação 3x + 15 = 60",
                        "Converta 100 metros em pés",
                        "Qual o logaritmo natural de 2.718?",
                        "Me explique a teoria da relatividade",
                        "Faça um resumo sobre inteligência artificial"
                    ],
                    retry_btn="🔄 Tentar Novamente",
                    undo_btn="↩️ Desfazer", 
                    clear_btn="🗑️ Limpar Chat"
                )
            
            # Coluna lateral - Status e informações
            with gr.Column(scale=1):
                status_display = gr.HTML(get_system_status())
                
                gr.HTML("""
                <div style="padding: 15px; background: #e8f4f8; border-radius: 8px; margin: 10px 0;">
                    <h4>💡 Dicas de Uso</h4>
                    <ul style="font-size: 0.9em;">
                        <li><strong>Para cálculos:</strong> Use "calcule", "resolva", "integral"</li>
                        <li><strong>Para conversas:</strong> Pergunte naturalmente</li>
                        <li><strong>Histórico:</strong> Mantido durante a sessão</li>
                        <li><strong>Notion:</strong> Tudo salvo automaticamente</li>
                    </ul>
                </div>
                """)
                
                gr.HTML("""
                <div style="padding: 15px; background: #f0f8f0; border-radius: 8px; margin: 10px 0;">
                    <h4>🌟 Funcionalidades</h4>
                    <ul style="font-size: 0.9em;">
                        <li>🤖 Conversação inteligente</li>
                        <li>🔢 Cálculos precisos</li>
                        <li>📊 Gráficos e análises</li>
                        <li>🗃️ Organização automática</li>
                        <li>☁️ 100% na nuvem</li>
                        <li>🔒 Dados seguros</li>
                    </ul>
                </div>
                """)
                
                # Botão para atualizar status
                refresh_btn = gr.Button("🔄 Atualizar Status", size="sm")
                refresh_btn.click(
                    fn=get_system_status,
                    outputs=status_display
                )
    
    return demo

if __name__ == "__main__":
    print("🚀 Iniciando interface web...")
    demo = create_interface()
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
```
