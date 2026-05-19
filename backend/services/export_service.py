"""
Export service for downloading chat sessions and conversations.
Supports multiple formats: Markdown, JSON, TXT.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ExportService:
    """
    Service for exporting chat sessions and conversations.
    
    Features:
    - Export to Markdown format
    - Export to JSON format
    - Export to plain text
    - Include metadata and formatting
    - Add timestamps
    """

    def __init__(self):
        self.formats = {'markdown', 'json', 'txt'}

    def export_session(
        self,
        session_id: str,
        messages: List[Dict[str, Any]],
        format: str = 'markdown',
        session_summary: Optional[str] = None
    ) -> str:
        """
        Export a chat session in specified format.
        
        Args:
            session_id: Chat session ID
            messages: List of messages in session
            format: Export format ('markdown', 'json', 'txt')
            session_summary: Optional session summary
            
        Returns:
            Exported content as string
        """
        if format not in self.formats:
            raise ValueError(f"Unsupported format: {format}. Use: {self.formats}")

        if format == 'markdown':
            return self._export_markdown(session_id, messages, session_summary)
        elif format == 'json':
            return self._export_json(session_id, messages, session_summary)
        else:  # txt
            return self._export_txt(session_id, messages, session_summary)

    def _export_markdown(
        self,
        session_id: str,
        messages: List[Dict[str, Any]],
        session_summary: Optional[str]
    ) -> str:
        """Export as Markdown with formatting."""
        lines = []
        
        # Header
        lines.append(f"# Chat Session Export\n")
        lines.append(f"**Session ID**: `{session_id}`\n")
        lines.append(f"**Exported**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**Messages**: {len(messages)}\n")
        
        if session_summary:
            lines.append(f"\n## Summary\n")
            lines.append(f"{session_summary}\n")

        # Messages
        lines.append(f"\n## Conversation\n")
        for idx, msg in enumerate(messages, 1):
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            
            lines.append(f"\n### Message {idx} - {role}")
            if timestamp:
                lines.append(f"*{timestamp}*\n")
            lines.append(f"{content}\n")
            
            # Add citations if present
            if msg.get('citations'):
                lines.append(f"\n**Sources:**")
                for citation in msg['citations']:
                    source = citation.get('source', 'Unknown')
                    score = citation.get('score', 0)
                    lines.append(f"- {source} (Relevance: {score:.2f})")
                lines.append("")

        return "\n".join(lines)

    def _export_json(
        self,
        session_id: str,
        messages: List[Dict[str, Any]],
        session_summary: Optional[str]
    ) -> str:
        """Export as JSON."""
        data = {
            'session_id': session_id,
            'exported_at': datetime.now().isoformat(),
            'summary': session_summary,
            'message_count': len(messages),
            'messages': messages
        }
        return json.dumps(data, indent=2)

    def _export_txt(
        self,
        session_id: str,
        messages: List[Dict[str, Any]],
        session_summary: Optional[str]
    ) -> str:
        """Export as plain text."""
        lines = []
        
        lines.append("=" * 80)
        lines.append("CHAT SESSION EXPORT")
        lines.append("=" * 80)
        lines.append(f"\nSession ID: {session_id}")
        lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Messages: {len(messages)}\n")
        
        if session_summary:
            lines.append("SUMMARY")
            lines.append("-" * 80)
            lines.append(session_summary)
            lines.append("")

        lines.append("CONVERSATION")
        lines.append("-" * 80)
        
        for idx, msg in enumerate(messages, 1):
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', '')
            
            lines.append(f"\n[{idx}] {role}")
            if timestamp:
                lines.append(f"Time: {timestamp}")
            lines.append(content)
            
            if msg.get('citations'):
                lines.append("\nSources:")
                for citation in msg['citations']:
                    source = citation.get('source', 'Unknown')
                    score = citation.get('score', 0)
                    lines.append(f"  - {source} (Relevance: {score:.2f})")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def generate_filename(
        self,
        session_id: str,
        format: str
    ) -> str:
        """Generate appropriate filename for export."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = 'md' if format == 'markdown' else format
        return f"chat_{session_id}_{timestamp}.{ext}"


# Singleton instance
export_service = ExportService()
