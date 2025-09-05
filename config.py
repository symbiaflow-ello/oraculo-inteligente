```python
import os

class Config:
    # Chaves das APIs (via Repository Secrets)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    WOLFRAM_APP_ID = os.getenv('WOLFRAM_APP_ID')
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    
    @classmethod
    def validate(cls):
        required = ['OPENAI_API_KEY', 'WOLFRAM_APP_ID', 'NOTION_TOKEN']
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"🔑 Chaves faltando: {missing}")
        return True
    
    @classmethod  
    def get_status(cls):
        status = {
            'openai': '✅' if cls.OPENAI_API_KEY else '❌',
            'wolfram': '✅' if cls.WOLFRAM_APP_ID else '❌', 
            'notion': '✅' if cls.NOTION_TOKEN else '❌',
            'database': '✅' if cls.NOTION_DATABASE_ID else '⚠️'
        }
        return status
```
