# EduTrack AI

Aplicativo academico em Streamlit para organizar estudos, tarefas, notas, calendario, professores e assistente de estudos.

## Como rodar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

- `app.py`: ponto principal do sistema.
- `assets/images`: imagens da interface.
- `assets/logos`: logos e marcas.
- `pages`: telas do app.
- `components`: componentes reutilizaveis.
- `utils`: estilos, sessao e autenticacao.
- `services`: ponto de integracao com dados/API.
