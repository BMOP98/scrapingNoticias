import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class DataProcessor:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path, parse_dates=["Fecha"])

    def generar_graficos(self):
        # **Gráfico 1: Frecuencia de incidentes por mes**
        self.df["Mes"] = self.df["Fecha"].dt.to_period("M")
        count_data = self.df["Mes"].value_counts().sort_index()
        fig1 = px.bar(x=count_data.index.astype(str), y=count_data.values, title="")

        # **Gráfico 2: Línea de tiempo de eventos**
        fig2 = px.line(self.df, x="Fecha", y=self.df.index, text="Título", title="", markers=True)
        fig2.update_traces(textposition="top center")

        # **Gráfico 3: Nube de Palabras de Títulos**
        text = " ".join(self.df["Título"].tolist())
        wordcloud = WordCloud(max_font_size=None, background_color='white').generate(text)
        fig3_plt = plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        img_buf = BytesIO()
        fig3_plt.savefig(img_buf, format='png')
        img_str = base64.b64encode(img_buf.getvalue()).decode('utf-8')
        fig3 = html.Img(src='data:image/png;base64,' + img_str, style={'width': '100%'})

        # **Gráfico 4: Dispersión de Incidentes en el Tiempo**
        fig4 = px.scatter(self.df, x="Fecha", y=self.df.index, title="")

        return fig1, fig2, fig3, fig4

    def obtener_ultimas_novedades(self, n=10):
        ultimas_novedades = self.df.sort_values("Fecha", ascending=False).head(n)
        ultimas_novedades['Mes'] = ultimas_novedades['Mes'].astype(str)  # Convertir Period a str
        return ultimas_novedades


# Uso de la clase
data_processor = DataProcessor("./elCOmercio/datos_scrapeados.csv")  # Reemplaza con tu ruta
fig1, fig2, fig3, fig4 = data_processor.generar_graficos()
ultimas_novedades = data_processor.obtener_ultimas_novedades(4)

# Iniciar aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Br(),
    html.H1("Lahares Río Upano", className="text-center mb-4", style={"color": "#343a40"}),  # Darker heading
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H2("Número Total de Noticias", className="text-center", style={"color": "#007bff"}),  # Blue title
                    html.P(
                        f"Se encontraron {len(data_processor.df)} noticias en total.",
                        className="card-text text-center",
                        style={"font-size": "1.2rem"}  # Larger font
                    ),
                ])
            ], color="light", outline=True),  # Light card with outline
            width=12,
            className="mb-4"  # Margin bottom
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H2("Últimas Novedades", style={"color": "#007bff"}),  # Blue title
                    dash_table.DataTable(
                        data=ultimas_novedades.to_dict('records'),
                        columns=[{"name": "Fecha", "id": "Fecha"}, {"name": "Título", "id": "Título"}],
                        style_cell={'textAlign': 'left', 'padding': '8px'},  # Add padding
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'},  # Lighter background
                            {'if': {'row_index': 'even'}, 'backgroundColor': '#ffffff'} # White background for even rows
                        ],
                        style_header={'backgroundColor': '#007bff', 'color': 'white', 'fontWeight': 'bold', 'padding': '8px'}, # Blue header
                        page_size=4,  # Pagination
                        style_table={'overflowX': 'auto'} # Horizontal scroll if needed
                    )
                ])
            ], color="light", outline=True),  # Light card with outline
            width=12,
            className="mb-4"  # Margin bottom
        ),
    ]),

    

    # Gráficos con mejor diseño
    dbc.Row([
        dbc.Col(html.H2("Casos Encontrados", style={"color": "#007bff"}), width=12, className="mb-2"),  # Blue title, margin bottom
        dbc.Col(dcc.Graph(figure=fig1.update_layout(title_font=dict(size=20),  plot_bgcolor="#f8f9fa", paper_bgcolor="#f8f9fa"), style={'height': '600px', 'width': '100%'}), width=12, className="mb-4"), # Updated layout, margin bottom
    ]),
    dbc.Row([
        dbc.Col(html.H2("Linea de Tiempo", style={"color": "#007bff"}), width=12, className="mb-2"),  # Blue title, margin bottom
        dbc.Col(dcc.Graph(figure=fig2.update_layout(title_font=dict(size=20), plot_bgcolor="#f8f9fa", paper_bgcolor="#f8f9fa"), style={'height': '600px', 'width': '100%'}), width=12, className="mb-4"), # Updated layout, margin bottom
    ]),
    dbc.Row([
        dbc.Col(html.H2("Nube de Palabras", style={"color": "#007bff"}), width=12, className="mb-2"),  # Blue title, margin bottom
        dbc.Col(fig3, width=12, className="mb-4"),  # Margin bottom
    ]),
    dbc.Row([
        dbc.Col(html.H2("Dispersión de Incidentes en el Tiempo", style={"color": "#007bff"}), width=12, className="mb-2"),  # Blue title, margin bottom
        dbc.Col(dcc.Graph(figure=fig4.update_layout(title_font=dict(size=20), plot_bgcolor="#f8f9fa", paper_bgcolor="#f8f9fa"), style={'height': '600px', 'width': '100%'}), width=12, className="mb-4"), # Updated layout, margin bottom
    ]),

    dbc.Row([
    dbc.Col(html.H2("Analis con Redes Sociales", style={"color": "#007bff"}), width=12, className="mb-2"),  # Título azul, margen inferior
    dbc.Col(
        html.A(
            html.Button("Ir", style={"color": "white", "backgroundColor": "#007bff", "border": "none", "padding": "10px 20px", "cursor": "pointer"}),
            href="https://black-rock-0969ed51e.6.azurestaticapps.net/", target="_blank"  # Redirige al link en una nueva pestaña
        ),
        width=12, className="mb-4"
    ),
]),
], fluid=True, style={"backgroundColor": "#f8f9fa", "padding": "20px"}) # Light background for the whole dashboard, padding

if __name__ == "__main__":
    app.run_server(debug=True)