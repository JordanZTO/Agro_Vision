# 📖 Guia de Contribuição

Obrigado por estar interessado em contribuir com **AgroVision AI**! 🌾

## Como Começar

### 1. Fork o Repositório
```bash
# Clone seu fork
git clone https://github.com/SEU_USUARIO/agrovision_ia.git
cd agrovision_ia
```

### 2. Criar Branch de Desenvolvimento
```bash
git checkout -b feature/sua-feature
```

### 3. Configurar Ambiente Local
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Configurar `.env`
```bash
# Copie o exemplo
copy .env.example .env

# Edite com suas configurações
notepad .env
```

### 5. Fazer Mudanças
- Faça alterações incrementais
- Teste localmente: `python -m uvicorn app:app --reload`
- Commit frequente: `git add . && git commit -m "Descrição clara"`

### 6. Enviar Pull Request
```bash
git push origin feature/sua-feature
```

---

## Padrões de Código

### Python
- Use **PEP 8**
- Máximo 100 caracteres por linha
- Docstrings em funções
- Type hints quando possível

```python
def processar_evento(evento: Dict) -> str:
    """
    Processa um evento detectado.
    
    Args:
        evento: Dict com dados do evento
        
    Returns:
        String com resultado do processamento
    """
    pass
```

### Commits
```bash
# Bom
git commit -m "feat: adicionar detecção de motos no YOLO"
git commit -m "fix: corrigir delay no chat"
git commit -m "docs: atualizar README com câmeras suportadas"

# Ruim
git commit -m "atualizar código"
git commit -m "mudanças"
```

---

## Estrutura de Branches

```
main (estável, pronto para produção)
├── develop (desenvolvimento)
│   ├── feature/nova-funcionalidade
│   ├── bugfix/corrigir-problema
│   └── docs/melhorar-documentação
```

---

## Áreas para Contribuir

### 🎯 Ficou Fácil
- [ ] Melhorar documentação
- [ ] Adicionar comentários ao código
- [ ] Criar exemplos
- [ ] Corrigir erros de digitação

### 🏗️ Intermediário
- [ ] Otimizar performance
- [ ] Adicionar testes
- [ ] Refatorar código
- [ ] Melhorar UI/UX

### 🚀 Avançado
- [ ] Múltiplas câmeras simultâneas
- [ ] Autenticação e roles
- [ ] Integração com webhooks
- [ ] Deployment em Docker/Kubernetes
- [ ] API REST completa
- [ ] Histórico gráfico

---

## Testes

Se adicionar feature, inclua testes:

```python
# services/test_monitoring_agent.py
def test_build_event_context():
    events = [
        {"label": "car", "confidence": 0.9, "event_time": "2026-04-17 12:00:00"}
    ]
    context = build_event_context(events)
    assert "car" in context
    assert "0.90" in context or "0.9" in context
```

Execute:
```bash
pytest services/
```

---

## Checklist antes de enviar PR

- [ ] Código segue PEP 8
- [ ] `.env` não foi commitado
- [ ] `requirements.txt` foi atualizado (se instalou novo package)
- [ ] README foi atualizado (se mudou funcionalidade)
- [ ] Nenhum erro no console ao testar
- [ ] Commits têm mensagens claras
- [ ] Sem arquivos temporários (`.pyc`, `__pycache__`)

---

## Reportar Issues

Se encontrou um bug:

1. Verifique se já não foi reportado
2. Teste em versão mais recente
3. Inclua:
   - Sistema operacional
   - Versão do Python
   - Passos para reproduzir
   - Mensagem de erro exata
   - Logs relevantes

---

## Licença

Ao contribuir, você concorda que seu código será licenciado sob a mesma licença do projeto.

---

## Dúvidas?

- Abra uma **Issue** para discussão
- Veja **Discussions** para perguntas gerais
- Entre em contato via **Pull Request**

**Obrigado por melhorar AgroVision AI!** 🙏
