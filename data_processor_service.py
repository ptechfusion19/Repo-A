#!/usr/bin/env python3
"""
Data Processor Service
Handles data transformation and processing operations
"""

import json
from typing import Dict, List, Any
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.processed_count = 0
        self.errors = []
    
    def process_batch(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of data items"""
        results = []
        for item in data:
            try:
                processed = self.transform(item)
                results.append(processed)
                self.processed_count += 1
            except Exception as e:
                self.errors.append({"item": item, "error": str(e)})
        return results
    
    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a single data item"""
        return {
            "id": item.get("id"),
            "processed_at": datetime.now().isoformat(),
            "data": item.get("data", {})
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            "processed": self.processed_count,
            "errors": len(self.errors),
            "error_list": self.errors
        }

processor = DataProcessor()
print("Data processor service initialized")

