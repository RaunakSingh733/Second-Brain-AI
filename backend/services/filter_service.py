"""
Advanced search filters service for detailed search customization.
Supports filtering by: date range, file type, relevance threshold, file tags.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AdvancedFilterService:
    """
    Service for advanced search filtering and result refinement.
    
    Features:
    - Filter by date range
    - Filter by file type
    - Filter by relevance score threshold
    - Filter by document tags
    - Sort results multiple ways
    - Pagination support
    """

    def __init__(self):
        self.valid_file_types = {'pdf', 'txt', 'md', 'docx'}
        self.valid_sort_fields = {
            'relevance': 'relevance_score',
            'date': 'upload_date',
            'filename': 'source'
        }

    def apply_filters(
        self,
        results: List[Dict[str, Any]],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Apply filters to search results.
        
        Args:
            results: Original search results
            filters: Filter configuration dict
            
        Returns:
            Filtered results
        """
        filtered = results

        # Filter by date range
        if 'date_from' in filters or 'date_to' in filters:
            filtered = self._filter_by_date(filtered, filters)

        # Filter by file type
        if 'file_types' in filters:
            filtered = self._filter_by_file_type(filtered, filters['file_types'])

        # Filter by relevance threshold
        if 'min_relevance' in filters:
            filtered = self._filter_by_relevance(filtered, filters['min_relevance'])

        # Filter by tags
        if 'tags' in filters:
            filtered = self._filter_by_tags(filtered, filters['tags'])

        # Sort results
        if 'sort_by' in filters:
            filtered = self._sort_results(
                filtered,
                filters['sort_by'],
                filters.get('sort_order', 'desc')
            )

        # Pagination
        if 'limit' in filters:
            offset = filters.get('offset', 0)
            filtered = filtered[offset:offset + filters['limit']]

        logger.info(
            f"Applied filters: {len(results)} results -> {len(filtered)} results"
        )
        return filtered

    def _filter_by_date(
        self,
        results: List[Dict[str, Any]],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Filter results by date range."""
        filtered = []

        date_from = filters.get('date_from')
        date_to = filters.get('date_to')

        for result in results:
            try:
                # Parse upload date (assuming ISO format or timestamp)
                upload_date = result.get('upload_date')
                if isinstance(upload_date, str):
                    upload_date = datetime.fromisoformat(upload_date)
                elif isinstance(upload_date, (int, float)):
                    upload_date = datetime.fromtimestamp(upload_date)

                if date_from:
                    if isinstance(date_from, str):
                        date_from = datetime.fromisoformat(date_from)
                    if upload_date < date_from:
                        continue

                if date_to:
                    if isinstance(date_to, str):
                        date_to = datetime.fromisoformat(date_to)
                    if upload_date > date_to:
                        continue

                filtered.append(result)
            except Exception as e:
                logger.warning(f"Error parsing date for result: {e}")
                filtered.append(result)

        return filtered

    def _filter_by_file_type(
        self,
        results: List[Dict[str, Any]],
        file_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Filter results by file type."""
        file_types = [ft.lower().lstrip('.') for ft in file_types]
        filtered = []

        for result in results:
            source = result.get('source', '').lower()
            for file_type in file_types:
                if source.endswith(f'.{file_type}'):
                    filtered.append(result)
                    break

        return filtered

    def _filter_by_relevance(
        self,
        results: List[Dict[str, Any]],
        min_relevance: float
    ) -> List[Dict[str, Any]]:
        """Filter results by relevance score threshold."""
        if not (0 <= min_relevance <= 1):
            logger.warning(f"Invalid relevance threshold: {min_relevance}")
            return results

        return [
            r for r in results
            if r.get('relevance_score', 0) >= min_relevance
        ]

    def _filter_by_tags(
        self,
        results: List[Dict[str, Any]],
        tags: List[str]
    ) -> List[Dict[str, Any]]:
        """Filter results by document tags."""
        filtered = []

        for result in results:
            doc_tags = result.get('tags', [])
            # Check if any requested tag matches
            if any(tag in doc_tags for tag in tags):
                filtered.append(result)

        return filtered

    def _sort_results(
        self,
        results: List[Dict[str, Any]],
        sort_by: str,
        sort_order: str = 'desc'
    ) -> List[Dict[str, Any]]:
        """Sort results by specified field."""
        if sort_by not in self.valid_sort_fields:
            logger.warning(f"Invalid sort field: {sort_by}")
            return results

        field = self.valid_sort_fields[sort_by]
        reverse = sort_order.lower() == 'desc'

        try:
            return sorted(
                results,
                key=lambda x: x.get(field, 0),
                reverse=reverse
            )
        except Exception as e:
            logger.error(f"Error sorting results: {e}")
            return results

    def build_filter_config(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        file_types: Optional[List[str]] = None,
        min_relevance: Optional[float] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = 'relevance',
        sort_order: str = 'desc',
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Build filter configuration dictionary.
        
        Returns a validated filter config.
        """
        config = {}

        if date_from:
            config['date_from'] = date_from
        if date_to:
            config['date_to'] = date_to
        if file_types:
            config['file_types'] = [ft.lower().lstrip('.') for ft in file_types]
        if min_relevance is not None:
            config['min_relevance'] = max(0, min(1, min_relevance))
        if tags:
            config['tags'] = tags
        if sort_by in self.valid_sort_fields:
            config['sort_by'] = sort_by
        if sort_order in ['asc', 'desc']:
            config['sort_order'] = sort_order

        config['limit'] = min(100, max(1, limit))  # 1-100
        config['offset'] = max(0, offset)

        return config


# Singleton instance
filter_service = AdvancedFilterService()
