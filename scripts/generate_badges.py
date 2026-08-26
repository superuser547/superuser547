from __future__ import annotations

import shutil
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "assets" / "badges"

BADGES = {
    # Languages
    "python": ("Python", "3776AB", "python"),
    "typescript": ("TypeScript", "3178C6", "typescript"),
    "javascript": ("JavaScript", "323330", "javascript"),
    "sql": ("SQL", "336791", None),
    "powershell": ("PowerShell", "5391FE", "powershell"),
    "bash": ("Bash", "4EAA25", "gnubash"),

    # Backend & Apps
    "fastapi": ("FastAPI", "009688", "fastapi"),
    "flask": ("Flask", "000000", "flask"),
    "uvicorn": ("Uvicorn", "4051B5", None),
    "nodejs": ("Node.js", "339933", "nodedotjs"),
    "pydantic": ("Pydantic", "E92063", "pydantic"),
    "sqlalchemy": ("SQLAlchemy", "D71F00", "sqlalchemy"),
    "streamlit": ("Streamlit", "FF4B4B", "streamlit"),
    "plotly-dash": ("Plotly Dash", "3F4F75", "plotly"),
    "aiogram": ("aiogram", "26A5E4", None),

    # Frontend
    "react": ("React", "20232A", "react"),
    "vite": ("Vite", "646CFF", "vite"),
    "tailwind": ("Tailwind CSS", "06B6D4", "tailwindcss"),
    "lucide": ("Lucide", "F56565", "lucide"),
    "ag-grid": ("AG Grid", "0084E7", None),
    "playwright": ("Playwright", "2EAD33", None),
    "vitest": ("Vitest", "6E9F18", "vitest"),

    # Data
    "pandas": ("Pandas", "150458", "pandas"),
    "numpy": ("NumPy", "013243", "numpy"),
    "plotly": ("Plotly", "3F4F75", "plotly"),
    "jupyter": ("Jupyter", "F37626", "jupyter"),
    "openpyxl": ("OpenPyXL", "217346", None),

    # Databases / Storage
    "postgresql": ("PostgreSQL", "4169E1", "postgresql"),
    "redis": ("Redis", "FF4438", "redis"),
    "sqlite": ("SQLite", "003B57", "sqlite"),
    "mssql": ("Microsoft SQL Server", "CC2927", None),
    "minio": ("MinIO / S3", "C72E49", "minio"),

    # DevOps & Infrastructure
    "docker": ("Docker", "2496ED", "docker"),
    "docker-compose": ("Docker Compose", "2496ED", "docker"),
    "kubernetes": ("Kubernetes", "326CE5", "kubernetes"),
    "terraform": ("Terraform", "844FBA", "terraform"),
    "ansible": ("Ansible", "000000", "ansible"),
    "nginx": ("Nginx", "009639", "nginx"),
    "caddy": ("Caddy", "1F88C0", "caddy"),
    "github-actions": ("GitHub Actions", "2088FF", "githubactions"),
    "gitlab-ci": ("GitLab CI/CD", "FC6D26", "gitlab"),

    # Observability & Security
    "prometheus": ("Prometheus", "E6522C", "prometheus"),
    "grafana": ("Grafana", "F46800", "grafana"),
    "loki": ("Loki", "F46800", None),
    "dependabot": ("Dependabot", "025E8C", "dependabot"),

    # Tools / Platforms
    "git": ("Git", "F05032", "git"),
    "github": ("GitHub", "181717", "github"),
    "gitlab": ("GitLab", "FC6D26", "gitlab"),
    "linux": ("Linux", "333333", "linux"),
    "vscode": ("VS Code", "007ACC", "visualstudiocode"),
    "google-cloud": ("Google Cloud", "4285F4", "googlecloud"),

    # AI
    "openai": ("OpenAI", "101010", None),
    "huggingface": ("Hugging Face", "292D32", "huggingface"),
    "deepseek": ("DeepSeek", "4D6BFE", "deepseek"),
    "codex": ("Codex", "101010", None),
    "github-copilot": ("GitHub Copilot", "181717", "githubcopilot"),
}


def generate_badge(
    name: str,
    label: str,
    color: str,
    logo: str | None,
) -> None:
    badge_content = quote(f"{label}-{color}", safe="")

    params = {
        "style": "for-the-badge",
    }

    if logo:
        params["logo"] = logo
        params["logoColor"] = "white"

    url = (
        f"https://img.shields.io/badge/{badge_content}"
        f"?{urlencode(params)}"
    )

    request = Request(
        url,
        headers={
            "User-Agent": "superuser547-profile-badge-generator/1.0",
        },
    )

    print(f"Generating {name}...")

    with urlopen(request, timeout=30) as response:
        svg = response.read()

    if b"<svg" not in svg:
        raise RuntimeError(f"Invalid SVG returned for {name}")

    (OUTPUT_DIR / f"{name}.svg").write_bytes(svg)


def main() -> None:
    # Regenerate the directory from scratch so removed badges
    # do not remain in the repository.
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True)

    errors: list[str] = []

    for name, (label, color, logo) in BADGES.items():
        try:
            generate_badge(
                name=name,
                label=label,
                color=color,
                logo=logo,
            )
        except Exception as exc:
            errors.append(name)
            print(f"ERROR: {name}: {exc}")

    print()
    print(f"Generated {len(BADGES) - len(errors)}/{len(BADGES)} badges.")

    if errors:
        print("Failed badges:")
        for name in errors:
            print(f"  - {name}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()