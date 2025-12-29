"""
Performance Optimization Utilities.

Provides caching, memoization, and performance monitoring
for the AI Gym Workout Recommendation System.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
from functools import wraps, lru_cache
from dataclasses import dataclass
from datetime import datetime, timedelta
import time
import logging
from collections import OrderedDict
import hashlib
import json


logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics for operations."""
    operation_name: str
    execution_time: float
    timestamp: datetime
    cache_hit: bool = False
    input_size: int = 0
    output_size: int = 0


class PerformanceMonitor:
    """
    Monitor and track performance metrics.
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize performance monitor.
        
        Args:
            max_history: Maximum number of metrics to keep
        """
        self.metrics: List[PerformanceMetrics] = []
        self.max_history = max_history
        self.operation_stats: Dict[str, Dict[str, Any]] = {}
    
    def record_metric(self, metric: PerformanceMetrics):
        """
        Record a performance metric.
        
        Args:
            metric: Performance metric to record
        """
        self.metrics.append(metric)
        
        # Maintain max history
        if len(self.metrics) > self.max_history:
            self.metrics.pop(0)
        
        # Update statistics
        op_name = metric.operation_name
        if op_name not in self.operation_stats:
            self.operation_stats[op_name] = {
                "total_calls": 0,
                "total_time": 0.0,
                "cache_hits": 0,
                "min_time": float('inf'),
                "max_time": 0.0
            }
        
        stats = self.operation_stats[op_name]
        stats["total_calls"] += 1
        stats["total_time"] += metric.execution_time
        stats["min_time"] = min(stats["min_time"], metric.execution_time)
        stats["max_time"] = max(stats["max_time"], metric.execution_time)
        
        if metric.cache_hit:
            stats["cache_hits"] += 1
    
    def get_statistics(self, operation_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Args:
            operation_name: Specific operation or None for all
        
        Returns:
            Statistics dictionary
        """
        if operation_name:
            if operation_name not in self.operation_stats:
                return {}
            
            stats = self.operation_stats[operation_name].copy()
            if stats["total_calls"] > 0:
                stats["avg_time"] = stats["total_time"] / stats["total_calls"]
                stats["cache_hit_rate"] = stats["cache_hits"] / stats["total_calls"]
            return stats
        
        # Return all statistics
        result = {}
        for op_name, stats in self.operation_stats.items():
            op_stats = stats.copy()
            if stats["total_calls"] > 0:
                op_stats["avg_time"] = stats["total_time"] / stats["total_calls"]
                op_stats["cache_hit_rate"] = stats["cache_hits"] / stats["total_calls"]
            result[op_name] = op_stats
        
        return result
    
    def get_recent_slow_operations(self, threshold_seconds: float = 1.0, count: int = 10) -> List[PerformanceMetrics]:
        """
        Get recent slow operations.
        
        Args:
            threshold_seconds: Threshold for slow operations
            count: Number of operations to return
        
        Returns:
            List of slow operations
        """
        slow_ops = [
            m for m in self.metrics
            if m.execution_time >= threshold_seconds
        ]
        
        # Sort by execution time (slowest first)
        slow_ops.sort(key=lambda m: m.execution_time, reverse=True)
        
        return slow_ops[:count]
    
    def clear_metrics(self):
        """Clear all metrics."""
        self.metrics.clear()
        self.operation_stats.clear()


# Global performance monitor
performance_monitor = PerformanceMonitor()


def monitor_performance(operation_name: str):
    """
    Decorator to monitor function performance.
    
    Args:
        operation_name: Name for the operation
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Record metric
                metric = PerformanceMetrics(
                    operation_name=operation_name,
                    execution_time=execution_time,
                    timestamp=datetime.now(),
                    cache_hit=False
                )
                performance_monitor.record_metric(metric)
                
                # Log slow operations
                if execution_time > 1.0:
                    logger.warning(f"Slow operation: {operation_name} took {execution_time:.2f}s")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Operation {operation_name} failed after {execution_time:.2f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator


class TTLCache:
    """
    Time-To-Live cache with automatic expiration.
    """
    
    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        """
        Initialize TTL cache.
        
        Args:
            ttl_seconds: Time to live in seconds
            max_size: Maximum cache size
        """
        self.ttl = timedelta(seconds=ttl_seconds)
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, datetime] = {}
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired."""
        if key not in self.timestamps:
            return True
        
        age = datetime.now() - self.timestamps[key]
        return age > self.ttl
    
    def _evict_if_needed(self):
        """Evict oldest entries if cache is full."""
        while len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        if key not in self.cache:
            return None
        
        if self._is_expired(key):
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def set(self, key: str, value: Any):
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self._evict_if_needed()
        
        self.cache[key] = value
        self.timestamps[key] = datetime.now()
        self.cache.move_to_end(key)
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        self.timestamps.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)


class SmartCache:
    """
    Intelligent caching system with multiple strategies.
    """
    
    def __init__(self):
        """Initialize smart cache."""
        # Different caches for different data types
        self.exercise_cache = TTLCache(ttl_seconds=3600, max_size=100)  # 1 hour
        self.plan_cache = TTLCache(ttl_seconds=1800, max_size=500)  # 30 minutes
        self.search_cache = TTLCache(ttl_seconds=600, max_size=1000)  # 10 minutes
        
        self.cache_hits = 0
        self.cache_misses = 0
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generate cache key from arguments.
        
        Args:
            prefix: Cache key prefix
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Cache key string
        """
        # Create deterministic string from arguments
        key_data = {
            "args": str(args),
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True)
        
        # Hash for consistent key length
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{prefix}:{key_hash}"
    
    def get_from_cache(self, cache_type: str, *args, **kwargs) -> Optional[Any]:
        """
        Get value from appropriate cache.
        
        Args:
            cache_type: Type of cache (exercise, plan, search)
            *args: Key generation arguments
            **kwargs: Key generation arguments
        
        Returns:
            Cached value or None
        """
        cache_map = {
            "exercise": self.exercise_cache,
            "plan": self.plan_cache,
            "search": self.search_cache
        }
        
        cache = cache_map.get(cache_type)
        if not cache:
            return None
        
        key = self._generate_key(cache_type, *args, **kwargs)
        value = cache.get(key)
        
        if value is not None:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        return value
    
    def set_in_cache(self, cache_type: str, value: Any, *args, **kwargs):
        """
        Set value in appropriate cache.
        
        Args:
            cache_type: Type of cache
            value: Value to cache
            *args: Key generation arguments
            **kwargs: Key generation arguments
        """
        cache_map = {
            "exercise": self.exercise_cache,
            "plan": self.plan_cache,
            "search": self.search_cache
        }
        
        cache = cache_map.get(cache_type)
        if not cache:
            return
        
        key = self._generate_key(cache_type, *args, **kwargs)
        cache.set(key, value)
    
    def get_hit_rate(self) -> float:
        """Get cache hit rate."""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "hit_rate": self.get_hit_rate(),
            "exercise_cache_size": self.exercise_cache.size(),
            "plan_cache_size": self.plan_cache.size(),
            "search_cache_size": self.search_cache.size()
        }
    
    def clear_all(self):
        """Clear all caches."""
        self.exercise_cache.clear()
        self.plan_cache.clear()
        self.search_cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0


