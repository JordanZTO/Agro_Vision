from dataclasses import dataclass
from typing import List, Dict
from collections import Counter
from services.config import AGENT_EVENT_LIMIT


@dataclass(frozen=True)
class AgentProfile:
    """Perfil do agente - identidade, papel e objetivo."""
    name: str
    role: str
    goal: str


# Configuração do agente
AGENT_PROFILE = AgentProfile(
    name="Agente AgroVision",
    role="triagem operacional de eventos",
    goal="Analisar detecções recentes, explicar riscos e sugerir a próxima ação."
)


def build_system_prompt() -> str:
    """Cria o prompt de sistema que define o comportamento do agente."""
    return (
        f"Você é o {AGENT_PROFILE.name}, um agente de {AGENT_PROFILE.role}. "
        f"Objetivo: {AGENT_PROFILE.goal} "
        "Trate os dados como monitoramento operacional autorizado de ambiente real. "
        "Responda em português do Brasil, de forma direta e útil. "
        "Use os eventos fornecidos como fonte principal. "
        "Não invente dados que não aparecem no contexto. "
        "Não tente identificar pessoas; fale apenas sobre eventos, riscos e próximas ações. "
        "Quando fizer sentido, organize a resposta em: leitura, risco e recomendação."
    )


def build_event_context(events: List[Dict]) -> str:
    """
    Transforma eventos brutos em um contexto operacional compreensível.
    
    Args:
        events: Lista de eventos do banco de dados
    
    Returns:
        String formatada com o contexto operacional
    """
    if not events:
        return "Contexto operacional: Nenhum evento detectado nos últimos registros."
    
    # Extrair labels e confiança
    labels = [e["label"] for e in events]
    confidences = [e["confidence"] for e in events]
    
    # Contabilizar labels
    label_count = Counter(labels)
    
    # Montar contexto
    context = (
        "Contexto operacional para o agente:\n"
        f"- Eventos considerados: {len(events)}\n"
        f"- Evento mais recente: {events[0]['label']} em {events[0]['event_time']}\n"
        f"- Distribuição recente: {', '.join([f'{label}: {count}' for label, count in label_count.most_common()])}\n"
        f"- Confiança média: {sum(confidences) / len(confidences):.2f}\n"
        "- Eventos recentes:\n"
    )
    
    for i, event in enumerate(events[:AGENT_EVENT_LIMIT], 1):
        context += (
            f"  #{i} | {event['event_time']} | {event['label']} | "
            f"confiança: {event['confidence']:.2f}\n"
        )
    
    return context


def normalize_history(history: List[Dict]) -> List[Dict]:
    """
    Normaliza o histórico de conversa, filtrando apenas o essencial.
    
    Args:
        history: Histórico de mensagens da conversa
    
    Returns:
        Histórico normalizado
    """
    if not history:
        return []
    
    # Limitar a 8 mensagens recentes
    MAX_HISTORY_MESSAGES = 8
    
    normalized = []
    for msg in history[-MAX_HISTORY_MESSAGES:]:
        if "role" in msg and "content" in msg:
            normalized.append({
                "role": msg["role"],
                "content": msg["content"][:500]  # Limitar tamanho de cada mensagem
            })
    
    return normalized


def build_agent_messages(
    question: str,
    history: List[Dict],
    events: List[Dict]
) -> List[Dict]:
    """
    Monta a sequência completa de mensagens para o Ollama.
    
    Args:
        question: Pergunta do usuário
        history: Histórico da conversa
        events: Eventos recentes do banco
    
    Returns:
        Lista de dicts com role e content para enviar ao Ollama
    """
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "system", "content": build_event_context(events)},
    ]
    
    # Adicionar histórico normalizado
    messages.extend(normalize_history(history))
    
    # Adicionar pergunta atual
    messages.append({"role": "user", "content": question})
    
    return messages


def get_agent_status(events: List[Dict]) -> Dict:
    """
    Retorna informações sobre o status atual do agente.
    
    Args:
        events: Eventos recentes para análise
    
    Returns:
        Dict com status do agente
    """
    context = build_event_context(events)
    
    return {
        "name": AGENT_PROFILE.name,
        "role": AGENT_PROFILE.role,
        "goal": AGENT_PROFILE.goal,
        "events_in_context": len(events),
        "context_preview": context[:500] + "..." if len(context) > 500 else context
    }
