"""
Asynchronous Event Bus for FacilityOps Event-Driven Architecture.
Supports topic-based pub/sub, pattern wildcards, and audit buffering.
"""

import asyncio
import fnmatch
import logging
import time
from typing import Dict, List, Callable, Any, Set
from datetime import datetime

logger = logging.getLogger("facilityops.eventbus")

class Event:
    def __init__(self, topic: str, payload: Dict[str, Any], source: str = "system"):
        self.id = f"EVT-{int(time.time()*1000)%1000000}"
        self.topic = topic
        self.payload = payload
        self.source = source
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "payload": self.payload,
            "source": self.source,
            "timestamp": self.timestamp
        }

class EventBus:
    def __init__(self, max_history: int = 500):
        self._subscribers: Dict[str, Set[Callable[[Event], Any]]] = {}
        self._history: List[Event] = []
        self._max_history = max_history
        self._lock = asyncio.Lock()

    def subscribe(self, topic_pattern: str, handler: Callable[[Event], Any]):
        """Subscribe a callable/coroutine to a topic pattern (e.g. 'energy.*')."""
        if topic_pattern not in self._subscribers:
            self._subscribers[topic_pattern] = set()
        self._subscribers[topic_pattern].add(handler)
        logger.debug(f"Subscribed handler to pattern '{topic_pattern}'")

    def unsubscribe(self, topic_pattern: str, handler: Callable[[Event], Any]):
        """Unsubscribe handler from a topic pattern."""
        if topic_pattern in self._subscribers:
            self._subscribers[topic_pattern].discard(handler)

    async def publish(self, topic: str, payload: Dict[str, Any], source: str = "system") -> Event:
        """Publish an event to all matching subscribers."""
        event = Event(topic=topic, payload=payload, source=source)
        
        # Add to history
        async with self._lock:
            self._history.insert(0, event)
            if len(self._history) > self._max_history:
                self._history = self._history[:self._max_history]

        # Find matching subscribers
        matched_handlers = set()
        for pattern, handlers in self._subscribers.items():
            if pattern == "#" or fnmatch.fnmatch(topic, pattern):
                matched_handlers.update(handlers)

        # Dispatch handlers concurrently
        for handler in matched_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(event))
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for topic '{topic}': {e}", exc_info=True)

        return event

    async def get_history(self, limit: int = 50, topic_filter: str = None) -> List[Dict[str, Any]]:
        """Retrieve recent events buffer."""
        async with self._lock:
            events = self._history
            if topic_filter:
                events = [e for e in events if fnmatch.fnmatch(e.topic, topic_filter)]
            return [e.to_dict() for e in events[:limit]]

# Global Event Bus Singleton
event_bus = EventBus()
