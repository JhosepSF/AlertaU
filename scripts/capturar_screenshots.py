import time
from pathlib import Path
from playwright.sync_api import sync_playwright

output_dir = Path("docs/screenshots")
output_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(viewport={"width": 1366, "height": 820}, device_scale_factor=1.25)
    page = context.new_page()

    # 1. Portada / Landing
    print("1. Capturando portada...")
    page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "01_portada.png"))

    # 2. Login
    print("2. Capturando login...")
    page.goto("http://127.0.0.1:8000/login/", wait_until="networkidle")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "02_login.png"))

    # Autenticación
    page.fill("#id_username", "admin")
    page.fill("#id_password", "admin123")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    # 3. Dashboard
    print("3. Capturando dashboard...")
    page.screenshot(path=str(output_dir / "03_dashboard.png"))

    # 4. Formulario de predicción individual
    print("4. Capturando formulario de predicción...")
    page.goto("http://127.0.0.1:8000/prediccion/individual/", wait_until="networkidle")
    time.sleep(0.5)
    # Autocompletar con caso 1 demo para que se vea lleno e informativo
    page.click("#btn-cargar-caso-1")
    time.sleep(0.5)
    page.screenshot(path=str(output_dir / "04_formulario_prediccion.png"))

    # 5. Resultado de predicción
    print("5. Capturando resultado de predicción...")
    page.click("button:has-text('Predecir Riesgo')")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "05_resultado_diagnostico.png"))

    # 6. Historial de predicciones
    print("6. Capturando historial...")
    page.goto("http://127.0.0.1:8000/historial/", wait_until="networkidle")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "06_historial.png"))

    # 7. Reportes
    print("7. Capturando reportes...")
    page.goto("http://127.0.0.1:8000/reportes/", wait_until="networkidle")
    time.sleep(1)
    page.screenshot(path=str(output_dir / "07_reportes.png"))

    browser.close()
    print("Todas las capturas se guardaron exitosamente en docs/screenshots/")
