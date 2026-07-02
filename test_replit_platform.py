from unittest import result

import pytest
from replit_platform import ReplitPlatform # type: ignore

# ====================================
# ФИКСТУРЫ (Pytest Fixtures)
# ====================================
@pytest.fixture
def authenticated_platform():
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")
    return platform


# ====================================
# ТЕСТЫ
# ====================================

# Тест на успешную аутентификацию
def test_authentication_success(authenticated_platform):
    # Act (дія)
    result = authenticated_platform.authenticate("replit123")

    # Assert (перевірка)
    assert result == "Автентифікація успішна"
    assert authenticated_platform.authenticated is True

    # EP: валідний пароль
    # Позитивний тест


def test_authenticate_short_password():
    # Arrange
    platform = ReplitPlatform("user")

    # Act + Assert
    with pytest.raises(ValueError):
        platform.authenticate("123")

    # BVA: пароль менше мінімальних 6 символів
    # Негативний тест



def test_authenticate_wrong_password():

    # Arrange
    platform = ReplitPlatform("user")

    # Act + Assert
    with pytest.raises(PermissionError):
        platform.authenticate("wrong123")

    # EP: невірний пароль
    # Негативний тест



# ==============================
# ТЕСТИ create_project()
# ==============================


def test_create_project_python():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    # Act
    result = platform.create_project(
        "MyApp",
        "Python"
    )

    # Assert
    assert result == "Проєкт MyApp створено"
    assert "MyApp" in platform.projects

    # EP: підтримувана мова програмування
    # Позитивний тест



def test_create_project_duplicate():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    platform.create_project(
        "MyApp",
        "Python"
    )

    # Act + Assert
    with pytest.raises(ValueError):
        platform.create_project(
            "MyApp",
            "Python"
        )

    # EP: дублювання назви проєкту
    # Негативний тест



def test_create_project_empty_name(authenticated_platform):
    # Arrange
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        authenticated_platform.create_project("", "Python")

    # Додаткова перевірка повідомлення помилки (точний Assert)
    assert "Назва проєкту не може бути порожньою" in str(exc_info.value)

    # BVA: порожня назва проєкту
    # Негативний тест



def test_create_project_unsupported_language():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    # Act + Assert
    with pytest.raises(ValueError):
        platform.create_project(
            "App",
            "Ruby"
        )

    # EP: непідтримувана мова
    # Негативний тест



# ==============================
# ТЕСТИ generate_ai_code()
# ==============================


def test_generate_ai_code_success(authenticated_platform):
    # Arrange
    authenticated_platform.create_project("AIProject", "Python")

    # Act
    code = authenticated_platform.generate_ai_code("AIProject", "створити калькулятор")

    # Assert
    assert "Код створено ШI" in code
    assert authenticated_platform.projects["AIProject"]["code"] != ""

    # EP: коректний опис задачі
    # Позитивний тест



def test_generate_ai_code_empty_task():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    platform.create_project(
        "AIProject",
        "Python"
    )

    # Act + Assert
    with pytest.raises(ValueError):
        platform.generate_ai_code("")

    # BVA: порожній рядок
    # Негативний тест



# ==============================
# ТЕСТИ run_project()
# ==============================


def test_run_project_success():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    platform.create_project(
        "TestApp",
        "Python"
    )

    platform.generate_ai_code(
        "створити програму"
    )

    # Act
    result = platform.run_project()

    # Assert
    assert "Процес виконання" in result
    assert platform.projects["TestApp"]["status"] == "running"

    # EP: проєкт має код
    # Позитивний тест



def test_run_project_without_code():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    platform.create_project(
        "EmptyApp",
        "Python"
    )

    # Act + Assert
    with pytest.raises(RuntimeError):
        platform.run_project()

    # EP: запуск проєкту без коду
    # Негативний тест



# ==============================
# ТЕСТИ deploy_application()
# ==============================


def test_deploy_application_success():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    platform.create_project(
        "WebApp",
        "Python"
    )

    platform.generate_ai_code(
        "створити сайт"
    )

    platform.run_project()

    # Act
    result = platform.deploy_application()

    # Assert
    assert "успішно розгорнуто" in result
    assert platform.projects["WebApp"]["status"] == "deployed"

    # EP: правильна послідовність станів
    # Позитивний тест



def test_deploy_before_run():

    # Arrange
    platform = ReplitPlatform("user")
    platform.authenticate("replit123")

    platform.create_project(
        "App",
        "Python"
    )

    # Act + Assert
    with pytest.raises(RuntimeError):
        platform.deploy_application()

    # BVA: перехід зі стану created
    # Негативний тест