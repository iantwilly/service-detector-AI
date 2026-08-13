## AI Cloud Cost Detective - Request Flow

```
①  User ─·─·─► React ─·─·─► FastAPI Auth ─·─·─► JWT (GCP PostgreSQL)

②  User selects Project ─·─·─► Python Backend

③  Python ─·─·─► GCP CLI ─·─·─► Fetches all resources in RG

④  Python ─·─·─► FastAPI WebSocket ─·─·─► React (live progress)

⑤  Python ─·─·─► OpenAI API ─·─·─► Cost analysis

⑥  Python ─·─·─► GCP PostgreSQL ─·─·─► Stores analysis history

⑦  React ◄·─·─·─ Final report with suggestions & fixes
```
