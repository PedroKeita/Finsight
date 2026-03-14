from unittest.mock import patch, MagicMock
from scheduler import scheduled_collect, start_scheduler

def test_scheduled_collect_executa():
    with patch("scheduler.collect_all") as mock_collect, \
         patch("scheduler.invalidate_cache") as mock_cache:
        scheduled_collect()
        mock_collect.assert_called_once()
        mock_cache.assert_called_once()

def test_start_scheduler_retorna_scheduler():
    with patch("scheduler.BackgroundScheduler") as mock_scheduler:
        instance = MagicMock()
        mock_scheduler.return_value = instance
        result = start_scheduler()
        instance.start.assert_called_once()