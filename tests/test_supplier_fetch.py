import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from services.supplier_fetch_service import fetch_one_async, fetch_all_concurrently, fetch_all_sequentially
from utils.config import ENDPOINTS


@patch("services.supplier_fetch_service.requests.get")
@patch("services.supplier_fetch_service.save_json")
def test_sequential_calls_each_endpoint(mock_save, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"id": 1}]
    mock_get.return_value = mock_response

    fetch_all_sequentially()

    assert mock_get.call_count == len(ENDPOINTS)

@patch("services.supplier_fetch_service.requests.get")
@patch("services.supplier_fetch_service.save_json")
def test_sequential_saves_each_endpoint(mock_save, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    fetch_all_sequentially()

    assert mock_save.call_count == len(ENDPOINTS)

@patch("services.supplier_fetch_service.requests.get")
@patch("services.supplier_fetch_service.save_json")
def test_sequential_saves_correct_filenames(mock_save, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    fetch_all_sequentially()

    saved_filenames = [call.args[0] for call in mock_save.call_args_list]
    for name in ENDPOINTS:
        assert f"{name}.json" in saved_filenames

@patch("services.supplier_fetch_service.requests.get")
def test_sequential_raises_on_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="HTTP Error"):
        fetch_all_sequentially()


@pytest.mark.asyncio
@patch("services.supplier_fetch_service.save_json")
async def test_concurrent_saves_each_endpoint(mock_save):
    mock_data = [{"id": 1}]

    async def mock_json():
        return mock_data

    mock_response = MagicMock()
    mock_response.json = mock_json
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)

    mock_session = MagicMock()
    mock_session.get = MagicMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        await fetch_all_concurrently()

    assert mock_save.call_count == len(ENDPOINTS)

@pytest.mark.asyncio
@patch("services.supplier_fetch_service.save_json")
async def test_concurrent_saves_correct_filenames(mock_save):
    mock_data = []

    async def mock_json():
        return mock_data

    mock_response = MagicMock()
    mock_response.json = mock_json
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)

    mock_session = MagicMock()
    mock_session.get = MagicMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("aiohttp.ClientSession", return_value=mock_session):
        await fetch_all_concurrently()

    saved_filenames = [call.args[0] for call in mock_save.call_args_list]
    for name in ENDPOINTS:
        assert f"{name}.json" in saved_filenames
