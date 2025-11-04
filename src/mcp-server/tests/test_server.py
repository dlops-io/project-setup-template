"""Tests for MCP server tools and resources."""


def test_get_model_info():
    """Test get_model_info tool."""
    from src.server import get_model_info

    result = get_model_info("test-model")

    assert result["model_name"] == "test-model"
    assert "status" in result
    assert "version" in result
    assert "accuracy" in result


def test_list_available_models():
    """Test list_available_models tool."""
    from src.server import list_available_models

    result = list_available_models()

    assert isinstance(result, list)
    assert len(result) > 0
    assert all("model_name" in model for model in result)
    assert all("type" in model for model in result)


def test_get_system_health():
    """Test get_system_health tool."""
    from src.server import get_system_health

    result = get_system_health()

    assert result["status"] == "healthy"
    assert "services" in result
    assert "api" in result["services"]
    assert "database" in result["services"]


def test_trigger_model_training():
    """Test trigger_model_training tool."""
    from src.server import trigger_model_training

    result = trigger_model_training(
        model_name="test-model", dataset_path="/data/test.csv", epochs=5
    )

    assert result["model_name"] == "test-model"
    assert result["dataset_path"] == "/data/test.csv"
    assert result["epochs"] == 5
    assert result["status"] == "queued"
    assert "job_id" in result


def test_get_model_metrics():
    """Test get_model_metrics tool."""
    from src.server import get_model_metrics

    result = get_model_metrics(model_name="test-model", metric_type="accuracy")

    assert result["model_name"] == "test-model"
    assert result["metric_type"] == "accuracy"
    assert "value" in result
    assert "all_metrics" in result


def test_get_mlops_config():
    """Test get_mlops_config resource."""
    from src.server import get_mlops_config

    result = get_mlops_config()

    assert isinstance(result, str)
    assert "MLOps Configuration" in result
    assert "Services" in result


def test_get_models_resource():
    """Test get_models_resource resource."""
    from src.server import get_models_resource

    result = get_models_resource()

    assert isinstance(result, str)
    assert "Available Models" in result
    assert len(result) > 0