# Global smart cache instance
smart_cache = SmartCache()


def cached(cache_type: str):
    """
    Decorator for automatic caching.
    
    Args:
        cache_type: Type of cache to use
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get from cache
            cached_value = smart_cache.get_from_cache(cache_type, *args, **kwargs)
            
            if cached_value is not None:
                # Record cache hit
                metric = PerformanceMetrics(
                    operation_name=func.__name__,
                    execution_time=0.0,
                    timestamp=datetime.now(),
                    cache_hit=True
                )
                performance_monitor.record_metric(metric)
                
                return cached_value
            
            # Execute function
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Cache result
            smart_cache.set_in_cache(cache_type, result, *args, **kwargs)
            
            # Record metric
            metric = PerformanceMetrics(
                operation_name=func.__name__,
                execution_time=execution_time,
                timestamp=datetime.now(),
                cache_hit=False
            )
            performance_monitor.record_metric(metric)
            
            return result
        
        return wrapper
    return decorator


class BatchProcessor:
    """
    Process items in batches for better performance.
    """
    
    @staticmethod
    def process_in_batches(
        items: List[Any],
        process_func: Callable,
        batch_size: int = 100
    ) -> List[Any]:
        """
        Process items in batches.
        
        Args:
            items: Items to process
            process_func: Function to apply to each batch
            batch_size: Size of each batch
        
        Returns:
            List of processed results
        """
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = process_func(batch)
            results.extend(batch_results)
        
        return results


class LazyLoader:
    """
    Lazy load data only when needed.
    """
    
    def __init__(self, load_func: Callable):
        """
        Initialize lazy loader.
        
        Args:
            load_func: Function to load data
        """
        self.load_func = load_func
        self._data = None
        self._loaded = False
    
    @property
    def data(self) -> Any:
        """Get data, loading if necessary."""
        if not self._loaded:
            self._data = self.load_func()
            self._loaded = True
        return self._data
    
    def reload(self):
        """Force reload of data."""
        self._loaded = False
        self._data = None


class PerformanceOptimizer:
    """
    Central performance optimization utilities.
    """
    
    @staticmethod
    def optimize_list_operations(items: List[Any]) -> List[Any]:
        """
        Optimize list operations using generators where possible.
        
        Args:
            items: List of items
        
        Returns:
            Optimized list
        """
        # Use list comprehension instead of loops
        # Already optimized in most places
        return items
    
    @staticmethod
    def optimize_filtering(
        items: List[Any],
        filters: List[Callable]
    ) -> List[Any]:
        """
        Optimize multiple filtering operations.
        
        Args:
            items: Items to filter
            filters: List of filter functions
        
        Returns:
            Filtered items
        """
        # Combine filters to reduce iterations
        def combined_filter(item):
            return all(f(item) for f in filters)
        
        return [item for item in items if combined_filter(item)]
    
    @staticmethod
    def precompute_common_values(func: Callable) -> Callable:
        """
        Precompute values that don't change.
        
        Args:
            func: Function to optimize
        
        Returns:
            Optimized function
        """
        # Use lru_cache for memoization
        return lru_cache(maxsize=128)(func)
    
    @staticmethod
    def get_performance_report() -> Dict[str, Any]:
        """
        Get comprehensive performance report.
        
        Returns:
            Performance report
        """
        return {
            "monitor": performance_monitor.get_statistics(),
            "cache": smart_cache.get_statistics(),
            "slow_operations": [
                {
                    "operation": m.operation_name,
                    "time": m.execution_time,
                    "timestamp": m.timestamp.isoformat()
                }
                for m in performance_monitor.get_recent_slow_operations()
            ]
        }


# Optimize data loading
@lru_cache(maxsize=1)
def get_cached_exercises():
    """Get cached exercise list (singleton pattern)."""
    from src.infrastructure.data.data_loader import DataLoader
    loader = DataLoader()
    return loader.load_exercises()


# Export optimization utilities
__all__ = [
    'PerformanceMonitor',
    'performance_monitor',
    'monitor_performance',
    'TTLCache',
    'SmartCache',
    'smart_cache',
    'cached',
    'BatchProcessor',
    'LazyLoader',
    'PerformanceOptimizer',
    'get_cached_exercises'
]
