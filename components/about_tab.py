from dash import html, dcc

def create_about_tab():
    """Creates the static layout for the 'About & Help' tab."""
    return html.Div(className='card about-container', children=[
        html.H2("About GridAware", className='card-header'),

        html.P(
            "GridAware is a modern, intelligent dashboard that empowers EV owners in Germany to "
            "make cost-optimal charging decisions using real-time electricity prices. By integrating the "
            "Awattar market API, advanced EV configuration, and a clean, data-driven interface, "
            "GridAware delivers actionable, transparent insights — enabling users to maximize savings, "
            "efficiency, and confidence in their energy decisions."
        ),

        html.H3("Design Principles"),
        html.Ul([
            # CORRECTED: Pass a list of children instead of using the '+' operator
            html.Li([
                html.B("Clarity & Transparency:"),
                " All data sources, timestamps, and calculations are clearly presented. No black boxes."
            ]),
            html.Li([
                html.B("User Control:"),
                " Market data is only fetched on user request. All charging parameters are user-configurable."
            ]),
            html.Li([
                html.B("Actionable Insights:"),
                " The dashboard provides clear, unambiguous recommendations to help users save money."
            ])
        ]),
        
        html.H3("Data Source"),
        html.P([
            "Live market prices are sourced directly from the Awattar Germany API. More information can be found on their official documentation page: ",
            html.A("https://www.awattar.de/services/api", href="https://www.awattar.de/services/api", target="_blank")
        ]),

        html.H3("Technology Stack"),
        html.Ul([
            html.Li("Python: The core backend language."),
            html.Li("Dash: The web application framework."),
            html.Li("Plotly: For creating interactive data visualizations."),
            html.Li("Pandas: For efficient data manipulation and analysis."),
            html.Li("Requests: For communicating with the Awattar API.")
        ]),

        html.H3("Planned Roadmap (Future Enhancements)"),
        html.Ul([
            html.Li("CO2-aware charging using grid emission factors."),
            html.Li("User authentication and persistent profiles."),
            html.Li("Solar production integration (PVGIS API)."),
            html.Li("Smart auto-scheduling and notification integration."),
            html.Li("Fully mobile-optimized layout.")
        ]),
        
        html.H3("Author & License"),
        html.P(
            "Developed by Vaijayanth Sheri. This project is open-source and distributed under the MIT License."
        )
    ])