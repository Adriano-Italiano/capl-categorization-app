import pandas as pd
import gradio as gr
from fastapi import FastAPI

# Wczytaj dane
df = pd.read_excel("Categorization_tool_CAPL.xlsx", sheet_name="tool", engine="openpyxl")

def znajdz_kategorie_pim(front_kategoria):
    df2 = df[df['front_category_leaf_name'].str.lower() == front_kategoria.lower()]
    if not df2.empty:
        return df2[['pim_category_id', 'pim_category_full_path']].drop_duplicates().reset_index(drop=True)
    else:
        return pd.DataFrame({
            "pim_category_id": ["Nie znaleziono"],
            "pim_category_full_path": ["Brak danych"]
        })

with gr.Blocks() as demo:
    gr.Markdown("## 🔍 Narzędzie do mapowania kategorii")
    wej = gr.Textbox(label="Wprowadź kategorię")
    btn = gr.Button("Szukaj")
    out = gr.Dataframe(headers=["pim_category_id", "pim_category_full_path"])
    btn.click(fn=znajdz_kategorie_pim, inputs=wej, outputs=out)
    gr.Image(value="cat_app_file.jpg", label="Instrukcja")

# ✅ FastAPI app z Gradio
app = FastAPI()
app = gr.mount_gradio_app(app, demo, path="/")
